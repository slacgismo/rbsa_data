import sys, os
import pandas as pd
import utility
import datetime

csvfiles = {
	2012: ['data/rbsa1-1.csv','data/rbsa1-2.csv','data/rbsa1-3.csv','data/rbsa1-4.csv'],
	2013: ['data/rbsa2-1.csv','data/rbsa2-2.csv','data/rbsa2-3.csv','data/rbsa2-4.csv','data/rbsa2-5.csv']
}
class rbsa:
	def __init__(self,year):
		self.data = None
		if not year in csvfiles.keys():
			raise Exception("year=%d is not a valid RBSA year" % (year))
		for csvname in csvfiles[year]:
			if not os.path.exists(csvname):
				utility.debug(2,"%s not found" % csvname)
				zipname = csvname.replace(".csv",".zip")
				utility.message("Extracting %s..."%zipname)
				os.system("unzip -d data %s"%zipname)
			utility.message("Loading %s..."%csvname)
			c = pd.read_csv(csvname, converters={"time":rbsa.get_datetime},nrows=100)
			utility.debug(2,"%s is %.2f GB" % (csvname,sys.getsizeof(c)/1.0e9))
			h = list(map(lambda x: int(x.timestamp()/3600),c["time"]))
			ymdh = list(map(lambda x: datetime.datetime(x.year,x.month,x.day,x.hour,0,0),c["time"]))
			hod = list(map(lambda x: x.hour,ymdh))
			dow = list(map(lambda x: x.weekday,ymdh))
			moy = list(map(lambda x: x.month,ymdh))
			c.insert(0,"hour",h)
			c.insert(1,"hod",hod)
			c.insert(2,"dow",dow)
			c.insert(3,"moy",moy)
			c.set_index(["hour","siteid"],inplace=True)
			eus = rbsa.get_enduses(c)
			d = None
			for eu,cols in eus.items():
				cd = c[cols].groupby(["hour"]).sum()
				yy = pd.DataFrame({"sites":cd.count(axis=1),eu:cd.mean(axis=1)},index=h)
				if d is None :
					d = yy
				else:
					d.insert(len(d.columns),eu,yy[eu])
			utility.debug(2,"dataframe is %.2f GB" % (sys.getsizeof(d)/1.0e9))
			if type(self.data) == type(None):
				self.data = d
			else:
				self.data = self.data.append(d)
		utility.debug(1,"RBSA size is %.2f GB" % (sys.getsizeof(self.data)/1.0e9))

	###
	### RBSA datetime conversion
	###
	@staticmethod
	def get_datetime(ts):
		return datetime.datetime.strptime(ts,"%d%b%y:%H:%M:%S")

	###
	### RBSA enduse identification
	###
	@staticmethod
	def get_enduse(column_name):
		p0 = column_name.find("(")
		p1 = column_name.find(")")
		if p0 > 0 and p1 > p0:
			d = column_name[0:p0].strip()
			e = column_name[p0+1:p1].strip()
			return {"name":column_name,"device":d, "enduse":e}
		else:
			return {"name":column_name}

	@staticmethod
	def get_enduses(df):
		enduses = {}
		for n in df.columns:
			if not n in ["siteid","time","hour","hod","dow","moy"]:
				e = rbsa.get_enduse(n)
				if "enduse" in e.keys():
					eu = e["enduse"]
					if not eu in enduses.keys():
						enduses[eu] = []
				enduses[eu].append(e["name"])
		return enduses		

rbsa(2012).data.to_csv("output/rbsa.csv",index_label="hour",float_format="%.4g")