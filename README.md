# Auto Backup
 Automatically copy data from a source folder to a destination folder. A nice user interface is designed to be able to easily interact with the code. Further modifications are to be made to automaticallly backup date after receiving a trigger signal.
 
 This code can be used to take mobile phone backup to you computer as it is programmmed to copy only unique files and ignore duplicate file names. 

## Run the AutoBackup.py file:
1. If you want to perform wireless mobile backup Make sure that you have made the necessary settings mentioned below in the "Setup for wireless mobile phone backup" section.
2. With the necessary modules installed, start a command prompt in the location where AutoBackup.py file is located.
3. Enter the "python AutoBackup.py"
4. Select the type of file transfer you want to perform.
5. If you select "Proceed with the saved source and the Destination" then the code will consider the source and destination directory as the one saved in the first if loop of select_dir() functon.
6. If you select "to enter new source and destination", then it will enter the second if loop in the select_dir() function and will take your source and destination path as an input and check if the path is valid.
7. If you select "wireless mobile phone backup", then the code will enter the third if loop and assign source folder as "Z:\\" and enter the check_device() function to search for "_device_info.txt" file in the source folder and depending on the device name mentioned in the text file, it would select the destination folder. 
8. Information regarding the files to be copied will be displayed. 
9. Enter 'Y' to proceed and 'N' to abort the process.
10. If you enter 'Y' the the necessary files will be copied from the source directory to the destination directory. 

## Flow of the code:
1. When you run the code, it will first ask you to select if you want to proceed with the saved source and destination, enter new source and destination, or perform wireless backup of the saved device.
2. If you select "Proceed with the saved source and the Destination" then the code will consider the source and destination directory as the one saved in the first if loop of select_dir() functon.
3. If you select "to enter new source and destination", then it will enter the second if loop in the select_dir() function and will take your source and destination path as an input and check if the path is valid.
4. If you select "wireless mobile phone backup", then the code will enter the third if loop and assign source folder as "Z:\\" and enter the check_device() function to search for "_device_info.txt" file in the source folder and depending on the device name mentioned in the text file, it would select the destination folder.
5. Next, it will check if the source and destination are two different folders and then move ahead.
6. The total_files in the source folder will be calculated.
7. It will enter "files_in_dst(destPath)" function and will create a list of files already present in the destination folder at a particular location.
8. The code will enter "files_to_copy(sourcePath)" function and create a list of files which are not present in the destination folder and needs to be copied.
9. A message will be displayed with the number of new files which can be copied.
10. Select 'Y' to proceed and 'N' to abort.
11. If you enter 'N' the process would eventually terminate.
12. But if you enter 'Y' then the code would enter "copy_files(files_to_be_copied)" function where the list of files to be copied is given as an input and the source and destination path are created and the files are copied.
13. There is a "_Backup_log" folder created at the destination where a new .txt file is created during every backup which saves the files copied in the process.
14. To edit the details regarding the log file make the necessary changes to 'update_log()' function.
15. There are several other function block used to design interface and calculate different parameters and are called during the process.
16. When the process is completed a "Completed!!!" message is displayed in Estimated time left.

## Setup for wireless mobile phone backup:

## Mobile Phone Setup:

1. Download WebDAV app from the play store.
2. Recommended settings are:
   Network interface - WiFi
   Port - 8080
   Home directory - SdCard
3. Turn on the server while attempting to take wireless backup

## Setting up a network drive on windows (Windows 10):

1. With the WebDAV server turned ON on your mobile device and your mobile and PC connected to the same wireless network.
2. Open File Explorer or press Win + E on your computer and right click on the network folder 
3. Find 'Network' from the left side pane of the window
4. Right click on it and select 'Map Network Drive'. Map Network Drive dialog box will appear
5. Choose a drive letter. It is recommended to use 'Z:'. If you want to choose any other drive letter, then you need to replace 'Z:\\' with the new drive letter in the code
6. Enter enter the network path displayed on your mobile phone in WebDAV app (e.g. http:\\192.168.187.21:8080) in the Folder section.
7. Click on finish.
8. Next you also need to change the wireless file size transfer limit. As by default you wont be able to tranfer a size more than 50MB. But we can make the necessary changes to registry to be able to send a file with a maximum size of 4GB.

## Registry Settings:

1. Click on start and search registry editor or regedit and press ENTER.
2. Open the registry editor (using regedit on the Windows Start menu)
3.  Locate and click the following registry subkey:
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WebClient\Parameters
4. Select DWORD FileSizeLimitInBytes.
5. Go to Edit > Modify.
6. In the Value data box, enter 50000000 (decimal) and then click OK.
This sets the maximum you can download from the WebDAV to 4 GB at one time, where 4 GB is the maximum value supported by Windows OS.
7. Next we have to increase the timeout value wich is set to 30 minutes by default.
8. Locate and then click the following registry subkey:
HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\MRxDAV\Parameters
9.locate the DWORD FsCtlRequestTimeoutInSec
10.On the Edit menu, click Modify.
11.In the Value data box increase the Value of 1800 (Decimal)
12.Exit Registry Editor and restart your PC.

## Destination Folder Setup:

1. Create a destination folder in your local directory where you want to save your mobile phone data

## Setup for source folder:

1. In the root folder to backup, create a new text file named _device_info.txt
2. Enter the name of device on the first line which would be used later to identify the device usich the check_device() fuction and the device name is stored in 'deviceName' variable and is later compared with the saved names.
   (See to it that the name of device is only one word without any space)
   
## Caution:
 
1. Duplicates are detected only with respect to the filenames and not the date of creation, modification or attributes of the file
2. Few changes must be made to registry to be enable to transfer a file over 50MB (the max. limit is 4GB)
3.If you want to transfer your files from your mobile phone to your PC/Laptop, you can create a server using webDAV and use it as a source location to copy files to a destination folder. 


