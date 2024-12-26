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
    SHOULDER   = "Shoulder Camcorder"
    SYSTEM     = "System"
    BLOCK      = "BBlock"
    SLOWMO     = "Slow Motion"
    CINESTYLE  = "CineStyle"
    MIRRORLESS = "Mirrorless"
    MINICAM    = "Minicam"
    MINIZOOM   = "Minicam IZT" # Should be MiniZoom
    MINIMOT    = "Minicam Motorizable"
    HANDHELD   = "Handheld Camcorder"
    PTZ        = "PTZ"
    TBD        = "TBD"
class CameraCategories(StrEnum):
    BROADCAST        = 'Broadcast'
    CINE_XCHANGE     = 'Cine Interchangeable'
    IZF_INTEGRATED   = 'IZF Integrated'
    FIXED_LENS       = 'Fixed Lens'
    MINICAM_MOT_LENS = 'Minicam Motorizable Lens'
    TBD              = 'TBD'
    def from_camera_type(camera_type):
        if camera_type in [CameraType.SHOULDER,CameraType.SYSTEM,CameraType.BLOCK,CameraType.SLOWMO]:
            return CameraCategories.BROADCAST
        elif camera_type in [CameraType.CINESTYLE,CameraType.MIRRORLESS]:
            return CameraCategories.CINE_XCHANGE
        elif camera_type in [CameraType.HANDHELD,CameraType.PTZ,CameraType.MINIZOOM]:
            return CameraCategories.IZF_INTEGRATED
        elif camera_type in [CameraType.MINICAM]: 
            return CameraCategories.FIXED_LENS
        elif camera_type in [CameraType.MINIMOT]:
            return CameraCategories.MINICAM_MOT_LENS
        else:
            return CameraCategories.TBD 
    def options_lensControlNeeds(camera_category):
        if camera_category == CameraCategories.BROADCAST:
            return [LensControlNeed.NO_NEED,LensControlNeed.IRIS,LensControlNeed.IZF]
        elif camera_category == CameraCategories.CINE_XCHANGE:
            return [LensControlNeed.NO_NEED,LensControlNeed.IRIS,LensControlNeed.IZF]
        elif camera_category == CameraCategories.IZF_INTEGRATED:
            return [LensControlNeed.IZF]
        elif camera_category == CameraCategories.FIXED_LENS:
            return [LensControlNeed.NO_NEED]
        elif camera_category == CameraCategories.MINICAM_MOT_LENS:
            return [LensControlNeed.NO_NEED,LensControlNeed.IZF]
        else:
            return [LensControlNeed.NO_NEED]
    def options_lensTypeNeeds(camera_category):
        if camera_category == CameraCategories.BROADCAST:
            return [LensTypeNeed.B4_MOUNT]
        elif camera_category == CameraCategories.CINE_XCHANGE:
            return [LensTypeNeed.B4_MOUNT,LensTypeNeed.E_MOUNT,LensTypeNeed.CABRIO,LensTypeNeed.CINESERVO,LensTypeNeed.PRIMELENS,LensTypeNeed.MOTORIZED,LensTypeNeed.TBD]
        elif camera_category == CameraCategories.IZF_INTEGRATED:   
            return [LensTypeNeed.CAMERA_IN]
        elif camera_category == CameraCategories.FIXED_LENS:
            return [LensTypeNeed.MANUAL]
        elif camera_category == CameraCategories.MINICAM_MOT_LENS:
            return [LensTypeNeed.MANUAL]
        else:
            return [LensTypeNeed.NONE]
    def options_lensMotorTypeNeeds(camera_category):  
        if camera_category == CameraCategories.BROADCAST:
            return [MotorNeed.NONE] 
        elif camera_category == CameraCategories.CINE_XCHANGE:  
            return [MotorNeed.NONE,MotorNeed.TILTA,MotorNeed.ARRI,MotorNeed.TBD]
        elif camera_category == CameraCategories.IZF_INTEGRATED:
            return [MotorNeed.INTEGRATED]
        elif camera_category == CameraCategories.FIXED_LENS:
            return [MotorNeed.NONE]     
        elif camera_category == CameraCategories.MINICAM_MOT_LENS:
            return [MotorNeed.NONE,MotorNeed.DREAMCHIP]
        else:       
            return [MotorNeed.NONE]      
    def options_needsInit(camera_category):
        if camera_category == CameraCategories.BROADCAST:
            return (LensControlNeed.NO_NEED,LensTypeNeed.B4_MOUNT,MotorNeed.NONE)
        elif camera_category == CameraCategories.CINE_XCHANGE:
            return (LensControlNeed.NO_NEED,LensTypeNeed.TBD,MotorNeed.TBD)
        elif camera_category == CameraCategories.IZF_INTEGRATED:
            return (LensControlNeed.IZF,LensTypeNeed.CAMERA_IN,MotorNeed.INTEGRATED)
        elif camera_category == CameraCategories.FIXED_LENS:
            return (LensControlNeed.NO_NEED,LensTypeNeed.MANUAL,MotorNeed.NONE)
        elif camera_category == CameraCategories.MINICAM_MOT_LENS:
            return (LensControlNeed.NO_NEED,LensTypeNeed.MANUAL,MotorNeed.NONE)
        else:
            return (LensControlNeed.NO_NEED,LensTypeNeed.MANUAL,MotorNeed.NONE)

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