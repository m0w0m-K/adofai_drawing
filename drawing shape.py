import math as m
import statistics
import turtle as t
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import re
import json
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

def path2angle(path):
    angle = [i for i in path]
    for i in range(len(angle)):
        match angle[i]:
            case "R":
                angle[i] = 0
            case "p":
                angle[i] = 15
            case "J":
                angle[i] = 30
            case "E":
                angle[i] = 45
            case "T":
                angle[i] = 60
            case "o":
                angle[i] = 75
            case "U":
                angle[i] = 90
            case "q":
                angle[i] = 105
            case "G":
                angle[i] = 120
            case "Q":
                angle[i] = 135
            case "H":
                angle[i] = 150
            case "W":
                angle[i] = 165
            case "L":
                angle[i] = 180
            case "x":
                angle[i] = 195
            case "N":
                angle[i] = 210
            case "Z":
                angle[i] = 225
            case "F":
                angle[i] = 240
            case "V":
                angle[i] = 255
            case "D":
                angle[i] = 270
            case "Y":
                angle[i] = 285
            case "B":
                angle[i] = 300
            case "C":
                angle[i] = 315
            case "M":
                angle[i] = 330
            case "A":
                angle[i] = 345
            case "!":
                angle[i] = 999
    return angle
            
def is_valid_filename(filename):
    return 1 if re.match(r"^[^\\\/\:\*\?\"\<\>\|]*$", filename) and filename and re.match(r"^[^\.]+$",filename) else 0

def update_status_bar(message):
    status_label.config(text=message)

def open_file_dialog(file_button):
    global angles
    file_path = filedialog.askopenfilename()
    
    if file_path and is_adofai_file(file_path):
        angles = read_adofai_file(file_path)
        midspinCount = angles.count(999)
        file_button.config(text=len(angles)-midspinCount)
    elif file_path:
        update_status_bar("The selected file is not an adofai file.")

def is_adofai_file(file_path):
    _, extension = os.path.splitext(file_path)
    return extension == ".adofai"

def read_adofai_file(file_path):
    global center
    file_path = file_path.strip('"').replace('\\', '/')
    
    with open(file_path, "r", encoding="utf-8-sig") as file:
        f = file.read()
        f = re.sub(',[ \t\r\n]+}', "}", f)
        f = re.sub(',[ \t\r\n]+\]', "]", f)
        f = re.sub('\][\t\r\n]+\"', "], \"", f)
        adofai_data = json.loads(f)
        
        if "pathData" in adofai_data:
            angle = path2angle(adofai_data['pathData'])
        elif "angleData" in adofai_data:
            angle = path2angle(adofai_data['angleData'])
        
        center = calculate_center(angle)
        
    return angle

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
        else:
            latest += 180
            turtle.seth(latest)
            turtle.forward(scaling_value)
            
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
    tScreen.reset()
    turtle.hideturtle()
    
def save():
    file_name = file_name_entry.get() + '.eps'
    if (is_valid_filename(file_name)):
        cv.postscript(file=file_name)
        extention = var.get()
        eps_image = Image.open(file_name)
        
        if extention=='eps':
            pass
        
        elif extention==".jpg" or extention==".png":
            eps_image = Image.open(file_name)
            eps_image.load(scale=1)
            eps_image.save(f"{file_name[:-4]}{extention}")
            eps_image.close()
            os.remove(file_name)
            
        elif extention=='.svg':
            fig = plt.figure()
            svgfile   = f'{file_name[:-4]}.svg'
            logoax    = [0, 0, 1, 1]
            img=mpimg.imread(file_name)
            
            newax = fig.add_axes(logoax, anchor='SW', zorder=100)
            newax.imshow(img)
            newax.axis('off')
            
            fig.savefig(svgfile,dpi=300)
            eps_image.close()
            os.remove(f"{file_name}.eps")
            
        update_status_bar(f"{file_name}{extention} file saved")
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
turtle = t.RawTurtle(tScreen)
turtle.hideturtle()

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

extention_frame = tk.Frame(save_labelframe)
extention_frame.grid(row=2,column=0,columnspan=2)

var = tk.StringVar(value=".eps")
eps_radiobutton = tk.Radiobutton(extention_frame, text=".eps", variable=var, value=".eps")
svg_radiobutton = tk.Radiobutton(extention_frame, text=".svg", variable=var, value=".svg")
jpg_radiobutton = tk.Radiobutton(extention_frame, text=".jpg", variable=var, value=".jpg")
png_radiobutton = tk.Radiobutton(extention_frame, text=".png", variable=var, value=".png")
drawing_widget = [
    [file_label,tile_color_label,bg_color_label,size_label,thickness_label],
    [file_button, tile_color_entry, bg_color_entry, size_combobox, thickness_combobox, draw_button, clear_button],
    ]

save_widget = [
    [file_name_label],
    [file_name_entry, save_button],
]

extention_widget = [
    [eps_radiobutton, jpg_radiobutton, png_radiobutton, svg_radiobutton]
]

for i in range(len(drawing_widget)):
    for j in range(len(drawing_widget[i])):
        drawing_widget[i][j].grid(row=i,column=j, padx=3, pady=2)
        
for i in range(len(save_widget)):
    for j in range(len(save_widget[i])):
        save_widget[i][j].grid(row=i,column=j,padx=5)
        
for i in range(len(extention_widget)):
    for j in range(len(extention_widget[i])):
        extention_widget[i][j].grid(row=i,column=j,padx=5)

drawing_labelframe.grid(row=0, column=0, padx=10)
save_labelframe.grid(row=0, column=1, padx=10)

window.mainloop()
