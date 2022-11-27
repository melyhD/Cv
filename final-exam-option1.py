import numpy as np
from random import randint
from datetime import datetime as dt
import json, os

# Json file

file_path = "C:/Users/demir/Desktop/cvD/final-exam-option1/gamelog.json"

if not os.path.exists(file_path):
    file = open(file_path, "w")
    file.close()

def write_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def json_file_control(file_path, moves, score):
    global date
    f = open(file_path, "r")
    if f.read() == "":
        data = {date: {"moves": moves, "score": score}}
    else:
        f = open(file_path, "r")
        data = json.load(f)
        inner_dict = {"moves": moves, "score": score}
        data[date] = inner_dict
    
    write_data(data, file_path)

# Create adventure land

row_num, clmn_num = 6, 7

user = np.full((row_num, clmn_num), " ")
back = np.full((row_num, clmn_num), " ")

# Set cell values

def set_cell_value(num, val):
    x = 0
    while x < num:
        row = randint(0,row_num - 1)
        clmn = randint(0,clmn_num - 1)
        if back[row][clmn] == ' ':
            back[row][clmn] = val
            x += 1

def all_cell_values(num_val_list):
    for i in range(0, len(num_val_list), 2):
        set_cell_value(num_val_list[i], num_val_list[i+1])

all_cell_values([5, "T", 5, "M", 2, "S", 3, "P", 3, "V", 1, "E"])

# Initialize game display

user_row, user_clmn = np.where(back == "E")[0][0].item(), np.where(back == "E")[1][0].item()
user[user_row][user_clmn] = "E"
user_row_str, user_clmn_str = user_row, user_clmn

score, sword, poition = 0, 0, 0

print(user)
print(f"\nScore : [{score}] Sword : [{sword}] Poition : [{poition}]")

# Movement of the user

moves = []

def movement(inp, key1, key2, axis1, axis1_change, axis2, axis2_change, border1, border2):
    global mv_st, moves

    if (inp == key1 or inp == key2) and axis1 != border1 and axis2 != border2:
        if user[axis1 + axis1_change][axis2 + axis2_change] == " ":
            axis1 += axis1_change
            axis2 += axis2_change
            moves.append(inp)
        else:
            mv_st = False

    return axis1, axis2

# game loop

visited_cell_number = 1

d = dt.now()
date = "%d/%d/%d %s" % (d.day, d.month, d.year, d.time().isoformat(timespec="seconds"))

for i in range(row_num*clmn_num - 1):
    
    dth = ""
    tool_use = ""
    new_tool = ""
    br_st = ""

    move = input("\nPress L, U, R, D to move: ")

    mv_st = True

    if (move == "q" or move == "Q"):
        print("\nQuitted the game.")
        json_file_control(file_path, moves, score)
        break

    user_row, user_clmn = movement(move, "u", "U", user_row, -1, user_clmn, 0, 0, "")
    user_row, user_clmn = movement(move, "d", "D", user_row, 1, user_clmn, 0, 5, "")
    user_row, user_clmn = movement(move, "l", "L", user_row, 0, user_clmn, -1, "", 0)
    user_row, user_clmn = movement(move, "r", "R", user_row, 0, user_clmn, 1, "", 6)

    # Control of the cell values and score update

    if user_clmn_str != user_clmn or user_row_str != user_row:
        if back[user_row][user_clmn] == " ":
            user[user_row][user_clmn] = "E"
            score += 1
        else:
            user[user_row][user_clmn] = back[user_row][user_clmn]
            if back[user_row][user_clmn] == "T":
                score += 2
                new_tool = "\n" + "-"*32 + "\n\n+TREASURE" + "\n\n" + "-"*32
            elif back[user_row][user_clmn] == "S":
                score += 1
                sword += 1
                new_tool = "\n" + "-"*32 + "\n\n+SWORD" + "\n\n" + "-"*32
            elif back[user_row][user_clmn] == "P":
                score += 1
                poition += 1
                new_tool = "\n" + "-"*32 + "\n\n+POITION" + "\n\n" + "-"*32
            elif back[user_row][user_clmn] == "M":
                if sword != 0:
                    sword -= 1
                    score += 1
                    tool_use = "\n" + "-"*32 + "\n\nOh no! MONSTER.\nSWORD is used." + "\n\n" + "-"*32
                else:
                    dth = "\n" + "-"*32 + "\n\nOh no! MONSTER.\nYou die."
            else:
                if poition != 0:
                    poition -= 1
                    score += 1
                    tool_use = "\n" + "-"*32 + "\n\nOh no! VENOM.\nPOITION is used." + "\n\n" + "-"*32
                else:
                    dth = "\n" + "-"*32 + "\n\nOh no! VENOM.\nYou die."

    user_row_str, user_clmn_str = user_row, user_clmn

    # Game display

    print("\033[H\033[J", end="")
    print(user)

    if new_tool != "":
        print(new_tool)
    if tool_use != "":
        print(tool_use)
    if dth != "":
        print(dth)
    if not mv_st:
        print("\nYou have already visited that cell before!!!")
    print(f"\nScore : [{score}] Sword : [{sword}] Poition : [{poition}]")

    if dth != "":
        print("\nThe game ends.")
        visited_cell_number = i
        json_file_control(file_path, moves, score)
        break

    # Control of whether the user is able to move or not

    if (user_row == 0 and user_clmn == 0 and user[user_row + 1][user_clmn] != " " and user[user_row][user_clmn + 1] != " ") or (
        user_row == 0 and user_clmn == clmn_num - 1 and user[user_row + 1][user_clmn] != " " and user[user_row][user_clmn - 1] != " ") or (
        user_row == row_num - 1 and user_clmn == clmn_num - 1 and user[user_row - 1][user_clmn] != " " and user[user_row][user_clmn - 1] != " ") or (
        user_row == row_num - 1 and user_clmn == 0 and user[user_row - 1][user_clmn] != " " and user[user_row][user_clmn + 1] != " "):

        print("\nYou can't move anywhere further.\nThe game ends.")
        visited_cell_number = i
        json_file_control(file_path, moves, score)
        break

    elif (user_row == 0 and user[user_row + 1][user_clmn] != " " and user[user_row][user_clmn + 1] != " " and user[user_row][user_clmn - 1] != " ") or (
          user_clmn == clmn_num - 1 and user[user_row + 1][user_clmn] != " " and user[user_row - 1][user_clmn] != " " and user[user_row][user_clmn - 1] != " ") or (
          user_row == row_num - 1 and user[user_row - 1][user_clmn] != " " and user[user_row][user_clmn + 1] != " " and user[user_row][user_clmn - 1] != " ") or (
          user_clmn == 0 and user[user_row + 1][user_clmn] != " " and user[user_row - 1][user_clmn] != " " and user[user_row][user_clmn + 1] != " "):

        print("\nYou can't move anywhere further.\nThe game ends.")
        visited_cell_number = i
        json_file_control(file_path, moves, score)
        break

    elif user_row < row_num - 1 and user_row > 0 and user_clmn < user_clmn - 1 and user_clmn > 0:
        if user[user_row + 1][user_clmn] != " " and user[user_row - 1][user_clmn] != " " and user[user_row][user_clmn + 1] != " " and user[user_row][user_clmn - 1] != " ":
            print("\nYou can't move anywhere further.\nThe game ends.")
            visited_cell_number = i
            json_file_control(file_path, moves, score)
            break

if visited_cell_number == int(row_num*clmn_num):
    print("\nYou have visited all cells without dying. Congratulations :)")