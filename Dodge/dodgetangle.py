import pygame
import random
import time

# Initialize the font module in pygame
pygame.font.init()

# Constants for player
player_width = 30
player_height = 60
player_vel = 12

# Constants for comets
comet_height = 15
comet_width = 5
comet_vel = 3

# Font for displaying text
FONT = pygame.font.SysFont('Times New Roman', 25)

# Screen dimensions
width, height = 1366, 768
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("DodgeTangle")

# Load background image
BG = pygame.image.load("space.jpeg")

# Function to draw elements on the screen
def draw(player, elapsed_time, comets):
    win.blit(BG, (0, 0))

    # Display elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    win.blit(time_text, (10, 10))

    # Draw the player rectangle
    pygame.draw.rect(win, "green", player)

    # Draw comets
    for comet in comets:
        pygame.draw.rect(win, "white", comet)

    # Update the display
    pygame.display.update()

# Main game loop
def main():
    run = True

    # Initialize player rectangle
    player = pygame.Rect(200, height - player_height, player_width, player_height)

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # Variables for managing comets
    comet_add_increment = 2000
    comet_count = 0
    comets = []
    hit = False

    while run:
        # Increment comet_count and get elapsed time
        comet_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Add new comets at regular intervals
        if comet_count >= comet_add_increment:
            for _ in range(3):
                # Generate random x-coordinate for comets
                comet_x = random.randint(0, width - comet_width)
                comet = pygame.Rect(comet_x, -comet_height, comet_width, comet_height)
                comets.append(comet)
            # Adjust comet_add_increment for more challenging gameplay
            comet_add_increment = max(200, comet_add_increment - 50)
            comet_count = 0

        for event in pygame.event.get():
            # Check for quit event
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        # Move player based on key inputs
        if keys[pygame.K_LEFT] and player.x - player_vel >= 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player_width <= width:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel >= 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player_height <= height:
            player.y += player_vel

        for comet in comets[:]:
            # Move comets downward
            comet.y += comet_vel
            # Remove comets that go off the screen
            if comet.y > height:
                comets.remove(comet)
            # Check for collision with player
            elif comet.y + comet.height >= player.y and comet.colliderect(player):
                comets.remove(comet)
                hit = True
                break

        if hit:
            # Display "You Lost" message
            lost_text = FONT.render("You Lost!!! :'-(", 1, "white")
            win.blit(lost_text, (width // 2 - lost_text.get_width() // 2, height // 2 - lost_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(500)
            break

        # Draw elements on the screen
        draw(player, elapsed_time, comets)

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main()