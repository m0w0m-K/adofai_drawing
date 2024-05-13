import turtle
import tkinter as tk
from tkinter import ttk

# Tkinter 창 생성
root = tk.Tk()
root.geometry('500x500-5+40')

# 프레임 생성
frame = tk.Frame(root)
frame.pack()

# 터틀 캔버스 생성
canvas = tk.Canvas(frame, width=900, height=900)
canvas.pack()

# 터틀 스크린 설정
screen = turtle.TurtleScreen(canvas)
screen.screensize(2000, 1500)

# 터틀 생성
t = turtle.RawTurtle(screen)
t.hideturtle()
t.circle(100)

# 다른 위젯 생성
file_label = tk.Label(frame, text="파일")
tile_color_label = tk.Label(frame, text="타일색")
bg_color_label = tk.Label(frame, text="배경색")
size_label = tk.Label(frame, text="크기")
thickness_label = tk.Label(frame, text="두께")

file_button = tk.Button(frame, text="파일 선택", width=10, command=lambda: open_file_dialog(file_button))
tile_color_entry = tk.Entry(frame, width=10)
tile_color_entry.insert(0, 'debb7b')
bg_color_entry = tk.Entry(frame, width=10)
bg_color_entry.insert(0, '101121')
size_combobox = ttk.Combobox(frame, width=5, values=[i for i in range(99, 1, -1)])
size_combobox.current(59)
thickness_combobox = ttk.Combobox(frame, width=5, values=[i for i in range(99, 1, -1)])
thickness_combobox.current(77)
draw_button = tk.Button(frame, text='그리기', command=lambda: draw_shape(angles, center))
clear_button = tk.Button(frame, text='초기화', command=lambda: clear())
file_name_entry = tk.Entry(frame, width=10)
save_button = tk.Button(frame, text='그림 저장', command=lambda: save())

# 위젯 배열
widget = [
    [file_label, tile_color_label, bg_color_label, size_label, thickness_label],
    [file_button, tile_color_entry, bg_color_entry, size_combobox, thickness_combobox, draw_button, clear_button],
    [file_name_entry, save_button]
]

# Frame에 위젯 배치
for i in range(len(widget)):
    for j in range(len(widget[i])):
        widget[i][j].grid(row=i, column=j, padx=5)

# Tkinter 이벤트 루프 시작
root.mainloop()
