[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared Raw_DataAdventureWorks_Product_Categories = let
  Source = Lakehouse.Contents([HierarchicalNavigation = null, EnableVorder = true, OutputMetadataRefresh = true]),
  #"Navigation 1" = Source{[workspaceId = "2ff589e8-6b79-4bdf-ba88-1f2d730b59a9"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "48e0a0e6-d4a3-4b3e-a5e3-7ccaffa0d1e2"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "Files", ItemKind = "Folder"]}[Data],
  #"Navigation 4" = #"Navigation 3"{[Name = "Raw_DataAdventureWorks_Product_Categories"]}[Content],
  Navigation = #"Navigation 4"{[Name = "AdventureWorks_Product_Categories.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 2, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"ProductCategoryKey", Int64.Type}, {"CategoryName", type text}}),
  #"Uppercased text" = Table.TransformColumns(#"Changed column type", {{"CategoryName", each Text.Upper(_), type nullable text}}),
  #"Removed duplicates" = Table.Distinct(#"Uppercased text", {"ProductCategoryKey"})
in
  #"Removed duplicates";
[BindToDefaultDestination = true]
shared Raw_DataProduct_Subcategories = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "2ff589e8-6b79-4bdf-ba88-1f2d730b59a9"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "48e0a0e6-d4a3-4b3e-a5e3-7ccaffa0d1e2"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "Files", ItemKind = "Folder"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Name = "Raw_DataProduct_Subcategories"]}[Content],
  #"Navigation 4" = #"Navigation 3"{[Name = "AdventureWorks_Product_Subcategories.csv"]}[Content],
  #"Imported CSV" = Csv.Document(#"Navigation 4", [Delimiter = ",", Columns = 3, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"ProductSubcategoryKey", Int64.Type}, {"SubcategoryName", type text}, {"ProductCategoryKey", Int64.Type}}),
  #"Removed blank rows" = Table.SelectRows(#"Changed column type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
  #"Uppercased text" = Table.TransformColumns(#"Removed blank rows", {{"SubcategoryName", each Text.Upper(_), type nullable text}}),
  #"Removed duplicates" = Table.Distinct(#"Uppercased text", {"ProductSubcategoryKey"})
in
  #"Removed duplicates";
[BindToDefaultDestination = true]
shared Merge = let
  Source = Table.NestedJoin(Raw_DataProduct_Subcategories, {"ProductCategoryKey"}, Raw_DataAdventureWorks_Product_Categories, {"ProductCategoryKey"}, "Raw_DataAdventureWorks_Product_Categories", JoinKind.LeftOuter),
  #"Expanded Raw_DataAdventureWorks_Product_Categories" = Table.ExpandTableColumn(Source, "Raw_DataAdventureWorks_Product_Categories", {"ProductCategoryKey", "CategoryName"}, {"ProductCategoryKey.1", "CategoryName"}),
  #"Inserted conditional column" = Table.AddColumn(#"Expanded Raw_DataAdventureWorks_Product_Categories", "CustomFlag", each if [ProductCategoryKey] = 1 then "One" else if [ProductCategoryKey] = 2 then "Two" else if [ProductCategoryKey] = 3 then "Three" else "Four")
in
  #"Inserted conditional column";
shared DefaultDestination = let
  Source = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  #"Navigation 1" = Source{[workspaceId = "2ff589e8-6b79-4bdf-ba88-1f2d730b59a9"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "48e0a0e6-d4a3-4b3e-a5e3-7ccaffa0d1e2"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "dbo", ItemKind = "Schema"]}[Data]
in
  #"Navigation 3";
