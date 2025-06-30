import pandas as pd
import streamlit as st
from pprint import pprint
from streamlit_gsheets import GSheetsConnection
from logger_config import setup_logger
from constants import LensMountType, CameraType, BrandType, AdapterType, NetworkType
logger = setup_logger()

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
        invalid_indexes = {}
        invalid_indexes['LensMount'] = self.detect_invalid_values(cam_df, 'LensMount',  lambda x: x in LensMountType._value2member_map_)
        cam_df['Name'] = cam_df['Model']
        cam_df['ManufacturerURL'] = cam_df['ManufacturerURL'].fillna("")
        cam_df['ManufacturerURL'] = cam_df['ManufacturerURL'].astype(str)
        cam_df['Remark']          = cam_df['Remark'].fillna("")
        cam_df['Remark']          = cam_df['Remark'].astype(str)
        self.dump_invalid_indexes(invalid_indexes, "Cameras")
        return cam_df
    def get_protocol_gsheet(self): 
        conn = st.connection("protocols", type=GSheetsConnection)
        proto_df = conn.read(usecols=[
            "Protocol","Brand","Type","Cable",
            "SupportURL","Message",
            "MaxDelayToComplete",
            "ControlCoverage","Bidirectionnal"])
        logger.info("Descriptor-->Protocols table successfully loaded from Gsheet")
        #  CHECKING PROTOCOL VALUES
        invalid_indexes = {}

        proto_df['Protocol']        = proto_df['Protocol'].fillna("")
        invalid_indexes['Protocol'] = False # Not checked cause it is the key
        invalid_indexes['Brand'] = self.detect_invalid_values(proto_df, 'Brand', lambda x: x in BrandType._value2member_map_)
        invalid_indexes['Type']  = self.detect_invalid_values(proto_df, 'Type',  lambda x: x in CameraType._value2member_map_)
        invalid_indexes['Cable']     = self.detect_invalid_values(proto_df, 'Cable', lambda x: x in AdapterType._value2member_map_)

        proto_df['SupportURL']      = proto_df['SupportURL'].fillna("")
        proto_df['Message']         = proto_df['Message'].fillna("")
        # MaxDelayToComplete column
        proto_df['MaxDelayToComplete']        = proto_df['MaxDelayToComplete'].fillna(500)
        invalid_indexes['MaxDelayToComplete'] = self.detect_invalid_values(proto_df, 'MaxDelayToComplete', lambda x: int(x))
        # ControlCoverage column
        proto_df['ControlCoverage']    = proto_df['ControlCoverage'].fillna(0)
        # invalid_indexes['ControlCoverage'] = self.detect_invalid_values(proto_df, 'ControlCoverage', lambda x: int(x))
        # CONVERTING COLUMN VALLUES
        proto_df['Bidirectionnal']     = proto_df['Bidirectionnal'].apply(lambda x: False if x == "No" else True)

        self.dump_invalid_indexes(invalid_indexes, "Protocols")
        return proto_df
    def build_camera_set(self,cam_df,proto_df):
        # LEFT JOIN FOR COMBINING CAMERAS AND PROTOCOLS DATA
        camera_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
        # ADDING DEFAULT COLUMNS
        camera_df['Number']   = 0
        camera_df['Selected'] = False
        camera_df['Network']  = NetworkType.LAN_WIRED.value
        print("Lan wired",NetworkType.LAN_WIRED.value)
        return camera_df
    # CHECKING VALUES
    def detect_invalid_values(self, df= None, column_name='Type', condition=None):
        # condition = lambda x: x in allowed_values
        is_valid = df[column_name].apply(condition)
        if not is_valid.all():
            return df[~is_valid].index
        else:
            return False        
    def dump_invalid_indexes(self,invalid_indexes, table_name=""):
        if invalid_indexes:
            logger.warning(f"Descriptor-->Invalid indexes found in the table {table_name}:")
            for key, value in invalid_indexes.items():
                if value is not False:
                    logger.warning(f"  {key}: {value.tolist()}")
        else:
            logger.info(f"Descriptor-->No invalid indexes found in the table {table_name}.")
    # LOADING FROM AND SAVING TO PICKLE
    def set_pickel_camera(self,cameras_df):
        cameras_df.to_pickle(self.pickel_filename)
    def get_camera_pickle(self):
        return pd.read_pickle(self.pickel_filename)

  
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