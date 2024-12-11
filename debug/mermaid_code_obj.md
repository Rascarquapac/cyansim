:::mermaid
graph RL
subgraph TBD
Arc360_0{{"Arc360_0 fa:fa-camera-retro"}}---|Undefined|IP_8
  subgraph Arc360_0_cameralens [No lens control required]
    Arc360_0
    Manual_Arc360_0
  end
end
subgraph Minicam Motorizable
AtomOne_0{{"AtomOne_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_81
  subgraph AtomOne_0_cameralens [No lens control required]
    AtomOne_0
    Manual_AtomOne_0
  end
AtomOne_1{{"AtomOne_1 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_81
  subgraph AtomOne_1_cameralens [No lens control required]
    AtomOne_1
    Manual_AtomOne_1
  end
end
subgraph Minicam
CV225_0{{"MarshallCV2250"}}<-->|CY-CBL-6P-PFAN|CI0_82
end
subgraph Mirrorless
Alpha_0{{"Alpha_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|IP_9
  subgraph Alpha_0_cameralens [No lens control required]
    Alpha_0
    E-Mount_Alpha_0
  end
end
subgraph Shoulder Camcorder
PXW-500_0{{"PXW-500_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|CI0_83
  subgraph PXW-500_0_cameralens [No lens control required]
    PXW-500_0
    B4-Mount_PXW-500_0
  end
end
subgraph "Control Room" 
IP_8 --- |Ethernet|TBDSwitch
CI0_81 --- |Ethernet|MinicamMotorizableSwitch
CI0_82 --- |Ethernet|MinicamSwitch
IP_9 --- |Ethernet|MirrorlessSwitch
CI0_83 --- |Ethernet|ShoulderCamcorderSwitch
TBDSwitch --- |Ethernet|CY-RCP-DUO_0
MinicamMotorizableSwitch --- |Ethernet|CY-RCP-DUO_1
MinicamSwitch --- |Ethernet|CY-RCP-DUO_2
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_1
end

:::
