# SCHED helper
This script is written to form an optimized pull of radio sources to observe in particular order and dwell (see NRAO SCHED manual) by VLBA. 

Worked on numpy 1.15.4, mlrose 1.2.0 libraries, python 3.7.3

To save time obsering sources it was decided to use the soulution of Salesman problem to solve this problem.

Input: list of objects in string format as 'J0143+1338'. Caution! Your sources must be seen from VLBA telescopes! 
And sould be sorded by RA.
  All coordinates to put on TSP optimizer script obtain from the name in source list.
  
Output: text file ready to copy into .key file.




