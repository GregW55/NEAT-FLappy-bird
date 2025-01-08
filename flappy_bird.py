from pickle import GLOBAL

import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 690
WIN_HEIGHT = 1000
FPS = 300
GEN = 0
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))), ]
PIPE_IMG = pygame.transform.scale_by(pygame.image.load(os.path.join("imgs", "pipe.png")), 2.4)
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale_by(pygame.image.load(os.path.join("imgs", "bg.png")), 2.4)

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # how much tilt degree the bird has
    ROT_VEL = 20  # how much you will rotate on each frame
    ANIMATION_TIME = 5  # how long each bird animation is displayed

    def __init__(self, x, y):  # x/y = starting position of each bird
        self.x = x
        self.y = y
        self.tilt = 0  # how tilted the bird is
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0  # which img for the bird is being shown, allows animation
        self.img = self.IMGS[0]

    def jump(self):  # function to have the bird move upward
        self.vel = -10.5  # pygames 0,0 is top left so to go up you need negative velocity
        self.tick_count = 0  # when the bird last jumped
        self.height = self.y  # where the bird originally started jumping from

    def move(self):  # function called every frame to move the bird
        self.tick_count += 1
        # displacement, how many pixels we are going up or down this frame
        # (velocity x tick count) + (1.5 x tick_count^2)
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d  # add displacement value to current y position to determine new position on screen

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1  # how many times in a row weve shown one image

        if self.img_count < self.ANIMATION_TIME:  # if image count is less than 5(animation_time)
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:  # if image count is less than 10(animation time x 2)
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:  # if image count is less than 15 (animation time x 3)
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:  # if image count is less than 20 ( animation time x 4)
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:  # if image count is less than 21(animation time x 4 + 1)
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """Collision for objects"""
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200  # how much space inbetween the pipes
    VEL = 5  # bird doesnt move left/right but pipes will

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)  # pipe from the top facing upside down
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False  # if the bird has passed by this pipe
        self.set_height()  # how tall each pipe is, and the gap between them

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))  # offset from the bird to the top mask
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))  # offset from the bird to the bottom mask

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)  # point of overlap between the bird mask and bottom pipe using the offset
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:  # if the bird mask overlaps either the top or bottom pipe
            return True

        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:  # if the base is off the screen
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Generation: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()

def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(930)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1  # Take one fitness point away if a bird hits a pipe
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # if the pipe is off the screen
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 930 or bird.y < 0:  # if bird hits the floor or goes above bounds
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)  # Population

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,500)  # amount of generations, in this case 100

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)