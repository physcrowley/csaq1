with open("./data/file1.txt", "w", encoding="ansi") as file:
    file.write('Hello, World!')

with open("./data/file1.txt", "r", encoding="utf-8") as file:
    print(file.read())
