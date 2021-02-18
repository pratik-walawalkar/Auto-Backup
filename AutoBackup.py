#!/usr/bin/env python
# =============================================================================

# This script is written to copy files from a source folder to destination folder
# It can be used to copy large number of files from mobile or other devices
# It can be further programmed to backup mobile data automatically when 
# connected to the computer

# Created on Tue Feb 16 07:46:46 2021

# @author: Pratik Walawalkar

# =============================================================================


import os
import time
import curses
import shutil
from datetime import datetime
import sys

files_copied = 0
total_files_scanned = 1
action = ''
t0_start = time.time()
now = datetime.now()


def main():
    '''
    # files_skipped - stores the no. of files that already exist
    # total_files   - total no. of files in source folder
    loop - condition for while loop
    '''
    global total_files, files_skipped, sourcePath, dir_select, no_of_files_to_be_copied
    
    #input source and destination path      

    select_dir()

    #check if source and destination is not the same
    if sourcePath is not destPath:
        
        print("\nSearchning for new files...")
        print("Please wait...")
        
        #Find total no. of files in the source directory
        total_files = sum(len(files) for path, directory, files in os.walk(os.path.join(sourcePath)))
        
        #iterate through destination and source folder
        files_in_dst(destPath)
        files_to_copy(sourcePath)
        
        print("Found " + str(no_of_files_to_be_copied) + " files to be copied\n")
        
        files_skipped = total_files - no_of_files_to_be_copied
        
        #while loop to decide the ececution of copy_files command
        loop = True
        while loop == True:
            cmd = input("Press 'Y' to proceed and 'N' to abort: ").lower()
            if cmd == 'y':
                try:
                    copy_files(files_to_be_copied)
                except:
                    no_of_files_to_be_copied = files_copied
                    update_log()
                
                curses.initscr().getch()
                loop = False
            elif cmd == 'n':
                print("The process was aborted by the user!!") 
                loop = False
            else:    
                print("Please enter a valid input")
                loop = True
                
    elif sourcePath is destPath:
        print("The source and destination path you entered is same...")

def select_dir():
    '''
    Description
    -----------
    Select source and destination directory    

    Returns
    -------
    None.

    '''
    global sourcePath, destPath
    loop = True
    #loop until a valid path is selected 
    dir_select = input("Do you want to proceed with the saved source and destination?\nPress 1 to proceed \nPress 2 to enter new source and destination \nPress 3 for wireless mobile phone backup \nInput: ")

    while loop == True:
        
        if dir_select == "1":           
            sourcePath = "D:\\Users\\Pratik\\OneDrive - stud.th-deg.de\\Documents\\GitHub\\Auto-Backup\\Test\\source" 
            destPath = "D:\\Users\\Pratik\\OneDrive - stud.th-deg.de\\Documents\\GitHub\\Auto-Backup\\Test\\destination"
            loop = False 
            
        elif dir_select == "2":
            sourcePath = check_path(input("\nEnter the source folder: "))        
            destPath = check_path(input("Enter the destination folder: ")) 
            loop = False
            
        elif dir_select == "3":
            sourcePath = "Z:\\"
            check_device() #select destination from the saved directory 
            loop = False
            
        else:
            print("Please enter a valid input!", end = "\r")

