import pandas as pd
from gear_lens import CameraLensGraph
#################### DRAW WITH MERMAID ###########################
class Mermaid():
    def __init__(self) -> None:
        self.df  = pd.DataFrame()
        self.obj = {}
        pass
    def code(self,cyangear):
        def objectize():
            for index in self.df.index.to_list():
                self.obj[(index,'camLens')] = CameraLensGraph(index,self.df.loc[index])
#                self.obj[(index,'medium')]  = MediumBlock(index,self.df.loc[index])
        def clean(code):
            return(code.replace(' ', ''))
        def cameras():
            mermaid_code = ''
            camgroups = self.df['Camgroup'].unique() 
            for camgroup in camgroups:
                camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist()
                mermaid_code+= 'subgraph ' + camgroup + "\n"
                for index in camgroup_indexes:
                    mermaid_code += self.obj[(index,'camLens')].code
                mermaid_code += 'end\n'
            return mermaid_code 
        def networks():
            mermaid_code = ''
            networks = self.df['Network']
            return mermaid_code
        def switches():
            mermaid_code = ''
            switches = self.df['Switch_id'].unique() 
            for switch in switches:
                switch_df  = self.df.loc[self.df['Switch_id'] == switch]
                # We suppose one type of network per camera_type … routing should be reviewed
                network = switch_df['Network'].iloc[0]
                device_ids = switch_df['Device_id'].unique()
                for device_id in device_ids:
                    mermaid_code += clean(device_id) + ' --- |'+ network + '|' + clean(switch) + '\n'
            return mermaid_code
        def rcps():
            mermaid_code = ''
            rcps = self.df['RCP_id'].unique()
            for rcp in rcps:
                switch_df  = self.df.loc[self.df['RCP_id'] == rcp]
                switches  = switch_df['Switch_id'].unique()
                for switch in switches:
                    RCPtype = switch_df['RCPtype'].unique()[0]
                    mermaid_code += clean(switch) + ' --- |Ethernet|' + clean(rcp) + '\n'
            return mermaid_code
                        
        self.df = cyangear.df
        objectize()
        mermaid_code = ''
        mermaid_code = 'graph RL\n'
        mermaid_code += cameras()
        mermaid_code += networks()
        mermaid_code += 'subgraph "Control Room" \n'
        mermaid_code += switches()
        mermaid_code += rcps()
        mermaid_code += 'end\n'
        code = ':::mermaid\n' + mermaid_code  + '\n:::\n' 
        with open('./debug/mermaid_code_obj.md', 'w') as f:
            f.write(code)
        return(mermaid_code)
    