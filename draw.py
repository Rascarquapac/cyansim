import base64
import mermaid as md
import pandas as pd
from mermaid.graph  import Graph
from draw_mermaid import Mermaid
from difflib import Differ
from logger_config import setup_logger
logger = setup_logger()

#################### DRAW WITH MERMAID ###########################
class Draw():
    def __init__(self) -> None:
        self.df      = pd.DataFrame()
        self.mermaid = Mermaid()
        self.obj = {}
        self.mermaid_test_code =  """
            graph RL
            subgraph Mini Camera
            AtomOne4K_0{{"AtomOne4K_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
            AtomOne4K_1{{"AtomOne4K_1 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
            AtomOne4K_2{{"AtomOne4K_2 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_1
            AtomOne4K_3{{"AtomOne4K_3 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_1
            CV225_0{{"CV225_0 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_2
            CV225_1{{"CV225_1 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_2
            end
            subgraph PTZ
            AW-HE130_0{{"AW-HE130_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            AW-HE130_1{{"AW-HE130_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            AW-HE130_2{{"AW-HE130_2 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            AW-HE130_3{{"AW-HE130_3 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            BRC-H800_0{{"BRC-H800_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_1
            BRC-H800_1{{"BRC-H800_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_2
            end
            subgraph Shoulder Camcorder
            PXW-500_0{{"PXW-500_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_2
            PXW-500_1{{"PXW-500_1 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_3
            PXW-500_2{{"PXW-500_2 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_4
            PXW-500_3{{"PXW-500_3 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_5
            end
            subgraph DSLR
            Alpha7Mark4_0{{"Alpha7Mark4_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|PassThru_3
            FX3_0{{"FX3_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|PassThru_3
            end
            subgraph Large Sensor
            Burano_0{{"Burano_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_5
            Burano_1{{"Burano_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_6
            end
            subgraph "Control Room" 
            CI0_0 --- |Ethernet|MiniCameraSwitch
            CI0_1 --- |Ethernet|MiniCameraSwitch
            CI0_2 --- |Ethernet|MiniCameraSwitch
            PassThru_1 --- |Ethernet|PTZSwitch
            RIO_1 --- |Ethernet|PTZSwitch
            RIO_2 --- |Ethernet|PTZSwitch
            RIO-Live_2 --- |Ethernet|ShoulderCamcorderSwitch
            RIO-Live_3 --- |Ethernet|ShoulderCamcorderSwitch
            RIO-Live_4 --- |Ethernet|ShoulderCamcorderSwitch
            RIO-Live_5 --- |Ethernet|ShoulderCamcorderSwitch
            PassThru_3 --- |Ethernet|DSLRSwitch
            RIO_5 --- |Ethernet|LargeSensorSwitch
            RIO_6 --- |Ethernet|LargeSensorSwitch
            MiniCameraSwitch --- |Ethernet|CY-RCP-OCTO_0
            PTZSwitch --- |Ethernet|CY-RCP-OCTO-J_0
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_1
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_2
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_3
            DSLRSwitch --- |Ethernet|CY-RCP-DUO-J_4
            DSLRSwitch --- |Ethernet|CY-RCP-DUO-J_5
            LargeSensorSwitch --- |Ethernet|CY-RCP-DUO-J_6
            LargeSensorSwitch --- |Ethernet|CY-RCP-DUO-J_7
            end            
            """
        self.mermaid_test_code =  """
graph RL
subgraph CineStyle
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
    V-Raptor_0<-->|IP-to-USB-C|RIO-LIVE_0
    TBD_V-Raptor_0<==>V-Raptor_0
    %%INF: No lens cable displayed
    subgraph V-Raptor_0_cameralens [NO Remote Control Request]
    TBD_V-Raptor_0@{ shape: stadium, label: TBD }
    V-Raptor_0@{ shape: hex, label: VRaptor0  }
    end
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
    V-Raptor_1<-->|IP-to-USB-C|RIO-LIVE_1
    TBD_V-Raptor_1<==>V-Raptor_1
    %%INF: No lens cable displayed
    subgraph V-Raptor_1_cameralens [NO Remote Control Request]
    TBD_V-Raptor_1@{ shape: stadium, label: TBD }
    V-Raptor_1@{ shape: hex, label: VRaptor1  }
    end
end
subgraph Mirrorless
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
    BGH1_0<-->|Ethernet-RJ45|RIO-LIVE_2
    TBD_BGH1_0<==>BGH1_0
    %%INF: No lens cable displayed
    subgraph BGH1_0_cameralens [NO Remote Control Request]
    TBD_BGH1_0@{ shape: stadium, label: TBD }
    BGH1_0@{ shape: hex, label: BGH10  }
    end
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
    BGH1_1<-->|Ethernet-RJ45|RIO-LIVE_3
    TBD_BGH1_1<==>BGH1_1
    %%INF: No lens cable displayed
    subgraph BGH1_1_cameralens [NO Remote Control Request]
    TBD_BGH1_1@{ shape: stadium, label: TBD }
    BGH1_1@{ shape: hex, label: BGH11  }
    end
end
subgraph Minicam
    %%DBG: CameraCategory.FIXED_LENS branch
    %% CameraCategory:Fixed Lens, LensControl:No Need, LensType:Manual
    CV225_0<-->|CY-CBL-6P-PFAN|RIO_0
    %%INF: No lens displayed
                        CV225_0@{ shape: hex, label: MarshallCV2250  }
        %%DBG: CameraCategory.FIXED_LENS branch
    %% CameraCategory:Fixed Lens, LensControl:No Need, LensType:Manual
    CV225_1<-->|CY-CBL-6P-PFAN|RIO_1
    %%INF: No lens displayed
                        CV225_1@{ shape: hex, label: MarshallCV2251  }
    end
subgraph Shoulder Camcorder
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Broadcast, LensControl:No Need, LensType:B4-Mount
    PXW-500_0<-->|CY-CBL-SONY-8P-03|CI0_0
    B4-Mount_PXW-500_0<==>PXW-500_0
    %%INF: No lens cable displayed
    subgraph PXW-500_0_cameralens [NO Remote Control Request]
    B4-Mount_PXW-500_0@{ shape: stadium, label: B4-Mount }
    PXW-500_0@{ shape: hex, label: PXW-X5000  }
    end
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Broadcast, LensControl:No Need, LensType:B4-Mount
    PXW-500_1<-->|CY-CBL-SONY-8P-03|CI0_0
    B4-Mount_PXW-500_1<==>PXW-500_1
    %%INF: No lens cable displayed
    subgraph PXW-500_1_cameralens [NO Remote Control Request]
    B4-Mount_PXW-500_1@{ shape: stadium, label: B4-Mount }
    PXW-500_1@{ shape: hex, label: PXW-X5001  }
    end
end
subgraph Slow Motion
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Broadcast, LensControl:No Need, LensType:B4-Mount
    AtomOneSSM500_0<-->|CY-CBL-6P-DCHIP-02|CI0_1
    B4-Mount_AtomOneSSM500_0<==>AtomOneSSM500_0
    %%INF: No lens cable displayed
    subgraph AtomOneSSM500_0_cameralens [NO Remote Control Request]
    B4-Mount_AtomOneSSM500_0@{ shape: stadium, label: B4-Mount }
    AtomOneSSM500_0@{ shape: hex, label: AtomOne SSM5000  }
    end
    %%DBG: NOT (CameraCategory.FIXED_LENS, CameraCategory.IZF_INTEGRATED) branch
    %% CameraCategory:Broadcast, LensControl:No Need, LensType:B4-Mount
    AtomOneSSM500B4_0<-->|CY-CBL-6P-DCHIP-02|CI0_1
    B4-Mount_AtomOneSSM500B4_0<==>AtomOneSSM500B4_0
    %%INF: No lens cable displayed
    subgraph AtomOneSSM500B4_0_cameralens [NO Remote Control Request]
    B4-Mount_AtomOneSSM500B4_0@{ shape: stadium, label: B4-Mount }
    AtomOneSSM500B4_0@{ shape: hex, label: AtomOne SSM500 B40  }
    end
end
subgraph "Control Room" 
RIO-LIVE_0 --- |LAN RF Halow|CineStyleSwitch
RIO-LIVE_1 --- |LAN RF Halow|CineStyleSwitch
RIO-LIVE_2 --- |LAN RF Halow|MirrorlessSwitch
RIO-LIVE_3 --- |LAN RF Halow|MirrorlessSwitch
RIO_0 --- |WAN 4G 5G|MinicamSwitch
RIO_1 --- |WAN 4G 5G|MinicamSwitch
CI0_0 --- |LAN Wired|ShoulderCamcorderSwitch
CI0_1 --- |LAN Wired|SlowMotionSwitch
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_0
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_1
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_2
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_3
MinicamSwitch --- |Ethernet|CY-RCP-DUO_0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_4
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_5
SlowMotionSwitch --- |Ethernet|CY-RCP-DUO_1
end
                """    
    def graph_mermaid(self,code):
        if code == None :
            mermaid_code = self.mermaid_test_code
        else:
            mermaid_code = code
        graph = Graph('example-flowchart',mermaid_code)
        mermaid_graph  = md.Mermaid(graph)
        return(mermaid_graph)
    def streamlit_mermaid(self,mermaid_graph):
        def render_svg(svg):
            b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
            html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
            return (html)
        svg_html = mermaid_graph._repr_html_()
        result = render_svg(svg_html) 
        return(result)
    def mermaidize(self,cyangear):
        mermaid_code = self.mermaid.code(cyangear)
        # Use Differ to compare
        differ = Differ()
        splitted_code      = mermaid_code.split()
        splitted_code_test = self.mermaid_test_code.split()
        difference = list(differ.compare(splitted_code, splitted_code_test))
        # Print the differences
        if mermaid_code == self.mermaid_test_code:
            logger.info("No difference")
        else:
            logger.info("Difference")
            logger.info(f"Length of generated = {len(mermaid_code)}; Length of expected = {len(self.mermaid_test_code)}")
            logger.info(f"Generated: {mermaid_code}")
            logger.info(f"Expected: {self.mermaid_test_code}")
        logger.info("\n".join(difference))
        # mermaid_graph=self.graph_mermaid(self.mermaid_test_code)
        mermaid_graph=self.graph_mermaid(mermaid_code)

        html = self.streamlit_mermaid(mermaid_graph)
        return(html)

