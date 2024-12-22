import streamlit as st
import json 
import pandas as pd
from gear_lens import PoolLens
from debug import Debug
class Pool:
	def __init__(self):
		self.df = pd.DataFrame()
		self.cameralens = PoolLens()
		self.debug = Debug()
		self.initcase_dict = {}
	def update(self,camera_pool):
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
			self.df["lensControl"]        = self.df.apply(user_lensControl,axis=1)
			self.df["lensType"]           = self.df.apply(user_lensType,axis=1)
			self.df["lensMotor"]          = self.df.apply(user_lensMotor,axis=1)
		if camera_pool.empty:
			pass
		else:
			self.df = camera_pool
			columns()

