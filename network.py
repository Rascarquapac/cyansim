import streamlit as st
import pandas as pd
from constants import Network_Enum

class Network():
	def __init__(self,pool):
		self.df = pool.df
		self.view = NetworkTabView(self.df)
	def setdf(self, df):
		if df.empty:
			pass
		else:
			self.df = df

# TAB NETWORK
class NetworkTabView():
	def __init__(self,selected):
		self.df = selected
	def edit(self,selected):
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
			return(df)
		blocks = {}
		camera_types = selected["Type"].unique()
		print("Camera Types:",camera_types)
		for camera_type in camera_types:
            #filter instance dataframe by type
			selected_rows = selected.loc[selected['Type'] == camera_type]
			if not selected_rows.empty :
				print("Camera Type:",camera_type)
				st.markdown(camera_type)
				blocks[camera_type] = network_edit_block(selected_rows,key=camera_type)
		final = pd.concat(list(blocks.values()))
		print("StreamUI->pool_edit_camera_for_network-> POOL.FINAL columns:\n",final.columns)
		return final
