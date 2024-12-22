import base64
import mermaid as md
import pandas as pd
from mermaid.graph  import Graph
from draw_mermaid import Mermaid
#################### DRAW WITH MERMAID ###########################
class Draw():
    def __init__(self) -> None:
        self.df      = pd.DataFrame()
        self.mermaid = Mermaid()
        self.obj = {}
        pass
    def graph_mermaid(self,code):
        if code == None :
            mermaid_code = """
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
        mermaid_graph=self.graph_mermaid(mermaid_code)
        html = self.streamlit_mermaid(mermaid_graph)
        return(html)

