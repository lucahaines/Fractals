#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:31:10 2024

@author: lucahaines
"""

from PIL import Image
import numpy as np
import os

W, H = 100, 100 # Image dimensions would recommend 1000 x 1000 for it to not look silly
imax = 500  # Maximum iterations

# Choose a c-value
#c = -0.70176 - 0.3842j
c = -0.8 + 0.156j

# Other parameters in equation z = a*z**d + c
a = complex(1, 0)
d = 2


# Zoom parameters
num_frames = 100
zoom_factor = 0.95

# Saving frames
output_dir = "julia_frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Julia set function
def julia(z):
    for n in range(imax):
        z = a * z**d + c
        if abs(z) > 2:
            return n
    return imax  # Point remains bounded

# Function to normalize coordinates from pixel space to the complex plane
def normalizevalx(x, x_min, x_max):
    return x_min + (x / W) * (x_max - x_min)

def normalizevaly(y, y_min, y_max):
    return y_min + (y / H) * (y_max - y_min)

# Generate and save frames with zoom
for frame_num in range(num_frames):
    imax = 500 + frame_num 
    # Define zoom region in the complex plane
    x_min, x_max = -1.5 * (zoom_factor ** frame_num), 1.5 * (zoom_factor ** frame_num)
    y_min, y_max = -1.5 * (zoom_factor ** frame_num), 1.5 * (zoom_factor ** frame_num)
    
    # Initialize the image
    im = Image.new("L", (W, H))
    pixels = im.load()

    # Generate the Julia set image for the zoom level
    for x in range(W):
        for y in range(H):
            z = complex(normalizevalx(x, x_min, x_max), normalizevaly(y, y_min, y_max))
            n = julia(z)
            
            # Calculate pixel intensity based on iteration count
            # TRYING TO FIGURE OUT HOW TO DECREASE BRIGHTNESS OF LOWS
            # AS FRAME_NUM INCREASES. I TRIED A LINEAR AND LOGARITHMIC 
            # DECREASE BUT NEITHER SEEMED TO WORK.
            
            intensity = int(255 * n / imax)  # Map n to [0, 255] which is the
            # range of brightnesses any pixel can be
            pixels[x, y] = intensity

    # Save the image with a filename including the frame number
    frame_filename = os.path.join(output_dir, f"frame_{frame_num:03d}.png")
    im.save(frame_filename)
    print(f"Saved {frame_filename}")

print("Sweet! Now go to your terminal and enter the command: ffmpeg -framerate 30 -i frame_%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p julia_zoom.mp4")

# in terminal using ffmpeg enter command:
# ffmpeg -framerate 30 -i frame_%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p julia_zoom.mp4
