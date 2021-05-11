# Ten-pin Bowling

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

For a detailed look at the rules, check out: https://en.wikipedia.org/wiki/Ten-pin_bowling#Scoring

---

## Prerequisites
Python 3.6+ must be installed before running the program.  
Follow the instructions at https://realpython.com/installing-python/ for your operating system.

---
## Getting Started
1. Clone this repository
1. Navigate to the root level.
1. Run `python3 main.py`
1. Enter a number between 2 to 4 for the number of players.
1. For each player, enter a name. They do not need to be unique.
1. Take a look at the simulated bowling game output! The winner will be the last thing printed out.

---

## Running tests

* Tests are included to catch different edge cases and make sure the program returns the expected value.
* Run `python3 -m unittest tests.py`

---

## Example Output
```
How many players? Up to 4...
4
Enter Player 1's name...
Jim
Enter Player 2's name...
Amanda
Enter Player 3's name...
Terry
Enter Player 4's name...
Steph

---------------------
FINAL SCOREBOARD
---------------------

***********************
Jim 

| 2 6 | 7 / | 2 0 | X | 4 4 | 1 1 | 8 1 | 1 2 | 9 0 | 0 / 3 | 

Total: 84
***********************

***********************
Amanda 

| 3 0 | 4 / | 1 / | 0 4 | 3 1 | 2 7 | 7 / | 1 7 | 0 0 | 9 / 5 | 

Total: 75
***********************

***********************
Terry 

| 4 0 | 8 0 | 4 4 | 9 0 | 3 3 | 9 / | 8 1 | 3 4 | 3 0 | 8 / 2 | 

Total: 84
***********************

***********************
Steph 

| 9 / | 9 0 | 9 / | 7 1 | 4 0 | 7 1 | 8 / | 3 0 | 6 1 | 0 1 | 

Total: 89
***********************

********************

WINNER, WINNER, SOMETHING DINNER!

Steph won!!!

********************
```
