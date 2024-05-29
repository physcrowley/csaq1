with open('./data/new_file.txt', 'r') as file:
    data = file.readlines() # reads all the content in one go
print(data) # data available outside of the with block