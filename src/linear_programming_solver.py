"""
	Author: (MSc) Guilherme Mendes Marques de Oliveira
	Contact: gmmoliveira@gmail.com / guilherme_1994@yahoo.com.br
	Creation Date: May 13, 2020
	Last Updated: apr 12, 2021
	----------------------------------------------------------------------------------------
	Copyright 2020 Guilherme Mendes Marques de Oliveira
	SPDX-License-Identifier: Apache-2.0
	----------------------------------------------------------------------------------------
	This file was created using Google OR-Tools found at
	https://developers.google.com/optimization,
	all credits for the Google OR-Tools goes to Google LLC (please, note that I am NOT
	endorsed by Google LLC):

	Copyright Google LLC
	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	     http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
	----------------------------------------------------------------------------------------
	The Google OR-Tools uses, by default, the CBC (Coin-or branch and cut) solver which may
	be found at "https://github.com/coin-or/Cbc" which is distributed under the Eclipse
	Public License 1.0. Please, note that I am NOT endorsed by the developers of CBC.
	----------------------------------------------------------------------------------------
	 ********* Thank-you very much to the developers of Google OR-Tools and CBC! **********
	----------------------------------------------------------------------------------------
"""
from ortools.linear_solver import pywraplp
import numpy as np


VAR_TYPE_BINARY = 0
VAR_TYPE_INTEGER = 1
VAR_TYPE_CONTINUOUS = 2


def solver_infinity():
	'''
	output:
	------
		* returns the solver's infinity value
	'''
	return pywraplp.Solver_Infinity()


