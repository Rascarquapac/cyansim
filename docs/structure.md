::: mermaid
graph TB
    subgraph CAMS
	subgraph CAMERA_TAB
		PATTERN[rank=1]
		BRAND[rank=1]
		TYPE[rank=1]
		SELECT[rank=1]
		matching
		MATCHED_df
		edit_cam
	PATTERN-->matching
	BRAND-->matching
	TYPE-->matching
	end
	subgraph CAMERA
		load[["load"]]
		GSHEET_gs[("Gsheet")]
		GSHEET_gs-->load
		load-->CATALOG_df
	CATALOG_df-->matching
	end
	end
	%% CAMERA
	matching-->MATCHED_df
	MATCHED_df-->edit_cam
	edit_cam--> SELECT
	SELECT-->edit_cam
	edit_cam-->POOL_df
	POOL_df-->display
	subgraph RESULT
		SELECTED
		display-->SELECTED
	end
	%% UI FIELDS
	SELECT["`#CAM SELECT`"]
	%% Methods
	matching[["matching"]]
	edit_cam[["edit"]]
	display[["display"]]
	analyze[["analyze"]]
	%% DATAFRAMES
	CATALOG_df[("Catalog")]
	MATCHED_df[("Matched")] 
	
    subgraph POOL
       POOL_df[("Pool")] 
	end
	POOL_df-->analyze
	analyze-->ROUTED_df
	ROUTED_df-->schematize
	schematize-->SCHEME
	subgraph NETWORK_TAB
		NETWORK_TYPE1
		NETWORK_TYPEn
		edit_net
	end
	edit_net-->NETWORK_TYPE1
	edit_net-->NETWORK_TYPEn
	NETWORK_TYPE1-->edit_net
	NETWORK_TYPEn-->edit_net
	POOL_df-->edit_net
	edit_net-->POOL_df
	%% Methods
	edit_net[["edit"]]
    %% DATAFRAME

	subgraph LENS_TAB
		LENS_TYPE1
		LENS_TYPEn
		edit_lens
	end
	POOL_df-->edit_lens
	edit_lens-->POOL_df
	edit_lens-->LENS_TYPE1
	edit_lens-->LENS_TYPEn
	LENS_TYPE1-->edit_lens
	LENS_TYPEn-->edit_lens
	edit_lens--> POOL_df
	%% Methods
	edit_lens[["edit"]]
    %% DATAFRAME
	subgraph SCHEME_TAB
		SCHEME
       	ROUTED_df[("Routed")] 
	   	analyze[["graph"]]
	   	schematize[["graph"]]
	end
%% Node@{ img: "https://i.imgur.com/ctZI7sm.png", h: 50, w: 100, pos: "b", constraint: "on"}

:::