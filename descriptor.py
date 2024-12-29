import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from constants import LensMountType, CameraType, NetworkType
class Descriptor():
    def __init__(self,updateFromGsheet=True,debug=False):
        self.df  = self.load(updateFromGsheet)
        self.check_values()
        self.pickel_filename = "./data/cameras.pkl"
    def load(self,update):
        def gsheet():
            conn = st.connection("cameras", type=GSheetsConnection)
            cam_df = conn.read(usecols=[
                'Model','Reference','Protocol','Brand','ManufacturerURL','Remark',"LensMount"])        
                # cameraType is missing in the listed column names but is present in gsheet as a protocol property 
                #   (suppress in it in gsheet or color it: not user modificable?)
                # cameraLensControl is missing in the listed column names but is present in gsheet but can be computed from camera type
                #   (suppress in it in gsheet or color it: not user modificable?)
            conn = st.connection("protocols", type=GSheetsConnection)
            proto_df = conn.read(usecols=[
                "Protocol","Brand","Type","Cable","SupportURL","Message","MaxDelayToComplete","ControlCoverage","Bidirectionnal"])
            # PROFILE THE CAMERA POOL
            del proto_df['Brand']
            cam_df['Name'] = cam_df['Model']
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
            camera_df.to_pickle("./data/cameras.pkl")
            return camera_df
        def pickel_file():
            return pd.read_pickle(self.pickel_filename)
        if update:
            cameras_df = gsheet()
        else:
            try:
                cameras_df = pickel_file()
            except:
                cameras_df = gsheet()
        return(cameras_df)
    def check_values(self):
        check_ok = True
        check = {}
        # check value as calue attribute of StrEnum subclass
        check['Type']      = bool(self.df['Type'].apply(lambda x: x in CameraType._value2member_map_).all())
        check['LensMount'] = bool(self.df['LensMount'].apply(lambda x: x in LensMountType._value2member_map_).all())
        check['Network']   = bool(self.df['Network'].apply(lambda x: x in NetworkType._value2member_map_).all())
        # check value as boolean
        check['Bidirectionnal'] = bool(self.df['Bidirectionnal'].apply(lambda x: isinstance(x,bool)).all())
        check['Selected']       = bool(self.df['Selected'].apply(lambda x: isinstance(x, bool)).all())
        # check value as integer
        check['MaxDelayToComplete'] = bool(self.df['MaxDelayToComplete'].apply(lambda x: isinstance(x, int)).all())
        check['ControlCoverage']    = bool(self.df['ControlCoverage'].apply(lambda x: isinstance(x, int)).all())
        check['Number']             = bool(self.df['Number'].apply(lambda x: isinstance(x, int)).all())
        # check value as string but could be check as value of an Enum
        self.df['Brand']    = self.df['Brand'].astype(str)
        self.df['Cable']    = self.df['Cable'].astype(str)
        self.df['Protocol'] = self.df['Protocol'].astype(str)
        # check value as string but could be check as a more precise value type
        self.df['ManufacturerURL'] = self.df['ManufacturerURL'].astype(str)
        self.df['Remark']          = self.df['Remark'].astype(str)
        self.df['SupportURL']      = self.df['SupportURL'].astype(str)
        self.df['Message']         = self.df['Message'].astype(str)
        if False not in check.values():
            return
        else:
            print ("Descriptor-->Status of gsheet values with bad type: ",check)
            st.write("Check the values of the DataFrame")
            st.write(self.df)
            st.stop()

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