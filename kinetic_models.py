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
