# Generated with SMOP  0.41
# psnrhvsm.m
import numpy as np
import torch 
import scipy as sp
from scipy.fftpack import dct, dctn, idctn
from skimage.util.shape import view_as_windows, view_as_blocks

def psnrhvsm(img1=None,img2=None,wstep=8,*args,**kwargs):
    varargin = args
    nargin = 2 + len(varargin)
    verbose = True
    p_hvs_m = 0 
    p_hvs = 0
    
    '''
    ========================================================================
        
        Calculation of PSNR-HVS-M and PSNR-HVS image quality measures
        
        PSNR-HVS-M is Peak Signal to Noise Ratio taking into account 
        Contrast Sensitivity Function (CSF) and between-coefficient   
        contrast masking of DCT basis functions
        PSNR-HVS is Peak Signal to Noise Ratio taking into account only CSF
        

        Python 3 port by: Eduardo Prado , 2019  
        
        Homepage: https://t2ac32.wordpress.com/
        E-mail:   eduardo.prado@tum.de

        Original by: 
        Copyright(c) 2006 Nikolay Ponomarenko 
        All Rights Reserved
        
        Homepage: http://ponomarenko.info, E-mail: nikolay{}ponomarenko.info
        
        ----------------------------------------------------------------------
        
        # Permission to use, copy, or modify this software and its documentation
        for educational and research purposes only and without fee is hereby
        granted, provided that this copyright notice and the original authors'
        names appear on all copies and supporting documentation. This program
        shall not be used, rewritten, or adapted as the basis of a commercial
        software or hardware product without first obtaining permission of the
        authors. The authors make no representations about the suitability of
        this software for any purpose. It is provided "as is" without express
         or implied warranty.
        
        #----------------------------------------------------------------------
        
        This is an implementation of the algorithm for calculating the PSNR-HVS-M
        or PSNR-HVS between two images. Please refer to the following papers:
       
       # PSNR-HVS-M:
         [1] Nikolay Ponomarenko, Flavia Silvestri, Karen Egiazarian, Marco Carli, 
             Jaakko Astola, Vladimir Lukin, "On between-coefficient contrast masking 
             of DCT basis functions", CD-ROM Proceedings of the Third International 
             Workshop on Video Processing and Quality Metrics for Consumer Electronics 
             VPQM-07, Scottsdale, Arizona, USA, 25-26 January, 2007, 4 p.
           
           # PSNR-HVS:
         [2] K. Egiazarian, J. Astola, N. Ponomarenko, V. Lukin, F. Battisti, 
             M. Carli, New full-reference quality metrics based on HVS, CD-ROM 
             Proceedings of the Second International Workshop on Video Processing 
             and Quality Metrics, Scottsdale, USA, 2006, 4 p.
       
        Kindly report any suggestions or corrections for its python implementation to: 
        python implementation: eduardo.prado{}tum.de
       
       #----------------------------------------------------------------------
       
       # Input : (1) img1: the first image being compared
                 (2) img2: the second image being compared
                 (3) wstep: step of 8x8 window to calculate DCT 
                     coefficients. Default value is 8.
           
       # Output: (1) p_hvs_m: the PSNR-HVS-M value between 2 images.
                     If one of the images being compared is regarded as 
                     perfect quality, then PSNR-HVS-M can be considered as the
                     quality measure of the other image.
                     If compared images are visually undistingwished, 
                     then PSNR-HVS-M = 100000.
                 (2) p_hvs: the PSNR-HVS value between 2 images.
        
        # Default Usage:
            Given 2 test images img1 and img2, whose dynamic range is 0-255
        
           [p_hvs_m, p_hvs] = psnrhvsm(img1, img2);
        
             See the results:
            
             p_hvs_m  # Gives the PSNR-HVS-M value
             p_hvs    # Gives the PSNR-HVS value
    ========================================================================
    '''  
    if nargin < 2:
        p_hvs_m =- Inf
        p_hvs =- Inf
        return p_hvs_m,p_hvs
    
    if img1.size() != img2.size():
        p_hvs_m=- Inf
        p_hvs=- Inf
        return p_hvs_m,p_hvs
    
    if nargin > 2:
        step=copy(wstep)
    else:
        step=8

    #this is required since was originally intended to use with Pytorch.

    img1= img1.detach().cpu().clone().numpy()[0,:,:]
    img2= img2.detach().cpu().clone().numpy()[0,:,:]
    LenXY= img1.shape
    ( LenX, LenY) = LenXY

    CSFCof=np.array([[1.608443, 2.339554, 2.573509, 1.608443, 1.072295, 0.643377, 0.504610, 0.421887],
                   [2.144591, 2.144591, 1.838221, 1.354478, 0.989811, 0.443708, 0.428918, 0.467911],
                   [1.838221, 1.979622, 1.608443, 1.072295, 0.643377, 0.451493, 0.372972, 0.459555],
                   [1.838221, 1.513829, 1.169777, 0.887417, 0.504610, 0.295806, 0.321689, 0.415082],
                   [1.429727, 1.169777, 0.695543, 0.459555, 0.378457, 0.236102, 0.249855, 0.334222],
                   [1.072295, 0.735288, 0.467911, 0.402111, 0.317717, 0.247453, 0.227744, 0.279729],
                   [0.525206, 0.402111, 0.329937, 0.295806, 0.249855, 0.212687, 0.214459, 0.254803],
                   [0.357432, 0.279729, 0.270896, 0.262603, 0.229778, 0.257351, 0.249855, 0.25995]])
    # see an explanation in [2]
    
    MaskCof=np.array([[0.390625, 0.826446, 1.000000, 0.390625, 0.173611, 0.062500, 0.038447, 0.026874],
                    [0.694444, 0.694444, 0.510204, 0.277008, 0.147929, 0.029727, 0.027778, 0.033058],
                    [0.510204, 0.591716, 0.390625, 0.173611, 0.062500, 0.030779, 0.021004, 0.031888],
                    [0.510204, 0.346021, 0.206612, 0.118906, 0.038447, 0.013212, 0.015625, 0.026015],
                    [0.308642, 0.206612, 0.073046, 0.031888, 0.021626, 0.008417, 0.009426, 0.016866],
                    [0.173611, 0.081633, 0.033058, 0.024414, 0.015242, 0.009246, 0.007831, 0.011815],
                    [0.041649, 0.024414, 0.016437, 0.013212, 0.009426, 0.006830, 0.006944, 0.009803],
                    [0.019290, 0.011815, 0.011080, 0.010412, 0.007972, 0.010000, 0.009426, 0.010203]])
    # see an explanation in [1]
    
    S1=0
    S2=0
    Num=0
    X=0
    Y=0
    window_shape = (8, 8)
    
    A = view_as_blocks(img1, window_shape)
    B = view_as_blocks(img2, window_shape)
    num_patchsA = A.shape[0]
    num_patchsB = B.shape[0]
    for p in range(num_patchsA):
        for py in range(num_patchsB):
    #compute the 2d Discrete Cosine Transform
            patchA = A[p][py]
            patchB = B[p][py]
            '''Thanks to 
            https://www.tu-ilmenau.de/fileadmin/public/mt_ams/GrundlagenDerVideotechnikb/Vorlesung/WS_2017-18/06_16-11-28DCT_-_English.pdf
            that explains how dct work and should be modified for 2d images. 
            '''
            #dct2(A)
            a_dct=dct(patchA,type=2,axis=1,norm='ortho')
            A_dct=dct(a_dct,type=2,axis=0,norm='ortho')
            #dct2(B)
            b_dct=dct(patchB,type=2,axis=1,norm='ortho')
            B_dct=dct(b_dct,type=2,axis=0,norm='ortho')
                    
            MaskA=maskeff(patchA,A_dct)
            MaskB=maskeff(patchB,B_dct)
            
            if MaskB > MaskA:
                MaskA= MaskB.copy()
            for k in range(7):
                for l in range(7):
                    u=abs(A_dct[k,l] - B_dct[k,l])
                    S2=S2 + ((np.dot(u,CSFCof[k,l]))**2) #PSNR-hvs
                    if (k != 1) or (l != 1):
                        if u < MaskA / MaskCof[k,l]:
                            u=0
                        else:
                            u=u - (MaskA / MaskCof[k,l])
                    S1=S1 + ((np.dot(u,CSFCof[k,l]))** 2) # PSNR-HVS-M
                    Num=Num + 1
    
    if Num != 0:
        S1= S1/Num
        S2= S2/Num
        if S1 == 0:
            p_hvs_m=100000
            #print("p_hvs_m=100000")
        else:
            p_hvs_m= 10*(np.log10(255*(255/ S1)))
            #print('p_hvs_m: {:.0f}'.format(p_hvs_m))
        if S2 == 0:
            #print("p_hvs=100000")
            p_hvs=100000
        else:
            p_hvs= 10*(np.log10(255*(255 / S2)))
            #print('p_hvs: {:.0f}'.format(p_hvs))
    #print('returned on end of loop')  
        
    #print('p_hvs_m: {:.0f} dB'.format(p_hvs_m))
    #print('p_hvs: {:.0f} dB'.format(p_hvs))

    return p_hvs_m, p_hvs
    
    
