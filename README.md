# Evaluate Cyanview ressources base on use-case description
A sample Streamlit application do determine Cyanview resources required by a givien use-case.

# TODO
## CYANVIEW DATA DESCRIPTION
###  Improve camera database:
- add a field for "Control Level" (for Broadcast ? Cinematic ?, General ?)
- add field on maxDelaySystainable for decinding about network
- fill missing protocol
### Improve generic explanation on choices and special attention
- create a FAQs pages on Odoo (bifirectionality, HF,)
### Improve UI
- Table of current selection: replace cable column by cameratype
### Develop Network selection
- add right network list
### Develop Lens selection
### Develop Extra-Devices (Tally, GPIO, NIO,…) selection
### Develop Non-Camera-Device-Control (switchers,…)
### Develop storing in database and emailing for quote request
### Manage target application (Specialty, Broadcast, Cinematic,Remote Production)
### Details:
- SSM500 should require a RCP-Full ( 1 x camera ?)
- Downloading SVG file
- Analyze and display schematic on any change
## FAQ
- Delay in camera process control
- RIO vs CI0
- RIO, RIO-Live and CI0 Pro & Cons
  - according to network
  - flexibility
  - power supply
- Delay with 
## MERMAID
- Display result with Mermaid
  - Check [this solution](https://discuss.streamlit.io/t/st-markdown-does-not-render-mermaid-graphs/25576/4)
## CODE
## SSL Certificates:
/Applications/Python\ 3.12/Install\ Certificates.command
## FLOWCHART
:::mermaid
flowchart TD
    CYAN(    Cyan User  ) --> TEXT
    CYAN --> GSHEET
    subgraph picklize
        TEXT[messages.md] -->|picklize.py| PKLMESS[messages.pkl]
        GSHEET[Cyanview Description.gs] -->|picklize.py| PKLCAMS[cameras.pkl]
        GSHEET[Cyanview Description.gs] -->|picklize.py| PKLPROP[properties.pkl]
    end
    PKLMESS -->|usecase_analyzemessages.py| MESSDIC(messages.dic)
    PKLCAMS --> |pool.py|POOLDF(pool.df)
    PKLPROP --> |pool.py|POOLDF(pool.df)
    subgraph salesagent
        MESSDIC --> |usecase_analyze|COMMENTANALYZE
        POOLDF --> |streamUI.py|POOLDF
        POOLDF-->|usecase.py|USECASEDF(usecase.df)
        USECASEDF--> |streamUI.py|USECASEDF
        USECASEDF -->|usecase_analyze| GRAPH(Mermaid)
        USECASEDF -->|usecase_analyze| COMMENTANALYZE(Analysis Messages)
    end
:::