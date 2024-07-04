import serial
from time import*
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 300
GROUND_HEIGHT = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up box properties
box_width, box_height = 20, 20
box_color = (0,255,0)  # White color
box_speed = 5
box_spawn_interval = 500  # Interval to spawn a new box (in pixels)
character_velocity = 0  # Initial velocity
character_jump_velocity = -10  # Initial jump velocity
# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blowing Game!Nfekh Nfekh")

# Load character image
character_image = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.rect(character_image, WHITE, (0, 0, 50, 50))  # White rectangle for simplicity

# Set up the character
character_rect = character_image.get_rect()
character_rect.topleft = (100, HEIGHT - GROUND_HEIGHT - character_rect.height)

# Set up the ground
ground_rect1 = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
ground_rect2 = pygame.Rect(WIDTH, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)

# Ground movement variables
ground_speed = 5

# Clock to control the frame rate
clock = pygame.time.Clock()

# List to store boxes
boxes = []
# Main game loop
is_jumping = False
jump_count = 10
# Scoring
score = 0
font = pygame.font.Font(None, 36)
gameOver=False

# Load background music
pygame.mixer.music.load("C:\\Users\\PurplE\\Downloads\\Music\\Bolero.mp3")
pygame.mixer.music.set_volume(0.5)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music indefinitely

#load sound effect
sound_effect_file = "C:\\Users\\PurplE\\Downloads\\Music\\jump.wav"
sound_effect1= pygame.mixer.Sound(sound_effect_file)
sound_effect1.set_volume(0.1)  # Set the volume (0.0 to 1.0)
#load sound effect
sound_effect_file = "C:\\Users\\PurplE\\Downloads\\Music\\game over1.wav"
sound_effect = pygame.mixer.Sound(sound_effect_file)
sound_effect.set_volume(0.1)  # Set the volume (0.0 to 1.0)
#load sound effect
sound_effect_file = "C:\\Users\\PurplE\\Downloads\\Music\\LEVELUP2.wav"
sound_effect2= pygame.mixer.Sound(sound_effect_file)
sound_effect2.set_volume(0.1)  # Set the volume (0.0 to 1.0)
# Flag to track if the sound effect has been played
sound_effect_played = False
arduinoData=serial.Serial('com5',115200)

while True:
    #getting data from arduino
    while (arduinoData.inWaiting()==0):
        pass
    dataPacket = arduinoData.readline() #reply
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(",")
    pressure=float(splitPacket[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not gameOver:
        

        # Check for jump
        if not is_jumping and character_rect.y >= HEIGHT - GROUND_HEIGHT - character_rect.height:
            if pressure>0.006:
                is_jumping = True
                sound_effect1.play()
                character_velocity = character_jump_velocity

        # Update character position based on velocity
        character_rect.y += character_velocity

        # Update velocity due to gravity
        if character_rect.y < HEIGHT - GROUND_HEIGHT - character_rect.height:
            character_velocity += 0.5
        else:
            character_rect.y = HEIGHT - GROUND_HEIGHT - character_rect.height
            character_velocity = 0
            is_jumping = False

        # Move the ground
        ground_rect1.x -= ground_speed
        ground_rect2.x -= ground_speed

        # Reset the ground position when it moves out of the screen
        if ground_rect1.right <= 0:
            ground_rect1.x = ground_rect2.right

        if ground_rect2.right <= 0:
            ground_rect2.x = ground_rect1.right

        # Limit character position to stay above the ground
        character_rect.y = min(character_rect.y, HEIGHT - GROUND_HEIGHT - character_rect.height)




        # Clear the screen
        screen.fill(BLACK)

        # Spawn a new box at regular intervals
        if len(boxes) == 0 or boxes[-1].x < WIDTH - box_spawn_interval:
            box_x = WIDTH
            box_y = random.randint(0, HEIGHT - box_height - GROUND_HEIGHT)
            boxes.append(pygame.Rect(box_x, box_y, box_width, box_height))
            

        # Move the boxes horizontally
        for box in boxes:
            box.x -= box_speed
            # Check for collisions with character
            if character_rect.colliderect(box):
                gameOver=True
            
        # Remove boxes that go off the left edge
        boxes = [box for box in boxes if box.right > 0]
        # Draw the boxes
        for box in boxes:
            pygame.draw.rect(screen, box_color, box)
        # Draw the ground
        pygame.draw.rect(screen, WHITE, ground_rect1)
        pygame.draw.rect(screen, WHITE, ground_rect2)

        # Draw the character
        screen.blit(character_image, character_rect.topleft)

            # Update score
        score += .5

        # Display score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))
        if score ==900:
            box_speed = 5.5  # increase the speed of boxes
            sound_effect2.play()
        if score==1500:
            box_speed = 6  # increase the speed of boxes
            sound_effect2.play()
        if score==2000:
            box_speed = 6.5  # increase the speed of boxes
            sound_effect2.play()
        if score==2600:
            box_speed = 9  # increase the speed of boxes
            sound_effect2.play()

        # Update the display
        pygame.display.flip()


        # Cap the frame rate
        clock.tick(FPS)
        sound_effect_played = False
    else:
        
        # If game is over, display "Game Over" message
        #print("Game Over!Nfakh mzyan, Score:", score)
        gameOver_text = font.render("Game Over!Nfakh mzyan, Score:" + str(score), True,(245, 66, 90))
        screen.blit(gameOver_text, (200,120))
        restart_text = font.render("R Bach T3awd", True, WHITE)
        screen.blit(restart_text, (280, 180))
        pygame.mixer.music.stop()
        if not sound_effect_played:
            sound_effect.play()
            sound_effect_played = True 
        if keys[pygame.K_r]:
            gameOver = False
            score = 0
            character_rect.topleft = (100, HEIGHT - GROUND_HEIGHT - character_rect.height)
            boxes = []  # Clear the boxes
            pygame.mixer.music.load("C:\\Users\\PurplE\\Downloads\\Music\\Bolero.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  
        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)
