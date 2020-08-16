####################################
#criteria_Rtog0813.py
#calculate the does/volume criteria based on PTV volume in RTOG 0813
#
#Modified by:
#BH 2015 07
####################################
#make sure this file and all other subfiles are stored in script home in the main Script
import sys

class Crit:
 N = 11 #number of points
 PTVlim = [1.8,3.8,7.4,13.2,22.0,34.0,50.0,70.0,95.0,126.0,163.0] #PTV volume limits
 R100Non = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2]
 R100Min = [1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5]
 R50Non = [5.9,5.5,5.1,4.7,4.5,4.3,4.0,3.5,3.3,3.1,2.9]
 R50Min = [7.5,6.5,6.0,5.8,5.5,5.3,5.0,4.8,4.4,4.0,3.7]
 D2cmNon = [50.0,50.0,50.0,50.0,54.0,58.0,62.0,66.0,70.0,73.0,77.0]
 D2cmMin = [57.0,57.0,58.0,58.0,63.0,68.0,77.0,86.0,89.0,91.0,94.0]
 V20Non = [10,10,10,10,10,10,10,10,10,10,10]
 V20Min = [15,15,15,15,15,15,15,15,15,15,15]

def criteria_Rtog(PTVvol,savFolder):
 #set the criteria parameters
 CritPara = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
 if PTVvol <= Crit.PTVlim[0]:
  CritPara[0] = Crit.R100Non[0]
  CritPara[1] = Crit.R100Min[0]
  CritPara[2] = Crit.R50Non[0]
  CritPara[3] = Crit.R50Min[0]
  CritPara[4] = Crit.D2cmNon[0]
  CritPara[5] = Crit.D2cmMin[0]
  CritPara[6] = Crit.V20Non[0]
  CritPara[7] = Crit.V20Min[0]

 for i in range(1,Crit.N-1):
  if PTVvol > Crit.PTVlim[i-1] and PTVvol <= Crit.PTVlim[i]:
   CritPara[0] = Crit.R100Non[i-1] + (Crit.R100Non[i]-Crit.R100Non[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])
   CritPara[1] = Crit.R100Min[i-1] + (Crit.R100Min[i]-Crit.R100Min[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])
   CritPara[2] = Crit.R50Non[i-1] + (Crit.R50Non[i]-Crit.R50Non[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])
   CritPara[3] = Crit.R50Min[i-1] + (Crit.R50Min[i]-Crit.R50Min[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])
   CritPara[4] = Crit.D2cmNon[i-1] + (Crit.D2cmNon[i]-Crit.D2cmNon[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])
   CritPara[5] = Crit.D2cmMin[i-1] + (Crit.D2cmMin[i]-Crit.D2cmMin[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])
   CritPara[6] = Crit.V20Non[i-1] + (Crit.V20Non[i]-Crit.V20Non[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])
   CritPara[7] = Crit.V20Min[i-1] + (Crit.V20Min[i]-Crit.V20Min[i-1])*(PTVvol-Crit.PTVlim[i-1])/(Crit.PTVlim[i]-Crit.PTVlim[i-1])

 if PTVvol > Crit.PTVlim[Crit.N-1]:
  CritPara[0] = Crit.R100Non[Crit.N-1]
  CritPara[1] = Crit.R100Min[Crit.N-1]
  CritPara[2] = Crit.R50Non[Crit.N-1]
  CritPara[3] = Crit.R50Min[Crit.N-1]
  CritPara[4] = Crit.D2cmNon[Crit.N-1]
  CritPara[5] = Crit.D2cmMin[Crit.N-1]
  CritPara[6] = Crit.V20Non[Crit.N-1]
  CritPara[7] = Crit.V20Min[Crit.N-1]

 f = open(savFolder+'Criteria_Parameters.Rtog0813','w')
 f.write('The PTV volume is: %.2f\n'%PTVvol)
 f.write('The following are the parameters used:\n')
 f.write('Ratio of Prescription Isodose Volume to the PTV Volume (No Deviation) = %.2f\n'%CritPara[0])
 f.write('Ratio of Prescription Isodose Volume to the PTV Volume (Minor Deviation) = %.2f\n'%CritPara[1])
 f.write('Ratio of V50p to the PTV volume (No Deviation) = %.2f\n'%CritPara[2])
 f.write('Ratio of V50p to the PTV volume (Minor Deviation) = %.2f\n'%CritPara[3])
 f.write('Max Dose (in Percent of Prescription Dose) more than 2cm away from PTV (No Deviation) = %.2f\n'%CritPara[4])
 f.write('Max Dose (in Percent of Prescription Dose) more than 2cm away from PTV (Minor Deviation) = %.2f\n'%CritPara[5])
 f.write('Percent of V20 of lung (No Deviation) = %.2f\n'%CritPara[6])
 f.write('Percent of V20 of lung (Minor Deviation) = %.2f\n'%CritPara[7])
 f.close()

 return CritPara

if __name__ == "__main__":
 PTVvol = float(sys.argv[1])
 savFolder = str(sys.argv[2])
 criteria_Rtog(PTVvol,savFolder)
