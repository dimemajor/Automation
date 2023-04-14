Created this project for a client to map product from different e-comm stores to products in an erpsystem when seting up the erp. 

The g-spreadsheet has three columns;

1. The sku on the e-comm store
2. The internal reference (IR) in the Erp (another name for SKU). If the
	e-comm product is linked to multiple items in the erp, they would
	be seperated by "+" and if an item occurs multiple times, it 
	would be suffixed by (*n), n being the number of occurences. So, 
	123, 123*5, 123*2+456, are all valid. This column forms the bill 
	of materials for the first column.
3. A prefix to be used in the name of the product

Periodically the sheet is inspected for validity and the script is run. This creates new products in the erp with some predefined field values and the bill of materials of the e-commm products as defined by the IR column
are also created for the products.
