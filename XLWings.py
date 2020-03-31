import xlwings as xw
import numpy as np
from adsorption_calculations import specific_volume_calibration
from convert_units import convert_pressure
from convert_units import convert_temperature
from convert_units import convert_volume
from thermodynamic_calculations import get_z
from thermodynamic_calculations import get_rhom

@xw.sub  # only required if you want to import it or run it via UDF Server
def main():
    wb = xw.Book.caller()
    wb.sheets[0].range("A1").value = "Hello xlwings!"

@xw.func
def hello(name):
    return "hello {0}".format(name)

@xw.func
def pressure_conversion(input_value, input_units, output_units):
    return convert_pressure(input_value, input_units, output_units)

@xw.func
def calibrate_specific_volume(Vr,Vs,Pi,Pc,Pe,Wsh):
    #convert to SI units
    Pi_Pa = convert_pressure(Pi,"bar_g","Pa_a")
    Pc_Pa = convert_pressure(Pc,"bar_g","Pa_a")
    Pe_Pa = convert_pressure(Pe,"bar_g","Pa_a")

    Vsp = specific_volume_calibration(Vr,Vs,Pi_Pa,Pc_Pa,Pe_Pa,Wsh)
    Vv = (Pc_Pa-Pe_Pa)*Vr / (Pe_Pa-Pi_Pa)
    Vsh = Vs - Vv
    Vsp = Vsh/Wsh

    return Vsp

@xw.func
def moles_SI(P,V,T,gas):
    R = 8.3144598
    z = get_z(P,T,gas)
    n = (P*V)/(z*R*T)

    return n

@xw.func
def moles(pressure, volume, temperature, gas):

    V = convert_volume(volume, 'ml', 'm3')
    T = convert_temperature(temperature,'degC','K')
    P = convert_pressure(pressure,'bar_a','Pa_a')

    n = moles_SI(P,V,T,gas)

    return n

@xw.func
def inject(gas,reference_volume,temperature,initial_pressure,charge_pressure,previously_injected):

    Vr = convert_volume(reference_volume, 'ml', 'm3')
    T = convert_temperature(temperature,'degC','K')
    Pi = convert_pressure(initial_pressure,'bar_a','Pa_a')
    Pc = convert_pressure(charge_pressure,'bar_a','Pa_a')

    ni = moles_SI(Pi,Vr,T,gas) #initial moles
    nc = moles_SI(Pc,Vr,T,gas) #charge moles
    ninj = nc - ni + previously_injected #injected moles

    return ninj

if __name__ == "__main__":
    xw.books.active.set_mock_caller()
    main()
