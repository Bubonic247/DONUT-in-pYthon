import os
from math import cos, sin
import pygame
import colorsys

# Color palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
hue = 0

# Window settings
os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 800, 800
FPS = 60

# Pixel settings
pixel_width = 20
pixel_height = 20

# Screen settings
x_pixel = 0
y_pixel = 0
screen_width = WIDTH // pixel_width
screen_height = HEIGHT // pixel_height
screen_size = screen_width * screen_height

# Rotation angles
A, B = 0, 0

# Spacing between theta and phi
theta_spacing = 10
phi_spacing = 3

# Character set for rendering
chars = ".,-~:;=!*#$@"

# Donut settings
R1 = 10
R2 = 20
K2 = 200
K1 = screen_height * K2 * 3 / (8 * (R1 + R2))

# Pygame initialization
pygame.init()

# Screen and font setup
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20, bold=True)

# HSV to RGB conversion function
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Text rendering function
def text_display(char, x, y):
    text = font.render(str(char), True, hsv2rgb(hue, 1, 1))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

# Main loop variables
k = 0
paused = False
running = True

while running:
    clock.tick(FPS)
    pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)

    # Donut rendering
    output = [' '] * screen_size
    zbuffer = [0] * screen_size

    for theta in range(0, 628, theta_spacing):  
        for phi in range(0, 628, phi_spacing):  

            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi = cos(phi)
            sinphi = sin(phi)

            # x, y coordinates before revolving
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D (x, y, z) coordinates after rotation
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z  

            # x, y projection
            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            position = xp + screen_width * yp

            # Luminance (L ranges from -sqrt(2) to sqrt(2))
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (
                cosA * sintheta - costheta * sinA * sinphi)

            if ooz > zbuffer[position]:
                zbuffer[position] = ooz  
                luminance_index = int(L * 8)  
                output[position] = chars[luminance_index if luminance_index > 0 else 0]

    # Rendering the donut
    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display(output[k], x_pixel, y_pixel)
            k += 1
        x_pixel = 0
    y_pixel = 0
    k = 0

    # Rotation update
    A += 0.15
    B += 0.035

    # Hue update
    hue += 0.005

    # Update display if not paused
    if not paused:
        pygame.display.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused