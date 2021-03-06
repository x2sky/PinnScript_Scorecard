#!/opt/csw/bin/python
####################################
#createScoreCardsScript_Rtog0915.py
#Use the information from Pinnacle to
#create a script to start the score card
#of RTOG 0915
#
#Modified:
#2015 08 Becket Hui
#2015 10 Becket Hui remove ribs dose from score card as it's never used
#2017 05 Becket Hui change code to incorporate the new scorecard editor with description
####################################
#make sure this file and all other subfiles are stored in script home in the main Script
import sys, re
import criteria_Rtog0915
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
 @brief read the information from Store.Rtog0915 to create score card script
 @param savFolder location of the patient folder, where all the intermediate files located
 """
 #read the parameters from the store file
 with open(savFolder+'Store.Rtog0915', 'r') as f:
  for line in f:
   if re.search('.PatientName',line):
    line2 = f.next()
    PatientName = readMe(line2,'s')
   if re.search('.MRN',line):
    line2 = f.next()
    MRN = readMe(line2,'s')
   if re.search('.Plan',line):
    line2 = f.next()
    PlanName = readMe(line2,'s')
   if re.search('.PresDose',line):
    line2 = f.next()
    PresDose = readMe(line2,'f')
   if re.search('.NoFractions',line):
    line2 = f.next()
    NoFrac = readMe(line2,'f')
   if re.search('.PTVVol',line):
    line2 = f.next()
    PTVvol = readMe(line2,'f')

 #calculate the criteria parameters
 CritPara = criteria_Rtog0915.criteria_Rtog(PTVvol,savFolder)
 
 #write scripts that would create the score cards

 #heading
 f = open(savFolder+'createScoreCardsRtog0915.Script','w')

 f.write('////////////////////////////////////\n')
 f.write('//createscoreCardsRtog0915.Script\n')
 f.write('//Create score card in Pinnacle \n')
 f.write('////////////////////////////////////\n')
 f.write('\n')
 f.write('//clear score card window and goals//\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Unrealize = \"\";\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Destroy = \"\";\n')
 f.write('\n')
 f.write('//clear current score card\n')
 f.write('Scorecard.DoseVolClinicalGoalList.DestroyAllChildren = \"Clear Score Card\";\n')
 f.write('\n')
 f.write('//name score cards\n')
 f.write('Scorecard.Name = \"UVA RTOG 0915 \-%i fractions\";\n' %NoFrac)
 f.write('Scorecard.Description = \"Scorecard for %s %s\";\n' %(PatientName, MRN))
 f.write('\n')

 #start writing goals
 f.write('//define goals//\n')
 #PTV requirements
 line = defineGoalinCards.writetext('Target coverage','PTV','Min DVH (%)',VT1=95,DT1=PresDose)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Target coverage','PTV','Min DVH (%)',VT1=99,DT1=0.9*PresDose)
 f.write(line+'\n')
 #max dose requirement
 line = defineGoalinCards.writetext('Heterogeneity: max dose','Pt_MaxDose','Max Dose',DT1=PresDose/0.6)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Heterogeneity: max dose','Pt_MaxDose','Min Dose',DT1=PresDose/0.9)
 f.write(line+'\n')
 #high dose spillage
 line = defineGoalinCards.writetext('Spillage: IDL105% outside PTV','External\-PTV','Max DVH (cm^3)',VT1=0.15*PTVvol,DT1=1.05*PresDose)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Spillage: IDL100% volume','External','Max DVH (cm^3)',VT1=CritPara[0]*PTVvol,DT1=PresDose,VT2=CritPara[1]*PTVvol,DT2=PresDose)
 f.write(line+'\n')
 #intermediate dose spillage
 line = defineGoalinCards.writetext('Spillage: 2cm from PTV','External\-PTV_2cm','Max Dose',DT1=0.01*CritPara[4]*PresDose,DT2=0.01*CritPara[5]*PresDose)
 f.write(line+'\n')
 line = defineGoalinCards.writetext('Spillage: IDL50%','External','Max DVH (cm^3)',VT1=CritPara[2]*PTVvol,DT1=0.5*PresDose,VT2=CritPara[3]*PTVvol,DT2=0.5*PresDose)
 f.write(line+'\n')
 #lung dose
 line = defineGoalinCards.writetext('Whole lung V20Gy','Lungs\-ITV','Max DVH (%)',VT1=CritPara[6],DT1=2000,VT2=CritPara[7],DT2=2000)
 f.write(line+'\n')

 #fractions dependent OAR dose limit
 if NoFrac == 1:
  #lung dose
  line = defineGoalinCards.writetext('Whole lung D1500cc','Lungs\-ITV','Max DVH (cm^3)',VT1=1500,DT1=700)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Whole lung D1000cc','Lungs\-ITV','Max DVH (cm^3)',VT1=1000,DT1=740)
  f.write(line+'\n')
  #cord dose
  line = defineGoalinCards.writetext('Spinal cord V10Gy','SpinalCord','Max DVH (cm^3)',VT1=0.35,DT1=1000)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Spinal cord V7Gy','SpinalCord','Max DVH (cm^3)',VT1=1.2,DT1=700)
  f.write(line+'\n') 
  line = defineGoalinCards.writetext('Spinal cord Dmax','SpinalCord','Max Dose',DT1=1400)
  f.write(line+'\n')
  #ipsilateral brachial plexus dose
  line = defineGoalinCards.writetext('Brachial plexus V14Gy','BrachialPlexus_Ipsi','Max DVH (cm^3)',VT1=3,DT1=1400)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Brachial plexus Dmax','BrachialPlexus_Ipsi','Max Dose',DT1=1750)
  f.write(line+'\n')
  #esophagus dose
  line = defineGoalinCards.writetext('Esophagus V11.9Gy','Esophagus','Max DVH (cm^3)',VT1=5,DT1=1190)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Esophagus Dmax','Esophagus','Max Dose',DT1=1540)
  f.write(line+'\n')
  #heart dose
  line = defineGoalinCards.writetext('Heart V16Gy','Heart','Max DVH (cm^3)',VT1=15,DT1=1600)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Heart Dmax','Heart','Max Dose',DT1=2200)
  f.write(line+'\n')
  #great vessels dose
  line = defineGoalinCards.writetext('Great vessels V31Gy','GreatVessel','Max DVH (cm^3)',VT1=10,DT1=3100)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Great vessels Dmax','GreatVessel','Max Dose',DT1=3700)
  f.write(line+'\n')
  #trachea and bronchus dose
  line = defineGoalinCards.writetext('Trachea & bronch V10.5Gy','Trachea\+BronchialTree','Max DVH (cm^3)',VT1=4,DT1=1050)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Trachea & bronch Dmax','Trachea\+BronchialTree','Max Dose',DT1=2020)
  f.write(line+'\n')
  #stomach dose
  line = defineGoalinCards.writetext('Stomach V11.2Gy','Stomach','Max DVH (cm^3)',VT1=10,DT1=1120)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Stomach Dmax','Stomach','Max Dose',DT1=1240)
  f.write(line+'\n')
  #skin dose
  line = defineGoalinCards.writetext('Skin V23Gy','Skin','Max DVH (cm^3)',VT1=10,DT1=2300)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Skin Dmax','Skin','Max Dose',DT1=2600)
  f.write(line+'\n')
  ############Remove Ribs Dose##############
  #ribs dose
  #line = defineGoalinCards.writetext('Rib objective','Rib','Max DVH (cm^3)',VT1=1,DT1=2200)
  #f.write(line+'\n')
  #line = defineGoalinCards.writetext('Rib objective','Rib','Max Dose',DT1=3000)
  #f.write(line+'\n')
  ##########################################
  #chest wall dose
  line = defineGoalinCards.writetext('Chest wall V30Gy','ChestWall','Max DVH (cm^3)',VT1=30,DT1=3000)
  f.write(line+'\n')
 else:
  #lung dose
  line = defineGoalinCards.writetext('Whole lung D1500cc','Lungs\-ITV','Max DVH (cm^3)',VT1=1500,DT1=1160)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Whole lung D1000cc','Lungs\-ITV','Max DVH (cm^3)',VT1=1000,DT1=1240)
  f.write(line+'\n')
  #cord dose
  line = defineGoalinCards.writetext('Spinal cord V20.8Gy','SpinalCord','Max DVH (cm^3)',VT1=0.35,DT1=2080)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Spinal cord V13.6Gy','SpinalCord','Max DVH (cm^3)',VT1=1.2,DT1=1360)
  f.write(line+'\n') 
  line = defineGoalinCards.writetext('Spinal cord Dmax','SpinalCord','Max Dose',DT1=2600)
  f.write(line+'\n')
  #ipsilateral brachial plexus dose
  line = defineGoalinCards.writetext('Brachial plexus V23.6Gy','BrachialPlexus_Ipsi','Max DVH (cm^3)',VT1=3,DT1=2360)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Brachial plexus Dmax','BrachialPlexus_Ipsi','Max Dose',DT1=2720)
  f.write(line+'\n')
  #esophagus dose
  line = defineGoalinCards.writetext('Esophagus V18.8Gy','Esophagus','Max DVH (cm^3)',VT1=5,DT1=1880)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Esophagus Dmax','Esophagus','Max Dose',DT1=3000)
  f.write(line+'\n')
  #heart dose
  line = defineGoalinCards.writetext('Heart V28Gy','Heart','Max DVH (cm^3)',VT1=15,DT1=2800)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Heart Dmax','Heart','Max Dose',DT1=3400)
  f.write(line+'\n')
  #great vessels dose
  line = defineGoalinCards.writetext('Great vessels V43Gy','GreatVessel','Max DVH (cm^3)',VT1=10,DT1=4300)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Great vessels Dmax','GreatVessel','Max Dose',DT1=4900)
  f.write(line+'\n')
  #trachea and bronchus dose
  line = defineGoalinCards.writetext('Trachea & bronch V15.6Gy','Trachea\+BronchialTree','Max DVH (cm^3)',VT1=4,DT1=1560)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Trachea & bronch Dmax','Trachea\+BronchialTree','Max Dose',DT1=3480)
  f.write(line+'\n')
  #stomach dose
  line = defineGoalinCards.writetext('Stomach V17.6Gy','Stomach','Max DVH (cm^3)',VT1=10,DT1=1760)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Stomach Dmax','Stomach','Max Dose',DT1=2720)
  f.write(line+'\n')
  #skin dose
  line = defineGoalinCards.writetext('Skin V33.2Gy','Skin','Max DVH (cm^3)',VT1=10,DT1=3320)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('Skin Dmax','Skin','Max Dose',DT1=3600)
  f.write(line+'\n')
  ############Remove Ribs Dose##############
  #ribs dose
  ##line = defineGoalinCards.writetext('Rib objective','Rib','Max DVH (cm^3)',VT1=1,DT1=3200)
  ##f.write(line+'\n')
  ##line = defineGoalinCards.writetext('Rib objective','Rib','Max Dose',DT1=4000)
  ##f.write(line+'\n')
  ##########################################
  #chest wall dose
  line = defineGoalinCards.writetext('Chest wall V30Gy','ChestWall','Max DVH (cm^3)',VT1=30,DT1=3000)
  f.write(line+'\n')

 #finish writing goals
 f.write('//create score card window//\n')
 f.write('WindowList.TrialScoreCardEditor_wDesc.Create = \"Score Card Window\";\n')
 f.close()

if __name__ == "__main__":
 savFolder = str(sys.argv[1])
 createScroeCardsScript(savFolder)
