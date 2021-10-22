from Tkinter import Tk
import os
import sys
from os.path import join, isdir

''' 
This file retrieves all file and directory names from the
current directory and copies the result to the clipboard
of the operating system.
'''

print sys.argv[0]

# List for temporarily storing the results
filelist = []

# Sort order:
# 1 = directories
# 2 = png files
# 3 = other files

# Store the path we are looking in
pth = os.path.dirname(sys.argv[0])

for fil in os.listdir(pth):

    fullname = os.path.join(pth,fil)
    
    if os.path.isdir(fullname):
        filelist.append( (1, fil) )
    else:
        if fil[-3:]=='png':
            filelist.append( (2, fil) )
        else:
            filelist.append( (3, fil) )

# Sort the files and directories
filelist.sort()

# Assemble the string with sorted files and directories
s=''
for isd, fil in filelist:
    print fil
    s+='%s\n' % fil

# Copy the result to the cliboard
r = Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(s)
r.destroy()

# Report the result
print 'The following lines are copied to the clipboard:'
print s
