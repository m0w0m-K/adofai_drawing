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
        file_button.config(text=f"{len(angles)} 타일")
    elif file_path:
        update_status_bar("선택한 파일이 .adofai 파일이 아닙니다.")

def is_adofai_file(file_path):
    _, extension = os.path.splitext(file_path)
    return extension == ".adofai"

def read_adofai_file(file_path):
    global center
    file_path = file_path.strip('"').replace('\\', '/')
    
    with open(file_path, "r", encoding="utf-8-sig") as file:
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

def draw_shape(angles, center = [0,0], start_index = 0):
    if not angles:
        update_status_bar('타일이 없습니다')
        return
    
    tile_color = "#" + tile_color_entry.get()
    bg_color = "#" + bg_color_entry.get()
    scaling_value = int(size_combobox.get())
    a = angles[start_index:] + angles[:start_index]
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
        tScreen.getcanvas().postscript(file=f"{file_name}.eps")
        update_status_bar(f"파일을 저장했습니다.")
    else:
        update_status_bar("유효하지 않은 파일 이름입니다.")
        
window = tk.Tk()
window.title("Drawing shape")
window.size()
frame1 = tk.Frame(window)
frame1.pack()
frame2 = tk.Frame(window)
frame2.pack()
cv = t.ScrolledCanvas(frame1, width=768, height=768, canvheight=1536, canvwidth=1536)
cv.pack()
tScreen = t.TurtleScreen(cv)
tScreen.bgcolor('#101121')
window.resizable(False,False)

angles = ""
center = [0,0]
size = [i for i in range(99,1,-1)]
thickness = [i for i in range(99,1,-1)]

status_label = tk.Label(window, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill=tk.X)

file_label = tk.Label(frame2, text="파일")

tile_color_label = tk.Label(frame2, text="타일색")

bg_color_label = tk.Label(frame2, text="배경색")

size_label = tk.Label(frame2, text="크기")

thickness_label = tk.Label(frame2, text="두께")

file_button = tk.Button(frame2, text="파일 선택", width= 8, command=lambda: open_file_dialog(file_button))

tile_color_entry = tk.Entry(frame2, width=7, justify='center')
tile_color_entry.insert(0, 'debb7b')

bg_color_entry = tk.Entry(frame2, width=7, justify='center')
bg_color_entry.insert(0, '101121')

size_combobox = ttk.Combobox(frame2, width=3, values=size)
size_combobox.current(79)

thickness_combobox = ttk.Combobox(frame2, width=3, values=thickness)
thickness_combobox.current(88)

draw_button = tk.Button(frame2, text='그리기', command=lambda: draw_shape(angles, center))

clear_button = tk.Button(frame2, text='초기화', command=lambda: clear())

file_name_entry = tk.Entry(frame2, width=10)

save_button = tk.Button(frame2, text='그림 저장', command= lambda: save())

widget = [
    [file_label,tile_color_label,bg_color_label,size_label,thickness_label],
    [file_button, tile_color_entry, bg_color_entry, size_combobox, thickness_combobox, draw_button, clear_button],
    [file_name_entry, save_button]
    ]

for i in range(len(widget)):
    for j in range(len(widget[i])):
        widget[i][j].grid(row=i,column=j,padx=5)

window.mainloop()
