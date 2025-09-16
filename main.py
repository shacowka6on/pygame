import pygame
import settings
import spritesheet

pygame.init()

clock = pygame.time.Clock()

sprite_sheet_image = pygame.image.load('pygame/assets/blastalot-wings-alpha.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

animation_list = []
animation_steps = [1,1,1,6] #idle,jump,fall,run1-6
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 100
step_counter = 0
frame = 0


for animation in animation_steps:
    temp_img_list = []
    for i in range(animation):
        x = step_counter * settings.FRAME_WIDTH
        y = 0 
        temp_img_list.append(sprite_sheet.get_image(x,y,settings.FRAME_WIDTH,settings.FRAME_HEIGHT,settings.SCALE))
        step_counter += 1
    animation_list.append(temp_img_list)

GAME_RUNNING = True
dt = 0
player_pos = pygame.Vector2(100, 600)
facing_right = True

jumping = False
Y_GRAVITY = 1.1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT


while GAME_RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUNNING = False

    settings.screen.fill(settings.BACKGROUND_COLOR)

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        if frame >= len(animation_list[action]):
            frame = 0
        last_update = current_time

    #-------Physics--------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 250 * dt
        facing_right = False
    if keys[pygame.K_d]:
        player_pos.x += 250 * dt
        facing_right = True
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True

    if jumping:
        player_pos.y -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT

    #-------Handles animation------- 
    if jumping:
        if Y_VELOCITY > 0:
            action = 1
        else:
            action = 2
    elif keys[pygame.K_a] or keys[pygame.K_d]:
        action = 3
    else:
        action = 0

    frame = min(frame, len(animation_list[action]) - 1)
    frame_img = animation_list[action][frame]
    if not facing_right:
        frame_img = pygame.transform.flip(frame_img, True, False)

    frame_rect = frame_img.get_rect(center=player_pos)
    settings.screen.blit(frame_img,frame_rect)

    #-----End of animation code------

    pygame.display.flip()

    dt = clock.tick(60) / 1000  

pygame.quit()