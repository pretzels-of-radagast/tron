import pygame, time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 660  # window dimensions
offset = SCREEN_WIDTH - SCREEN_HEIGHT  # vertical space at top of window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # creates window
pygame.display.set_caption("Tron")  # sets window ///////////////


class Player:
   def __init__(self, x, y, dir, colour, speed=1):
       self.x = x
       self.y = y
       self.speed = speed
       self.dir = dir
       self.colour = colour
       self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # player rect object

       self.is_boost = False
       self.start_boost = time.time()  # used to control boost length
       self.boosts = 3

   def draw(self):
       self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # redefines rect
       pygame.draw.rect(screen, self.colour, self.rect, 0)  # draws player onto screen

   def move(self):
       if not self.is_boost:  # player isn't currently boosting
           self.x += self.dir[0]
           self.y += self.dir[1]
       else:
           self.x += self.dir[0] * 2
           self.y += self.dir[1] * 2

   def set_dir(self, x, y):
       if not (self.dir[0] != x and self.dir[1] == y or self.dir[0] == x and self.dir[1] != y):
           self.dir = x, y

   def boost(self):
       if self.boosts > 0:
           self.boosts -= 1
           self.is_boost = True
           self.start_boost = time.time()

def gradient(c1, c2, t):
   r = c1[0] + int((c2[0] - c1[0]) * t)
   g = c1[1] + int((c2[1] - c1[1]) * t)
   b = c1[2] + int((c2[2] - c1[2]) * t)

   return (r,g,b)

def reset():
   new_p1 = Player(50, SCREEN_HEIGHT / 2, (2, 0), P1_COLOUR)
   new_p2 = Player(SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2, (-2, 0), P2_COLOUR)
   return new_p1, new_p2


BG_COLOUR = (54, 54, 53)
WALL_COLOUR = (72, 72, 71)
P1_COLOUR = (219, 41, 85)
P2_COLOUR = (108, 145, 191)

# BG_COLOUR = (0, 255, 0)
# WALL_COLOUR = (0, 0, 0)
# P1_COLOUR = (0, 0, 255)
# P2_COLOUR = (255, 0, 0)

FONT_COLOUR = (245, 251, 239)
# FONT_COLOUR = (255, 255, 255)

font = pygame.font.SysFont('roboto mono', 70)

objects = []  # list of all the player objects
path = []  # list of all the path rects in the game
p1 = Player(50, (SCREEN_HEIGHT - offset) / 2, (2, 0), P1_COLOUR)  # creates player
p2 = Player(SCREEN_WIDTH - 50, (SCREEN_HEIGHT - offset) / 2, (-2, 0), P2_COLOUR)
objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))

player_score = [0, 0]  # current player score

wall_rects = [pygame.Rect((0, 0, 30, SCREEN_HEIGHT)),  # left
             pygame.Rect((0, 0, SCREEN_WIDTH, 80)),  # top
             pygame.Rect((SCREEN_WIDTH - 20, 0, 30, SCREEN_HEIGHT)),  # right
             pygame.Rect((0, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 30))]  # bottom

new = False

clock = pygame.time.Clock()  # used to regulate FPS
check_time = time.time()  # used to check collisions with rects

keys = [False] * 10

prev_winner = None
FADE_TIMER = 180
timer = 0

while True:
   for event in pygame.event.get():  # gets all event in last tick
       if event.type == pygame.QUIT:  # close button pressed
           pygame.quit()
           quit()
       elif event.type == pygame.KEYDOWN:  # keyboard key pressed
           # P1
           if event.key == pygame.K_w:
               objects[0].set_dir(0, -2)
           elif event.key == pygame.K_s:
               objects[0].set_dir(0, 2)
           elif event.key == pygame.K_a:
               objects[0].set_dir(-2, 0)
           elif event.key == pygame.K_d:
               objects[0].set_dir(2, 0)
           elif event.key == pygame.K_q:
               objects[0].boost()

           # P2
           if event.key == pygame.K_UP:
               objects[1].set_dir(0, -2)
           elif event.key == pygame.K_DOWN:
               objects[1].set_dir(0, 2)
           elif event.key == pygame.K_LEFT:
               objects[1].set_dir(-2, 0)
           elif event.key == pygame.K_RIGHT:
               objects[1].set_dir(2, 0)
           elif event.key == pygame.K_SLASH:
               objects[1].boost()
       elif event.type == pygame.KEYUP:
           if event.key == pygame.K_w:
               keys[0] = False
           elif event.key == pygame.K_s:
               keys[0] = False
           elif event.key == pygame.K_a:
               keys[0] = False
           elif event.key == pygame.K_d:
               keys[0] = False
           elif event.key == pygame.K_q:
               keys[0] = False
           # === Player 2 === #
           if event.key == pygame.K_UP:
               keys[0] = False
           elif event.key == pygame.K_DOWN:
               keys[0] = False
           elif event.key == pygame.K_LEFT:
               keys[0] = False
           elif event.key == pygame.K_RIGHT:
               keys[0] = False
           elif event.key == pygame.K_SLASH:
               keys[0] = False

   # P1
   if keys[0]: objects[0].dir = (0, -2)
   elif keys[1]: objects[0].dir = (0, 2)
   elif keys[2]: objects[0].dir = (-2, 0)
   elif keys[3]: objects[0].dir = (2, 0)
   elif keys[4]: objects[0].boost()

   # P2
   if keys[5]: objects[1].dir = (0, -2)
   elif keys[6]: objects[1].dir = (0, 2)
   elif keys[7]: objects[1].dir = (-2, 0)
   elif keys[8]: objects[1].dir = (2, 0)
   elif keys[9]: objects[1].boost()

   screen.fill(BG_COLOUR)  # clears the screen

   if timer > 0:
       timer -= 1
       final_wall_colour = gradient(WALL_COLOUR, prev_winner.colour, timer / FADE_TIMER * 0.3)
   else:
       final_wall_colour = WALL_COLOUR

   for r in wall_rects:
       pygame.draw.rect(screen, final_wall_colour, r)  # draws the walls

   for o in objects:
       if time.time() - o.start_boost >= 0.5:  # limits boost to 0.5s
           o.is_boost = False

       if (o.rect, '1') in path or (o.rect, '2') in path \
               or o.rect.collidelist(wall_rects) > -1:  # collided with path or wall
           # prevent player from hitting the path they just made
           if (time.time() - check_time) >= 0.1:
               check_time = time.time()

               timer = FADE_TIMER
               if o.colour == P1_COLOUR:
                   prev_winner = objects[1]
                   player_score[1] += 1
               else:
                   prev_winner = objects[0]
                   player_score[0] += 1

               new = True
               new_p1, new_p2 = reset()
               objects = [new_p1, new_p2]
               path = [(p1.rect, '1'), (p2.rect, '2')]
               break
       else:  # not yet traversed
           path.append((o.rect, '1')) if o.colour == P1_COLOUR else path.append((o.rect, '2'))

       o.draw()
       o.move()

   for r in path:
       if new:  # empties the path - needs to be here to prevent graphical glitches
           path = []
           new = False
           break
       if r[1] == '1':
           pygame.draw.rect(screen, P1_COLOUR, r[0], 0)
       else:
           pygame.draw.rect(screen, P2_COLOUR, r[0], 0)

   # display the current score on the screen
   score_text = font.render(f'{player_score[0]} : {player_score[1]}', True, FONT_COLOUR)
   score_text_pos = (SCREEN_WIDTH / 2 - (score_text.get_width() / 2), 20)
   screen.blit(score_text, score_text_pos)

   pygame.display.update()  # flips display

   clock.tick(60)  # regulates FPS

