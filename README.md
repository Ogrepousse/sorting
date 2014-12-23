README

Program take in argument the number of point to read

Path of the file can be set line 26 in main.py in second argument for the function read_header,
by default the path is '../files/ALL.filtered'

The result are written in a file name output at the root of the program, this can be changed in the initial parameter of the environment.

In libpy/environment/class_env.py:
	The constructor set several constant for the algorithm
	You can change the length of block and mega block but other constant should stay the same

	The function set_overlap charge the overlap matrix from extern file, the path of the file must be set in argument in the function get_overlap. There are four overlap, currently only one is charged and used in the code. To use the four overlap line must be decommented in function set_overlap and del_overlap, and in the file libpy/dot_prod/scal_prod.py in the function maj_scalar.

In libpy/environment/env_fct.py:
	The function get_temp read the template from a matlab file, the path of the file must be set in the function
	Same thing in the function get_amp_lim which get the limit for the aij. The limits are in the same file as the template


Data file are .filtered file
Template file must be matlab file.
The overlap must be written in binary mode in file, currently the value of the overlap are on 64bits.
