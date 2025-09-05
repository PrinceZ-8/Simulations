import pygame
import math as m

running = True
#osd = []
ray_count = 200
ray_length = 1000
angle = 2 * m.pi / ray_count

sun_size = 50
sun_x , sun_y = 200,100
sun_drag = False

earth_x , earth_y = 500, 500
earth_size = 50
earth_drag = False

mirror_x , mirror_y = 200, 300
mirror_size = 40
mirror_drag = False

# Initialize pygame
pygame.init()
# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray Tracing 1.0")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (155,155,155)
BLACK = (0,0,0)

# Game loop
while running:
    screen.fill(BLACK)  # Clear the screen

    #Sun
    for r in range(ray_count):
        rew = sun_x + (m.cos(angle) * ray_length)
        reh = sun_y - (m.sin(angle) * ray_length)

        #Calculating the Distance from the Light Source to Object - OBJECT,SOURCE,DISTANCE
        osd = m.sqrt((earth_x-sun_x)**2 + (earth_y-sun_y)**2)
        osd2 = m.sqrt((mirror_x+(mirror_size/2)-sun_x)**2 + (mirror_y+(mirror_size/2)-sun_y)**2)

        #Using the OSD, the endpoints of the rays are calculated
        ex_coord, ey_coord = sun_x + (m.cos(angle) * osd) , sun_y - (m.sin(angle) * osd)
        mx_coord, my_coord = sun_x + (m.cos(angle) * osd2) , sun_y - (m.sin(angle) * osd2)

        #Using distance formula to check if endpoints of rays are inside Earth, yes --> ray stop there
        if m.sqrt((ex_coord-earth_x)**2 + (ey_coord-earth_y)**2) <= earth_size:
            pygame.draw.line(screen, WHITE, [sun_x, sun_y], [ex_coord, ey_coord], 2)
        # Otherwise if calculated end point not in object then proceed to normal endpoint
        else:
            pygame.draw.line(screen, WHITE, [sun_x, sun_y], [rew, reh], 2)

        #if m.sqrt((mx_coord-earth_x)**2 + (my_coord-earth_y)**2) <= mirror_size:
         #pygame.draw.line(screen, WHITE, [sun_x, sun_y], [mx_coord, my_coord], 2)
         #pygame.draw.line(screen, WHITE, [mx_coord, my_coord], [0, 0], 2)

        angle = angle + (2 * m.pi / ray_count)
    pygame.draw.circle(screen, WHITE, [sun_x, sun_y], sun_size)

    #Earth Drawn to Screen
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, BLUE, [earth_x, earth_y], earth_size)

    #Mirror Drawn to Screen
    pygame.draw.rect(screen, GREY, pygame.Rect(mirror_x, mirror_y, mirror_size, mirror_size))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Was Something Clicked?
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if  m.sqrt((mouse_x-sun_x)**2 + (mouse_y-sun_y)**2) <= sun_size:
                sun_drag = True
            if  m.sqrt((mouse_x-earth_x)**2 + (mouse_y-earth_y)**2) <= earth_size:
                earth_drag = True
            if (mouse_x > mirror_x) and (mouse_x < mirror_x+mirror_size) and (mouse_y > mirror_y) and (mouse_y < mirror_y+mirror_size):
                mirror_drag = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            sun_drag = False
            earth_drag = False
            mirror_drag = False

    #IS SUN OR EARTH Being Dragged Around?
    if sun_drag:
        sun_x, sun_y = mouse_x, mouse_y
    if earth_drag:
        earth_x , earth_y = mouse_x, mouse_y
    if mirror_drag:
        mirror_x, mirror_y = mouse_x, mouse_y

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()