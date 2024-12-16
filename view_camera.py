import pandas as pd
import streamlit as st
from pprint import pprint
from debug import Debug

class ViewCamera():
    def __init__(self,descriptor):
        self.df = descriptor.df
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
        self.debug       = Debug(data=self.df,mode='camera',debug_rec=False,debug_load=False)
    def init_cameradf(self, init_dict):
        # Updating camera.df will create camera.selected in self.display() 
        print("CAMERA->INIT_SELECT->camera.selected: start ---------->:\n",self.selected)
        if init_dict != {}:
            print("CAMERA->INIT_SELECT: init_dict[Reference] ",init_dict.keys())
            row_to_include = list(init_dict['Reference'].keys())
            # Add stored values
            for index in row_to_include:
                self.df.loc[index,'Number']=init_dict['Number'][index]
            print("CAMERA->INIT_SELECT camera.selected: end ---------->:\n",self.selected)
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
        self.step_match = match
        return 
    # TAB "CAMERA" FOR CAMERA NUMBER SELECTION
    def select(self):
        pattern = st.session_state.camera_pattern.upper()
        if ("brand_selector" not in st.session_state) and ("type_selector" not in st.session_state):
            self.matching(camera_pattern=pattern)
        elif ("type_selector" not in st.session_state):
            brand = st.session_state.brand_selector
            st.session_state.camera.matching(camera_pattern=pattern,brand=brand)
        elif ("brand_selector" not in st.session_state):
            camera_type = st.session_state.type_selector
            self.matching(camera_pattern=pattern,camera_type=camera_type)
        else:
            brand   = st.session_state.brand_selector
            camera_type = st.session_state.type_selector
            self.matching(camera_pattern=pattern,brand=brand,camera_type=camera_type)
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
                key = "camera_number",
    #            on_change = st.rerun,
                )
            return(camera.step_select)
    def display_selected(self):
        #  self.df = self.debug.load(data=self.df)
        camera = self
        # Update the camera camera Dataframe with the number of camera selected on this step
        camera.df.update(camera.step_select)
        self.debug.record(data=self.df,record=True,dump=True)
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
                hide_index = True,
                key= 'display_select')
        return(camera.selected)


if __name__ == "__main__":
    camera = ViewCamera()
    pprint(camera.df)
 
