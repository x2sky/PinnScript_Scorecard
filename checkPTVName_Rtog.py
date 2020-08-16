#!/opt/csw/bin/python
####################################
#checkPTVName_Rtog.py
#create the script that write the PTV_pres.dose
#in the store for Rtog 0924 score card calculation
#input:
#1) prescribed dose
#2) folder to save the Script that Pinnacle runs to save the string
#
#Modified by
#2015 08 Becket Hui
#2015 08 Becket Hui
####################################
#make sure this file and all other subfiles are stored in script home in the main Script
import sys

def writeName(presDose,savFolder):
 if presDose[0] == ' ':
  presDose = presDose[1:]
 name = 'PTV_'+str(int(presDose))

 f = open(savFolder+'checkPTVName.Script','w')
 f.write('Store.At.SCard.StringAt.PTV_Name = SimpleString{String = \"%s\";};\n' %name)
 f.write('Store.At.SCard.FloatAt.PTV_NameExist = 0;\n')
 f.write('IF.RoiList.ContainsObject.%s.THEN.Store.At.SCard.FloatAt.PTV_NameExist = 1;\n' %name)
 f.write('Store.At.SCard.FloatAt.PTVVol = 0;\n')
 f.write('IF.RoiList.ContainsObject.%s.THEN.RoiList.%s.RecomputeStatistics = \"Recompute\";\n' %(name,name))
 f.write('IF.RoiList.ContainsObject.%s.THEN.Store.At.SCard.FloatAt.PTVVol = RoiList.%s.Volume;\n' %(name,name))
 f.write('IF.Store.At.SCard.At.PTV_NameExist.Value.EQUALTO.#"#0".THEN.WarningMessage = \"%s is not defined, please define %s before running script\";\n' %(name, name))
 f.write('IF.Store.At.SCard.At.PTV_NameExist.Value.EQUALTO.#"#0".THEN.Store.At.SCard.FloatAt.FlgGo = 0;\n')
 f.close()

if __name__ == "__main__":
 presDose = str(sys.argv[1])
 savFolder = str(sys.argv[2])
 writeName(presDose,savFolder)
