# ecef_to_llh.py
#
# Usage: python3 script_name.py arg1 arg2 ...
# Text explaining script usage
# Parameters:
# arg1: description of argument 1
# arg2: description of argument 2
# ...
# Output:
# A description of the script output
#
# Written by Michael Hoffman
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.
# import Python modules
# e.g., import math # math module
import sys # argv
# "constants"
# e.g., R_E_KM = 6378.137
# helper functions
## function description
# def calc_something(param1, param2):
# pass
# initialize script arguments
# arg1 = '' # description of argument 1
# arg2 = '' # description of argument 2
# parse script arguments
# if len(sys.argv)==3:
# arg1 = sys.argv[1]
# arg2 = sys.argv[2]
# ...
# else:
# print(\
# 'Usage: '\
# 'python3 arg1 arg2 ...'\
# )
# exit()
# write script below this line
import math 

# Constants
RE = 6378.1363  # Earth radius
eE = 0.081819221456  # Earth eccentricity

# Helper functions
# Calculate ϕ0
def initial_latitude(rX, rY, rZ):
    r_mag = math.sqrt(rX ** 2 + rY ** 2 + rZ ** 2)
    return math.asin(rZ / r_mag)

# Calculate CE
def calc_CE(ϕgd):
    return RE / math.sqrt(1 - (eE ** 2) * (math.sin(ϕgd) ** 2))

# Calculate SE
def calc_SE(ϕgd):
    return RE * (1 - eE ** 2) / math.sqrt(1 - (eE ** 2) * (math.sin(ϕgd) ** 2))

# ECEF to LLH 
def ecef_to_llh(rX, rY, rZ):
    # Calculate the initial guess for ϕ0 and rλ0
    ϕ0 = initial_latitude(rX, rY, rZ)
    rλ0 = math.sqrt(rX ** 2 + rY ** 2)

    # Iterate
    ϕgd = ϕ0
    for _ in range(5):  
        CE = calc_CE(ϕgd)
        SE = calc_SE(ϕgd)
        ϕgd = math.atan((rZ + CE * eE ** 2 * math.sin(ϕgd)) / rλ0)

    # Calculate hae
    CE = calc_CE(ϕgd)
    SE = calc_SE(ϕgd)
    hae = (rZ / math.sin(ϕgd)) - SE

    # Calculate λ
    λ = math.atan2(rY, rX) 

    # Convert to degrees
    ϕgd_deg = math.degrees(ϕgd)
    λ_deg = math.degrees(λ)

    return ϕgd_deg, λ_deg, hae

# Initialize script arguments
if len(sys.argv) == 4:
    rX = float(sys.argv[1])
    rY = float(sys.argv[2])
    rZ = float(sys.argv[3])
else:
    print('Usage: python3 ecef_to_llh.py rX rY rZ')
    sys.exit()

# ECEF to LLH 
latitude, longitude, height = ecef_to_llh(rX, rY, rZ)

print(f"Latitude: {latitude:.6f}°")
print(f"Longitude: {longitude:.6f}°")
print(f"Height above ellipsoid: {height:.6f} km")