def check_device():
    '''
    Description
    -------
    Searches for _device_info.txt in the source folder to find the name of the device 

    Returns
    -------
    None.

    '''
    global destPath
    
    deviceInfo = os.path.join(sourcePath, "_device_info.txt")
    
    if os.path.exists(deviceInfo):
        with open(deviceInfo, 'r') as file:
            for line in file:
                deviceName = line.strip()

            if deviceName.lower() == "oneplus7":
                #your desired destination path for this device
                destPath = "D:\\Users\\Pratik\\OneDrive - stud.th-deg.de\\Pictures\\OnePlus 7\\"
            elif deviceName.lower() == "redminote4":
                #your desired destination path for this device
                destPath = "D:\\Users\\Pratik\\OneDrive - stud.th-deg.de\\Pictures\\OnePlus 7\\"
            elif deviceName.lower() == "redminote5pro":
                #your desired destination path for this device
                destPath = "D:\\Users\\Pratik\\OneDrive - stud.th-deg.de\\Pictures\\OnePlus 7\\" 
            elif deviceName.lower() == "oppof1s":
                #your desired destination path for this device
                destPath = "D:\\Users\\Pratik\\OneDrive - stud.th-deg.de\\Pictures\\OnePlus 7\\"
            elif deviceName.lower() == "samsungm31":
                #your desired destination path for this device
                destPath = "D:\\Users\\Pratik\\OneDrive - stud.th-deg.de\\Pictures\\OnePlus 7\\"                  
            else:
                print("Device name did not match the saved device name")
    else:
        print("Device verification file (_device_info.txt) not found at {}". format(sourcePath))
        print("\nTerminating the program!")
        terminate()
        
def check_path(path): 
    '''
    Description
    ----------
    check if the entered path is a valid directory     

    Parameters
    ----------
    path : TYPE
        DESCRIPTION.

    Returns
    -------
    path : TYPE
        DESCRIPTION.

    '''
    loop = True
    #loop until a valid path is entered
    while loop == True: 
        if not os.path.isdir(path):
            path = input("Please enter a valid path!!\n")
            loop == True
        else:
            return path            
            
def files_in_dst(destPath):
    '''
    Description
    ----------
    find the list of files in destination folder
    
    Parameters
    ----------
    destPath            : TYPE - string.

    Returns
    -------
    dst                 : TYPE - string.
    files_in_dest       : TYPE - list.
    no_of_files_in_dest : TYPE - int.
    
    Variables
    -------
    dst : destination file path - destPath
    files_in_dest - list of files in destination folder
    no_of_files_in_dest : no. of files in destination folder
    '''
    global dst, files_in_dest, no_of_files_in_dest
    files_in_dest = list()   
    
    for (dirpath, dirnames, filenames) in os.walk(destPath):
            #removes destPath from dirPath to get a path within the destination directory to compare with source directory
            dst = dirpath.replace(destPath,"")
            files_in_dest += [ os.path.join(dst, file) for file in filenames]
    no_of_files_in_dest = len(files_in_dest)
    print("Found {} files in the destination folder". format(no_of_files_in_dest))
    return dst, files_in_dest, no_of_files_in_dest

def files_to_copy(sourcePath):
    '''
    Description
    ----------
    iterates through source folder to find unique files to be copied to the destination    
    
    Parameters
    ----------
    sourcePath               : TYPE - string

    Returns
    -------
    src                      : TYPE - string
    files_to_be_copied       : TYPE - list
    no_of_files_to_be_copied : TYPE - int
    size_files_to_be_copied  : TYPE - float
    
    Variables
    -------
    src = source file path - the sourcePath
    files_to_be_copied = list of new files to be copied
    no_of_files_to_be_copied = number of files to be copied
    size_files_to_be_copied = size of files to be copied
    '''    
    global src, files_to_be_copied, no_of_files_to_be_copied, size_files_to_be_copied
         
    files_to_be_copied = list()
    size_files_to_be_copied = 0
    
    #Add unique/new files in source folder to a  list of files to be copied
    for (dirpath, dirnames, filenames) in os.walk(sourcePath):
        #removes the sourcePath from dirPath to compare the file path with destination 
        #to check if the same file exists in the destination at the same location
        src = dirpath.replace(sourcePath,"")
        files_to_be_copied += [ os.path.join(src, file) for file in filenames if os.path.join(src, file) not in files_in_dest]
        
    size_files_to_be_copied = round(sum(os.path.getsize(os.path.join(sourcePath, file.strip("\\"))) for file in files_to_be_copied)/(1024*1024.0), 4)
    
    no_of_files_to_be_copied = len(files_to_be_copied)
    print("Found {} unique files to copy.".format(no_of_files_to_be_copied))
    return files_to_be_copied, no_of_files_to_be_copied, size_files_to_be_copied
    
