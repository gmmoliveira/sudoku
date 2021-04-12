# sudoku
Solving a n-sudoku using a Mixed Integer Programming formulation


<h2>src/nsudoku.py</h2>
<p align="justify">
This script implements a method to solve (and handle) a N-size sudoku using
Linear Programming (LP), specifically by means of Mixed Integer Programming
(MIP). All MIP variables have the format X<sub>ijk</sub> which means wether cell at position (i, j) in the sudoku table
should be assigned number (k+1) or not. They may assume only integer binary values 
X<sub>ijk</sub> &#8712; {0, 1} &#8704; i, j, k &#8712; {0, N-1} and i, j, k &#8712; &#8469;, where the sudoku
table is a N by N grid. Further, the MIP constraints are created as follows:
</p>

Rows constraints:

<p align="center">
	<img src="documentation/resources/sudoku_row_constraint.png" alt="Rows constraints" width="408" height="82">
</p>

Columns constraints:

<p align="center">
	<img src="documentation/resources/sudoku_col_constraint.png" alt="Columns constraints" width="408" height="82">
</p>

<p align="justify">
Boxes constraints, where (lowercase) n and m refer to the boxes which may be indexed in each dimension of rows and columns of the sudoku table, furthermore, in this work, the sudoku version implemented always defines exactly N boxes, evenly distributed without overlapping accross the sudoku table (this means n=N<sup>1/2</sup> and m=N<sup>1/2</sup>):
</p>

<p align="center">
	<img src="documentation/resources/sudoku_block_constraint.png" alt="boxes constraints" width="603" height="141">
</p>
Uniqueness constraints (single number assigned per sudoku cell):

<p align="center">
	<img src="documentation/resources/sudoku_uniqueness_constraint.png" alt="Uniqueness constraints" width="408" height="82">
</p>

Prespecified cell values constraints:

<p align="center">
	<img src="documentation/resources/sudoku_nonempty_cells.png" alt="Prespecified cell constraints">
</p>

<p align="justify">
Since all constraints in the MIP model are of equality type, rather than inequality, maximizing
or minimizing the objective function, defined as an array of 1s, yields the exact same optimum solution.
</p>

The following functions are implemented in the object:
<table><tr><td><ul>
	<li>A class '<b>Sudoku</b>', implementing the following:</li>
	<ul>
		<li><b>linear_programming_model</b>: generates a valid linear programming (LP)
			model for the sudoku represented by this object;</li>
		<li><b>linear_programming_solve</b>: solves the generated linear programming model;</li>
		<li><b>random</b>: generates a new n by n sudoku with a few random entries
			already filled (as would be a regular sudoku challenge be);</li>
		<li><b>get_puzzle_state</b>: returns a 2D NumPy array representing the sudoku in
			it's current state;</li>
		<li><b>_lpsolution2sudoku</b>: translantes the binary LP solution array to the
			sudoku table;</li>
	</ul>
</ul></td></tr></table>
