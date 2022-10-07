The goal here is to take a sample like so;

| Date | Product | Quantity | SellingPrice | Amount | Cost | Profit
| --- | --- | --- | --- | --- | --- | --- |
| 01/08/22 | widget1 | 5 | 500 | 2500 | 2000 | 500 |
| 01/08/22 | widget1 | 4 | 600 | 2400 | 1500 | 900 |
| 01/08/22 | widget2 | 3 | 200 | 600 | 700 | -100 |
| 02/08/22 | widget2 | 2 | 250 | 500 | 300 | 200 |
| 02/08/22 | widget1 | 4 | 600 | 1200 | 1200 | 0 |
| 02/08/22 | widget1 | 5 | 600 | 3000 | 2800 | 200 |

to create a printable format that presents each product
 sales by day.

Here i create two views, the first is the collasped view and by simply pivoting the data we
 have;
 | Date | Product | Quantity | Amount | Cost | Profit
| --- | --- | --- | --- | --- | --- |
| 01/08/22 | widget1 | 9 | 4900 | 3500 | 1400 |
| 01/08/22 | widget2 | 3 | 600 | 700 | -100 |
| 02/08/22 | widget1 | 9 | 4200 | 4000 | 200 |
| 02/08/22 | widget2 | 2 | 250 | 300 | 200 |

the second view is the expanded view like so;
| Date | Product | Quantity | SellingPrice | Amount | Cost | Profit
| --- | --- | --- | --- | --- | --- | --- |
| 01/08/22 | widget1 | 5 | 500 | 2500 | 2000 | 500 |
|  |  | 4 | 600 | 2400 | 1500 | 900 |
|  |  | **9** |  | **4900** | **3500** | **1400** |
|  | widget2 | 3 | 200 | 600 | 700 | -100 |
|  |  | **3** |  | **600** | **700** | **-100** |
| 02/08/22 | widget1 | 4 | 600 | 1200 | 1200 | 0 |
|  |  | 5 | 600 | 3000 | 2800 | 200 |
|  |  | **9** |  | **4200** | **4000** | **200** |
|  | widget2 | 2 | 250 | 500 | 300 | 200 |
|  |  | **2** |  | **500** | **300** | **200** |

and save to different excel sheets in the same workbook

