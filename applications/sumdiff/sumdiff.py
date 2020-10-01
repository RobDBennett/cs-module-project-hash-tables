"""
find all a, b, c, d in q such that
f(a) + f(b) = f(c) - f(d)
"""

#q = set(range(1, 10))
#q = set(range(1, 200))
q = (1, 3, 4, 7, 12)


def f(x):
    return x * 4 + 6

maths = {} #Create the first cache 

for element in q:
    if element not in maths: #Fill the first cache with the f() values for each item in the initial array.
        maths[element] = f(element)

maths_list = sorted(maths.items()) #convert to a list and sort for easy of use.

add_pairs = {} #We need a cache for all f() + f() values. 
sub_pairs = {} #We need a cahce for all f() - f() values 
results = {} #This will hold our results

for f in range(len(maths_list)): #Run through the sorted list.
    add_pairs[(maths_list[f][0], maths_list[f][0])] = maths_list[f][1] + maths_list[f][1] #Fills addition cache up with keys/values for f() + same f()

    for s in range(len(maths_list)): #runs through the rest of the combos of f() + f(). Important for keys/values to match.
        add_pairs[(maths_list[f][0], maths_list[s][0])] = maths_list[f][1] + maths_list[s][1]
    
    if f != s and s < len(maths_list): #Original list was sorted for this. This allows us to find all *positive* values for the solutions to f() - f()
        sub_pairs[(maths_list[s][0], maths_list[f][0])] = maths_list[s][1] - maths_list[f][1]

for value in add_pairs.items(): #Iterate through the addition cache
    if value[1] in sub_pairs.values(): #Looks for if the value of a add_pair cache item is the same as any sub_pair cache item.
        keys = list(sub_pairs.keys())[list(sub_pairs.values()).index(value[1])] #Stores value of paired keys

        for key in range(1, len(keys)):#Iterates through stored keys
            results[(value[0], value[1])] = ((keys[key - 1], keys[key]), sub_pairs[(keys[key-1], keys[key])]) #Loads the paired keys into the final cache.

results_list = sorted(results.items()) #Sort the results dictionary.

for result in results_list: #Cycles through the various answers.
    a = result[0][0][0] #Gives first pair
    b = result[0][0][1] #Gives second pair
    c = result[1][0][0] #Gives first pair
    d = result[1][0][1] #Gives second pair

    a_result = maths[a] #answer to f(a)
    b_result = maths[b] #answer to f(b)
    c_result = maths[c] #answer to f(c)
    d_result = maths[d] #answer to f(d)

    print(f'f({a}) + f({b}) = f({c}) - f({d}) \t {a_result} + {b_result} = {c_result} - {d_result}') #Output iterates through for loop, displaying math. Definitely tricky.
