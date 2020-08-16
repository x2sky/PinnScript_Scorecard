#!/opt/csw/bin/python
####################################
#createScoreCardsScript_Nrg_HN002.py
#Use the information from Pinnacle to
#create a script to start the score card
#of NRG HN002
#
#Modified:
#2015 09 Becket Hui
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

def createScroeCardsScript(savFolder,m):
 """!
 @brief read the information from Store.Nrg_HN002 to create score card script
 @param savFolder location of the patient folder, where all the intermediate files located
 """
 if m == 's': #the start of the scorecard
  #read the parameters from the store file
  with open(savFolder+'Store.Nrg_HN002','r') as f:
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

  #write scripts that would create the score cards
  #heading
  f = open(savFolder+'createScoreCardsNrg_HN002.Script','w')
  f.write('/////////////////////////////////////\n')
  f.write('//createScoreCardsNrg_HN002.Script///\n')
  f.write('///Create score card in Pinnacle ////\n')
  f.write('/////////////////////////////////////\n')
  f.write('\n')
  f.write('//create score card window and goals//\n')
  f.write('WindowList.TrialScoreCardEditor.Create = \"Score Card Window\";\n')
  f.write('\n')
  f.write('//clear current score card\n')
  f.write('Scorecard.DoseVolClinicalGoalList.DestroyAllChildren = \"Clear Score Card\";\n')
  f.write('\n')
  f.write('//name score cards\n')
  f.write('Scorecard.Name = \"UVA NRG HN 002\";\n')
  f.write('Scorecard.Description = \"Scorecard for %s %s\";\n' %(PatientName, MRN))
  f.write('\n')
  f.close()

 if m == 'p': #start writing PTV goals
  #read the parameters from the store file
  with open(savFolder+'Store.Nrg_HN002','r') as f:
   for line in f:
    if re.search('.PTV_N = SimpleString',line):
     line2 = f.next()
     PTV_N = readMe(line2,'s')
    if re.search('.PTVVol = SimpleString',line):
     line2 = f.next()
     PTVVol = readMe(line2,'s')
    if re.search('.CurrDose = Float',line):
     line2 = f.next()
     Dose = int(readMe(line2,'f'))
  #start writing goals
  f = open(savFolder+'createScoreCardsNrg_HN002.Script','a')
  if Dose == 6000:
   line = defineGoalinCards.writetext('','PTV_6000','Min DVH (%)',VT1=95,DT1=6000)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','PTV_6000','Max DVH (%)',VT1=95,DT1=6000,VT2=95,DT2=6300)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','PTV_6000','Min DVH (%)',VT1=99,DT1=5580,VT2=99,DT2=5400)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','PTV_6000','Max Dose',DT1=6600,DT2=6900)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','CTV_6000','Min DVH (%)',VT1=99,DT1=6000,VT2=95,DT2=6000)
   f.write(line+'\n')
  if Dose == 5400:
   line = defineGoalinCards.writetext('','PTV_5400','Min DVH (%)',VT1=95,DT1=5400,VT2=95,DT2=5130)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','PTV_5400','Min DVH (%)',VT1=99,DT1=5020,VT2=99,DT2=4800)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','CTV_5400','Min DVH (%)',VT1=99,DT1=5400,VT2=95,DT2=5400)
   f.write(line+'\n')
  if Dose == 4800:
   line = defineGoalinCards.writetext('','PTV_4800','Min DVH (%)',VT1=95,DT1=4800,VT2=95,DT2=4400)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','PTV_4800','Min DVH (%)',VT1=99,DT1=4460,VT2=99,DT2=4320)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','PTV_4800','Max Dose',DT1=5520,DT2=5760)
   f.write(line+'\n')
   line = defineGoalinCards.writetext('','CTV_4800','Min DVH (%)',VT1=99,DT1=4800,VT2=95,DT2=4800)
   f.write(line+'\n')
  f.close()

 if m == 'o': #start writing OAR tolerance
  #start writing goals
  f = open(savFolder+'createScoreCardsNrg_HN002.Script','a')
  line = defineGoalinCards.writetext('','SpinalCord_05','Max Dose',DT1=4800,DT2=5000)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','SpinalCord','Max Dose',DT1=4500,DT2=4800)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','BrainStem_03','Max Dose',DT1=5000,DT2=5200)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Parotid_L','Mean Dose',DT1=2600)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Parotid_R','Mean Dose',DT1=2600)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Larynx','Mean Dose',DT1=3500)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Pharynx','Mean Dose',DT1=4000)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Submandibular_L','Mean Dose',DT1=3900)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Submandibular_R','Mean Dose',DT1=3900)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','OralCavity','Mean Dose',DT1=3200)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Esophagus_Upper','Mean Dose',DT1=3000)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','NonPTV','Max DVH (cm^3)',VT1=1,DT1=6300)
  f.write(line+'\n')
  line = defineGoalinCards.writetext('','Mandible','Max Dose',DT1=6300)
  f.write(line+'\n')
  f.close()

if __name__ == "__main__":
 savFolder = str(sys.argv[1])
 m = str(sys.argv[2])
 createScroeCardsScript(savFolder,m)
