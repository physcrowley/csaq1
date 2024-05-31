[Home](index.md#lessons) 

# File IO - 2: Extracting data from a simple file

## Vocabulary

**delimiter**: a character or sequence of characters used to separate fields in a text file. Common delimiters include spaces (the default), commas `,`, tabs `\t`, and pipes `|`, but any character can be used as a delimiter.

**field**: a single piece of data in a text file. Fields are separated by delimiters and their type is usually known. As pure data, they are also called **tokens**.

**record**: a collection of fields that represent a single line in a text file. Hence records are delimited by newlines `\n`.

**method chaining**: a programming technique where one method is called directly on the result of another method. For example, `file.readline()` will return a string. Instead of assigning this result to a variable and applying a string method like `strip()` to that variable, we can chain the method calls together, for example: `file.readline().strip()`. The result of the method on the left is always the object that the method on the right uses.

## Extracting and cleaning fields

Assume we have a text file named `simple_data.txt` with the following content:

```
Jimbo, Johnson, 14, 87.2\n
```

The data appears to be separated by commas, but there are spaces after the commas. 

We can use the `split()` method with the `,` as the delimiter and see if the spaces cause any problems.

```python
with open('simple_data.txt', 'r') as file:
    fields = file.readline().split(',') # split the line into a list of fields
    print(fields) # for educational purposes
    first = fields[0] # to prepare the data for future use
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

### Test your comprehension

Take this short quiz to verify your understanding : [Quick check](./review/2-fields.html)

### Coding challenges

> You can use the JuiceMind platform to complete these challenges with the following classroom: [Physcrowley's Class](https://play.juicemind.com/dashboard/teams/XUUbpCs933IEk84h7SFH/item/802271cf-be62-45b4-9886-2373b8bfd553)

1. Reproduce the code and data file above in your project's folder (write the code in `main.py`). Set the delimiter in the `split()` method to `', '` (comma and space). What happens to the output? Would this remove the need for `strip()` if there was a text field at the end of the record (i.e. just before the newline)? Add your answers as a comment in main.py.

2. Change the data file to remove the comma between the first and last names, and change the code so there is only one variable for the full name (why not `full_name`?). 
   - Don't forget to change the field indexes for the other variables. 
   - Also don't forget to change the print statements. 
   - Does the delimiter in `split()` apply each character individually (i.e. comma OR space) or as a sequence (comma AND space)? How could you tell? Add your answers as a comment in main.py.

3. Create a new data file that includes one record made of several fields of different data types separated by commas. Write a script in your project's `main.py` file that reads, cleans and presents the data in this file just after it reads that data from the `simple_data.txt` file.

<details><summary><i>JuiceMind solutions</i></summary>

<p>main.py</p>

<pre><code class="language-python">	
with open('simple_data.txt', 'r') as file:
    fields = file.readline().split(', ')
    print(fields) # for educational purposes
    # first = fields[0]
    # last = fields[1]
    full = fields[0]
    age = int(fields[1])
    average = float(fields[2])

print("Name:", full, "age:", age, "average:", average)
# print(last, "is Johnson:", last == "Johnson")

"""
Answers
1. The extra spaces disappear in the output and we get:
['Jimbo', 'Johnson', '14', '87.2\n']... however the '\n' is still
there, so we still need a 'strip()' call if the last field is a
string

2. The delimiter is applied as a sequence, not as a set of individual
separators. If they applied individually, then the two names (separated
by a space), would not be a single field but two distinct fields. Instead
we got ['Jimbo Johnson', '14', '87.2\n'] so the ', ' delimiter only applied when both characters were present in that sequence.
"""

#
# ONE POSSIBILITY FOR #3
#

with open("weather.txt", "r") as file:
  fields = file.readline().split(", ")
  # skipping field[0]
  temperature = float(fields[1])
  uv = int(fields[2])
  sky = fields[3].strip()

print("The weather today is", sky, "with a temperture of", temperature, "Celcius")
print("and a UV index of", uv)
</code></pre>

<p>simple_data.txt</p>

<pre>
Jimbo Johnson, 14, 87.2

</pre>	

<p>weather.txt</p>

<pre>
weather, 25.2, 9, sunny

</pre>	

</details>
<p></p>

(C) 2024 David Crowley, EAO
