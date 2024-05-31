[Home](index.md#lessons) 

# File IO - 5: Writing output to a file

...this one is also left as an exercice for the reader. 😂 The content of this lesson is not yet written.

## Vocabulary

**overwrite**: to replace the contents of a file with new data. This corresponds to the `"w"` mode of file access in Python. When you do this programmatically (ie. with your program's instructions), there are no helpful "are you sure?" prompts like you might get in a word processor, so be careful and keep backup copies of important data.

**append**: to add new data to the end of an existing file. his corresponds to the `"a"` mode of file access in Python. This is a safer way to add data to a file without losing the old data. Log files are often written in append mode so that all the historical data is preserved.

**newline**: the character or characters that indicate the end of a line in a text file. This is usually a single character, but on some systems it can be two characters. In Python, the newline character is `"\n"`. The `write()` method of a file object does not automatically add a newline character to the end of the data it writes, so you must add it yourself if you want to write data line-by-line.

## Example: writing a list of numbers to a file


## Example: keeping track of user data, like names and high scores


## Example: writing a log file for time spent running a program


## 📝 Practice

### Coding challenges

1. Take any program you have previously written during this course that printed output to the console. Make a copy of the program and modify it so that it writes the output to a file instead of the console.


(C) 2024 David Crowley, EAO