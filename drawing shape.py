import json
import math as m
import statistics
import turtle as t
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

def open_file_dialog(file_button):
    global angles
    file_path = filedialog.askopenfilename()
    
    if file_path and is_adofai_file(file_path):
        angles = read_adofai_file(file_path)
        file_button.config(text=f"{len(angles)} 타일")
    elif file_path:
        print("선택한 파일이 .adofai 파일이 아닙니다.")

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

def draw_shape(angles, center = [0,0], start_index = 0):
    if not angles:
        print('타일이 없습니다')
        return
    
    tile_color = "#" + tile_color_entry.get()
    bg_color = "#" + bg_color_entry.get()
    scaling_value = int(size_combobox.get())
    current = [-center[0],-center[1]]
    a = angles[start_index:] + angles[:start_index]
    
    t.screensize(1000,1000)
    t.hideturtle()
    t.width(int(thickness_combobox.get()))
    t.color(tile_color)
    t.bgcolor(bg_color)
    t.speed(0)
    t.penup()
    t.goto(current[0]*scaling_value,current[1]*scaling_value)
    t.pendown()
    
    for i in a:
        current[0] += m.cos(m.radians(i))
        current[1] += m.sin(m.radians(i))
        t.goto(current[0] * scaling_value, current[1] * scaling_value)
    
    t.end_fill()


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
    t.clear()

root = tk.Tk()
root.geometry("600x75")
root.resizable(False, False)
root.title("Drawing shape")
frame1 = tk.Frame(root)
frame1.pack(pady=10)

t.setup()

angles = ""
center = [0,0]
size = [i for i in range(1,99)]
thickness = [i for i in range(1,99)]

file_label = tk.Label(frame1, text="파일")

tile_color_label = tk.Label(frame1, text="타일색")

bg_color_label = tk.Label(frame1, text="배경색")

size_label = tk.Label(frame1, text="크기")

thickness_label = tk.Label(frame1, text="두께")

file_button = tk.Button(frame1, text="파일 선택", width= 10, command=lambda: open_file_dialog(file_button))

tile_color_entry = tk.Entry(frame1, width=10)
tile_color_entry.insert(0, 'debb7b')

bg_color_entry = tk.Entry(frame1, width=10)
bg_color_entry.insert(0, '101121')

size_combobox = ttk.Combobox(frame1, width=5, values=size)
size_combobox.current(39)

thickness_combobox = ttk.Combobox(frame1, width=5, values=thickness)
thickness_combobox.current(21)

draw_button = tk.Button(frame1, text='그리기', command=lambda: draw_shape(angles, center))

clear_button = tk.Button(frame1, text='초기화', command=lambda: clear())

widget = [[file_label,tile_color_label,bg_color_label,size_label,thickness_label],
          [file_button, tile_color_entry,bg_color_entry,size_combobox,thickness_combobox,draw_button,clear_button]]

for i in range(len(widget[0])):
    widget[0][i].grid(row=0,column=i,padx=5)
for i in range(len(widget[1])):
    widget[1][i].grid(row=1,column=i,padx=5)

t.bgcolor("#" + bg_color_entry.get())

root.mainloop()