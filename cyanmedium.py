import pandas as pd
from constants import CameraLensDevice
# compatibility purposes
class DevicesStatus():
    def __init__(self):
        self.ci0      = {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"CI0"}
        self.rio      = {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"RIO"}
        self.rio_live = {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"RIO-LIVE"}
        self.rsbm     = {'current_instance':0,'consumed_connections':0,'max_connections':8  ,'instanciated':False,'name':"RSBM"}
        self.ip       = {'current_instance':0,'consumed_connections':0,'max_connections':100,'instanciated':False,'name':"IP"}
        # update devices status when changing camgroup
    def camgroup_update(self):
        for attribute, status in vars(self).items():
            if status['instanciated']:
                status['current_instance'] += 1
                status['consumed_connections'] = 0
            status['instanciated'] = False
    # A new camera row is processed, update the devices_status
    def get_device_id (self,device,fanout):
        device_status = self.__dict__[device]
        device_status['instanciated'] = True
        if (device_status['consumed_connections'] + fanout) <= device_status['max_connections']:
            # Change only the consumed_connections
            device_status['consumed_connections'] += fanout
        else:
            # Create a new instance and set consumed connections to row fanout
            device_status['consumed_connections'] = fanout
            device_status['current_instance']    += 1
        return (device_status["name"] + "_" + str(device_status['current_instance']))
class Medium():
    def __init__(self) -> None:
        pass
        # Select the converter for each camera and set it in "Device" index. A Specific column could be more appropriate
        # A cable type is already associated to the camera model
        # The function return "CI0" if a serial converter is required or "Passthru"
    @classmethod
    def device_direct(self,camera_cable,lens_cable,motor_cable):
        if lens_cable[0:7]     == "CY-CBL-" : return CameraLensDevice.RIO_LIVE.value
        elif motor_cable[0:7]  == "CY-CBL-" : return CameraLensDevice.RIO_LIVE.value
        elif camera_cable[0:7] == "CY-CBL-" : return CameraLensDevice.CI0.value
        else: pass
        # IP "passthrough" pseudo device
        match camera_cable:
            case "Ethernet-RJ45"  : return CameraLensDevice.IP.value
            case "USB-A-to-USB-C" : return CameraLensDevice.IP.value
            case "IP-to-USB-C"    : return CameraLensDevice.IP.value
            case "BM-SDI"         : return CameraLensDevice.IP.value
            case "JVC USB-to-IP"  : return CameraLensDevice.IP.value 
            case "XDCA back"      : return CameraLensDevice.IP.value 
            case _                : return CameraLensDevice.IP.value 
    # Set the fanout of converter device
    @classmethod
    def fanout(self,camera_cable,lens_cable,motor_cable):
    # A cable type is already associated to the camera model
    # The function return "CI0" if a serial converter is required or "Passthru"
        fanout = 0
        if camera_cable != "No cable" : fanout += 1
        if lens_cable   != "No cable" : fanout += 1
        if motor_cable  != "No cable" : fanout += 1
        # if lens_cable[0:7]   == "CY-CBL-" : fanout += 1
        # if camera_cable[0:7] == "CY-CBL-" : fanout += 1
        return fanout

    # Select the device from network for each camera and set it in "Device" column.
    @classmethod
    def device_network(self,current_device,network,MaxDelayToComplete):
        # Select the device from network associated to the camera
        assert current_device in [member.value for member in CameraLensDevice]
        #TODO: add a check between case values and contraints
        match network:
            case "LAN Wired" : return current_device
            case "LAN RF Halow"    :
                if  MaxDelayToComplete > 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "LAN RF Mesh"    :
                if  MaxDelayToComplete > 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "LAN RF WiFi"    :
                if  MaxDelayToComplete > 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "P2P RF Pro Modem"    :
                if  MaxDelayToComplete > 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "P2P RF Unidir"    :
                if  MaxDelayToComplete > 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "WAN 4G 5G" : return CameraLensDevice.RIO.value
            case "P2MP UHF Video"  : return CameraLensDevice.RIO_LIVE.value
            case _           : return CameraLensDevice.UNDEFINED.value
        return
    # Set the "Camgroup" column with the "Camtype" value: the camera groups are based on camera type 
    @classmethod
    def camgroup(self,camtype,network):
        return camtype
    @classmethod
    # According to device fanout and the camera camgroup instanciate devices and add instance number
    def device_id_from_device(self):
        devices_status = DevicesStatus()
        camgroups = self.df['Camgroup'].unique() 
        for camgroup in camgroups:
            # update_status(devices_status)
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            # print("Camgroup:",camgroup)
            for index in camgroup_indexes:
                device = self.df.loc[index,'Device']
                fanout = self.df.loc[index,'Fanout']
                self.df.loc[index,'Device_id'] = devices_status.get_device_id(device,fanout)
                print(f'usecase-->_network-->get_device_id->device_status=\n{devices_status.__dict__[device]}\n Fanout = {fanout}')
                value = (self.df.loc[index,'LensCable'],self.df.loc[index,'MotorCable'],self.df.loc[index,'LensMotor'])
                print(f'CABLES: {value}\n')
            # camgroup_update_status(devices_status)
            devices_status.camgroup_update()
                # print("    Device_id    : ",self.df.loc[index,'Device_id'])
                # print("    Device Status: ",devices_status)

