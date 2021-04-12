'''
	Author: (MSc) Guilherme Mendes Marques de Oliveira
	Contact: gmmoliveira@gmail.com / guilherme_1994@yahoo.com.br
	Date: 07/05/2020
	---------------------------------------------------------------
	The purpose of this work is to have fun while practicing skills
	relevant to my fields of iterest: computer science and mathematics
	(specially machine learning, combinatorial optimization
	and related topics)
	---------------------------------------------------------------
'''
'''
	Copyright 2020 Guilherme Mendes Marques de Oliveira
	SPDX-License-Identifier: Apache-2.0
'''
'''
	========================================================================================
	Below, I mention the credits for the original code snippets and/or libraries used in this
	work. Please, notice that NONE of the below mentioned institution(s)/company(ies)/
	developer(s)/etc endorse my work. I simply mentioned them to givem them credit for their
	original work (from which this work was, somehow, derived from) and also to THANK them!
	Please, refer to the "NOTICE.txt" file at the root directory for more information.
	========================================================================================

	This file is built using Google ORTools, all credits goes to Google LLC for the development
	of such library.
	----------------------------------------------------------------------------------------
	This file is built using the NumPy library (https://numpy.org/index.html)
	----------------------------------------------------------------------------------------
'''
from linear_programming_solver import solve_lp, solver_infinity
import numpy as np


