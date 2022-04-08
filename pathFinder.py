import heapq
import sys
from dataclasses import dataclass

COLOR_CELL_CHECKED = [240, 100, 50]
COLOR_CELL_TO_CHECK = [0, 200, 0]
COLOR_PATH = [220, 220, 220]
COLOR_POINT = [255, 255, 0]


@dataclass
class Cell:
    cell_color = "COLOR_CELL"
    cell_parent = (0, 0)
    g_cost = sys.maxsize  # DISTANCE FROM STARTING CELL
    h_cost = 0  # DISTANCE FROM GOAL CELL
    f_cost = 0  # g_cost + h_cost


class PathFinder:
    def __init__(self, grid_queue, row_count, col_count, start_point, goal_point):
        self.grid_queue = grid_queue
        self.goalFound = False
        self.row_count = row_count
        self.col_count = col_count
        self.start_point = start_point
        self.goal_point = goal_point
        self.matrix = [[Cell() for _ in range(row_count)] for _ in range(col_count)]

    def change_cell_to_wall(self, x, y, color):
        self.matrix[x][y].g_cost = sys.maxsize
        self.matrix[x][y].cell_color = color

    def is_visitable(self, current_cell):
        if 0 <= current_cell[0] < self.row_count and 0 <= current_cell[1] < self.col_count:
            return True
        else:
            return False

    def get_visitable_cells(self, current_cell):
        x, y = current_cell
        visitable_cells = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        return filter(self.is_visitable, visitable_cells)

    def show_path(self, current_cell):
        self.grid_queue.put((current_cell[0], current_cell[1], COLOR_POINT))
        while current_cell != self.start_point:
            current_cell = self.matrix[current_cell[0]][current_cell[1]].cell_parent
            self.grid_queue.put((current_cell[0], current_cell[1], COLOR_PATH))
        self.grid_queue.put((current_cell[0], current_cell[1], COLOR_POINT))

    def a_star(self):
        priority_queue = []
        heapq.heapify(priority_queue)
        heapq.heappush(priority_queue, (0, self.start_point))
        searched_cells = {}
        start_x, start_y = self.start_point
        self.matrix[start_x][start_y].g_cost = 0

        while len(priority_queue) > 0:
            # FIND LOWEST COST&UPDATE SEARCHED CELLS
            x, y = heapq.heappop(priority_queue)[1]
            searched_cells[(x, y)] = True
            # UPDATE CHECKED COLOR MARK
            self.grid_queue.put((x, y, COLOR_CELL_CHECKED))
            # EXIT LOOP IF GOAL REACHED
            if (x, y) == self.goal_point:
                self.goalFound = True
                break

            for visitable_cell in self.get_visitable_cells((x, y)):
                row = visitable_cell[0]
                col = visitable_cell[1]
                if (row, col) in searched_cells or self.matrix[row][col].cell_color == "COLOR_WALL":
                    continue
                new_cost = self.matrix[x][y].g_cost + 1
                current_cost = self.matrix[row][col].g_cost
                if current_cost == sys.maxsize or new_cost < current_cost:
                    # UPDATE MAIN VARS
                    self.matrix[row][col].g_cost = new_cost
                    dif_x = abs(row - self.goal_point[0])
                    dif_y = abs(col - self.goal_point[1])
                    h = min(dif_x, dif_y) + abs(dif_x - dif_y)
                    f = new_cost + h
                    # PUSH TO STACK
                    heapq.heappush(priority_queue, (f, (row, col)))
                    self.matrix[row][col].cell_parent = (x, y)
                    # COLOR CELL TO CHECK
                    self.grid_queue.put((row, col, COLOR_CELL_TO_CHECK))
        self.show_path(self.goal_point)
