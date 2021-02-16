import os
import pandas as pd

files = os.listdir(".")
data = None
for file in files:
    if file[-4:] == ".csv":
        site = pd.read_csv(file)
        if data is None:
            data = site
        else:
            data.append(site)
print(data.columns.tolist())
load = data.mean()
total = 0.0
for enduse in ['InteriorLighting','Ventilation','Cooking','Electronics','Refrigeration','WaterHeating','Appliances','ExteriorLighting','Miscellaneous']:
    if load[enduse] == 0.0:
        print("warning: enduse %s is zero" % enduse)
    total += load[enduse]
print(load/total)
