NOTE : Detailed description and documentaiton of the script is still pending... 

BRIEF INTRO OF SCRIPTS :
SolveNerdle - Main script for generating equations such that ANSWER script is guessed in <=6 tries.  
TestNerdle - It is used to test and generate stats on number of tries for solving all possible equations of length 8

NERDLE RELATED INFO
Website : https://nerdlegame.com/
 
Guess the NERDLE in 6 tries. After each guess, the color of the tiles will change to show how close your guess was to the solution.
Rules:
* Each guess is a calculation.
* You can use 0 1 2 3 4 5 6 7 8 9 + - * / or =.
* It must contain one “=”.
* It must only have a number to the right of the “=”, not another calculation. 
  ----> Also means no negative numbers as output
* Standard order of operations applies, so calculate * and / before + and - eg. 3+2*5=13 not 25!
  ----> Currently the submit / feedback generation logic does not handle this logic. Hence there are still equation which are taking 7 and 8 iterations to solve
* If the answer we're looking for is 10+20=30, then we will accept 20+10=30 too (unless you turn off 'commutative answers' in settings).
* If your guess includes, say, two 1s but the answer has only one, you will get one color tile and one black.
* Tiles will only go green if the number is in the correct position or when a full guess is rearranged as a winning commutative answer.

