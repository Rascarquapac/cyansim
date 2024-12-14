:::mermaid
graph RL
subgraph Minicam
CV225_0{{"MarshallCV2250"}}<-->|CY-CBL-6P-PFAN|CI0_1
CV226_0{{"MarshallCV2260"}}<-->|CY-CBL-6P-PFAN|CI0_1
CV226_1{{"MarshallCV2261"}}<-->|CY-CBL-6P-PFAN|CI0_2
end
subgraph "Control Room" 
CI0_1 --- |Ethernet|MinicamSwitch
CI0_2 --- |Ethernet|MinicamSwitch
MinicamSwitch --- |Ethernet|CY-RCP-QUATTRO_0
end

:::
