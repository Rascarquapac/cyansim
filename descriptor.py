import pandas as pd
import streamlit as st
from pprint import pprint
from streamlit_gsheets import GSheetsConnection
from logger_config import setup_logger
from constants import LensMountType, CameraType, BrandType, AdapterType, NetworkType
logger = setup_logger()
class Clean():
	def __init__(self,df=None,cols_names=[]):
		self.df = df 
		self.col_names = cols_names
	def detect_invalid_values(self, df= None, column_name='Type', condition=None):
		# condition = lambda x: x in allowed_values
		is_valid = df[column_name].apply(condition)
		if not is_valid.all():
			return df[~is_valid].index
		else:
			return False        
	def all_valid_indexes(self, invalid_indexes):
		validity_check = True
		for key, value in invalid_indexes.items():
			if value is not False:
				validity_check = False
		return validity_check
	def dump_invalid_indexes(self,df, invalid_indexes, table_name=""):
		if self.all_valid_indexes(invalid_indexes) is False:
			logger.warning(f"Descriptor-->Invalid indexes found in the table {table_name}:")
			for key, value in invalid_indexes.items():
				if value is not False:
					logger.warning(f"  {key}: {value.tolist()}")
					logger.warning(f"  {key} values: {df.loc[value, key].tolist()}")
		else:
			logger.info(f"Descriptor-->Valid indexes in table {table_name}.")
	def clean_cameras(self):
		cameras_df = self.df
		cameras_df['Model'].fillna("").astype(str)
		cameras_df['Reference'].fillna("").astype(str)
		cameras_df['Protocol'].fillna("").astype(str)
		cameras_df['LensMount'].fillna("").astype(str)
		cameras_df['ManufacturerURL'].fillna("").astype(str)
		cameras_df['Remark'].fillna("").astype(str)
		cameras_df.drop(['CameraLensControl','CameraType','TallyOptions','Brand',''], axis=1, errors='ignore', inplace=True)
		cameras_df = cameras_df[['Model', 'Reference', 'Protocol', 'LensMount','ManufacturerURL','Remark']]
		return cameras_df
	def clean_protocols(self):
		protocols_df = self.df
		protocols_df['Protocol'].fillna("").astype(str)
		protocols_df['Brand'].fillna("").astype(str)
		protocols_df['Type'].fillna("").astype(str)
		protocols_df['Cable'].fillna("").astype(str)
		protocols_df['SupportURL'] = protocols_df['SupportURL'].fillna("").astype(str)
		protocols_df['Message'].fillna("").astype(str)
		protocols_df['MaxDelayToComplete'] = protocols_df['MaxDelayToComplete'].replace({'':0,'\n':0}).fillna(500).astype(int)
		protocols_df['ControlCoverage'] = protocols_df['ControlCoverage'].replace({'':0,'\n':0}).fillna(0).astype(int)
		protocols_df['Bidirectionnal'] = protocols_df['Bidirectionnal'].apply(lambda x: False if x == "No" else True)
		#protocols_df.drop(['Message'], axis=1, errors='ignore', inplace=True)
		protocols_df = protocols_df[['Protocol', 'Brand', 'Type', 'Cable', 'MaxDelayToComplete', 'ControlCoverage', 'Bidirectionnal','SupportURL','Message']]
		return protocols_df
	def check_cameras(self):
		cameras_df = self.df
		invalid_indexes = {}
		invalid_indexes['LensMount'] = self.detect_invalid_values(cameras_df, 'LensMount',  lambda x: x in LensMountType._value2member_map_)
		return invalid_indexes
	def check_protocols(self):
		protocols_df = self.df
		invalid_indexes = {}
		invalid_indexes['Protocol'] = False # Not checked cause it is correct by construction of the gsheet
		invalid_indexes['Brand']    = self.detect_invalid_values(protocols_df, 'Brand', lambda x: x in BrandType._value2member_map_)
		invalid_indexes['Type']     = self.detect_invalid_values(protocols_df, 'Type',  lambda x: x in CameraType._value2member_map_)
		invalid_indexes['Cable']    = self.detect_invalid_values(protocols_df, 'Cable', lambda x: x in AdapterType._value2member_map_)
		invalid_indexes['MaxDelayToComplete'] = self.detect_invalid_values(protocols_df, 'MaxDelayToComplete', lambda x: isinstance(x,int))
		invalid_indexes['ControlCoverage']    = self.detect_invalid_values(protocols_df, 'ControlCoverage', lambda x:  isinstance(x,int))
		invalid_indexes['Bidirectionnal']     = self.detect_invalid_values(protocols_df, 'Bidirectionnal', lambda x:  isinstance(x,bool))
		return invalid_indexes

