# PSNR-HVS-M-for-python
A python implementation of PSNR that takes the Human visual system into account. This code is based on Nikolay Ponomarenko matlab implementation of the PSNR-HVS & PSNR-m algorithm.


PSNR-HVS-M is Peak Signal to Noise Ratio taking into account Contrast Sensitivity Function (CSF) and between-coefficient contrast masking of DCT basis functions.

## Ported by :
Eduardo Prado (t2ac32)

## Original work by:
Nikolay Ponomarenko
http://www.ponomarenko.info/psnrhvsm.htm

## Installation
  Clone the repository or dowload the zip.
  Add the 'psnrhvsm' folder to your project
  
  In you .py file imports add this line.
  
    'from psnrhvsm import psnrhvsm'
  ### Quick test:
  Or use the jupyter notebook included in the main folder the test images used in the paper are also included.

### USAGE:
 Input : 
 1. img1: the first image being compared   
 2. img2: the second image being compared   
 3. wstep: step of 8x8 window to calculate DCT coefficients. Default value is 8.   
           
 #### Output:
  + p_hvs_m: the PSNR-HVS-M value between 2 images.
    + If one of the images being compared is regarded as perfect quality, then PSNR-HVS-M can be considered as the quality measure of the other image.
    + If compared images are visually undistingwished,then PSNR-HVS-M = 100000.   
  + p_hvs: the PSNR-HVS value between 2 images.   
       
 #### Default Usage:
           Given 2 test images img1 and img2, whose dynamic range is 0-255
        
           [p_hvs_m, p_hvs] = psnrhvsm(img1, img2);
        
 #### See the results:
            
             p_hvs_m  # Gives the PSNR-HVS-M value
             p_hvs    # Gives the PSNR-HVS value

### Descriptions of PSNR-HVS and PSNR-HVS-M are given in following papers:

[1] K. Egiazarian, J. Astola, N. Ponomarenko, V. Lukin, F. Battisti, M. Carli, New full-reference quality metrics based on HVS, CD-ROM Proceedings of the Second International Workshop on Video Processing and Quality Metrics, Scottsdale, USA, 2006, 4 p.

[2] Nikolay Ponomarenko, Flavia Silvestri, Karen Egiazarian, Marco Carli, Jaakko Astola, Vladimir Lukin, On between-coefficient contrast masking of DCT basis functions, CD-ROM Proceedings of the Third International Workshop on Video Processing and Quality Metrics for Consumer Electronics VPQM-07, Scottsdale, Arizona, USA, 25-26 January, 2007, 4 p.
