:::mermaid
graph RL
subgraph Minicam
CV225_0{{"CV225_0 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_0
  subgraph CV225_0_cameralens [No lens control required]
    CV225_0
    Manual_CV225_0
  end
CV225_1{{"CV225_1 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_0
  subgraph CV225_1_cameralens [No lens control required]
    CV225_1
    Manual_CV225_1
  end
CV226_0{{"CV226_0 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_1
  subgraph CV226_0_cameralens [No lens control required]
    CV226_0
    Manual_CV226_0
  end
CV226_1{{"CV226_1 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_1
  subgraph CV226_1_cameralens [No lens control required]
    CV226_1
    Manual_CV226_1
  end
end
subgraph "Control Room" 
CI0_0 --- |Ethernet|MinicamSwitch
CI0_1 --- |Ethernet|MinicamSwitch
MinicamSwitch --- |Ethernet|CY-RCP-QUATTRO_0
end

:::
