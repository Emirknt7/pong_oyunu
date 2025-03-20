import pygame
import sys
import random

# oyunu başlatma 
pygame.init()

# ekran ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Oyunu")

# Renk paletleri
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS ayarlanması
clock = pygame.time.Clock()
FPS = 60

# Raketler
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 7

# Top
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Skor
score_player = 0
score_opponent = 0
font = pygame.font.SysFont(None, 36)

# Raketlerin oluşturulması
player_paddle = pygame.Rect(WIDTH - PADDLE_WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Topun oluşturulması
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

def move_player_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

def move_opponent_paddle():
    # Basit AI: Topun y konumunu takip et
    if opponent_paddle.centery < ball.centery and opponent_paddle.bottom < HEIGHT:
        opponent_paddle.y += PADDLE_SPEED - 2  # Biraz daha yavaş
    if opponent_paddle.centery > ball.centery and opponent_paddle.top > 0:
        opponent_paddle.y -= PADDLE_SPEED - 2

def move_ball():
    global ball_speed_x, ball_speed_y, score_player, score_opponent
    
    # Topun hareketi
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Üst ve alt kenarlarla çarpışma
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    
    # Raketlerle çarpışma
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1
    
    # Sol duvara çarpışma (oyuncu skor)
    if ball.left <= 0:
        score_player += 1
        reset_ball()
    
    # Sağ duvara çarpışma (rakip skor)
    if ball.right >= WIDTH:
        score_opponent += 1
        reset_ball()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

def draw_objects():
    # Ekranı temizle
    screen.fill(BLACK)
    
    # Raketleri çiz
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    
    # Topu çiz
    pygame.draw.ellipse(screen, WHITE, ball)
    
    # Orta çizgiyi çiz
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Skorları çiz
    score_text = font.render(f"{score_opponent} - {score_player}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        move_player_paddle()
        move_opponent_paddle()
        move_ball()
        draw_objects()
        
        # Ekranı güncelle
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()