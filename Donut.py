import math
import os

theta_spacing = 0.07
phi_spacing = 0.02

R = 0.03  # large circle radius
r = 0.01 # small circle radius
k1, k2 = 50, 1  # projection constants

# screen size
width, height = 40,20

# Calculate the scaling 
K1 = width * k2 * 2 / (8 * (R + r))

# ASCIIs
asii_char = ".,-~:;=!*#$@"

def frames(A, B):
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    # empty buffers
    output = [[' ' for _ in range(width)] for _ in range(height)]
    z_buffer = [[0 for _ in range(width)] for _ in range(height)]

    for theta in frange(0, 2 * math.pi, theta_spacing):
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        for phi in frange(0, 2 * math.pi, phi_spacing):
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            # 3D coordinates of the torus
            circle_x = R + r * cos_theta
            circle_y = r * sin_theta

            # Rotated 3D coordinates
            x = circle_x * (cosB * cos_phi + sinA * sinB * sin_phi) - circle_y * cosA * sinB
            y = circle_x * (sinB * cos_phi - sinA * cosB * sin_phi) + circle_y * cosA * cosB
            z = k2 + cosA * circle_x * sin_phi + circle_y * sinA
            depth = 1 / z  # One over z (depth)

            # Project 3D coordinates to 2D
            scr_x = int(width / 2 + K1 * depth * x)
            scr_y = int(height / 2 - K1 * depth * y)

            # Calculate the luminance
            L = cos_phi * cos_theta * sinB - cosA * cos_theta * sin_phi - sinA * sin_theta + cosB * (cosA * sin_theta - cos_theta * sinA * sin_phi)

            if L > 0 and 0 <= scr_x < width and 0 <= scr_y < height:
                if depth > z_buffer[scr_y][scr_x]:
                    z_buffer[scr_y][scr_x] = depth
                    luminance_index = int(L * 8)
                    luminance_index = min(max(luminance_index, 0), 11)
                    output[scr_y][scr_x] = asii_char[luminance_index]

    os.system('cls' if os.name == 'nt' else 'clear')
    for row in output:
        print(' '.join(row))

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

# angles
A = 0
B = 0

# render frames
while True:
    frames(A, B)
    A += 0.04
    B += 0.02
