#!/usr/bin/env python
""" This is the library for all gcode lookups. Consider this the local reference database or dictionary.
"""
__author__ = "Jacob Goldman"
__copyright__ = "Copyright 2020, Ahead Wind"
__credits__ = "[]"

__license__ = "NO LICENSE THIS CODE IS NOT FOR DISTRIBUTION - CONFIDENTIAL"
__version__ = "0.1.0"
__maintainer__ = "Jacob Goldman"
__email__ = "jacobgoldman@aheadwind.com"
__status__ = "Development"

__all__ = [] # exported function and variables

from os import path

def display_title_bar():
    print('------------------------------------------------------')
    print('*** This program slows down a region of your print ***')
    print('------------------------------------------------------\n\n')
    print('Make sure you sliced your file with absolute coordinates and without sticky parameters')
    
def display_ending_message(status,input_file_name,output_file_name):
    if status: success = "successfully"
    else: status = "failed"
    print(f'Your file \"{input_file_name}\" has been {status} adjusted into {output_file_name}\n\n')
    
    print('*******')
    print('\nDo you want to convert another profile?')
    another = input('Type \"Y\" or \"y\" if yes. otherwise press any key\n\t')
    another = another.lower()
    print('\n\n-------------------------------------------------------\n-------------------------------------------------------\n')
    return another
    
def get_gcode_file_name():
    print('Put your desired gcode file into the \"input_files\" folder')
    input('Then press enter')
    
    infile_name = input('\n\nType the EXACT name of your gcode file excluding \".gcode\"\n\t')
  
    return infile_name

def get_io_paths():
    infile_name = get_gcode_file_name()
    inpath = path.join('input_files',infile_name + '.gcode')

    while not path.exists(inpath):
        print(f'\nERROR :: your file \"{inpath}\" does not exist\n')
        print('-------------------------------------------------------')
        
        infile_name = get_gcode_file_name()
        inpath = path.join('profiles',infile_name)
    
    outfile_name = infile_name + 'adjusted.gcode'
    outpath = path.join('output_files',outfile_name)
    
    return [inpath,outpath]
    
def get_xyz_values():
    # [0] : x_min
    # [1] : x_max
    # [2] : y_min
    # [3] : y_max
    # [4] : z_min
    # [5] : z_max
    
    minmax_array = ['','','','','','']
    
        
    print('-------------------------------------------------------')
    print('The X, Y, & Z minimum and maximum values are used to define the region you want to slow as a cube')
    print('\t if you want the region to be unbounded (go to edge of printer), please enter \"-1\"')
    minmax_array[0] = input('X Minimum: ')
    while minmax_array[0] == '':
        minmax_array[0] = input('please reenter X Minimum as a number')
    minmax_array[1] = input('X Maximum: ')
    while minmax_array[1] == '':
        minmax_array[1] = input('please reenter X Maximum as a number')
    minmax_array[2] = input('Y Minimum: ')
    while minmax_array[2] == '':
        minmax_array[2] = input('please reenter Y Minimum as a number')
    minmax_array[3] = input('Y Maximum: ')
    while minmax_array[3] == '':
        minmax_array[3] = input('please reenter Y Maximum as a number')
    minmax_array[4] = input('Z Minimum: ')
    while minmax_array[4] == '':
        minmax_array[4] = input('please reenter Z Minimum as a number')
    minmax_array[5] = input('Z Maximum: ')
    while minmax_array[5] == '':
        minmax_array[5] = input('please reenter Z Maximum as a number')
    
    for index in range(len(minmax_array)):
        minmax_array[index] = float(minmax_array[index])
        
    return minmax_array
      
def get_speed_multiplier():
    print('-------------------------------------------------------')
    print('The speed multiplier will be used to direclty adjust your print speed.')
    print('This works in the same way as adjusting the print speed on a gcode sender or on the printer\n')
    multiplier = input('Please enter your print speed multiplier, then press enter.\n\t')
    while multiplier == '':
        print('Please reenter your print speed multiplier as a number')
        multiplier = input('Then press enter.')
    
    return float(multiplier)

def adjust_gcode_print(io_paths,regions,speed_multiplier):
    with open(io_paths[0],'r') as input, open(io_paths[1],'w') as output:
        x = None
        y = None
        z = None
        
        for line in input:
            # if its a movement command
            line.replace('\n','').replace('\r','')
            line_array = line.split(' ')
            if line_array[0].find('G1') != -1:
                # grab xyz values   
                for elem in line_array[1:]:
                    if elem.find('X') != -1:
                        x = float(elem[1:])
                    elif elem.find('Y') != -1:
                        y = float(elem[1:])
                    elif elem.find('Z') != -1:
                        z = float(elem[1:])
        
            # if the current position is within the defined region
            if (x is None) or (y is None) or (z is None):
                pass
            elif (regions[0] <= x <= regions[1]) and (regions[2] <= y <= regions[3]) and (regions[4] <= z <= regions[5]):
                # find the F value and change it
                for i in range(len(line_array)):
                    index = line_array[i].find('F')
                    if index != -1:
                        current_value = float(line_array[i][1:])
                        updated_value = int(current_value * speed_multiplier)
                        line_array[i] = 'F'+ str(updated_value)
                        line = ' '.join(line_array)
                        line += '\n'
            
            output.write(line)
            
            

if __name__ == "__main__":
    # if a min or max is missing, just consider it [value,infinity)
    display_title_bar()
    another = True
    while another:
        io_paths = get_io_paths()   # [0] is input [1] is output
        # regions = get_xyz_values()  # x_min,x_max,y_min,y_max,z_min,z_max
        # speed_multiplier = get_speed_multiplier()
        
        regions = ['150', '167.58', '0', '150', '1', '34.38']
        for index in range(len(regions)):
            regions[index] = float(regions[index])
        speed_multiplier = 0.5
        adjust_gcode_print(io_paths,regions,speed_multiplier)
        
        another = display_ending_message(True,io_paths[0],io_paths[1])
    
    