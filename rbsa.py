import sys, os
import pandas as pd
import utility
import datetime

class rbsa:
	def __init__(self,year=1):
		data = None
		ncsv = [4,5]
		for n in range(1,ncsv[year]):
			fn = "data/rbsa%d-%d" % (year,n)
			csvname = fn + '.csv'
			if not os.path.exists(csvname):
				utility.debug(2,"%s not found" % csvname)
				zipname = fn + ".zip"
				utility.message("Extracting %s..."%zipname)
				os.system("unzip -d data %s"%zipname)
			utility.message("Loading %s..."%csvname)
			c = pd.read_csv(csvname, converters={"time":utility.get_datetime})
			h = list(map(lambda x: int(x.timestamp()/3600),c["time"]))
			# ymdh = list(map(lambda x: datetime.datetime(x.year,x.month,x.day,x.hour,0,0),c["time"]))
			c.insert(0,"hour",h)
			c.set_index(["hour","siteid"],inplace=True)
			eus = utility.get_enduses(c);
			d = None
			for eu,cols in utility.get_enduses(c).items():
				cd = c[cols].groupby(["hour"]).sum()
				yy = pd.DataFrame({"sites":cd.count(axis=1),eu:cd.mean(axis=1)},index=h)
				if d is None :
					d = yy
				else:
					d.insert(len(d.columns),eu,yy[eu])
			utility.debug(2,"%s is %.2f GB" % (csvname,sys.getsizeof(d)/1.0e9))
			if type(data) == type(None):
				data = d
			else:
				data = data.append(d)
		self.data = data
		utility.debug(1,"total size is %.2f GB" % (sys.getsizeof(data)/1.0e9))

rbsa(1).data.to_csv("output/rbsa.csv")