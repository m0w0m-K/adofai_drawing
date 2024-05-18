import math as m
import statistics
import turtle as t
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import re
import json

def is_valid_filename(filename):
    return 1 if re.match(r"^[^\\\/\:\*\?\"\<\>\|]*$", filename) and filename and re.match(r"^[^\.]+$",filename) else 0

def update_status_bar(message):
    status_label.config(text=message)

def open_file_dialog(file_button):
    global angles
    file_path = filedialog.askopenfilename()
    
    if file_path and is_adofai_file(file_path):
        angles = read_adofai_file(file_path)
        file_button.config(text=f"{len(angles)}")
    elif file_path:
        update_status_bar("The selected file is not an adofai file.")

def is_adofai_file(file_path):
    _, extension = os.path.splitext(file_path)
    return extension == ".adofai"

def read_adofai_file(file_path):
    global center
    file_path = file_path.strip('"').replace('\\', '/')
    
    with open(file_path, "r", encoding="utf-8-sig") as file:
        adofai_data = json.load(file) 
        adofai_data = json.load(file) 
        center = calculate_center(adofai_data["angleData"])
        
    return adofai_data["angleData"]

def calculating_size(angles):
    minimum = [0,0]
    maximum = [0,0]
    current = [0,0]
    for i in angles:
        current[0] += m.cos(m.radians(i))
        current[1] += m.sin(m.radians(i))
        minimum[0] = min(minimum[0], current[0])
        minimum[1] = min(minimum[1], current[1])
        maximum[0] = max(maximum[0], current[0])
        maximum[1] = max(maximum[1], current[1])
    # print(maximum[0] - minimum[0], maximum[1] - minimum[1])
    return (maximum[0] - minimum[0] + maximum[1] - minimum[1])/2

def calculating_size(angles):
    minimum = [0,0]
    maximum = [0,0]
    current = [0,0]
    for i in angles:
        current[0] += m.cos(m.radians(i))
        current[1] += m.sin(m.radians(i))
        minimum[0] = min(minimum[0], current[0])
        minimum[1] = min(minimum[1], current[1])
        maximum[0] = max(maximum[0], current[0])
        maximum[1] = max(maximum[1], current[1])
    # print(maximum[0] - minimum[0], maximum[1] - minimum[1])
    return (maximum[0] - minimum[0] + maximum[1] - minimum[1])/2

def draw_shape(angles, center = [0,0], start_index = 0):
    if not angles:
        update_status_bar('There is no File')
        return
    
    tile_color = "#" + tile_color_entry.get()
    bg_color = "#" + bg_color_entry.get()
    scaling_value = int(size_combobox.get())
    a = angles[start_index:] + angles[:start_index]
    latest = 0
    latest = 0
    
    turtle = t.RawTurtle(tScreen)
    turtle.hideturtle()
    turtle.width(int(thickness_combobox.get()))
    turtle.color(tile_color)
    tScreen.bgcolor(bg_color)
    turtle.speed(0)
    tScreen.delay(0)
    turtle.penup()
    turtle.goto(-center[0]*scaling_value,-center[1]*scaling_value)
    turtle.pendown()
    turtle = t.RawTurtle(tScreen)
    turtle.hideturtle()
    turtle.width(int(thickness_combobox.get()))
    turtle.color(tile_color)
    tScreen.bgcolor(bg_color)
    turtle.speed(0)
    tScreen.delay(0)
    turtle.penup()
    turtle.goto(-center[0]*scaling_value,-center[1]*scaling_value)
    turtle.pendown()
    
    for i in a:
        if i != 999:
            turtle.seth(i)
            turtle.forward(scaling_value)
            latest = i
        else: # 미드스핀인 경우
            turtle.forward(scaling_value)
            turtle.seth(-latest)
            latest = -latest
    turtle.end_fill()

def calculate_center(angles, start_index = 0):
    a = angles[start_index:] + angles[:start_index]
    current = [0,0]
    coordinates = [[0],[0]]
    for i in a:
        current[0] += m.cos(m.radians(i))
        current[1] += m.sin(m.radians(i))
        coordinates[0].append(current[0])
        coordinates[1].append(current[1])
    return [statistics.mean(coordinates[0]),statistics.mean(coordinates[1])]

def clear():
    tScreen.clear()
    tScreen.bgcolor("#" + bg_color_entry.get())
    
def save():
    file_name = file_name_entry.get()
    if (is_valid_filename(file_name)):
        cv.postscript(file=f"{file_name}.eps")
        update_status_bar(f"File saved")
    else:
        update_status_bar("Invalid file name")
        
window = tk.Tk()
window.title("ADOFAI Shape Drawing")
window.size()
frame1 = tk.Frame(window)
frame1.pack()
frame2 = tk.Frame(window)
frame2.pack(pady=10)
cv = t.ScrolledCanvas(frame1, width=768, height=768, canvheight=1536, canvwidth=1536)
cv.pack()
tScreen = t.TurtleScreen(cv)
tScreen.bgcolor('#101121')
window.resizable(False,False)

angles = ""
center = [0,0]
size = [i for i in range(50,1,-1)]
thickness = [i for i in range(25,1,-1)]

status_label = tk.Label(window, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill=tk.X)

drawing_labelframe = tk.LabelFrame(frame2, text='Drawing')

file_label = tk.Label(drawing_labelframe, text="File")

tile_color_label = tk.Label(drawing_labelframe, text="Tile Color")

bg_color_label = tk.Label(drawing_labelframe, text="BG Color")

size_label = tk.Label(drawing_labelframe, text="Size")

thickness_label = tk.Label(drawing_labelframe, text="Thickness")

file_button = tk.Button(drawing_labelframe, text="Select File", width= 8, command=lambda: open_file_dialog(file_button))

tile_color_entry = tk.Entry(drawing_labelframe, width=7, justify='center')
tile_color_entry.insert(0, 'debb7b')

bg_color_entry = tk.Entry(drawing_labelframe, width=7, justify='center')
bg_color_entry.insert(0, '101121')

size_combobox = ttk.Combobox(drawing_labelframe, width=3, values=size)
size_combobox.current(30)

thickness_combobox = ttk.Combobox(drawing_labelframe, width=3, values=thickness)
thickness_combobox.current(15)

draw_button = tk.Button(drawing_labelframe, text='Draw', command=lambda: draw_shape(angles, center))

clear_button = tk.Button(drawing_labelframe, text='Clear', command=lambda: clear())

save_labelframe = tk.LabelFrame(frame2, text='Save')

file_name_label = tk.Label(save_labelframe, text="File name")

file_name_entry = tk.Entry(save_labelframe, width=10)

save_button = tk.Button(save_labelframe, text='Save', command= lambda: save())

drawing_widget = [
    [file_label,tile_color_label,bg_color_label,size_label,thickness_label],
    [file_button, tile_color_entry, bg_color_entry, size_combobox, thickness_combobox, draw_button, clear_button],
    ]

save_widget = [
    [file_name_label],
    [file_name_entry, save_button]
]

for i in range(len(drawing_widget)):
    for j in range(len(drawing_widget[i])):
        drawing_widget[i][j].grid(row=i,column=j, padx=3)
        
for i in range(len(save_widget)):
    for j in range(len(save_widget[i])):
        save_widget[i][j].grid(row=i,column=j,padx=5)

drawing_labelframe.grid(row=0, column=0, padx=10)
save_labelframe.grid(row=0, column=1, padx=10)

window.mainloop()