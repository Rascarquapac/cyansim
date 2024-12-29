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
