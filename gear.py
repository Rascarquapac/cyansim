import pandas as pd
from constants import CameraLens
from gear_glue import GlueTBD, DevicesState
from gear_medium import Medium
from gear_rcp import *
from pprint import pprint
from logger_config import setup_logger
logger = setup_logger()
class InstancesAsRows():
    def __init__(self,pool_df):
        self.df = self.flatten(pool_df)
    def flatten(self,pool_df):
        # Flatten the dataframe to a list of instances
        instances = []
        for index, row in pool_df.iterrows():
            if row['Number'] > 0:
                for i in range(int(row['Number'])):
                    instance = row.copy()
                    instance['Instance'] = f"{index}_{i}"
                    instances.append(instance)
        df = pd.DataFrame(instances)
        df.set_index('Instance', inplace=True)
        # Suppress unused pool_df columns
        df.drop(columns=['SupportURL', 'ManufacturerURL','Remark','Selected','Message'], inplace=True)
        # Add result columns storing the results of protocol analyse
        df['Camera_id'] = df.index
        df['Device']    = ""
        df['Device_id'] = ""
        df['Switch_id'] = ""
        df['RCP_id']    = ""
        df['Camgroup']  = ""
        df['RCPtype']   = ""
        df['Fanout']    = 0
        # Add result columns storing the results of lens analyse
        df['LensCable']  = ""
        df['MotorCable'] = ""
        df['LensMotor']  = ""
        return df
class InstancesAsObjects():
    def __init__(self,pool_df):
        self.dic = self.flatten(pool_df)
    def flatten(self,pool_df):
        # Flatten the dataframe to a list of instances
        instances_dic = {}
        for index, row in pool_df.iterrows():
            if row['Number'] > 0:
                for i in range(int(row['Number'])):
                    camera_id = f"{index}_{i}"
                    cameralens = CameraLens()
                    glue       = GlueTBD() 
                    medium     = Medium()
                    rcp        = RCP_TBD()
                    instances_dic[camera_id]= {'rcp':rcp,'medium':medium,'glue':glue,'cameralens':cameralens}
        return instances_dic                    

