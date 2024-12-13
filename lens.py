import streamlit as st
import pandas as pd
from cyancameralens import CameraLens
class Lens():
	def __init__(self):
		self.df         = pd.DataFrame()
		self.view       = LensTabView()
		self.cameralens = CameraLens()
	def setdf(self,df):
		def columns():
			def lensCategory(row):
				return self.cameralens.cameraLens_category(row["Type"])
			def user_lensControl(row):
				return self.cameralens.options_needs_init[row["CameraLensCategory"]][0]
			def user_lensType(row):
				return self.cameralens.options_needs_init[row["CameraLensCategory"]][1]
			def user_lensMotor(row):
				return self.cameralens.options_needs_init[row["CameraLensCategory"]][2]
			self.df["CameraLensCategory"] = self.df.apply(lensCategory,axis=1)
			self.df["lensControl"]= self.df.apply(user_lensControl,axis=1)
			self.df["lensType"]   = self.df.apply(user_lensType,axis=1)
			self.df["lensMotor"]  = self.df.apply(user_lensMotor,axis=1)
		if df.empty:
			pass
		else:
			self.df = df
			columns()
# TAB LENS
class LensTabView():
	def __init__(self):
		pass
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
							options = pool.cameralens.options_needs_lensControl[cameraLensCategory],
							# options = st.session_state.property.constraints[(cameraLensCategory,'LensControls')],
							#options=st.session_state.property.options['LensUserControls'],
							required = True),
						'lensType':  st.column_config.SelectboxColumn(
							"Type of Lens",
							help="Main characteristics of the lens",
							# width="medium",
							#options = st.session_state.property.options['LensTypes'],
							options = pool.cameralens.options_needs_lensType[cameraLensCategory],
							# options=st.session_state.property.constraints[(cameraLensCategory,'LensTypes')],
							required = True),
						'lensMotor':  st.column_config.SelectboxColumn(
							"Motorization",
							help="Type of motorization",
							# width="small",
							options = pool.cameralens.options_needs_motorType[cameraLensCategory],
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
		pool = st.session_state.lens
		blocks = {}
		#cameraLensCategory est l'élément de sélection
		if 'LensTypes' not in pool.df.columns:
			pool.df['LensTypes']=""
		cameraLensCategories = pool.df["CameraLensCategory"].unique()
		pool.df.to_csv('debug_pool_display_lens.csv', index=False)
		#print("################CAMERAS LENS CATEGORIES  :",cameraLensCategories)
		for cameraLensCategory in cameraLensCategories:
			#filter instance dataframe by type
			selected_rows = pool.df.loc[pool.df['CameraLensCategory'] == cameraLensCategory]
			if not selected_rows.empty :
				st.markdown(cameraLensCategory)
				#??? NO USE?? constraints = Lens.filter_constraints(cameraLensCategory)
				blocks[cameraLensCategory] = edit_camera_lens(selected_rows,cameraLensCategory)
		print("blocks.values:",list(blocks.values()))
		if list(blocks.values()) != []:
			final_df = pd.concat(list(blocks.values()))
		return final_df
    
if __name__  == "__main__":
	test = Lens()
