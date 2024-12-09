import pandas as pd
import pickle
class Debug():
	def __init__(self,camera=False,network=False,lens=False,pool=False):
		pass
	def debug(self, data = None,mode=None,record=False,output=False,dump=False):
		if record: 
			filename = f"./debug/dbgimport_{mode}.pkl"
			if isinstance(data,dict):
				with open(filename, 'wb') as file:
					pickle.dump(data, file)
		elif isinstance(data,pd.DataFrame):
			data.to_pickle(filename)
		else:
			raise Exception
		if input:
			filename = f"./debug/dbgimport_{mode}.pkl"
			if isinstance(data,dict):
				with open(filename, 'rb') as file:
					data = pickle.load(file)
			elif isinstance(data,pd.DataFrame):
				data = pd.read_pickle(filename)
		else:
			raise Exception
		if dump:
			filename = f"./debug/dbgexport_{mode}.csv"
		elif isinstance(data,pd.DataFrame):
			self.data.to_csv(filename)
		else:
			raise Exception
	def camera(self, data = None,mode = None,record=False, pkl=False,output=False,dump=False):
		self.debug(data = data,mode = 'camera',record=record, output=output,dump=dump)
	def network(self, data = None,mode = None,record=False, pkl=False,output=False,dump=False):
		self.debug(data = data,mode = 'network',record=record, output=output,dump=dump)
	def lens(self, data = None,mode = None,record=False, pkl=False,output=False,dump=False):
		self.debug(data = data,mode = 'lens',record=record, output=output,dump=dump)
	def pool(self, data = None,mode = None,record=False, pkl=False,output=False,dump=False):
		self.debug(data = data,mode = 'camera',record=record, output=output,dump=dump)