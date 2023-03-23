import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# The display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprite.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        global bullets_fired
        if len(bullets) < bullet_limit:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullets_fired += 1

class Alien(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("alien.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 20))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(HEIGHT // 4, HEIGHT // 2)
            self.speed_x = random.randint(1, 4)

        def update(self):
            self.rect.x += self.speed_x
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.speed_x = -self.speed_x

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

num_aliens = 10
bullet_limit = num_aliens + 5
bullets_fired = 0

for i in range(10):
    alien = Alien()
    all_sprites.add(alien)
    aliens.add(alien)

score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
    score += len(hits)

    if len(aliens) == 0:
        game_over_text = font.render("YOU WON", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 ))
        pygame.display.flip()
        pygame.time.wait(3000)
        game_over = True

    if bullets_fired >= bullet_limit and len(aliens) > 0:
        game_over_text = font.render("YOU LOST", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 ))
        pygame.display.flip()
        pygame.time.wait(3000)
        game_over = True

    screen.fill(BLACK)
    all_sprites.draw(screen)

    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()