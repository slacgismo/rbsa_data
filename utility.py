import sys, os, traceback
if not ( sys.version_info[0]>=3 and sys.version_info[1]>=7 ):
	raise Exception("rbsa.py: %s is not supported" % str(sys.version_info))
try:
	import config
except:
	config = None

def in_context(msg,level=-3):
	call = traceback.extract_stack()[level]

	return "%s(%s:%d): %s" % (call.name,call.filename.replace(os.getcwd()+"/",""),call.lineno,msg)

def debug(level,msg):
	if hasattr(config,"debug") and config.debug > level :
		print("DEBUG %s" % in_context(msg),flush=True)

def message(msg) :
	if not hasattr(config,"quiet") or config.quiet == False :
		print(msg,flush=True)
