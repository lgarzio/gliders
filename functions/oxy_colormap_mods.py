import cmocean
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

"""
Author: Laura Nazzaro on 10/24/2023
Last modified: 10/24/2023
Functions to modify colormaps with defined breakpoints.
Mostly for oxygen, but who knows where this will take us.
Individual colors can be removed from any version

cm_oxy_mod: original cmocean colormap red to gray to yellow
cm_rygg: red to yellow to gray to green
cm_rogg: red to orange to gray to green (gray shading reversed from original oxy)
cm_partialturbo_r: red to orange/yellow to gray to blue

Based on our best research (Fed and NJ) so far, 
and concentration/saturation equivalents based on summer 2023 ru28 and ru40 deployments
(concentration to saturation conversions are variable so these should be used with a grain of salt):

hypoxia = < 3 mg/L, = 93.75 umol/L, approx = 40% saturation
low DO = < 5 mg/L, = 156.25 umol/L, approx = 65% saturation
supersaturation = > 100% saturation, approx = 7.5 mg/L, = 234.375
"""

def cm_oxy_mod(vmin=2, vmax=9, breaks=[3,7.5], red=True, gray=True, yellow=True):
    """
    Modify cmocean oxy colormap with defined break points
    red (dark to less dark) to gray (dark to light) to yellow (light to dark-ish)
    """
    all_nums = np.append(np.append(vmin,breaks),vmax)
    # check that all values are real numbers
    if not np.all(np.isreal(all_nums)) or np.any(np.isnan(all_nums)):
        print('All values must be real numbers.')
        return 0
    # check that all values increase in the right order
    if np.any(np.diff(all_nums)<0):
        print('All values must be increasing from vmin -> breaks -> vmax')
        return 0
    # check that number of break values works with number of colors
    if red+gray+yellow != len(breaks)+1:
        print(f'Number of breakpoints ({len(breaks)}) must be one less than number of colors ({red+gray+yellow})')
        return 0
    # define interval
    ni = (vmax-vmin)/100
    
    b=1
    if red:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(0,.19,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if gray:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(.2,.79,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if yellow:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(.8,1,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    newmap = mcolors.LinearSegmentedColormap.from_list('my_colormap',cmfull)
    return newmap


def cm_rygg(vmin=2, vmax=9, breaks=[3,5,7.5], red=True, yellow=True, gray=True, green=True):
    """
    Modify cmocean oxy colormap with defined break points
    red (dark to less dark) to yellow (light to dark-ish)to gray (dark to light) to green (light to mid)
    """
    all_nums = np.append(np.append(vmin,breaks),vmax)
    # check that all values are real numbers
    if not np.all(np.isreal(all_nums)) or np.any(np.isnan(all_nums)):
        print('All values must be real numbers.')
        return 0
    # check that all values increase in the right order
    if np.any(np.diff(all_nums)<0):
        print('All values must be increasing from vmin -> breaks -> vmax')
        return 0
    # check that number of break values works with number of colors
    if red+yellow+gray+green != len(breaks)+1:
        print(f'Number of breakpoints ({len(breaks)}) must be one less than number of colors ({red+yellow+gray+green})')
        return 0
    # define interval
    ni = (vmax-vmin)/100
    
    b=1
    if red:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(0,.19,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if yellow:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(.8,1,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if gray:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(.2,.79,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if green:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.algae(np.linspace(0,.5,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    
    newmap = mcolors.LinearSegmentedColormap.from_list('my_colormap',cmfull)
    return newmap

def cm_rogg(vmin=2, vmax=9, breaks=[3,5,7.5], red=True, orange=True, gray=True, green=True):
    """
    Modify cmocean oxy colormap with defined break points
    red (dark to less dark) to orange (dark-ish to light)to gray (light to dark) to green (mid to light)
    """
    all_nums = np.append(np.append(vmin,breaks),vmax)
    # check that all values are real numbers
    if not np.all(np.isreal(all_nums)) or np.any(np.isnan(all_nums)):
        print('All values must be real numbers.')
        return 0
    # check that all values increase in the right order
    if np.any(np.diff(all_nums)<0):
        print('All values must be increasing from vmin -> breaks -> vmax')
        return 0
    # check that number of break values works with number of colors
    if red+orange+gray+green != len(breaks)+1:
        print(f'Number of breakpoints ({len(breaks)}) must be one less than number of colors ({red+orange+gray+green})')
        return 0
    # define interval
    ni = (vmax-vmin)/100
    
    b=1
    if red:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(0,.19,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if orange:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = plt.cm.Oranges(np.linspace(.8,.4,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if gray:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(.7,.2,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if green:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = plt.cm.Oranges(np.linspace(.8,.4,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    
    newmap = mcolors.LinearSegmentedColormap.from_list('my_colormap',cmfull)
    return newmap

def cm_partialturbo_r(vmin=2, vmax=9, breaks=[3,5,7.5], red=True, orange=True, gray=True, blue=True):
    """
    Modify cmocean oxy colormap with defined break points
    red (dark to bright) to orange/yellow (orangey orange to orangey yellow)to gray (dark to light) to blue (cyan to bright)
    """
    all_nums = np.append(np.append(vmin,breaks),vmax)
    # check that all values are real numbers
    if not np.all(np.isreal(all_nums)) or np.any(np.isnan(all_nums)):
        print('All values must be real numbers.')
        return 0
    # check that all values increase in the right order
    if np.any(np.diff(all_nums)<0):
        print('All values must be increasing from vmin -> breaks -> vmax')
        return 0
    # check that number of break values works with number of colors
    if red+orange+gray+blue != len(breaks)+1:
        print(f'Number of breakpoints ({len(breaks)}) must be one less than number of colors ({red+orange+gray+blue})')
        return 0
    # define interval
    ni = (vmax-vmin)/100
    
    b=1
    if red:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = plt.cm.turbo(np.linspace(1,.85,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if orange:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = plt.cm.turbo(np.linspace(.75,.6,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if gray:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = cmocean.cm.oxy(np.linspace(.3,.79,nints))  #cm0 = plt.cm.binary(np.linspace(.8,.3,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    if blue:
        nints = int(np.floor((all_nums[b]-all_nums[b-1])/ni))
        cm0 = plt.cm.turbo(np.linspace(.3,.1,nints))
        if b==1:
            cmfull = cm0
        else:
            cmfull = np.vstack((cmfull,cm0))
        b+=1
    
    newmap = mcolors.LinearSegmentedColormap.from_list('my_colormap',cmfull)
    return newmap