import pandas as pd
import streamlit as st
from pprint import pprint
from streamlit_gsheets import GSheetsConnection
from logger_config import setup_logger
from constants import LensMountType, CameraType, NetworkType
logger = setup_logger()

class Descriptor():
    def __init__(self,updateFromGsheet=True,debug=False):
        self.pickel_filename = "./data/cameras.pkl"
        self.df  = self.load(updateFromGsheet)
        self.check_values()

    def load(self,update):
        if update:
            cameras_df = self.get_camera_gsheet()
            proto_df   = self.get_protocol_gsheet()
            cameras_df = self.build_camera_set(cameras_df,proto_df)
            self.set_pickel_camera(cameras_df)
        else:
            try:
                cameras_df = self.get_camera_pickle()
            except:
                cameras_df = self.get_camera_gsheet()
                proto_df   = self.get_protocol_gsheet()
                cameras_df = self.build_camera_set(cameras_df,proto_df)
                self.set_pickel_camera(cameras_df)
        return(cameras_df)

    def get_camera_gsheet(self):
        conn = st.connection("cameras", type=GSheetsConnection)
        cam_df = conn.read(usecols=[
            'Model','Reference','Protocol','Brand','ManufacturerURL','Remark',"LensMount"])        
            # cameraType is missing in the listed column names but is present in gsheet as a protocol property 
            #   (suppress in it in gsheet or color it: not user modificable?)
            # cameraLensControl is missing in the listed column names but is present in gsheet but can be computed from camera type
            #   (suppress in it in gsheet or color it: not user modificable?)
        cam_df['Name'] = cam_df['Model']
        logger.info("Descriptor-->Cameras table successfully loaded from Gsheet")
        return cam_df
    
    def get_protocol_gsheet(self): 
        conn = st.connection("protocols", type=GSheetsConnection)
        proto_df = conn.read(usecols=[
            "Protocol","Brand","Type","Cable","SupportURL","Message","MaxDelayToComplete","ControlCoverage","Bidirectionnal"])
        # PROFILE THE CAMERA POOL
        del proto_df['Brand']
        logger.info("Descriptor-->Protocols table successfully loaded from Gsheet")
        return proto_df

    def build_camera_set(self,cam_df,proto_df):
        # LEFT JOIN FOR COMBINING CAMERAS AND PROTOCOLS DATA
        camera_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
        # FILL NAN  VALUES
        camera_df['MaxDelayToComplete'] = camera_df['MaxDelayToComplete'].fillna(500)
        camera_df['ControlCoverage'] = camera_df['ControlCoverage'].fillna(0)
        camera_df['Brand']    = camera_df['Brand'].fillna("")
        camera_df['Cable']    = camera_df['Cable'].fillna("")
        camera_df['Protocol'] = camera_df['Protocol'].fillna("")
        # check value as string but could be check as a more precise value type
        camera_df['ManufacturerURL'] = camera_df['ManufacturerURL'].fillna("")
        camera_df['Remark']          = camera_df['Remark'].fillna("")
        camera_df['SupportURL']      = camera_df['SupportURL'].fillna("")
        camera_df['Message']         = camera_df['Message'].fillna("")
        # CONVERTING COLUMN VALLUES
        camera_df['Bidirectionnal']     = camera_df['Bidirectionnal'].apply(lambda x: False if x == "No" else True)
        camera_df['MaxDelayToComplete'] = camera_df['MaxDelayToComplete'].apply(lambda x: int(x))
        camera_df['ControlCoverage']     = camera_df['ControlCoverage'].apply(lambda x: int(x))
        # ADDING COLUMNS
        camera_df['Number']   = 0
        camera_df['Selected'] = False
        camera_df['Network']  = NetworkType.LAN_WIRED.value
        print("Lan wired",NetworkType.LAN_WIRED.value)
        return camera_df

    def set_pickel_camera(self,cameras_df):
        cameras_df.to_pickle(self.pickel_filename)

    def get_camera_pickle(self):
        return pd.read_pickle(self.pickel_filename)

    def check_values(self):
        incorrect = {}
        # check value as calue attribute of StrEnum subclass
        condition = lambda x: x in CameraType._value2member_map_
        if not bool(self.df['Type'].apply(lambda x: condition(x)).all()):            
            incorrect['Type'] = self.df['Type'].apply(lambda x: condition(x)).index[~self.df['Type'].apply()]
        else: 
            incorrect['Type'] = False
        condition = lambda x: x in LensMountType._value2member_map_
        if not bool(self.df['LensMount'].apply(lambda x: condition(x)).all()):            
            incorrect['LensMount'] = self.df['LensMount'].apply(lambda x: condition(x)).index[~self.df['LensMount'].apply()]
        else: 
            incorrect['LensMount'] = False
        condition = lambda x: x in NetworkType._value2member_map_
        if not bool(self.df['Network'].apply(lambda x: condition(x)).all()):            
            incorrect['NetworkType'] = self.df['Network'].apply(lambda x: condition(x)).index[~self.df['Network'].apply()]
        else: 
            incorrect['NetworkType'] = False
        # check value as boolean
        condition = lambda x: isinstance(x,bool)
        if not bool(self.df['Bidirectionnal'].apply(lambda x: condition(x)).all()):
            incorrect['Bidirectionnal'] = self.df['Bidirectionnal'].apply(lambda x: condition(x)).index[~self.df['Bidirectionnal'].apply()]
        else:
            incorrect['Bidirectionnal'] = False
        if not bool(self.df['Selected'].apply(lambda x: condition(x)).all()):
            incorrect['Selected'] = self.df['Selected'].apply(lambda x: condition(x)).index[~self.df['Selected'].apply()]
        else:
            incorrect['Selected'] = False
        # check value as integer
        condition = lambda x: isinstance(x,int)
        if not bool(self.df['MaxDelayToComplete'].apply(lambda x: condition(x)).all()):
            incorrect['MaxDelayToComplete'] = self.df['MaxDelayToComplete'].apply(lambda x: condition(x)).index[~self.df['MaxDelayToComplete'].apply()]
        else:
            incorrect['MaxDelayToComplete'] = False
        if not bool(self.df['ControlCoverage'].apply(lambda x: condition(x)).all()):
            incorrect['ControlCoverage'] = self.df['ControlCoverage'].apply(lambda x: condition(x)).index[~self.df['ControlCoverage'].apply()]
        else:
            incorrect['ControlCoverage'] = False
        if not bool(self.df['Number'].apply(lambda x: condition(x)).all()):           
            incorrect['Number'] = self.df['Number'].apply(lambda x: condition(x)).index[~self.df['Number'].apply()]   

        # check value as string but could be check as value of an Enum
        self.df['Brand']    = self.df['Brand'].astype(str)
        self.df['Cable']    = self.df['Cable'].astype(str)
        self.df['Protocol'] = self.df['Protocol'].astype(str)
        # check value as string but could be check as a more precise value type
        self.df['ManufacturerURL'] = self.df['ManufacturerURL'].astype(str)
        self.df['Remark']          = self.df['Remark'].astype(str)
        self.df['SupportURL']      = self.df['SupportURL'].astype(str)
        self.df['Message']         = self.df['Message'].astype(str)

        # Error analysis if any
        check_ok = True
        pprint(incorrect)
        if not all(incorrect.values()):
            for key in incorrect.keys():
                if incorrect[key]:
                    check_ok = False
                    logger.error(f"Descriptor-->Bad type for {key} in rows {incorrect[key]}, model {self.df.loc[incorrect[key]]['Model']}")
        if check_ok:
            logger.info("Descriptor-->All values have the correct type")
        else:
            st.write("Check the values of the DataFrame")
            st.write(self.df)
  
if __name__ == "__main__":
    descriptor = Descriptor()
    descriptor.df.to_csv("./debug/descriptor_df.csv")
    # Summary of the DataFrame 
    print("\nInfo summary:") 
    descriptor.df.info() 
    # Display the first few rows 
    head_summary = descriptor.df.head() 
    print("\nFirst few rows of the DataFrame:") 
    print(head_summary) 
    # Display the last few rows
    tail_summary = descriptor.df.tail() 
    print("\nLast few rows of the DataFrame:") 
    print(tail_summary) 
    # Shape of the DataFrame 
    shape_summary = descriptor.df.shape 
    print("\nShape of the DataFrame:") 
    print(shape_summary) 
    # Column names of the DataFrame 
    columns_summary = descriptor.df.columns 
    print("\nColumn names of the DataFrame:") 
    print(columns_summary)