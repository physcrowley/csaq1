[Home](index.md#lessons) 

# File IO - 1: Using the `with` keyword and `open()` to manage file access

## Vocabulary

**file path**: text representing the sequence of folders from a reference point to a specific file, including the file's name and extension. Folders and files are separated by slashes, and Python will recognize the forward slash `/` on all systems even Windows (whose official path separator is the backslash `\`). For example, the file path `C:/Users/username/Documents/file.txt` represents a file named `file.txt` in the `Documents` folder of the `username` folder in the `Users` folder on the `C:` drive.

**special folders**: character sequences at the beginning of a file path that represent special cases. `..` represents the parent folder of the current folder, `.` represents the current folder, `~` represents the user's home folder and `/` represents the root folder of the current drive. These special folders are recognised on all systems (except some old versions of Window that use Command Prompt instead of Powershell as the default shell).

- Using special folders, the path from the previous example could be written as `/Users/username/Documents/file.txt` or, even better, `~/Documents/file.txt` to represent the same file in the user's home folder.
- Python projects take the script's (often `main.py`'s) folder as the current folder, so `.` is often used at the beginning of file paths to refer to project files.

**resource**: a file, network connection, or other external data source that a program uses. Resources are limited and must be managed carefully to avoid conflicts between programs or between a program and the operating system.

**context manager**: an object that manages a resource and ensures that it is properly closed or released when it is no longer needed. The `with` keyword is used to create a context manager in Python.

**file encoding**: the character set and encoding used to represent text in a file. Common encodings include ANSI, UTF-8, and UTF-16. Python uses UTF-8 as the default encoding for reading and writing text files, but some Windows files may be written in ANSI. Since all encodings are compatible with ASCII, reading a file in the wrong encoding will not cause an error if the file only contains ASCII characters. This works well for English text, but other languages (like French) regularly include characters beyond the ASCII table and specifying the encoding becomes important.

## File structures and file paths

Python projects that use files outside of the script are often structured with subfolders for the different types of files they contain. Here is one example of a project that includes data files, images and sounds :

```
project
│
├── data
│   ├── file1.txt
│   ├── file2.txt
│   └── file3.txt
│
├── images
│   ├── image1.png
│   ├── image2.png
│   └── image3.png
│
├── sounds
│   ├── sound1.wav
│   ├── sound2.wav
│   └── sound3.wav
│
└── main.py
```

Notice that folder names do not have file extensions, but file names do (`.txt`, `.png`, `.wav`, `.py`, etc.).

To refer to any of these files from the code in `main.py`, we need to use the appropriate file path. For example, to refer to `file2.txt` in the `data` subfolder, we would use the file path `./data/file2.txt`:

- `.` refers to the current folder, which is the project folder in this case.
- `/data` refers to the `data` subfolder of the project folder.
- `/file2.txt` refers to the `file2.txt` file in the `data` subfolder.


### Try it out 

Take this short quiz to verify your understanding : [Quick check](./review/1-paths-quiz.html)

## The open() function, its options and methods

The `open()` function is used to open a file and return a file object. The file object is used to read or write data to the file. The `open()` function takes one required argument (file_path) and several optional arguments (mode, encoding, etc.). We will only look at the `mode` argument in this lesson, but file encoding may be important when working with files that contain non-ASCII characters.

```python
file = open(file_path, mode)
```

- `file_path` is the path to the file to be opened, as described above.
- `mode` is a string that specifies how the file should be opened. The most common modes for text files are:
  - `'r'` (read): opens the file for reading. The file must exist. This is the default mode.
  - `'w'` (write): opens the file for writing. If the file does not exist, it will be created. If the file does exist, it will be overwritten.
  - `'a'` (append): opens the file for writing. If the file does not exist, it will be created. If the file does exist, new data will be added to the end of the file.

The file object returned by `open()` has several methods that can be used to read or write data to the file. The most common methods are:

- For reading (in 'r' mode):
  - `read()`: reads the entire file and returns its contents as a (possibly enormous) string.
  - `readline()`: reads the next line of the file and returns it as a string.
  - `readlines()`: reads all the lines of the file and returns them as a list of strings.
- For writing (in 'w' or 'a' mode):
  - `write(data)`: writes the data to the file.

> We will see some examples for these methods in the coding challenges below and again in the next lessons.

Finally, the file object returned by `open()` must be closed when it is no longer needed. This is done using the `close()` method:

