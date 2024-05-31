[Home](index.md#lessons) 

# File IO - 3: Reading and using structured data

## Vocabulary

**structured data**: data that is organised in a predictable way, such as a table. Structured data is easy to read and write by both humans and computers. We will be working with two types of structured data files in this lesson. One is structured as a list of records, where each record is a list of fields (or values). The other is a custom structure based on different delimiters within the file that separate different types of data used to describe a game world.

**unpacking**: the process of assigning the elements of a tuple or a list to individual variables. This is done by placing the variable names on the left side of an assignment statement and the tuple on the right side. For example, if `record = ("David", "Crowley", 42)` - a tuple with three elements, `first`, `last`, and `age` - we can unpack the tuple like this: `first, last, age = record`. With this unpacking, `first` will be assigned the value `"David"`, `last` will be assigned the value `"Crowley"`, and `age` will be assigned the value `42`.

## Examples

- [Weather data analysis](#example-average-monthly-temperature-and-total-monthly-precipitation)
- [Game data](#a-less-data-oriented-example--game-data)

## Example: Average monthly temperature and total monthly precipitation

You can check out weather data for Ottawa, Ontario, Canada at the government of Canada's climate data website: [Climate data for Ottawa](https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=49568) and download the data for the current (and previous years) in CSV format.

One such file has been downloaded for you: [en_climate_daily_ON_6106001_2024_P1D.csv](./public_data/en_climate_daily_ON_6106001_2024_P1D.csv)

We are going to use this file to compile monthly average temperatures and total monthly precipitation for the year 2024.

### Step 1: Open the file yourself and examine its contents

We do this to get an idea of how the data is structured, and also to see if any data is missing or unexpected. A CSV file is easier to read in a spreadsheet program like Microsoft Excel or Google Sheets (which formats the data in rows/records and columns/fields), but you can also open it in a text editor, if you need to. This is what the raw text looks like:

```
"Longitude (x)","Latitude (y)","Station Name","Climate ID","Date/Time","Year","Month","Day","Data Quality","Max Temp (°C)","Max Temp Flag","Min Temp (°C)","Min Temp Flag","Mean Temp (°C)","Mean Temp Flag","Heat Deg Days (°C)","Heat Deg Days Flag","Cool Deg Days (°C)","Cool Deg Days Flag","Total Rain (mm)","Total Rain Flag","Total Snow (cm)","Total Snow Flag","Total Precip (mm)","Total Precip Flag","Snow on Grnd (cm)","Snow on Grnd Flag","Dir of Max Gust (10s deg)","Dir of Max Gust Flag","Spd of Max Gust (km/h)","Spd of Max Gust Flag"
"-75.67","45.32","OTTAWA INTL A","6106001","2024-01-01","2024","01","01","","-4.3","","-8.8","","-6.6","","24.6","","0.0","","0.0","","0.0","T","0.0","T","","","","M","","M"
```

> This is not an easy piece of data to look at, so we will make it easier to read in the next step.

We can see the following things in the file:
- The first line is a header that describes the data in each column. This helps us know which fields to extract from each record for our averages and totals
- The data is in text (all in quotes) and separated by commas without spaces
- Some fields are usually empty
- Some fields that normally have numbers can be empty and but then the letter "M" is in the next field. This is a placeholder for missing data, so we will need to skip these values in our code instead of trying to convert them to numbers.
- All records in the future have entirely empty `""` fields after the date fields. For records in the past with missing data, the value field is also empty, but its flag field has the letter `"M"` in it. We can use this pattern to stop extracting data when we find the first empty data field that also has an empty flag field.

### Step 2: Extract some of the data

We can run a short program to extract the header from the file and print it out so we can see what fields we have to work with. 

> If you save the data file directly in your project directory, the file path will be just the file name. Otherwise, adjust the file path in your own code accordingly. For example, if it is in a `data` subfolder, the file path would be `'./data/en_climate_daily_ON_6106001_2024_P1D.csv'` instead.

```python
# File: weather.py

with open('en_climate_daily_ON_6106001_2024_P1D.csv', 'r') as file:
    header = file.readline().strip().split(',') # get the header line and clean it up
    first_record = file.readline().strip().split(',') # also get the first record
    
    # print each field's index, name and a sample value in fixed-width columns
    for i in range(len(header)):
        print(f"{i:2} {header[i]:30} {first_record[i]:10}")
```

This produces the output:

```
 0 "Longitude (x)"                "-75.67"  
 1 "Latitude (y)"                 "45.32"
 2 "Station Name"                 "OTTAWA INTL A"
 3 "Climate ID"                   "6106001"
 4 "Date/Time"                    "2024-01-01"
 5 "Year"                         "2024"
 6 "Month"                        "01"
 7 "Day"                          "01"
 8 "Data Quality"                 ""
 9 "Max Temp (°C)"                "-4.3"
10 "Max Temp Flag"                ""
11 "Min Temp (°C)"                "-8.8"
12 "Min Temp Flag"                ""
13 "Mean Temp (°C)"               "-6.6"
14 "Mean Temp Flag"               ""
15 "Heat Deg Days (°C)"           "24.6"
16 "Heat Deg Days Flag"           ""
17 "Cool Deg Days (°C)"           "0.0"
18 "Cool Deg Days Flag"           ""
19 "Total Rain (mm)"              "0.0"
20 "Total Rain Flag"              ""
21 "Total Snow (cm)"              "0.0"
22 "Total Snow Flag"              "T"
23 "Total Precip (mm)"            "0.0"
24 "Total Precip Flag"            "T"
25 "Snow on Grnd (cm)"            ""        
26 "Snow on Grnd Flag"            ""
27 "Dir of Max Gust (10s deg)"    ""
28 "Dir of Max Gust Flag"         "M"
29 "Spd of Max Gust (km/h)"       ""
30 "Spd of Max Gust Flag"         "M"
```

From this output, we can identify fields that will be handy:

- The `Month` field (index 6) will be used to group the data by month
- The `Mean Temp (°C)` field (index 13) will be used to calculate the average temperature for each month
- The `Total Precip (mm)` field (index 23) will be used to calculate the total precipitation for each month

We can also see that:

- all the data is surrounded by actual quotes `"`, so we will need to strip these off when we extract the data.
- each data field has its own flag field that seems to be empty when the data is present and `"M"` when the data is missing. We can use this to skip missing data when calculating the averages and totals.

### Step 3: Extract all the data

Before writing our code, it is a good idea to have a plan that takes into account everything we know about the data and about the calculation we want to do. For example, we can't immediately convert the temperature and precipitation fields to numbers because some of the values are missing. We will need some kind of condition to decide wether to skip the value or to convert it to a number. We also need to decide if we do this when creating the records or when calculating the averages and totals. 

There are a number of such decisions that need to be made to manage the data effectively.

This is one possible implementation:

```python
# File: weather.py

# create data list to hold the records
data = []

""" Read the file """

# field indexes in the data file
month = 6
temp = 13
precip = 23

# extract selected fields from all valid records in the file
with open("en_climate_daily_ON_6106001_2024_P1D.csv", "r") as file:
    for line in file:
        fields = line.strip().split(",")
        # check for completely empty data fields (end of data)
        if fields[temp] == '""' and fields[temp + 1] == '""':
            break
        # strip quotes before adding chosen fields to the record
        record = (
            fields[month].strip('"'),
            fields[temp].strip('"'),
            fields[precip].strip('"'),
        )
        # add the record to the data list
        data.append(record)


""" Compile data from the records """

# initialize collector and flag variables
current_month = data[1][0]
temp_count = 0
temp_sum = 0
precip_sum = 0

# initialize output list with the header record
monthly_data = [data[0]]  
# iterate over other records
for i in range(1, len(data)):
    # unpack the record
    month, temp, precip = data[i]
    # when the month changes
    if month != current_month:
        # create new record for the previous month
        last_month = (current_month, temp_sum / temp_count, precip_sum)
        monthly_data.append(last_month)
        # update the current month
        current_month = month
        # reset the counters
        temp_count = 0
        temp_sum = 0
        precip_sum = 0
    # accumulate data for the current month, skipping missing values
    if len(temp) > 0:
        temp_sum += float(temp)
        temp_count += 1
    if len(precip) > 0:
        precip_sum += float(precip)

# add the last month
last_month = (current_month, temp_sum / temp_count, precip_sum)
monthly_data.append(last_month)

# display the results in a table format
for record in monthly_data:
    # unpack the record
    month, temp, precip = record
    if month == monthly_data[0][0]:
        # header record
        print(f"{month:10} {temp:>15} {precip:>20}")
    else:
        # data records
        print(f"{month:10} {temp:15.1f} {precip:20.1f}")
```

For the included file, this code produces the following output:

```
Month       Mean Temp (°C)    Total Precip (mm)
01                    -6.1                 52.0
02                    -3.9                 16.0
03                     1.8                 39.4
04                     6.8                107.8
05                    15.8                 98.1
```

## A less data-oriented example : Game data

If you are designing a game, all the text data you need to store can be structured in a similar way instead of spreading the text throughout the code. This usually makes it a lot easier to update the game content without having to worry about breaking the game logic.

For example, in a text-based adventure game, you could store the game's text in a file with the following structure:

```
### 
Room/Area Name
(empty line)
Description
(empty line)
Option 1, Option 2, Option 3
```

- The `###` is a marker that indicates the start of a new area. It is followed by the room's name, description and options.
- The empty line (`\n\n`) separates the room name, the description and the options.
- The options are separated by commas and a space (`, `).

### Sample game data file

Let's say we have the following text in a file named `game_data.txt`:

```
Dark basement

You are in a dim basement, lit only by the pale glow of the computer screen.
It has been days since you have seen the sun.

Main floor, Computer, Furnace room

###
Main floor

You are on the main floor of the house. It is raining outside, but there is
an interesting smell coming from the kitchen.

Dark basement, Kitchen

###
Kitchen

Mmmmmm, coffee!

Main floor, Dark basement

###
Computer

You see a screen with a blinking cursor. It is waiting for your command.
In fact, it is waiting for you to type `exit`.

Exit

###
Furnace room

What a mess! You can't even see the furnace for all the junk in here.
Oh wait! Is that my old skateboard?

Dark basement

```

- Notice that every single option is the name of a room. This is a simple way to manage the game's navigation.

### Using the structured game data

We can use this data in a fairly simple game engine that relies on extracting all the file data into program memory then using the various structural elements to extract and find the data we need.

```python
# File: game.py

""" Extract and organize the game data """

# read data into memory
with open("game_data.txt", "r") as file:
    data = file.read()

# split the data into rooms
rooms = data.strip().split("###")  

# split each room into sections
for i in range(len(rooms)):
    rooms[i] = rooms[i].strip().split("\n\n")

NAME = 0
DESCRIPTION = 1
OPTIONS = 2

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
```	

The great thing about this approach is that you can add new areas, descriptions, and options to the game without changing the code. You can even add new types of data to the file and modify the code to handle it without changing the existing code. The game play still needs to be developed, but the basic game data is fairly straightforward to manage.

## 📝 Practice

### Coding challenges

> You can use the JuiceMind platform to complete these challenges with the following classroom: [Physcrowley's Class](https://play.juicemind.com/dashboard/teams/XUUbpCs933IEk84h7SFH/item/802271cf-be62-45b4-9886-2373b8bfd553)

1. Copy these examples and their data files into your project folder and run them. Make sure no transcription errors have been introduced during the copying and that the file paths are correct when attempting to open the files.
2. Change the algorithm in `weather.py` to extract different information from the data. For example, the maximum and minimum temperatures for the year or the longest stretch of days with no precipitation.
3. Change the game data in `game_data.txt` to add a new area and some options. Run the game and see if the new area is accessible and if the options work as expected.
4. Try adding some more logic to the game to make it more interesting. For example, you could add items to collect (a new section in the data file plus logic to handle them in the game loop) or you could add dangers/enemies to avoid.

<details><summary><i>JuiceMind solutions</i></summary>

<p>Flat file structure once the code and data have been copied into the project folder:</p>

<pre>
project/
├── en_climate_daily_ON_6106001_2024_P1D.csv
├── game.py
├── game_data.txt
├── main.py
└── weather.py
</pre>

<p>main.py</p>

<pre><code class="language-python">
# Simply import the script here to run it. Comment out the ones you don't want to run.

# import weather
import game
</code></pre>

<p>Other file contents begin as described in the notes but should morph. Here is one possibility for each file after the changes:</p>

<p>weather.py</p>

<pre><code class="language-python">
# File: weather.py

"""
Modified to output maximum and minimum temperatures recorded during the year and the longest stretch of days without any precipitation.

The file reading portion was changed to exclude the month value from the record since it is not needed, but added the date value for the output.

The data compilation algorithm was significantly changed.
"""

# create data list to hold the records
data = []

""" Read the file """

# field indexes in the data file
# month = 6
date_str = 4
temp = 13
precip = 23

# extract selected fields from all valid records in the file
with open("en_climate_daily_ON_6106001_2024_P1D.csv", "r") as file:
    for line in file:
        fields = line.strip().split(",")
        # check for completely empty data fields (end of data)
        if fields[temp] == '""' and fields[temp + 1] == '""':
            break
        # strip quotes before adding chosen fields to the record
        record = (
            # fields[month].strip('"'),
            fields[date_str].strip('"'),
            fields[temp].strip('"'),
            fields[precip].strip('"'),
        )
        # add the record to the data list
        data.append(record)


""" Compile data from the records """

# initialize collector and flag variables with first data record
date, temp, precip = data[1]

max_T = float(temp)
max_date = date
min_T = float(temp)
min_date = date
streak = 1 if precip == 0 else 0
max_streak = streak
streak_start = date
streak_end = date

# iterate over other records
for i in range(2, len(data)):
    # unpack the record
    date, temp, precip = data[i]
    # check if max values need updating
    if len(temp) > 0:
        temp = float(temp)
        if temp > max_T :
          max_T = temp
          max_date = date
        elif temp < min_T :
          min_T = temp
          min_date = date
    if len(precip) > 0:
        if float(precip) == 0: # on a streak
          streak += 1
          if streak > max_streak:
            max_streak = streak
            streak_start = data[i-streak][0]
            streak_end = date
        else: # streak ends
          streak = 0

print(f"The highest recorded temperature was {max_T}C on {max_date}")
print(f"The lowest recorded temperature was {min_T}C on {min_date}")
print("The longest number of days with no precipitation was", max_streak, "days from", streak_start, "to", streak_end)
</code></pre>

<p>game_data.txt</p>

<pre>
Dark basement

You are in a dim basement, lit only by the pale glow of the computer screen.
It has been days since you have seen the sun.

Main floor, Computer, Furnace room

sock, bag of chips

Eww! That's smelly!, All dressed are the best

###
Main floor

You are on the main floor of the house. It is raining outside, but there is
an interesting smell coming from the kitchen.

Dark basement, Kitchen, Bathroom

keys

Wonder what this opens?

###
Kitchen

Mmmmmm, coffee!

Main floor, Dark basement

steaming mug of joe

That's what I needed

###
Computer

You see a screen with a blinking cursor. It is waiting for your command.
In fact, it is waiting for you to type `exit`.

Exit

power button

Time for sleep

###
Furnace room

What a mess! You can't even see the furnace for all the junk in here.
Oh wait! Is that my old skateboard?

Dark basement

skateboard, broken electronics box

I should take this for a ride, I'm sure this will come in handy one day

###
Bathroom

The white ceramic gleams menacingly. There is a strong odour of soap.

Main floor

toothbrush

I should make my teeth gleam menacingly too!

</pre>

<p>game.py</p>

<pre><code class="language-python">
# File: game.py

"""
Added items and an associated item-message list to each room

Updated the file reading and game logic accordingly
"""

""" Extract and organize the game data """

# read data into memory
with open("game_data.txt", "r") as file:
    data = file.read()

# split the data into rooms
rooms = data.strip().split("###")  

# split each room into sections
for i in range(len(rooms)):
    rooms[i] = rooms[i].strip().split("\n\n")

NAME = 0
DESCRIPTION = 1
OPTIONS = 2
ITEMS = 3
ITEM_MSGS = 4

room_names = [r[NAME] for r in rooms]

for r in rooms:
    # split options section into a list of options
    r[OPTIONS] = r[OPTIONS].strip().split(", ")
    # split items section into a list of items
    r[ITEMS] = r[ITEMS].strip().split(", ")
    # split item_message section into a list of item_messages
    r[ITEM_MSGS] = r[ITEM_MSGS].strip().split(", ")


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
collected_items = []
current_item = None


while room[NAME] != "Computer" or current_move == "power button":
    # the current exit condition is in the Computer room... but the power
    # button item shows a special message before triggering the exit

    # interpret the current move as navigation or item selection
    if current_move in room_names:
        room_id = room_names.index(current_move)
        room = rooms[room_id]
        show_description = True
    else:
        item_id = room[ITEMS].index(current_move)
        item_name = room[ITEMS][item_id]
        item_msg = room[ITEM_MSGS][item_id]
        # show item message
        print("\n| ", item_msg)
        # special exit condition
        if item_name == "power button":
            print("Shutting down... ", end="")
            break
        # update collection and show results
        collected_items.append(item_name)
        print("|  You have added", item_name, "to your collection.")
        print("|  Inventory: ", collected_items)
        # skip the room description
        show_description = False

    # extract room data
    name, description, options, items, item_msgs = room

    # show room information
    print("\n" + name)
    if show_description:
        print(description)
    # show navigation options
    print("\nYou can go here: ", end="")
    for o in options:
        print(f"  [{o}]  ", end="")
    # show items available to pick up
    print("\nOr you can pick up one of these items : ", end="")
    available_items = [i for i in items if i not in collected_items]
    for i in available_items:
        print(f"  [{i}]  ", end="")
    if len(available_items) == 0:
        print("(nothing here)", end="")
    print("\n")
    # get the next valid move
    print("Enter your move (at least 3 characters)")
    valid_move = False
    while not valid_move:
        current_move = input("> ")
        if len(current_move) < 3:
            continue
        for e in options + available_items:
            if e.lower().startswith(current_move.lower()):
                current_move = e
                valid_move = True
                break

print("Goodbye!")
</code></pre>


</details>

<p></p>

(C) 2024 David Crowley, EAO
