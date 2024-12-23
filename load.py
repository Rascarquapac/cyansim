import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from pprint import pprint

class Descriptor():
    def __init__(self,update=True,debug=False):
        self.df  = self.load(update)
        self.pickel_filename = "./picklized/cameras.pkl"
    def load(self,update):
        def gsheet():
            conn = st.connection("cameras", type=GSheetsConnection)
            cam_df = conn.read(usecols=[
                'Model','Reference','Protocol','Brand','ManufacturerURL','Remark',"CameraLensControl","LensMount"])        
            conn = st.connection("protocols", type=GSheetsConnection)
            proto_df = conn.read(usecols=[
                "Protocol","Brand","Type","Cable","SupportURL","Message","MaxDelayToComplete","ControlCoverage","Bidirectionnal"])
            # PROFILE THE CAMERA POOL
            del proto_df['Brand']
            cam_df['Name'] = cam_df['Model']
            # LEFT JOIN FOR COMBINING CAMERAS AND PROTOCOLS DATA
            camera_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
            camera_df['Number'] = 0
            camera_df['Selected'] = False
            camera_df['Network'] = 'LAN Wired'
            camera_df.to_pickle("./picklized/cameras.pkl")
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
if __name__ == "__main__":
    descriptor = Descriptor()
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