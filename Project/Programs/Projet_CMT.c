//----------------------------------------------------------------------------------------------------------------------------------------------------------
// IMPORT MODULS //
//----------------------------------------------------------------------------------------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//----------------------------------------------------------------------------------------------------------------------------------------------------------
// INPUTS OF THE PROGRAM WHICH CAN BE CHANGED DEPENDING ON THE LOCATION CHOSEN //
//----------------------------------------------------------------------------------------------------------------------------------------------------------

// Le Säntis documentation: https://saentisbahn.ch/fr/vivre/le-telepherique/techniques/

double g = 9.81;                  // Gravitationnal constant [m^2/s]
double rho_eau = 1000.0;          // Water density [kg/m^3]
double average_human_mass = 74.3; // Average mass of a human being [kg]            
double denivelation = 1122.48;    // Denivelation of the telecabin [m] (height between the turbine and the bassin)
double nt = 0.8;                  // Yield of the turbine [-]
double nf = 0.8;                  // Yield of the pipe due to friction [-]
double np = 0.85;                 // Yield of the pannels [-]
double pannel_power = 400.0;      // Power of one 1m^2 solar pannel [W]            
double mass_cabin = 9090.0;       // Mass of the empty cabin [kg]
int passengers = 70;              // Average number of passengers [-]
double nc = 0.7;                  // Yield of telecabin's engine [-]                
int departures = 16;              // Number of departures per day [-]

//----------------------------------------------------------------------------------------------------------------------------------------------------------
// FUNCTIONS //
//----------------------------------------------------------------------------------------------------------------------------------------------------------

// To find the size of the retention bassin and the number of solar pannels we use the Energie of the cabin per day 
// We then calculate the average precipitation and daylight using the Python list
// We use the energy equations for each list to find: the bassin's minimum area and the minimum number of solar pannels needed
// We use a 50%-50% ratio per day for the two energies

// Telecabine's power

double telecabine_consumption_day(double mass_empty_cabin, int persons, double denivelation, double engine_yield, int nbr_departures_day){
    // Energy for one ascent with the average number of passengers
    // Use the fact that the empty cabin coming back down compensates the mass of the empty cabin going up
    // We then assume that only the mass of the persons and the frictions affect the energy demand of the accent
    double Energy_consumed_per_day = 0;
    double Energy_one_ascent = ((mass_empty_cabin + persons * average_human_mass) - mass_empty_cabin)* g * denivelation / engine_yield;
    // Divide by 3'600'000 to get kWh
    Energy_consumed_per_day = Energy_one_ascent * nbr_departures_day / 3600000;

    return Energy_consumed_per_day;
}

// Main fucntion that returns the energy needed for the cabin in one day
int main(){
    telecabine_consumption_day(mass_cabin, passengers, denivelation, nc, departures);
    
    return 0;
}

// Minimum number of pannels 

int Pannels(float *Daylight_day, int Daylight_day_size, double Energy_consumed_per_day){
    // Loop on Daylight list to calculate the average daylight in the year
    double pannels = 0.0;
    double sum_daylight = 0.0;
    
    for (int i = 0; i < Daylight_day_size; i++){
        sum_daylight += Daylight_day[i];
    }
    // Calculate the average daylight 
    double average_daylight = sum_daylight / Daylight_day_size;
    // Calculate the the minimum number of pannels
    // Multiply by 0.001 to get kW instead of W for the pannels' power
    pannels = (Energy_consumed_per_day * 0.5) / (pannel_power * 0.001 * np * average_daylight);

    return pannels;   
}


// Minimum area of the retention bassin

double Area( float *Precipitation_day, int Precipitation_day_size, double Energy_consumed_per_day){
    // Loop on Precipitation list to calculate the average precipitation in the year
    double sum_precipitation = 0.0;
    double area_bassin = 0.0;
    for (int day = 0; day < Precipitation_day_size; day++){
        sum_precipitation += Precipitation_day[day];
    }
    // Calculate the average precipitation
    double average_precipitation = sum_precipitation / Precipitation_day_size;
    // Minimum area of the bassin, using a height 10 times greater than the average precipitation, so there is no risk of overflow 
    area_bassin = (Energy_consumed_per_day * 0.5) / ((average_precipitation * 0.001) * rho_eau * g * nf * nt * denivelation /3600000);

    return area_bassin;

}

// Energy of the retention bassin

void Energy_Dam(float *Precipitation_day, int Precipitation_day_size, double area_bassin){
    // Loop on each index of the Python list created from the file "somme précipitations / jour.txt"
    for (int i = 0; i < Precipitation_day_size; i++){
        // The 0.001 multiplication transforms the precipitation in mm to m
        // The 3.6 * 10^6 division tranforms J into kWh
        Precipitation_day[i] = (Precipitation_day[i] * 0.001) * area_bassin * rho_eau * denivelation * g * nf * nt / 3600000; 
    }    
}

// Solar pannels' Energy

void Solar_Energy(float *Daylight_day, int Daylight_day_size, double pannels){
    // Loop on each index of the Python list created from the file "somme heures ensoleillement / jour.txt"
    for (int i = 0; i < Daylight_day_size; i++){
        // The 0.001 multiplication transforms W into kW for the pannel's power
        Daylight_day[i] = Daylight_day[i] * pannel_power * np * pannels * 0.001;  
    }      
}





