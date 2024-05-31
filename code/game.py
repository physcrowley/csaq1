# File: game.py

""" Extract and organize the game data """

# read data into memory
with open("./data/game_data.txt", "r") as file:
    data = file.read()

# created nested lists from the data
rooms = data.strip().split("###")  # split the data into rooms

NAME = 0
DESCRIPTION = 1
OPTIONS = 2

# split each room into sections
for i in range(len(rooms)):
    rooms[i] = rooms[i].strip().split("\n\n")

room_names = [r[NAME] for r in rooms]

for r in rooms:
    # split options section into a list of options
    r[OPTIONS] = r[OPTIONS].strip().split(", ")


""" Game logic """

# welcome message
print("Welcome to the game!")
print("You are about to be teleported into the game world.")
print("Here are your options:")
print("  [exit] or [enter]\n")
choice = ""
while choice not in ["exit", "enter"]:
    choice = input("> ").lower()

if choice == "exit":
    print("Goodbye!")
    exit()

# game loop
room = rooms[0]
current_move = room_names[0]


while room[NAME] != "Computer" and current_move != "Exit":
    # the current exit condition is in the Computer area
    
    # check if the current move is a room name
    if current_move in room_names:
        room_id = room_names.index(current_move)
        room = rooms[room_id]
    else:
        print("Error : that room does not exist.")
        break

    # show room information
    name, description, options = room
    print("\n" + name)
    print(description)
    # show options
    print("\nHere are your options. Enter at least the 3 first characters:")
    for o in options:
        print(f"  [{o}]  ", end="")
    # get the next valid move
    print("\n")
    valid_move = False
    while not valid_move:
        current_move = input("> ")
        if len(current_move) < 3:
            continue
        for o in options:
            if o.lower().startswith(current_move.lower()):
                current_move = o
                valid_move = True
                break

print("Goodbye!")
