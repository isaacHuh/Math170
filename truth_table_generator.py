import itertools
from tabulate import tabulate
from collections import OrderedDict

# http://stackoverflow.com/questions/4284991/parsing-nested-parentheses-in-python-grab-content-by-level
# https://www.programiz.com/python-programming
# https://codereview.stackexchange.com/questions/145465/creating-truth-table-from-a-logical-statement
# https://stackoverflow.com/questions/6336424/python-build-a-dynamic-growing-truth-table
#https://www.geeksforgeeks.org/python-list-pop/

symbols = ['+', '|', '>', '#','@']

statement = input()
original_statement = statement

variables = []
for char in statement:
    if char.isalpha() and not(char in variables):
        variables.append(char)
variables.sort()

def solve_exp(exp):
    exp = exp.replace(' ', '')
    temp = exp[:]
    for i, char in enumerate(exp):
        if char == '~':
            if(int(exp[i+1]) == 1):
                negated = '0'
            elif(int(exp[i+1]) == 0):
                negated = '1'
            temp = temp.replace('~'+exp[i+1], negated)
    exp = temp

    for i, char in enumerate(exp):
        if char in symbols:
            operation = char
            val_1 = int(exp[i-1])
            val_2 = int(exp[i+1])

            if operation == '+':
                if val_1 and val_2:
                    solved = True
                else:
                    solved = False
            if operation == '|':
                if val_1 or val_2:
                    solved = True
                else:
                    solved = False
            if operation == '>':
                if val_1 and not val_2:
                    solved = False
                else:
                    solved = True
            if operation == '#':
                if val_1 == val_2:
                    solved = True
                else:
                    solved = False
            if operation == '@':
                if val_1 == val_2:
                    solved = False
                else:
                    solved = True

    try:
        return int(solved)
    except:
        return int(exp)

# Add brackets to ends
if statement[0] != '(':
    statement = '(' + statement + ')'

truth_lst = []
for bools in itertools.product([1, 0], repeat = len(variables)):
    #this combines two lists as a dictionary and appends it to the truth list
    truth_lst.append(dict(zip(variables, bools)))

truth_table = []
for truth_values in truth_lst:
    val_str = statement
    for variable in truth_values:
        bool_string = str(truth_values[variable])
        val_str = val_str.replace(variable, bool_string)
        
    ordered_truth_values = OrderedDict(sorted(truth_values.items()))

    while len(val_str) > 1:
        stack = []
        lst = []
        for i, char in enumerate(val_str):
            if char == '(':
                stack.append(i)
            elif char == ')' and stack:
                lst.append((len(stack), val_str[stack.pop() + 1: i]))

        brackets_list = lst

        lowest_level = max([i for (i,j) in brackets_list])
        for level, string in brackets_list:
            if level == lowest_level:
                bool_string = str(solve_exp(string))
                # to make sure all imports are in the same format
                val_str = val_str.replace('('+string+')', bool_string)

    truth_table.append(list(ordered_truth_values.values()) + [val_str])


print("\n" + "Table:" + "\n" + (tabulate(truth_table, headers=variables + [original_statement]))) 

