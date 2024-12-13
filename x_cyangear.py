import pandas as pd
from pool import Pool
from cyancameralens import CameraLens
from cyanglue import *
from cyanmedium import Medium
from cyanrcp import *

class Cyangear():
    def __init__(self,pool) -> None:
        self.pool = pool
#        self.df = pool.df
        self.dic= {}
        self.devices_state = DevicesState(self.pool.df)
    def setdf(self,df):
        self.df = df
    # Setup Cyangear dataframe with instancied nodes from Pool dataframe
    def instances_df(self):
        # Create a dictionnary from the Pool dataframe with 
        #     key = instance name based on dataframe index
        #     data = dataframe row retlated to the index as a list
        def dataframe_to_dic():
            paths_dict = {}
            if not self.pool.df.empty:
                for camera_index in self.pool.df.index.to_list():
                    for i in range(int(self.pool.df.loc[camera_index,'Number'])):
                        new_index = str(camera_index) + "_" + str(i) 
                        variables = []
                        variables.extend(self.pool.df.loc[camera_index].tolist())
                        paths_dict[new_index] = list(variables)
            return (paths_dict)
        # Create a dataframe from dictionnary   
        def dic_to_dataframe(paths_dict):
            df = pd.DataFrame.from_dict(paths_dict, orient = 'index', columns = self.pool.df.columns.values)
            df.index.name = 'Instance'     
            return(df)
        # Suppress and add columns
        def columns():
            # Suppressunused column
            self.df.drop(columns=['SupportURL', 'ManufacturerURL','Remark','Selected','Message'], inplace=True)
            # Add result columns storing the results of protocol analyse
            self.df['Camera_id'] = self.df.index
            self.df['Device']    = ""
            self.df['Device_id'] = ""
            self.df['Switch_id'] = ""
            self.df['RCP_id']    = ""
            self.df['Camgroup']  = ""
            self.df['RCPtype']   = ""
            self.df['Fanout']    = 0
            # Add result columns storing the results of lens analyse
            self.df['LensCable']  = ""
            self.df['MotorCable'] = ""
            self.df['LensMotor']  = ""
            # User's Need parameters
            self.df['LensControlNeed']  = "No Need"
            self.df['LensTypeNeed']     = "TBD"
            self.df['LensMotorNeed']    = "TBD"
            return
        if not self.pool.df.empty:
            paths_dict = dataframe_to_dic()
            self.df = dic_to_dataframe(paths_dict)
            columns()       
        return 
    # Create a dictionnary of objects associated to the dataframe index
    def set_objects_dic(self):
        for index in self.df.index.to_list():
            df_row = self.df.loc[index]
            # cameralens = CameraLens(index,df_row["Reference"],df_row["Protocol"],df_row["Cable"])
            cameralens = CameraLens()
            glue   = GlueTBD() 
            medium = Medium()
            rcp    = RCP_TBD()
            self.dic[index]= (cameralens,glue,medium,rcp)
    def adapter(self,row):
        parameters=(row['Type'],row['Brand'],row['Reference'],row['LensControlNeed'],row['LensTypeNeed'],row['LensMotorNeed'])
        accessories =CameraLens.adapter(parameters)
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
            # print("Camgroup:",camgroup)
            for index in camgroup_indexes:
                device = self.df.loc[index,'Device']
                fanout = self.df.loc[index,'Fanout']
                self.df.loc[index,'Device_id'] = devices_state.get_device_id(device,fanout)
                print(f'usecase-->_network-->get_device_id->device_status=\n{devices_state.devices[device]}\n Fanout = {fanout}')
                value = (self.df.loc[index,'LensCable'],self.df.loc[index,'MotorCable'],self.df.loc[index,'LensMotor'])
                print(f'CABLES: {value}\n')
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
                print(f'!!!!RCP_ID: {value}')
            print(f"CAMGROUPS: {camgroup}, RCPS_STATUS: {rcps_status}")
            for key in rcps_status:
                (number,port,maxconnect,camgroup_instanciated) = rcps_status[key]
                if camgroup_instanciated :
                    port = 0
                    camgroup_instanciated = False
                    number += 1
                rcps_status[key] = (number,port,maxconnect,camgroup_instanciated)
            print(f"END CAMGROUPS: {camgroup}, RCPS_STATUS: {rcps_status}")
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
                #??self.df.loc[index,'RCPtype'] = RCPtype 
    def rcp_count(self):
        self.rcps = {}
        rcp_ids = self.df['RCP_id'].unique()
        for rcp_id in rcp_ids:
            rcp_index  = self.df.loc[self.df['RCP_id'] == rcp_id].index.tolist()[0]
            rcp_type   = self.df.loc[rcp_index,'RCPtype']
            if rcp_type not in self.rcps: 
                self.rcps[rcp_type] = 1
            else:
                self.rcps[rcp_type] += 1
    # Count Cables for quoting
    def cable_count(self):
        self.cables = {}
        cable_types = self.df['Cable'].unique()
        for cable_type in cable_types:
            self.cables[cable_type] = self.df['Cable'].tolist().count(cable_type)
    # Count devices for quoting
    def device_count(self):
        self.devices = {}
        device_ids = self.df['Device_id'].unique()
        for device_id in device_ids:
            device_index  = self.df.loc[self.df['Device_id'] == device_id].index.tolist()[0]
            device_type   = self.df.loc[device_index,'Device']
            if device_type not in self.devices: 
                self.devices[device_type] = 1
            else:
                self.devices[device_type] += 1
    def analyze(self):
        self.instances_df()
        self.set_objects_dic()
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
        self.rcp_count()
        self.cable_count()
        self.device_count()
        # if global_debug_usecase_record: debug_usecase_to_csv(self.df,global_debug_prefix)
        # print('########## RCPs :',self.rcps)
        # print('########## DEVICES :',self.devices)
        # print('########## CABLEs :',self.cables)
        pass
