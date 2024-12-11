::: mermaid
graph TD
subgraph CYANSIM_UI
	subgraph CAMERA_TAB
		Pattern
		Brand
		Type
		Selection
		Selected
	end
	subgraph NETWORK_TAB
		Network
	end
	subgraph LENS_TAB
		Lens
	end
	subgraph SCHEME_TAB
		Scheme
	end
end
subgraph VIEW
end
Node@{ img: "https://i.imgur.com/ctZI7sm.png", h: 50, w: 100, pos: "b", constraint: "on"}
Pattern-->Filter
Brand-->Filter
Type-->Filter
Catalog-->Filter
Filter-->Selected
Gsheet-->Load
Load-->Catalog
Selected-->Update
Update-->Catalog
Catalog-->Display
Display-->Selection
Display[["display"]]
Update[["update"]]
Gsheet[("Gsheet")]
Catalog[("Catalog")] 
Pool[("Pool")]
Filter[["filter"]]
Selected["`#cam select`"]
Load[["load"]]
:::