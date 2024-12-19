import matplotlib.pyplot as plt
import numpy as np

def mdf_nickerson2016(Aa, tc, freq, V, A, P, T):
    '''
    Input
    Aa: analytical accuracy [ppb]
    tc: closure time of the chamber [s]
    freq: frequency of the measured data [Hz]
    V: chamber volume [m3]
    A: chamber surface area [m2]
    P: atmospheric pressure [Pa]
    T: ambient temperature [K]
    
    Output:
    mdf: Minimum detectable flux [nmol m-2 s-1]
    '''
    R = 8.314 #m3 Pa K-1 mol-1
    mdf = (Aa/(tc*(tc*freq)**(1/2)))*(V*P/(A*R*T))
    return mdf

def mdf_nickerson2016_minimal_height(mdf, Aa, tc, freq, P, T, diameter):
    '''
    Input
    mdf: Minimum detectable flux [nmol m-2 s-1]
    Aa: analytical accuracy [ppb]
    tc: closure time of the chamber [s]
    freq: frequency of the measured data [Hz]
    P: atmospheric pressure [Pa]
    T: ambient temperature [K]
    # diameter: diameter of the chamber [m]
    
    Output:
    height: minimal height of the chamber [m]
    '''
    R = 8.314 #m3 Pa K-1 mol-1
    # height = (Aa/(mdf*(tc*freq)**(1/2)))*(P/(np.pi*diameter*R*T))
    V_A = mdf*R*T*tc*(tc*freq)**(1/2)/(Aa*P)
    return V_A


def chamber_properties(diameter, height):
    '''
    Input
    diameter: diameter of the chamber [m]
    height: height of the chamber [m]
    
    Output:
    V: chamber volume [m3]
    A: chamber surface area [m2]
    '''
    V = np.pi*diameter**2/4*height
    A = np.pi*diameter*height
    return V, A 

class ChamberDesign:
    def __init__(self, expected_flux_range, temperature_range, pressure_range, sensors_frequency=1, sensors_accuracy=30*1000, measurement_time=120):
        '''
        Input:
        expected_flux_range: (expected_flux_min, expected_flux_max) [nmol m-2 s-1]
        temperature_range: (temperature_min, temperature_max)  [K]
        pressure_range: (pressure_min, pressure_max) [Pa]
        sensors_frequency: frequency of the sensors [Hz]
        sensors_accuracy: accuracy of the sensors [ppb]
        measurement_time: time of the measurement [s]
        '''
        self.expected_flux_min = expected_flux_range[0]
        self.expected_flux_max = expected_flux_range[1]
        self.temperature_min = temperature_range[0]
        self.temperature_max = temperature_range[1]
        self.pressure_min = pressure_range[0]
        self.pressure_max = pressure_range[1]

        self.sensors_frequency = sensors_frequency
        self.sensors_accuracy = sensors_accuracy

        self.measurement_time = measurement_time

        self.tolerance_flux = 50 #[%]

    def _chamber_diameter_options(self):

        outer_diameter = [0.1, 0.11, 0.12, 0.133, 0.133, 0.15, 0.18, 0.2, 0.25, 0.3, 0.4, 0.5]
        inner_diameter = [0.094, 0.1, 0.11, 0.123, 0.127, 0.144, 0.172, 0.194, 0.24, 0.29, 0.39, 0.492]

        return outer_diameter, inner_diameter
        
    def minimal_height(self, diameter):
        height_mdf = mdf_nickerson2016_minimal_height(mdf=self.expected_flux_min*(1-self.tolerance_flux/100), 
                                                      Aa=self.sensors_accuracy, 
                                                      tc=self.measurement_time, freq=self.sensors_frequency, P=self.pressure_min, 
                                                      T=self.temperature_min, diameter=diameter)
        print('Minimal height of the chamber:')
        print('height <= {:.2f} m'.format(height_mdf))

        ratio = self.ratio_area_perimeter(diameter)
        print('ratio:\t', ratio, 'cm')


    def ratio_area_perimeter(self, diameter):
        '''
        Input:
        diameter: diameter of the chamber [m]

        Output:
        ratio: [cm]
        '''
        diameter = diameter*100
        area = np.pi*diameter**2/4
        perimeter = np.pi*diameter
        return area/perimeter


if __name__ == '__main__':
    # a = mdf_nickerson2016(Aa=30*1000, tc=120, freq=1,
    #               V=np.pi*0.2**2/4*0.2, A=np.pi*0.2**2/4,
    #               P=101325, T=298.15)
    # print(a)
    a = ChamberDesign(expected_flux_range=(0.5*1000, 8*1000), 
                      temperature_range=(280, 300), 
                      pressure_range=(100000, 110000))
    a.minimal_height(diameter=0.25)