class Sudoku:
	"""
	Class defining nSudoku utilities to create and solve it.
	"""

	def __init__(self, sudoku=None, n=9):
		if not (n ** (1 / 2)).is_integer():
			raise Exception('[n-sudoku solver] n=' + str(n) + ' have an invalid (non-integer) square root: "' + str(
				(n ** (1 / 2))) + '".')
		self.n = n
		if sudoku is not None:
			self.sudoku = sudoku
		else:
			self.sudoku = self.random()

		self.solved = False
		self.lp_solution = None
		self.indexing_encoder = lambda i, j, k: (i * self.n + j) * self.n + k
		self.tableau = {}

	def _lpsolution2sudoku(self):
		"""
		output:
		------
			* writes to 'self.sudoku' the solution computed using
				linear programming;
		"""
		for i in range(0, self.n):
			for j in range(0, self.n):
				for k in range(0, self.n):
					if self.lp_solution.item(self.indexing_encoder(i, j, k)) != 0:
						self.sudoku.itemset(i, j, k + 1)

	def get_puzzle_state(self):
		"""
		output:
		------
			* returns a 2D NumPy array representing the sudoku table
				which holds it's current state inside this object;
		"""
		return self.sudoku

	def random(self):
		"""
		output:
		------
			* returns a 'self.n' by 'self.n' sudoku table, as a NumPy array,
				initialized with a few values (the remaining values are meant
				to be filled by means of the optimum solution given by the
				linear programming);
		"""
		sudoku = np.zeros(shape=(self.n, self.n), dtype=int)

		feasible_rows = []
		feasible_columns = []
		feasible_boxes = []
		for k in range(0, self.n):
			feasible_rows.append(set(range(1, self.n + 1)))
			feasible_columns.append(set(range(1, self.n + 1)))
			feasible_boxes.append(set(range(1, self.n + 1)))

		box_index = lambda i, j: int(i / (self.n ** (1 / 2))) * int(self.n ** (1 / 2)) + int(j / (self.n ** (1 / 2)))

		drafted_sudoku_cells = [(i, j) for i in range(0, self.n) for j in range(0, self.n)]
		np.random.shuffle(drafted_sudoku_cells)
		drafted_sudoku_cells = drafted_sudoku_cells[: np.random.randint(low=int(0.5 * self.n), high=int(1.5 * self.n))]

		for i, j in drafted_sudoku_cells:
			k = box_index(i, j)
			intersection = list(feasible_rows[i] & feasible_columns[j] & feasible_boxes[k])

			if len(intersection) > 0:
				draft_index = np.random.randint(len(intersection))
				draft = intersection[draft_index]

				sudoku.itemset(i, j, draft)

				feasible_rows[i].remove(draft)
				feasible_columns[j].remove(draft)
				feasible_boxes[k].remove(draft)

		return sudoku

	def linear_programming_model(self):
		"""
		output:
		------
			Computes a linear programming (LP) model of the format
				max Cx
		s. t.:	Ax = b
				x >= 0

			and returns:
				* a dict representing the LP tableau with the following values:
					* 'constraint_coeffs': the constraints matrix A as a 2D NumPy array
					* 'obj_coeffs': coefficients of the objective function C
					* 'upper_bounds': coefficients of the upper bounds represented by b
					* 'lower_bounds': coefficients of the lower bounds represented by b
					* 'num_vars': the number of variables (columns) in A, without
						taking any (potential) slack variables into considerations;
					* 'num_constraints': the amount of constraints, i. e., the number
						of lines in matrix A
		"""
		nonempty_values = 0
		for i in range(0, self.n ** 2):
			if self.sudoku.item(i) != 0:
				nonempty_values += 1
		# each X_ijk indicates cell ij with color k: either 0 or 1
		A = np.zeros(shape=(4 * (self.n ** 2) + nonempty_values, self.n ** 3), dtype=int)
		b = np.ones(shape=A.shape[0], dtype=int)

		constraint = 0
		# row constraints to avoid repetition of numbers
		while constraint < (self.n ** 2):
			for i in range(0, self.n):
				for k in range(0, self.n):
					for j in range(0, self.n):
						A.itemset(constraint, self.indexing_encoder(i, j, k), 1)
					constraint += 1

		# column constraints to avoid repetition of numbers
		while constraint < 2 * (self.n ** 2):
			for j in range(0, self.n):
				for k in range(0, self.n):
					for i in range(0, self.n):
						A.itemset(constraint, self.indexing_encoder(i, j, k), 1)
					constraint += 1

		# cell constraints to avoid assigning multiple numbers to a single cell
		while constraint < 3 * (self.n ** 2):
			for i in range(0, self.n):
				for j in range(0, self.n):
					for k in range(0, self.n):
						A.itemset(constraint, self.indexing_encoder(i, j, k), 1)
					constraint += 1

		sqrtn = int(self.n ** (1 / 2))  # self.n always have an integer square root
		# box constraints to avoid assigning the same numbers in a single box
		for boxcol in range(0, sqrtn):
			for boxrow in range(0, sqrtn):
				for k in range(0, self.n):
					for i in range(boxrow * sqrtn, (boxrow + 1) * sqrtn):
						for j in range(boxcol * sqrtn, (boxcol + 1) * sqrtn):
							A.itemset(constraint, self.indexing_encoder(i, j, k), 1)
					constraint += 1

		# pre assigned cell values constraint
		for i in range(0, self.n):
			for j in range(0, self.n):
				cell_value = self.sudoku.item(i, j)
				if cell_value != 0:
					A.itemset(constraint, self.indexing_encoder(i, j, cell_value - 1), 1)
					constraint += 1

		self.tableau['constraint_coeffs'] = A
		self.tableau['upper_bounds'] = b
		self.tableau['lower_bounds'] = b
		self.tableau['obj_coeffs'] = np.ones(shape=self.n ** 3, dtype=int)
		self.tableau['num_vars'] = A.shape[1]
		self.tableau['num_constraints'] = A.shape[0]

		return self.tableau.copy()

	def linear_programming_solve(self):
		"""
		output:
		------
			Uses, indirectly, the Google ORTools mixed integer programming solver:
			* the objective function C
			* the binary 1D solution numpy array (solution at this stage wasn't yet
				translated to a sudoku)
			* the status of the optimization (for instance, it could be infeasible)
			* the number of branch and bound nodes needed to find the solution
			* the time spent to find the solution, measured in milliseconds
			* the number of iterations needed to find the solution
		"""
		self.C, self.lp_solution, self.status, time_spent = solve_lp(
							C=self.tableau['obj_coeffs'],
							A=self.tableau['constraint_coeffs'],
							lb=self.tableau['lower_bounds'],
							ub=self.tableau['upper_bounds'],
							vars_properties={},
							maximization=False,
							method="BOP",
							num_threads=9,
								)
		self._lpsolution2sudoku()
		self.solved = True
		return self.C, self.lp_solution, self.status, time_spent


if __name__ == '__main__':
	'''
		a sample test case
	'''
	for k in [3, 4]:
		s = Sudoku(n=k ** 2)
		print('A starting {:d}-Sudoku state:'.format(k))
		print(s.get_puzzle_state())
		s.linear_programming_model()
		_, _, _, t = s.linear_programming_solve()
		print()
		print('The solved {:d}-Sudoku state:'.format(k))
		print(s.get_puzzle_state())
		print('time spent on the optimization (in milisecs) = ', t)
