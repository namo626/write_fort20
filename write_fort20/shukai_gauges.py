"""
Convert the flow data from Shukai to the format used in writefort20
"""
import numpy as np
import pandas as pd
from re import sub

def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])


data = pd.read_csv("shukai.csv")
ids = data.iloc[[0]]

dates = pd.to_datetime(data["Date"].drop(0))
data = data.drop("Date",axis=1)

for river in data:
    print(river)

    flow = data[river].drop(0)
    flow_info = pd.concat([dates, flow], axis=1)

    flow_id = int(data.at[0,river])
    #flow_file = str(flow_id) + '_' + camel_case(river)
    flow_file = '%02d_%s.csv' % (flow_id, river.replace(" ",""))

    flow_info.to_csv(flow_file, index=False)
