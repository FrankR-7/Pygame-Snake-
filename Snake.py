"""
Pygame Snake!
(My first Python program!)
Made by Franklin Rosales

A simple Snake ripoff I made with Pygame.

May be buggy and unoptimised as hell, but any help would be welcome.
And no, I don't care if you change something.

"""
import pygame
import random

pygame.font.init()
# Set the window settings
WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Snake")
step = 10  # The grid in which the game runs on


class Snake:
    def __init__(self, x, y):
        self.size = 10
        self.x = x
        self.y = y

    def draw(self, window):  # Draw the snake's piece onto the screen
        pygame.draw.rect(window, (0, 196, 72), (self.x, self.y, self.size, self.size))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Food:
    def __init__(self):
        self.size = 10
        self.x = random.randrange(0, WIDTH - self.size, step)
        self.y = random.randrange(0, HEIGHT - self.size, step)

    def respawn(self):  # Set new random coordinates for the food
        self.x = random.randrange(0, WIDTH - self.size, step)
        self.y = random.randrange(0, HEIGHT - self.size, step)

    def draw(self, window):  # Draw the food to the screen
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.size, self.size))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def main():
    # Set everything right before starting
    snake_body = []
    clock = pygame.time.Clock()
    food = Food()
    snake_size = 4
    direction = 'right'
    new_x, new_y = 250, 250
    alive = True
    flag = True
    score = 0
    score_font = pygame.font.SysFont('Candara', 15, 1)

    def head(window, direction, xx, yy):  # The eyes of the snake
        if direction == 'up' or direction == 'down':
            pygame.draw.rect(window, (255, 255, 255), (xx + 1, yy + 4, 3, 3))
            pygame.draw.rect(window, (255, 255, 255), (xx + 6, yy + 4, 3, 3))
        elif direction == 'left' or direction == 'right':
            pygame.draw.rect(window, (255, 255, 255), (xx + 4, yy + 1, 3, 3))
            pygame.draw.rect(window, (255, 255, 255), (xx + 4, yy + 6, 3, 3))

    def render(direction):  # Draw everything to the screen
        pygame.draw.rect(WIN, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

        score_label = score_font.render(f'Score: {score}', 1, (255, 255, 255))
        WIN.blit(score_label, (10, 10))

        if len(snake_body) <= snake_size:
            snake = Snake(new_x, new_y)
            snake_body.insert(0, snake)
        if len(snake_body) > snake_size:
            snake_body.pop()
        for snake in snake_body:
            snake.draw(WIN)

        food.draw(WIN)
        head(WIN, direction, new_x, new_y)

        pygame.display.update()

    def keyboard(keys, direction):  # Avoids the snake from ramming into itself
        yes = False
        if keys[pygame.K_DOWN] and direction != 'up':
            yes = True
        if keys[pygame.K_UP] and direction != 'down':
            yes = True
        if keys[pygame.K_RIGHT] and direction != 'left':
            yes = True
        if keys[pygame.K_LEFT] and direction != 'right':
            yes = True
        return yes

    while alive:
        clock.tick(10)
        render(direction)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()  # The snake's movement
        if keyboard(keys, direction):
            if keys[pygame.K_DOWN] and direction != 'up':
                new_y += step
                direction = 'down'
            elif keys[pygame.K_UP] and direction != 'down':
                new_y -= step
                direction = 'up'
            elif keys[pygame.K_LEFT] and direction != 'right':
                new_x -= step
                direction = 'left'
            elif keys[pygame.K_RIGHT] and direction != 'left':
                new_x += step
                direction = 'right'
        else:  # The snake's automatic movement
            if direction == 'down':
                new_y += step
            elif direction == 'up':
                new_y -= step
            elif direction == 'left':
                new_x -= step
            elif direction == 'right':
                new_x += step

        if new_x < 0 or new_x > WIDTH or new_y > HEIGHT or new_y < 0:
            high_score = score  # Kill the snake if it leaves the screen
            alive = False
        if new_x == food.get_x() and new_y == food.get_y():
            food.respawn()  # Move the food to a new place
            snake_size += 1  # Make the snake longer
            score += 1
        if not flag:  # Only work after the first frame
            for snake in snake_body:
                if new_x == snake.get_x() and new_y == snake.get_y():
                    alive = False  # Kill the snake if it hits itself
                    high_score = score

        flag = False  # After the first frame, start checking for collisions

    return (high_score, score)
    

def main_menu():
    font = pygame.font.SysFont("Candara", 25, 1)
    high_font = pygame.font.SysFont('Candara', 15, 1)
    high = old_high = scr = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                old_high = high
                ret = main()
                high, scr = ret[0], ret[1]
                if high < old_high:
                    high = old_high

        high_label = high_font.render(f'High Score: {high}', 1, (255, 255, 255))
        score_label = high_font.render(f'Last Game: {scr}', 1, (255, 255, 255))
        pygame.draw.rect(WIN, (4, 71, 17), (0, 0, WIDTH, HEIGHT))
        title = font.render('Pygame Snake! Click to continue', 1, (255, 255, 255))
        WIN.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - title.get_height()))
        WIN.blit(high_label, (10, 10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))

        pygame.display.update()


main_menu()