```python
file.close()
```

If the file is not closed, the operating system may not release the file's resources, which can cause problems for other programs that need to access the file.

## Using the `with` keyword

The `with` keyword is used to help manage files and other resources in Python. It basically makes sure everything is clean and tidy when we are done with a file or if an error occurs in our program while we are using the file.

### Without `with` - just `open()` and `close()`

```python
file = open(file_path, mode)
# do something with the file
file.close()
```

### With ... well, `with`

```python
with open(file_path, mode) as file:
    # do something with the file
```

The second example is more concise and easier to read. 

The `with` command uses the `as` keyword to assign the file object to a variable that we can name as we please, just as with any variable. The file object is only available within the `with` block, so all file operations need to be done there.

This is because the close operation is included automatically and implicitly at the end of the block so we don't have to worry about it. However, it does mean that the file is not available outside of the `with` block.

## 📝 Practice

### Coding challenges

> You can use the JuiceMind platform to complete these challenges with the following classroom: [Physcrowley's Class](https://play.juicemind.com/dashboard/teams/XUUbpCs933IEk84h7SFH/item/802271cf-be62-45b4-9886-2373b8bfd553)

In your project folder, write a Python script named `file_io_1.py` that includes the following code for writing to a new file:

```python	
with open('./data/new_file.txt', 'w') as file:
    file.write('Hello, world!')
    file.write('is this on a new line?')
    file.write('\nwhat about now?')
```

1. Did the program create a data folder if it didn't exist? Or did it crash? If it crashed, create the folder manually in your editor and run the program again.
1. Add comments to answer the questions in the write statements.

Now write a Python script named `file_io_2.py` that includes the following code for reading from the file you just created line-by-line using a loop:

```python
with open('./data/new_file.txt', 'r') as file:
    for line in file:
        print(line)    
```

1. Does the program print the text as you expected? If not, why not?
2. Inside the print function, add `.strip()` to the `line` variable. This removes extra whitespace characters from the beginning and end of the text. Run the program again and see if the output is as you expected.

In the two previous scripts, none of the data in the `with` block is available later in the program (except by reading the file again). The next example is different. Write a Python script named `file_io_3.py` that includes the following code:

```python
with open('./data/new_file.txt', 'r') as file:
    data = file.read() # reads all the content in one go
print(data) # outside of the with block
```

1. Does the program print the text as you expected? Does it give you an error?
2. Change the `read()` method to `readlines()`  (plural) and run the program again. What is the difference in the output?


<details><summary><i>JuiceMind solutions</i></summary>

<p>File structure</p>

<pre>
project/
├── data/
|   └── new_file.txt
├── file_io_1.py
├── file_io_2.py
├── file_io_3.py
└── main.py
</pre>

<p>main.py</p>

<pre><code class="language-python">
# Add an import statement for the script you want to run.
# This file should only have a single import statement in it.

# For example, to run file_io_1.py uncomment the next line:
# import file_io_1
# import file_io_2
import file_io_3
</code></pre>

<p>./data/new_file.txt</p>

<pre>
Hello, world!is this on a new line?
what about now?

</pre>	

<p>file_io_1.py</p>

<pre><code class="language-python">
with open('./data/new_file.txt', 'w') as file:
    file.write('Hello, world!')
    file.write('is this on a new line?')
    file.write('\nwhat about now?')

"""
Answers

1. The program crashed. I had to add the main folder manually
for it to work.

1. The second write data is on the same line as the first
write data. You need to use the \n with write, unlike with 
print.
"""
</code></pre>

<p>file_io_2.py</p>

<pre><code class="language-python">
with open('./data/new_file.txt', 'r') as file:
    for line in file:
        print(line.strip())  

"""
Answers

1. There is an extra space between the lines that isn't there
in the file.

1. Adding .strip() fixed the appearance of the text. Both the
printed lines and the file contents look the same.
"""
</code></pre>	

<p>file_io_3.py</p>

<pre><code class="language-python">
with open('./data/new_file.txt', 'r') as file:
    data = file.readlines() # reads all the content in one go

print(data) # outside of the with block

"""
Answers

1. It prints as expected. The data variable seems to be available
outside the with block. And all the data in on single print statement
didn't affect the line returns within the data.

1. The data variable is now a list containing each line in the file
as a separate element. The \n character is visible at the end of the
first line.
"""
</code></pre>

</details>

(C) 2024 David Crowley, EAO
