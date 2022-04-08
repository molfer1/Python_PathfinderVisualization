import queue
import sys
import threading
import pygame
from pygame.locals import *

# Local
from visualizer import Visualizer
from pathFinder import PathFinder
from menu import *

COLOR_WALL = [255, 0, 0]
COLOR_POINT = [255, 255, 0]


def init_settings():
    menu = Menu()
    menu.mainloop()
    return menu


def get_user_settings(menu):
    user_settings = {
        "start": menu.user_settings["start"],
        "map_size": menu.user_settings["map_size"].get(),
        "start_x": menu.user_settings["start_x"].get(),
        "start_y": menu.user_settings["start_y"].get(),
        "goal_x": menu.user_settings["goal_x"].get(),
        "goal_y": menu.user_settings["goal_y"].get()
    }
    return user_settings


def init_visualizer(gridQueue, user_settings):
    row = (0, 0)
    col = (0, 0)
    if user_settings['map_size'] == "10x10":
        row = (200, 10)
        col = (240, 10)
    elif user_settings['map_size'] == "20x20":
        row = (400, 20)
        col = (440, 20)
    elif user_settings['map_size'] == "30x30":
        row = (600, 30)
        col = (640, 30)
    elif user_settings['map_size'] == "40x40":
        row = (800, 40)
        col = (840, 40)

    grid = Visualizer(row[0], col[0])
    matrix = PathFinder(gridQueue, row[1], col[1], (user_settings['start_x'], user_settings['start_y']), (user_settings['goal_x'], user_settings['goal_y']))

    pygame.init()
    grid.initMap()
    return {"grid": grid, "matrix": matrix}


def add_goal_points(grid, user_settings):
    grid.fillCell(user_settings['start_x'], user_settings['start_y'], COLOR_POINT)
    grid.fillCell(user_settings['goal_x'], user_settings['goal_y'], COLOR_POINT)


def record_walls_set(grid, matrix):
    mouse_x = 0
    mouse_y = 0
    getWalls = True
    fillCells = False
    while getWalls:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    getWalls = False
            elif event.type == MOUSEBUTTONDOWN:
                fillCells = True
            elif event.type == MOUSEBUTTONUP:
                fillCells = False

            # Check if user has selected any walls to add to the grid
            if fillCells:
                try:
                    # Get event pos and then convert coordinates to an actual location on the grid
                    # Color in the cell and set the coordinates in matrix to non-visitable
                    mouse_x, mouse_y = event.pos
                    mouse_x, mouse_y = grid.getCell(mouse_x, mouse_y)
                    rec = pygame.Rect(mouse_x, mouse_y, 20, 20)
                    pygame.draw.rect(grid.screen, COLOR_WALL, rec)
                    matrix.change_cell_to_wall(mouse_y // 20, mouse_x // 20, "COLOR_WALL")
                    pygame.display.update()
                except:
                    pass
        pygame.display.flip()


def start_pathFinder(matrix):
    threading.Thread(target=matrix.a_star()).start()


def visualize_path(grid, gridQueue):

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if not gridQueue.empty():
            x, y, clr = gridQueue.get()
            grid.fillCell(x, y, clr)

            pygame.display.update()


def init():
    gridQueue = queue.Queue()
    menu = init_settings()
    user_settings = get_user_settings(menu)
    if user_settings['start']:
        visualizer_data = init_visualizer(gridQueue, user_settings)
        add_goal_points(visualizer_data['grid'], user_settings)
        record_walls_set(visualizer_data['grid'], visualizer_data['matrix'])
        start_pathFinder(visualizer_data['matrix'])
        visualize_path(visualizer_data['grid'], gridQueue)
    else:
        pass

init()