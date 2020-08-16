#!/opt/csw/bin/python
####################################
#defineGoalinCards.py
#write the text of a defined goal in the score card format
#
#Modified:
#2015 8 Becket Hui
#2017 6 Becket Hui change code to incorporate the new scorecard editor with description
####################################
#volume and dose thresholds are set as kwargs
def writetext(Description, Name, Goal, VT1='NA', DT1='NA', VT2='NA', DT2='NA'):
 script = 'Scorecard.DoseVolClinicalGoalList.CreateChildMakeCurrent = \"Add Goal\";\n'
 script = script + 'Scorecard.DoseVolClinicalGoalList.Last = {\n'
 script = script + ' Store.StringAt.Description = \"'+Description+'\";\n'
 script = script + ' ExpectedRoi.Name = \"'+Name+'\";\n'
 script = script + ' GoalType = \"'+Goal+'\";\n'
 if VT1 is not 'NA':
  VT1 = '%.2f'%VT1
  script = script + ' VolPassingCriteria = \"'+str(VT1)+'\";\n'
 if DT1 is not 'NA':
  DT1 = int(round(DT1))
  script = script + ' DosePassingCriteria = \"'+str(DT1)+'\";\n'
 if VT2 is not 'NA':
  VT2 = '%.2f'%VT2
  script = script + ' VolAcceptableVariance = \"'+str(VT2)+'\";\n'
 if DT2 is not 'NA':
  DT2 = int(round(DT2))
  script = script + ' DoseAcceptableVariance = \"'+str(DT2)+'\";\n'
 script = script + '};\n'
 return script
