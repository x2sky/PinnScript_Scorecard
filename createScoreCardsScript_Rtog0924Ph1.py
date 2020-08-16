#!/opt/csw/bin/python
####################################
#createScoreCardsScript_Rtog0924Ph1.py
#Use the information from Pinnacle to
#create a script to start the score card
#of RTOG 0924 Phase 1
#
#Modified:
#2015 08 Becket Hui
#2015 10 Becket Hui: change max & min dose to max & min DVH(cm^3)
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
 f = open(savFolder+'createScoreCardsRtog0924Ph1.Script','w')

 f.write('/////////////////////////////////////\n')
 f.write('//createScoreCardsRtog0924Ph1.Script/\n')
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
 f.write('Scorecard.Name = \"RTOG 0924 Phase 1\";\n')
 f.write('Scorecard.Description = \"Scorecard for %s %s\";\n' %(PatientName, MRN))
 f.write('\n')

 #start writing goals
 f.write('//define goals//\n')
 #Phase 1 dose
 PTV_N = 'PTV_' + str(int(PresDose))
 #PTV requirements
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
 #finish writing goals
 f.write('//create score card window//\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Create = \"Score Card Window\";\n')
 f.close()

if __name__ == "__main__":
 savFolder = str(sys.argv[1])
 createScroeCardsScript(savFolder)
