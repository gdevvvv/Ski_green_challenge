# SIE ENG270 Ski_Green_Challenge

## Project Description

This program simulates how to provide energy to a cable car from green energies.

The program will:
1. Read in inputs
   - Precipitation found in "*Data/somme précipitations / jour.txt*",
   - Daylight found in "*Data/somme heures ensoleillement / jour.txt*".

2. Plot a histogram of precipitation/day ("*Plots/Histogram of precipitation per day in 2023.png*").
3. Plot a histogram of daylight/day ("*Plots/Histogram of daylight per day in 2023*").
4. Plot a histogram of energies produced/day ("*Plots/Histograms of Energies produced per day in 2023.png*").
5. Plot a graph of accumulated energies in 2023 ("*Graph of accumulated energies produced in 2023*").

## Project structure

- "*Data/*" contains input data
- "*Plots/*" contains program outputs
- "*Programs/*" contains program code (C and Python)

### Inputs and outputs

Inputs:
- "*Data/somme précipitations / jour.txt*" is a tab-delimited (three columns) file (";"-separated).
- "*Data/somme heures ensoleillement / jour.txt*" is a tab-delimited (three columns) file (";"-separated).

Outputs:
- ("*Plots/Histogram of precipitation per day in 2023.png*") is a histogram of precipitation/day [mm/day].
- ("*Plots/Histogram of daylight per day in 2023*") is a histogram of daylight/day [hours/day]
- ("*Plots/Histograms of Energies produced per day in 2023.png*") is a histogram of energies produced/day [kWh/day].
- ("*Plots/Graph of accumulated energies produced in 2023*") is a graph of accumulated energies in 2023 [kWh/day].

### Implementation details

Overview:
- The simulation is handled by C. The C program is compiled to a shared library, which is called by Python via the `ctypes` module.
- Python handles most of the I/O, which includes reading sensor information (files from the IDAWEB plateform) and formatting the output of the single point simulation.
- For the grid simulation, the C program directly writes each simulation result to two python lists (lists of energies) designated by the calling Python script.

Structure. In the directory "*src/*":
- "*simulategrid.py*":
  - imports "*mylib.py*" as a module, which wraps the compiled C library file.
  - reads in "*data/capteurs.csv*" and executes the C code.
- "*analysis.py*":
  - reads in the generated output ("*outputs/plausibilite.csv*") and makes the plot.

In each Python code, the project root directory is assigned using 

```{python}
import sys
from pathlib import Path
ROOT = Path(sys.path[0]).parent
```
`sys.path[0]` is the directory of the script or noteoobk file, and not the working directory of the shell from which the code is called. This allows the following commands to produce equivalent output. Starting in the project root directory:
```
$ python src/simulategrid.py
$ cd src && python simulategrid.py
```
This convention works for both Python scripts and Jupyter notebooks / Quarto documents, so the following two commands will also generate the same output.
```
$ quarto render docs/analysis.qmd
$ cd docs && quarto render analysis.qmd
```

## Instructions

To reproduce results in the report, two steps should be followed:

1. Build (compile) the shared library.
2. Run the program.

To compile the C code, run the following line in the terminal from the project root directory (location of this README.md file):
```{sh}
make
```
This command will create a directory called bin/ and populated it with C object files, and the compiled .so file.

To run the Python and C code, run the following line in the terminal from the project root directory:
```{sh}
bash run.sh
```
This command will run the program and generate all of the output described above.

To generate documentation for the validation, run the following command from the root directory:
```{sh}
quarto render docs/analysis.qmd --to pdf
```
This generates the file "*docs/analysis.pdf*".

## Requirements

Versions of Python and C used are as follows. Optionally, the Quarto version is also included for rendering the "*docs/analysis.qmd*" file. 
```
$ python --version
Python 3.9.18

$ gcc --version
gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0

$ quarto --version
1.3.450
```

The "*requirements.txt*" file for Python packages was generated with the command
```{sh}
conda list --export > requirements.txt
```
and deleting all but the relevant packages specifically used by this project.

## Credits

The code is adapted from the [solutions](https://sieprog.ch/#c/pollution/solutions) of sieprog.ch.

