import pandas as pd
import pickle
class Debug():
	def __init__(self, data = None,mode=None,debug_rec=False,debug_load=False):
		self.debug_rec  = debug_rec
		self.debug_load = debug_load
		self.data   = data
		self.mode   = mode
	def record(self,data=None,record=False,dump=False):
		if self.debug_rec == False:
			return
		if isinstance(data,pd.DataFrame):
			if data.empty:
				data = self.data
		elif data == None:
			data = self.data
		if record: 
			filename = f"./debug/dbgimport_{self.mode}.pkl"
			if isinstance(data,dict):
				with open(filename, 'wb') as file:
					pickle.dump(data, file)
			elif isinstance(data,pd.DataFrame):
				data.to_pickle(filename)
			else:
				raise Exception
		if dump:
			filename = f"./debug/dbgexport_{self.mode}.csv"
			if isinstance(data,pd.DataFrame):
				data.to_csv(filename)
			else:
				raise Exception
		return
	def load(self,data=None):
		if self.debug_load == False:
			return data
		if isinstance(data,pd.DataFrame):
			if data.empty:
				data = self.data
		elif data == None:
			data = self.data
		filename = f"./debug/dbgimport_{self.mode}.pkl"
		if isinstance(data,dict):
			with open(filename, 'rb') as file:
				data = pickle.load(file)
		elif isinstance(data,pd.DataFrame):
			data = pd.read_pickle(filename)
		else:
			raise Exception
		return data
