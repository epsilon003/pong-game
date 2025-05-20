import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60
FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 40)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong-Game by epsilon003")
clock = pygame.time.Clock()

# Sound effects
bounce_sound = pygame.mixer.Sound("C:\\Users\\Abhimantr Singh\\Downloads\\codecplus\\pong-game\\bounce.wav")
score_sound = pygame.mixer.Sound("C:\\Users\\Abhimantr Singh\\Downloads\\codecplus\\pong-game\\score.wav")

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - 50, 10, 100)
        self.speed = 7

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
            bounce_sound.play()

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, self.rect)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= -1


class Game:
    def __init__(self):
        self.player = Paddle(10)
        self.opponent = Paddle(WIDTH - 20)
        self.ball = Ball()
        self.player_score = 0
        self.opponent_score = 0
        self.state = STATE_MENU

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(True)
        if keys[pygame.K_s]:
            self.player.move(False)

    def update(self):
        self.ball.move()

        # Opponent AI
        if self.opponent.rect.centery < self.ball.rect.centery:
            self.opponent.move(False)
        elif self.opponent.rect.centery > self.ball.rect.centery:
            self.opponent.move(True)

        # Paddle collisions
        if self.ball.rect.colliderect(self.player.rect) or self.ball.rect.colliderect(self.opponent.rect):
            self.ball.speed_x *= -1
            bounce_sound.play()

        # Scoring
        if self.ball.rect.left <= 0:
            self.opponent_score += 1
            self.ball.reset()
            score_sound.play()

        if self.ball.rect.right >= WIDTH:
            self.player_score += 1
            self.ball.reset()
            score_sound.play()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.player.draw(surface)
        self.opponent.draw(surface)
        self.ball.draw(surface)
        pygame.draw.aaline(surface, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Scores
        player_text = FONT.render(str(self.player_score), True, WHITE)
        opponent_text = FONT.render(str(self.opponent_score), True, WHITE)
        surface.blit(player_text, (WIDTH // 4, 20))
        surface.blit(opponent_text, (WIDTH * 3 // 4, 20))

    def draw_menu(self, surface):
        surface.fill((0, 0, 0))
        title = FONT.render("PONG GAME", True, WHITE)
        subtitle = SMALL_FONT.render("Press SPACE to Start", True, WHITE)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        surface.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2))

    def draw_pause(self, surface):
        pause_text = SMALL_FONT.render("Game Paused. Press P to Resume.", True, WHITE)
        surface.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))


def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Global input
            if event.type == pygame.KEYDOWN:
                if game.state == STATE_MENU and event.key == pygame.K_SPACE:
                    game.state = STATE_PLAYING
                elif game.state == STATE_PLAYING and event.key == pygame.K_p:
                    game.state = STATE_PAUSED
                elif game.state == STATE_PAUSED and event.key == pygame.K_p:
                    game.state = STATE_PLAYING

        # Game logic
        if game.state == STATE_PLAYING:
            game.handle_input()
            game.update()
            game.draw(screen)
        elif game.state == STATE_MENU:
            game.draw_menu(screen)
        elif game.state == STATE_PAUSED:
            game.draw(screen)
            game.draw_pause(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
