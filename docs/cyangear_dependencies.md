::: mermaid
flowchart LR
CAMERA_PROPERTIES-->CAMERA_CATEGORY
CAMERA_CATEGORY-->CAMERA_LENS_OBJECT
USER_NEEDS_IZT-->CAMERA_LENS_OBJECT
USER_NEEDS_LENS_TYPE-->CAMERA_LENS_OBJECT
USER_NEEDS_MOTOR_TYPE-->CAMERA_LENS_OBJECT
CAMERA_LENS_OBJECT-->LENS_CABLE
CAMERA_LENS_OBJECT-->MOTOR_CABLE
CAMERA_LENS_OBJECT-->MOTOR
CAMERA_PROPERTIES-->CAMERA_CABLE
USER_NEEDS_CAMERA-->CAMERA_CABLE
CAMERA_SUPPORT_PAGE-->CAMERA_PROTOCOL
CAMERA_LINK-->CAMERA_PROTOCOL
CAMERA_PROTOCOL-->CAMERA_PROPERTIES
CAMERA_DB-->CAMERA_PROPERTIES
CAMERA_LENS_OBJECT-->CYANGLUE_OBJECT
USER_NEEDS_IP_MEDIUM-->IP_MEDIUM_OBJECT
IP_MEDIUM_OBJECT-->CYANGLUE_OBJECT
CYANGLUE_OBJECT-->CYANRCP_OBJECT
CYANRCP_OBJECT-->CYANRCP
subgraph PICKLE
CAMERA_DB
CAMERA_PROPERTIES
CAMERA_LINK
CAMERA_PROTOCOL
CAMERA_SUPPORT_PAGE
end
subgraph POOL
USER_NEEDS_IP_MEDIUM
IP_MEDIUM_OBJECT
end
subgraph POOL
USER_NEEDS_CAMERA
CAMERA_CABLE
end
subgraph CAMERA_LENS
CAMERA_CATEGORY
USER_NEEDS_IZT
USER_NEEDS_LENS_TYPE
USER_NEEDS_MOTOR_TYPE
CAMERA_LENS_OBJECT
LENS_CABLE
MOTOR_CABLE
MOTOR
end
PICKLE-->POOL
POOL-->CAMERA_LENS
CAMERA_LENS-->CYANGLUE_OBJECT

:::