class Cyangear():
    def __init__(self,pool) -> None:
        self.pool = pool
        # Intialization with the pool object (cameras x properties) dataframe describing the production setup 
        if not pool.df.empty:
            self.df = InstancesAsRows(pool.df).df
            self.dic = InstancesAsObjects(pool.df).dic
            self.devices_state = DevicesState(pool.df)
        else:
            self.df = pd.DataFrame()
            self.dic = {}
            self.devices_state = DevicesState(pd.DataFrame())
        self.rcps    = {}
        self.cables  = {}
        self.devices = {}
    def adapter(self,row):
        parameters=(row['Type'],row['Brand'],row['Reference'],row['lensControl'],row['lensType'],row['lensMotor'])
        accessories =CameraLens.adapters(parameters)
        return pd.Series([accessories[0], accessories[1],accessories[2]])
    def device_direct(self,row):
        dev = Medium.device_direct(row['Cable'],row['LensCable'],row['MotorCable'])
        return pd.Series([dev])
    def device_network(self,row):
        dev = Medium.device_network (row['Device'],row['Network'],row['MaxDelayToComplete'])
        return pd.Series([dev])
    def fanout(self,row):
        fan = Medium.fanout(row['Cable'],row['LensCable'],row['MotorCable'])
        return pd.Series([fan])
    def camgroup(self,row):
        group = Medium.camgroup(row['Type'],row['Network'])
        return pd.Series([group])
    def device_id(self,row):
        camgroup = row['Camgroup']
        device   = row['Device']
        fanout   = row['Fanout']
        id = self.devices_state.get_device_id(device,fanout)
        return pd.Series([id])
    # A new camera row is processed, update the devices_status
    def device_id_from_device(self):
        devices_state = self.devices_state
        camgroups = self.df['Camgroup'].unique() 
        for camgroup in camgroups:
            # update_status(devices_status)
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            for index in camgroup_indexes:
                device = self.df.loc[index,'Device']
                fanout = self.df.loc[index,'Fanout']
                print("Iteration on camgroup_indexes",index,device,fanout)
                self.df.loc[index,'Device_id'] = devices_state.get_device_id(device,fanout)
                value = (self.df.loc[index,'LensCable'],self.df.loc[index,'MotorCable'],self.df.loc[index,'LensMotor'])
            # camgroup_update_status(devices_status)
            devices_state.camgroup_update()
    # Add one switcher per camera group
    def switch_id_from_camgroup(self,row):
        name = row['Camgroup'] + " Switch"
        return pd.Series([name])
    # Select the RCP type based on the camera group
    def rcptype(self,row):
        camgroup = row['Camgroup']
        rcptype = RCP.rcptype_from_camgroup(camgroup)
        return pd.Series([rcptype])
    # According to fanins in a camera group set RCP_instances
    def rcp_id_from_camgroup(self):
        def get_rcp_id(rcps_status,RCPtype):
            try:
                (number,port,maxconnect,camgroup_instanciated) = rcps_status[RCPtype]
            except:
                print(f"RCP of type {RCPtype} not defined")
                raise
            camgroup_instanciated = True
            if port < maxconnect : 
                port += 1
            else : 
                number += 1
                port = 1
            rcps_status[RCPtype] = (number,port,maxconnect,camgroup_instanciated)
            return ("CY-" + RCPtype + "_" + str(number))
        
        rcps_status = {"RCP":(0,0,200,False),"RCP-J":(0,0,200,False),"RCP-DUO-J":(0,0,1,False)}
        camgroups   = self.df['Camgroup'].unique() 
        #self.df.to_csv('./debug_unknown_cameras.csv')
        for camgroup in camgroups:
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            for index in camgroup_indexes:
                self.df.loc[index,'RCP_id'] = get_rcp_id(rcps_status,self.df.loc[index,'RCPtype']) 
                value = self.df.loc[index,'RCP_id']
            for key in rcps_status:
                (number,port,maxconnect,camgroup_instanciated) = rcps_status[key]
                if camgroup_instanciated :
                    port = 0
                    camgroup_instanciated = False
                    number += 1
                rcps_status[key] = (number,port,maxconnect,camgroup_instanciated)
    # Optimize the number of RCPs required
    def rcp_optimize(self):
        def get_rcptype_rcp_id(current_RCP,occurences):
            if current_RCP[0:12] == "CY-RCP-DUO-J": 
                rcptype = "CY-RCP-DUO-J"
                postfix = current_RCP[12:]
            elif current_RCP[0:8] == "CY-RCP-J":
                postfix =  current_RCP[8:]
                if occurences < 3 : 
                    rcptype = "CY-RCP-DUO-J_"
                elif occurences < 5 :
                    rcptype = "CY-RCP-QUATTRO-J"
                elif occurences < 9 :
                    rcptype = "CY-RCP-OCTO-J"
                else:
                    rcptype = current_RCP
            elif current_RCP[0:6] == "CY-RCP":
                postfix =  current_RCP[6:]
                if occurences < 3 :
                    rcptype = "CY-RCP-DUO"
                elif occurences < 5 :
                    rcptype = "CY-RCP-QUATTRO"
                elif occurences < 9 :
                    rcptype = "CY-RCP-OCTO"
                else:
                    rcptype = current_RCP
            else: 
                rcptype = current_RCP
                postfix = ""
            return((rcptype,rcptype+postfix))
        rcp_ids = self.df['RCP_id'].unique() 
        for rcp_id in rcp_ids:
            occurences = self.df['RCP_id'].value_counts().get(rcp_id, 0) 
            rcp_indexes  = self.df.loc[self.df['RCP_id'] == rcp_id].index.tolist() 
            for index in rcp_indexes:
                (RCPtype, RCP_id)=get_rcptype_rcp_id(rcp_id,occurences)
                self.df.loc[index,'RCP_id'] = RCP_id 
                self.df.loc[index,'RCPtype'] = RCPtype 
    def count(self):
        def rcp_count(gear_df):
            rcp_ids = gear_df['RCP_id'].unique()
            rcps = {}
            for rcp_id in rcp_ids:
                rcp_index  = gear_df.loc[gear_df['RCP_id'] == rcp_id].index.tolist()[0]
                rcp_type   = gear_df.loc[rcp_index,'RCPtype']
                if rcp_type not in rcps: 
                    rcps[rcp_type] = 1
                else:
                    rcps[rcp_type] += 1
            return rcps
        def cable_count(gear_df):
            cable_types = gear_df['Cable'].unique()
            cables = {}
            for cable_type in cable_types:
                cables[cable_type] = gear_df['Cable'].tolist().count(cable_type)
            return cables
        def device_count(gear_df):
            device_ids = self.df['Device_id'].unique()
            devices = {}
            for device_id in device_ids:
                device_index  = gear_df.loc[gear_df['Device_id'] == device_id].index.tolist()[0]
                device_type   = gear_df.loc[device_index,'Device']
                if device_type not in devices: 
                    devices[device_type] = 1
                else:
                    devices[device_type] += 1
            return devices
        self.rcps    = rcp_count(self.df)
        self.cables  = cable_count(self.df)
        self.devices = device_count(self.df)

    def analyze(self):
        # self.create_gear()
        self.df = InstancesAsRows(self.pool.df).df
        self.dic = InstancesAsObjects(self.pool.df).dic
        self.devices_state = DevicesState(self.pool.df)
        # Set the cable from current parameter values
        self.df[['LensCable','MotorCable','LensMotor']]=self.df.apply(self.adapter,axis=1)
        # # IP or serial converter
        self.df[['Device']]    = self.df.apply(self.device_direct,axis=1)
        self.df[['Fanout']]    = self.df.apply(self.fanout,axis=1)
        self.df[['Device']]    = self.df.apply(self.device_network,axis=1)
        self.df[['Camgroup']]  = self.df.apply(self.camgroup, axis=1)
        # Compute device_id from running through dataframe index
        # self.df[['Device_id']] = self.df.apply(self.device_id,axis=1)
        # Compute device_id from running through camgroups not through dataframe index
        self.device_id_from_device()
        self.df[['Switch_id']] = self.df.apply(self.switch_id_from_camgroup, axis=1)
        self.df[['RCPtype']] = self.df.apply(self.rcptype, axis=1)    
        # Compute device_id from running through camgroups not through dataframe index
        self.rcp_id_from_camgroup()
        self.rcp_optimize()
        self.count()
        self.df.to_csv("./debug/cyangear_df.csv")
