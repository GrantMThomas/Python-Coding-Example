
#PROBLEM DESCRIPTION:

# A crossword puzzle is a grid with blank slots, starting at some initial
# (x, y) and going either across or down, for some length of squares. The
# blank slots need to be filled with words from a vocabulary, where one
# character goes into each square. The blank slots may overlap requiring
# that the words in each slot share the same character at that point.

# Given a vocabulary as a list of strings,

# ```
# vocab = ['word', 'another', 'longer', ...]
# ```

# and a list of blank slots,

# ```
# ACROSS = 0
# DOWN = 1
# blanks = [(start_x, start_y, direction, length), ...]
# ```

# Write a function that returns any solution to the crossword, or `None`
# if no solution exists. The solution should be a list of
# `[(start_x, start_y, direction, word_from_vocab_that_goes_here), ...]`.


# Example outputs are below.

# ```
# solve_crossword(vocab=['the', 'begin'],
#   blanks=[
#     (0, 1, ACROSS, 3),
#     (2, 0, DOWN, 5)
#   ]) == [
#     (0, 1, ACROSS, 'the'),
#     (2, 0, DOWN, 'begin')
#   ]
#
# solve_crossword(vocab=['next', 'time', 'expect', 'electric'],
#   blanks=[
#     (0, 0, ACROSS, 4),
#     (1, 0, DOWN, 6),
#     (3, 0, DOWN, 4),
#     (1, 3, ACROSS, 8)
#   ]) == [
#     (0, 0, ACROSS, 'next'),
#     (1, 0, DOWN, 'expect'),
#     (3, 0, DOWN, 'time'),
#     (1, 3, ACROSS, 'electric')
#   ]
#
# solve_crossword(vocab=['one', 'two', 'three'],
#   blanks=[
#     (0, 0, ACROSS, 4)
#   ]) == None

# SOLUTION: 

import copy

# Custom printing function used for the whole board. I used for debugging
def out(crossword):
    for i in range(len(crossword)):
        print(crossword[i])
    print()
def crossword(dictionary,blanks):
    height = 1
    width = 1
    # This for loop finds the width and height of the crossword puzzle
    # so it can be represented as a 2D matrix
    for i in range(len(blanks)):
        # Across
        if(blanks[i][2] == 0):
            if(blanks[i][0] + blanks[i][3] > width):
                width = blanks[i][0] + blanks[i][3]
        # Down
        else:
            if(blanks[i][1] + blanks[i][3] > height):
                height = blanks[i][1] + blanks[i][3]
    # Allocating the size of the 2D matrix
    array = []
    for i in range(height):
        array.append([])
        for j in range(width):
            array[i].append(0)
    
    # Now placing 1's in every spot of the 2D matrix in order to
    # represent an open square
    for i in range(len(blanks)):
        # Across
        if(blanks[i][2] == 0):
            for j in range(blanks[i][3]):
                array[blanks[i][1]][blanks[i][0] + j] = 1
        else:
            for j in range(blanks[i][3]):
                array[blanks[i][1] + j][blanks[i][0]] = 1
    
    
    
    answer = []
    # All work is done in helper function, recursively solving problem
    result = helper(dictionary, array, blanks,answer)

    if(len(result) == 0):
        return "None"
    
    return result


def helper(dictionary, array, blanks,answers):
    # Base case, if length is 0 every word has been placed

    if(len(dictionary) == 0):
        return answers
    # Main logic: for every word in the dictionary, check 
    # if there are blanks that match its length. If there are,
    # recursively call a board where the word fills that spot
    for i in range(len(dictionary)):
        for j in range(len(blanks)):
            if(len(dictionary[i]) == blanks[j][3]):
                #Across
                if(blanks[j][2] == 0):
                    # Deep copying so we can have multiple variations of the array
                    cop = copy.deepcopy(array)
                    dx = copy.deepcopy(dictionary)
                    bl = copy.deepcopy(blanks)
                    ans = copy.deepcopy(answers)
                    # If statement checks if the current square is either a 1 (empty space)
                    # or the appropriate letter
                    if(cop[blanks[j][1]][blanks[j][0]] == 1 or cop[blanks[j][1]][blanks[j][0]] == dictionary[i][0]):
                        valid = True 
                        for e in range(blanks[j][0], blanks[j][0] + blanks[j][3]):
                            if(cop[blanks[j][1]][e] == 1 or cop[blanks[j][1]][e] == dictionary[i][e - blanks[j][0]]):
                                cop[blanks[j][1]][e] = dictionary[i][e - blanks[j][0]]
                            # If neither 1 or appropriate letter, this is not a valid board
                            else:
                                valid = False
                        if(valid):
                            dx.pop(i)
                            bl.pop(j)
                            ans.append((blanks[j][0],blanks[j][1],0,dictionary[i]))
                            
                            return helper(dx,cop,bl,ans)

                # Exact same logic as above, just moves down instead of across
                else:
                    cop = copy.deepcopy(array)
                    dx = copy.deepcopy(dictionary)
                    bl = copy.deepcopy(blanks)
                    ans = copy.deepcopy(answers)
                    if(cop[blanks[j][1]][blanks[j][0]] == 1 or cop[blanks[j][1]][blanks[j][0]] == dictionary[i][0]):
                        valid = True
                        for e in range(blanks[j][1], blanks[j][1] + blanks[j][3]):
                            if(cop[e][blanks[j][0]] == 1 or cop[e][blanks[j][0]] == dictionary[i][e - blanks[j][1]]):
                                cop[e][blanks[j][0]] = dictionary[i][e - blanks[j][1]]
                            else:
                                valid = False
                        if(valid):
                            dx.pop(i)
                            bl.pop(j)
                            ans.append((blanks[j][0],blanks[j][1],1,dictionary[i]))
                            
                            return helper(dx,cop,bl,ans)
                                              
    return []


# TEST CASES:
print(crossword(['the', 'begin'],[(0,1,0,3), (2,0,1,5)])) #valid
print(crossword(['tht', 'begin'],[(0,1,0,3), (2,0,1,5)])) #none
print(crossword(['next','time','expect','electric'], [(0,0,0,4),(1,0,1,6),(3,0,1,4),(1,3,0,8)])) #valid
print(crossword(['one', 'two', 'three'], [(0,0,0,4)])) #none
print(crossword(['sheep','ant','arm','table','sugar','pencil','tale'],[(0,0,0,5),(4,0,1,6),(3,2,0,3),(5,2,1,4),(0,3,0,3),(1,5,0,5),(0,0,1,5)])) #valid
              