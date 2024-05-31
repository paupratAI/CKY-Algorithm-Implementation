# CKY Algorithm Implementation

This project implements the CKY (Cocke-Kasami-Younger) algorithm for verifying strings against Context-Free Grammars (CFG) and Probabilistic Context-Free Grammars (PCFG).

## Files

- `main.py`: Main script to run the program.
- `cfg.py`: Defines the CFG class.
- `Pcfg.py`: Defines the PCFG class.
- `transform_into_cnf.py`: Contains the CNF class for converting CFG to CNF.

## Input Files

- `input.txt`: Contains test sets for CFGs.
- `input_PCKY.txt`: Contains test sets for PCFGs.

## Output Files

- `output.txt`: Results for CFGs.
- `output_PCKY.txt`: Results for PCFGs.

## Usage

1. Run `main.py`.

2. Answer the interactive questions:
    - Choose whether to use a PCFG. 
    - Choose whether to print the CKY table in the output file.

3. Results are saved to `output.txt` or `output_PCKY.txt` based on your choices.
