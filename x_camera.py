import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from pprint import pprint

class Camera():
    def __init__(self,update=True,debug=False):
        self.df       = self.load(update)
        # Brands list
        self.brand_df = self.df["Brand"].unique()
        # Types list
        self.type_df  = self.df["Type"].unique()
        # Dataframe 
        self.step_match  = pd.DataFrame()
        # self.step_select contains the cameras selected by the user for the current selection step
        self.step_select = pd.DataFrame()
        # self.selected contains the full set of cameras selected by the user 
        self.selected    = pd.DataFrame()
        # Concat of 
        self.final       = pd.DataFrame()
        self.pickel_filename = "./picklized/x_cameras.pkl"

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
            # LEFT JOIN FOR COMBINING CAMERAS AND PROTOCOLS DATA
            camera_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
            camera_df['Number'] = 0
            camera_df['Selected'] = False
            camera_df['Network'] = 'LAN Wired'
            camera_df.to_pickle("./picklized/x_cameras.pkl")
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
    def pattern(self,camera_pattern="",brand="",camera_type=""):
        if camera_pattern != None and camera_pattern != "":
            pattern_selection = self.df.filter(like=camera_pattern,axis=0)
        else:
            pattern_selection = self.df
        if brand != None and brand != "":
            brand_query = f'Brand == "{brand}"'
            brand_selection = pattern_selection.query(brand_query)
        else:
            brand_selection = pattern_selection
        if camera_type != None and camera_type != "":
            type_query = f'Type == "{camera_type}"'
            match = brand_selection.query(type_query)
        else:
            match = brand_selection
        self.step_match = match
        return 

if __name__ == "__main__":
    camera = Camera()
    pprint(camera.df)
 
