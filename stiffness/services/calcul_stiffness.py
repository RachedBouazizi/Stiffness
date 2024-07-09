import math

from stiffness.services.interpolation import interpolate_parameters

# sd = soil density
# D = pipe outside diameter
# H = depth to pipe centerline
# Gamma  = effective unit weight of soil
# delta = Tu = interface angle of friction for pipe and soil = f*phi
# phi = internal friction angle of the soil
# f = coating dependent factor relating the internal friction angle of the soil to the friction angle at the soil-pipe interface
    # Concrete 1.0
    # Coal Tar 0.9
    # Rough Steel 0.8
    # Smooth Steel 0.7
    # Fusion Bonded EpoH / Dy 0.6
    # Polyethylene 0.6

# delta_t = displacement at Tu
    #  (3 mm) for dense sand
    #  (5 mm) for loose sand

def displacement_at_Tu(sd):
    if sd == 'dense':
        delta_t = 3
    elif sd == 'loose':
        delta_t = 5
    else:
        delta_t = 4
    return delta_t

def get_radians(angle):
    return math.radians(angle)

#  K0 = coefficeitn of pressure at rest
def coefficeitn_of_pressure_at_rest(phi):
    K0 = 1 - math.sin(math.radians(phi))
    K0 =  round(K0, 3)
    return K0


# Nqh = horizontal bearing capacity factor (0 for phi = 0) 
def horizontal_bearing_capacity(phi, H, DD):
    a, b, c, d, e = interpolate_parameters(phi)
    Nqh = a + b * (H / DD)+ c * (H / DD)** 2 + d * (H / DD)** 3 + e * (H / DD)** 4
    Nqh = round(Nqh, 3)
    return Nqh

# Pu = Lateral Soil Springs
def lateral_soil_springs(Nqh, gamma, H, D):
    Pu = Nqh * gamma * H * D
    Pu = round(Pu, 3)
    return Pu

# Delta p = Displacement at Pu <= 0.1 * D to 0.15 * D
def displacement_at_Pu(Pu, K0, D, H):
    Delta_p = 0.04 * ( H + D/2 ) 
    Delta_p = round(Delta_p, 3)
    return Delta_p

# Qu = Vertical Uplift Soil Springs 
def vertical_uplift_soil_springs(Nqv, gamma, H, D):
    Qu = Nqv * gamma * H * D
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
    Nqv = phi * H / 44 * D
    Nqv = round(Nqv, 3)
    return Nqv

# Qd Vertical Bearing Soil Springs
def vertical_bearing_soil_springs(Nq, Ng, gamma, H, D):
    Qd = (  Nq * gamma * H * D ) + ( Ng * gamma * (D ** 2) / 2 )
    Qd = round(Qd, 3)
    return Qd

# Nq, Ng = bearing capacity factors
def bearing_capacity_factors(phi):
    Nq = math.exp(math.pi * math.tan(phi))* (math.tan(math.pi/4 + phi/2) )** 2
    Nq = round(Nq, 3)
    Ng = math.exp( 0.18 * math.pi - 2.5 )
    Ng = round(Ng, 3)
    return Nq, Ng


# stiffness calculation

def stiffness_calculation(sd, D, H, f,phi,Gamma):
    
    a,b,c,d,e = interpolate_parameters(phi)
    delta_t = displacement_at_Tu(sd)
    K0 = coefficeitn_of_pressure_at_rest(phi)
    Nqh = horizontal_bearing_capacity(phi, H, D)
    Pu = lateral_soil_springs(Nqh, Gamma, H, D)
    Delta_p = displacement_at_Pu(Pu, K0, D, H)
    Nqv = vertical_uplift_factor(phi, H, D)
    Qu = vertical_uplift_soil_springs(Nqv, Gamma, H, D)
    delta_qu = displacement_at_Qu(sd, H, D)
    Nq, Ng = bearing_capacity_factors(phi)
    Qd = vertical_bearing_soil_springs(Nq, Ng, Gamma, H, D) 

    stiffness = {
        'sd': sd,
        'D': D,
        'H': H,
        'f': f,
        'phi': phi,
        'gamma': Gamma,
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
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'e': e 
    
    }
    return  stiffness

