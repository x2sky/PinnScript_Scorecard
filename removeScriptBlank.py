####################################
#removeScriptBlank.py
#remove the blank space from Pinnacle Float variable and
#rewrite script that creats the non-space value in a new string
#input:
#1) float value created by Pinnacle saved as String
#2) Store.At.String that you want the resulting String to be saved as in Store
#   !do not use StringAt
#3) folder to save the Script that Pinnacle runs to save the string
#
#Modified by
#BH 2015 07
####################################
#make sure this file and all other subfiles are stored in script home in the main Script
import sys, re

def removeSpace(inputNum,outputStr,savFolder):
 numNoSpc = re.sub(r'\s+',r'',inputNum)
 numNoSpc = re.sub(r'\:',r'',numNoSpc)

 f = open(savFolder+'removeSpace.Script','w')
 f.write(outputStr + ' = SimpleString{String = \"%s\";};' %numNoSpc)
 f.close()

if __name__ == "__main__":
 inputNum = str(sys.argv[1])
 outputStr = str(sys.argv[2])
 savFolder = str(sys.argv[3])
 removeSpace(inputNum,outputStr,savFolder)
