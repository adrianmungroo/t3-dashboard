import pandas as pd
import os
import numpy as np
from enum import Enum
from scipy import interpolate

class DATACENTER_COOLING_TECH(Enum): # Facility Power / IT Power; different categories for different types of energy
    TRADITIONAL_AIR = 1.8
    ADVANCED_AIR = 1.35
    LIQUID = 1.1
    IMMERSION_COOLING = 1.025

class DATACENTER_TYPE(Enum): # Power per rack (in kW)
    AI = 60
    NETWORK = 5
    TRADITIONAL = 7.5
    ULTRA_HIGH_DENSITY = 85

def compute_BW(DB_temperature, Humidity):
    return DB_temperature * np.arctan(
			0.151977 * np.sqrt(Humidity + 8.313659)) + 0.00391838 * np.sqrt(
			Humidity ** 3) * np.arctan(0.023101 * Humidity) - np.arctan(
			Humidity - 1.676331) + np.arctan(
			DB_temperature + Humidity) - 4.686035

class DatacenterConsumptionModel:
    """
    A virtual data center generator that estimates power consumption and heat generation
    based on cooling technology, datacenter type, and external weather conditions.
    """
    def __init__(self, datacenter_name, datacenter_size, working_temperature=23.33, cooling_technology=None, datacenter_type=None, location='Atlanta', num_datacenters=1):
        self.name = datacenter_name
        self.datacenter_size = datacenter_size # Size of each individual datacenter in KW envelope
        self.num_datacenters = num_datacenters # Number of datacenters of this type
        self.location = location               # City or location where this datacenter operate
        self.working_temperature = working_temperature

        # Fixed but Modifiable:
        self.yearly_mean_temperature = 21.777524 # Modulating the PUE contribution on cooling is a yearly system.
        self.yearly_mean_humidity = 66.44765
        # Enumerators for datacenter type and cooling technology
        if isinstance(cooling_technology, DATACENTER_COOLING_TECH):
            self.cooling_technology = cooling_technology
            self.pue = cooling_technology.value    
        else:
            self.cooling_technology = None
            self.pue = None     
        if isinstance(datacenter_type, DATACENTER_TYPE):
            self.datacenter_type = datacenter_type.value
        else:
            self.datacenter_type = None

        # Load COP regressions
        base_folder = "./data"
        file_list = ["Datacenter_20_Eq.csv", "Datacenter_30_Eq.csv", "Datacenter_45_Eq.csv"]
        get_curve_interpolator = True

        self.COP_tables = self.load_COP_data(base_folder, file_list, get_curve_interpolator)


    def set_cooling_technology(self, cooling_tech):
        """
        Set the cooling technology for the datacenter.
        This will impact the estimated PUE (Power Usage Effectiveness).
        """
        if isinstance(cooling_tech, DATACENTER_COOLING_TECH):
            self.cooling_technology = cooling_tech
            self.pue = cooling_tech.value    
        else:
            self.cooling_technology = None
            self.pue = None     

    def set_datacenter_type(self, datacenter_type):
        """
        Set the type of datacenter.
        This, along with the cooling technology, will determine power consumption.
        """
        self.datacenter_type = datacenter_type

    def estimate_power_consumption(self, DB_temperature, Humidity):
        """
        Estimate the hourly power consumption of the datacenters
        based on the datacenter type, cooling technology, and external weather conditions.
        """
        # Compute Real WB Temperature using Stull formula:
        wetbulb_temperature = compute_BW(DB_temperature=DB_temperature, Humidity=Humidity)
        yearly_wetbulb_temperature = compute_BW(DB_temperature=self.yearly_mean_temperature, Humidity=self.yearly_mean_humidity)

        COP_multiplier = self.estimate_COP(yearly_wetbulb_temperature) / self.estimate_COP(wetbulb_temperature) # How much "worse" a warmer weather is compared to a cooler weather

        # print('COP_scenario: '+str(self.estimate_COP(wetbulb_temperature)))
        # print('COP_average: ' + str(self.estimate_COP(yearly_wetbulb_temperature)))
        # print('COP_ratio: '+str(COP_multiplier))
        # IT_equipment_power = (self.datacenter_size * self.num_datacenters) / self.pue # Share of the power that is IT only
        #
        # non_IT_power = (self.datacenter_size * self.num_datacenters) - IT_equipment_power

        IT_equipment_power = (self.datacenter_size * self.num_datacenters)  # Share of the power that is IT only by design

        non_IT_power = IT_equipment_power * (self.pue - 1)

        non_IT_cooling_power = 0.74 * non_IT_power # Other uses for non_IT_power, such as lighting and electricity transformed should not be counted

        non_IT_misc_power = 0.26 * non_IT_power # Lighting and electricity generation

        fixed_power = IT_equipment_power + non_IT_misc_power  # Power in the datacenter that will not fluctuate due to weather

        weather_induced_cooling_power = non_IT_cooling_power * (COP_multiplier)

        total_power = fixed_power + weather_induced_cooling_power

        cooling_power = weather_induced_cooling_power

        return total_power, cooling_power

    def estimate_heat_generation(self, efficiency=0.6):
        """
        Estimate the heat generation of the datacenters
        to enable potential use of excess heat for other purposes.
        """
        heat_conduction_efficiency = efficiency # Lower bound taken, could be up to 95%

        # IT_equipment_power = (self.datacenter_size * self.num_datacenters) / self.pue # Share of the power that is IT only
        IT_equipment_power = (self.datacenter_size * self.num_datacenters)  # Share of the power that is IT only by design
        
        return IT_equipment_power * heat_conduction_efficiency
    
    def load_COP_data(self, base_folder, list_files, make_spline=True):
        file_tables = {}
        for a_file in list_files:
            file_location = os.path.join(base_folder, a_file)
            my_data = np.genfromtxt(file_location, delimiter=',', skip_header=1)
            number_on_file = [int(s) for s in a_file.split('_') if s.isdigit()]
            temperature_focus = number_on_file[0]
            if make_spline:
                f_COP = interpolate.interp1d(np.squeeze(my_data[:,0]), np.squeeze(my_data[:,1]))
                file_tables[temperature_focus] = f_COP
            else:
                file_tables[temperature_focus] = my_data
        return file_tables

    def estimate_COP(self, wetbulb_temperature):
        temperature_list = list(self.COP_tables.keys())
        for i in range(1,len(temperature_list)):
            if self.working_temperature == temperature_list[i-1]:
                min_index = i-1
                max_index = i-1
            elif self.working_temperature > temperature_list[i-1] and self.working_temperature < temperature_list[i]:
                min_index = i-1
                max_index = i
            elif self.working_temperature == temperature_list[i]:
                min_index = i
                max_index = i
            elif self.working_temperature > temperature_list[-1]:
                min_index = len(temperature_list) - 1
                max_index = len(temperature_list) - 1
        COP_low_table = self.COP_tables[temperature_list[min_index]]
        COP_high_table = self.COP_tables[temperature_list[max_index]]

        COP_low = COP_low_table(wetbulb_temperature)
        COP_high = COP_high_table(wetbulb_temperature)

        COP_estimated = (self.working_temperature - temperature_list[min_index])/(temperature_list[max_index] - temperature_list[min_index])* (COP_high - COP_low) + COP_low

        return COP_estimated

