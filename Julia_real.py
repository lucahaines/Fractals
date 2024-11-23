#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 01:55:26 2024

@author: lucahaines
"""

from PIL import Image
import numpy as np

W, H = 1000, 1000
imax = 256

# Starting c-values
#c = -0.70176 - 0.3842j
#c = 0.355 + 0.355j
#c = -0.4 + 0.6j
#c = -0.8 + 0.156j
c = complex(1/np.sqrt(2),(1/np.sqrt(3)))

# Change the scaling or power of the function z = a*z**d + c
a = complex(1, 0)
d = 2

# Map pixel coordinates to the complex plane
def normalizevalx(x):
    return -1.5 + (x / W) * 3

def normalizevaly(y):
    return -1.5 + (y / H) * 3

# Julia set function
def julia(z):
    for n in range(imax):
        z = a*z**d + c
        if abs(z) > 2:
            return n
    return imax

# Create image
im = Image.new("L", (W, H))
pixels = im.load()

# Generate the Julia set image
for x in range(W):
    for y in range(H):
        z = complex(normalizevalx(x), normalizevaly(y))
        n = julia(z)
        
        # Calculate pixel intensity based on the number of iterations
        intensity = int(255 * n / imax)  # Map n to [0, 255]
        pixels[x, y] = intensity

# Save and show the image
im.save("julia_set_grayscale.png")
im.show()