class Descriptor():
	def __init__(self,updateFromGsheet=True,debug=False):
		self.pickel_filename = "./data/cameras.pkl"
		self.invalid_indexes = {}
		self.df  = self.load(updateFromGsheet)

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
				# First time loading the cameras, no pickle file available
				cameras_df = self.get_camera_gsheet()
				proto_df   = self.get_protocol_gsheet()
				cameras_df = self.build_camera_set(cameras_df,proto_df)
				self.set_pickel_camera(cameras_df)
		return(cameras_df)
	# LOADING DATA FROM GOOGLE SHEETS
	def get_camera_gsheet(self):
		conn = st.connection("cameras", type=GSheetsConnection)
		cam_df = conn.read(usecols=[
			'Model','Reference','Protocol','LensMount','ManufacturerURL','Remark'])        
		logger.info("Descriptor-->Cameras table successfully loaded from Gsheet")
		cam_df = Clean(df=cam_df).clean_cameras()
		cam_df['Name'] = cam_df['Model']
		return cam_df
	def get_protocol_gsheet(self): 
		conn = st.connection("protocols", type=GSheetsConnection)
		proto_df = conn.read(usecols=[
			"Protocol","Brand","Type","Cable",
			"SupportURL","Message",
			"MaxDelayToComplete",
			"ControlCoverage","Bidirectionnal"])
		logger.info("Descriptor-->Protocols table successfully loaded from Gsheet")
		proto_df = Clean(df=proto_df).clean_protocols()
		return proto_df
	def build_camera_set(self,cam_df,proto_df):
		# LEFT JOIN FOR COMBINING CAMERAS AND PROTOCOLS DATA
		camera_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
		# ADDING DEFAULT COLUMNS
		camera_df['Number']   = 0
		camera_df['Selected'] = False
		camera_df['Network']  = NetworkType.LAN_WIRED.value
		return camera_df
	# LOADING FROM AND SAVING TO PICKLE TO AVOID RELOADING DATA
	def set_pickel_camera(self,cameras_df):
		cameras_df.to_pickle(self.pickel_filename)
	def get_camera_pickle(self):
		return pd.read_pickle(self.pickel_filename)

  
if __name__ == "__main__":
	descriptor = Descriptor()
	# descriptor.df.to_csv("./debug/descriptor_df.csv")
	# # Summary of the DataFrame 
	# print("\nInfo summary:") 
	# descriptor.df.info() 
	# # Display the first few rows 
	# head_summary = descriptor.df.head() 
	# print("\nFirst few rows of the DataFrame:") 
	# print(head_summary) 
	# # Display the last few rows
	# tail_summary = descriptor.df.tail() 
	# print("\nLast few rows of the DataFrame:") 
	# print(tail_summary) 
	# # Shape of the DataFrame 
	# shape_summary = descriptor.df.shape 
	# print("\nShape of the DataFrame:") 
	# print(shape_summary) 
	# # Column names of the DataFrame 
	# columns_summary = descriptor.df.columns 
	# print("\nColumn names of the DataFrame:") 
	# print(columns_summary)