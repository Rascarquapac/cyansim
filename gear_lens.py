import pandas as pd
import constants as cst 
from constants import CameraCategory as CameraCategory
# Should be part of cyangear Constants object
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

class CameraLensGraph():
    def __init__(self,index,row) -> None:
        #convert columns into attributes
        self.df_index  = index
        self.reference = row['Reference']
        self.protocol  = row['Protocol']
        self.camera_id = row['Camera_id'] 
        self.device_id = row['Device_id'] 
        self.cable     = row['Cable']
        self.device    = row['Device']
        #lensControl,lensType,lensMotor
        self.lensControl = row['lensControl']
        self.lensType    = row['lensType']
        self.lensMotor   = row['lensMotor']
        #LensCable,MotorCable,LensMotor
        self.llensCable  = row['LensCable']
        self.lmotorCable = row['MotorCable']
        self.llensMotor  = row['LensMotor']
        self.camLensCat  = row['CameraLensCategory']
        self.code = self.mermaid()
    def mermaid(self):
        def clean(code):
            return(code.replace(' ', ''))
        device_id   = clean(self.device_id)
        camera_id   = clean(self.camera_id)
        cable       = clean(self.cable)
        lens_cable  = clean(self.llensCable)
        camera_name = self.reference + camera_id.split('_',-1)[-1]
        lens_type   = clean(self.lensType) 
        lens_id     = f'{lens_type}_{camera_id}'
        code = ''
        header = f"%% CameraCategory:{self.camLensCat}, LensControl:{self.lensControl}, LensType:{self.lensType}\n"
        subgraph_start = ''
        subgraph_end   = ''
        lens2device    = ''
        match (self.camLensCat,self.lensControl,self.lensType):
            case (CameraCategory.IZF_INTEGRATED.value,lensControl,lensType):   
                dbg_code = f"%%DBG: CameraCategory.IZF_INTEGRATED branch\n"      
                lens2camera   = lens_id + '<==>' + camera_id+'\n'
                camera2device = camera_id + '<-->' + '|' + cable + '|' + device_id+'\n'
                lens2device   = ''
                lens_node   = f"{lens_id}@{{ shape: stadium, label: {lens_type} }}\n"
                camera_node = f"{camera_id}@{{ shape: hex, label: {camera_name}  }}\n"
            case (CameraCategory.FIXED_LENS.value,lensControl,lensType):
                dbg_code = f"%%DBG: CameraCategory.FIXED_LENS branch\n"
                lens2camera   = f"%%INF: No lens displayed\n"
                camera2device = camera_id +  '<-->' + '|' + cable + '|' + device_id+'\n'
                lens2device   = ''
                camera_node = f"{camera_id}@{{ shape: hex, label: {camera_name}  }}\n"
                lens_node   = ""
            case _:
                dbg_code = f"%%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch\n"
                lens2camera   = lens_id + '<==>' + camera_id+'\n'
                camera2device = camera_id +  '<-->' + '|' + cable + '|' + device_id+'\n'
                if self.lensType != 'TBD' and self.llensCable != 'No cable' :
                    lens2device = lens_id + '<-->' + '|' + lens_cable + '|' + device_id+'\n'
                else:
                    lens2device = f'%%INF: No lens cable displayed\n'
                # SUBGRAPH
                self.subgraph_id   = f'{clean(self.camera_id)}_cameralens'
                if self.lensControl   == 'No Need': self.subgraph_title = 'NO Remote Control Request'
                elif self.lensControl == 'Iris':  self.subgraph_title = 'Iris Remote Control Request'
                elif self.lensControl == 'IZF':   self.subgraph_title = 'I+Z+F Remote Control Request'
                else:                             self.subgraph_title = self.lensControl
                subgraph_start = f'  subgraph {self.subgraph_id} [{self.subgraph_title}]\n'
                subgraph_end   = '  end\n'
                camera_node = f"{camera_id}@{{ shape: hex, label: {camera_name}  }}\n"
                if self.lensType != 'TBD' and self.llensCable != 'No Cable' :
                    lens_node = f"{lens_id}@{{ shape: stadium, label: {lens_type} }}\n"
                else:
                    lens_node = f"{lens_id}@{{ shape: stadium, label: {lens_type} }}\n"
                    # code += f'    {lens_id}@{{ img: "https://i.imgur.com/ctZI7sm.png", h: 50, w: 100, pos: "b", constraint: "on"}}\n'
        code += '    ' + dbg_code 
        code += '    ' + header 
        code += '     ' + camera2device 
        code += '     ' + lens2camera
        code += '     ' + lens2device
        code += '     ' + subgraph_start
        code += '       ' + lens_node
        code += '       ' + camera_node 
        code += '     ' + subgraph_end
        return code

