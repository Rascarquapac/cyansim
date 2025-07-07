import pickle
import re
import os
from pprint import pprint

from user_interface  import ViewCamera
from gear import Cyangear

class Messages():
    def __init__(self) -> None:
        self.dic = {}
        pickle_filepath   = './data/messages.pkl' 
        markdown_filepath = './data/Messages.md' 
        if os.path.exists(pickle_filepath):
            self.dic = self.read_pickle(pickle_filepath)
        else:
            self.dic = self.picklize_messages(markdown_filepath,pickle_filepath)
        return
    def read_pickle(self,pickle_filepath):
        with open(pickle_filepath, 'rb') as file:
            message_dic = pickle.load(file)        
        return message_dic
    def picklize_messages(self,markdown_filepath,pickle_filepath):
        message_dic = {}
        def store(topic,subtopic,message):
            if topic not in message_dic : message_dic[topic]={}
            if subtopic not in message_dic[topic]: message_dic[topic][subtopic]={}
            message_dic[topic][subtopic]=message
        p  = re.compile(r"/\[(.*)\,(.*)\]")
        message = ""
        with open(markdown_filepath, 'r') as reader:
            line = reader.readline()
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
                line = reader.readline()
            # Store last message
            store(topic,subtopic,message)           
        with open('./data/messages.pkl', 'wb') as file:
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
            message = "Error: message.gear_list--> Pool.df is empty"
        if not gear.dic:
            message = "Error: message.gear_list--> gear.dic is empty"
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
        return(message)

if __name__ == "__main__":
    message=Messages()
    pprint(message.dic) 