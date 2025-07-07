import pandas as pd
import constants as cst 
from constants import CameraCategory as CameraCategory
from constants import CameraLens as CameraLens
# Should be part of cyangear Constants object
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

