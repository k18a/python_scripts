def firstorder(t, q0, qe, k1):
    """
    first order fitting function
    :param t: time
    :param q0: initial adsorbed at t = 0
    :param qe: equilibrium adsorbed at t = infinity
    :param k1: first order fitting parameter
    :return: amount adsorbed at time t
    """
    import numpy as np
    return qe - qe * np.exp(-k1 * t) + q0 * np.exp(-k1 * t)

def secondorder(t, q0, qe, k2):
    """
    second order fitting function
    :param t: time
    :param q0: initial adsorbed at time t = 0
    :param qe: equilibrium adsorbed at time t = infinity
    :param k2: second order fitting parameter
    :return: amount adsorbed at time t
    """
    return (qe * k2 * t * abs(qe - q0) + q0)/(1 + k2 * t * abs(qe - q0))

def elovich(t, q0, qe, k2):
    """
    second order fitting function
    :param t: time
    :param q0: initial adsorbed at time t = 0
    :param qe: equilibrium adsorbed at time t = infinity
    :param k2: second order fitting parameter
    :return: amount adsorbed at time t
    """
    return 1#(-log(exp))

def _get_analytical_roots(Kc,n):
    """calculate roots for the analytical equation ...
    for radial diffusion based on carlslaw jaeger
    
    Arguments:
        Kc {float} -- Kc - ratio of gas storage capacity 
        n {float} -- number of roots
    
    Returns:
        numpy list -- list of roots
    """
    import numpy as np
    y0 = 0
    y1 = 0
    a0 = 0
    roots = []
    alpha_set = np.linspace(0,10*np.pi,5000)
    for a1 in alpha_set:
        y1 = 3*np.sin(a1) + Kc*(a1**2)*np.sin(a1) - 3*a1*np.cos(a1)
        if abs(y0+y1) != (abs(y0)+abs(y1)):
            af = a0 - y0*((a1-a0)/(y1-y0))
            roots.append(af)
            if len(roots)>=n:
                break
        a0 = a1
        y0 = y1
    return roots

def cj_analytical_edge_concentration(t,rho_c0,rho_i,Kc,Ra,n):
    """get analytical solution for gas concentration based ...
    on radial diffusion function (Carlslaw Jaeger)
    
    Arguments:
        t {int} -- time in seconds
        rho_c0 {float} -- initial concentration at edge mol/m^3
        rho_i {float} --  initial concentration at centre mol/m^3
        Kc {float} -- gas storage capacity 
        Ra {float} -- particle radius
        n {int} -- number of roots
    
    Returns:
        float -- gas concentration at edge
    """
    import numpy as np
    sum_roots = 0
    roots = _get_analytical_roots(Kc,n)
    for alpha in roots:
        sum_roots += np.exp(-(Kc*(alpha**2)*t)/((Ra)**2))/(((Kc**2)*(alpha**2))+9*(Kc+1))
    rho =rho_c0-(rho_c0-rho_i)/(Kc+1)+(6*Kc)*(rho_c0-rho_i)*sum_roots
    return rho