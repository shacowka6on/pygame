import random
import pygame
from settings import *
from spritesheet import SpriteSheet

ANIMATION_MAP = {
    "WANDER": "walk",
    "CHASE":  "walk",
    "ATTACK": "attack",
    "HURT":   "hurt",
    "DEATH":  "death",
}

ANIMATION_OFFSETS = {
    True:  {"demon": (-90,  -150), "lizard": (-100, -120)},
    False: {"demon": (-140, -150), "lizard": (-130, -120)},
}

STATE_COLORS = {
    "WANDER": (0,   255, 0),
    "CHASE":  (255, 255, 0),
    "ATTACK": (255, 0,   0),
    "HURT":   (10,  10,  10),
    "DEATH":  (0,   0,   0),
}

class Enemy:
    def __init__(self, x, y, type):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, 60, 80)

        self.type = type
        self.health = ENEMY_HEALTH
        self.speed = ENEMY_SPEED
        self.state = "WANDER"

        self.detection_radius = ENEMY_DETECTION_RANGE
        self.attack_radius = ENEMY_ATTACK_RANGE
        self.attack_cooldown = ENEMY_ATTACK_COOLDOWN
        self.last_attack = 0

        self.is_grounded = False
        self.jumping = False
        self.facing_right = True
        self.wander_direction = pygame.Vector2(random.choice([-1, 1]), 0)
        self.wander_timer = 0

        self.sprites = self._load_sprites()
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

    # ------------------------------------------------------------------ state

    def _set_state(self, new_state):
        if self.state == "DEATH":
            return  # dead enemies ignore all state changes
        self.state = new_state

    def decide_state(self, player):
        if self.state in ("DEATH", "HURT"):
            return

        distance = (player.pos - self.pos).length()

        if distance <= self.attack_radius:
            self.state = "ATTACK"
        elif distance <= self.detection_radius:
            self.state = "CHASE"
        else:
            self.state = "WANDER"

    def take_damage(self):
        if self.state == "DEATH":
            return False  # already dead, ignore hits

        self.health -= BULLET_DAMAGE

        if self.health <= 0:
            self.health = 0
            self.state = "DEATH"
            self.current_frame = 0
            self.animation_timer = 0
            return True

        self.state = "HURT"
        self.current_frame = 0
        self.animation_timer = 0
        return False

    # ----------------------------------------------------------------- movement

    def apply_gravity(self, dt):
        if not self.is_grounded:
            self.velocity.y += GRAVITY * dt + 1

        self.pos.y += GRAVITY * dt + 1

        if self.pos.y >= FLOOR:
            self.pos.y = FLOOR
            self.is_grounded = True
            self.jumping = False
            self.velocity.y = 0

    def _face_toward(self, target_x):
        diff = target_x - self.pos.x
        if abs(diff) > 10:
            self.facing_right = diff > 0

    def wander(self, dt):
        self.wander_timer += dt
        if self.wander_timer >= random.uniform(2.0, 4.0):
            self.wander_direction.x = random.choice([-1, 1])
            self.wander_timer = 0

        self.velocity.x = self.wander_direction.x * self.speed * 0.5 * dt
        if self.velocity.x != 0:
            self.facing_right = self.velocity.x > 0

    def chase_player(self, player, dt):
        diff = player.pos.x - self.pos.x
        if abs(diff) > 10:
            self.velocity.x = (diff / abs(diff)) * self.speed * dt
            self._face_toward(player.pos.x)
        else:
            self.velocity.x = 0

    def attack_player(self, player):
        self.velocity.x = 0
        self._face_toward(player.pos.x)

        now = pygame.time.get_ticks()
        if now - self.last_attack >= self.attack_cooldown:
            player.take_damage()
            self.last_attack = now

    def handle_enemy_platform_collisions(self, platforms):
        self.is_grounded = False
        for platform in platforms:
            if platform.check_collision(self.rect):
                is_grounded = platform.handle_collision(self, self.rect)
                if is_grounded:
                    self.is_grounded = True

    # ------------------------------------------------------------------ update

    def update(self, player, dt):
        self.apply_gravity(dt)

        if self.state not in ("HURT", "DEATH"):
            self.decide_state(player)

        if self.state == "WANDER":
            self.wander(dt)
        elif self.state == "CHASE":
            self.chase_player(player, dt)
        elif self.state == "ATTACK":
            self.attack_player(player)
        elif self.state in ("HURT", "DEATH"):
            self.velocity.x = 0
            if self.state == "DEATH":
                self.velocity.y = 0

        new_animation = ANIMATION_MAP.get(self.state, "idle")
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
            self.animation_timer = 0

        self.update_animation(dt)

        if self.state != "DEATH":
            self.pos.x = max(0, min(self.pos.x, WIDTH - self.rect.width))
            self.pos.x += self.velocity.x
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer < self.animation_speed:
            return

        self.animation_timer = 0
        frames = self.sprites[self.current_animation]

        if self.current_animation == "hurt":
            if self.current_frame >= len(frames) - 1:
                self.state = "WANDER"  # hurt animation finished, back to wandering
            else:
                self.current_frame += 1

        elif self.current_animation == "death":
            if self.current_frame < len(frames) - 1:
                self.current_frame += 1  # freeze on last frame when done

        else:
            self.current_frame = (self.current_frame + 1) % len(frames)

    # ------------------------------------------------------------------- draw

    def draw(self, screen):
        if self.sprites[self.current_animation]:
            img = self.sprites[self.current_animation][self.current_frame]

            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)

            offsets = ANIMATION_OFFSETS[self.facing_right].get(self.type, (0, 0))
            screen.blit(img, (self.rect.centerx + offsets[0], self.rect.centery + offsets[1]))

        self._draw_healthbar(screen)

        # state indicator dot (debug)
        pygame.draw.circle(screen, STATE_COLORS[self.state],
                           (int(self.pos.x + 15), int(self.pos.y - 20)), 3)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def _draw_healthbar(self, screen):
        bar_x, bar_y = self.pos.x, self.pos.y - 10
        bar_w, bar_h = 30, 5

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))

        ratio = self.health / ENEMY_HEALTH
        fill_w = max(0, int(bar_w * ratio))
        if fill_w:
            color = (0, 255, 0) if ratio > 0.6 else (255, 255, 0) if ratio > 0.3 else (255, 0, 0)
            pygame.draw.rect(screen, color, (bar_x, bar_y, fill_w, bar_h))

    # ------------------------------------------------------------------ setup

    def _load_sprites(self):
        prefix_map = {"A": "attack", "D": "death", "H": "hurt", "I": "idle", "W": "walk"}
        sprites = {key: [] for key in prefix_map.values()}

        for filename, image in SpriteSheet.load_enemy_images(self.type).items():
            scaled = pygame.transform.scale(image, (256, 256))
            key = prefix_map.get(filename[0])
            if key:
                sprites[key].append(scaled)

        return sprites