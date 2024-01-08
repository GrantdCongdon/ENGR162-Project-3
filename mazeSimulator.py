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
# create goal
def placeGoal(event):
    goal = canvas.create_rectangle(event.x-50, event.y, event.x+50, event.y+20, fill="red", outline="red")
    return [event.x-25, event.y, event.x+25, event.y+10, goal]
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
                slope = (wall[3]-wall[1])/(wall[2]-wall[0])
                yValue = slope*(self.x-wall[0])+wall[1]
                if (yValue < self.y and ((self.y-yValue) < frontWallDistance)):
                    frontWallDistance = self.y - yValue
                elif (yValue > self.y and ((yValue-self.y) < backWallDistance)):
                    backWallDistance = yValue - self.y
            elif ((wall[1]<self.y and wall[3]>self.y) or (wall[1]>self.y and wall[3]<self.y)):
                slope = (wall[3]-wall[1])/(wall[2]-wall[0])
                xValue = (self.y-wall[1])/slope+wall[0]
                if (xValue < self.x and ((self.x-xValue) < leftWallDistance)):
                    leftWallDistance = self.x - xValue
                elif (xValue > self.x and ((xValue-self.x) < rightWallDistance)):
                    rightWallDistance = xValue - self.x
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
def my_max_by_weight(sequence):
    if not sequence:
        raise ValueError('empty sequence')

    maximum = sequence[0]

    for item in sequence:
        # Compare elements by their weight stored
        # in their second element.
        if item[1] > maximum[1]:
            maximum = item

    return maximum
def my_min_by_weight(sequence):
    if not sequence:
        raise ValueError('empty sequence')

    minimum = sequence[0]

    for item in sequence:
        # Compare elements by their weight stored
        # in their second element.
        if item[1] < minimum[1]:
            minimum = item

    return minimum
def resolveMaze():
    # take the lines and connect them to the edge of the canvas
    # select the 4 points that are closest to the canvas edge
    pointList = []
    for line in lineList:
        pointList.append([line[0], line[1]])
        pointList.append([line[2], line[3]])
    closestPoints = []
    for i in range(2):
        closestPoints.append(my_max_by_weight(pointList))
        pointList.remove(my_max_by_weight(pointList))
        closestPoints.append(my_min_by_weight(pointList))
        pointList.remove(my_min_by_weight(pointList))
        
    for point in closestPoints:
        if (point[1] < 250):
            canvas.create_line(point[0], point[1], point[0], 0, width=3, fill="white")
            lineList.append([point[0], point[1], point[0], 0])
        else:
            canvas.create_line(point[0], point[1], point[0], 500, width=3, fill="white")
            lineList.append([point[0], point[1], point[0], 500])

def main():
    global resolveMaze
    # bind mouse click event to canvas
    canvas.bind("<Button-1>", drawLine)
    canvas.bind("<Button-2>", placeGoal)
     # create button that will print out the wall distances
    wallButton = tk.Button(buttonFrame, text="Wall Distances", command=lambda: print(mouse.getWallDistances(lineList)))
    wallButton.grid(row=0, column=1)
    # create button that will print mouse path
    pathButton = tk.Button(buttonFrame, text="Get Path", command=lambda: print(mouse.getMousePath()))
    pathButton.grid(row=0, column=2)
    # resolve maze
    resolveMaze = tk.Button(buttonFrame, text="Resolve Maze", command=resolveMaze)
    resolveMaze.grid(row=0, column=3)
    # button that will start the maze solver
    solveButton = tk.Button(buttonFrame, text="Solve", command=lambda: mouse.solveMaze())
    solveButton.grid(row=0, column=4)
    # create buttons to move mouse
    t.bind("<Up>", lambda event: mouse.moveUp())
    t.bind("<Right>", lambda event: mouse.moveRight())
    t.bind("<Down>", lambda event: mouse.moveDown())
    t.bind("<Left>", lambda event: mouse.moveLeft())
    # create mouse
    mouse = Mouse(250, 475, canvas)
    # run window loop
    t.mainloop()
if __name__ == "__main__":
    main()