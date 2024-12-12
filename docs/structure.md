::: mermaid
graph TB
	subgraph CAMERA_TAB
	    direction TB
		PATTERN
		BRAND
		TYPE
		SELECT
		SELECTED
	end
	%% CAMERA
	subgraph CAMERA
		GSHEET_gs-->load
		load-->CATALOG_df
		PATTERN-->matching
		BRAND-->matching
		TYPE-->matching
		CATALOG_df-->matching
		matching-->MATCHED_df
		MATCHED_df-->edit_cam
		edit_cam--> SELECT
		SELECT-->edit_cam
		edit_cam-->SELECTED_df
		SELECTED_df-->display
		display-->SELECTED
	end
	%% UI FIELDS
	SELECT["`#CAM SELECT`"]
	%% Methods
	load[["load"]]
	matching[["matching"]]
	edit_cam[["edit"]]
	display[["display"]]
	%% DATAFRAMES
	GSHEET_gs[("Gsheet")]
	CATALOG_df[("Catalog")]
	MATCHED_df[("Matched")] 
	SELECTED_df[("Selected")] 

	subgraph NETWORK_TAB
		NETWORK_TYPE1
		NETWORK_TYPEx
		NETWORK_TYPEn
		edit_net
	end
	SELECTED_df-->edit_net
	edit_net-->NETWORK_TYPE1
	edit_net-->NETWORK_TYPEx
	edit_net-->NETWORK_TYPEn
	NETWORK_TYPE1-->edit_net
	NETWORK_TYPEx-->edit_net
	NETWORK_TYPEn-->edit_net
	edit_net--> FINAL_df
	%% Methods
	edit_net[["edit"]]
    %% DATAFRAME
	FINAL_df[("Final")]

	subgraph LENS_TAB
		LENS_TYPE1
		LENS_TYPEx
		LENS_TYPEn
		edit_lens
	end
	FINAL_df-->edit_net
	edit_lens-->LENS_TYPE1
	edit_lens-->LENS_TYPEx
	edit_lens-->LENS_TYPEn
	LENS_TYPE1-->edit_lens
	LENS_TYPEx-->edit_lens
	LENS_TYPEn-->edit_lens
	edit_lens--> FINAL_df
	%% Methods
	edit_lens[["edit"]]
    %% DATAFRAME
	subgraph SCHEME_TAB
		SCHEME
	end
%% Node@{ img: "https://i.imgur.com/ctZI7sm.png", h: 50, w: 100, pos: "b", constraint: "on"}

:::