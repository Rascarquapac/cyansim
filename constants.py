from enum import StrEnum,auto,unique
@unique
class CameraLensDevice (StrEnum):
    IP        = auto()  # Transparent connection
    CI0       = auto()  # Simple serial to IP conversion
    RIO_LIVE  = auto()  # Serial to IP with multiple USB/IP connectors and LAN packets management
    RIO       = auto()  # Serial to IP  with multiple USB/connector, LAN and WAN packets management
    NIO       = auto()  # Multiple USB/connector, LAN packets management
    RSBM      = auto()  # IPtoBlackMagic SDI 
    UNDEFINED = auto()  # Undefined device
class CameraProtocol():
    def __init__(self,brand,type,cable,supportURL,max_delay,control_coverage,bidirectionnal):
        self.brand = brand
        self.type = type
        self.cable = cable
        self.supportURL = supportURL
        self.max_delay = max_delay
        self.control_coverage = control_coverage
        self.bidirectional = bidirectionnal
class Camera(CameraProtocol):
    def __init__(self,protocol,model,reference,mount,b4_connector):
        for key,value in protocol.__dict__.items():
            self.__dict__[key] = value
        self.model     = model
        self.reference = reference
        self.mount     = mount
        self.b4_connector = b4_connector
class LensControlNeed(StrEnum):
    NO_NEED = 'No need' # No Need of Cyanview control for lens
    IRIS    = 'Iris' # Need of Cynaview control for Iris only
    IZF     = 'IZF' # Need of Cyanview control for Iris, Zoom, Focus
class LensTypeNeed(StrEnum):
    B4_MOUNT  = 'B4-Mount'
    E_MOUNT   = 'E-Mount'
    CABRIO    = 'Cabrio'
    CINESERVO = 'Cineservo'
    PRIMELENS = 'Primelens'
    MOTORIZED = 'Motorized Others'
    TBD       = 'TBD'
    CAMERA_IN = 'Camera Integrated'
    MANUAL    = 'Manual'
    NONE      = 'No Need' # ! "No need" ?
class MotorNeed(StrEnum):
    NONE = 'No extra motors'
    INTEGRATED = 'Camera Integrated'
    TILTA = 'Tilta'
    ARRI = 'Arri'
    DREAMCHIP = 'Dreamchip'
    TBD = 'TBD'
class CameraType(StrEnum):
    BLOCK = "BBlock"
    CINESTYLE = "CineStyle"
    HANDHELD = "Handheld Camcorder"
    MINICAM = "Minicam"
    MINIMOT = "Minicam Motorizable"
    MIRRORLESS = "Mirrorless"
    PTZ = "PTZ"
    SHOULDER = "Shoulder Camcorder"
    SLOWMO = "Slow Motion"
    SYSTEM = "System"
    TBD = "TBD"
class CameraCategories(StrEnum):
    BROADCAST = 'Broadcast'
    CINE_XCHANGE = 'Cine Interchangeable'
    IZF_INTEGRATED = 'IZF Integrated'
    FIXED_LENS = 'Fixed Lens'
    MINICAM_MOT_LENS= 'Minicam Motorizable Lens'
    TBD = 'TBD' 
class Network_Enum(StrEnum):
     LAN_WIRED = "LAN Wired"  
     LAN_RF_HALOW = "LAN RF Halow"
     LAN_RF_MESH = "LAN RF Mesh"  
     LAN_RF_WIFI ="LAN RF WiFi" 
     P2P_RF_PRO_MODEM = "P2P RF Pro Modem" 
     P2P_RF_Unidir = "P2P RF Unidir"
     WAN_4G_5G = "WAN 4G 5G" 
     P2MP_UHF_VIDEO = "P2MP UHF Video" 
# Get a list of all values
if __name__ == "__main__":
    print(CameraCategories.MINICAM_MOT_LENS)
    print([member for member in CameraLensDevice])
    print([member.value for member in CameraLensDevice])
    print([member.name for member in CameraLensDevice])    
    print([member.value for member in Network_Enum])
    print([member.name for member in Network_Enum])