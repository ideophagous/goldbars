Developed by: Mounir AFIFI for a job interview at Episteme (London, UK)
Python version: 2.7.12

Brief Summary and Motivation:

The problem can be summarized as follows: a bank wants to transport a number of gold bars from their current location to Sheffield. They have to pay a tax upon entry to every town or village crossed, but not upon leaving. The tax at villages is one gold bar regardless of the amount transported, whereas at towns the tax is evaluated as the rounded up value of the twentieth of the amount at the entry. Given a fixed number of gold bars that must reach Sheffield, how much should be carried to begin with while paying the least amount of tax?
The solution of the problem therefore consists in minimizing the cost by choosing the minimal path from source to destination. The obvious method would be to check every single path, calculate the cost, and choose the smallest value. We can improve upon this idea by understanding the problem more deeply, from a mathematical standpoint, and finding some formulas or heuristic rules to minimize the search set.

Assumptions:

In order to understand our problem, we have to explicitly lay down all the basic assumptions about its variables and aspects. Some of these assumptions were explicit in the problem description, and other ones could be deduced from its wording.
1.	The number of villages and towns each cannot exceed 26, since they are represented only as Latin alphabet letters. In general, this may not necessarily be true, but considering our problem specifications, it is.
2.	A map cannot be empty or contain a single node (village or town). This would be a trivial problem of no practical importance.
3.	A road must link two distinct nodes (villages or towns).
4.	The number of gold bars cannot be equal to zero, since the bank would have no interest in transporting 0 gold bars to another location, and paying taxes for it!
5.	The number of gold bars cannot exceed 1000.
6.	The problem must always have a solution, that is, there must always be a path from source to destination.
7.	A path must be non-cyclic (source and destination are not  the same node) and non-repetitive (does not pass through the same node twice), otherwise it would be by default a wasteful path.

Files:
sheffield.py : main program
sheffield_test.py : unit test program, still under development
delivery.txt : file containing test cases
mathematics of sheffield.pdf : mathematical formulation of the problem
docs : contains Pycco-generated documentation (html+css)
