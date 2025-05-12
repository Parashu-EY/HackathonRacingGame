import pygame
import logging

# Initialize Pygame
pygame.init()

# Set up logging
logging.basicConfig(
    filename="game_stats.log",  # Log file name
    level=logging.INFO,         # Log level
    format="%(asctime)s - %(message)s"  # Log format
)

#importing modules
import time
import random


# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Loading car image
carimg = pygame.image.load('car1.jpg').convert_alpha()
car_width = 56

#load all images
grass = pygame.image.load('grass.jpg').convert_alpha()
yellow_strip = pygame.image.load('yellow_strip.jpg').convert_alpha()
strip = pygame.image.load('strip.jpg').convert_alpha()

# Crashed Message
myfont = pygame.font.SysFont("none", 50)
render_text = myfont.render("CAR CRASHED",1, (0, 0, 0))

# Clock
clock = pygame.time.Clock()

# Set the title of the window
pygame.display.set_caption("Racing Game")

def obstacle(obs_x, obs_y, obs):
    if obs == 0:
        obs_pic = pygame.image.load('car2.jpg').convert_alpha()
    elif obs == 1:
        obs_pic = pygame.image.load('car3.jpg').convert_alpha()
    elif obs == 2:
        obs_pic = pygame.image.load('car4.jpg').convert_alpha()
    elif obs == 3:
        obs_pic = pygame.image.load('car5.jpg').convert_alpha()
    elif obs == 4:
        obs_pic = pygame.image.load('car6.jpg').convert_alpha()
    elif obs == 5:
        obs_pic = pygame.image.load('car7.jpg').convert_alpha()
    screen.blit(obs_pic, (obs_x, obs_y))  # Draw the obstacle

def background():
    # Draw the background
    screen.blit(grass, (0, 0))  # Grass background
    screen.blit(grass, (700, 0))
    screen.blit(yellow_strip, (400, 0))
    screen.blit(yellow_strip, (400, 100))
    screen.blit(yellow_strip, (400, 200))
    screen.blit(yellow_strip, (400, 300))
    screen.blit(yellow_strip, (400, 400))
    screen.blit(yellow_strip, (400, 500))
    screen.blit(yellow_strip, (400, 600))  # Yellow strip background
    screen.blit(strip, (120, 0))
    screen.blit(strip, (680, 0))   # Strip background

# Function for score card
def score_card(car_passed, score):
    font = pygame.font.SysFont("none", 35) #30
    passed = font.render("Cars Passed: " + str(car_passed), 1, (255, 255, 255))
    score = font.render("Score: " + str(score), 1, (0, 0, 0))
    screen.blit(passed, (0, 50))  # Display cars passed
    screen.blit(score, (0, 100))  # Display score


# Car image appearance
def car(x, y):
    screen.blit(carimg, (x, y))  # Use x and y to position the car

# Main game loop
def game_loop():
    global x, y, x_change, running  # Declare variables as global to modify them inside the function

    # Initialize car position and speed
    x = 400  
    y = 470  
    x_change = 0  
    obstacle_speed = 3
    obs = 0
    y_change = 0
    obs_x = random.randrange(200, 650)  # Random x position for the obstacle
    obs_y = -750  # Start the obstacle off-screen
    enemy_width = 56
    enemy_height = 125
    car_passed = 0
    score = 0
    level = 0
    cheat_activated = False  # Track if the cheat code is activated

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for the QUIT event
                running = False

            # Moving x and y coordinates
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -3
                if event.key == pygame.K_RIGHT:
                    x_change = 3

                if event.key == pygame.K_s:
                    obstacle_speed += 2  # Increase speed when 's' is pressed   
                if event.key == pygame.K_b:
                    obstacle_speed -= 2 # Decrease speed when 's' is pressed
                
                # Cheat code activation (e.g., press 'C' to activate cheat)
                if event.key == pygame.K_c:
                    cheat_activated = True
                    score += 100  # Add 100 points to the score
                    logging.warning(
                        f"CHEAT_CODE_ACTIVATED: Player X Position: {x}, "
                        f"Score: {score}, Game Time: {pygame.time.get_ticks() / 1000:.2f} seconds"
                    )


            if event.type == pygame.KEYUP:    
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0 

        x += x_change

        # Log player's x position and game time
        game_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
        logging.info(f"Player X Position: {x}, Game Time: {game_time:.2f} seconds")

        # Background color
        screen.fill((119, 119, 119))  # Fill the background first
        background()
        obs_y -= (obstacle_speed/4)
        obstacle(obs_x, obs_y,obs)  # Draw the obstacle
        obs_y += obstacle_speed

        # Calling car function
        car(x, y)  # Draw the car after the background

        # Calling score card function
        score_card(car_passed, score)  # Display the score card



        if x > 680 - car_width or x < 120:
            screen.blit(render_text, (300, 250))
            pygame.display.update()
            time.sleep(5)
            game_loop()  # Restart the game loop

        if obs_y > screen_height:
            # Log OBSTACLE_DODGED event
            logging.info(
                f"OBSTACLE_DODGED: Obstacle Position: ({obs_x}, {obs_y}), "
                f"Size: ({enemy_width}, {enemy_height}), Score: {score}"
            )
            obs_y = 0 - enemy_height
            obs_x = random.randrange(170, screen_width - 170)  # Random x position for the obstacle
            obs = random.randrange(0, 6)  # Randomly select an obstacle type
            car_passed += 1
            score = car_passed * 10  # Update score based on cars passed
            if int(car_passed) % 10 == 0:
                level += 1
                obstacle_speed += 2
                myfont = pygame.font.SysFont("none", 100)
                level_text = myfont.render("Level " + str(level), 1, (0, 0, 0))
                screen.blit(level_text, (300, 250))
                pygame.display.update()
                time.sleep(3)

        if y < obs_y + enemy_height:
            if x > obs_x and x < obs_x + enemy_width or x + car_width > obs_x and x + car_width < obs_x + enemy_width:
                screen.blit(render_text, (300, 250))
                pygame.display.update()
                time.sleep(5)
                game_loop()

        # Updating the game
        pygame.display.update()
        clock.tick(200)  # Set the frame rate to 100 FPS

# Quit Pygame
game_loop()
pygame.quit()
