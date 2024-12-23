import pickle
import re
import os
from pprint import pprint

from view_camera  import ViewCamera
from gear import Cyangear

class Messages():
    def __init__(self) -> None:
        self.dic = {}
        pickle_filepath = './picklized/messages.pkl' 
        if os.path.exists(pickle_filepath):
            self.dic = self.read_pickle()
        else:
            self.dic = self.picklize_messages()
        return
    def read_pickle(self):
        with open('./picklized/messages.pkl', 'rb') as file:
            message_dic = pickle.load(file)        
        return message_dic
    def picklize_messages(self):
        message_dic = {}
        def store(topic,subtopic,message):
            if topic not in message_dic : message_dic[topic]={}
            if subtopic not in message_dic[topic]: message_dic[topic][subtopic]={}
            message_dic[topic][subtopic]=message
        p  = re.compile(r"/\[(.*)\,(.*)\]")
        message = ""
        with open('./Messages.md', 'r') as reader:
            line = reader.readline()
            print("Line: ",line)
            first_line = True
            while line != '':  # The EOF char is an empty string
                if line[0:2]== "/[":
                    if first_line:
                        # No message to store
                        first_line = False
                    else:
                        # Store currently collected message
                        store(topic,subtopic,message)
                        message = ""
                    result   = p.search(line)
                    topic    = result.group(1)
                    subtopic = result.group(2)
                else:
                    message += line
                    # print("Keys: ",context, state,name)
                    # print("Message: ",message)
                line = reader.readline()
            # Store last message
            store(topic,subtopic,message)           
        with open('./picklized/messages.pkl', 'wb') as file:
            pickle.dump(message_dic, file)
        return (message_dic)
    def camera_comments(self,camera):
        def control_message(controlLevel):
            match controlLevel:
                case 0: return "no control"
                case 1|2: return "a basic control"
                case 3|4: return "a good control"
                case 5: return "an advanced control"
                case _: return "to be defined"
        df = camera.selected 
        message = ""
        if df.empty:
            message = ""
        else:
            # print(df)
            # print(df.columns)
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
    def gear_list(self,gear):
        message = ""
        if gear.pool.df.empty:
            message = ""
            print("POOL DATAFRAME IS EMPTY … ")
        if not gear.dic:
            message = ""
            print("CYANGEAR ATTRIBUTES ARE EMPTY … ")
        else:
            message+=self.dic['quote']['general']
            message += "\n"
            message+=self.dic['quote']['rcps']
            for rcp_type,rcp_number in gear.rcps.items():
                message += f'  - {rcp_type} x {rcp_number}'
                message += "\n"
            message+=self.dic['quote']['devices']
            for device_type,device_number in gear.devices.items():
                message += f'  - {device_type.upper()} x {device_number}'
                message += "\n"
            message+=self.dic['quote']['cables']
            for cable_type,cable_number in gear.cables.items():
                message += f'  - {cable_type} x {cable_number}'
                message += "\n"
        # print("CYANGEAR DATAFRAME IS NOT EMPTY … ",message)
        return(message)

if __name__ == "__main__":
    message=Messages()
    pprint(message.dic) 