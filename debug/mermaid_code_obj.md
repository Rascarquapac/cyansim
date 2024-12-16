:::mermaid
graph RL
subgraph Minicam
CV225_0{{"MarshallCV2250"}}<-->|CY-CBL-6P-PFAN|RIO-LIVE_0
CV226_0{{"MarshallCV2260"}}<-->|CY-CBL-6P-PFAN|RIO-LIVE_0
CV226_1{{"MarshallCV2261"}}<-->|CY-CBL-6P-PFAN|RIO-LIVE_1
end
subgraph Shoulder Camcorder
PMW-EX3_0{{"PMW-EX3_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-LIVE_2
  subgraph PMW-EX3_0_cameralens [No lens control required]
    PMW-EX3_0
    B4-Mount_PMW-EX3_0
  end
PMW-EX3_1{{"PMW-EX3_1 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-LIVE_2
  subgraph PMW-EX3_1_cameralens [No lens control required]
    PMW-EX3_1
    B4-Mount_PMW-EX3_1
  end
PMW-EX3_2{{"PMW-EX3_2 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-LIVE_3
  subgraph PMW-EX3_2_cameralens [No lens control required]
    PMW-EX3_2
    B4-Mount_PMW-EX3_2
  end
end
subgraph TBD
PXW-200_0{{"PXW-200_0 fa:fa-camera-retro"}}---|Undefined|IP_0
  subgraph PXW-200_0_cameralens [No lens control required]
    PXW-200_0
    Manual_PXW-200_0
  end
end
subgraph "Control Room" 
RIO-LIVE_0 --- |Ethernet|MinicamSwitch
RIO-LIVE_1 --- |Ethernet|MinicamSwitch
RIO-LIVE_2 --- |Ethernet|ShoulderCamcorderSwitch
RIO-LIVE_3 --- |Ethernet|ShoulderCamcorderSwitch
IP_0 --- |Ethernet|TBDSwitch
MinicamSwitch --- |Ethernet|CY-RCP-QUATTRO_0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_1
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_2
TBDSwitch --- |Ethernet|CY-RCP-DUO_1
end

:::
