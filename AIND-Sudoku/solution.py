assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
	
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[r+c for r,c in zip(rows,cols)],[r+c for r,c in zip(rows,cols[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # Iterate over squares
    for unit in unitlist:
        # List of unsolved boxes.
        unsolved = [box for box in unit if len(values[box]) > 1]
        if len(unsolved) > 2:
            twins = []
            for box1,box2 in [(s,t) for s in unsolved if len(values[s]) == 2 for t in unsolved if len(values[t]) == 2]:
                if ((values[box1] == values[box2]) & (box1 != box2) & ((box1,box2) not in twins) & ((box2,box1) not in twins)):
                    twins.append((box1,box2))
                    unsolved.remove(box1)
                    unsolved.remove(box2)
            # Once twins is filled with the tuples of twins it's time to extract de values
            twin_values = []
            for pair in twins:
                twin_values.append(values[pair[0]])
            for box in unsolved:
                for val in twin_values:
                    for num in val:
                        assign_value(values, box, values[box].replace(num,''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Return a dictionary with both list zipped
    return  dict(zip(list(boxes),['123456789' if c ==  '.' else c for c in list(grid)])) 

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    # Find the solved boxes ( only 1 value)
    for key in values.keys():
        if( len(values[key]) == 1 ):
            # Iterate over its peers removing the value
            for peer in peers[key]:
                assign_value(values, peer, values[peer].replace(values[key], ''))
    return values 

def only_choice(values):
    # Iterate over units
    for unit in unitlist:
        # For each possible number, create a list with the boxes which contain it.
        for i in '123456789':
            lista_i = []
            for elem in unit:
                if i in values[elem]:
                    lista_i.append(elem)
            # If the list is equal to 1 then is a unique value
            if len(lista_i) == 1:
                assign_value(values, lista_i[0], i)

    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Eliminate
        values = eliminate(values)
        # Only_choice
        values = only_choice(values)
        # Naked_Twins
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[i]) == 1 for i in boxes):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    lista = [(e,values[e]) for e in values.keys() if len(values[e]) > 1]
    l = sorted(lista,key=lambda x: len(x[1]))[0]
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for i in l[1]:
        values2 = values.copy()
        values2[l[0]] = i
        # If you're stuck, see the solution.py tab!
        values3 = search(values2)
        if values3:
            return values3

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')