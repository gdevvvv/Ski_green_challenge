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
- In the terminal are printed: "Energy_Cabin_per_day_rounded", "Energy_cable_car_2023", "solar" (number of solar pannels) and "area" (area of the square retention bassin.

### Implementation details

Overview:
- The simulation is handled by C. The C program is compiled to a shared library, which is called by Python via the `ctypes` module. All the variables used to describe the specifics of the cable car systme is implemented in C.
- Python handles most of the I/O, which includes reading sensor information (files from the IDAWEB plateform) and formatting the output of the single point simulation.
- For the grid simulation, the C program directly writes each simulation result to two python lists (lists of energies) designated by the calling Python script.

Structure. In the directory "*src/*":
- "*Projet_CMT.py*":
  - reads in "*Data/somme précipitations / jour.txt*" and "*Data/somme heures ensoleillement / jour.txt*" and executes the C code.
  - reads in the generated output ("List_Dam_Energies_rounded", "List_Solar_Energie_rounded") and makes four plots.

The C program is compiled automatically via the Python line: "os.system("gcc -shared -o libProjet_CMT.so -fPIC ./Programs/Projet_CMT.c")". The C program then changes the python lists and return a copy of each list with changed values. 

## Instructions

To reproduce results in the report, two steps should be followed:

1. Open the whole folder in VSCode.
2. Run the Python program.

## Requirements

Versions of Python and C used are as follows. 
```
$ python --version
Python 3.11.7

$ gcc --version
gcc (Clang 14.0.6 on darwin) 

```

## Credits

The code was written by Sacha Meyer (sacha.meyer@epfl.ch) and Gaspard Devaux (gaspard.devaux@epfl.ch)

