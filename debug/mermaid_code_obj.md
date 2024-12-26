:::mermaid
graph RL
subgraph Shoulder Camcorder
%% CameraCategory:Broadcast, LensControl:No Need, LensType:B4-Mount
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
B4-Mount_PXW-500_0[[B4-Mount]]<-->PXW-500_0
PXW-500_0{{"PXW-500_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|CI0_0
  subgraph PXW-500_0_cameralens [No lens control required]
    PXW-500_0
    B4-Mount_PXW-500_0[[B4-Mount]]
  end
%% CameraCategory:Broadcast, LensControl:No Need, LensType:B4-Mount
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
B4-Mount_PXW-500_1[[B4-Mount]]<-->PXW-500_1
PXW-500_1{{"PXW-500_1 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|CI0_0
  subgraph PXW-500_1_cameralens [No lens control required]
    PXW-500_1
    B4-Mount_PXW-500_1[[B4-Mount]]
  end
end
subgraph CineStyle
%% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
TBD_V-Raptor_0[[TBD]]<-->V-Raptor_0
V-Raptor_0{{"V-Raptor_0 fa:fa-camera-retro"}}---|IP-to-USB-C|RIO-LIVE_0
  subgraph V-Raptor_0_cameralens [No lens control required]
    V-Raptor_0
    TBD_V-Raptor_0[[TBD]]
  end
end
subgraph Mirrorless
%% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
TBD_BGH1_0[[TBD]]<-->BGH1_0
BGH1_0{{"BGH1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO-LIVE_1
  subgraph BGH1_0_cameralens [No lens control required]
    BGH1_0
    TBD_BGH1_0[[TBD]]
  end
end
subgraph Minicam
%% CameraCategory:Fixed Lens, LensControl:No Need, LensType:Manual
%%DBG: CC.FIXED_LENS branch
CV225_0{{"MarshallCV2250"}}<-->|CY-CBL-6P-PFAN|RIO-LIVE_2
%% CameraCategory:Fixed Lens, LensControl:No Need, LensType:Manual
%%DBG: CC.FIXED_LENS branch
CV225_1{{"MarshallCV2251"}}<-->|CY-CBL-6P-PFAN|RIO-LIVE_2
end
subgraph "Control Room" 
CI0_0 --- |LAN Wired|ShoulderCamcorderSwitch
RIO-LIVE_0 --- |LAN RF Halow|CineStyleSwitch
RIO-LIVE_1 --- |LAN RF Halow|MirrorlessSwitch
RIO-LIVE_2 --- |LAN RF Halow|MinicamSwitch
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_1
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_2
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_3
MinicamSwitch --- |Ethernet|CY-RCP-DUO_0
end

:::