def file_size(list_of_files):
    '''
    Description
    ----------
    calculates the sum of files size in a list
    
    Parameters
    ----------
    list_of_files : TYPE - list

    Returns
    -------
    size          : TYPE - float

    Variables
    -------
    size - calculates size of a file
    '''
    global size
    size = 0
    size = sum(os.path.getsize(file) for file in list_of_files)
    
    return round(size/(1024*1024.0), 4)  

def status(filename):
    '''
    Description
    ----------
    designs user interface and displays different stats.
    
    Parameters
    ----------
    filename : TYPE - string

    Returns
    -------
    None.
    
    Variables
    -------
    '''
    global interrupt
    
    curses.initscr().clear()
    curses.initscr().addstr(0, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(1, 0,"File's copied                                      :" + str(files_copied) + " files / " + str(file_size(list_of_copied_files)) +" MB")
    curses.initscr().addstr(2, 0,"Files already exist at destination                 :" + str(files_skipped))
    curses.initscr().addstr(3, 0,"Total file's to be copied                          :" + str(no_of_files_to_be_copied) +" files / "+ str(size_files_to_be_copied) +" MB")
    curses.initscr().addstr(4, 0,"Total file's in the Source Directory               :" + str(total_files))
    curses.initscr().addstr(5, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(6, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(7, 0,'Copying files from : ...' + src.replace(os.path.dirname(sourcePath),""))
    curses.initscr().addstr(8, 0,'Copying files to : ...' + dst.replace(os.path.dirname(destPath),""))
    curses.initscr().addstr(9, 0,"")
    curses.initscr().addstr(10, 0,">>> " + str(action))
    curses.initscr().addstr(11, 0,"------------------------------------------------------------------------------")

    curses.initscr().addstr(13, 0,str(progressBar(files_copied, no_of_files_to_be_copied)))
    
    curses.initscr().addstr(15, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(16, 0,"Time elapsed = " + str(time_conversion(time_elapsed())))
    curses.initscr().addstr(17, 0,"Estimated time left = " + str(time_conversion(time_left())))
    curses.initscr().addstr(18, 0,"------------------------------------------------------------------------------")    
    curses.initscr().addstr(19, 0,"")  

def copy_files(files_to_be_copied):
    
    '''
    Description
    ----------
    main block to copy frile from source to destination folder
    
    Parameters
    ----------
    files_to_be_copied : TYPE - list

    Returns
    -------
    None.
    
    Variables
    -------
    src - complete source file path
    dst - complete destination path
    directory - complete directory path
    files_copied - counts the no. of files copied
    action - stores a string which denotes which file has been copied
    list_of_copied_files - stores list of copied files
    '''
    
    global files_copied, directory, action
    global list_of_copied_files, src, dst
    
    list_of_copied_files = list()
    

    
    for file in files_to_be_copied:
    
        
        #removes \\ from the file path to join as a valid path
        src = os.path.join(sourcePath, file.strip("\\"))
        dst = os.path.join(destPath, file.strip("\\"))
        
        #saves name of the directory
        directory = os.path.dirname(dst)
        
        #make directory trees
        os.makedirs(directory, exist_ok=True)
        #copies file from source to destination
        shutil.copy2(src, dst)    
        
        #creates a list of copied files
        list_of_copied_files.append(dst)
        files_copied += 1
              
        action = "Copied: {}" .format(os.path.basename(file))
        update_log()
        status(file)
        

    else:
        action = "No new files to be copied"

def terminate():
    sys.exit()

def update_log():
    '''
    Description
    -------
    Creates a folder and saves the log file in it

    Returns
    -------
    None.

    '''
    backup_log = os.path.join(destPath, "_backup_log")
    
    if not os.path.exists(backup_log):
        os.mkdir(backup_log)
        
    with open(os.path.join(backup_log, "Backup_log_{}.txt".format(now.strftime("%Y%m%d_%H%M%S"))), 'a') as textFile:
    
        if files_copied <= no_of_files_to_be_copied:
            
            if files_copied == 1:
                textFile.write("*****************************************************************************\n\n")
                textFile.write("Found " + str(no_of_files_to_be_copied) + " unique files to be copied - " + str(size_files_to_be_copied) + " MB\n")
                textFile.write("Start time: " + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "\n\n")
                textFile.write("*****************************************************************************\n\n")
                
            textFile.write(" Copied -  "+ str(dst) + "\n")
            
            if files_copied == no_of_files_to_be_copied:
    
                textFile.write("\n*****************************************************************************\n\n")
                textFile.write(now.strftime("%d/%m/%Y %H:%M:%S") + ' - Backed up '+ str(files_copied) + ' files' + "(" + str(file_size(list_of_copied_files)) + " MB)\n")
                textFile.write("Total time taken: " + str(time_conversion(time_elapsed())) + "\n\n")
                textFile.write("*****************************************************************************\n\n")
            
def time_conversion(time):
    '''
    Description
    ----------
    convert seconds to hh mm ss format

    Parameters
    ----------
    time : TYPE - int(sec)

    Returns
    -------
    time : TYPE - string(hh mm ss)
    
    Convert time to hh mm ss format
    
    Variables
    -------
    hours - hours
    rem - remainder after calculation
    minutes - minutes
    seconds - seconds
    '''

    if time == "Completed!!!":
        return time
    else:
        hours, rem = divmod(time, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}h {:0>2}m {:0>2}s".format(int(hours), int(minutes), int(seconds))
    
def time_elapsed():
    '''
    Description
    ----------
    Calculate time elapsed since initiating the code
    Variables
    -------
    time_elapsed - calculates the time elapsed since the process started
    '''
    
    time_elapsed = (time.time() - t0_start)     #Difference between the program execution end and start time
    return time_elapsed        
        
def time_left():
    '''
    Description
    ----------
    Calculate the difference between the approximate time left to complete the process
    
    Variables
    -------
    time_left - calculates the approximate process completion time
    '''
    
    if file_size(list_of_copied_files) > 0:
        
        time_left = (((size_files_to_be_copied - file_size(list_of_copied_files)) * time_elapsed())/(file_size(list_of_copied_files)))
        
        if time_left <= 0:
            return ("Completed!!!")
        else:
            return time_left 
        
    else:
        return 0
        
def progressBar(files_copied, no_of_files_to_be_copied, decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    '''
    Description
    ----------
    Block of code which designs and updates the process bar
    
    Parameters
    ----------
    files_copied : TYPE - int
    no_of_files_to_be_copied : TYPE - int
    decimals : TYPE, optional
        DESCRIPTION. The default is 1.
    length : TYPE, optional
        DESCRIPTION. The default is 50.
    fill : TYPE, optional
        DESCRIPTION. The default is '█'.
    printEnd : TYPE, optional
        DESCRIPTION. The default is "\r".

    Returns
    -------
    str
        DESCRIPTION.
    
    Variables
    -------
    percent        - percent of process completed
    filled_length  - calculate the length of filled bar
    progress_bar   - design process bar
    
    '''
      
    percent = round(100*(files_copied/float(no_of_files_to_be_copied)), 2)   
    filled_length = int(length * files_copied // no_of_files_to_be_copied)   
    progress_bar = fill * filled_length + '-' * (length - filled_length)     
    return f'Progress |{progress_bar}| {percent}% complete'
        
    if files_copied == no_of_files_to_be_copied: 
        print()
    

if __name__ == "__main__":
    main()

 




