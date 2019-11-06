function [p_hvs_m, p_hvs] = psnrhvsm(img1, img2, wstep)

%========================================================================
%
% Calculation of PSNR-HVS-M and PSNR-HVS image quality measures
%
% PSNR-HVS-M is Peak Signal to Noise Ratio taking into account 
% Contrast Sensitivity Function (CSF) and between-coefficient   
% contrast masking of DCT basis functions
% PSNR-HVS is Peak Signal to Noise Ratio taking into account only CSF 
%
% Copyright(c) 2006 Nikolay Ponomarenko 
% All Rights Reserved
%
% Homepage: http://ponomarenko.info, E-mail: nikolay{}ponomarenko.info
%
%----------------------------------------------------------------------
%
% Permission to use, copy, or modify this software and its documentation
% for educational and research purposes only and without fee is hereby
% granted, provided that this copyright notice and the original authors'
% names appear on all copies and supporting documentation. This program
% shall not be used, rewritten, or adapted as the basis of a commercial
% software or hardware product without first obtaining permission of the
% authors. The authors make no representations about the suitability of
% this software for any purpose. It is provided "as is" without express
% or implied warranty.
%
%----------------------------------------------------------------------
%
% This is an implementation of the algorithm for calculating the PSNR-HVS-M
% or PSNR-HVS between two images. Please refer to the following papers:
%
% PSNR-HVS-M:
% [1] Nikolay Ponomarenko, Flavia Silvestri, Karen Egiazarian, Marco Carli, 
%     Jaakko Astola, Vladimir Lukin, "On between-coefficient contrast masking 
%     of DCT basis functions", CD-ROM Proceedings of the Third International 
%     Workshop on Video Processing and Quality Metrics for Consumer Electronics 
%     VPQM-07, Scottsdale, Arizona, USA, 25-26 January, 2007, 4 p.
%
% PSNR-HVS:
% [2] K. Egiazarian, J. Astola, N. Ponomarenko, V. Lukin, F. Battisti, 
%     M. Carli, New full-reference quality metrics based on HVS, CD-ROM 
%     Proceedings of the Second International Workshop on Video Processing 
%     and Quality Metrics, Scottsdale, USA, 2006, 4 p.
%
% Kindly report any suggestions or corrections to uagames{}mail.ru
%
%----------------------------------------------------------------------
%
% Input : (1) img1: the first image being compared
%         (2) img2: the second image being compared
%         (3) wstep: step of 8x8 window to calculate DCT 
%             coefficients. Default value is 8.
%
% Output: (1) p_hvs_m: the PSNR-HVS-M value between 2 images.
%             If one of the images being compared is regarded as 
%             perfect quality, then PSNR-HVS-M can be considered as the
%             quality measure of the other image.
%             If compared images are visually undistingwished, 
%             then PSNR-HVS-M = 100000.
%         (2) p_hvs: the PSNR-HVS value between 2 images.
%
% Default Usage:
%   Given 2 test images img1 and img2, whose dynamic range is 0-255
%
%   [p_hvs_m, p_hvs] = psnrhvsm(img1, img2);
%
% See the results:
%
%   p_hvs_m  % Gives the PSNR-HVS-M value
%   p_hvs    % Gives the PSNR-HVS value
%
%========================================================================

if nargin < 2
  p_hvs_m = -Inf;
  p_hvs = -Inf;
  return;
end

if size(img1) ~= size(img2)
  p_hvs_m = -Inf;
  p_hvs = -Inf;
  return;
end

if nargin > 2 
  step = wstep;
else
  step = 8; % Default value is 8;
end

img1=double(img1);
img2=double(img2);

LenXY=size(img1);LenY=LenXY(1);LenX=LenXY(2);

CSFCof  = [1.608443, 2.339554, 2.573509, 1.608443, 1.072295, 0.643377, 0.504610, 0.421887;
           2.144591, 2.144591, 1.838221, 1.354478, 0.989811, 0.443708, 0.428918, 0.467911;
           1.838221, 1.979622, 1.608443, 1.072295, 0.643377, 0.451493, 0.372972, 0.459555;
           1.838221, 1.513829, 1.169777, 0.887417, 0.504610, 0.295806, 0.321689, 0.415082;
           1.429727, 1.169777, 0.695543, 0.459555, 0.378457, 0.236102, 0.249855, 0.334222;
           1.072295, 0.735288, 0.467911, 0.402111, 0.317717, 0.247453, 0.227744, 0.279729;
           0.525206, 0.402111, 0.329937, 0.295806, 0.249855, 0.212687, 0.214459, 0.254803;
           0.357432, 0.279729, 0.270896, 0.262603, 0.229778, 0.257351, 0.249855, 0.259950];
