import streamlit as st
import json 
import pandas as pd
import constants as cst 
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

class PoolLens():
    # def __init__(self,df_index,reference,protocol,cable) -> None:
    def __init__(self) -> None:
        self.camera_types = [member.value for member in cst.CameraType]
        self.camera_types = ["BBlock","CineStyle","Handheld Camcorder","Minicam","Minicam Motorizable","Minicam IZT","Mirrorless","PTZ","Shoulder Camcorder","Slow Motion","System","TBD"]
        self.camera_categories = ['Broadcast','Cine Interchangeable','IZF Integrated','Fixed Lens','Minicam Motorizable Lens','TBD' ]
        # User options of IZF control per camera category
        self.options_needs_lensControl={
             'Broadcast':['No Need','Iris','IZF'],
             'Cine Interchangeable':['No Need','Iris','IZF'],
             'IZF Integrated':['IZF'],
             'Fixed Lens':['No Need'],
             'Minicam Motorizable Lens':['No Need','IZF'],
             'TBD' :["No Need"]
        }
        # User options of lens type per camera category
        self.options_needs_lensType={
             'Broadcast':['B4-Mount'],
             'Cine Interchangeable':['B4-Mount','E-Mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD'],
             'IZF Integrated':['Camera Integrated'],
             'Fixed Lens':['Manual'], # "Manual" only ?
             'Minicam Motorizable Lens':['Manual'],
             'TBD' :["No Need"]
        }
        # User options of motor type per camera category
        self.options_needs_motorType={
             'Broadcast':['No extra motors'],
             'Cine Interchangeable':['No extra motors','Tilta','Arri','TBD'],
             'IZF Integrated':['Camera Integrated'],
             'Fixed Lens':['Manual'], # "Manual" only ?
             'Minicam Motorizable Lens':['No extra motors','Dreamchip'],
             'TBD' :['No extra motors']
        }
        # Initial values for user options per camera category (lensControl,lensType,motorType)
        self.options_needs_init = {
            "Broadcast" : ('No Need','B4-Mount','No extra motors'),
            "Cine Interchangeable" : ('No Need','TBD','TBD'),
            "IZF Integrated" : ('IZF','Camera Integrated','No extra motors'),
            "Fixed Lens" : ("No Need",'Manual','No extra motors'),
            'Minicam Motorizable Lens' : ("No Need",'Manual','No extra motors'),
            "TBD" : ("No Need",'Manual','No extra motors')
        }
                # case "Broadcast": return ('No Need','B4-Mount','No extra motors')
                # case "Cine Interchangeable": return ('No Need','TBD','TBD')
                # case "IZF Integrated": return ('IZF','Camera Integrated','No extra motors')
                # case "Fixed Lens": return ("No Need",'Fixed and Manual','No extra motors')
                # case "TBD": return ("No Need",'Fixed and Manual','No extra motors')
    @classmethod
    def cameraLens_category(self,cameraType):
        # cameraMount can be suppressed except for exception
        match (cameraType):
            case ("TBD") : cameraLensCategory = "TBD"
            case ("Slow Motion") | ("System")|("BBlock")|("Shoulder Camcorder") : cameraLensCategory = "Broadcast"
            case ("CineStyle")|("Mirrorless")       : cameraLensCategory = "Cine Interchangeable"
            case ("PTZ") | ("Handheld Camcorder")|("Minicam IZT")   : cameraLensCategory = "IZF Integrated"
            case ("Minicam")    : cameraLensCategory = "Fixed Lens"
            case ("Minicam Motorizable") : cameraLensCategory = "Minicam Motorizable Lens"
            case _: raise KeyError(f"cameraType= {cameraType}")
        return cameraLensCategory
	
    # Select camera cable + lens cable + lens motor from user needs in Cyanview control
