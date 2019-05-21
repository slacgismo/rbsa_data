import sys
if not ( sys.version_info[0]>=3 and sys.version_info[1]>=7 ):
	raise Exception("rbsa.py: %s is not supported" % str(sys.version_info))
import os
import pandas as pd

class rbsa:
	def __init__(self,year):
		data = None
		ncsv = {1:4,2:5}
		for n in range(1,ncsv[year]+1):
			fn = 'data/rbsa%d-%d' % (year,n)
			csvname = fn + '.csv'
			if not os.path.exists(csvname):
				zipname = fn + '.zip'
				print("Extracting %s..."%zipname,flush=True)
				os.system("unzip -d data %s"%zipname)
			print("Loading %s..."%csvname,flush=True)
			d = pd.read_csv(csvname, index_col=['siteid','time'])
			#print("  size: %.2f GB" % (sys.getsizeof(d)/1.0e9))
			if type(data) == type(None):
				data = d
			else:
				data = data.append(d)
		self.data = data

y1 = rbsa(year=1)
print("RBSA year 1 size: %.2f GB" % (sys.getsizeof(y1.data)/1.0e9))
