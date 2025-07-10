# Evaluate Cyanview ressources based on use-case description
A sample Streamlit application do determine Cyanview resources required by a givien use-case.

The purpose is to provide the candidate buyers (resellers, integrators, final users) with information so that he can quickly describe a use-case by providing the equipment he plans to use
- the cameras models
- the lenses for these cameras
- the medium networks 
From this description the user will get 
- a schema of the use-case
- a Json description of the use case
- the Cyanview devices (RIO/CI0), cables, tally, power supply related to his use-case and explanation on selection
- the level of performance of the cameras of its use-case
- recommendations,and potential issues of its use-case (UF,…)
## Dataflow
- descriptor.py : creates a dataframe containing cameras properties for each camera by taking camera descriptions from  
  - "Cyanview descriptor" gsheet ("Camera" sheet and CameraProtocol" sheet)
  - or from the equivalent pickle file for faster use, when no update of the   "Cyanview descriptor" gsheet
- user_interface.py: module related to the user inferface used for describing a use-case (selection of cameras, lenses, network medium, tally) 
  - Modules: 
    - Options class: creates the default values and default options for the user interface. 
        - Lenses: the ux will require the user to provide lens properties (proposing a list of lenses should be nice but currently unreachabe due to the number of existing lenses and adapters). Setting values for these properties will provide full information for the devices and cables required
        - the properties are
            - lensControl i.e. what you need to control IZF
            - lensType i.e. the internal capacity of the lens
            - lensMotor: choice, if any, of the lens motors
        - depending on the cameraLensCategory (a grouping of the cameras type according to the potential usable lenses), the lens user interface will propose 
            - a default value for these parameters 
            - options values in a selection list
        - Network medium: the type of network for telemetry data
        - A defautl value will be proposed
        - A selection list will be proposed from existing alternatives
    - ViewCamera class: selection of camera based on a substring, on the brand or on the type of camera
    - ViewLens class: selection of lens properties
    - ViewNetwork class: selection of telemetry network
    - Sidebar: sidebar display
  - Output : 
    - a dataframe with properties for each camera choosen
    - a JSON file describing the setup. In check mode the JSON file can be replace the user selection in order to test independently the "Cyanview equipment induction"

- gear_xxx: inducing Cyanview equipment according to use-case and Cyanview
- draw_xxx: drawing of the use case equipped with Cyanview gear
## Input data
- The simulator can use Cyanview device description from either a Google Gsheet or a pickle file. The choic is set by the "gsheet" variable in the secrets.toml file (.streamlit folder)
- The simulator can be set with a predefined use case. The choice is set by the "case_init" variable in the secrets.toml file . The json file with the setup description is defined in simulator.py. The final setup description is always stored in the json file defined in simulator.py (…TODO: split input and output json file…)
## Description  of "Camera Descriptor" Spreadsheet
### Camera Sheet
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
### Mermaid
- Display result with Mermaid
  - Check [this solution](https://discuss.streamlit.io/t/st-markdown-does-not-render-mermaid-graphs/25576/4)
### SSL Certificates:
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