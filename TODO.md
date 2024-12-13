## Developments
- debug / record / upload/ pool for starting from predefined setups or building predefined setup
- correct instance number for devices
- correct camera name for schema
- abstract edit method with groups/blocks:
	- init values for columns of each_group : 
		- {'groupname':{'colname': value},{}} 
	- options list for each group: 
		- {'groupname':{'colname': [options_list],{}}}
## Improvement
- intelligent update of pool: when changing camera selection update only variation of camera number, clean id camera number is 0
- add network structure
