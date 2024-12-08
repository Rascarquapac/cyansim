:::mermaid
graph RL
subgraph Minicam
CV225_0{{"MarshallCV2250"}}<-->|CY-CBL-6P-PFAN|CI0_19
CV225_1{{"MarshallCV2251"}}<-->|CY-CBL-6P-PFAN|CI0_19
CV226_0{{"MarshallCV2260"}}<-->|CY-CBL-6P-PFAN|CI0_20
CV226_1{{"MarshallCV2261"}}<-->|CY-CBL-6P-PFAN|CI0_20
CV345_0{{"MarshallCV3450"}}<-->|CY-CBL-6P-MARS-02|CI0_21
CV345_1{{"MarshallCV3451"}}<-->|CY-CBL-6P-MARS-02|CI0_21
end
subgraph "Control Room" 
CI0_19 --- |Ethernet|MinicamSwitch
CI0_20 --- |Ethernet|MinicamSwitch
CI0_21 --- |Ethernet|MinicamSwitch
MinicamSwitch --- |Ethernet|CY-RCP-OCTO_0
end

:::
