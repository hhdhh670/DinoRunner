import pygame
import os
import random

# 初始化pygame
pygame.init()
# 设置屏幕大小
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
# 获取资源
DINO_START = pygame.image.load(os.path.join("Assets/Dino", "DinoStart.png"))
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
DEAD = [pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png")),]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

OVER_PNG=pygame.image.load(os.path.join("Assets/Other", "GameOver.png"))
# 创建窗口
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
#  一些全局变量
death_count = 0


# 恐龙
class Dinosaur:
    # 默认位置
    X_POS = 80
    Y_POS = 310
    # 下蹲位置
    Y_POS_DUCK = 340
    # 跳跃速度
    JUMP_VEL = 8.5

    # 初始化
    def __init__(self):
        # 获取资源
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        # 标志
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        # 参数
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    # 更新精灵
    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= len(self.run_img) * 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_jump = True
            self.dino_duck = False
            self.dino_run = False
        elif (userInput[pygame.K_DOWN] or userInput[pygame.K_LCTRL] or userInput[
            pygame.K_RCTRL]) and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (
                self.dino_jump or (userInput[pygame.K_DOWN] or userInput[pygame.K_LCTRL] or userInput[pygame.K_RCTRL])):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    # 蹲
    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    # 跑
    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    # 跳
    def jump(self):
        self.image = self.jump_img
        # 跳跃状态逐渐减速并回落
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        # 落地
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    # 绘制
    def draw(self, window):
        window.blit(self.image, self.dino_rect)


# 云
class Cloud:
    def __init__(self):
        self.x_pos = SCREEN_WIDTH + random.randint(800, 1000)
        self.y_pos = random.randint(50, 100)
        self.image = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
        self.width = self.image.get_width()

    def update(self):
        self.x_pos -= game_speed
        # 跑出窗口
        if self.x_pos < -self.width:
            self.x_pos = SCREEN_WIDTH + random.randint(500, 2000)
            self.y_pos = random.randint(50, 100)

    def draw(self, window):
        window.blit(self.image, (self.x_pos, self.y_pos))


# 障碍物
class Obstacle:
    is_Passed = False
    def __init__(self, image, index):
        self.type = index
        self.image = image
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()  # 移出障碍物列表

    def draw(self, window):
        window.blit(self.image[self.type], self.rect)


# 小仙人掌
class SmallCactus(Obstacle):  # 继承障碍物
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


# 大仙人掌
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        super().__init__(image, self.type)
        self.rect.y = 300


# 鸟
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, window):
        if self.index >= len(BIRD)*10:
            self.index = 0
        window.blit(self.image[self.index//10], self.rect)
        self.index += 1

# 音效
class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()

        # 加载所有游戏音效
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        """加载所有音效文件"""
        sound_files = {
            'game_over': 'game_over.wav',
            'coin': 'Pickup_Coin.wav',
        }

        for name, filename in sound_files.items():
            try:
                if os.path.exists(filename):
                    self.sounds[name] = pygame.mixer.Sound(filename)
                else:
                    # 创建占位音效
                    self.create_placeholder_sound(name)
            except pygame.error as e:
                print(f"无法加载 {filename}: {e}")
                self.create_placeholder_sound(name)

    def create_placeholder_sound(self, name):
        """创建占位音效"""
        # 创建一个简单的静音音效
        self.sounds[name] = pygame.mixer.Sound(buffer=b'\x00\x00' * 44100)  # 1秒静音

    def play(self, name, volume=1.0, loops=0, fade_ms=0):
        """播放音效"""
        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(volume)
            channel = sound.play(loops=loops, fade_ms=fade_ms)
            return channel
        return None

    def stop(self, name):
        """停止播放特定音效"""
        if name in self.sounds:
            self.sounds[name].stop()

    def stop_all(self):
        """停止所有音效"""
        pygame.mixer.stop()


# 帮助信息
def help(center):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Jump:Space   Duck:Ctrl", True, 'black')
    textRect = text.get_rect()
    textRect.center = center
    window.blit(text, textRect)


# 主函数
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, death_count
    soundplayer = SoundPlayer()
    is_Running = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []

    # 分数
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Score: " + str(points), True, 'black')
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH - 100, 40)
        window.blit(text, textRect)

    # 背景
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        window.blit(BG, (x_pos_bg, y_pos_bg))
        window.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            window.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while is_Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_Running = False

        # 灰色清空整个屏幕
        window.fill((230, 230, 230))
        # 获取用户案件
        userInput = pygame.key.get_pressed()
        # 绘制角色
        player.draw(window)
        player.update(userInput)
        # 控制障碍物
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
        # 碰撞检测
        for obstacle in obstacles:
            obstacle.draw(window)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                background()
                window.blit(OVER_PNG, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                pygame.display.flip()
                soundplayer.play('game_over',volume=0.2,fade_ms=200)
                pygame.time.delay(3000)
                death_count += 1
                is_Running = False
                return
            if player.X_POS >= obstacle.rect.x+100 and obstacle.is_Passed == False:
                obstacle.is_Passed = True
                soundplayer.play('coin',volume=0.2, loops=0, fade_ms=200)


        background()
        cloud.draw(window)
        cloud.update()
        score()
        help((SCREEN_WIDTH - 150, 80))
        pygame.display.flip()
        clock.tick(60)



def menu():
    global points, text
    run = True
    # 背景音乐
    pygame.mixer.music.load('background.ogg')
    pygame.mixer.music.set_volume(0.08)
    pygame.mixer.music.play(-1)
    while run:
        window.fill((200, 200, 200))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
            window.blit(DINO_START, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            window.blit(score, scoreRect)
            window.blit(DEAD[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        window.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False
                else:
                    main()
        pygame.time.delay(100)

menu()
pygame.quit()
