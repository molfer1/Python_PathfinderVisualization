import pygame
import time

COLOR_CELL = [40, 40, 40]
COLOR_CELL_BORDER = [150, 150, 150]
COLOR_TEXT = [200, 200, 200]

class Visualizer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cost = 0

    def initMap(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(COLOR_CELL)
        pygame.display.set_caption("A* Path Finding Visualization")

        self.visualizeMap()

    def visualizeMap(self):
        x = 0
        y = 0
        cell_count = self.width // 20
        for _ in range(cell_count):
            pygame.draw.aaline(self.screen, COLOR_CELL_BORDER, (0, y), (self.width, y))
            pygame.draw.aaline(self.screen, COLOR_CELL_BORDER, (x, 0), (x, self.height - 40))
            x += 20
            y += 20

    def fillCell(self, x, y, color):
        if color == [220, 220, 220]:
            # PATH
            self.cost += 1
            text = pygame.font.Font('freesansbold.ttf', 14).render(f"Path length: {self.cost} ", True, COLOR_TEXT, COLOR_CELL)
            textRect = text.get_rect()
            textRect.center = (75, self.height - 20)
            self.screen.blit(text, textRect)

            time.sleep(0.1)
        elif color == [240, 100, 50] or color == [0, 200, 0]:
            # SEARCH FOR COST
            time.sleep(0.004)

        rec = pygame.Rect(y*20, x*20, 19, 19)
        pygame.draw.rect(self.screen, color, rec)
        pygame.display.update(rec)

    def getCell(self, x, y):
        return x - (x % 20), y - (y % 20)