def solve_lp(C, A, lb, ub, vars_properties={}, maximization=True, method='CBC', hint=[], num_threads=1):
	'''
	This function solves a given linear programming (LP) of the following type:
			max/min 	Cx
				s.t.	lb <= Ax <= ub
						vars_properties[i][j] <= x <= vars_properties[i][j+1]
						x belongs to {binary, integer, continuous}
	intput:
	------
		* C: the objective function to minimize or maximize as a 1D numpy array;
		* A: the constraints coefficients as a 2D numpy array;
		* lb: the lower bounds for each constraint as a 1D numpy array;
		* ub: the upper bounds for each constraint as a 1D numpy array;
		* vars_properties: a dictionary keyed by indexes of decision variables which defines the properties of each var as explained below:
			* if method is 'BOP', vars_properties won't be considered;
			* if method is 'CBC':
				* "vars_properties" is a dict keyed by indexes of decision variables, mapping to 3-uples: (var_type, lower_bound, upper_bound)
				* as long as "lower_bound" is always less or equal to "upper_bound", their values are irrestricted floats
				* "var_type" may assyme 3 different values: 0 means binary, 1 means integer, 2 means continuous, refer to the constants "VAR_TYPE_BINARY", "VAR_TYPE_INTEGER", "VAR_TYPE_CONTINUOUS" in this file to use one of the supported variable types;
				* if "var_type" is set to "VAR_TYPE_BINARY", the "lower_bound" must always be 0 and the "upper_bound" must always be 1 or an exception will be thrown
				* any missing variables in vars_properties dict will be assumed to be integer ranging between [0, +infinity).
			* if method is 'CLP', vars_properties is a dict keyed by indexes of decision variables, mapping to 2-uples: (lower_bound, upper_bound);
				* as long as "lower_bound" is always less or equal than "upper_bound", their values are unrestricted floats
				* all variables are assumed to be continuous;
				* any missing variables in "vars_properties" dict will be assumed to be continuous ranging between [0, +infinity);
		* maximization: True if the LP model is to be maximized, False if it is to be minimized;
		* method: a non-casesensitive string which defines which underneath solver structure provided by Google ORTools to be used:
			* 'BOP': binary integer programming, all decision variables belongs to {0, 1} and the contents of "vars_properties" is ignored;
			* 'CBC': mixed integer programming, where variables may be binary, integer or continuous, as specified by "vars_properties";
			* 'CLP': regular linear programming, where variables are always continuous and their interval is defined by "vars_properties";
		* num_threads: the number of threads to be used on the optimization, default is 1. Note that there are platforms which doesn't support more than 1 thread;
	output:
	------
		The possible outputs are:
			* C*: the optimum objective value
			* X*: optimum solution as a 1D numpy array (in case of alternate optima this array is a single possible optimum solution)
			* status: the resulting status of the optimization, which could be: optimum, alternate optima, infeasible and unbounded
			* time: the time needed to complete the optimization task in milliseconds
			* iters: the number of iterations demanded to find the optimum solution
			* bb_nodes: the number of branch and bound nodes created for solving an integer programming model

		The actual output depends on the choosen "method", based on what they support:
			* method 'BOP' returns:
				* C*
				* X*
				* status
				* time
			* method 'CBC' returns:
				* C*
				* X*
				* status
				* time
				* iters
				* bb_nodes
			* method 'CLP' returns:
				* C*
				* X*
				* status
				* time
				* iters
	Exceptions:
	----------
		Raises an exception of type "Exception", each with it's own customized message, due to model inconsistency problems, in the following cases:
			* the number of variables (length over axis 0) in C is different than the number of variables (columns) in A;
			* the number of constraints (length over axis 0) in A, lb and ub mismatch;
			* the number of variables (keys) in "vars_properties" is greater than the number of variables (columns in A) in the model;
			* if method is 'CBC' and the size of tuples in "vars_properties" is not exactly 3;
			* if method is 'CBC' and the first element in any 3-uple in "vars_properties" is not VAR_TYPE_BINARY, VAR_TYPE_INTEGER or VAR_TYPE_CONTINUOUS;
			* if method is 'CBC' and the first element in any 3-uple in "vars_properties" is VAR_TYPE_BINARY but the lower_bound is not 0 or the upper_bound is not 1;
			* if method is 'CLP' and the size of tuples in "vars_properties" is not exactly 2;
			* if method is 'CBC' or 'CLP' and for any uple found in "vars_properties" the lower_bound is strictly greater than the upper_bound
			* independently of method, if the k-th item in lb is strictly greater than the corresponding k-th item in ub for any valid k

	'''
	if C.shape[0] != A.shape[1]:
		raise Exception('The number of variables in C and A doesn\'t match.')
	if (A.shape[0] != lb.shape[0]) or (A.shape[0] != ub.shape[0]):
		raise Exception('The number of variables in lb, ub and A doesn\'t match.')

	n = A.shape[1]
	c = A.shape[0]
	X = []

	# determine the solver method
	solver_method = None
	solver_name = ''
	if method.upper() == 'BOP':
		solver_method = pywraplp.Solver.BOP_INTEGER_PROGRAMMING
		solver_name = 'binary_integer_programming'
	elif method.upper() == 'CBC':
		if len(vars_properties.keys()) > A.shape[1]:
			raise Exception('Too many variables properties for too few decision variables in the model.')
		solver_method = pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
		solver_name = 'mixed_integer_programming'
	elif method.upper() == 'CLP':
		if len(vars_properties.keys()) > A.shape[1]:
			raise Exception('Too many variables properties for too few decision variables in the model.')
		solver_method = pywraplp.Solver.CLP_LINEAR_PROGRAMMING
		solver_name = 'continuous_linear_programming'
	else:
		raise Exception('Unsupported method:', method)
	# creates the solver instance
	solver = pywraplp.Solver(solver_name, solver_method)
	infinity = solver.infinity()

	# sets the number of threads (currently doesn't works for some platforms like windows)
	if num_threads <= 0:
		num_threads = 1
	else:
		num_threads = int(num_threads)
	solver.SetNumThreads(num_theads=num_threads)

	# creates the variables, setting all their properties
	if method.upper() == 'BOP':
		for k in range(0, n):
			variable = solver.BoolVar('x[%i]' % k)
			X.append(variable)

	elif method.upper() == 'CBC':
		for k in range(0, n):
			kth_type = 1
			kth_lb = 0.0
			kth_ub = infinity
			if k in vars_properties:
				try:
					kth_type, kth_lb, kth_ub = vars_properties[k]
				except ValueError:
					raise Exception('The "CBC: method expected tuples of size exactly 3 in the "vars_properties" dictionary.')
			if kth_lb > kth_ub:
				raise Exception('Inconsistent '+str(k)+'-th variable bounds: the lower bound "'+str(kth_lb)+'" is greater than the upper bound "'+str(kth_ub)+'".')

			variable = None
			if kth_type == 0:
				if kth_lb != 0 or kth_ub != 1:
					raise Exception('Binary variables must always have their lower bound set to 0 and their upper bound set to 1.')
				variable = solver.BoolVar('x[%i]' % k)
			elif kth_type == 1:
				variable = solver.IntVar(kth_lb, kth_ub, 'x[%i]' % k)
			elif kth_type == 2:
				variable = solver.Var(kth_lb, kth_ub, False,'x[%i]' % k)
			else:
				raise Exception('Unknown variable type in vars_properties:', kth_type)
			X.append(variable)

	elif method.upper() == 'CLP':
		for k in range(0, n):
			kth_lb = 0.0
			kth_ub = infinity
			if k in vars_properties:
				try:
					kth_lb, kth_ub = vars_properties[k]
				except ValueError:
					raise Exception('The "CLP: method expected tuples of size exactly 2 in the "vars_properties" dictionary.')
			if kth_lb > kth_ub:
				raise Exception('Inconsistent '+str(k)+'-th variable bounds: the lower bound "'+str(kth_lb)+'" is greater than the upper bound "'+str(kth_ub)+'".')

			variable = solver.Var(kth_lb, kth_ub, False,'x[%i]' % k)
			X.append(variable)

	# creates the constraints, setting all their properties
	for k in range(0, c):
		kth_lb = lb.item(k)
		kth_ub = ub.item(k)
		if kth_lb > kth_ub:
			raise Exception('Inconsistent '+str(k)+'-th constraint bounds: the lower bound "'+str(kth_lb)+'" is greater than the upper bound "'+str(kth_ub)+'".')
		
		constraint = solver.RowConstraint(kth_lb, kth_ub, 'constraint[%i]' % k)
		for v in range(0, n):
			constraint.SetCoefficient(X[v], A.item(k, v))

	# sets the LP objective
	objective = solver.Objective()
	for k in range(n):
		objective.SetCoefficient(X[k], C.item(k))
	if maximization:
		objective.SetMaximization()
	else:
		objective.SetMinimization()

	# sets a hint for a initial basic feasible solution
	if len(hint) > 0:
		if len(hint) != n:
			raise Exception('The hint list has an inconsistent number of elements:', len(hint))
		solver.SetHint(solver.variables(), hint)

	# attempts to solve the problem
	status = solver.Solve()
	if method.upper() == 'BOP':
		return solver.Objective().Value(), np.array([variable.solution_value() for variable in X]), status, solver.wall_time()
	elif method.upper() == 'CBC':
		return solver.Objective().Value(), np.array([variable.solution_value() for variable in X]), status, solver.wall_time(), solver.iterations(), solver.nodes()
	elif method.upper() == 'CLP':
		return solver.Objective().Value(), np.array([variable.solution_value() for variable in X]), status, solver.wall_time(), solver.iterations()

