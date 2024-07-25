import math
 
from stiffness.services.interpolation import interpolate_parameters
 
# sd = soil density
# D = pipe outside diameter
# H = depth to pipe centerline
# gammaBar  = effective unit weight of soil
# delta = interface angle of friction for pipe and soil = f*phi
# phi = internal friction angle of the soil
# f = coating dependent factor relating the internal friction angle of the soil to the friction angle at the soil-pipe interface
    # Concrete 1.0
    # Coal Tar 0.9
    # Rough Steel 0.8
    # Smooth Steel 0.7
    # Fusion Bonded EpoH / Dy 0.6
    # Polyethylene 0.6
 
# delta_t = displacement at Tu
    #  3 (mm) for dense sand = 3 * 10^-3 (m)
    #  5 (mm) for loose sand = 5 * 10^-3 (m)
 
def displacement_at_Tu(sd):
    if sd == 'dense':
        delta_t = 3
    elif sd == 'loose':
        delta_t = 5
    else:
        delta_t = 4
    return (delta_t * 10**-3)
 
def get_radians(angle):
    return math.radians(angle)
 
#  K0 = coefficeitn of pressure at rest
def coefficeitn_of_pressure_at_rest(phi):
    K0 = 1 - math.sin(math.radians(phi))
    K0 =  round(K0, 3)
    return K0
 
#delta = interface angle of friction for pipe and soil = f*phi
def interface_angle_of_friction(f, phi):
    delta = f * phi
    delta = round(delta, 3)
    return delta
 
# Tu = Axial Soil Springs ( kN/m)
def axial_soil_springs(K0, gammaBar, D, H, delta):
    Tu =(math.pi) * D * H * gammaBar * ( (1+K0) / 2 ) * ( math.tan(math.radians(delta)) )
    Tu = round(Tu, 3)
    return Tu
 
 
# Nqh = horizontal bearing capacity factor (0 for phi = 0)
def horizontal_bearing_capacity(phi, H, DD):
    a, b, c, d, e = interpolate_parameters(phi)
    Nqh = a + b * (H / DD)+ c * (H / DD)** 2 + d * (H / DD)** 3 + e * (H / DD)** 4
    Nqh = round(Nqh, 3)
    return Nqh
 
# Pu = Lateral Soil Springs (kN/m)
def lateral_soil_springs(Nqh, gammaBar, H, D):
    Pu = Nqh * gammaBar * H * D
    Pu = round(Pu, 3)
    return Pu
 
# Delta p = Displacement at Pu <= 0.1 * D to 0.15 * D
def displacement_at_Pu(Pu, K0, D, H):
    Delta_p = 0.04 * ( H + D/2 )
    Delta_p = round(Delta_p, 3)
    return Delta_p
 
# Qu = Vertical Uplift Soil Springs (kN/m)
def vertical_uplift_soil_springs(Nqv, gammaBar, H, D):
    Qu = Nqv * gammaBar * H * D
    Qu = round(Qu, 3)
    return Qu
 
# delta qu = displacement at Qu= 0.01H to 0.02H for dense to loose sands < 0.1D
def displacement_at_Qu(sd, H, D):
    if sd == 'dense':
        delta_qu = 0.01 * H
    elif sd == 'loose':
        delta_qu = 0.02 * H
    else:
        delta_qu = 0.015 * H
    delta_qu = round(delta_qu, 3)
    return delta_qu
 
# Nqv = vertical  uplift factor for sand (0 for phi = 0)
def vertical_uplift_factor(phi, H, D):
    Nqv = phi * H / ( 44 * D )
    Nqv = round(Nqv, 3)
    return Nqv
 
# Qd Vertical Bearing Soil Springs (kN/m)
    # gamma = gammaBar + 10
def vertical_bearing_soil_springs(wt,Nq, Ng, gammaBar, H, D):
    if wt == 'Dry':
        Qd = (  Nq * gammaBar * H * D ) + ( Ng * ( gammaBar ) * (D ** 2) / 2 )
    else :
        Qd = (  Nq * gammaBar * H * D ) + ( Ng * ( gammaBar + 10 ) * (D ** 2) / 2 )
    Qd = round(Qd, 3)
    return Qd
 
