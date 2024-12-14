import pandas as pd
import constants as cst 
from constants import CameraCategories as CC
from pool import PoolLens
# Should be part of cyangear Constants object
class CameraLens():
    # Select camera cable + lens cable + lens motor from user needs in Cyanview control
    @classmethod
    def adapter(self,parameters):
        def check(parameters):
            print("Lens->lens_cable->check->PARAMETERS:\n",parameters)
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
        cameraLensCategory = PoolLens.cameraLens_category(cameraType)
        # Set cables and motors
        # print("\n_lens->lens_cable_selext->PARAMETERS: ",parameters)
        # print("\n_lens->lens_cable_selext->MATCH INPUT: ",(cameraLensCategory,cameraBrand,cameraModel,lensControl,lensType,lensMotor) )
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
        # print(f"_lens->lens_cable_selext->RESULT: {result}")
        return result
        
    ########## FLAT ANALYZIS
        self.camera_type='TBD' 
        self.camera_category='TBD' 
    # to be replaced by attribute
    def cameraLensCategories(self):
          return(["Broadcast","Cine Interchangeable","IZF Integrated","Fixed Lens","TBD"])

class CamLensBlock():
    def __init__(self,index,serie) -> None:
        self.df_index  = index
        self.reference = serie['Reference']
        self.protocol  = serie['Protocol']
        self.camera_id = serie['Camera_id'] 
        self.device_id = serie['Device_id'] 
        self.cable     = serie['Cable']
        self.device    = serie['Device']
        #lensControl,lensType,lensMotor
        self.lensControl = serie['lensControl']
        self.lensType    = serie['lensType']
        self.lensMotor   = serie['lensMotor']
        #LensCable,MotorCable,LensMotor
        self.llensCable  = serie['LensCable']
        self.lmotorCable = serie['MotorCable']
        self.llensMotor  = serie['LensMotor']
        self.camLensCat  = serie['CameraLensCategory']
        self.code = ''
        self.draw_1()
    def draw_0(self):
        def clean(code):
            return(code.replace(' ', ''))
        # Add to mermaid code LR edge from Camera to Cyanglue
        self.code += clean(self.camera_id) + '{{"' + clean(self.camera_id) + ' fa:fa-camera-retro"}}---|'+clean(self.cable) +'|'+clean(self.device_id)+'\n'
        # Add to mermaid code LR edge from lens to Cyanglue
        self.lens_id = f'{clean(self.lensType)}_{clean(self.camera_id)}'
        if self.lensType != 'TBD' and self.llensCable != 'No cable' :
            self.code += f'{self.lens_id}([{self.lensType}])---|{clean(self.llensCable)}|{clean(self.device_id)}\n'
        # Create subgraph parameters for camera + lens
        self.subgraph_id   = f'{clean(self.camera_id)}_cameralens'
        if self.lensControl == 'No Need':
            self.subgraph_title = 'No lens control required'
        elif self.lensControl == 'Iris':
            self.subgraph_title = 'Iris control required'
        elif self.lensControl == 'IZF':
            self.subgraph_title = 'Iris/Zoom/Focus control required'
        else:
            self.subgraph_title = self.lensControl
        # Add to mermaid code the camera-lens subgraph 
        self.code += f'  subgraph {self.subgraph_id} [{self.subgraph_title}]\n'
        self.code += f'    {clean(self.camera_id)}\n'
        if self.lensType != 'TBD' and self.llensCable != 'No Cable' :
            self.code += f'    {self.lens_id}\n'
        self.code += '  end\n'
    def draw_1(self):
        def clean(code):
            return(code.replace(' ', ''))
        device_id   = clean(self.device_id)
        camera_id   = clean(self.camera_id)
        cable       = clean(self.cable)
        camera_name = self.reference + camera_id.split('_',-1)[-1]
        lens_type   = clean(self.lensType) 
        lens_id = f'{lens_type}_{camera_id}'
        # print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x\n")
        # print(f'Camera Lens Category: {self.camLensCat} IZF_INTEGRATED.name: {CC.IZF_INTEGRATED.value}')
        match (self.camLensCat,self.lensControl,self.lensType):
            case (CC.IZF_INTEGRATED.value,lensControl,lensType):
                self.code += lens_id   + '([' + lens_type   + '])<-->'+camera_id+'\n'
                self.code += camera_id + '[' + camera_name + ']<-->|'+ cable +'|'+ device_id +'\n'
            case (CC.FIXED_LENS.value,lensControl,lensType):
                self.code += camera_id + '{{"' + camera_name + '"}}<-->|'+ cable +'|'+ device_id +'\n'
            case _:
                self.code += camera_id + '{{"' + camera_id + ' fa:fa-camera-retro"}}---|'+cable +'|'+device_id+'\n'
                # Add to mermaid code LR edge from lens to Cyanglue
                if self.lensType != 'TBD' and self.llensCable != 'No cable' :
                    self.code += f'{self.lens_id}([{self.lensType}])---|{clean(self.llensCable)}|{clean(self.device_id)}\n'
                # Create subgraph parameters for camera + lens
                self.subgraph_id   = f'{clean(self.camera_id)}_cameralens'
                if self.lensControl == 'No Need':
                    self.subgraph_title = 'No lens control required'
                elif self.lensControl == 'Iris':
                    self.subgraph_title = 'Iris control required'
                elif self.lensControl == 'IZF':
                    self.subgraph_title = 'Iris/Zoom/Focus control required'
                else:
                    self.subgraph_title = self.lensControl
                # Add to mermaid code the camera-lens subgraph 
                self.code += f'  subgraph {self.subgraph_id} [{self.subgraph_title}]\n'
                self.code += f'    {camera_id}\n'
                if self.lensType != 'TBD' and self.llensCable != 'No Cable' :
                    self.code += f'    {lens_id}\n'
                self.code += '  end\n'
