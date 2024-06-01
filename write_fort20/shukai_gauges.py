"""
Convert the flow data from Shukai to the format used in writefort20
This assumes that the current dir has shukai.txt and the output will be
saved in ./data dir.
"""
import numpy as np
import pandas as pd
from re import sub
from datetime import datetime
from dateutil import parser
import os
import rapidfuzz as rp

def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])


# data = pd.read_csv("shukai.txt")
# #ids = data.iloc[[1]]

# dates = pd.to_datetime(data["Date"].drop(0))
# data = data.drop("Date",axis=1)

# for river in data:
#     print(river)

#     flow = data[river].drop(0)
#     flow_info = pd.concat([dates, flow], axis=1)

#     flow_id = int(data.at[0,river])
#     #flow_file = str(flow_id) + '_' + camel_case(river)
#     # Remove duplicates
#     flow_file = 'data/%02d_%s.csv' % (flow_id, river.replace(" ",""))

#     flow_info.to_csv(flow_file, index=False)

# Mapping river name to ID
river_list = [
  "Rio Grande",
  "Arroyo Colorado",
  "Los Olmos Creek",
  "Santa Gertrudis Creek",
  "Petronila Creek",
  "Oso Creek",
  "Nueces River",
  "Chiltipin Creek",
  "Aransas River",
  "Mission River",
  "Copano River",
  "Guadalupe River",
  "San Antonio River",
  "Placedo Creek",
  "Arenosa Creek",
  "Lavaca River",
  "Tres Palacios River",
  "Colorado River",
  "Live Oak Bayou",
  "Celery Creek",
  "Cedar Lake Creek",
  "San Bernard River",
  "Brazos River",
  "Oyster Creek",
  "Bastrop Bayou",
  "Chocolate Bayou",
  "Dickinson Bayou",
  "Clear Creek",
  "Greens Bayou",
  "Vince Bayou",
  "Sims Bayou",
  "Brays Bayou",
  "Buffalo Bayou",
  "Hunting Bayou",
  "San Jacinto River",
  "Goose Creek",
  "Cedar Bayou",
  "Trinity River",
  "Taylor Bayou",
  "Hillebrant Bayou",
  "Pine Island Bayou",
  "Neches River",
  "Cow Bayou",
  "Adams Bayou",
  "Sabine River"
  ]

# setup folders
os.system("rm -rf data")
os.system("mkdir data")
os.system("cp ../TemplateFlows/* data/")

fp = open("shukai.txt", "r")
lines = fp.read().splitlines()

# First row is Date, river1, river2, ..., riverN
data = []
for line in lines:
  data.append(line.split(","))

fp.close()

# Proceed column by column
cols = len(data[0])
rows = len(data)

for i in range(1,cols):
  river = data[0][i]
  # Fuzzy search for matching river name, and get the ID
  fuzzy = rp.process.extractOne(river, river_list)
  flow_id = 1 + fuzzy[-1]
  river_name = fuzzy[0]

  print("%s --> %s" % (river, river_name) )

  # remove existing river files
  os.system("rm data/%02d*" % flow_id)
  fflow = open("data/%02d_%s.csv" % (flow_id, river.replace(" ","")), "w")

  # header
  fflow.write("Date,%s\n" % river)
  # Loop over time series
  for j in range(1,rows):
    #timestamp = datetime.strptime(data[j][0], '%m/%d/%y %H:%M')
    timestamp = parser.parse(data[j][0])
    timestring = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # If flow value is empty, just put zero
    flow_string = data[j][i]
    if flow_string:
      flow = float(data[j][i])
    else:
      flow = 0.0

    # write to csv file
    fflow.write("%s,%.7f\n" % (timestring, flow))

  fflow.close()
