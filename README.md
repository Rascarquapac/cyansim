# Evaluate Cyanview ressources base on use-case description
A sample Streamlit application do determine Cyanview resources required by a givien use-case.

The purpose is to provide the candidate buyers (resellers, integrators, final users) with information so that
- he can select the extra cyaniew devices (RIO/CI0/None), cables, tally, power supply related to his use-case with reasons why to select it
- he knows about the level of performance of the cameras of its use-case
- remarks

# Description  of "Camera Descriptor" Spreadsheet
## Camera Sheet
Fields describing properties of the camera allowing to select the required accessories for data link, power supply and any recommendations related to the use of the camera.
- Model : Display name of the camera
- Reference :	Unique reference id of the camera
- Protocol : Protocol id refering to the software part (driver) and cables managing the camera control as well as performances of the camera. It hsould be unique for the tuple ()
- Brand : 
- CameraLensControl	
- LensMount	
- cameraType
- ManufacturerURL
- Remark	
- TallyOptions																		
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