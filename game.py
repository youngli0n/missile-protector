import pygame
import random
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOWL_WIDTH = 100
BOWL_HEIGHT = 50
OBJECT_SIZE = 64  # Increased from 32 to 64
INITIAL_SPEED = 3
SPEED_INCREMENT = 0.1
WIN_SCORE = 10
LOSE_SCORE = -3
NUM_STARS = 100  # Number of stars in the background

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 40)  # Dark blue for night sky

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Objects!")

# Load and scale sprite image
SPRITE_PATH = os.path.join('images', 'missile.png')
original_sprite = pygame.image.load(SPRITE_PATH).convert_alpha()
falling_object_sprite = pygame.transform.scale(original_sprite, (OBJECT_SIZE, OBJECT_SIZE))

# Star class for background
class Star:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2.0)
        self.brightness = random.randint(50, 255)

    def update(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = 0
            self.x = random.randint(0, WINDOW_WIDTH)
            self.brightness = random.randint(50, 255)

    def draw(self):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

# Falling object class
class FallingObject:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH - OBJECT_SIZE)
        self.y = -OBJECT_SIZE
        self.speed = INITIAL_SPEED
        self.rect = pygame.Rect(self.x, self.y, OBJECT_SIZE, OBJECT_SIZE)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self):
        screen.blit(falling_object_sprite, self.rect)

# Bowl class
class Bowl:
    def __init__(self):
        self.width = BOWL_WIDTH
        self.height = BOWL_HEIGHT
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - self.height - 10
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        elif direction == 'right' and self.x < WINDOW_WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

def main():
    clock = pygame.time.Clock()
    bowl = Bowl()
    falling_objects = []
    stars = [Star() for _ in range(NUM_STARS)]  # Create stars
    score = 0
    font = pygame.font.Font(None, 36)
    game_over = False
    current_speed = INITIAL_SPEED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Update stars
            for star in stars:
                star.update()

            # Add new objects
            if random.random() < 0.02:  # 2% chance each frame to add a new object
                falling_objects.append(FallingObject())

            # Update objects
            for obj in falling_objects[:]:
                obj.speed = current_speed
                obj.update()
                
                # Check collision with bowl
                if obj.rect.colliderect(bowl.rect):
                    score += 1
                    falling_objects.remove(obj)
                
                # Check if object was missed
                elif obj.y > WINDOW_HEIGHT:
                    score -= 1
                    falling_objects.remove(obj)

            # Update speed
            current_speed += SPEED_INCREMENT * 0.01

            # Check win/lose conditions
            if score >= WIN_SCORE:
                game_over = True
                message = "You Win!"
            elif score <= LOSE_SCORE:
                game_over = True
                message = "Game Over!"

            # Bowl control
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                bowl.move('left')
            if keys[pygame.K_RIGHT]:
                bowl.move('right')

        # Drawing
        screen.fill(DARK_BLUE)  # Dark blue background
        
        # Draw stars
        for star in stars:
            star.draw()
        
        # Draw objects and bowl
        for obj in falling_objects:
            obj.draw()
        bowl.draw()

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)  # Changed to white for better visibility
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render(message, True, WHITE)  # Changed to white for better visibility
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 