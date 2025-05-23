import streamlit as st
import json 
import pandas as pd
from debug import Debug
import constants as cst 
from constants import CameraCategory as CameraCategory
class CameraLens():
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
    # Select camera cable + lens cable + lens motor from user needs in Cyanview control
    @classmethod
    def adapter(self,parameters):
        def check(parameters):
            (cameraType,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
            ## DUPLICATE !!!!
            if cameraType not in ["BBlock","CineStyle","Handheld Camcorder","Minicam","Minicam Motorizable","Minicam IZT","Mirrorless","PTZ","Shoulder Camcorder","Slow Motion","System","TBD"]:
                raise KeyError(f"cameraType= {cameraType}")
            # if cameraMount not in ['B4-Mount','C-Mount','E-Mount','S-Mount','EF-Mount','MFT-Mount','RF-Mount','LPL-Mount','PL-Mount','LNE-Mount','L-Mount','No-Xchange-Manual','No-Xchange-Motorized','TBD']:
            #     raise KeyError(f"cameraMount= {cameraMount}")
            if lensControl not in ['No Need','Iris','IZF']:
                raise KeyError(f"lensControl= {lensControl}")
            if lensType not in ['B4-Mount','E-Mount','Cabrio','Cineservo','Primelens','Motorized Others','Camera Integrated','Manual','No Need','TBD']:
                raise KeyError(f"lensType= {lensType}")
            if lensMotor not in ['No extra motors','Tilta','Arri','Dreamchip','TBD']:
                raise KeyError(f"lensMotor= {lensMotor}")
            return
        (cameraType,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
        check(parameters)
        # define constant values
        (no_cable,cable_B4,cable_tilta,cable_fuji,cable_arri) = ("No cable","CY-CBL-6P-B4-02","CY-CBL-6P-TILTA-SERIAL","CY-CBL-6P-FUJI-02","ARRI CForce cable")
        (no_motor,motor_arri,motor_tilta,motor_dreamchip) = ("No motor","Arri","Tilta","Dreamchip")
        # Set cameraLensCategory
        cameraLensCategory = self.cameraLens_category(cameraType)
        # Set cables and motors
        # print("\nDBG CameraLens.adapter parameters=",parameters,cameraLensCategory)
        match (cameraLensCategory,cameraBrand,cameraModel,lensControl,lensType,lensMotor):
            # No Cyanview lens control is needed
            case(a,b,c,"No Need",e,f) : 
                result = (no_cable,no_cable,no_motor,"No lens control by Cyanview is requested by the user")
            # Broadcast camera have a B4-mount
            case ("Broadcast",b,c,"Iris",e,f) : 
                result = (no_cable,no_cable,no_motor,"The lens iris is controllable trhough the camera protocol. No extra cable is required")
            case ("Broadcast",b,c,"IZF",e,f)  : 
                result = (cable_B4,no_cable,no_motor,"The lens iris is controllable trhough the camera protocol but an extra B4 cable is required to control Zoom and Focus")
            #  Camera with no lens interchange cannot be controlled
            case ("IZF Integrated",b,c,d,e,f)    : 
                result = (no_cable,no_cable,no_motor,"The lens could not be interchanged and lens could be controlled through the camera prorocol")
            #  Camera with no lens interchange cannot be controlled
            case ("Fixed Lens",b,c,d,e,f)    : 
                result = (no_cable,no_cable,no_motor,"The lens could not be interchanged and there is probably no motor solution for this case")
            # CineStyle, Mirrorless, Mini camera with lens interchange
            # Canon cameras and (Cineservo or B4-Mount)
            case ("Cine Interchangeable","Canon",c,d,"Cineservo",f) : 
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
            case ("Cine Interchangeable","Canon",c,d,"B4-Mount",f) : 
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
            # URSA cameras and (Cineservo or B4-Mount)
            case ("Cine Interchangeable",b,"URSA",d,"Cineservo",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera")
            case ("Cine Interchangeable",b,"URSA",d,"B4-Mount",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera") 
            # (Neither URSA nor Canon cameras) and (Cineservo or B4-Mount)
            case ("Cine Interchangeable",b,c,"Iris","Cineservo",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
            case ("Cine Interchangeable",b,c,"IZF","Cineservo",f) :
                result =(cable_B4,no_cable,no_motor,"Cyanview B4 adapter is require for Zoom/Focus control")
            case ("Cine Interchangeable",b,c,"Iris","B4-Mount",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
            case ("Cine Interchangeable",b,c,"IZF","B4-Mount",f) :
                result =(cable_B4,no_cable,no_motor,"Cyanview B4 adapter is require for Zoom/Focus control")
            # E-Mount lens (only Sony cameras ??? XDE)
            case ("Cine Interchangeable",b,c,"Iris","E-mount",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
            case ("Cine Interchangeable",b,c,"IZF","E-mount",f) :
                result =(no_cable,cable_tilta,motor_tilta,"Adding Tilta motors and Cyanview Tilta adapter is required for Zoom/Focus control")
            # Cabrio lens
            case ("Cine Interchangeable",b,c,d,"Cabrio",f) : 
                result = (f'{cable_B4} +\n{cable_fuji}',no_motor,no_cable,"The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
            # Primelens (or… RTI) Motors
            case ("Cine Interchangeable",b,c,d,"Primelens","Tilta") : 
                result = (no_cable,cable_tilta,motor_tilta,"The user needs the control of Iris/Zoom/Focus, it cannot be done through the camera and the user want to use Tilta motors")
            case ("Cine Interchangeable",b,c,d,"Primelens","Arri") : 
                result = (no_cable,cable_arri,motor_arri,"The user needs the control of Iris/Focus, it cannot be done through the camera and the user want to use ARRI motors")
            case ("Cine Interchangeable","Dreamchip",c,d,e,"Dreamchip") : 
                result = (no_cable,no_cable,motor_dreamchip,"The user needs the control of Iris/Zoom and it can be done through the camera")
            case _: 
                result =(no_cable,no_cable,no_motor,"This case is probably not supported")
        # print("DBG CameraLens.adapter result=",result)  
        return result
        
    ########## FLAT ANALYZIS
        self.camera_type='TBD' 
        self.camera_category='TBD' 
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

class Pool:
	def __init__(self):
		self.df = pd.DataFrame()
		self.cameralens = CameraLens()
		self.debug = Debug()
		self.initcase_dict = {}
	def build(self,camera_pool):
		# Add columns intiating the Lens definition UI ("Tab Lens")
		def lensCategory(row):
			return self.cameralens.cameraLens_category(row["Type"])
		def user_lensControl(row):
			return self.cameralens.options_needs_init[row["CameraLensCategory"]][0]
		def user_lensType(row):
			return self.cameralens.options_needs_init[row["CameraLensCategory"]][1]
		def user_lensMotor(row):
			return self.cameralens.options_needs_init[row["CameraLensCategory"]][2]
		if camera_pool.empty:
			pass
		else:
			self.df = camera_pool
			self.df.loc[:,"CameraLensCategory"] = self.df.apply(lensCategory,axis=1)
			self.df.loc[:,"lensControl"]        = self.df.apply(user_lensControl,axis=1)
			self.df.loc[:,"lensType"]           = self.df.apply(user_lensType,axis=1)
			self.df.loc[:,"lensMotor"]          = self.df.apply(user_lensMotor,axis=1)