def maskeff(z=None,zdct=None,*args,**kwargs):
    varargin = args
    nargin = 2 + len(varargin)
    
    # Calculation of Enorm value (see [1])
    m=0
    MaskCof=np.array([[0.390625, 0.826446, 1.000000, 0.390625, 0.173611, 0.062500, 0.038447, 0.026874],
                    [0.694444, 0.694444, 0.510204, 0.277008, 0.147929, 0.029727, 0.027778, 0.033058],
                    [0.510204, 0.591716, 0.390625, 0.173611, 0.062500, 0.030779, 0.021004, 0.031888],
                    [0.510204, 0.346021, 0.206612, 0.118906, 0.038447, 0.013212, 0.015625, 0.026015],
                    [0.308642, 0.206612, 0.073046, 0.031888, 0.021626, 0.008417, 0.009426, 0.016866],
                    [0.173611, 0.081633, 0.033058, 0.024414, 0.015242, 0.009246, 0.007831, 0.011815],
                    [0.041649, 0.024414, 0.016437, 0.013212, 0.009426, 0.006830, 0.006944, 0.009803],
                    [0.01929, 0.0118150, 0.011080, 0.010412, 0.007972, 0.010000, 0.009426, 0.010203]])
    # see an explanation in [1]
    
    for k in range(7):
        for l in range(7):
            if (k != 1) or (l != 1):
                m=m + np.dot((zdct[k,l] ** 2),MaskCof[k,l])
    
    pop=vari(z)
    #print('pop: ', pop)
    #print('z shape:', z.shape)
    if pop != 0:
        block1 = vari(z[0:3, 0:3])
        block2 = vari(z[0:3, 4:7])
        block3 = vari(z[4:7, 4:7])
        block4 = vari(z[4:7, 0:3])
        '''
        print('block1', block1.shape)
        print('block1', block2.shape)
        print('block1', block3.shape)
        print('block1', block4.shape)
        '''
        pop=(block1 + block2 + block3 + block4 ) / pop
    
    m=np.sqrt(np.dot(m,pop)) / 32

    return m
    
def vari(AA=None,*args,**kwargs):
    varargin = args
    nargin = 1 + len(varargin)
    flat = AA.flatten(1)
    varia = np.var(flat)
    #flat_sz = np.size(flat)
    
    #print(flat)
    #print(varia)
    #print(flat_sz)
    d=np.dot(varia, flat.size)
    return d


def print_v(message='', verbose =False):
    if verbose == True:
        print(message)