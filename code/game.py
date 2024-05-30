# File: game.py

""" Extract and organize the game data """

# read data into memory
with open("./data/game_data.txt", "r") as file:
    data = file.read()

# created nested lists from the data
rooms = data.strip().split("###")  # split the data into rooms
# split each room into sections
for i in range(len(rooms)):
    rooms[i] = rooms[i].strip().split("\n\n")
# split options section into a list of options
for r in rooms:
    r[2] = r[2].strip().split(", ")


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
current_move = "Dark basement"
current_room = ""

# the current exit condition is in the Computer area
while current_room != "Computer" and current_move != "Exit":
    current_room = current_move

    # find the current room
    room = None
    for r in rooms:
        if r[0] == current_room:
            room = r
            break
    if room is None:
        print("Error: Room not found")
        break
    # show room information
    name, description, options = room
    print("\n" + name)
    print(description)
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
