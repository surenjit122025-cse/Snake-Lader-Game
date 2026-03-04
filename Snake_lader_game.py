import tkinter as tk
import random
import time

# ------------------ SOUND ------------------
try:
    import winsound
    def play_sound():
        winsound.Beep(700, 120)
except:
    def play_sound():
        root.bell()

# ------------------ GAME DATA ------------------
snakes = {99: 54, 70: 55, 52: 42, 25: 2, 95: 72}
ladders = {6: 25, 11: 40, 60: 85, 46: 90, 17: 69}

CELL = 50
positions = [1, 1]
current_player = 0

# ------------------ COORDINATES ------------------
def get_xy(pos):
    row = (pos - 1) // 10
    col = (pos - 1) % 10
    if row % 2:
        col = 9 - col
    x = col * CELL + CELL // 2
    y = (9 - row) * CELL + CELL // 2
    return x, y

# ------------------ DRAW BOARD ------------------
def draw_board():
    for i in range(500):
        canvas.create_line(0, i, 500, i, fill="#e3f2fd")

    num = 100
    for r in range(10):
        for c in range(10):
            x1, y1 = c * CELL, r * CELL
            x2, y2 = x1 + CELL, y1 + CELL
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")
            canvas.create_text(x1+25, y1+25, text=str(num), font=("Arial", 10))
            num -= 1

# ------------------ DRAW SNAKES ------------------
def draw_snakes():
    for start, end in snakes.items():
        x1, y1 = get_xy(start)
        x2, y2 = get_xy(end)

        canvas.create_line(x1, y1, x2, y2,
                           smooth=True, width=8, fill="#1b5e20")

        canvas.create_oval(x1-10, y1-10, x1+10, y1+10,
                           fill="#2e7d32", outline="black")

        tongue = canvas.create_line(x1, y1, x1+12, y1,
                                    fill="red", width=2)

        def flick(t=0):
            dx = 12 if t % 2 == 0 else 6
            canvas.coords(tongue, x1, y1, x1+dx, y1)
            root.after(400, flick, t+1)

        flick()

# ------------------ DRAW LADDERS ------------------
def draw_ladders():
    for start, end in ladders.items():
        x1, y1 = get_xy(start)
        x2, y2 = get_xy(end)

        canvas.create_line(x1-12, y1, x2-12, y2,
                           width=5, fill="#5d4037")
        canvas.create_line(x1+12, y1, x2+12, y2,
                           width=5, fill="#5d4037")

        for i in range(7):
            sx = x1 - 12 + (x2 - x1) * i / 7
            sy = y1 + (y2 - y1) * i / 7
            ex = x1 + 12 + (x2 - x1) * i / 7
            ey = y1 + (y2 - y1) * i / 7
            canvas.create_line(sx, sy, ex, ey,
                               width=4, fill="#8d6e63")

# ------------------ MOVE PLAYER ------------------
def move_player(pid, pos):
    x, y = get_xy(pos)
    canvas.coords(players[pid], x-10, y-10, x+10, y+10)

# ------------------ ROLL DICE ------------------
def roll_dice():
    global current_player

    dice = random.randint(1, 6)
    dice_label.config(text=f"🎲 Dice: {dice}")
    play_sound()

    if positions[current_player] + dice <= 100:
        for _ in range(dice):
            positions[current_player] += 1
            move_player(current_player, positions[current_player])
            root.update()
            time.sleep(0.15)

    pos = positions[current_player]

    if pos in snakes:
        status_label.config(text="🐍 Snake Bite!")
        positions[current_player] = snakes[pos]

    elif pos in ladders:
        status_label.config(text="🪜 Ladder Climb!")
        positions[current_player] = ladders[pos]

    move_player(current_player, positions[current_player])
    pos_label.config(text=f"P1: {positions[0]}   P2: {positions[1]}")

    if positions[current_player] == 100:
        status_label.config(text=f"🎉 Player {current_player+1} Wins!")
        roll_btn.config(state="disabled")
        return

    current_player = 1 - current_player
    status_label.config(text=f"Player {current_player+1}'s Turn")

# ------------------ UI ------------------
root = tk.Tk()
root.title("Snake & Ladder Final Game")
root.resizable(False, False)

left = tk.Frame(root)
left.pack(side="left", padx=10, pady=10)

right = tk.Frame(root)
right.pack(side="right", padx=10)

canvas = tk.Canvas(left, width=500, height=500)
canvas.pack()

draw_board()
draw_snakes()
draw_ladders()

players = [
    canvas.create_oval(0,0,0,0, fill="red"),
    canvas.create_oval(0,0,0,0, fill="blue")
]

move_player(0, 1)
move_player(1, 1)

tk.Label(right, text="🐍 Snake & Ladder 🎲",
         font=("Arial", 18, "bold")).pack(pady=10)

pos_label = tk.Label(right, text="P1: 1   P2: 1", font=("Arial", 14))
pos_label.pack(pady=10)

dice_label = tk.Label(right, text="🎲 Dice: -", font=("Arial", 14))
dice_label.pack(pady=10)

roll_btn = tk.Button(right, text="Roll Dice",
                     font=("Arial", 14),
                     bg="green", fg="white",
                     command=roll_dice)
roll_btn.pack(pady=20)

status_label = tk.Label(right, text="Player 1's Turn",
                        font=("Arial", 12), fg="blue")
status_label.pack(pady=10)

root.mainloop()
