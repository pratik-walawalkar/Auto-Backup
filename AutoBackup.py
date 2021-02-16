# =============================================================================

# This script is written to copy files from a source folder to destination folder

# Created on Tue Feb 16 07:46:46 2021

# @author: Pratik Walawalkar

# =============================================================================


import os
import time
import curses
import shutil
from datetime import datetime

#sourcePath = r"D:\Users\Pratik\OneDrive - stud.th-deg.de\Documents\GitHub\Auto-Backup\Test\source" 
#destPath = r"D:\Users\Pratik\OneDrive - stud.th-deg.de\Documents\GitHub\Auto-Backup\Test\destination"

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
    global total_files, files_skipped, sourcePath, destPath
          
    sourcePath = check_path(input("Enter the source folder: "))        
    destPath = check_path(input("Enter the destination folder: ")) 

    
    if os.path.isdir(sourcePath) and os.path.isdir(destPath) and sourcePath is not destPath:
        
        print("Searchning for new files...")
        print("Please wait...")
        
        #Find total no. of files in the given directory
        total_files = sum(len(files) for path, directory, files in os.walk(os.path.join(sourcePath)))
        
        files_in_dst(destPath)
        files_to_copy(sourcePath)
        
        print("Found " + str(no_of_files_to_be_copied) + " files to be copied\n")
        
        files_skipped = total_files - no_of_files_to_be_copied
        loop = True
        while loop == True:
            cmd = input("Press 'Y' to proceed and 'N' to abort: ").lower()
            if cmd == 'y':
                copy_files(files_to_be_copied)
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
        
def check_path(path):    
    loop = True
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
            dst = dirpath.replace(destPath,"")
            files_in_dest += [ os.path.join(dst, file) for file in filenames]
    no_of_files_in_dest = len(files_in_dest)
    
    return dst, files_in_dest, no_of_files_in_dest
    
def files_to_copy(sourcePath):
    '''
    Description
    ----------
    find new files to be copied
    
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
        src = dirpath.replace(sourcePath,"")
        files_to_be_copied += [ os.path.join(src, file) for file in filenames if os.path.join(src, file) not in files_in_dest]
        size_files_to_be_copied = round(sum(os.path.getsize(os.path.join(sourcePath, file.strip("\\"))) for file in files_to_be_copied)/(1024*1024.0), 4)
    
    no_of_files_to_be_copied = len(files_to_be_copied)
    
    return src, files_to_be_copied, no_of_files_to_be_copied, size_files_to_be_copied
 
def file_size(list_of_files):
    '''
    Description
    ----------
    calculates sum for files in a list
    
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
    
    curses.initscr().clear()
    curses.initscr().addstr(0, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(1, 0,"File's copied                                      :" + str(files_copied) + " files / " + str(file_size(list_of_copied_files)) +" MB")
    curses.initscr().addstr(2, 0,"Files already exist                                :" + str(files_skipped))
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
    
    time.sleep(0.1)

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
    
        
        src = os.path.join(sourcePath, file.strip("\\"))
        dst = os.path.join(destPath, file.strip("\\"))
    
        directory = os.path.dirname(dst)
        
        os.makedirs(directory, exist_ok=True)
        shutil.copy2(src, dst)    
        
        list_of_copied_files.append(dst)
        files_copied += 1
              
        action = "Copied: {}" .format(os.path.basename(file))
        status(file)
        
    else:
        action = "No new files to be copied"

def update_log():
    with open(os.path.join(destPath, "Update_log.txt"), 'a') as textFile:
            

        textFile.write(now.strftime("%d/%m/%y %H:%M:%S") + ' - Backed up '+ str(files_copied) + ' files' + "(" + str(file_size(list_of_copied_files)) + ")" "\n")
    
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
 