% see an explanation in [2]

MaskCof = [0.390625, 0.826446, 1.000000, 0.390625, 0.173611, 0.062500, 0.038447, 0.026874;
           0.694444, 0.694444, 0.510204, 0.277008, 0.147929, 0.029727, 0.027778, 0.033058;
           0.510204, 0.591716, 0.390625, 0.173611, 0.062500, 0.030779, 0.021004, 0.031888;
           0.510204, 0.346021, 0.206612, 0.118906, 0.038447, 0.013212, 0.015625, 0.026015;
           0.308642, 0.206612, 0.073046, 0.031888, 0.021626, 0.008417, 0.009426, 0.016866;
           0.173611, 0.081633, 0.033058, 0.024414, 0.015242, 0.009246, 0.007831, 0.011815;
           0.041649, 0.024414, 0.016437, 0.013212, 0.009426, 0.006830, 0.006944, 0.009803;
           0.019290, 0.011815, 0.011080, 0.010412, 0.007972, 0.010000, 0.009426, 0.010203];
% see an explanation in [1]

S1 = 0; S2 = 0; Num = 0;
X=1;Y=1;
while Y <= LenY-7
  while X <= LenX-7 
    A = img1(Y:Y+7,X:X+7);
    B = img2(Y:Y+7,X:X+7);
    A_dct = dct2(A); B_dct = dct2(B);
    MaskA = maskeff(A,A_dct);
    MaskB = maskeff(B,B_dct);
    if MaskB > MaskA
      MaskA = MaskB;
    end
    X = X + step;
    for k = 1:8
      for l = 1:8
        u = abs(A_dct(k,l)-B_dct(k,l));
        S2 = S2 + (u*CSFCof(k,l)).^2;    % PSNR-HVS
        if (k~=1) | (l~=1)               % See equation 3 in [1]
          if u < MaskA/MaskCof(k,l) 
            u = 0;
          else
            u = u - MaskA/MaskCof(k,l);
          end
        end
        S1 = S1 + (u*CSFCof(k,l)).^2;    % PSNR-HVS-M
        Num = Num + 1;
      end
    end
  end
  X = 1; Y = Y + step;
end

if Num ~=0
  S1 = S1/Num;S2 = S2/Num;
  if S1 == 0 
    p_hvs_m = 100000; % img1 and img2 are visually undistingwished
  else
    p_hvs_m = 10*log10(255*255/S1);
  end
  if S2 == 0  
    p_hvs = 100000; % img1 and img2 are identical
  else
    p_hvs = 10*log10(255*255/S2);
  end
end

function m=maskeff(z,zdct)  
% Calculation of Enorm value (see [1])
m = 0;

MaskCof = [0.390625, 0.826446, 1.000000, 0.390625, 0.173611, 0.062500, 0.038447, 0.026874;
           0.694444, 0.694444, 0.510204, 0.277008, 0.147929, 0.029727, 0.027778, 0.033058;
           0.510204, 0.591716, 0.390625, 0.173611, 0.062500, 0.030779, 0.021004, 0.031888;
           0.510204, 0.346021, 0.206612, 0.118906, 0.038447, 0.013212, 0.015625, 0.026015;
           0.308642, 0.206612, 0.073046, 0.031888, 0.021626, 0.008417, 0.009426, 0.016866;
           0.173611, 0.081633, 0.033058, 0.024414, 0.015242, 0.009246, 0.007831, 0.011815;
           0.041649, 0.024414, 0.016437, 0.013212, 0.009426, 0.006830, 0.006944, 0.009803;
           0.019290, 0.011815, 0.011080, 0.010412, 0.007972, 0.010000, 0.009426, 0.010203];
% see an explanation in [1]

for k = 1:8
  for l = 1:8
    if (k~=1) | (l~=1)
      m = m + (zdct(k,l).^2) * MaskCof(k,l);
    end
  end
end
pop=vari(z);
if pop ~= 0
  pop=(vari(z(1:4,1:4))+vari(z(1:4,5:8))+vari(z(5:8,5:8))+vari(z(5:8,1:4)))/pop;
end
m = sqrt(m*pop)/32;   % sqrt(m*pop/16/64)

function d=vari(AA)
  d=var( AA(:) ) * length( AA(:) );
