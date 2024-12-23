:::mermaid
graph RL
subgraph Shoulder Camcorder
%% CameraCategory:Broadcast, LensControl:No Need, LensType:B4-Mount
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
B4-Mount_PMW-EX3_0[[B4-Mount]]<-->PMW-EX3_0
PMW-EX3_0{{"PMW-EX3_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-LIVE_0
  subgraph PMW-EX3_0_cameralens [No lens control required]
    PMW-EX3_0
    B4-Mount_PMW-EX3_0[[B4-Mount]]
  end
end
subgraph Mirrorless
%% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
TBD_Alpha_0[[TBD]]<-->Alpha_0
Alpha_0{{"Alpha_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|RIO-LIVE_1
  subgraph Alpha_0_cameralens [No lens control required]
    Alpha_0
    TBD_Alpha_0[[TBD]]
  end
%% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
TBD_Alpha_1[[TBD]]<-->Alpha_1
Alpha_1{{"Alpha_1 fa:fa-camera-retro"}}---|USB-A-to-USB-C|RIO-LIVE_1
  subgraph Alpha_1_cameralens [No lens control required]
    Alpha_1
    TBD_Alpha_1[[TBD]]
  end
%% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
TBD_Alpha7CR_0[[TBD]]<-->Alpha7CR_0
Alpha7CR_0{{"Alpha7CR_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|RIO-LIVE_2
  subgraph Alpha7CR_0_cameralens [No lens control required]
    Alpha7CR_0
    TBD_Alpha7CR_0[[TBD]]
  end
%% CameraCategory:Cine Interchangeable, LensControl:No Need, LensType:TBD
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
TBD_Alpha7CR_1[[TBD]]<-->Alpha7CR_1
Alpha7CR_1{{"Alpha7CR_1 fa:fa-camera-retro"}}---|USB-A-to-USB-C|RIO-LIVE_2
  subgraph Alpha7CR_1_cameralens [No lens control required]
    Alpha7CR_1
    TBD_Alpha7CR_1[[TBD]]
  end
end
subgraph Minicam Motorizable
%% CameraCategory:Minicam Motorizable Lens, LensControl:No Need, LensType:Manual
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
Manual_AtomOne_0[[Manual]]<-->AtomOne_0
AtomOne_0{{"AtomOne_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-03|CI0_0
  subgraph AtomOne_0_cameralens [No lens control required]
    AtomOne_0
    Manual_AtomOne_0[[Manual]]
  end
%% CameraCategory:Minicam Motorizable Lens, LensControl:No Need, LensType:Manual
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
Manual_AtomOne_1[[Manual]]<-->AtomOne_1
AtomOne_1{{"AtomOne_1 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-03|CI0_0
  subgraph AtomOne_1_cameralens [No lens control required]
    AtomOne_1
    Manual_AtomOne_1[[Manual]]
  end
%% CameraCategory:Minicam Motorizable Lens, LensControl:No Need, LensType:Manual
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
Manual_AtomOne_2[[Manual]]<-->AtomOne_2
AtomOne_2{{"AtomOne_2 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-03|CI0_1
  subgraph AtomOne_2_cameralens [No lens control required]
    AtomOne_2
    Manual_AtomOne_2[[Manual]]
  end
%% CameraCategory:Minicam Motorizable Lens, LensControl:No Need, LensType:Manual
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
Manual_AtomOnemini_0[[Manual]]<-->AtomOnemini_0
AtomOnemini_0{{"AtomOnemini_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-03|CI0_1
  subgraph AtomOnemini_0_cameralens [No lens control required]
    AtomOnemini_0
    Manual_AtomOnemini_0[[Manual]]
  end
%% CameraCategory:Minicam Motorizable Lens, LensControl:No Need, LensType:Manual
%%DBG: NOT (CC.FIXED_LENS, CC.IZF_INTEGRATED) branch
Manual_AtomOnemini_1[[Manual]]<-->AtomOnemini_1
AtomOnemini_1{{"AtomOnemini_1 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-03|CI0_2
  subgraph AtomOnemini_1_cameralens [No lens control required]
    AtomOnemini_1
    Manual_AtomOnemini_1[[Manual]]
  end
end
subgraph "Control Room" 
RIO-LIVE_0 --- |LAN RF Halow|ShoulderCamcorderSwitch
RIO-LIVE_1 --- |LAN RF Halow|MirrorlessSwitch
RIO-LIVE_2 --- |LAN RF Halow|MirrorlessSwitch
CI0_0 --- |LAN Wired|MinicamMotorizableSwitch
CI0_1 --- |LAN Wired|MinicamMotorizableSwitch
CI0_2 --- |LAN Wired|MinicamMotorizableSwitch
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_1
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_2
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_3
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_4
MinicamMotorizableSwitch --- |Ethernet|CY-RCP-OCTO_0
end

:::
