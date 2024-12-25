
class Glue():
    def __init__(self,serial_port_max,usba_port_max,ethernet_port_max,poe_powered):
        self.instance_id = 0
        self.serial_port_used = 0
        self.usba_port_used = 0
        self.ethernet_port_used = 0
        self.instanciated = False
        self.serial_port_max  = serial_port_max
        self.usba_port_max = usba_port_max
        self.ethernet_port_max = ethernet_port_max
        self.poe_powered = poe_powered
    def device_id(self):
        devices_status = DevicesState()
        camgroups = self.df['Camgroup'].unique() 
        for camgroup in camgroups:
            # update_status(devices_status)
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            for index in camgroup_indexes:
                device = self.df.loc[index,'Device']
                fanout = self.df.loc[index,'Fanout']
                self.df.loc[index,'Device_id'] = devices_status.get_device_id(device,fanout)
                value = (self.df.loc[index,'LensCable'],self.df.loc[index,'MotorCable'],self.df.loc[index,'LensMotor'])
            # camgroup_update_status(devices_status)
            devices_status.camgroup_update()

class GlueTBD(Glue):
    def __init__(self):
        super().__init__(0,0,0,False)
class CI0(Glue):
    def __init__(self):
        super().__init__(2,0,0,True)
class CI03P(Glue):
    def __init__(self):
        super().__init__(3,0,0,True)
class RSBM(Glue):
    def __init__(self):
        super().__init__(0,0,0,True)
        self.sdi_in_port = 1
        self.sdi_out_port = 1
class RIO(Glue):
    def __init__(self):
        super().__init__(2,2,1,False)
class NIO(Glue):
    def __init__(self):
        super().__init__(0,2,1,False)
        self.gpio_used = 0
        self.gpio_max  = 16

# compatibility purposes copied from DevicesStatus in _network.py
class DevicesState():
    def __init__(self,df):
        self.devices = {
            'ci0'      : {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"CI0"},
            'rio'      : {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"RIO"},
            'rio_live' : {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"RIO-LIVE"},
            'rsbm'     : {'current_instance':0,'consumed_connections':0,'max_connections':8  ,'instanciated':False,'name':"RSBM"},
            'ip'       : {'current_instance':0,'consumed_connections':0,'max_connections':100,'instanciated':False,'name':"SWITCH-IP"},
        }
        self.camgroup = None
        self.df       = df
    # update all devices status when changing camgroup
    def camgroup_update(self):
        for device, status in self.devices.items():
            if status['instanciated']:
                status['current_instance'] += 1
                status['consumed_connections'] = 0
            status['instanciated'] = False
    # A new camera row is processed, update the devices_status
    def get_device_id (self,device,fanout):
        device_status = self.devices[device]
        device_status['instanciated'] = True
        if (device_status['consumed_connections'] + fanout) <= device_status['max_connections']:
            # Change only the consumed_connections
            device_status['consumed_connections'] += fanout
        else:
            # Create a new instance and set consumed connections to row fanout
            device_status['consumed_connections'] = fanout
            device_status['current_instance']    += 1
        return (device_status["name"] + "_" + str(device_status['current_instance']))

