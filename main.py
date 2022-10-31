from tkinter import Canvas ,Tk, messagebox, font
from random import randrange
from itertools import cycle


win = Tk()
win.title("chaos")
win.resizable(False, False)
WIDTH, HEIGHT = 800, 600
canvas = Canvas(win, width=WIDTH, height=HEIGHT,
                bg='black')

rec = canvas.create_rectangle(150,250,50,270, fill="red")
rec1 = canvas.create_rectangle(420,150,350,170, fill="red")
p = canvas.create_rectangle(355, 55, 465, 75,
                             fill='gold')
p1 = canvas.create_rectangle(440, 555, 560, 575,
                             fill='white')
ball = canvas.create_oval(400,300,420,320, fill='white')

canvas.pack()
score= 0
p1score = 0


farb_zyklus = cycle(["light blue", "light green", "light pink", "light yellow"])
ei_width = 25
ei_height = 25
ei_tempo = 200
ei_intervall = 3000
schwierigkeit = 0.85
PADDLE_MOVEMENT = 5
REFRESH_TIME = 10

game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

punktzahl = 0
punktzahl_text = canvas.create_text(10,10, anchor="nw", font= game_font, fill="red", text="Punktzahl: " +str(punktzahl))
verbleibende_leben = 3
leben_text = canvas.create_text(WIDTH - 10, 10, anchor="ne", font=game_font, fill="red", text="leben " + str(verbleibende_leben))

xspeed =6
yspeed = 0
aspeed =4
bspeed = 0

x,y = 4,4

p1x0, p1y0, p1x1, p1y1 = canvas.coords(p1)
px0, py0, px1, py1 = canvas.coords(p)
x0, y0, x1, y1 = canvas.coords(ball)
eier = []

def bewegen():
    global xspeed,yspeed
    canvas.move(rec,xspeed,yspeed)
    (leftPos,topPos,rightPos, bottomPos) = canvas.coords(rec)

    if leftPos <= 0 or rightPos >= WIDTH:
        xspeed = -xspeed
    if topPos <= 0 or bottomPos >= HEIGHT:
        yspeed = -yspeed
    canvas.after(30,bewegen)
canvas.after(30,bewegen)
def bewegen1():
    global aspeed,bspeed
    canvas.move(rec1,aspeed,bspeed)
    (leftPos,topPos,rightPos, bottomPos) = canvas.coords(rec1)

    if leftPos <= 0 or rightPos >= WIDTH:
        aspeed = -aspeed
    if topPos <= 0 or bottomPos >= HEIGHT:
        bspeed = -bspeed
    canvas.after(30,bewegen1)
canvas.after(30,bewegen1)
def create_ei():
    x = randrange(10, 740)
    y = 40
    neues_ei = canvas.create_oval(x, y, x + ei_width, y +ei_height, fill = next(farb_zyklus), width=0)
    eier.append(neues_ei)
    win.after(ei_intervall, create_ei)

def move_eier():
    global x, y
    for ei in eier:
        p1x0, p1y0, p1x1, p1y1 = canvas.coords(p1)
        (ei_x, ei_y, ei_x2, ei_y2) = canvas.coords(ei)
        if ei_y2 >= 555 and ei_y2 <= 575:
            if ei_x >= p1x0 and ei_x2 <= p1x1:
                ei_gefallen(ei)



        canvas.move(ei, 0, 10)

        if ei_y2 > HEIGHT:
            ei_gefallen1(ei)


    win.after(ei_tempo, move_eier)

def ei_gefallen1(ei):
    eier.remove(ei)
    canvas.delete(ei)


def ei_gefallen(ei):
        eier.remove(ei)
        canvas.delete(ei)
        verliere_ein_leben()
        if verbleibende_leben == 0:
            messagebox.showinfo("Gameover")
            win.destroy()

def verliere_ein_leben():
    global verbleibende_leben
    verbleibende_leben -= 1
    canvas.itemconfigure(leben_text, text="leben" + str(verbleibende_leben))

def erhöhe_punkt():
    global punktzahl

    punktzahl += 1

    canvas.itemconfigure(punktzahl_text, text="punktzahl: " + str(punktzahl))
    top()
    if punktzahl == 3:
        messagebox.showinfo("du hast gewonnen")
        win.destroy()

def top():
    global  ei_tempo
    global ei_intervall
    if punktzahl == 1:
        ei_tempo = ei_tempo -100
    if punktzahl == 2:
        ei_intervall = ei_intervall -2000


def moveBall():
    global x ,y
    global schwierigkeit
    global ei_intervall
    global punktzahl
    canvas.move(ball, x, y)

    (leftPos, topPos, rightPos, bottomPos) = canvas.coords(ball)
    x0, y0, x1, y1 = canvas.coords(ball)

    if y1 >= HEIGHT:
        punktzahl = punktzahl - 1
        canvas.itemconfigure(punktzahl_text, text="punktzahl: " + str(punktzahl))
        if punktzahl == -3:
            messagebox.showinfo("du hast verloren")
            win.destroy()


    if y0 <= 0 or y1 >= HEIGHT:
        y = -y

    if x0 <= 0 or x1 >= WIDTH:
        x = -x

    p1x0, p1y0, p1x1, p1y1 = canvas.coords(p1)
    px0, py0, px1, py1 = canvas.coords(p)
    pxa0, pya0, pxa1, pya1 = canvas.coords(rec)
    pxb0, pyb0, pxb1, pyb1 = canvas.coords(rec1)

    if y1 >= 555 and y1 <= 575 and y > 0:
        if x0>= p1x0 and x1 <= p1x1:
            y *= -1
    if y1 >= 55 and y1 <= 75 and y < 0:
        if x0>= px0 and x1 <= px1:

            erhöhe_punkt()
            y *= -1
    if y1 >= 250 and y1 <= 270 and y < 0:
        if x0>= pxa0 and x1 <= pxa1:
            x *= -1
    if y1 >= 150 and y1 <= 170 and y < 0:
        if x0>= pxb0 and x1 <= pxb1:
            y *= -1


    canvas.after(30,moveBall)
canvas.after(30,moveBall)


def move_p1(event):
    if event.keysym == "w" and p1y0 > 0:
        canvas.move(p1, -50, 0)


    elif event.keysym == "s" and p1y1 < 800:
        canvas.move(p1, 50, 0)

canvas.bind_all("<KeyPress-w>", move_p1)
canvas.bind_all("<KeyPress-s>", move_p1)



win.after(1000, move_eier)
win.after(1000,create_ei)

win.mainloop()