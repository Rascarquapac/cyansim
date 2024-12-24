import json
import os 
class Case():
	def __init__(self,camera=None,pool=None,active=False,filename="./data/xcase_initcase.json"):
		self.filename = filename
		self.pool   = pool
		self.camera = camera
		self.active = active
		self.initcase_dict = {}
		if active and os.path.exists(filename) : self.init_case()
	def init_case(self):
		def init_camera_df():
			if self.initcase_dict != {}:
				row_to_include = list(self.initcase_dict['Reference'].keys())
				# Add stored values
				for index in row_to_include:
					self.camera.df.loc[index,'Number']=self.initcase_dict['Number'][index]
			return
		def init_pool_df():
			self.pool.update(self.camera.df)
			if self.initcase_dict == {}:
				row_to_include = []
			else:	
				row_to_include = list(self.initcase_dict['Reference'].keys())
			for index in row_to_include:
				self.pool.df.loc[index,'Reference']  = self.initcase_dict['Reference'][index]
				self.pool.df.loc[index,'Number']     = self.initcase_dict['Number'][index]
				self.pool.df.loc[index,'Network']    = self.initcase_dict['Network'][index]
				self.pool.df.loc[index,'lensControl']= self.initcase_dict['lensControl'][index]
				self.pool.df.loc[index,'lensType']   = self.initcase_dict['lensType'][index]
				self.pool.df.loc[index,'lensMotor']  = self.initcase_dict['lensMotor'][index]
			return
		try:
			with open(self.filename, 'r') as json_file: 
				self.initcase_dict = json.load(json_file) 
		except:
			self.initcase_dict = {}
		if self.initcase_dict == {} : return
		init_camera_df()
		init_pool_df()
		return
	def save_case(self):
		if self.active :
			if not self.pool.df.empty:
				self.initcase_dict = self.pool.df[['Reference','Number','Network','lensControl','lensType','lensMotor']].to_dict()
				# Write dictionary to a JSON file 
				with open(self.filename, 'w') as json_file: 
					json.dump(self.initcase_dict, json_file,indent=4)
