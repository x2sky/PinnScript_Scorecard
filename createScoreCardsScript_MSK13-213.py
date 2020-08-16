#!/opt/csw/bin/python
####################################
#createScoreCardsScript_MSK13-213.py
#Use the information from Pinnacle to
#create a script to start the score card
#of MSK rectal protocol
#
#Modified:
#2016 05 Becket Hui
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
 @brief read the information from Store.MSK13-213 to create score card script
 @param savFolder location of the patient folder, where all the intermediate files located
 """
 #initialize dose:
 PresDose = 0.0
 BstDose = 0.0
 OptBstDose = 0.0
 #read the parameters from the store file
 with open(savFolder+'Store.MSK13-213', 'r') as f:
  for line in f:
   if re.search('\.PatientName = SimpleString',line):
    line2 = f.next()
    PatientName = readMe(line2,'s')
   if re.search('\.MRN = SimpleString',line):
    line2 = f.next()
    MRN = readMe(line2,'s')
   if re.search('\.Plan = SimpleString',line):
    line2 = f.next()
    PlanName = readMe(line2,'s')
   if re.search('\.PresDose = Float',line):
    line2 = f.next()
    PresDose = readMe(line2,'f')
   if re.search('\.BstDose = Float',line):
    line2 = f.next()
    BstDose = readMe(line2,'f')
   if re.search('\.OptBstDose = Float',line):
    line2 = f.next()
    OptBstDose = readMe(line2,'f')
   if re.search('\.PTV50Max = Float',line):
    line2 = f.next()
    PTV50Max = readMe(line2,'f')
   if re.search('\.PTVBtMax = Float',line):
    line2 = f.next()
    PTVBstMax = readMe(line2,'f')

 #find 3D cases:
 if BstDose == 540:
  PresDose = PresDose + BstDose
  if OptBstDose == 360 or OptBstDose == 540:
   BstDose = OptBstDose
  else:
   BstDose = 0

 #write scripts that would create the score cards
 #heading
 f = open(savFolder+'createScoreCards.Script','w')

 f.write('/////////////////////////////////\n')
 f.write('/////createscoreCards.Script/////\n')
 f.write('//Create score card in Pinnacle//\n')
 f.write('/////////////////////////////////\n')
 f.write('\n')
 f.write('//clear current score card\n')
 f.write('Scorecard.DoseVolClinicalGoalList.DestroyAllChildren = \"Clear Score Card\";\n')
 f.write('\n')
 f.write('//name score cards\n')
 f.write('Scorecard.Name = \"MSK Rectal Protocol\";\n')
 f.write('Scorecard.Description = \"Scorecard for %s %s\";\n' %(PatientName, MRN))
 f.write('\n')

 #start writing goals
 f.write('//define goals//\n')
 #PTV requirements
 line = defineGoalinCards.writetext('Target','PTV45','Max Dose',DT1=PTV50Max)
 f.write(line+'\n')
 if BstDose < 100 : #10% limit only runs in non-boost version or it fails
  line = defineGoalinCards.writetext('Target','PTV45','Max DVH (%)',VT1=10,DT1=5000)
  f.write(line+'\n')
 line = defineGoalinCards.writetext('Target','PTV45','Min DVH (%)',VT1=95,DT1=4500)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Target','PTV45','Min DVH (%)',VT1=100,DT1=4275)
 f.write(line+'\n')
 if BstDose > 100 : #if there is boost
  line = defineGoalinCards.writetext('Boost','PTV50','Max Dose',DT1=round(PTVBstMax))
  f.write(line+'\n')
 else:
  line = defineGoalinCards.writetext('Boost','PTV50','Max Dose',DT1=round(PresDose*1.1))
  f.write(line+'\n')
 line = defineGoalinCards.writetext('Boost','PTV50','Min DVH (%)',VT1=95,DT1=PresDose)
 f.write(line+'\n')
 if BstDose == 360 or BstDose == 400:
  line = defineGoalinCards.writetext('Extra boost','PTVBoost','Max Dose',DT1=5940)
  f.write(line+'\n')
 if BstDose == 540 or BstDose == 600:
  line = defineGoalinCards.writetext('Extra boost','PTVBoost','Max Dose',DT1=6160)
  f.write(line+'\n')
 #bowel dose
 line = defineGoalinCards.writetext('Bowel D5%','Bowel','Max DVH (%)',VT1=5,DT1=5000)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Small bowel V45Gy','SmallBowel','Max DVH (cm^3)',VT1=100,DT1=4500)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Small bowel V50Gy','SmallBowel','Max DVH (cm^3)',VT1=10,DT1=5000)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Large bowel V45Gy','LargeBowel','Max DVH (cm^3)',VT1=135,DT1=4500)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Large bowel V50Gy','LargeBowel','Max DVH (cm^3)',VT1=45,DT1=5000)
 f.write(line+'\n')
 #bladder dose
 line = defineGoalinCards.writetext('Bladder Dmax','Bladder','Max Dose',DT1=round(max(PTV50Max,PTVBstMax)))
 f.write(line+'\n')
 #vagina dose
 line = defineGoalinCards.writetext('Vagina V45Gy','Vagina','Max DVH (%)',VT1=85,DT1=4500)
 f.write(line+'\n')
 #femurs dose
 line = defineGoalinCards.writetext('Femurs Dmax','Femurs','Max Dose',DT1=5000)
 f.write(line+'\n')
 #cauda dose
 line = defineGoalinCards.writetext('Cauda Equina Dmax','CaudaEquina','Max Dose',DT1=5000)
 f.write(line+'\n')
 f.write('\n')
 f.write('//create score card window//\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Create = \"Score Card Window\";\n')
 #finish writing goals
 f.close()

if __name__ == "__main__":
 savFolder = str(sys.argv[1])
 createScroeCardsScript(savFolder)
