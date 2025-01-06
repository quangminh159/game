from ursina import *
import random
window.borderless = False
# Khởi tạo game
app = Ursina()

# Kích thước màn hình
window.size = (800, 600)
window.title = "Skill Game LOL"
window.color = color.black

# Tạo nhân vật chính
catlyn = Entity(
    model='quad',
    texture='catlyn.png',
    scale=(0.1, 0.1),  # Tùy chỉnh kích thước
    position=(0, -0.4)
)

# Tạo danh sách đạn
bullets = []
bullet_speed = 0.05

# Tạo danh sách kẻ thù
enemies = []
enemy_speed = 0.01
spawn_time = 2
last_spawn = time.time()

# Điểm số
score = 0
score_text = Text(text=f"Score: {score}", position=(-0.45, 0.45), color=color.white)

# Hàm tạo kẻ thù
def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    enemy = Entity(
        model='quad',
        texture='gromp.png',
        scale=(0.1, 0.1)
    )

    if side == "top":
        enemy.position = (random.uniform(-0.9, 0.9), 0.9)
        enemy.direction = Vec2(0, -1)
    elif side == "bottom":
        enemy.position = (random.uniform(-0.9, 0.9), -0.9)
        enemy.direction = Vec2(0, 1)
    elif side == "left":
        enemy.position = (-0.9, random.uniform(-0.9, 0.9))
        enemy.direction = Vec2(1, 0)
    elif side == "right":
        enemy.position = (0.9, random.uniform(-0.9, 0.9))
        enemy.direction = Vec2(-1, 0)

    enemies.append(enemy)

# Xử lý chuột
def input(key):
    global score
    if key == 'left mouse down':
        bullet = Entity(
            model='quad',
            color=color.red,
            scale=(0.02, 0.05),
            position=catlyn.position
        )
        bullets.append(bullet)

    if key == 'right mouse down':  # Di chuyển đến vị trí chuột
        catlyn.position = Vec2(mouse.world_point[0], mouse.world_point[1])

# Hàm cập nhật game
def update():
    global last_spawn, score

    # Di chuyển đạn
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y > 0.9:  # Xóa đạn khi ra khỏi màn hình
            bullets.remove(bullet)
            destroy(bullet)

    # Sinh kẻ thù
    if time.time() - last_spawn > spawn_time:
        spawn_enemy()
        last_spawn = time.time()

    # Di chuyển kẻ thù
    for enemy in enemies[:]:
        enemy.position += enemy.direction * enemy_speed

        # Kiểm tra va chạm với nhân vật chính
        if enemy.intersects(catlyn).hit:
            print("Game Over")
            app.quit()

        # Xóa kẻ thù khi ra khỏi màn hình
        if abs(enemy.x) > 1 or abs(enemy.y) > 1:
            enemies.remove(enemy)
            destroy(enemy)

    # Kiểm tra va chạm giữa đạn và kẻ thù
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.intersects(enemy).hit:
                score += 10
                score_text.text = f"Score: {score}"
                bullets.remove(bullet)
                enemies.remove(enemy)
                destroy(bullet)
                destroy(enemy)
                break

# Chạy ứng dụng
app.run()
