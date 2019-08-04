----
TRANSPOSE THE MAX LENGTH WORD
----

### Goals
This is a script designed to find the longest word in the text file, transpose the letters and show 
the result. 

The code for the script is contained in a single file and is self-documented.
With '--help', you can get the purpose of the script as well as the options it accepts.
The script has multiple functions. Each function is responsible only for one action.

- file_reading(): reads the txt file line by line and returns the result as a list of strings where one line
is equal to one list element. Script does not make any strings adjustment.
- transpose(): goes through the list of string and looks for the largest word, transpose it and prints the result
on the screen.
- parse_args(): parse CLI arguments, and keeps info about each argument.
- setup_logging(): that method is responsible for logging.
- main(): runs the process of reading the file and analyse it. If user sends the path to the folder with files,
the pool of processes will be created - one for each CPU.

You can also run unittests with:
    $ python3 tests.py -v

#### Requirements
* Python 3+

#### The functionality:
1. Read input from a file of words;
2. Find the largest word in the file
3. Transpose the letters in the largest word
4. Show the largest word and the largest word transposed

#### Assumptions:
- Accepts files in plain text format only.
- The result will be present on the screen only.
- If the list has multiple words with the same "maximum" size, the script returns the first one.
- If the word has digits as a part of the word, like 'Ford2", digits will be ignored (based on #3 of requirements).
- If the word has 2 parts like Sierra-Nevada or sierra_nevada, the script accepts it as one word. But if there are
spaces at least from one side of "-", like Sierra - Nevada, the script accepts it as 2 words.
- All punctuation symbols and special symbols also will be ignored based on req #3.

#### How to run:
usage: main.py [-h] [-f F] [-p P] [--debug | --silent]

optional arguments:
*  -h, --help    show this help message and exit
*  -f F          Path to the file
*  -p P          Path to the folder with multiple files
*  --debug, -d   enable debugging mode
*  --silent, -s  enable silent (only critical) mode

`$ python3 main.py -f /path_to_folder/file_name.txt`

Some test txt files can be found in `/txt_files/` folder

Example output:
    
    Original: abcde
    Transposed: edcba
