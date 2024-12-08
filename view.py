import streamlit as st
import pandas    as pd
from x_camera import Camera
from constants import Network_Enum

class View():
    def __init__(self,session_state) -> None:
        self.session_state = session_state
    # SIDEBAR
    def sidebar(self):
        # Sidebar
        st.sidebar.header(("Workflow"))
        st.sidebar.markdown((
            """
        1. Set **Cameras** pool
        2. Set **IP Network** mediums
        3. Set **Lenses**
        4. **Refine** your use-case
        """))
        st.sidebar.header(("Outputs"))
        st.sidebar.markdown((
            """
        1. **Schema** of use-case, 
        2. List of equipment for quote
        3. Tips, attention points, explanations
        """
        ))

        st.sidebar.header(("Resources"))
        st.sidebar.markdown((
            """
        - [Support Documentation](https://support.cyanview.com)
        - [Website](https://www.cyanview.com)
        - [Presentation](https://www.cyanview.com/presentation)
        - [Blog](https://www.cyanview.com/blog) (How to master Streamlit for data science)
        """
        ))

        st.sidebar.header(("About Cyanview"))
        st.sidebar.markdown((
            "[Cyanview](https://www.cyanview.com) is a company providing shading solutions for video productions."
        ))
        return 
    # TAB "CAMERA" FOR CAMERA NUMBER SELECTION
    def camera_select(self):
        pattern = st.session_state.x_camera_pattern.upper()
        if ("x_brand_selector" not in st.session_state) and ("x_type_selector" not in st.session_state):
            st.session_state.camera.pattern(camera_pattern=pattern)
        elif ("x_type_selector" not in st.session_state):
            brand = st.session_state.x_brand_selector
            st.session_state.camera.pattern(camera_pattern=pattern,brand=brand)
        elif ("x_brand_selector" not in st.session_state):
            camera_type = st.session_state.x_type_selector
            st.session_state.camera.pattern(camera_pattern=pattern,camera_type=camera_type)
        else:
            brand   = st.session_state.x_brand_selector
            camera_type = st.session_state.x_type_selector
            st.session_state.camera.pattern(camera_pattern=pattern,brand=brand,camera_type=camera_type)
        return
    def camera_edit_number(self):
        camera = self.session_state.camera
        if not isinstance(camera,Camera):
            raise ValueError("Paramer of method 'camera_edit_number' must be a Camera instance")
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
    def camera_display_selected(self):
        camera = self.session_state.camera
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
    # TAB NETWORK
    def network_edit_byblocks(self):
        def network_edit_block(df,key):
            if (len(df.index) != 0): 
                df = st.data_editor(
                    df,
                    column_config={
                        "Type": "Type",
                        "Reference": "Model",
                        'Number':st.column_config.NumberColumn(
                            "# Cams",
                            help="How much camera of this type in your use-case (0-15)?",
                            min_value=0,
                            max_value=15,
                            step=1,
                            default=0,
                            format="%d",
                        ),
                        'Network': st.column_config.SelectboxColumn(
                            "IP Network",
                            help="Select the IP network type",
                            width="small",
                            options = [member.value for member in Network_Enum],
                            required=True),
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
                        # "supportText": None,
                        "Message":None,
                        },
                    disabled=['Reference','Brand','Number','SupportURL'],
                    column_order=['Network','Reference','Brand','Number','SupportURL'],
                    hide_index = True,
                    use_container_width = True,
                    key = key+"_network",
        #            on_change = st.rerun,
                    )
                ## st.markdown(display)
                #print("\nDATAFRAME AFTER EDIT")
                #print(df)
                return(df)
        pool = self.session_state.camera
        blocks = {}
        camera_types = pool.selected["Type"].unique()
        print("Camera Types:",camera_types)
        for camera_type in camera_types:
            #filter instance dataframe by type
            selected_rows = pool.selected.loc[pool.selected['Type'] == camera_type]
            if not selected_rows.empty :
                print("Camera Type:",camera_type)
                st.markdown(camera_type)
                blocks[camera_type] = network_edit_block(selected_rows,key=camera_type)
        pool.final = pd.concat(list(blocks.values()))
        print("StreamUI->pool_edit_camera_for_network-> POOL.FINAL columns:\n",pool.final.columns)
        return pool.final
    # TAB LENS
    def lens_edit(self):
        def edit_camera_lens(df,cameraLensCategory):
            print("edit_camera_lens.df:")
            print(df)
            if (len(df.index) != 0): 
                df = st.data_editor(
                    df,
                    column_config={
                        "Type": "Type",
                        "Reference": "Model",
                        'Number':st.column_config.NumberColumn(
                            "# Cams",
                            help="How much camera of this type in your use-case (0-15)?",
                            min_value=0,
                            max_value=15,
                            step=1,
                            default=0,
                            format="%d"),
                        'lensControl': st.column_config.SelectboxColumn(
                            "Lens Control",
                            help= "Your needs for lens motorization",
                            # width="small",
                            options = pool.cameralens.options_needs_lensControl[cameraLensCategory],
                            # options = st.session_state.property.constraints[(cameraLensCategory,'LensControls')],
                            #options=st.session_state.property.options['LensUserControls'],
                            required = True),
                        'lensType':  st.column_config.SelectboxColumn(
                            "Type of Lens",
                            help="Main characteristics of the lens",
                            # width="medium",
                            #options = st.session_state.property.options['LensTypes'],
                            options = pool.cameralens.options_needs_lensType[cameraLensCategory],
                            # options=st.session_state.property.constraints[(cameraLensCategory,'LensTypes')],
                            required = True),
                        'lensMotor':  st.column_config.SelectboxColumn(
                            "Motorization",
                            help="Type of motorization",
                            # width="small",
                            options = pool.cameralens.options_needs_motorType[cameraLensCategory],
                            # options = st.session_state.property.constraints[(cameraLensCategory,'LensMotors')],
                            required=True),
                        "Brand": "Brand",
                        },
                    disabled=['Reference','Brand','Number'],
                    column_order=['Reference','lensControl','lensType','lensMotor','Brand','Number'],
                    hide_index = True,
                    use_container_width = True,
                    )
                return(df)
        pool = self.session_state.lens
        blocks = {}
        #cameraLensCategory est l'élément de sélection
        if 'LensTypes' not in pool.df.columns:
            pool.df['LensTypes']=""
        #print("DF Columns:",pool.df.columns)
        #print("SELECTED Columns:",pool.selected.columns)
        cameraLensCategories = pool.df["CameraLensCategory"].unique()
        pool.df.to_csv('debug_pool_display_lens.csv', index=False)
        #print("################CAMERAS LENS CATEGORIES  :",cameraLensCategories)
        for cameraLensCategory in cameraLensCategories:
            #filter instance dataframe by type
            selected_rows = pool.df.loc[pool.df['CameraLensCategory'] == cameraLensCategory]
            #print(cameraLensCategories)
            #print(selected_rows)
            if not selected_rows.empty :
                st.markdown(cameraLensCategory)
                #??? NO USE?? constraints = Lens.filter_constraints(cameraLensCategory)
                blocks[cameraLensCategory] = edit_camera_lens(selected_rows,cameraLensCategory)
        #print("################CAMERAS LENS CATEGORIES END################# :",cameraLensCategories)
        print("blocks.values:",list(blocks.values()))
        if list(blocks.values()) != []:
            final_df = pd.concat(list(blocks.values()))
        #print("StreamUI->pool_edit_camera_for_lens-> POOL.FINAL columns:\n",pool.final.columns)
        return final_df