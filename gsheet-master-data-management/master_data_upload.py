from xmlrpc import client
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# DB, PWD, EMAIL, URL, SPREADSHEET_ID, SERVICE_ACCOUNT_FILE are all defined in constants.py
from constants import *


def _get_occurencies(ir):
    if '*' in ir:
        ir = ir.split('*')
        return (ir[0], ir[1], 'set')
    else:
        return (ir, '1', 'single')        

def get_components(self, ir):
    bom=[]
    ir = ir.replace(' ', '')
    if '+' in ir:
        irs = ir.split('+')
        for ir in irs:
            bom.append(self._get_occurencies(ir))
    else:
        bom.append(self._get_occurencies(ir))
    if all(item[2] == 'single' for item in bom) and len(bom)<=1:
        return (bom, 'single')
    else:
        return (bom, 'set')

def create_products_from_gsheet():
    '''
    gsheet contains 3 columns. 
    1. The product SKU on the e-comm store, 
    2. The corresponding internal reference(IR) in Odoo (if it is linked to multiple items it would be 
    seperated by "+" and if an item occurs a number of times, "*2" would be suffixed to the IR), 
    3. The prefix to be added to the name in Odoo when it is created.

    The aim is to create the products with the SKU as the Odoo IR with some other predefined fields selected
    and create the BOMs of the newly created products as stated by the second columns
    '''
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='All',
        ).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        exit()

    data=[]
    all_skus=[]
    sku_dict={}
    for i, row in enumerate(values):
        if i>0: #skip header
            bom = get_components(row[1])
            sku = row[0].strip()
            prefix = row[2].strip()
            all_skus.append(row[0])
            [all_skus.append(item[0]) for item in bom[0]]
            sku_dict[sku] = (bom[0], prefix, bom[1])

    srv = URL
    api = client.ServerProxy('%s/xmlrpc/2/object' % srv)
    db, user, password = DB, EMAIL, PWD
    common = client.ServerProxy("%s/xmlrpc/2/common" % srv)
    uid = common.authenticate(db, user, password, {})

    domain = [('default_code', 'in', all_skus)]
    recs = api.execute_kw(db, uid, password, "product.product", "search_read",[domain, ['id', 'name', 'default_code']])
    recs_dict = {rec['default_code']: (rec['name'], rec['id']) for rec in recs}


    vals=[]
    for key, value in sku_dict.items():
        rec={}
        '''
        check that the sku does not yet exist and all the components of the BOMs 
        exist. If not, the record will just be ignored to avoid errors
        '''
        if key not in recs_dict and all(bom[0] in recs_dict for bom in value[0]):
            '''
            If we are dealing with a single BOM component, then we'll reuse the 
            name of the component to construct a new name. Otherwise, we'll just 
            use a generic set name and make it a consumable product with a kit BOM
            '''
            if value[2]=='single':
                rec['name'] = f'{value[1]}-{recs_dict[value[0][0][0]][0]}'
                rec['detailed_type'] = 'product'
            elif value[2]=='set':
                rec['name'] = f'{value[1]}-Set-{key}'
                rec['detailed_type'] = 'consu'
            rec['sale_ok'] = True
            rec['purchase_ok'] = False
            rec['available_in_pos'] = False
            rec['default_code'] = key
            vals.append(rec)
    if vals:
        new_recs = api.execute_kw(db, uid, password, "product.template", "create", [vals])
        new_recs = api.execute_kw(db, uid, password, "product.template", "read",[new_recs, ['id', 'default_code']])
    vals=[]
    for rec in new_recs:
        data={}
        data['bom_line_ids']=[]
        data['product_tmpl_id'] = rec['id']

        components = sku_dict[rec['default_code']][0]
        for item in components:
            data['bom_line_ids'].append((0, 0, {'product_id': recs_dict[item[0]][1], 'product_qty':item[1]}))
        data['product_qty'] = '1'
        if sku_dict[rec['default_code']][2] == 'single':
            data['type'] = 'normal'
        elif sku_dict[rec['default_code']][2] == 'set':
            data['type'] = 'phantom'
        vals.append(data)

    if vals:
        new_recs = api.execute_kw(db, uid, password, "mrp.bom", "create", [vals])

if __name__ == '__main__':
    create_products_from_gsheet()