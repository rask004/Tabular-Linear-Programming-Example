# Tabular-Linear-Programming-Example
An Example, for Students, of solving a Linear Programming problem, using tabular data.

## Problem Statement

You are given a number of workers, and a number of jobs to complete.

The number of workers should match the number of jobs, but might not.

Each worker can only work on one, and only one job. Each job can have one and only one worker.

You have been given a table (see file: job_costs.csv) showing how much it would cost for each worker to be given a specific job.

Find a combination of workers and jobs which gives the lowest total cost.

## Example

Example output could be:

  Worker 1 --> job 2 , cost = 5
  Worker 2 --> job 4 , cost = 7
  Worker 3 --> job 3 , cost = 4
  Worker 4 --> job 1 , cost = 5

  Total Cost = 21

Each worker has one unique job, and each job is given to one worker.
Note that there might be jobs or workers not assigned because the count of workers and number of jobs are not the same.

Another example could be:

  Worker 1 --> job 3 , cost = 6
  Worker 2 --> job 4 , cost = 7
  Worker 3 --> job 1 , cost = 3
  Worker 4 --> job 2 , cost = 2

  Total Cost = 18

If both examples use the same costs table, then the second example is better, because the cost is lower.

## Solution Code

### Files

.devcontainer		only used if project is installed in a docker environment.
requirements.txt	required packages for program to run.
job_costs.csv		CSV file, table showing costs for each worker and job combo.
config.py		Constants and fixed variables, used by the main script.
more_networkx.py	A couple of specialized functions for working with network.
main.py			Main script.

### Description

A customised object is used to store the worker names, job names, and associate costs with each.

The CSV file is loaded and converted into a custom object as described just above.

NetworkX is used to produce an undirected tree-like graph. Nodes are a starting node, and worker and job combinations with cumulative 
cost data and additional data to make easier to find some properties such as depth. Edges connect nodes such that a traversal
(path from the start node to an end node) contains only nodes with unique job and worker combos, no job or worker is mentioned more 
than once. End nodes have only one edge, the highest depth, and the total cost of a given combination.

The end node with the lowest total cost is found, the reverse traversal path from this node to start is found, and the worker and job
combinations are pulled from the node data. Finally the results are shown to screen in a human friendly format.

