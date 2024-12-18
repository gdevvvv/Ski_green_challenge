2#----------------------------------------------------------------------------------------------------------------------------------------------------------
## IMPORT MODULS ##
#----------------------------------------------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt 
import numpy as np              
import pandas as pd             
import subprocess
import ctypes
import os
from itertools import accumulate

#----------------------------------------------------------------------------------------------------------------------------------------------------------
## OPEN THE FILES AND EXTRACT THE THIRD COLUMN ## 
#----------------------------------------------------------------------------------------------------------------------------------------------------------

## Documentation on IDAWEB (upon request): https://gate.meteoswiss.ch/idaweb/login.do;idaweb=fX2Lt4GAv1US0E5F3KBAShHCLFHWTiN4jGMAGUPbxDeiDBmYVQKp!1141412351

with open("Data/somme heures ensoleillement : jour.txt", 'r') as file1:
    # Read each line
    lines1 = file1.readlines()

with open("Data/somme précipitations : jour.txt", 'r') as file2:
    # Read each line
    lines2 = file2.readlines()

## FILE 1 ##

# Create an empty list
Daylight_day = []
# Loop on each line
for line in lines1:
    parts = line.strip().split(';')  # Split each line when ";" occurs
    if len(parts) > 2:  # Verify that the line got three columns
        # If the third column is correct
        try:
            Daylight_day.append(float(parts[2]))  # Add to the empty list and convert the value into float 

        # If the value does not exist (missing values for some days sometimes)
        except ValueError:
            # Pass if missing value
            continue

## FILE 2 ##

Precipitation_day = []
for line in lines2:
    parts = line.strip().split(';')
    if len(parts) > 2:
        try:
            Precipitation_day.append(float(parts[2]))

        except ValueError:
            #print(f"Erreur de conversion dans la ligne : {line.strip()}")
            continue

#----------------------------------------------------------------------------------------------------------------------------------------------------------
## TRANSFER THE LISTS TO THE C FUNCTIONS ##
#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Compile the C file (here: Projet_CMT.c)
os.system("gcc -shared -o libProjet_CMT.so -fPIC ./Programs/Projet_CMT.c")

# Use the ctypes library to get the C file
Projet_CMT = ctypes.CDLL('./libProjet_CMT.so')  


## DEFINE THE SIGNATURES OF ALL FIVE C FUNCTIONS ##


# Define the types of income(argtypes) and outcome(restype) variables of each function
# None means no return of the function (function "void")

# Signature of the function of the energy of the cabin per day (no income variables)
Projet_CMT.main.restype = ctypes.c_double

# Signature of the function that returns in C the minimum number of pannels needed
Projet_CMT.Pannels.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_double)
Projet_CMT.Pannels.restype = ctypes.c_double

# Signature of the function that returns the minimum squared area of the retetntion bassin
Projet_CMT.Area.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_double)
Projet_CMT.Area.restype = ctypes.c_double

# Signature of the function that that returns the list of precipitation into a list of hydraulic energies
Projet_CMT.Energy_Dam.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_double)  
Projet_CMT.Energy_Dam.restype = None 

# Signature of the function that returns the list of daylight into a list of solar energies 
Projet_CMT.Solar_Energy.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_double)
Projet_CMT.Solar_Energy.restype = None

# Get the size of each Python list
size1 = len(Precipitation_day)
size2 = len(Daylight_day)


## CONVERT PYTHON LISTS INTO C ARRAYS ##


# File 1
array_type = ctypes.c_float * size1 # Size of the array
c_array = array_type(*Precipitation_day) # Convert the list

# File 2
array_type2 = ctypes.c_float * size2
c_array2 = array_type2(*Daylight_day)


## CALL ALL FIVE FUNCTIONS ##


# Call the funtion of the energy demand for the cabin and rename it for the following C functions
Energy_Cabin_per_day = Projet_CMT.main()
# Round the result to two decimals
Energy_Cabin_per_day_rounded = round(Energy_Cabin_per_day, 2)

# Call the function of the bassin's area and rename it 
area = Projet_CMT.Area(c_array, size1, Energy_Cabin_per_day_rounded)

# Call the function of the number of pannels and rename it
solar = Projet_CMT.Pannels(c_array2, size2, Energy_Cabin_per_day_rounded)

# Call the funtion that changes the list of precipitaion 
Projet_CMT.Energy_Dam(c_array, size1, area)

# Call the function that changes the list of daylight
Projet_CMT.Solar_Energy(c_array2, size2, solar)


## CONVERT C ARRAYS BACK INTO PYTHON LISTS ##


List_Dam_Energies = list(c_array)
List_Solar_Energies = list(c_array2)

# Round the values to two decimals
List_Dam_Energies_rounded = [round(i, 2) for i in List_Dam_Energies] 
List_Solar_Energie_rounded = [round(i, 2) for i in List_Solar_Energies]


#----------------------------------------------------------------------------------------------------------------------------------------------------------
## HISTOGRAMS ##
#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Create a list of months
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
# Create a list with corresponding days in each month
month_days = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365] 

## HISTROGRAM OF DAYLIGHT PER DAY IN 2023 ##

x_size_Daylight = size2 + 1 # Lenght of x axis
days_daylight = range(1, x_size_Daylight) # Create the x axis 

