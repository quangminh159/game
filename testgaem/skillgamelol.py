import pygame
import random
import sys
import math

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Skill Game LOL')

WHITE = (255, 255, 255)

font = pygame.font.Font(None, 36)

try:
    background_image = pygame.image.load('background.png')
    background_image = pygame.transform.scale(
        background_image, (screen_width, screen_height))
    catlyn_image = pygame.image.load('catlyn.png')
    catlyn_image = pygame.transform.scale(catlyn_image, (70, 70))
    linh_game_image = pygame.image.load('gromp.png')
    linh_game_image = pygame.transform.scale(linh_game_image, (50, 50))
except Exception as e:
    print(f"Lỗi tải tài nguyên: {e}")
    sys.exit()

catlyn_rect = catlyn_image.get_rect()
catlyn_rect.center = (screen_width // 2, screen_height - 100)

bullets = []  # Mỗi viên đạn sẽ lưu vị trí và hướng di chuyển
bullet_speed = 11
bullet_timer = 0  # Bộ đếm để bắn đạn tự động

enemies = []
enemy_spawn_time = 400
last_enemy_spawn = pygame.time.get_ticks()
enemy_speed = 3

score = 0


def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    enemy_rect = linh_game_image.get_rect()
    if side == "top":
        enemy_rect.x = random.randint(0, screen_width - enemy_rect.width)
        enemy_rect.y = -enemy_rect.height
    elif side == "bottom":
        enemy_rect.x = random.randint(0, screen_width - enemy_rect.width)
        enemy_rect.y = screen_height
    elif side == "left":
        enemy_rect.x = -enemy_rect.width
        enemy_rect.y = random.randint(0, screen_height - enemy_rect.height)
    elif side == "right":
        enemy_rect.x = screen_width
        enemy_rect.y = random.randint(0, screen_height - enemy_rect.height)
    return enemy_rect, side


# Khởi tạo target_x và target_y với giá trị mặc định
target_x, target_y = catlyn_rect.centerx, catlyn_rect.centery

running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Chuột phải
                mouse_x, mouse_y = pygame.mouse.get_pos()
                target_x, target_y = mouse_x, mouse_y

    # Di chuyển nhân vật từ từ về phía chuột
    dx = target_x - catlyn_rect.centerx
    dy = target_y - catlyn_rect.centery
    distance = math.sqrt(dx**2 + dy**2)

    if distance != 0:
        direction_x = dx / distance
        direction_y = dy / distance
        speed = 4  # Tốc độ di chuyển của nhân vật
        catlyn_rect.centerx += int(direction_x * speed)
        catlyn_rect.centery += int(direction_y * speed)

    # Giới hạn nhân vật trong màn hình
    if catlyn_rect.left < 0:
        catlyn_rect.left = 0
    if catlyn_rect.right > screen_width:
        catlyn_rect.right = screen_width
    if catlyn_rect.top < 0:
        catlyn_rect.top = 0
    if catlyn_rect.bottom > screen_height:
        catlyn_rect.bottom = screen_height

    # Vẽ nhân vật
    screen.blit(catlyn_image, catlyn_rect)

    # Tạo đạn tự động theo hướng chuột khi nhấn Q
    if pygame.key.get_pressed()[pygame.K_q]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - catlyn_rect.centerx
        dy = mouse_y - catlyn_rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            direction_x = dx / distance
            direction_y = dy / distance

            # Bắn đạn mỗi 200ms
            bullet_timer += clock.get_time()
            if bullet_timer > 200:
                bullets.append({
                    "rect": pygame.Rect(catlyn_rect.centerx - 5, catlyn_rect.top, 10, 10),
                    "direction": (direction_x, direction_y)
                })
                bullet_timer = 0

    # Di chuyển và vẽ đạn
    for bullet in bullets[:]:
        bullet["rect"].x += int(bullet_speed * bullet["direction"][0])
        bullet["rect"].y += int(bullet_speed * bullet["direction"][1])
        if (
            bullet["rect"].top < 0 or bullet["rect"].bottom > screen_height
            or bullet["rect"].left < 0 or bullet["rect"].right > screen_width
        ):
            bullets.remove(bullet)
        pygame.draw.rect(screen, WHITE, bullet["rect"])

    # Sinh và di chuyển kẻ thù
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemy_rect, side = spawn_enemy()
        enemies.append((enemy_rect, side))
        last_enemy_spawn = current_time

    for enemy_data in enemies[:]:
        enemy_rect, side = enemy_data
        if side == "top":
            enemy_rect.y += enemy_speed
        elif side == "bottom":
            enemy_rect.y -= enemy_speed
        elif side == "left":
            enemy_rect.x += enemy_speed
        elif side == "right":
            enemy_rect.x -= enemy_speed
        if enemy_rect.colliderect(catlyn_rect):
            running = False
        if (
            enemy_rect.top > screen_height
            or enemy_rect.bottom < 0
            or enemy_rect.left > screen_width
            or enemy_rect.right < 0
        ):
            enemies.remove(enemy_data)
        screen.blit(linh_game_image, enemy_rect)

    # Kiểm tra va chạm giữa đạn và kẻ thù
    for bullet in bullets[:]:
        for enemy_data in enemies[:]:
            enemy_rect, _ = enemy_data
            if bullet["rect"].colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy_data)
                score += 10
                break

    draw_score()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
