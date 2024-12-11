import csv
import re
import pickle
from camera  import CameraTabView
from cyangear import Cyangear

class Messages():
    def __init__(self) -> None:
        self.dic={}
        self.pkl_messages()
        return
    def pkl_messages(self):
        with open('./picklized/messages.pkl', 'rb') as file:
            self.dic = pickle.load(file)        
        return
    def display(self,object=None, subtopic=""):
        if isinstance(object,CameraTabView):
            return self.cameras(object.selected)
        elif isinstance(object,Cyangear):
            return self.cyangear(object)
        else:
            search_topic    = "instance"
            search_subtopic = "general" if subtopic == "" else subtopic
            message = self.dic[search_topic][search_subtopic]
            return(message)
    def cameras(self,df):
        def control_message(controlLevel):
            match controlLevel:
                case 0: return "no control"
                case 1|2: return "a basic control"
                case 3|4: return "a good control"
                case 5: return "an advanced control"
                case _: return "to be defined"
        message = ""
        if df.empty:
            message = ""
        else:
            print(df)
            print(df.columns)
            for camera in df.index.to_list():
                model = camera
                reference = df.loc[camera,'Reference']
                controlcoverage = df.loc[camera,"ControlCoverage"]
                supporturl = df.loc[camera,"SupportURL"]
                brand = df.loc[camera,"Brand"]
                manufacturerurl = df.loc[camera,"ManufacturerURL"]
                message += self.dic['camera']['performance'].format(model=model,reference=reference,control=control_message(controlcoverage),
                                                                   supporturl=supporturl,brand=brand,manufacturerurl=manufacturerurl)
                message += "\n"
                if (df.loc[camera,'Bidirectionnal']) == "No":
                    message += ("\n" + self.dic['camera']['unidirectional'])
        return(message)
    def cyangear(self,object):
        message = ""
        if object.df.empty:
            message = ""
            print("CYANGEAR DATAFRAME IS EMPTY … ")
        else:
            message+=self.dic['quote']['general']
            message += "\n"
            message+=self.dic['quote']['rcps']
            for rcp_type,rcp_number in object.rcps.items():
                message += f'  - {rcp_type} x {rcp_number}'
                message += "\n"
            message+=self.dic['quote']['devices']
            for device_type,device_number in object.devices.items():
                message += f'  - {device_type} x {device_number}'
                message += "\n"
            message+=self.dic['quote']['cables']
            for cable_type,cable_number in object.cables.items():
                message += f'  - {cable_type} x {cable_number}'
                message += "\n"
        print("CYANGEAR DATAFRAME IS NOT EMPTY … ",message)
        return(message)

if __name__ == "__main__":
    message=Messages()
    print(message.dic) 