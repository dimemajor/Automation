import pdfplumber
import pandas as pd
import glob
import re
from concurrent.futures import ProcessPoolExecutor
import time


class PdfExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.table = []
        self.page = None

    def _clean(self, table):
        for i, record in enumerate(table):
            record = [re.sub(r'\n|  +','', field) for field in record if field is not None]
            # bank statements should have atleast 5 columns
            # debit, credit, balance, date, remarks/reference
            # the length check is to help filter out all other unwanted tables
            if len(record) >= 5:
                if i > 0 and record != self.table[0]: # I assume the first record is the headings so I'm skipping them should they appear in the middle of the page
                    self.table.append(record)
                # If for some reason the first record on subsequent pages are not the same with headings, add them.
                # The subset and superset checks are because of inconsistency in headers of gtbank statement
                elif self.page > 1 and not (set(record) <=(set(self.table[0])) or set(record) >=(set(self.table[0]))): 
                    self.table.append(record)
                elif self.page == 1 and i==0:
                    self.table.append(record)
        return

    def extract_data(self):
        with pdfplumber.open(self.file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                self.page = i+1
                table = page.extract_table()
                self._clean(table)
        return self.table

    def save_to_excel(self, dataframe):
        file_name = self.file_path.replace('.pdf', '.xlsx')
        dataframe.to_excel(file_name, index=False,  header=False)

def process_pdf(file_path):
    extractor = PdfExtractor(file_path)
    data = extractor.extract_data()
    df = pd.DataFrame(data)
    extractor.save_to_excel(df)

def main():
    t1 = time.perf_counter()
    pdf_files = glob.glob("*.pdf")
    with ProcessPoolExecutor() as executor:
        executor.map(process_pdf, pdf_files)
    print(f'finished in {time.perf_counter()-t1}s')

if __name__ == '__main__':
    main()