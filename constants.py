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

class CameraLens():
	def __init__(self) -> None:
		self.camera_types = [member.value for member in CameraType]
		# self.camera_types = ["Smartphone","BBlock","CineStyle","Handheld Camcorder","Minicam","Minicam Motorizable","Minicam IZT","Mirrorless","PTZ","Shoulder Camcorder","Slow Motion","System","TBD"]
		self.camera_categories = [member.value for member in CameraCategory]
		# self.camera_categories = ['Broadcast','Cine Interchangeable','IZF Integrated','Fixed Lens','Minicam Motorizable Lens','TBD' ]
		# User options of IZF control per camera category
		self.options_needs_lensControl={
			 'Broadcast':['No Need','Iris','IZF'],
			 'Cine Interchangeable':['No Need','Iris','IZF'],
			 'IZF Integrated':['IZF'],
			 'Fixed Lens':['No Need'],
			 'Minicam Motorizable Lens':['No Need','IZF'],
			 'TBD' :["No Need"]
		}
		# User options of lens type per camera category
		self.options_needs_lensType={
			 'Broadcast':['B4-Mount'],
			 'Cine Interchangeable':['B4-Mount','E-Mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD'],
			 'IZF Integrated':['Camera Integrated'],
			 'Fixed Lens':['Manual'], # "Manual" only ?
			 'Minicam Motorizable Lens':['Manual'],
			 'TBD' :["No Need"]
		}
		# User options of motor type per camera category
		self.options_needs_motorType={
			 'Broadcast':['No extra motors'],
			 'Cine Interchangeable':['No extra motors','Tilta','Arri','TBD'],
			 'IZF Integrated':['Camera Integrated'],
			 'Fixed Lens':['Manual'], # "Manual" only ?
			 'Minicam Motorizable Lens':['No extra motors','Dreamchip'],
			 'TBD' :['No extra motors']
		}
		# Initial values for user options per camera category (lensControl,lensType,motorType)
		self.options_needs_init = {
			"Broadcast" : ('No Need','B4-Mount','No extra motors'),
			"Cine Interchangeable" : ('No Need','TBD','TBD'),
			"IZF Integrated" : ('IZF','Camera Integrated','No extra motors'),
			"Fixed Lens" : ("No Need",'Manual','No extra motors'),
			'Minicam Motorizable Lens' : ("No Need",'Manual','No extra motors'),
			"TBD" : ("No Need",'Manual','No extra motors')
		}
				# case "Broadcast": return ('No Need','B4-Mount','No extra motors')
				# case "Cine Interchangeable": return ('No Need','TBD','TBD')
				# case "IZF Integrated": return ('IZF','Camera Integrated','No extra motors')
				# case "Fixed Lens": return ("No Need",'Fixed and Manual','No extra motors')
				# case "TBD": return ("No Need",'Fixed and Manual','No extra motors')    
	# Select camera cable + lens cable + lens motor from user needs in Cyanview control
	@classmethod
	def adapters(self,parameters):
		# GET LIST OF ADAPTERS FOR A GIVEN COMBINATION OF LENS CONTROL, LENS TYPE AND LENS MOTOR
		def check(parameters):
			(cameraType,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
			## DUPLICATE !!!!
			if cameraType not in ["BBlock","CineStyle","Handheld Camcorder","Minicam","Minicam Motorizable","Minicam IZT","Mirrorless","PTZ","Shoulder Camcorder","Slow Motion","System","TBD"]:
				raise KeyError(f"cameraType= {cameraType}")
			# if cameraMount not in ['B4-Mount','C-Mount','E-Mount','S-Mount','EF-Mount','MFT-Mount','RF-Mount','LPL-Mount','PL-Mount','LNE-Mount','L-Mount','No-Xchange-Manual','No-Xchange-Motorized','TBD']:
			#     raise KeyError(f"cameraMount= {cameraMount}")
			if lensControl not in ['No Need','Iris','IZF']:
				raise KeyError(f"lensControl= {lensControl}")
			if lensType not in ['B4-Mount','E-Mount','Cabrio','Cineservo','Primelens','Motorized Others','Camera Integrated','Manual','No Need','TBD']:
				raise KeyError(f"lensType= {lensType}")
			if lensMotor not in ['No extra motors','Tilta','Arri','Dreamchip','TBD']:
				raise KeyError(f"lensMotor= {lensMotor}")
			return
		(cameraType,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
		check(parameters)
		# define constant values
		(no_cable,cable_B4,cable_tilta,cable_fuji,cable_arri) = ("No cable","CY-CBL-6P-B4-02","CY-CBL-6P-TILTA-SERIAL","CY-CBL-6P-FUJI-02","ARRI CForce cable")
		(no_motor,motor_arri,motor_tilta,motor_dreamchip) = ("No motor","Arri","Tilta","Dreamchip")
		# Set cameraLensCategory
		cameraLensCategory = self.cameraLens_category(cameraType)
		# Set cables and motors
		# print("\nDBG CameraLens.adapter parameters=",parameters,cameraLensCategory)
		match (cameraLensCategory,cameraBrand,cameraModel,lensControl,lensType,lensMotor):
			# No Cyanview lens control is needed
			case(a,b,c,"No Need",e,f) : 
				result = (no_cable,no_cable,no_motor,"No lens control by Cyanview is requested by the user")
			# Broadcast camera have a B4-mount
			case ("Broadcast",b,c,"Iris",e,f) : 
				result = (no_cable,no_cable,no_motor,"The lens iris is controllable trhough the camera protocol. No extra cable is required")
			case ("Broadcast",b,c,"IZF",e,f)  : 
				result = (cable_B4,no_cable,no_motor,"The lens iris is controllable trhough the camera protocol but an extra B4 cable is required to control Zoom and Focus")
			#  Camera with no lens interchange cannot be controlled
			case ("IZF Integrated",b,c,d,e,f)    : 
				result = (no_cable,no_cable,no_motor,"The lens could not be interchanged and lens could be controlled through the camera prorocol")
			#  Camera with no lens interchange cannot be controlled
			case ("Fixed Lens",b,c,d,e,f)    : 
				result = (no_cable,no_cable,no_motor,"The lens could not be interchanged and there is probably no motor solution for this case")
			# CineStyle, Mirrorless, Mini camera with lens interchange
			# Canon cameras and (Cineservo or B4-Mount)
			case ("Cine Interchangeable","Canon",c,d,"Cineservo",f) : 
				result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
			case ("Cine Interchangeable","Canon",c,d,"B4-Mount",f) : 
				result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
			# URSA cameras and (Cineservo or B4-Mount)
			case ("Cine Interchangeable",b,"URSA",d,"Cineservo",f) :
				result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera")
			case ("Cine Interchangeable",b,"URSA",d,"B4-Mount",f) :
				result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera") 
			# (Neither URSA nor Canon cameras) and (Cineservo or B4-Mount)
			case ("Cine Interchangeable",b,c,"Iris","Cineservo",f) :
				result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
			case ("Cine Interchangeable",b,c,"IZF","Cineservo",f) :
				result =(cable_B4,no_cable,no_motor,"Cyanview B4 adapter is require for Zoom/Focus control")
			case ("Cine Interchangeable",b,c,"Iris","B4-Mount",f) :
				result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
			case ("Cine Interchangeable",b,c,"IZF","B4-Mount",f) :
				result =(cable_B4,no_cable,no_motor,"Cyanview B4 adapter is require for Zoom/Focus control")
			# E-Mount lens (only Sony cameras ??? XDE)
			case ("Cine Interchangeable",b,c,"Iris","E-mount",f) :
				result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
			case ("Cine Interchangeable",b,c,"IZF","E-mount",f) :
				result =(no_cable,cable_tilta,motor_tilta,"Adding Tilta motors and Cyanview Tilta adapter is required for Zoom/Focus control")
			# Cabrio lens
			case ("Cine Interchangeable",b,c,d,"Cabrio",f) : 
				result = (f'{cable_B4} +\n{cable_fuji}',no_motor,no_cable,"The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
			# Primelens (or… RTI) Motors
			case ("Cine Interchangeable",b,c,d,"Primelens","Tilta") : 
				result = (no_cable,cable_tilta,motor_tilta,"The user needs the control of Iris/Zoom/Focus, it cannot be done through the camera and the user want to use Tilta motors")
			case ("Cine Interchangeable",b,c,d,"Primelens","Arri") : 
				result = (no_cable,cable_arri,motor_arri,"The user needs the control of Iris/Focus, it cannot be done through the camera and the user want to use ARRI motors")
			case ("Cine Interchangeable","Dreamchip",c,d,e,"Dreamchip") : 
				result = (no_cable,no_cable,motor_dreamchip,"The user needs the control of Iris/Zoom and it can be done through the camera")
			case _: 
				result =(no_cable,no_cable,no_motor,"This case is probably not supported")
		# print("DBG CameraLens.adapter result=",result)  
		return result
		
	########## FLAT ANALYZIS
		self.camera_type='TBD' 
		self.camera_category='TBD' 
	@classmethod
	def cameraLens_category(self,cameraType):
		# cameraMount can be suppressed except for exception
		match (cameraType):
			case (CameraType.TBD.value) : 
				cameraLensCategory = CameraCategory.TBD.value
			case (CameraType.SLOWMO.value) | (CameraType.SYSTEM.value) | (CameraType.BLOCK.value) | (CameraType.SHOULDER.value) : 
				cameraLensCategory = CameraCategory.BROADCAST.value
			case (CameraType.CINESTYLE.value)|(CameraType.MIRRORLESS.value) | (CameraType.SMARTPHONE.value)       : 
				cameraLensCategory = CameraCategory.CINE_XCHANGE.value
			case (CameraType.PTZ.value) | (CameraType.HANDHELD.value) | (CameraType.MINIZOOM.value)   : 
				cameraLensCategory = CameraCategory.IZF_INTEGRATED.value
			case (CameraType.MINICAM.value)    : 
				cameraLensCategory = CameraCategory.FIXED_LENS.value
			case (CameraType.MINIMOT.value) : 
				cameraLensCategory = CameraCategory.MINICAM_MOT_LENS.value
			case _: raise KeyError(f"cameraType= {cameraType}")
		# match (cameraType):
		# 	case ("TBD") : 
		# 		cameraLensCategory = "TBD"
		# 	case ("Slow Motion") | ("System") | ("BBlock") | ("Shoulder Camcorder") : 
		# 		cameraLensCategory = "Broadcast"
		# 	case ("CineStyle")|("Mirrorless") | ("Smartphone")       : 
		# 		cameraLensCategory = "Cine Interchangeable"
		# 	case ("PTZ") | ("Handheld Camcorder") | ("Minicam IZT")   : 
		# 		cameraLensCategory = "IZF Integrated"
		# 	case ("Minicam")    : 
		# 		cameraLensCategory = "Fixed Lens"
		# 	case ("Minicam Motorizable") : 
		# 		cameraLensCategory = "Minicam Motorizable Lens"
		# 	case _: raise KeyError(f"cameraType= {cameraType}")
		return cameraLensCategory


############################# INPUT TYPE CHECKING #############################
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
    SMARTPHONE = "Smartphone"
    TBD        = "TBD"
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
class BrandType(StrEnum):
    ADIMEC='Adimec'
    AIDA='Aida'
    AJA='Aja'
    ARC='ARC'
    ARRI='ARRI'
    ASTRODESIGN='AstroDesign'
    BELL='Bell'
    BIRDDOG='BirdDog'
    BLACKMAGIC='BlackMagic'
    BRADLEY='Bradley'
    CAMERACORPS='CameraCorps'
    CANON='Canon'
    CIS='CIS'
    CYAN='Cyan'
    DREAMCHIP='DreamChip'
    GRASSVALLEY='GrassValley'
    HAIVISION='Haivision'
    HITACHI='Hitachi'
    IKEGAMI='Ikegami'
    IOI='IOI'
    JVC='JVC'
    LUMENS='Lumens'
    MARSHALL='Marshall'
    MEDIAEDGE='MediaEdge'
    NONE='None'
    PACIFIC_CORP='Pacific Corp.'
    PANASONIC='Panasonic'
    RED='RED'
    ROBOSHOT='RoboSHOT'
    ROSS='Ross'
    SONY='Sony'
    TOSHIBA='Toshiba'
    VHD='VHD'
    VISIONRESEARCH='VisionResearch'
    YUSHIDA='Yushida'
class AdapterType(StrEnum):
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
    JVC_USB_to_IP = 'JVC USB-to-IP'
    XDCA_back = 'XDCA back'
    Undefined = 'Undefined'
    CUSTOM = 'Custom'
 
############################# INTERNAL TYPE CHECKING #############################
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