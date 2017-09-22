# BostonHack-Project
* Provide recommendation for team formation, given tasks data, people profiles, and team constraints
* A write-up[https://www.overleaf.com/read/nngzfjvyxdyv] of the algorithm is included(update needed)

### Prerequisites

Python 3, pulp

### Installing

ommited

### Running a test
This repo consists of three notebook files, which shall be run in order:
1. **test_data_generation**
  (result saved in "outfile", as generated test data)
2. **linear_programing_randomize**
  (need "outfile" and "all_cons" as input, results saved in "LPRD")
3. **constraint_Kmeans**

### Todo lists
* new test data for (3), add error measurement, or use sample data from fiona
* change distance function
* consider prefixed group without projects

## Authors
* **Marco Cai** 
## Acknowledgments
* constraint Kmeans: http://www.cs.utexas.edu/~ml/papers/semi-icml-02.pdf
* Linear Programing: https://pdfs.semanticscholar.org/b82e/1986a639efb69c379e87450aa5decfac5e79.pdf
