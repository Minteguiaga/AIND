# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver
In this project, we will be writing code to implement two extensions of our sudoku solver. The first one will be to implement the technique called "naked twins". The second one will be to modify our existing code to solve a diagonal sudoku.

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We apply naked twins as a strategy to reduce the number of possible values, identifying a pair of boxes belonging to the same unit that have the same 2 numbers and removing them from all the unit's boxes.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Formerly we have used the units (rows, columns and squares) as groups for applying the constraints, so the easiest way to add diagonal constraint is including an additional unit. In this way the diagonal constraint will be applied all the way down in every step of the recursion.