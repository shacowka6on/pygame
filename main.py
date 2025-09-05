import pygame
import spritesheet

pygame.init()

clock = pygame.time.Clock()

sprite_sheet_image = pygame.image.load('assets/blastalot-wings-alpha.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

animation_list = []
animation_steps = [1,1,1,6] #idle,jump,fall,run1-6
action = 3
last_update = pygame.time.get_ticks()
animation_cooldown = 100
step_counter = 0
frame = 0


frame_width = 44
frame_height = 44
scale = 2

for animation in animation_steps:
    temp_img_list = []
    for i in range(animation):
        x = step_counter * frame_width
        y = 0 
        temp_img_list.append(sprite_sheet.get_image(x,y,frame_width,frame_height,scale))
        step_counter += 1
    animation_list.append(temp_img_list)

running = True
dt = 0
player_pos = pygame.Vector2(100, 600)
facing_right = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        if frame >= len(animation_list[action]):
            frame = 0
        last_update = current_time


    # RENDER YOUR GAME HERE
    # pygame.draw.circle(screen, "cyan", player_pos, 30)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 250 * dt
        facing_right = False
    if keys[pygame.K_d]:
        player_pos.x += 250 * dt
        facing_right = True

    if keys[pygame.K_a] or keys[pygame.K_d]:
        action = 3
    else:
        action = 0

    frame = min(frame, len(animation_list[action]) - 1)
    frame_img = animation_list[action][frame]
    if not facing_right:
        frame_img = pygame.transform.flip(frame_img, True, False)

    frame_rect = frame_img.get_rect(center=player_pos)
    screen.blit(frame_img,frame_rect)

    pygame.display.flip()

    dt = clock.tick(60) / 1000  

pygame.quit()