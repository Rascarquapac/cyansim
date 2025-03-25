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

class Cable(StrEnum):
    CY_CBL_6P_AJA_01 = 'CY-CBL-6P-AJA-01'
    CY_CBL_6P_B4_01 = 'CY-CBL-6P-B4-01'
    CY_CBL_6P_B4_02 = 'CY-CBL-6P-B4-02'
    CY_CBL_6P_BRADLEY = 'CY-CBL-6P-BRADLEY'
    CY_CBL_6P_CIS_01 = 'CY-CBL-6P-CIS-01'
    CY_CBL_6P_CIS_02 = 'CY-CBL-6P-CIS-02'
    CY_CBL_6P_CN_REM = 'CY-CBL-6P-CN-REM'
    CY_CBL_6P_DCHIP_01 = 'CY-CBL-6P-DCHIP-01'
    CY_CBL_6P_DCHIP_02 = 'CY-CBL-6P-DCHIP-02'
    CY_CBL_6P_DCHIP_03 = 'CY-CBL-6P-DCHIP-03'
    CY_CBL_6P_DCM2 = 'CY-CBL-6P-DCM2'
    CY_CBL_6P_EXT100 = 'CY-CBL-6P-EXT100'
    CY_CBL_6P_EXT1000 = 'CY-CBL-6P-EXT1000'
    CY_CBL_6P_EXT300 = 'CY-CBL-6P-EXT300'
    CY_CBL_6P_EXT50 = 'CY-CBL-6P-EXT50'
    CY_CBL_6P_EXT500 = 'CY-CBL-6P-EXT500'
    CY_CBL_6P_FAN100 = 'CY-CBL-6P-FAN100'
    CY_CBL_6P_FAN20 = 'CY-CBL-6P-FAN20'
    CY_CBL_6P_FUJI = 'CY-CBL-6P-FUJI'
    CY_CBL_6P_FUJI_02 = 'CY-CBL-6P-FUJI-02'
    CY_CBL_6P_FUJI_03 = 'CY-CBL-6P-FUJI-03'
    CY_CBL_6P_IOI = 'CY-CBL-6P-IOI'
    CY_CBL_6P_LANC_1 = 'CY-CBL-6P-LANC-1'
    CY_CBL_6P_LANC_2 = 'CY-CBL-6P-LANC-2'
    CY_CBL_6P_MARS_01 = 'CY-CBL-6P-MARS-01'
    CY_CBL_6P_MARS_02 = 'CY-CBL-6P-MARS-02'
    CY_CBL_6P_PAN_10P = 'CY-CBL-6P-PAN-10P'
    CY_CBL_6P_PFAN = 'CY-CBL-6P-PFAN'
    CY_CBL_6P_PWR = 'CY-CBL-6P-PWR'
    CY_CBL_6P_ST_15 = 'CY-CBL-6P-ST-15'
    CY_CBL_6P_ST_50 = 'CY-CBL-6P-ST-50'
    CY_CBL_6P_TALLY = 'CY-CBL-6P-TALLY'
    CY_CBL_6P_TOSH_01 = 'CY-CBL-6P-TOSH-01'
    CY_CBL_6P_X3 = 'CY-CBL-6P-X3'
    CY_CBL_ASTRO_01 = 'CY-CBL-ASTRO-01'
    CY_CBL_ASTRO_02 = 'CY-CBL-ASTRO-02'
    CY_CBL_DTAP = 'CY-CBL-DTAP'
    CY_CBL_JACK_GPIO8 = 'CY-CBL-JACK-GPIO8'
    CY_CBL_SONY_8P_03 = 'CY-CBL-SONY-8P-03'
    CY_CBL_TILTA_SERIAL = 'CY-CBL-TILTA-SERIAL'
    CY_CBL_TILTA_USB = 'CY-CBL-TILTA-USB'
    WiFi = 'WiFi'
    IP_to_USB_C = 'IP-to-USB-C'
    USB_A_to_USB_C = 'USB-A-to-USB-C'
    Ethernet_RJ45 = 'Ethernet-RJ45'
    BM_SDI = 'BM-SDI'
    JVC_USB_to_IP = 'JVC-USB-to-IP'
    XDCA_back = 'XDCA-back'
    Undefined = 'Undefined'

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