from openpyxl import Workbook
import datetime
import time
class Operations:

    # def __copyToWorksheet(self):


    def createJournalReport():
        wb = Workbook()
        ws = wb.active
        ws.title = "Journal"
        ws['A1']= str(time.strftime("%Y-%m-%d"))
        wb.save('C:\\Users\\Emmanuel\\Desktop\\balances.xlsx')

# Operations.createJournalReport()
