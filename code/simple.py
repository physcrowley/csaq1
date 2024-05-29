with open('simple_data.txt', 'r') as file:
    fields = file.readline().split(', ')
    print(fields) # for educational purposes
    full = fields[0]
    # last = fields[1].strip()
    age = int(fields[1])
    average = float(fields[2])

print("Name:", full, "age:", age, "average:", average)
# print(last, "is Johnson:", last == "Johnson")