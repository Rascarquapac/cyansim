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
class CameraCategory(StrEnum):
    BROADCAST        = 'Broadcast'
    CINE_XCHANGE     = 'Cine Interchangeable'
    IZF_INTEGRATED   = 'IZF Integrated'
    FIXED_LENS       = 'Fixed Lens'
    MINICAM_MOT_LENS = 'Minicam Motorizable Lens'
    TBD              = 'TBD'
    def from_camera_type(camera_type):
        if camera_type in [CameraType.SHOULDER,CameraType.SYSTEM,CameraType.BLOCK,CameraType.SLOWMO]:
            return CameraCategory.BROADCAST
        elif camera_type in [CameraType.CINESTYLE,CameraType.MIRRORLESS]:
            return CameraCategory.CINE_XCHANGE
        elif camera_type in [CameraType.HANDHELD,CameraType.PTZ,CameraType.MINIZOOM]:
            return CameraCategory.IZF_INTEGRATED
        elif camera_type in [CameraType.MINICAM]: 
            return CameraCategory.FIXED_LENS
        elif camera_type in [CameraType.MINIMOT]:
            return CameraCategory.MINICAM_MOT_LENS
        else:
            return CameraCategory.TBD 
    def options_lensControlNeeds(camera_category):
        if camera_category == CameraCategory.BROADCAST:
            return [LensControlNeed.NO_NEED,LensControlNeed.IRIS,LensControlNeed.IZF]
        elif camera_category == CameraCategory.CINE_XCHANGE:
            return [LensControlNeed.NO_NEED,LensControlNeed.IRIS,LensControlNeed.IZF]
        elif camera_category == CameraCategory.IZF_INTEGRATED:
            return [LensControlNeed.IZF]
        elif camera_category == CameraCategory.FIXED_LENS:
            return [LensControlNeed.NO_NEED]
        elif camera_category == CameraCategory.MINICAM_MOT_LENS:
            return [LensControlNeed.NO_NEED,LensControlNeed.IZF]
        else:
            return [LensControlNeed.NO_NEED]
    def options_lensTypeNeeds(camera_category):
        if camera_category == CameraCategory.BROADCAST:
            return [LensTypeNeed.B4_MOUNT]
        elif camera_category == CameraCategory.CINE_XCHANGE:
            return [LensTypeNeed.B4_MOUNT,LensTypeNeed.E_MOUNT,LensTypeNeed.CABRIO,LensTypeNeed.CINESERVO,LensTypeNeed.PRIMELENS,LensTypeNeed.MOTORIZED,LensTypeNeed.TBD]
        elif camera_category == CameraCategory.IZF_INTEGRATED:   
            return [LensTypeNeed.CAMERA_IN]
        elif camera_category == CameraCategory.FIXED_LENS:
            return [LensTypeNeed.MANUAL]
        elif camera_category == CameraCategory.MINICAM_MOT_LENS:
            return [LensTypeNeed.MANUAL]
        else:
            return [LensTypeNeed.NONE]
    def options_lensMotorTypeNeeds(camera_category):  
        if camera_category == CameraCategory.BROADCAST:
            return [MotorNeed.NONE] 
        elif camera_category == CameraCategory.CINE_XCHANGE:  
            return [MotorNeed.NONE,MotorNeed.TILTA,MotorNeed.ARRI,MotorNeed.TBD]
        elif camera_category == CameraCategory.IZF_INTEGRATED:
            return [MotorNeed.INTEGRATED]
        elif camera_category == CameraCategory.FIXED_LENS:
            return [MotorNeed.NONE]     
        elif camera_category == CameraCategory.MINICAM_MOT_LENS:
            return [MotorNeed.NONE,MotorNeed.DREAMCHIP]
        else:       
            return [MotorNeed.NONE]      
    def options_needsInit(camera_category):
        if camera_category == CameraCategory.BROADCAST:
            return (LensControlNeed.NO_NEED,LensTypeNeed.B4_MOUNT,MotorNeed.NONE)
        elif camera_category == CameraCategory.CINE_XCHANGE:
            return (LensControlNeed.NO_NEED,LensTypeNeed.TBD,MotorNeed.TBD)
        elif camera_category == CameraCategory.IZF_INTEGRATED:
            return (LensControlNeed.IZF,LensTypeNeed.CAMERA_IN,MotorNeed.INTEGRATED)
        elif camera_category == CameraCategory.FIXED_LENS:
            return (LensControlNeed.NO_NEED,LensTypeNeed.MANUAL,MotorNeed.NONE)
        elif camera_category == CameraCategory.MINICAM_MOT_LENS:
            return (LensControlNeed.NO_NEED,LensTypeNeed.MANUAL,MotorNeed.NONE)
        else:
            return (LensControlNeed.NO_NEED,LensTypeNeed.MANUAL,MotorNeed.NONE)
class NetworkType(StrEnum):
     LAN_WIRED = "LAN Wired"  
     LAN_RF_HALOW = "LAN RF Halow"
     LAN_RF_MESH = "LAN RF Mesh"  
     LAN_RF_WIFI ="LAN RF WiFi" 
     P2P_RF_PRO_MODEM = "P2P RF Pro Modem" 
     P2P_RF_Unidir = "P2P RF Unidir"
     WAN_4G_5G = "WAN 4G 5G" 
     P2MP_UHF_VIDEO = "P2MP UHF Video" 
# Get a list of all values
class LensType(StrEnum):
    B4_MOUNT  = 'B4-Mount'
    E_MOUNT   = 'E-Mount'
    CABRIO    = 'Cabrio'
    CINESERVO = 'Cineservo'
    PRIMELENS = 'Primelens'
    MOTORIZED = 'Motorized Others'
    TBD       = 'TBD'
    CAMERA_IN = 'Camera Integrated'
    MANUAL    = 'Manual'
class LensMountType(StrEnum):
    B4    = "B4-Mount"
    C     = "C-Mount"
    E     = "E-Mount"
    S     = "S-Mount"
    EF    = "EF-Mount"
    MFT   = "MFT-Mount"
    RF    = "RF-Mount"
    LPL   = "LPL-Mount"
    PL    = "PL-Mount"
    LNE   = "LNE-Mount"
    L     = "L-Mount"
    NXMAN = "No-Xchange-Manual"
    NXMOT = "No-Xchange-Motorized"
    TBD   = "Unknown"


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

if __name__ == "__main__":
    print(CameraCategory.MINICAM_MOT_LENS)
    print([member for member in CameraLensDevice])
    print([member.value for member in CameraLensDevice])
    print([member.name for member in CameraLensDevice])    
    print([member.value for member in NetworkType])
    print("LENSTYPE NAME\n",[member.name for member in LensType])    
    print("LENSTYPENEED NAME\n",[member.name for member in LensTypeNeed])