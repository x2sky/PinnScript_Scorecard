#!/opt/csw/bin/python
####################################
#createScoreCardsScript_Rtog0924Ph2.py
#Use the information from Pinnacle to
#create a script to start the score card
#of RTOG 0924 Phase 2 Boost
#
#Modified:
#2015 08 Becket Hui
#2015 10 Becket Hui: change max & min dose to max & min DVH(cm^3)
#2017 05 Becket Hui change code to incorporate the new scorecard editor with description
####################################
#make sure this file and all other subfiles are stored in script home in the main Script
import sys, re
import defineGoalinCards

def readMe(line,m):
 """!
 @brief return the value after equal sign a line read from Pinnacle Store file
 @param line line read from Pinnacle Store file
 @param m mode of the value - 'f' being number and 's' being string
 """
 if m=='f':
  linesp = re.split(r';|\s+',line)
  for i in range(len(linesp)):
   if linesp[i] == '=':
    return float(linesp[i+1])
 if m=='s':
  linesp = re.split(r'\"|;',line)
  for i in range(len(linesp)):
   if re.search('=',linesp[i]):
    return linesp[i+1]

def createScroeCardsScript(savFolder):
 """!
 @brief read the information from Store.Rtog0924 to create score card script
 @param savFolder location of the patient folder, where all the intermediate files located
 """
 #read the parameters from the store file
 with open(savFolder+'Store.Rtog0924', 'r') as f:
  for line in f:
   if re.search('.PatientName = SimpleString',line):
    line2 = f.next()
    PatientName = readMe(line2,'s')
   if re.search('.MRN = SimpleString',line):
    line2 = f.next()
    MRN = readMe(line2,'s')
   if re.search('.Plan = SimpleString',line):
    line2 = f.next()
    PlanName = readMe(line2,'s')
   if re.search('.PresDose = Float',line):
    line2 = f.next()
    PresDose = readMe(line2,'f')
   if re.search('.PTVVol = Float',line):
    line2 = f.next()
    PTVvol = readMe(line2,'f')
 
 #write scripts that would create the score cards

 #heading
 print savFolder+'createScoreCardsRtog0924Ph2.Script'
 f = open(savFolder+'createScoreCardsRtog0924Ph2.Script','w')

 f.write('/////////////////////////////////////\n')
 f.write('//createScoreCardsRtog0924Ph2.Script/\n')
 f.write('///Create score card in Pinnacle ////\n')
 f.write('/////////////////////////////////////\n')
 f.write('\n')
 f.write('//clear score card window and goals//\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Unrealize = \"\";\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Destroy = \"\";\n')
 f.write('\n')
 f.write('//clear current score card\n')
 f.write('Scorecard.DoseVolClinicalGoalList.DestroyAllChildren = \"Clear Score Card\";\n')
 f.write('\n')
 f.write('//name score cards\n')
 f.write('Scorecard.Name = \"RTOG 0924 Phase 2-Boost\";\n')
 f.write('Scorecard.Description = \"Scorecard for %s %s\";\n' %(PatientName, MRN))
 f.write('\n')

 #start writing goals
 f.write('//define goals//\n')
 #phase 2 after boost dose (IMRT only)
 #PTV requirements
 PTV_N = 'PTV_' + str(int(PresDose))
 line = defineGoalinCards.writetext('Target coverage',PTV_N,'Min DVH (%)',VT1=98,DT1=0.98*PresDose)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Target coverage',PTV_N,'Max DVH (%)',VT1=98,DT1=1.02*PresDose)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Min 0.03cc dose',PTV_N,'Min DVH (%)',VT1=min(100*(PTVvol-0.03)/PTVvol,100),DT1=0.95*PresDose,VT2=min(100*(PTVvol-0.03)/PTVvol,100),DT2=0.9*PresDose)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Max 0.03cc dose',PTV_N,'Max DVH (cm^3)',VT1=0.03,DT1=1.07*PresDose,VT2=0.03,DT2=1.10*PresDose)
 f.write(line+'\n')
 #dose homogeneity requirement
 line = defineGoalinCards.writetext('Homogeneity: IDL107%','External','Max DVH (cm^3)',VT1=0.1*PTVvol,DT1=1.07*PresDose)
 f.write(line+'\n')
 #D_max in patient
 #line = defineGoalinCards.writetext('MaxPointDose-PTV_Ext','Min Dose',DT1=0)
 #f.write(line+'\n')
 #bladder dose
 line = defineGoalinCards.writetext('Bladder V80Gy','Bladder','Max DVH (%)',VT1=15,DT1=8000,VT2=20,DT2=8000)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Bladder V75Gy','Bladder','Max DVH (%)',VT1=25,DT1=7500,VT2=30,DT2=7500)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Bladder V70Gy','Bladder','Max DVH (%)',VT1=35,DT1=7000,VT2=40,DT2=7000)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Bladder V65Gy','Bladder','Max DVH (%)',VT1=50,DT1=6500,VT2=55,DT2=6500)
 f.write(line+'\n')
 #rectum dose
 line = defineGoalinCards.writetext('Rectum V75Gy','Rectum','Max DVH (%)',VT1=15,DT1=7500,VT2=20,DT2=7500)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Rectum V70Gy','Rectum','Max DVH (%)',VT1=25,DT1=7000,VT2=30,DT2=7000)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Rectum V65Gy','Rectum','Max DVH (%)',VT1=35,DT1=6500,VT2=40,DT2=6500)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Rectum V60Gy','Rectum','Max DVH (%)',VT1=50,DT1=6000,VT2=55,DT2=6000)
 f.write(line+'\n')
 #penile bulb dose
 line = defineGoalinCards.writetext('Penile bulb Dmean','PenileBulb','Mean Dose',DT1=5250)
 f.write(line+'\n')
 #finish writing goals
 f.write('//create score card window//\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Create = \"Score Card Window\";\n')
 f.close()

if __name__ == "__main__":
 savFolder = str(sys.argv[1])
 createScroeCardsScript(savFolder)
