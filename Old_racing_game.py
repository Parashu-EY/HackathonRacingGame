import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AI Racing Game")

# Colors
white = (255, 255, 255)
# Define a list of off-track colors
off_track_color = (99, 145, 61)# Add more if you find others

# Load track image
try:
    track_image = pygame.image.load('track.png').convert()
    track_rect = track_image.get_rect(center=(screen_width // 2, screen_height // 2))
except pygame.error as e:
    print(f"Error loading track image: {e}")
    sys.exit()

# Load car image
try:
    original_car_image = pygame.image.load('car.png').convert_alpha()
    car_image = original_car_image
    car_rect = car_image.get_rect(center=(screen_width // 2, screen_height - 100))
    car_speed = 1
    car_angle = 0
    rotation_speed = 1
except pygame.error as e:
    print(f"Error loading car image: {e}")
    sys.exit()

def check_collision(rect, track_surface, off_color):
    """Checks if any of the corners of the rect collide with the off-track color."""
    points_to_check = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]
    for point in points_to_check:
        x, y = int(point[0]), int(point[1])
        if 0 <= x < track_surface.get_width() and 0 <= y < track_surface.get_height():
            pixel_color = track_surface.get_at((x, y))[:3]
            print(f"Corner pixel color: {pixel_color} at {point}")
            if pixel_color == off_color:
                print("Collision detected!")
                return True
    return False

# Game loop
running = True
while running:
    # Store previous car position for collision check
    previous_car_rect = car_rect.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    if keys[pygame.K_UP]:
        move_x = car_speed * math.sin(math.radians(car_angle))
        move_y = -car_speed * math.cos(math.radians(car_angle))
    if keys[pygame.K_DOWN]:
        move_x = -car_speed * math.sin(math.radians(car_angle))
        move_y = car_speed * math.cos(math.radians(car_angle))
    if keys[pygame.K_LEFT]:
        car_angle += rotation_speed
        car_image = pygame.transform.rotate(original_car_image, car_angle)
        car_rect = car_image.get_rect(center=previous_car_rect.center) # Keep center
    if keys[pygame.K_RIGHT]:
        car_angle -= rotation_speed
        car_image = pygame.transform.rotate(original_car_image, car_angle)
        car_rect = car_image.get_rect(center=previous_car_rect.center) # Keep center

    # Update car position
    car_rect.x += move_x
    car_rect.y += move_y

    # Check for collision
    if check_collision(car_rect, track_image, off_track_color):
        # If collision, revert to previous position
        car_rect = previous_car_rect

    # Keep car within screen bounds (still basic)
    if car_rect.left < 0:
        car_rect.left = 0
    if car_rect.right > screen_width:
        car_rect.right = screen_width
    if car_rect.top < 0:
        car_rect.top = 0
    if car_rect.bottom > screen_height:
        car_rect.bottom = screen_height

    # Draw everything
    screen.fill(white)
    screen.blit(track_image, track_rect)
    screen.blit(car_image, car_rect)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()