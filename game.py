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
BOWL_HEIGHT = 100  # Changed to make the shield circular
OBJECT_SIZE = 64  # Increased from 32 to 64
INITIAL_SPEED = 3
INITIAL_SPEED2 = 3.5
SPEED_INCREMENT = 0.1  # How much the speed increases over time
WIN_SCORE = 20
LOSE_SCORE = -3
NUM_STARS = 100  # Number of stars in the background
INITIAL_SPAWN_CHANCE = 0.0019  # 0.19% initial chance
SPAWN_CHANCE_INCREMENT = 0.00001  # How much the spawn chance increases per frame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 40)  # Dark blue for night sky

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Objects!")

# Load and scale sprite images
SPRITE_PATH = os.path.join('images', 'missile.png')
SHIELD_PATH = os.path.join('images', 'shield.png')
original_sprite = pygame.image.load(SPRITE_PATH).convert_alpha()
original_shield = pygame.image.load(SHIELD_PATH).convert_alpha()
falling_object_sprite = pygame.transform.scale(original_sprite, (OBJECT_SIZE, OBJECT_SIZE))
shield_sprite = pygame.transform.scale(original_shield, (BOWL_WIDTH, BOWL_HEIGHT))

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
        screen.blit(shield_sprite, self.rect)

def reset_game():
    """Reset the game state"""
    return {
        'bowl': Bowl(),
        'falling_objects': [],
        'score': 0,
        'game_over': False,
        'bowl_speed': INITIAL_SPEED2,
        'falling_speed': INITIAL_SPEED,
        'spawn_chance': INITIAL_SPAWN_CHANCE,  # Add spawn chance to game state
        'show_instructions': True  # Add instructions state
    }

def draw_instructions(screen, font):
    """Draw the instructions screen"""
    # Title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Missile Protector", True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
    screen.blit(title, title_rect)

    # Instructions
    instructions = [
        "How to Play:",
        "• Use LEFT and RIGHT arrow keys to move the bowl",
        "• Catch missiles to score points",
        "• Missing missiles will cost you points",
        "• Reach " + str(WIN_SCORE) + " points to win",
        "• Don't reach " + str(LOSE_SCORE) + " points or you lose!",
        "",
        "Game Features:",
        "• Missiles fall faster over time",
        "• More missiles appear as you progress",
        "• Press SPACE to restart when game is over",
        "",
        "Press SPACE to Start!"
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 150 + i * 30))
        screen.blit(text, text_rect)

def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    stars = [Star() for _ in range(NUM_STARS)]  # Create stars
    
    # Initialize game state
    game_state = reset_game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state['show_instructions']:
                        game_state['show_instructions'] = False
                    elif game_state['game_over']:
                        game_state = reset_game()

        # Update stars
        for star in stars:
            star.update()

        # Drawing
        screen.fill(DARK_BLUE)  # Dark blue background
        
        # Draw stars
        for star in stars:
            star.draw()

        if game_state['show_instructions']:
            # Draw instructions screen
            draw_instructions(screen, font)
        else:
            if not game_state['game_over']:
                # Add new objects with increasing spawn chance
                if random.random() < game_state['spawn_chance']:
                    game_state['falling_objects'].append(FallingObject())
                
                # Increase spawn chance
                game_state['spawn_chance'] += SPAWN_CHANCE_INCREMENT

                # Update objects
                for obj in game_state['falling_objects'][:]:
                    obj.speed = game_state['falling_speed']
                    obj.update()
                    
                    # Check collision with bowl
                    if obj.rect.colliderect(game_state['bowl'].rect):
                        game_state['score'] += 1
                        game_state['falling_objects'].remove(obj)
                    
                    # Check if object was missed
                    elif obj.y > WINDOW_HEIGHT:
                        game_state['score'] -= 1
                        game_state['falling_objects'].remove(obj)

                # Update speed
                game_state['falling_speed'] += SPEED_INCREMENT * 0.01

                # Check win/lose conditions
                if game_state['score'] >= WIN_SCORE:
                    game_state['game_over'] = True
                    message = "You Win!"
                elif game_state['score'] <= LOSE_SCORE:
                    game_state['game_over'] = True
                    message = "Game Over!"

                # Bowl control
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    game_state['bowl'].move('left')
                if keys[pygame.K_RIGHT]:
                    game_state['bowl'].move('right')

                # Draw game objects
                for obj in game_state['falling_objects']:
                    obj.draw()
                game_state['bowl'].draw()

                # Draw score
                score_text = font.render(f"Score: {game_state['score']}", True, WHITE)
                screen.blit(score_text, (10, 10))

            if game_state['game_over']:
                # Draw game over/win message
                game_over_text = font.render(message, True, WHITE)
                text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30))
                screen.blit(game_over_text, text_rect)
                
                # Draw restart message
                restart_text = font.render("Press SPACE to restart", True, WHITE)
                restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
                screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 