if __name__ == "__main__":
    # Example with units in MW
    power_consumption = 100
    datacenter_name = 'Siemens'
    working_temp = 35
    cooling_tech = DATACENTER_COOLING_TECH.LIQUID
    datacenter_type = DATACENTER_TYPE.AI

    # Scenario
    temperature = 35 #C
    humidity = 68 #Percent

    data_industrial = pd.read_csv(r'data/Consumed_industrial_kW.csv')

    siemens_datacenter = DatacenterConsumptionModel(datacenter_name, power_consumption, working_temp, cooling_tech, datacenter_type, 'Atlanta', 1)

    print('Made Datacenter '+siemens_datacenter.name+' with PUE '+str(cooling_tech.value)+' and consumption '+str(power_consumption)+' MW')

    total_power, cooling_power = siemens_datacenter.estimate_power_consumption(temperature, humidity)

    data_industrial['Datacenter Consumption (MW)'] = data_industrial.apply(
    lambda x: siemens_datacenter.estimate_power_consumption((x['DBT']-32)*(5/9), x['Rhum']), axis=1)

    data_industrial['Datacenter Consumption PUE'] = data_industrial.apply(
        lambda x: x['Datacenter Consumption (MW)'][0]/100, axis=1)

    print('With temperature '+str(temperature)+' and humidity '+str(humidity)+' '+siemens_datacenter.name+' consumes '+str(total_power)+' MW'+' from which '+str(cooling_power)+ ' MW is for cooling')

    heat_generation = siemens_datacenter.estimate_heat_generation()

    print('The datacenter '+siemens_datacenter.name +' could redirect '+str(heat_generation)+' MW of heat')

    print('The Datacenter'+siemens_datacenter.name +' has a mean yearly PUE of '+str(data_industrial.loc[:,'Datacenter Consumption PUE'].mean()))
    siemens_datacenter.estimate_COP(25)
    