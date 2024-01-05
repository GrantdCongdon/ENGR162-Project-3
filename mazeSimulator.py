import tkinter as tk
# define variables
finishLine = False
xCoord = 0
yCoord = 0
# create empty list that will include all the lines
lineList = []
# create canvas
t = tk.Tk()
t.title("Maze Simulator")
# creates a window that is 750x750 pixels
t.configure(background="black")
t.geometry("750x540")
# create drawing canvas frame
canvasFrame = tk.Frame(t)
canvasFrame.grid(row=0, column=0, padx=125)
# create drawing canvas
canvas = tk.Canvas(canvasFrame, width=500, height=500, background="black")
canvas.grid(row=0, column=0)
# create button frame
buttonFrame = tk.Frame(t)
buttonFrame.grid(row=1, column=0)
# create buttons
resetButton = tk.Button(buttonFrame, text="Reset", command=lambda: print(lineList))
resetButton.grid(row=0, column=0)
# print mouse coords
def drawLine(event):
    global finishLine, xCoord, yCoord
    if not finishLine:
        xCoord = event.x
        yCoord = event.y
        finishLine = True
    else:
        canvas.create_line(xCoord, yCoord, event.x, event.y, width=3, fill="white")
        # get the coordinates of all the points on the line by defining the line parametrically
        lineList.append([xCoord, yCoord, event.x, event.y])
        finishLine = False
# create mouse class
class Mouse:
    # directions: up:0, right:1, down:2, left:3
    def __init__(self, x, y, canvas, size=5):
        self.x = x
        self.y = y
        self.size = size
        self.path = []
        self.path.append([self.x, self.y])
        self.mouse = canvas.create_rectangle(self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size, fill="brown", outline="brown")
        self.wallDistances = []
    def moveUp(self):
        moveVector = [0, -5]
        self.x+=moveVector[0]
        self.y+=moveVector[1]
        self.path.append([self.x, self.y])
        canvas.move(self.mouse, moveVector[0], moveVector[1])
    def moveRight(self):
        moveVector = [5, 0]
        self.x+=moveVector[0]
        self.y+=moveVector[1]
        self.path.append([self.x, self.y])
        canvas.move(self.mouse, moveVector[0], moveVector[1])
    def moveDown(self):
        moveVector = [0, 5]
        self.x+=moveVector[0]
        self.y+=moveVector[1]
        self.path.append([self.x, self.y])
        canvas.move(self.mouse, moveVector[0], moveVector[1])
    def moveLeft(self):
        moveVector = [-5, 0]
        self.x+=moveVector[0]
        self.y+=moveVector[1]
        self.path.append([self.x, self.y])
        canvas.move(self.mouse, moveVector[0], moveVector[1])
    def getWallDistances(self, wallList):
        # find the distance between whatever wall is to the left of the mouse
        # assume that the mouse is a squeare
        frontWallDistance = 10000000
        rightWallDistance = 10000000
        backWallDistance = 10000000
        leftWallDistance = 10000000
        for wall in wallList:
            if ((wall[0]<self.x and wall[2]>self.x) or (wall[0]>self.x and wall[2]<self.x)):
                if (wall[1] < self.y and ((self.y-wall[1]) < frontWallDistance)):
                    frontWallDistance = self.y - wall[1]
                elif (wall[1] > self.y and ((wall[1]-self.y) < backWallDistance)):
                    backWallDistance = wall[1] - self.y
                else:
                    frontWallDistance = 10000000
                    backWallDistance = 10000000
            elif ((wall[1]<self.y and wall[3]>self.y) or (wall[1]>self.y and wall[3]<self.y)):
                if (wall[0] < self.x and ((self.x-wall[0]) < rightWallDistance)):
                    leftWallDistance = self.x - wall[0]
                elif (wall[0] > self.x and ((wall[0]-self.x) < rightWallDistance)):
                    rightWallDistance = wall[0] - self.x
                else:
                    rightWallDistance = 10000000
                    leftWallDistance = 10000000
            else:
                frontWallDistance = 10000000
                rightWallDistance = 10000000
                backWallDistance = 10000000
                leftWallDistance = 10000000
        wallDistances = [frontWallDistance, rightWallDistance, backWallDistance, leftWallDistance]
        return wallDistances
    def getMousePath(self):
        return self.path
    def getMouseCoords(self):
        return [self.x, self.y]
    # function that will navigate the mouse through the maze
    def solveMaze(self):
        wallDistances = self.getWallDistances(lineList)
        mouseData = []
        while (wallDistances[0] < 10000000 and wallDistances[1] < 10000000 and wallDistances[3] < 10000000):
            # maze solver algorithm
            print("Solving Maze")
        return mouseData
    # function that will create a map of the maze
    def createMazeMap(self, mouseData):
        return 0
def main():
    # bind mouse click event to canvas
    canvas.bind("<Button-1>", drawLine)
    # create buttons to move mouse
    t.bind("<Up>", lambda event: mouse.moveUp())
    t.bind("<Right>", lambda event: mouse.moveRight())
    t.bind("<Down>", lambda event: mouse.moveDown())
    t.bind("<Left>", lambda event: mouse.moveLeft())
    # create mouse
    mouse = Mouse(250, 475, canvas)
    # create button that will print out the wall distances
    wallButton = tk.Button(buttonFrame, text="Wall", command=lambda: print(mouse.getWallDistances(lineList)))
    wallButton.grid(row=0, column=1)
    # create button that will print mouse path
    pathButton = tk.Button(buttonFrame, text="Path", command=lambda: print(mouse.getMousePath()))
    pathButton.grid(row=0, column=2)
    # button that will start the maze solver
    solveButton = tk.Button(buttonFrame, text="Solve", command=lambda: mouse.solveMaze())
    solveButton.grid(row=0, column=3)
    # run window loop
    t.mainloop()
if __name__ == "__main__":
    main()