import json
# 
class Case():
	def __init__(self,camera=None,pool=None,active=False,filename="initcase.json"):
		self.filename = filename
		self.pool   = pool
		self.camera = camera
		self.active = active
		self.initcase_dict = {}
		if active : self.init_case()
	def init_case(self):
		def init_camera_df():
			# Updating camera.df will create camera.selected in self.display() 
			print("CAMERA->INIT_SELECT->camera.selected: start ---------->:\n",self.camera.selected)
			if self.initcase_dict != {}:
				print("CAMERA->INIT_SELECT: init_dict[Reference] ",self.initcase_dict.keys())
				row_to_include = list(self.initcase_dict['Reference'].keys())
				# Add stored values
				for index in row_to_include:
					self.camera.df.loc[index,'Number']=self.initcase_dict['Number'][index]
				print("CAMERA->INIT_SELECT camera.selected: end ---------->:\n",self.camera.selected)
			return
		def init_pool_df():
			print("POOL->INIT_POOL->start: CAMERA_DF---------->:\n",self.pool.df)
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
			print("POOL->INIT_POOL->: end POOL.DF---------->:\n",self.pool.df)
			print("POOL->INIT_CASE: start")
			return
		try:
			print("POOL->INIT_CASE: initlaisizing seld.initcase_dict with JSON file")
			with open(self.filename, 'r') as json_file: 
				self.initcase_dict = json.load(json_file) 
		except:
			print(f"File {self.filename} describing init case does not exist")
			self.initcase_dict = {}
		if self.initcase_dict == {} : return
		init_camera_df()
		init_pool_df()
		print("POOL->INIT_CASE: End")
		return
	def save_case(self):
		if self.active :
			print("POOL.SAVE_CASE: POOL.DF before creating initcase_dict... --------------->\n",self.pool.df)
			if not self.pool.df.empty:
				self.initcase_dict = self.pool.df[['Reference','Number','Network','lensControl','lensType','lensMotor']].to_dict()
				print("POOL.SAVE_CASE: INITCASE_DICT;\n",self.initcase_dict["Reference"])
				# Write dictionary to a JSON file 
				with open(self.filename, 'w') as json_file: 
					json.dump(self.initcase_dict, json_file,indent=4)
			print("POOL.SAVE_CASE: end, self.initcase_dict -->\n",self.initcase_dict)
