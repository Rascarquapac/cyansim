import pandas as pd
class Network():
	def __init__(self):
		self.df = pd.DataFrame()
	def setdf(self, df):
		if df.empty:
			pass
		else:
			self.df = df
