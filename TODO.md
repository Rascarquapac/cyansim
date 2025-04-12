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
## Developments
- validation of descriptor values
- adding specific values for a camera different from camera x protocol (PMW-EX3)
- licence specific to camera (SSM500)
- abstract edit method with groups/blocks:
	- init values for columns of each_group : 
		- {'groupname':{'colname': value},{}} 
	- options list for each group: 
		- {'groupname':{'colname': [options_list],{}}}
## Improvement
- intelligent update of pool: when changing camera selection update only variation of camera number, clean id camera number is 0
- add network structure
