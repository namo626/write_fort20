"""
Convert the flow data from Shukai to the format used in writefort20
This assumes that the current dir has shukai.txt and the output will be
saved in ./data dir.
"""
import numpy as np
import pandas as pd
from re import sub
from datetime import datetime
import os

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

# setup folders
os.system("mkdir data")
os.system("cp ../TemplateFlows/* data/")

fp = open("shukai.txt", "r")
lines = fp.read().splitlines()

# First row is ID
data = []
for line in lines:
  data.append(line.split(","))

fp.close()

# Proceed column by column
cols = len(data[0])
rows = len(data)

for i in range(1,cols):
  flow_id = int(data[0][i])
  river = data[1][i]
  print(river)

  # remove existing river files
  os.system("rm data/%02d*" % flow_id)
  fflow = open("data/%02d_%s.csv" % (flow_id, river.replace(" ","")), "w")

  # header
  fflow.write("Date,%s\n" % river)
  # Loop over time series
  for j in range(2,rows):
    timestamp = datetime.strptime(data[j][0], '%m/%d/%y %H:%M')
    timestring = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    flow = float(data[j][i])

    # write to csv file
    fflow.write("%s,%.7f\n" % (timestring, flow))

  fflow.close()
