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
