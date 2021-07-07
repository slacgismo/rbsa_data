import pandas as pd 
import glob
data_path = 'data/rbsa_sites'
total_file = []
df_avg_per_appl = []
avg_val = []
rbsafiles = glob.glob(data_path + '/*.csv')
for filename in rbsafiles : 
	df = pd.read_csv(filename,index_col=None, header=0)
	total_file.append(df)
frame = pd.concat(total_file, axis=0, ignore_index=True)
headers = list(frame)
for header in headers : 
	if 'siteid' in header or 'time' in header or 'Service' in header or 'Panel' in header or 'Total' in header or 'Heating' == header or 'Cooling' in header or 'HeatCool' in header: 
		continue 
	df_avg_per_appl.append([header, frame[header].mean()])
	avg_val.append(frame[header].mean())
print(df_avg_per_appl)
print(sum(avg_val))

