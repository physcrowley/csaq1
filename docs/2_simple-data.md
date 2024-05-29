[Home](index.md#lessons) 

# File IO - 2: Extracting data from a simple file

## Vocabulary

**delimiter**: a character or sequence of characters used to separate fields in a text file. Common delimiters include spaces ` `, commas `,`, tabs `\t`, and pipes `|`, but any character can be used as a delimiter.

**field**: a single piece of data in a text file. Fields are separated by delimiters.

**record**: a collection of fields that represent a single entity in a text file. Records are separated by newlines `\n`.

**method chaining**: a programming technique where one method is called directly on the result of another method. For example, `file.readline()` will return a string. Instead of assigning this result to a variable and applying a string method like `strip()` to that variable, we can chain the method calls together, for example: `file.readline().strip()`. The result of the method on the left is always the object that the method on the right uses.

## Extracting and cleaning fields

Assume we have a text file named `simple_data.txt` with the following content:

```
Jimbo, Johnson, 14, 87.2\n
```

The data appears to be separated by commas, but there are spaces after the commas. We can just use the `split()` method with the `,` as the delimieter and see if the spaces cause any problems.

```python
with open('simple_data.txt', 'r') as file:
    fields = file.readline().split(',')
    print(fields) # for educational purposes
    first = fields[0]
    last = fields[1]
    age = int(fields[2])
    average = float(fields[3])

print("Name:", first, last.upper(), "age:", age, "average:", average)
```

The output of this code is:

```
['Jimbo', ' Johnson', ' 14', ' 87.2\n']
Name: Jimbo  JOHNSON age: 14 average: 87.2
```

We can see that the individual fields include leading and trailing spaces: ` Johnson`, ` 14` and ` 87.2\n`. However, the casting functions `int()` and `float()` ignore leading and trailing spaces when converting strings to numbers, so we didn't need to do that ourselves with the `strip()` method on each field.

There is an additional space in front of the last name that is noticeable when we output the data. Does it affect comparisons? We can check by adding a comparison to the code:

```python
print(last, "is Johnson:", last == "Johnson")
```

which gives us this additional line of output:

```
 Johnson is Johnson: False
```

To fix this, we add the `strip()` method to the `last` variable:

```python
last = fields[1].strip()
```

Now the output is:

```
['Jimbo', ' Johnson', ' 14', ' 87.2\n']
Name: Jimbo JOHNSON age: 14 average: 87.2
Johnson is Johnson: True
```

## Basic rule for using `strip()`

It's probably better to use it than not, but :

- It should always be used to clean string fields
- It is optional for numeric fields because the casting functions `int()` and `float()` will ignore leading and trailing spaces


## 📝 Practice

### Coding challenges

1. Reproduce the code and data file above in your project's folder (write the code in `main.py`). Set the delimiter in the `split()` method to `', '` (comma and space). What happens to the output? Would this remove the need for `strip()` if there was a text field at the end of the record (i.e. just before the newline)? Add your answers as a comment in main.py.

2. Change the data file to remove the comma between the first and last names, and change the code so there is only one variable for the full name (why not `full_name`?). Don't forget to change the field indexes for the other variables. Also don't forget to change the print statements. Does the delimiter in `split()` apply each character individually (i.e. comma OR space) or as a sequence (comma AND space)? How could you tell? Add your answers as a comment in main.py.

3. Create a new data file that includes one record made of several fields of different data types separated by commas. Write a script in your project's `main.py` file that reads, cleans and presents the data in this file after it reads that data from the `simple_data.txt` file.