import pygame
import sys
import random
import os

# 파이게임 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 480, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1945 슈팅 게임")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 게임 클래스 및 함수
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 비행기 모양 그리기
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        # 비행기 몸체
        pygame.draw.rect(self.image, BLUE, (10, 10, 30, 20))
        # 비행기 날개
        pygame.draw.polygon(self.image, BLUE, [(0, 20), (10, 20), (10, 10), (20, 10)])
        pygame.draw.polygon(self.image, BLUE, [(40, 10), (40, 20), (50, 20), (40, 10)])
        # 비행기 꼬리
        pygame.draw.polygon(self.image, BLUE, [(20, 0), (30, 0), (25, 10)])
        # 비행기 엔진 불꽃
        pygame.draw.polygon(self.image, RED, [(20, 30), (30, 30), (25, 40)])
        
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.color = random.choice([RED, GREEN, YELLOW, PURPLE])
        pygame.draw.rect(self.image, self.color, (0, 0, 30, 30))
        
        # 적 비행기 디테일 추가
        pygame.draw.rect(self.image, BLACK, (5, 15, 20, 5))
        pygame.draw.rect(self.image, BLACK, (13, 5, 4, 20))
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.shoot_delay = random.randrange(1000, 3000)
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)
            
        # 적 총알 발사
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()
            
    def shoot(self):
        bullet_type = random.randint(0, 3)  # 0: 원형, 1: 삼각형, 2: 사각형, 3: 다이아몬드
        enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, bullet_type)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.image, WHITE, (0, 0, 5, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_type):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.bullet_type = bullet_type
        
        if bullet_type == 0:  # 원형
            pygame.draw.circle(self.image, YELLOW, (5, 5), 5)
        elif bullet_type == 1:  # 삼각형
            pygame.draw.polygon(self.image, GREEN, [(5, 0), (0, 10), (10, 10)])
        elif bullet_type == 2:  # 사각형
            pygame.draw.rect(self.image, RED, (0, 0, 10, 10))
        else:  # 다이아몬드
            pygame.draw.polygon(self.image, PURPLE, [(5, 0), (10, 5), (5, 10), (0, 5)])
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = random.randrange(3, 6)
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# 플레이어 생성
player = Player()
all_sprites.add(player)

# 적 생성
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    # 프레임 설정
    clock.tick(60)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # 업데이트
    all_sprites.update()
    
    # 충돌 체크 (총알과 적)
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # 충돌 체크 (플레이어와 적)
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False
        
    # 충돌 체크 (플레이어와 적 총알)
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    if hits:
        running = False
    
    # 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # 화면 업데이트
    pygame.display.flip()

# 게임 종료
pygame.quit()
sys.exit()
