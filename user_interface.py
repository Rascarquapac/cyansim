import streamlit as st
import json 
import pandas as pd
from debug import Debug
from constants import CameraCategory as CameraCategory
from constants import CameraLens as CameraLens
from constants import NetworkType

class Pool:
	def __init__(self):
		# The camera_instances x properties dataframe specifying the setup of the production
		self.df = pd.DataFrame()
		self.cameralens = CameraLens()
		self.debug = Debug()
		self.initcase_dict = {}
	def build(self,camera_pool):
		# Add columns intiating the Lens definition UI ("Tab Lens")
		def lensCategory(camera_type):
			return CameraLens().cameraLens_category(camera_type)
		def user_defaults(camera_category):
			# Return the default values for the camera type
			return Options().needs_init[camera_category]
		if camera_pool.empty:
			pass
		else:
			camera_pool = camera_pool.copy()  
			camera_pool["CameraLensCategory"] = camera_pool["Type"].apply(lensCategory)
			camera_pool[['lensControl','lensType','lensMotor']] = camera_pool["CameraLensCategory"].apply(user_defaults).apply(pd.Series)
			self.df = camera_pool

class Options():
	def __init__(self):
		# Lens control options for each camera category
		# The lens control is the type of lens control
		# It can be "No control", "Basic control", "Good control", "Advanced control"
		self.lensControl = {
			CameraCategory.BROADCAST.value: ['No Need','Iris','IZF'],
			CameraCategory.CINE_XCHANGE.value: ['No Need','Iris','IZF'],
			CameraCategory.IZF_INTEGRATED.value: ['IZF'],
			CameraCategory.FIXED_LENS.value: ['No Need'],
			CameraCategory.MINICAM_MOT_LENS.value: ['No Need','IZF'],
			CameraCategory.TBD.value: ['No Need'],
		}
		self.lensType = {
			CameraCategory.BROADCAST.value: ['B4-Mount'],
			CameraCategory.CINE_XCHANGE.value: ['B4-Mount','E-Mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD'],
			CameraCategory.IZF_INTEGRATED.value: ['Camera Integrated'],
			CameraCategory.FIXED_LENS.value: ['Manual'],
			CameraCategory.MINICAM_MOT_LENS.value: ['Manual'],
			CameraCategory.TBD.value: ["No Need"],
		}
		# Motorization options for each camera category
		# The motorization is the type of lens motorization
		# It can be "No motor", "Motorized", "Manual"
		# The motorization is the type of lens motorization
		# It can be "No motor", "Motorized", "Manual"
		self.motorType = {
			CameraCategory.BROADCAST.value: ['No extra motors'],
			CameraCategory.CINE_XCHANGE.value: ['No extra motors','Tilta','Arri','TBD'],
			CameraCategory.IZF_INTEGRATED.value: ['Camera Integrated'],
			CameraCategory.FIXED_LENS.value: ['Manual'],
			CameraCategory.MINICAM_MOT_LENS.value: ['No extra motors','Dreamchip'],
			CameraCategory.TBD.value: ['No extra motors'],
		}
		self.needs_init = {
			CameraCategory.BROADCAST.value: ('No Need','B4-Mount','No extra motors'),
			CameraCategory.CINE_XCHANGE.value: ('No Need','TBD','TBD'),
			CameraCategory.IZF_INTEGRATED.value: ('IZF','Camera Integrated','No extra motors'),
			CameraCategory.FIXED_LENS.value: ("No Need",'Manual','No extra motors'),
			CameraCategory.MINICAM_MOT_LENS.value: ("No Need",'Manual','No extra motors'),
			CameraCategory.TBD.value: ("No Need",'Manual','No extra motors'),
		}
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
    def matching(self,camera_pattern="",brand="",camera_type=""):
        if camera_pattern != None and camera_pattern != "":
            # pattern_selection = self.df.filter(like=camera_pattern,axis=0)
            print(self.df.columns)
            pattern_selection = self.df[self.df[['Name','Reference']].apply(
                lambda row: row.astype(str).str.contains(camera_pattern, case=False).any(), 
                axis=1)]
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
class ViewLens():
	def __init__(self,pool):
		self.pool       = pool
		self.debug      = Debug(data=self.pool.df,mode='pool',debug_rec=False,debug_load=False)
	def edit(self):
		def edit_camera_lens(df,cameraLensCategory):
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
							options = Options().lensControl[cameraLensCategory],
							# options = self.pool.cameralens.options_needs_lensControl[cameraLensCategory],
							required = True),
						'lensType':  st.column_config.SelectboxColumn(
							"Type of Lens",
							help="Main characteristics of the lens",
							# width="medium",
							options = Options().lensType[cameraLensCategory],
							# options = self.pool.cameralens.options_needs_lensType[cameraLensCategory],
							required = True),
						'lensMotor':  st.column_config.SelectboxColumn(
							"Motorization",
							help="Type of motorization",
							# width="small",
							options = Options().motorType[cameraLensCategory],
							# options = self.pool.cameralens.options_needs_motorType[cameraLensCategory],
							required=True),
						"Brand": "Brand",
						},
					disabled=['Reference','Brand','Number'],
					column_order=['Reference','lensControl','lensType','lensMotor','Brand','Number'],
					hide_index = True,
					use_container_width = True,
					)
				return(df)
		# self.pool.df = self.debug.load(data=self.pool.df)
		# print("POOL SET ------------------------------------------>")
		# print(self.pool.df)
		blocks = {}
		#cameraLensCategory est l'élément de sélection
		if 'LensTypes' not in self.pool.df.columns:
			self.pool.df['LensTypes']=""
		cameraLensCategories = self.pool.df["CameraLensCategory"].unique()
		#print("################CAMERAS LENS CATEGORIES  :",cameraLensCategories)
		for cameraLensCategory in cameraLensCategories:
			#filter instance dataframe by type
			selected_rows = self.pool.df.loc[self.pool.df['CameraLensCategory'] == cameraLensCategory]
			if not selected_rows.empty :
				st.markdown(cameraLensCategory)
				#??? NO USE?? constraints = Lens.filter_constraints(cameraLensCategory)
				blocks[cameraLensCategory] = edit_camera_lens(selected_rows,cameraLensCategory)
		# print("blocks.values:",list(blocks.values()))
		if list(blocks.values()) != []:
			final_df = pd.concat(list(blocks.values()))
		self.pool.df = final_df
		# print("POOL-------------------->")
		# print(self.pool.df)
		self.debug.record(data=self.pool.df,record=True,dump=True)
		return final_df
class ViewNetwork():
	def __init__(self,pool):
		self.pool = pool
		self.df   = pool.df
	def edit(self):
		def network_edit_block(df,key):
			session_key =  key+"_network"
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
                            options = [member.value for member in NetworkType],
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
                    key = session_key,
        #            on_change = st.rerun,
                    )
			return(df)
		blocks = {}
		camera_types = self.pool.df["Type"].unique()
		for camera_type in camera_types:
            #filter instance dataframe by type
			selected_rows = self.pool.df.loc[self.pool.df['Type'] == camera_type]
			if not selected_rows.empty :
				st.markdown(camera_type)
				blocks[camera_type] = network_edit_block(selected_rows,key=camera_type)
		final = pd.concat(list(blocks.values()))
		self.pool.df = final
		return final
class Sidebar():
    def __init__(self) -> None:
        pass
    # SIDEBAR
    def display(self):
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

 