# Nq, Ng = bearing capacity factors
def bearing_capacity_factors(phi):
    Nq = math.exp(math.pi * math.tan(math.radians(phi)))* (math.tan(math.pi/4 + math.radians(phi/2)) )** 2
    Nq = round(Nq, 3)
    Ng = math.exp( 0.18 * phi - 2.5 )
    Ng = round(Ng, 3)
    return Nq, Ng
 
def displacement_at_Qd(D, H):
    delta_qd = 0.1 * D
    delta_qd = round(delta_qd, 3)
    return delta_qd
 
 
# STIFFNESS:
def axial_soil_springs_stiffness(Tu, delta_t, D):
    first = Tu / delta_t
    first = round(first, 3)
    second = (Tu / delta_t) / D
    second = round(second, 3)
    return first, second
 
def lateral_soil_springs_stiffness(Pu, Delta_p, D):
    first = Pu / Delta_p
    first = round(first, 3)
    second = (Pu / Delta_p) / D
    second = round(second, 3)
    return first, second
 
def vertical_uplift_soil_springs_stiffness(Qu, delta_qu, D):
    first = Qu / delta_qu
    first = round(first, 3)
    second = (Qu / delta_qu) / D
    second = round(second, 3)
    return first, second
 
def vertical_bearing_soil_springs_stiffness(Qd, delta_qd, D):
    first = Qd / delta_qd
    first = round(first, 3)
    second = (Qd / delta_qd) / D
    second = round(second, 3)
    return first, second
 
# stiffness calculation
 
def stiffness_calculation(sd,wt, D, H, f,phi,gammaBar):
   
    a,b,c,d,e = interpolate_parameters(phi)
    delta_t = displacement_at_Tu(sd)
    K0 = coefficeitn_of_pressure_at_rest(phi)
    delta = interface_angle_of_friction(f, phi)
    Tu = axial_soil_springs(K0, gammaBar, D, H, delta)
    Nqh = horizontal_bearing_capacity(phi, H, D)
    Pu = lateral_soil_springs(Nqh, gammaBar, H, D)
    Delta_p = displacement_at_Pu(Pu, K0, D, H)
    Nqv = vertical_uplift_factor(phi, H, D)
    Qu = vertical_uplift_soil_springs(Nqv, gammaBar, H, D)
    delta_qu = displacement_at_Qu(sd, H, D)
    Nq, Ng = bearing_capacity_factors(phi)
    Qd = vertical_bearing_soil_springs(wt,Nq, Ng, gammaBar, H, D)
    delta_qd = displacement_at_Qd(D, H)
 
    # stiffness calculation
    aTu, bTu = axial_soil_springs_stiffness(Tu, delta_t, D)
    aPu, bPu = lateral_soil_springs_stiffness(Pu, Delta_p, D)
    aQu, bQu = vertical_uplift_soil_springs_stiffness(Qu, delta_qu, D)
    aQd, bQd = vertical_bearing_soil_springs_stiffness(Qd, delta_qd,D)
 
 
    stiffness = {
        'sd': sd,
        'D': D,
        'H': H,
        'f': f,
        'phi': phi,
        'gammaBar': gammaBar,
        'delta_t': delta_t,
        'K0': K0,
        'Nqh': Nqh,
        'Pu': Pu,
        'Delta_p': Delta_p,
        'Nqv': Nqv,
        'Qu': Qu,
        'delta_q': delta_qu,
        'Nq': Nq,
        'Ng': Ng,
        'Qd': Qd,
        'delta_qd': delta_qd,
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'e': e ,
        'Tu': Tu,
        'delta': delta,
        'aTu': aTu,
        'bTu': bTu,
        'aPu': aPu,
        'bPu': bPu,
        'aQu': aQu,
        'bQu': bQu,
        'aQd': aQd,
        'bQd': bQd
   
    }
    return  stiffness