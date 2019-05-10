import sys
assert(sys.version_info[0]>=3 and sys.version_info[1]>=6)
import os
import pandas as pd

class rbsa:
	def __init__(self,year=1):
		data = None
		ncsv = [4,5]
		for n in range(1,ncsv[year]):
			fn = 'data/rbsa%d-%d' % (year,n)
			csvname = fn + '.csv'
			if not os.path.exists(csvname):
				zipname = fn + '.zip'
				print("Extracting %s..."%zipname,flush=True)
				os.system("unzip -d data %s"%zipname)
			print("Loading %s..."%csvname,flush=True)
			d = pd.read_csv(csvname, index_col=['siteid','time'])
			if type(data) == type(None):
				data = d
			else:
				data = data.append(d)
		self.data = data


a = rbsa()
print(a.data)