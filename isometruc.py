import pygame
import pygame.locals
import random

RECT_COLOR = pygame.Color(150, 150, 200)
BG_COLOR = pygame.Color(70, 70, 70)
TRANSPARANT = pygame.Color(0, 0, 0, 0)
WIN_WIDTH = 800
WIN_HEIGHT = 600
FLOOR_IMAGE = "pinkCube.png"
PLAYER_IMAGE = "greenCube.png"
GOAL_IMAGE = "blueCube.png"
ROW_NUM = 50
LINE_NUM = 50


X_VECT = (1, 0.5)
Y_VECT = (-1, 0.5)
TRANSFORMER = 4
IMAGE_WIDTH = 21* TRANSFORMER
IMAGE_HEIGHT = 22 * TRANSFORMER
if False:
    WIDTH_OFFSET  = -IMAGE_WIDTH/2 + WIN_WIDTH/2
    HEIGHT_OFFSET = 2*IMAGE_HEIGHT
else:
    WIDTH_OFFSET  = 0 
    HEIGHT_OFFSET = 0
INT_MAX = 9999999

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Vec2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y

    def __repr__(self):
       return f"x: {self.x}, y: {self.y}"

def vec2_mul_mat22(vec, mat):
    vec1 = Vec2(0, 0)
    vec1.x = vec.x*mat.a + vec.y*mat.c
    vec1.y = vec.x*mat.b + vec.y*mat.d
    return vec1

def vec2_mul_int(vec, i):
    vec1 = Vec2(0,0)
    vec1.x = vec.x * i
    vec1.y = vec.y * i
    return vec1

class Mat22():
    def __init__(self, e1, e2):
        self.a = e1.x
        self.b = e2.x
        self.c = e1.y
        self.d = e2.y

    def invert(self):
        det = 1/(self.a * self.d - self.c * self.b)
        a = det * self.d
        b = det * -self.b
        c = det * -self.c
        d = det * self.a
        return Mat22(Vec2(a, c), Vec2(b,d))


    def __repr__(self):
        return f"a: {self.a}, b: {self.b}, c: {self.c}, d: {self.d}"

    def to_vec2(self):
        return Vec2(self.a, self.c), Vec2(self.b, self.d)


class Image():
    def __init__(self, image, pos, top, picname):
        self.image = image
        self.pos = pos
        self.top = top
        self.picname = picname

def to_iso(vec, Mat_Co):
    i, j = Mat_Co.to_vec2()
    i1 = vec2_mul_int(i, vec.x)
    j1 = vec2_mul_int(j, vec.y)
    res = Vec2(i1.x + j1.x, i1.y + j1.y)
    return res

def to_screen(vec, Mat_Co):
    iMat_Co = Mat_Co.invert()
    return vec2_mul_mat22(vec, iMat_Co)

def load_tile_table():
    tile_table = []
    picname = FLOOR_IMAGE
    image = pygame.image.load(FLOOR_IMAGE).convert_alpha()
    image = pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
    for x in range(LINE_NUM):
        line = []
        tile_table.append(line)
        for y in range(ROW_NUM):
            pos = Point(x, y)
            top = [(pos.x, pos.y),
                   (pos.x, pos.y),
                   (pos.x, pos.y),
                   (pos.x, pos.y)]
            line.append(Image(image, pos, top, picname))
    return tile_table

def load_table_on_screen(table):
    iw, ih = table[0][0].image.get_size()
    x_vect = Vec2(X_VECT[0], X_VECT[1])
    y_vect = Vec2(Y_VECT[0], Y_VECT[1])
    for line in table:
        for image in line:
            screen_coordonates =  to_iso(Vec2(image.pos.x, image.pos.y),
                                         Mat22(vec2_mul_int(x_vect, IMAGE_WIDTH/2),
                                               vec2_mul_int(y_vect, IMAGE_HEIGHT/2)))

            screen_coordonates.x -= IMAGE_WIDTH //2
            screen_coordonates.x += WIN_WIDTH //2
            screen_coordonates.y -= IMAGE_HEIGHT * 10

            screen.blit(image.image, (screen_coordonates.x,
                                      screen_coordonates.y))

class Player:
    def __init__(self):
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        self.pos = Vec2(random.randint(21,29), random.randint(21,29))
        goal = Vec2(random.randint(21,29), random.randint(21,29))
        while goal == self.pos:
            goal = Vec2(random.randint(21,29), random.randint(21,29))
        self.goal = goal

    def set_goal(self):
        goal = Vec2(random.randint(21,29), random.randint(21,29))
        while goal == self.pos:
            goal = Vec2(random.randint(21,29), random.randint(21,29))
        self.goal = goal

    def load_player(self, screen):
        x_vect = Vec2(X_VECT[0], X_VECT[1])
        y_vect = Vec2(Y_VECT[0], Y_VECT[1])
        screen_coordonates = to_iso(self.pos, Mat22(vec2_mul_int(x_vect, IMAGE_WIDTH/2),
                                                    vec2_mul_int(y_vect, IMAGE_HEIGHT/2)))
        screen_coordonates.x += WIN_WIDTH // 2 - IMAGE_WIDTH // 2
        screen_coordonates.y -= IMAGE_HEIGHT * 10
        screen.blit(self.image, (screen_coordonates.x , screen_coordonates.y + IMAGE_HEIGHT))


    def load_goal(self, screen):
        x_vect = Vec2(X_VECT[0], X_VECT[1])
        y_vect = Vec2(Y_VECT[0], Y_VECT[1])
        screen_coordonates = to_iso(self.goal, Mat22(vec2_mul_int(x_vect, IMAGE_WIDTH/2),
                                                    vec2_mul_int(y_vect, IMAGE_HEIGHT/2)))
        screen_coordonates.x += WIN_WIDTH // 2 - IMAGE_WIDTH // 2
        screen_coordonates.y -= IMAGE_HEIGHT * 10
        goal_image = pygame.image.load(GOAL_IMAGE).convert_alpha()
        goal_image = pygame.transform.scale(goal_image, (IMAGE_WIDTH, IMAGE_HEIGHT))

        screen.blit(goal_image, (screen_coordonates.x , screen_coordonates.y + IMAGE_HEIGHT))

    def move(self, s):
        if s == "up":
            self.pos.y -= 1
        elif s == "down":
            self.pos.y += 1
        elif s == "right":
            self.pos.x += 1
        elif s == "left":
            self.pos.x -= 1

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
    screen.fill(BG_COLOR);

    table = load_tile_table()
    load_table_on_screen(table)
    pygame.display.flip()


    mem = (-1, -1)
    end = False
    x_vect = Vec2(X_VECT[0], X_VECT[1])
    y_vect = Vec2(Y_VECT[0], Y_VECT[1])
    goal = False
    player = Player()
    player.load_player(screen)
    
    while not end:
        if goal == False:
            player.set_goal()
            player.load_goal(screen)
            goal = True
        pygame.display.update()
        e = pygame.event.wait()
        if e.type == pygame.locals.QUIT:
            end = True
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                player.move("up")
            elif e.key == pygame.K_DOWN:
                player.move("down")
            elif e.key == pygame.K_LEFT:
                player.move("left")
            elif e.key == pygame.K_RIGHT:
                player.move("right")
            load_table_on_screen(table)
            player.load_goal(screen)
            player.load_player(screen)
        if player.pos.x == player.goal.x and player.pos.y == player.goal.y:
            goal = False