# axes[i] represents the subplot at line i (here frome 0 to 2) 
plt.figure(figsize=(12,6))
plt.bar(days_daylight, Daylight_day, color = 'orange') # Create the histogram 
plt.title("Daylight per day in Le Säntis in 2023 [hours/days]", fontsize=24) # Choose the title
plt.xlabel("Days", fontsize=18) # Name of x axis
plt.ylabel("Daylight [hours]", fontsize=18) # Name of y axis
plt.xlim(0, 365) # Limit of x axis
plt.ylim(0, 24) # Limit of y axis
plt.xticks(month_days, month_labels, fontsize=14) # Steps of x axis using months
plt.yticks(range(0, 25, 4), fontsize=14) # Steps of y axis
plt.grid(axis='y', linestyle='--', alpha=0.5) # Plot a horizontal grid 
plt.tight_layout() # Adjust the margins

# Save the figure in .png format in the same folder as the data
plt.savefig("Plots/Histogram of daylight per day in 2023.png", dpi=300, bbox_inches='tight')

plt.show()


# HISTOGRAM OF RAINFALL PER DAY IN 2023 ##

x_size_precipitation = size1 + 1
days_precipitation = range(1, x_size_precipitation)

plt.figure(figsize=(12,6))
plt.bar(days_precipitation, Precipitation_day, color = 'skyblue')
plt.title("Precipitation per day in Le Säntis in 2023 [mm/day]", fontsize=24)
plt.xlabel("Days", fontsize=18)
plt.ylabel("Precipitation [mm]", fontsize=18)
plt.xlim(0, 363)
plt.ylim(0, 100)
plt.xticks(month_days, month_labels, fontsize=14)
plt.yticks(range(0, 100, 5), fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

plt.savefig("Plots/Histogram of precipitation per day in 2023.png", dpi=300, bbox_inches='tight')

plt.show()


## SOLAR AND HYDRAULIC ENERGIES PRODUCED PER DAY IN 2023 ##

List_Dam_Energies_extended = List_Dam_Energies_rounded + [0.00, 0.00] # Add missing values with 0 kWh to the precipitation list, to get the same length
x_size_Energies = size2  # Lenght x_axis 
days_energies = range(0, x_size_Energies)
x = np.arange(len(days_energies)) # Arrange the days to be aligned with the two list of energies

plt.figure(figsize=(12,6))
plt.bar(x, List_Dam_Energies_extended, label='Hydraulic Energy', color='skyblue')
plt.bar(x, List_Solar_Energie_rounded, bottom=List_Dam_Energies_extended, label='Solar Energy', color='orange')
plt.axhline(y = Energy_Cabin_per_day_rounded, color='red', linestyle='--', label=f'Energy needed for the cabin per day ({Energy_Cabin_per_day_rounded} kWh)')
plt.legend(loc='upper left') # Plot the legend outside the graph
plt.xlim(0, 365) 
plt.ylim(0, 1850)
plt.title("Hydraulic and Solar Energies produced in 2023 in Le Säntis [kWh/day]", fontsize=20, pad=14)
plt.xlabel("Days", fontsize=16)
plt.ylabel("Energy produced [kWh]", fontsize=16) 
plt.xticks(month_days, month_labels)
plt.yticks(range(0, 1850, 100))
plt.tight_layout()

plt.savefig("Plots/Histograms of Energies produced per day in 2023.png", dpi=300, bbox_inches='tight')

plt.show()


## GRAPH OF ACCUMULATED SOLAR AND HYDRAULIC ENERGIES PRODUCED IN 2023 ##

# Define the x axis
days = list(range(1, 366)) 

# Calculate the accumulated sum of each energy
Hydraulic_Energy_accumulated = list(accumulate(List_Dam_Energies_extended))
Solar_Energy_accumulated = list(accumulate(List_Solar_Energie_rounded))

plt.figure(figsize=(12, 6)) 
plt.plot(days, Hydraulic_Energy_accumulated, label="Hydraulic Energy", color="skyblue", linestyle="-", marker="")
plt.plot(days, Solar_Energy_accumulated, label="Solar Energy", color="orange", linestyle="-", marker="")
plt.title("Evolution of Hydraulic and Solar Energies produced in 2023 in Le Säntis [kWh/months]", fontsize=18, pad=14)
plt.xticks(month_days, month_labels)
plt.ylabel("Energy [kWh]", fontsize=16)
plt.xlabel("Months", fontsize=16)
plt.legend(loc="best") 
plt.grid(True, linestyle="--", alpha=0.5)  
plt.tight_layout()  

plt.savefig("Plots/Graph of accumulated energies produced in 2023.png", dpi=300, bbox_inches='tight')

plt.show()


#----------------------------------------------------------------------------------------------------------------------------------------------------------
## PRINTED OUTPUTS ##
#----------------------------------------------------------------------------------------------------------------------------------------------------------

print("The Energy requiered for the cable car to function in one day is:", Energy_Cabin_per_day_rounded, "kWh" )
Energy_cable_car_2023 = 365 * Energy_Cabin_per_day_rounded
print("Total Energy consumed by the cable car in one year:", Energy_cable_car_2023, "kWh")
print("The minimum number of pannels of 1m x 1m is:", int(solar), "pannels")
print("The minimum length of the square retention bassin is:", int(np.sqrt(area)),"m")














    
    


