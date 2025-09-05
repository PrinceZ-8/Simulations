import pygame
import math as m

#Important Variables
running = True

# Initialize pygame
pygame.init()
# Set up display
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray Tracing 2.0")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (155,155,155)
BLACK = (0,0,0)
RED = (255,0,0)

#drag = False
#objs = []

class LightSource:
    def __init__(self, surface, size, pos_x, pos_y, rays, color):
        self.surface = surface
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rays = rays
        self.color = color

        #self.mouse_x , self.mouse_y = pygame.mouse.get_pos()
        self.angle = 2 * m.pi / self.rays
        self.drag = False
        self.flag = False

    def draw_source(self):
        pygame.draw.circle(self.surface, self.color, [self.pos_x, self.pos_y], self.size)

    def draw_rays(self, length, obj_list):
        for r in range(self.rays):
            angle = r * self.angle
            ray_end_width = self.pos_x + (m.cos(angle) * length)
            ray_end_height = self.pos_y - (m.sin(angle) * length)

            closest_hit = 0
            closest_dist = float('inf')

            for obj in obj_list:
                #Calculating the Distance from the Light Source to Object - OBJECT,SOURCE,DISTANCE
                OSD = m.sqrt((obj.pos_x - self.pos_x) ** 2 + (obj.pos_y - self.pos_y) ** 2)

                # Using the OSD, the endpoints of the rays are calculated
                x_coord = self.pos_x + (m.cos(angle) * OSD)
                y_coord = self.pos_y - (m.sin(angle) * OSD)
                dist_to_obj = m.sqrt((x_coord - obj.pos_x) ** 2 + (y_coord - obj.pos_y) ** 2)

                # Using distance formula to check if endpoints of rays are inside Object, yes --> flags ray stop there
                if dist_to_obj <= obj.size:
                    #Finds the closest one that blocks the ray.
                    if OSD < closest_dist:
                        closest_hit = (x_coord, y_coord)
                        closest_dist = OSD
                # Otherwise if calculated end point not in object then proceed to normal endpoint

            if closest_hit != 0:
                pygame.draw.line(self.surface, self.color, [self.pos_x, self.pos_y], closest_hit, 2)
            else:
                pygame.draw.line(self.surface, self.color, [self.pos_x, self.pos_y], [ray_end_width, ray_end_height], 2)

            #updates the angle
            angle = angle + (2 * m.pi / self.rays)


    def was_clicked(self,mx, my):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if  m.sqrt((mx-self.pos_x)**2 + (my-self.pos_y)**2) <= self.size:
                self.drag = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.drag = False

    def was_dragged(self, mx, my):
        if self.drag:
            self.pos_x, self.pos_y = mx, my

#-------------------------------------------------------------------------------------

class Objects:
    def __init__(self, surface, obj_type, size, pos_x, pos_y, color):
        self.surface = surface
        self.obj_type = obj_type
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color

        self.drag = False

        if obj_type == "Square":
            rect = pygame.Rect(self.pos_x, self.pos_y, self.size, self.size)
            self.pos_x, self.pos_y = rect.center


    def draw_source(self):
        if self.obj_type == "Circle":
            pygame.draw.circle(self.surface, self.color, [self.pos_x, self.pos_y], self.size)

        if self.obj_type == "Square":
            pygame.draw.rect(self.surface, self.color, [self.pos_x, self.pos_y, self.size, self.size])

    def was_clicked(self, mx, my):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if  m.sqrt((mx-self.pos_x)**2 + (my-self.pos_y)**2) <= self.size:
                self.drag = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.drag = False

    def was_dragged(self, mx, my):
        if self.drag:
            self.pos_x, self.pos_y = mx, my

#-------------------------------------------------------------------------------------



Sun = LightSource(screen, 50, 100, 100,200, WHITE)
#Star = LightSource(screen, 35, 600, 600,200, WHITE)

earth = Objects(screen, "Circle", 25, 200, 200, BLUE)
mars = Objects(screen, "Circle", 20, 300, 300, RED)
mercury = Objects(screen, "Circle", 15, 400, 400, GREY)
#mirror = Objects(screen, "Square", 50, 600, 600, GREY)

objs = [earth, mars, mercury]

# Game loop
while running:
    screen.fill(BLACK)  # Clear the screen
    Sun.draw_source()
    Sun.draw_rays(1500, objs)

    #Star.draw_source()
    #Star.draw_rays(1500, objs)

    earth.draw_source()
    mars.draw_source()
    mercury.draw_source()
    #mirror.draw_source()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        Sun.was_clicked(mouse_x, mouse_y)
        earth.was_clicked(mouse_x, mouse_y)
        #Star.was_clicked(mouse_x, mouse_y)
        mars.was_clicked(mouse_x, mouse_y)
        mercury.was_clicked(mouse_x, mouse_y)
        #mirror.was_clicked(mouse_x, mouse_y)

    #mouse_x, mouse_y = pygame.mouse.get_pos()
    Sun.was_dragged(mouse_x, mouse_y)
    earth.was_dragged(mouse_x, mouse_y)
    #Star.was_dragged(mouse_x, mouse_y)
    mars.was_dragged(mouse_x, mouse_y)
    mercury.was_dragged(mouse_x, mouse_y)
    #mirror.was_dragged(mouse_x, mouse_y)

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()