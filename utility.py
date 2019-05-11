import sys, os, traceback
if not ( sys.version_info[0]>=3 and sys.version_info[1]>=7 ):
	raise Exception("rbsa.py: %s is not supported" % str(sys.version_info))
try:
	import config
except:
	config = {}

def in_context(msg,level=-3):
	call = traceback.extract_stack()[level]

	return "%s(%s:%d): %s" % (call.name,call.filename.replace(os.getcwd()+"/",""),call.lineno,msg)

def debug(level,msg):
	if hasattr(config,"debug") and config.debug > level :
		print("DEBUG %s" % in_context(msg),flush=True)

def message(msg) :
	if not hasattr(config,"quiet") or config.quiet == False :
		print(msg,flush=True)

###
### RBSA datetime conversion
###
import datetime
def get_datetime(ts):
	return datetime.datetime.strptime(ts,"%d%b%y:%H:%M:%S")

###
### RBSA enduse identification
###
def get_enduse(column_name):
	p0 = column_name.find("(")
	p1 = column_name.find(")")
	if p0 > 0 and p1 > p0:
		d = column_name[0:p0].strip()
		e = column_name[p0+1:p1].strip()
		return {"name":column_name,"device":d, "enduse":e}
	else:
		return {"name":column_name}

def get_enduses(df):
	enduses = {}
	for n in df.columns:
		if not n in ["siteid","time"]:
			e = get_enduse(n)
			if "enduse" in e.keys():
				eu = e["enduse"]
				if not eu in enduses.keys():
					enduses[eu] = []
			enduses[eu].append(e["name"])
	return enduses