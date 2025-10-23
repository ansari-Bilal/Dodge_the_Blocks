import pygame
import random
import sys

pygame.init()

# --------- Dynamic Window Size (70% of screen) ----------
info = pygame.display.Info()
SCREEN_WIDTH = int(info.current_w * 0.7)
SCREEN_HEIGHT = int(info.current_h * 0.7)
# --------------------------------------------------------

FPS = 60
PLAYER_SIZE = 50
PLAYER_SPEED = 7
BLOCK_MIN_SIZE = 30
BLOCK_MAX_SIZE = 80
BLOCK_SPAWN_DELAY = 700
SPEED_INCREASE_EVERY = 5000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Blocks")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

#events

SPAWN_BLOCK = pygame.USEREVENT + 1
DIFFICULTY_UP = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_BLOCK, BLOCK_SPAWN_DELAY)
pygame.time.set_timer(DIFFICULTY_UP, SPEED_INCREASE_EVERY)


def draw_text(surf, text, x, y, font, color=(255, 255, 255)):
    img = font.render(text, True, color)
    surf.blit(img, (x, y))


class Player:
    def __init__(self):
        self.w = PLAYER_SIZE
        self.h = PLAYER_SIZE
        self.x = SCREEN_WIDTH // 2 - self.w // 2
        self.y = SCREEN_HEIGHT - self.h - 20
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, surf):
        pygame.draw.rect(surf, (50, 200, 255), self.rect)


class Block:
    def __init__(self, speed):
        self.size = random.randint(BLOCK_MIN_SIZE, BLOCK_MAX_SIZE)
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = -self.size
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)    
        
        #random color
        
        self.color = (                            
            random.randint(120, 255),
            random.randint(40, 200),
            random.randint(40, 200),
        )

    def update(self):
        self.rect.y += self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)


def game_loop():
    player = Player()
    blocks = []
    running = True
    game_over = False
    score = 0
    start_ticks = pygame.time.get_ticks()
    block_fall_speed = 4
    spawn_delay = BLOCK_SPAWN_DELAY

    while running:
        dt = clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == SPAWN_BLOCK and not game_over:
                blocks.append(Block(block_fall_speed))
            if ev.type == DIFFICULTY_UP and not game_over:
                #ramp difficulty : faster blocks, spawn more often  
                block_fall_speed += 0.4
                spawn_delay = max(180, spawn_delay - 40)
                pygame.time.set_timer(SPAWN_BLOCK, int(spawn_delay))
            if ev.type == pygame.KEYDOWN and game_over:
                if ev.key == pygame.K_r:
                    return                #restart by returning to caller
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()
        if not game_over:
            player.update(keys)
            for b in blocks:
                b.update()
                
                
        #remove off-screen blocks & update score based on time survived

            blocks = [b for b in blocks if b.rect.top <= SCREEN_HEIGHT + 200]
            score = (pygame.time.get_ticks() - start_ticks) // 1000      # seconds survived
            
            
        # collision happened or not ?
            for b in blocks:
                if player.rect.colliderect(b.rect):
                    game_over = True
                    break
                          
        #draw
        screen.fill((18, 18, 20))
        player.draw(screen)
        for b in blocks:
            b.draw(screen)

        draw_text(screen, f"Score: {score}", 10, 10, font)
        draw_text(screen, "Move: ← →  or A D", SCREEN_WIDTH - 260, 10, font)
        if game_over:
            draw_text(
                screen,
                "GAME OVER",
                SCREEN_WIDTH // 2 - 160,
                SCREEN_HEIGHT // 2 - 80,
                big_font,
                (255, 50, 50),
            )
            draw_text(
                screen,
                f"Final score: {score}",
                SCREEN_WIDTH // 2 - 110,
                SCREEN_HEIGHT // 2 - 10,
                font,
            )
            draw_text(
                screen,
                "Press R to restart or Esc to quit",
                SCREEN_WIDTH // 2 - 200,
                SCREEN_HEIGHT // 2 + 40,
                font,
            )

        pygame.display.flip()


def main():
    while True:
        game_loop()


if __name__ == "__main__":
    main()
