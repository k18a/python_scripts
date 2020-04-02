def langmuir(cg, qm, b):
    """calculates the langmuir amount adsorbed qa = qm*b*cg/(1+*cg)
    
    Arguments:
        cg {float} -- gas concentration mol/m3
        qm {float} -- maximum sorption capacity mol/kg
        b {float} -- affinity constant 1/Pa
    
    Returns:
        float -- amount adsorbed mol/kg
    """
    return (qm*b*cg)/(1+b*cg)

def langmuir_volume_temperature(T,a1,a2):
    """calculates the langmuir maximum sorption capacity at different temperatures qm = a1 + a2/T
    
    Arguments:
        T {float} -- Temperature K
        a1 {float} -- Fitting constant mol/(kg*T)
        a2 {float} -- Fitting constant mol/kg
    
    Returns:
        float -- maximum sorption capacity
    """
    return a1 + a2/T

def langmuir_pressure_temperature(T,P0,Q):
    """ to be completed 
    """
    from numpy import exp
    return P0*exp(Q/(8.314*T))

def linear(cg, K):
    """calculates linear amount adsorbed qa = k*cg
    
    Arguments:
        cg {float} -- gas concentration mol/m3
        K {float} -- henry's constant m3/kg
    
    Returns:
        float -- amount adsorbed mol/kg
    """
    return K*cg

def freundlich(P,K,n):
    """
    freundlich isotherm
    :param P:
    :param K:
    :param n:
    :return:
    """
    return K*P**(1/float(n))

def dubinin_radushkevich(P,T,P0,V0,E):
    """
    DR isotherm
    :param P:
    :param K:
    :param n:
    :return:
    """
    import numpy as np
    return V0*np.exp(-((8.314*T/E)*np.log(P0/P)) **2)

# calibrate specific volume
def specific_volume_calibration(Vr,Vs,Pi,Pc,Pe,Wsh):
    """calibrate specific volume
    
    Arguments:
        Vr {float} -- reference cell volume ml
        Vs {float} -- sample cell volume ml
        Pi {float} -- initial pressure bar_g
        Pc {float} -- charge pressure bar_g
        Pe {float} -- equilibrium pressure bar_g
        Wsh {float} -- sample weight g
    
    Returns:
        float -- specific volume ml/g
    """ 
    Vv = (Pc-Pe)*Vr / (Pe-Pi)
    Vsh = Vs - Vv
    Vsp = Vsh/Wsh

    return Vsp
