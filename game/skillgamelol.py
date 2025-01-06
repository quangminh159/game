import pygame
import random
import sys

# Khởi tạo pygame
pygame.init()

# Cấu hình game
clock = pygame.time.Clock()
fps = 60

# Kích thước màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Skill Game LOL')

# Màu sắc
WHITE = (255, 255, 255)

# Font chữ
font = pygame.font.Font(None, 36)

# Tải ảnh và âm thanh
try:
    # Ảnh nền
    background_image = pygame.image.load('background.png')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Nhân vật chính
    catlyn_image = pygame.image.load('catlyn.png')
    catlyn_image = pygame.transform.scale(catlyn_image, (80, 80))

    # Kẻ thù
    linh_game_image = pygame.image.load('gromp.png')
    linh_game_image = pygame.transform.scale(linh_game_image, (60, 60))

    # Âm thanh
    # pygame.mixer.music.load("nhacnen.mp3")
    # pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.play(-1, 0.0)

    # shoot_sound = pygame.mixer.Sound("shot_sound.mp3")
    # game_over_sound = pygame.mixer.Sound("game_over.mp3")

except Exception as e:
    print(f"Lỗi tải tài nguyên: {e}")
    sys.exit()

# Tạo nhân vật chính (Catlyn)
catlyn_rect = catlyn_image.get_rect()
catlyn_rect.center = (screen_width // 2, screen_height - 100)

# Tạo danh sách đạn
bullets = []
bullet_speed = -10

# Tạo danh sách kẻ thù (Gromp)
enemies = []
enemy_spawn_time = 500
last_enemy_spawn = pygame.time.get_ticks()
enemy_speed = 3

# Điểm số
score = 0

# Hàm hiển thị điểm
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Hàm tạo kẻ thù từ các phía
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

# Vòng lặp game
running = True
while running:
    screen.blit(background_image, (0, 0))

    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Bắn đạn
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet_rect = pygame.Rect(catlyn_rect.centerx - 5, catlyn_rect.top, 10, 20)
                bullets.append(bullet_rect)
                # shoot_sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target_x, target_y = pygame.mouse.get_pos()
                catlyn_rect.centerx = target_x
                catlyn_rect.centery = target_y

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

    # Di chuyển và vẽ đạn
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)
        pygame.draw.rect(screen, WHITE, bullet)

    # Sinh kẻ thù từ nhiều phía
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemy_rect, side = spawn_enemy()
        enemies.append((enemy_rect, side))
        last_enemy_spawn = current_time

    # Di chuyển và vẽ kẻ thù
    for enemy_data in enemies[:]:
        enemy_rect, side = enemy_data

        # Di chuyển kẻ thù theo hướng tương ứng
        if side == "top":
            enemy_rect.y += enemy_speed
        elif side == "bottom":
            enemy_rect.y -= enemy_speed
        elif side == "left":
            enemy_rect.x += enemy_speed
        elif side == "right":
            enemy_rect.x -= enemy_speed

        # Kiểm tra va chạm với nhân vật chính
        if enemy_rect.colliderect(catlyn_rect):
            # game_over_sound.play()
            running = False  # Kết thúc game

        # Loại bỏ kẻ thù khi ra ngoài màn hình
        if (
            enemy_rect.top > screen_height
            or enemy_rect.bottom < 0
            or enemy_rect.left > screen_width
            or enemy_rect.right < 0
        ):
            enemies.remove(enemy_data)

        # Vẽ kẻ thù
        screen.blit(linh_game_image, enemy_rect)

    # Kiểm tra va chạm giữa đạn và kẻ thù
    for bullet in bullets[:]:
        for enemy_data in enemies[:]:
            enemy_rect, _ = enemy_data
            if bullet.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy_data)
                score += 10  # Cộng điểm khi tiêu diệt kẻ thù
                break

    # Hiển thị điểm số
    draw_score()

    # Cập nhật màn hình
    pygame.display.update()
    clock.tick(fps)

# Hiển thị màn hình kết thúc
screen.blit(pygame.image.load('end_game.png'), (0, 0))
pygame.display.update()
pygame.time.wait(3000)

pygame.quit()
