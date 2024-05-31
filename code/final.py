"""
Name: David Crowley
Date: May 31st, 2024
File: main.py
Description:
This is an exemplar for the final task in the File IO unit.

The generated data is structured as follows, using a ~ as the delimiter because the
text itself can contain commas:

Random text~Random number

The program generates 100 of these records and saves them to a file called "data.txt".

It then reads the file and calculates the average word length and the finds the biggest
number in the file.

Finally it writes the results to a file called "results.txt".

~~~~~~~

For generation the random text, it uses a random substring from an excerpt from Oliver 
Twist that is saved in the `final_random_source.txt` file. The random number is just 
the sum of the ASCII values of the characters in the random text divided by a random number.
"""

import random

#
# GENERATE THE DATA
#

# get the source text for generating the random strings

with open("final_random_source.txt", "r") as f:
    source_text = f.read()

# remove all the newlines and extra spaces
source_text = source_text.replace("\n", " ").replace("  ", " ")

n = 101 # number of records to generate
text_values = []
number_values = []

# generate the random text values
size = 20 # max length of each value
max = len(source_text) - size

for i in range(n):
    start = random.randint(0, max)
    end = start + random.randint(3, size)
    text_values.append(source_text[start:end])

# generate the random number values
for text in text_values:
    number = sum([ord(c) for c in text])
    number /= random.randint(3, 7)
    number_values.append(number)

#
# WRITE THE DATA TO A FILE
#

with open("data.txt", "w") as f:
    f.write("Text~Number\n")
    for i in range(n):
        f.write(f"{text_values[i]}~{number_values[i]}\n")

#
# READ THE DATA FROM THE FILE AND ANALYZE IT
#

with open("data.txt", "r") as f:
    f.readline() # skip the header
    lines = f.readlines()

# traverse the lines to calculate the average word length and track the biggest number

quantity = len(lines)
total_length = 0
biggest_number = 0
biggest_number_text = ""

for line in lines:
    text, number = line.strip().split("~") # split the line into text and number
    # collect the length of the text
    total_length += len(text)
    # check if the number is the biggest
    number = float(number)
    if number > biggest_number:
        biggest_number = number
        biggest_number_text = text

average_length = total_length / quantity

#
# PREPARE THE OUTPUT
#

# as a string
output = f"Average word length: {average_length:.1f}\n"
output += f"Biggest number: {biggest_number:.1f} ('{biggest_number_text}')\n"

# to a file
with open("results.txt", "w") as f:
    f.write(output)

# to the console
print(output)
