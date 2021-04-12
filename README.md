# sudoku
Solving a n-sudoku using a Mixed Integer Programming formulation


Implements a class <code class="inline_code">Sudoku</code>, with the following methods:
<ul>
<li>
<code class="inline_code">Sudoku.__init__(self, sudoku=None, n=9)</code>
:
Builds an object which represents a <code class="inline_code">n-sudoku</code>.
	<ul>
		<li>
			<code class="inline_code">sudoku</code>:
			a sudoku state, as a 2D numpy array, to be used
			as the initial state for this object. Defaults to None,
			where a random sudoku initial state will get created,
			it's going to start with a few cells already filled with
			values, like a real sudoku game would;
		</li>
		<li>
			<code class="inline_code">n</code>:
			size of the n-sudoku in a single dimension, a sudoku of
			dimensions <code class="inline_code">n</code>
			by
			<code class="inline_code">n</code>
			gets created;
		</li>
	</ul>
	Raises an Exception if <code class="inline_code">&#x221A;n</code> isn't an integer;

</li>
<li>
<code class="inline_code">Sudoku.linear_programming_model(self)</code>
: generates a valid linear programming (LP) model for the sudoku represented by this object;
</li>
<li>
<code class="inline_code">Sudoku.linear_programming_solve(self)</code>
: solves the generated linear programming model;
</li>
<li>
<code class="inline_code">Sudoku.random(self)</code>
: generates a new n by n sudoku with a few random entries already filled
	(as would be a regular sudoku challenge be), the generated states
	might be biassed towards
	<code class="inline_code">alternate optima</code>
	sudoku scenarios;
</li>
<li>
<code class="inline_code">Sudoku.get_puzzle_state(self)</code>:
	returns a 2D NumPy array representing the sudoku in it's current state;
</li>
<li>
<code class="inline_code">Sudoku._lpsolution2sudoku(self)</code>:
	decodes the LP solution array
	<code class="inline_code">X*</code>
	into a valid sudoku state;
</li>
</ul>

<br>
<hr>
Executing the "src/sudoku.py" file outputs:
<br>

<pre><code>
The starting 3-Sudoku state:

[[0 0 9 0 0 0 0 0 0]
 [7 0 0 5 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 9 1 0 0]
 [3 0 0 0 0 6 4 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 2]]

A solved 3-Sudoku state:
[[4 1 9 8 2 3 5 6 7]
 [7 2 3 5 6 1 8 4 9]
 [8 5 6 9 4 7 2 3 1]
 [2 6 4 3 8 9 1 7 5]
 [3 7 5 2 1 6 4 9 8]
 [1 9 8 4 7 5 6 2 3]
 [5 4 1 7 3 2 9 8 6]
 [6 3 2 1 9 8 7 5 4]
 [9 8 7 6 5 4 3 1 2]]
time spent on the optimization (in milisecs) =  220

<hr>

The starting 4-Sudoku state:
[[ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0 11  0  0  5  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0 14  1  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  2  0  7  1  0  0  0  0  0]
 [ 2  0  0  0  0  0  0  0 16  0  0  0  0  0  0  9]
 [ 0  0  0  0  0  0  0  0  4  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]]

A solved 4-Sudoku state:
[[13  5 11  8  1  9  7 14  2  4 12  3  6 10 16 15]
 [ 1  2  7 16 11  4  3  5  6 10  8 15  9 12 13 14]
 [ 4  9  3 10  6  2 12 15  1 14 13 16 11  5  7  8]
 [15  6 12 14 10  8 13 16 11  5  7  9  1  2  4  3]
 [ 6  4  8  7  3 14  1 11  5  2  9 10 15 13 12 16]
 [10  1 16  3  5  6  9  4 13 12 15  8  2 14 11  7]
 [ 5 12  9 11 16 13 15  2  3  7  1 14 10  6  8  4]
 [ 2 14 13 15  7 12  8 10 16  6  4 11  5  1  3  9]
 [ 3 10  1  2  9  5  6  8  4 13 11  7 14 16 15 12]
 [ 7  8  5  6  2  1  4  3 15 16 14 12 13  9 10 11]
 [11 13  4  9 14 15 16 12 10  1  3  2  7  8  5  6]
 [14 16 15 12 13 10 11  7  8  9  5  6  3  4  1  2]
 [ 9  3  2  1  8  7  5  6 12 11 10  4 16 15 14 13]
 [ 8  7  6  5  4  3  2  1 14 15 16 13 12 11  9 10]
 [12 11 10  4 15 16 14 13  9  3  2  1  8  7  6  5]
 [16 15 14 13 12 11 10  9  7  8  6  5  4  3  2  1]]
time spent on the optimization (in milisecs) =  3147

Process finished with exit code 0

</code>
