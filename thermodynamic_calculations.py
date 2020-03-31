def calculate_pseudo_saturation_pressure(method,gas,temperature):
    import CoolProp.CoolProp as cp
    Tc = cp.PropsSI('TCRIT',gas)
    Pc = cp.PropsSI('PCRIT',gas)
    if (type(method) == int) or type(method) == float:
        Ps = method
    elif method == 'dubinin':
        T = temperature
        Ps = Pc*(T/Tc)**2
    elif method == 'amankwah':
        T = temperature
        k = input('enter k for amankwah :')
        Ps = Pc*(T/Tc)**k
    elif method == 'reduced_kirchoff':
        import numpy as np
        Tnbp = cp.PropsSI('T', 'P', 101325, 'Q', 0, gas)
        T = temperature
        Ps = Pc*np.exp((Tnbp/Tc)*(np.log(Pc)/(1-(Tnbp/Tc)))*(1-(Tc/T)))
    else:
        print('invalid method specified to calculate Ps; using dubinin method')
        T = temperature
        Ps = Pc*(T/Tc)**2
    print('P0 set as {}'.format(Ps))
    return Ps

def get_z(pressure, temperature, gas):
    import CoolProp.CoolProp as CP
    z = CP.PropsSI('Z','P',pressure,'T',temperature,gas)
    return z

def get_rhom(pressure, temperature, gas):
    import CoolProp.CoolProp as CP
    z = CP.PropsSI('Z','P',pressure,'T',temperature,gas)
    R = 8.3144598
    rhom = pressure/(z*R*temperature)
    return rhom