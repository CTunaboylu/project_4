#there are external libraries that are necessary for this to run , collect them
#grab all the packages that host has 
import os 
#import subprocess

#subprocess.call(['C:\\Temp\\a b c\\Notepad.exe', 'C:\\test.txt'])
p_free_command = 'pip freeze > requirements.txt'
os.system(p_free_command)
