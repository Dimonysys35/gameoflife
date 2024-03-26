import pygame
from pygame.locals import *
import random
from pprint import pprint as pp
import math

class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.tolive = [2,3]
        self.width = width
        self.height = height 
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def create_grid(self, randomize: bool=False):
        if randomize:
            grid = []
            for i in range(self.height // self.cell_size):
                grid.append([])
                for j in range(self.width // self.cell_size):
                    if random.randrange(0, 6) == 0:
                        grid[i].append(1)
                    else:
                        grid[i].append(0)
                    #grid[i].append(random.choice((0, 1)))
        else:
            grid = [[0 for j in range(self.cell_size)] for i in range(self.cell_size) ]
        return grid
    
    def draw_cells(self):
        y = 0
        x = 0
        for line in self.grid:
            x = 0
            for cell in line:
                if cell == 1:
                    pygame.draw.rect(self.screen, pygame.Color("green"), (x, y, self.cell_size, self.cell_size))
                    
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), (x, y, self.cell_size, self.cell_size))
                #cell_neighbours = self.get_neighbours(y / self.cell_size, x / self.cell_size)
                #for i in range(cell_neighbours):
                #    pygame.draw.circle(self.screen, pygame.Color("blue"), (x + self.cell_size / 2 + self.cell_size * 0.25 * math.sin(math.radians(i * 45)), 
                #                                                               y + self.cell_size / 2 + self.cell_size * 0.25 * math.cos(math.radians(i * 45))), 3)
                x += self.cell_size
            y += self.cell_size
    
    def update_grid(self):
        # main game logic
        # create & kill cells

        res_grid = [[] for i in range(self.height // self.cell_size)] #self.create_grid(randomize= False)
        y = 0
        x = 0
        for line in self.grid:
            x = 0
            for cell in line:
                cell_neighbours = self.get_neighbours(y, x)
                neighbours_num = cell_neighbours
                #print(neighbours_num)
                if neighbours_num == 3 and (self.grid[y][x] == 0 or self.grid[y][x] == 1):
                    res_grid[y].append(1)
                elif neighbours_num  == 2 and self.grid[y][x] == 1:
                    res_grid[y].append(1)
                else:
                    res_grid[y].append(0)
                x += 1 
            y += 1
        return res_grid

    def get_neighbours(self, y, x):
        meow = 0
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if 0 <= y + di < len(self.grid) and 0 <= x + dj < len(self.grid[0]) and not (di == 0 and dj == 0):
                        if self.grid[int(y + di)][int(x + dj)] == 1:
                            meow += 1
        return meow
    
    def in_bounds(self, i, j):                                                     
        return 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0])                           

    def run(self) -> None:
        self.grid = self.create_grid(randomize = True) 
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Gay of life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    pass
                    #print(event)
            self.draw_cells()
            pygame.display.flip()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
            self.grid = self.update_grid()

        pygame.quit()
    
if __name__ == "__main__":
    game = GameOfLife(640, 480, 20, 2)
    game.run()