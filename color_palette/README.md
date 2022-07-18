# color_palette
*Python script to generate a color palette from an image using k-means clustering.*

Michael D'Argenio  
mjdargen@gmail.com  
https://dargen.io  
https://github.com/mjdargen  
Created: July 10, 2022  

# Description
Have you ever seen the images floating around that show the color palettes from various scenes of visually striking movies? Well now you can create some images of your own using this script! The script uses a process called k-means clustering to generate a color palette from the image.

The script creates two versions of the original image: one with a color swatch at the bottom and one with the pixels in the image replaced with their closest color from the palette. The script will also plot all the pixels in 3D space based on their RGB values and show the clusters by coloring them based on their closest color from the palette.  

**Note**: The source code also contains a modified script from GitHub user v-za to download still images from movies from https://film-grab.com. See their original script here: https://github.com/v-za/film-grabber.  

To easily run the code in your browser and avoid having to install dependencies, you can use this Google Colab Notebook: https://colab.research.google.com/drive/1WkfTnGPPqsvJdV8SHu_zw3rnY21pIehT?usp=sharing  


# Set-Up
To run this code in your environment, you will need to:  
  * Install Python 3 and pip
  * Install Pillow, plotly, and beautifulsoup4: `pip3 install -r requirements.txt`


# Running the Code
To run the film grabber script, use the following command: `python3 filmgrabber.py -f <film> -p <path>`  
  * `-f <film>` - Name of the film to search for. Exp: `Blade Runner 2049`
  * `-p <path>` - Output file path to store images. Exp: `./stills`



To run the color palette script, use the following command: `python3 palette.py -i <image> -k <kcolors> -l <limit>`  
  * `-i <image>` - Path to image file. Exp: `./bladerunner001.jpg`  
  * `-k <kcolors>` - K value i.e. number of colors in palette. Exp: `6`
  * `-l <limit>` - Max number of iterations to test convergence. Exp: `20`


#  Demo  
**Original Image**  
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp1_original.jpg" width="48%">
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp2_original.jpg" width="48%">  


**Color Palette Image**  
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp1_palette.jpg" width="48%">
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp2_palette.jpg" width="48%">  


**Replaced Colors Image**  
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp1_replaced.jpg" width="48%">
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp2_replaced.jpg" width="48%">  

**Preview of Interactive 3D Pixel Plot**  
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp1_plot.png" width="48%">
<img src="https://raw.githubusercontent.com/mjdargen/tutorials/main/color_palette/exp/exp2_plot.png" width="48%">  

# Tutorial
For a complete walkthrough of how this program works, you can go here: [https://www.instructables.com/Color-Palette-Generator/](https://www.instructables.com/Color-Palette-Generator/).
