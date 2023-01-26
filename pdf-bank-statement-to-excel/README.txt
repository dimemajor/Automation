Convert Bank Statements with this program

I attempted to build an all-in-one solution but ended 
up settling for something that can be very versatile but 
is probably not perfect for all parties. 
I have tested on the current format of the bank statements following Nigerian 
banks and it works just fine without leaving out any row data;
- Gtbank
- Access Bank
- Zenith Bank
- Eco Bank
There is a good chance it will work for other banks so you can give it a try
if yours is not listed. Make sure you test the excel file however with step 4
of the next section

                 ---How to use---
1. Create a virtual environment and install the dependencies with this;
    pip install pandas glob2 pdfplumber openpyxl
2. Put the pdfs in the root working directory
3. Run the program. The excel files should
    popup in the root working directory.
4. To test that all the data was captured;
    - check and remove empty rows if any
    - create two new columns "calculated balances" and "difference"
    - copy and paste into the first row of the new column,
        the first row of the "balance" column from the original table
    - on the second row of the "calculated balance" column, enter the 
        formula that calculates for the original "balance" in that row.
        The "calculated balance" and "balance" should match. In other 
        words, the formula is the previous balance (on the "calculated balance" column)
        minus "debit" (on the same row) plus "credit" (also on the same row)
    - duplicate that formula down the "calculated balance" column to
        get their respective figures
    - the "difference" column should be "calculated balance" - "balance"
        and they should all be zero. If some values are not zero(to the nearest 5 or 
        6 decimal places) then a row was probably skipped. Check the pdf and move the 
        record manually

reach me at tonyatsevah@gmail.com for inquiries or customization. Thanks and enjoy.
    