#!/bin/env python3

import numpy as np
import pandas as pd
from ics import Calendar,Event
import sys

csv=sys.argv[1] # csv file of dates; don't forget year must be yyyy
outfile=sys.argv[2] # .ics file

# Reshaping POS giants game data into something consistent

apes=pd.read_csv(csv)
apes_sf=apes[apes['LOCATION'].str.contains('Oracle')]
apes_sf.dropna(inplace=True)
inds2rm=[]
for i in range(0,len(apes_sf.index)):
    try:
        if 8 > float(apes_sf['START TIME'].iloc[i].split(':')[0]) > 3 : # omit mornings
            inds2rm.append(i)
    except AttributeError: # some times are tbd
        inds2rm.append(i) # include on the calendar just in case
        print(apes_sf['START DATE'].iloc[i] + ' tbd time')
dates=apes_sf['START DATE'].iloc[inds2rm].values

# put in order that ics needs: yyyy/mm/dd; currently in mm/dd/yyyy format
# I manually changed the yy format to yyyy in the csv file >.>
# You could probably use a datetime library to fix that but baseball apes call for quick & dirty

c=Calendar()

for d in dates: # more like: commuters rule,  baseball apes meDROOL am I right?
    cpts = d.split('/')
    newdate = '/'.join([cpts[2],cpts[0],cpts[1]]) # again should probably be done with a datetime thing whatever
    e=Event(begin=newdate+' 00:00:00')
    e.make_all_day()
    e.name = "baseball apes"
    c.events.add(e)

with open(outfile,'w') as f:
   f.writelines(c.serialize_iter())
