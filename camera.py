import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from pprint import pprint

class Camera():
    def __init__(self,update=True,debug=False):
        self.df  = self.load(update)
        self.view            = CameraTabView(self.df)
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
    def matching(self,camera_pattern="",brand="",camera_type=""):
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
        self.view.step_match = match
        return 

class CameraTabView():
    def __init__(self,camera_catalog_df):
        self.df = camera_catalog_df
        # Options for "brand" and "type" st.text_input as Series (DataFrame)
        self.brand_df = self.df["Brand"].unique()
        self.type_df  = self.df["Type"].unique()
        # Current catalog lines matching the current criterias (pattern && brand && type)
        self.step_match  = pd.DataFrame()
        # self.step_select contains the cameras selected by the user for the current selection step
        self.step_select = pd.DataFrame()
        # self.selected contains the full set of cameras selected by the user 
        self.selected    = pd.DataFrame()
        # Concat of 
        self.final       = pd.DataFrame()
    # TAB "CAMERA" FOR CAMERA NUMBER SELECTION
    def select(self):
        pattern = st.session_state.camera_pattern.upper()
        if ("brand_selector" not in st.session_state) and ("type_selector" not in st.session_state):
            st.session_state.camera.matching(camera_pattern=pattern)
        elif ("type_selector" not in st.session_state):
            brand = st.session_state.brand_selector
            st.session_state.camera.matching(camera_pattern=pattern,brand=brand)
        elif ("brand_selector" not in st.session_state):
            camera_type = st.session_state.type_selector
            st.session_state.camera.matching(camera_pattern=pattern,camera_type=camera_type)
        else:
            brand   = st.session_state.brand_selector
            camera_type = st.session_state.type_selector
            st.session_state.camera.matching(camera_pattern=pattern,brand=brand,camera_type=camera_type)
        return
    def edit_number(self):
        camera = self
        # Validate inputs
        if (len(camera.step_match.index) != 0): 
            camera.step_select = st.data_editor(
                camera.step_match,
                height = 200,
                column_config={
                    'Number':st.column_config.NumberColumn(
                        "# of Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        format="%d",
                    ),
                    "Reference": "Model",
                    "Brand": "Brand",
                    "Cable": "Cable",
                    "SupportURL": st.column_config.LinkColumn(
                        "Support URL",
                        help = "Reference in Cyanview Support Website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Support Link",
                        max_chars = 30 ),
                    "ManufacturerURL": st.column_config.LinkColumn(
                        "Brand URL",
                        help = "Reference on Brand website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Brand link",
                        max_chars = 30 ),
                    # "Reference": None,
                    # "supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                disabled=['Selected','Reference','Cable','SupportURL','ManufacturerURL'],
                column_order=['Number','Reference','Brand','Cable','SupportURL','ManufacturerURL'],
                hide_index = True,
                use_container_width = True,
                key = "x_camera_number",
    #            on_change = st.rerun,
                )
            return(camera.step_select)
    def display_selected(self):
        camera = self
        # Update the camera camera Dataframe with the number of camera selected on this step
        camera.df.update(camera.step_select)
        # Set the set of selected cameras
        camera.selected = camera.df[(camera.df['Number']>0)]
        # Trying to set properties of camera.selected for display
        camera.selected.style.set_properties(**{'background_color': 'lightgreen'})
        if (len(camera.selected.index) != 0):
            st.dataframe(
                camera.selected,
                column_config={
                    "Reference": "Model",
                    'Number':st.column_config.NumberColumn(
                        "# of Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        format="%d",
                    ),
                    "Brand": "Brand",
                    "Cable": "Cable",
                    "SupportURL": st.column_config.LinkColumn(
                        "Support URL",
                        help = "Reference in Cyanview Support Website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Support Link",
                        max_chars = 30 ),
                    "ManufacturerURL": st.column_config.LinkColumn(
                        "Brand URL",
                        help = "Reference on Brand website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Brand link",
                        max_chars = 30 ),
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                column_order=['Number','Brand','Reference','Cable','SupportURL','ManufacturerURL'],
                hide_index = True)
        return(camera.selected)


if __name__ == "__main__":
    camera = Camera()
    pprint(camera.df)
 
