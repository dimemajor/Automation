import os

import pandas as pd
import openpyxl
from openpyxl.styles import Font, colors
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import numbers

os.chdir('sales-report/')

spot = [] # row numbers that tell excel where to apply formatting. More later...

df = pd.read_excel('sales.xls')

unq_dt = df['Date'].unique() #get all dates
df=df.sort_values(['Date', 'Product'])

# for each date..
for i in range(len(unq_dt)):
    temp_spot = []
    day_spot = []

    time = str(unq_dt[i])
    time=time.split('T') #seperate day from time

    temp_df = df.loc[df['Date'].dt.strftime('%Y-%m-%d') == time[0]].copy() # filter df by previous day gotten and save to new df
    unq_descp = temp_df['Product'].unique() 

    # coll_df is created for the purpose of showing a collapsed view of the sales
    coll_df = temp_df.groupby('Product').sum()
    coll_df['Date'] = unq_dt[i]
    coll_df['Date'] = coll_df['Date'].dt.date
    coll_df=coll_df.drop(columns=["Selling Price"]) # selling price column does not make sense in this df

    # for each unique product in each day... 
    counter = 0
    for j in unq_descp:
        t_df = temp_df.loc[temp_df['Product'].str.contains(j)].copy() # filtering by the unique values and saving to another temporary(reusable) df
        t_df['Date'] = t_df['Date'].dt.date

        # removing redundant values. One is enough...
        if counter == 0:
            t_df.loc[t_df['Product'].duplicated(), ['Date', 'Product']] = ''
        else:
            t_df.loc[t_df['Product'].duplicated(), ['Product']] = ''
            t_df['Date'] = ''

        
        t_df.loc['Total'] = t_df.sum(numeric_only=True, axis=0)
        t_df.loc['Total','Selling Price'] = '' # once again, sum of unit selling price does not make sense.
        
        # get appropriate "spot(s)" to apply excel formatting
        '''spots are just numbers that tell excel what row to apply
        formatting to. In this case, its any row that has the total 
        values so it distinguishable from other data since "total" won't 
        be written in any column. It is neater this way imo.
        '''
        # concat dfs of each product per day
        if counter == 0:
            d2 = t_df
            day_spot.append(t_df.shape[0])
            temp_spot.append(t_df.shape[0])# add the spots from the product just looped through
        else:
            d2 = pd.concat([d2,t_df], axis=0)
            day_spot.append(d2.shape[0]) # since this is not the first iteration, the length of the previous dfs are to be taken into consideration in relation to where the next spot should be
            temp_spot.append(t_df.shape[0])
        counter+=1
    
    #concat dfs of each day
    if i == 0:
        expanded_df = d2
        summ_df = coll_df
        spot.extend(day_spot) # add the spots list from the day just looped through
    else:
        expanded_df = pd.concat([expanded_df,d2], axis=0)
        summ_df = pd.concat([summ_df,coll_df], axis=0)

        [spot.append(spot[len(spot)-1] + num) for num in temp_spot] # again, since this is not the first iteration, the length of the previous dfs are to be taken into consideration in relation to where the next spot should be


expanded_df = expanded_df.set_index('Date', 'Product')
summ_df = summ_df.reset_index().set_index('Date', 'Product')

#writing to excel
with pd.ExcelWriter("transformed.xlsx", engine="openpyxl") as writer:
    startrow, startcol = 0, 0

    summ_df.to_excel(writer, 'Collapsed',
                         startcol=startcol, startrow=startrow)
    expanded_df.to_excel(writer, 'Expanded',
                         startcol=startcol, startrow=startrow)


    sheet = writer.sheets['Expanded']
    font_format = Font(bold=True, size=12)
    thick = Side(border_style="thick")
    style = Border(top=thick, bottom=thick)
    
    nrows, ncols = expanded_df.shape
    for row in range(nrows):
        if row+1 not in spot: # +1 because 0 not important
            for col in range(ncols):
                cell = sheet.cell(row=row + 2, column=col + 2) # +2 because 0 not important and first row is for title
                cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
        else:
            for col in range(ncols):
                cell = sheet.cell(row=row + 2, column=col + 2)
                cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
                cell.font = font_format
                cell.border = style 

os.startfile('transformed.xlsx')




