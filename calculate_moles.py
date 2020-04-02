def calculate_moles(pressure, volume, temperature, gas, eos):
    import CoolProp.CoolProp as CP
    R = 8.3144598
    critical_temperature = CP.PropsSI('TCRIT', gas)
    reduced_temperature = temperature / critical_temperature
    critical_pressure = CP.PropsSI('PCRIT', gas)
    acentric = CP.PropsSI('ACENTRIC', gas)
    vanderWaalsconstants = {
        'methane': [0.2283,4.278e-05],
        'carbondioxide': [0.364,4.267e-05],
        'helium':[0.00346,2.3800000000000003e-05]
    }
    n_init = (pressure*volume)/(R*temperature)
    if eos == 'ideal':
        moles = n_init
    elif eos == 'coolprop':
        z = CP.PropsSI('Z','P',pressure,'T',temperature,gas)
        moles = n_init/z
    elif eos == 'vanderWaals':
        a,b = vanderWaalsconstants.get(gas,'invalideos')
        n_old = 0
        n_new = n_init
        while not ((0.9999*n_new)<n_old<(1.0001*n_new)):
            n_old = n_new
            n_new = ((pressure*volume)/(R*temperature))*\
            (1 + ((n_new**2 * a)/(pressure * volume**2)))*\
            (1 - (n_new*b/volume))
        moles = n_new
    elif eos == 'RedlichKwong':
        alpha = reduced_temperature ** (-0.5)
        Xi = 0.42748
        Omega = 0.08664
        a = (Xi * alpha * (R ** 2) * (critical_temperature ** 2)) / (critical_pressure)
        b = (Omega * R * critical_temperature) / (critical_pressure)
        sigma = 1
        epsilon = 0
        n_old = 0
        n_new = n_init
        Vm = volume / n_init
        while not ((0.9999 * n_new) < n_old < (1.0001 * n_new)):
            n_old = n_new
            Vm = (R * temperature / pressure) + b - (a / pressure) * (Vm - b) / (
                    (Vm + epsilon * b) * (Vm + sigma * b))
            n_new = volume / Vm
        moles = n_new
    elif eos == 'PengRobinson':
        alpha = (1 + (0.37464 + 1.54226 * acentric - 0.26992 * (acentric ** 2)) * (
                    1 - reduced_temperature ** (0.5))) ** 2
        Xi = 0.45724
        Omega = 0.0778
        a = (Xi * alpha * (R ** 2) * (critical_temperature ** 2)) / (critical_pressure)
        b = (Omega * R * critical_temperature) / (critical_pressure)
        sigma = 1 + 2 ** (0.5)
        epsilon = 1 - 2 ** (0.5)
        n_old = 0
        n_new = n_init
        Vm = volume / n_init
        while not ((0.9999 * n_new) < n_old < (1.0001 * n_new)):
            n_old = n_new
            Vm = (R * temperature / pressure) + b - (a / pressure) * (Vm - b) / (
                    (Vm + epsilon * b) * (Vm + sigma * b))
            n_new = volume / Vm
        moles = n_new
    return moles

def get_z(pressure, temperature, gas):
    import CoolProp.CoolProp as CP
    z = CP.PropsSI('Z','P',pressure,'T',temperature,gas)
    return z

def get_rhom(pressure, temperature, gas):
    import CoolProp.CoolProp as CP
    rhom = CP.PropsSI('DMOLAR','P',pressure,'T',temperature,gas)
    return rhom