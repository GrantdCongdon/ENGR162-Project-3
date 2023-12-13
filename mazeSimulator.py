import tkinter as tk
# print mouse coords
def getCoords(event):
    print(event.x, event.y)
def main():
    t = tk.Tk()
    t.title("Maze Simulator")
    # creates a window that is 750x750 pixels
    t.configure(background="white")
    t.geometry("750x540")
    # create drawing canvas frame
    canvasFrame = tk.Frame(t)
    canvasFrame.grid(row=0, column=0, padx=125)
    # create drawing canvas
    canvas = tk.Canvas(canvasFrame, width=500, height=500, background="white")
    canvas.grid(row=0, column=0)
    # create button frame
    buttonFrame = tk.Frame(t)
    buttonFrame.grid(row=1, column=0)
    # create buttons
    resetButton = tk.Button(buttonFrame, text="Reset")
    resetButton.grid(row=0, column=0)
    # bind mouse click event to canvas
    canvas.bind("<Button-1>", getCoords)
    # run window loop
    t.mainloop()

if __name__ == "__main__":
    main()