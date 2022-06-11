import pygame
import pygame as pg
import math
from queue import PriorityQueue

WIDTH = 800

WIN = pg.display.set_mode((WIDTH,WIDTH))
pg.display.set_caption("deneme")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
orange = (255, 165 ,0)
grey = (128, 128, 128)
turquase = (64, 224, 208)

class Tile:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = white
        self.neighbors = []
        self.width = width
        self.totalRows = totalRows

    def getPos(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == red

    def isOpen(self):
        return self.color == green

    def isBarrier(self):
        return self.color == black

    def isStart(self):
        return self.color == orange

    def isEnd(self):
        return self.color == turquase

    def reset(self):
        self.color = white

    def makeClosed(self):
        self.color = red

    def makeOpen(self):
        self.color = green

    def makeBarrier(self):
        self.color = black

    def makeStart(self):
        self.color = orange

    def makeEnd(self):
        self.color = turquase

    def makePath(self):
        self.color = purple

    def draw(self,win):
        pg.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def updateNeighbors(self,grid):
        self.neighbors = []
        if self.row <self.totalRows-1 and not grid[self.row+1][self.col].isBarrier():
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row >0 and not grid[self.row-1][self.col].isBarrier():
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col <self.totalRows-1 and not grid[self.row][self.col+1].isBarrier():
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col >0 and not grid[self.row][self.col-1].isBarrier():
            self.neighbors.append(grid[self.row][self.col-1])



    def __lt__(self, other):
        return False

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.makePath()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.getPos(), end.getPos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.makeEnd()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.getPos(), end.getPos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.makeOpen()

		draw()

		if current != start:
			current.makeClosed()

	return False


def makeGrid(rows,width):
    grid = []
    gap = width//rows
    for i in range (rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i,j,gap,rows)
            grid[i].append(tile)

    return grid

def drwaGrid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win,grey,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pg.draw.line(win,grey,(i*gap,0),(i*gap,width))

def draw(win,grid,rows,width):
    win.fill(white)

    for row in grid:
        for tile in row:
            tile.draw(win)

    drwaGrid(win,rows,width)
    pg.display.update()

def getMousePos(pos,rows,width):
    gap = width//rows
    y,x = pos

    row = y // gap
    col = x // gap

    return row,col

def main(win,width):
    ROWS = 50
    grid = makeGrid(ROWS,width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run=False

            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                row, col= getMousePos(pos,ROWS,width)
                tile = grid[row][col]
                if not start and tile != end:
                    start = tile
                    start.makeStart()
                elif not end and tile != start:
                    end = tile
                    end.makeEnd()
                elif tile != end and tile !=start:
                    tile.makeBarrier()

            elif pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos ()
                row, col = getMousePos (pos, ROWS, width)
                tile = grid [row] [col]
                tile.reset()
                if tile == start:
                    start = None
                elif tile == end:
                    end =None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and start and end:
                    for row in grid:
                        for tile in row:
                            tile.updateNeighbors(grid)


                    algorithm(lambda: draw(win, grid, ROWS, width),grid,start,end)
                if event.key == pg.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS, width)
    pg.quit()


main(WIN,WIDTH)