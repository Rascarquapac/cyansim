import streamlit as st
import pandas as pd
from debug import Debug
class ViewLens():
	def __init__(self,pool):
		self.pool       = pool
		self.debug      = Debug(data=self.pool.df,mode='pool',debug_rec=False,debug_load=False)
	def edit(self):
		def edit_camera_lens(df,cameraLensCategory):
			if (len(df.index) != 0): 
				df = st.data_editor(
					df,
					column_config={
						"Type": "Type",
						"Reference": "Model",
						'Number':st.column_config.NumberColumn(
							"# Cams",
							help="How much camera of this type in your use-case (0-15)?",
							min_value=0,
							max_value=15,
							step=1,
							default=0,
							format="%d"),
						'lensControl': st.column_config.SelectboxColumn(
							"Lens Control",
							help= "Your needs for lens motorization",
							# width="small",
							options = self.pool.cameralens.options_needs_lensControl[cameraLensCategory],
							# options = st.session_state.property.constraints[(cameraLensCategory,'LensControls')],
							#options=st.session_state.property.options['LensUserControls'],
							required = True),
						'lensType':  st.column_config.SelectboxColumn(
							"Type of Lens",
							help="Main characteristics of the lens",
							# width="medium",
							#options = st.session_state.property.options['LensTypes'],
							options = self.pool.cameralens.options_needs_lensType[cameraLensCategory],
							# options=st.session_state.property.constraints[(cameraLensCategory,'LensTypes')],
							required = True),
						'lensMotor':  st.column_config.SelectboxColumn(
							"Motorization",
							help="Type of motorization",
							# width="small",
							options = self.pool.cameralens.options_needs_motorType[cameraLensCategory],
							# options = st.session_state.property.constraints[(cameraLensCategory,'LensMotors')],
							required=True),
						"Brand": "Brand",
						},
					disabled=['Reference','Brand','Number'],
					column_order=['Reference','lensControl','lensType','lensMotor','Brand','Number'],
					hide_index = True,
					use_container_width = True,
					)
				return(df)
		# self.pool.df = self.debug.load(data=self.pool.df)
		# print("POOL SET ------------------------------------------>")
		# print(self.pool.df)
		blocks = {}
		#cameraLensCategory est l'élément de sélection
		if 'LensTypes' not in self.pool.df.columns:
			self.pool.df['LensTypes']=""
		cameraLensCategories = self.pool.df["CameraLensCategory"].unique()
		self.pool.df.to_csv('debug_pool_display_lens.csv', index=False)
		#print("################CAMERAS LENS CATEGORIES  :",cameraLensCategories)
		for cameraLensCategory in cameraLensCategories:
			#filter instance dataframe by type
			selected_rows = self.pool.df.loc[self.pool.df['CameraLensCategory'] == cameraLensCategory]
			if not selected_rows.empty :
				st.markdown(cameraLensCategory)
				#??? NO USE?? constraints = Lens.filter_constraints(cameraLensCategory)
				blocks[cameraLensCategory] = edit_camera_lens(selected_rows,cameraLensCategory)
		# print("blocks.values:",list(blocks.values()))
		if list(blocks.values()) != []:
			final_df = pd.concat(list(blocks.values()))
		self.pool.df = final_df
		# print("POOL-------------------->")
		# print(self.pool.df)
		self.debug.record(data=self.pool.df,record=True,dump=True)
		return final_df
    
if __name__  == "__main__":
	test = ViewLens()
