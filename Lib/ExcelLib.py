import openpyxl as excel
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fills import PatternFill, FILL_SOLID
from openpyxl.styles.borders import BORDER_THIN
from openpyxl.styles.colors import BLACK
from Lib.FileSysProcess import FileSysProcess

defaultborder = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                       bottom=Side(style=BORDER_THIN, color=BLACK), 
                       left=Side(style=BORDER_THIN, color=BLACK),
                       right=Side(style=BORDER_THIN, color=BLACK))

class ECell(object):
    cellRange:str
    def __init__(self)->None: 
        self.columnNameList:dict[int,str] ={}  
        self.__createColumnNameList()
        self.cellRange = ""
        return

    def getColumnName(self, columnIndex:int) ->str:
        return self.columnNameList[columnIndex]
    
    def setCellRange(self,rowIndex:int = 0, columnIndex:int = 0, endRowIndex:int = 0,  endColumnIndex:int = 0)->None:
        
        if rowIndex + columnIndex == 0:
            self.cellRange = 'A1'
            return
        
        if rowIndex == endRowIndex:
            endRowIndex = 0
        if columnIndex == endColumnIndex:
            endColumnIndex = 0

        if columnIndex + endRowIndex + endColumnIndex == 0:
            self.cellRange = str(rowIndex) + ':'+ str(rowIndex)
            return

        if rowIndex + endRowIndex + endColumnIndex == 0:
            self.cellRange = self.getColumnName(columnIndex)
            return
        
        if rowIndex + endRowIndex == 0:
            self.cellRange = self.getColumnName(columnIndex) + ':'+ self.getColumnName(endColumnIndex)
            return

        if endRowIndex + endColumnIndex == 0:
            self.cellRange = self.getColumnName(columnIndex) + str(rowIndex)
            return
        
        if endRowIndex != 0 and endColumnIndex == 0:
            self.cellRange = self.getColumnName(columnIndex) + str(rowIndex)+ ':' + self.getColumnName(columnIndex) + str(endRowIndex)
            return
        if endRowIndex == 0 and endColumnIndex != 0:
            self.cellRange = self.getColumnName(columnIndex) + str(rowIndex)+ ':' + self.getColumnName(endColumnIndex) + str(rowIndex)
            return
        self.cellRange = self.getColumnName(columnIndex) + str(rowIndex)+ ':' + self.getColumnName(endColumnIndex) + str(endRowIndex)
        return
    def getCellRange(self) ->str:
        if self.cellRange == '':
            return 'A1'
        else:
            return self.cellRange
        
    def __createColumnNameList(self)->None:
        self.columnNameList.clear()
        self.columnNameList[  1 ] = 'A'
        self.columnNameList[  2 ] = 'B'
        self.columnNameList[  3 ] = 'C'
        self.columnNameList[  4 ] = 'D'
        self.columnNameList[  5 ] = 'E'
        self.columnNameList[  6 ] = 'F'
        self.columnNameList[  7 ] = 'G'
        self.columnNameList[  8 ] = 'H'
        self.columnNameList[  9 ] = 'I'
        self.columnNameList[ 10 ] = 'J'
        self.columnNameList[ 11 ] = 'K'
        self.columnNameList[ 12 ] = 'L'
        self.columnNameList[ 13 ] = 'M'
        self.columnNameList[ 14 ] = 'N'
        self.columnNameList[ 15 ] = 'O'
        self.columnNameList[ 16 ] = 'P'
        self.columnNameList[ 17 ] = 'Q'
        self.columnNameList[ 18 ] = 'R'
        self.columnNameList[ 19 ] = 'S'
        self.columnNameList[ 20 ] = 'T'
        self.columnNameList[ 21 ] = 'U'
        self.columnNameList[ 22 ] = 'V'
        self.columnNameList[ 23 ] = 'W'
        self.columnNameList[ 24 ] = 'X'
        self.columnNameList[ 25 ] = 'Y'
        self.columnNameList[ 26 ] = 'Z'
        self.columnNameList[ 27 ] = 'AA'
        self.columnNameList[ 28 ] = 'AB'
        self.columnNameList[ 29 ] = 'AC'
        self.columnNameList[ 30 ] = 'AD'
        self.columnNameList[ 31 ] = 'AE'
        self.columnNameList[ 32 ] = 'AF'
        self.columnNameList[ 33 ] = 'AG'
        self.columnNameList[ 34 ] = 'AH'
        self.columnNameList[ 35 ] = 'AI'
        self.columnNameList[ 36 ] = 'AJ'
        self.columnNameList[ 37 ] = 'AK'
        self.columnNameList[ 38 ] = 'AL'
        self.columnNameList[ 39 ] = 'AM'
        self.columnNameList[ 40 ] = 'AN'
        self.columnNameList[ 41 ] = 'AO'
        self.columnNameList[ 42 ] = 'AP'
        self.columnNameList[ 43 ] = 'AQ'
        self.columnNameList[ 44 ] = 'AR'
        self.columnNameList[ 45 ] = 'AS'
        self.columnNameList[ 46 ] = 'AT'
        self.columnNameList[ 47 ] = 'AU'
        self.columnNameList[ 48 ] = 'AV'
        self.columnNameList[ 49 ] = 'AW'
        self.columnNameList[ 50 ] = 'AX'
        self.columnNameList[ 51 ] = 'AY'
        self.columnNameList[ 52 ] = 'AZ'
        self.columnNameList[ 53 ] = 'BA'
        self.columnNameList[ 54 ] = 'BB'
        self.columnNameList[ 55 ] = 'BC'
        self.columnNameList[ 56 ] = 'BD'
        self.columnNameList[ 57 ] = 'BE'
        self.columnNameList[ 58 ] = 'BF'
        self.columnNameList[ 59 ] = 'BG'
        self.columnNameList[ 60 ] = 'BH'
        self.columnNameList[ 61 ] = 'BI'
        self.columnNameList[ 62 ] = 'BJ'
        self.columnNameList[ 63 ] = 'BK'
        self.columnNameList[ 64 ] = 'BL'
        self.columnNameList[ 65 ] = 'BM'
        self.columnNameList[ 66 ] = 'BN'
        self.columnNameList[ 67 ] = 'BO'
        self.columnNameList[ 68 ] = 'BP'
        self.columnNameList[ 69 ] = 'BQ'
        self.columnNameList[ 70 ] = 'BR'
        self.columnNameList[ 71 ] = 'BS'
        self.columnNameList[ 72 ] = 'BT'
        self.columnNameList[ 73 ] = 'BU'
        self.columnNameList[ 74 ] = 'BV'
        self.columnNameList[ 75 ] = 'BW'
        self.columnNameList[ 76 ] = 'BX'
        self.columnNameList[ 77 ] = 'BY'
        self.columnNameList[ 78 ] = 'BZ'
        self.columnNameList[ 79 ] = 'CA'
        self.columnNameList[ 80 ] = 'CB'
        self.columnNameList[ 81 ] = 'CC'
        self.columnNameList[ 82 ] = 'CD'
        self.columnNameList[ 83 ] = 'CE'
        self.columnNameList[ 84 ] = 'CF'
        self.columnNameList[ 85 ] = 'CG'
        self.columnNameList[ 86 ] = 'CH'
        self.columnNameList[ 87 ] = 'CI'
        self.columnNameList[ 88 ] = 'CJ'
        self.columnNameList[ 89 ] = 'CK'
        self.columnNameList[ 90 ] = 'CL'
        self.columnNameList[ 91 ] = 'CM'
        self.columnNameList[ 92 ] = 'CN'
        self.columnNameList[ 93 ] = 'CO'
        self.columnNameList[ 94 ] = 'CP'
        self.columnNameList[ 95 ] = 'CQ'
        self.columnNameList[ 96 ] = 'CR'
        self.columnNameList[ 97 ] = 'CS'
        self.columnNameList[ 98 ] = 'CT'
        self.columnNameList[ 99 ] = 'CU'
        self.columnNameList[ 100] = 'CV'
        self.columnNameList[ 101] = 'CW'
        self.columnNameList[ 102] = 'CX'
        self.columnNameList[ 103] = 'CY'
        self.columnNameList[ 104] = 'CZ'
        self.columnNameList[ 105] = 'DA'
        self.columnNameList[ 106] = 'DB'
        self.columnNameList[ 107] = 'DC'
        self.columnNameList[ 108] = 'DD'
        self.columnNameList[ 109] = 'DE'
        self.columnNameList[ 110] = 'DF'
        self.columnNameList[ 111] = 'DG'
        self.columnNameList[ 112] = 'DH'
        self.columnNameList[ 113] = 'DI'
        self.columnNameList[ 114] = 'DJ'
        self.columnNameList[ 115] = 'DK'
        self.columnNameList[ 116] = 'DL'
        self.columnNameList[ 117] = 'DM'
        self.columnNameList[ 118] = 'DN'
        self.columnNameList[ 119] = 'DO'
        self.columnNameList[ 120] = 'DP'
        self.columnNameList[ 121] = 'DQ'
        self.columnNameList[ 122] = 'DR'
        self.columnNameList[ 123] = 'DS'
        self.columnNameList[ 124] = 'DT'
        self.columnNameList[ 125] = 'DU'
        self.columnNameList[ 126] = 'DV'
        self.columnNameList[ 127] = 'DW'
        self.columnNameList[ 128] = 'DX'
        self.columnNameList[ 129] = 'DY'
        self.columnNameList[ 130] = 'DZ'
        return


class ExcelLib(ECell):
    workbook:excel.Workbook
    sheetName:str

    def __init__(self)->None:
        super(ExcelLib, self).__init__()
        self.FileSysProcess = FileSysProcess()
        self.sheetName = ''
        self.excelFileAddress = ''
        return
    
    def createExcelFile(self, excelFileAddress:str)->bool:
        """
        --------------------------------------------------
        ExcelFile新規作成\n
        【引数 】\n
            excelFileAddress:ExcelFile格納場所\n
        【戻り値】\n
            bool:処理結果\n
        --------------------------------------------------
        """
        bResult:bool =  True
        try:
            self.excelFileAddress = excelFileAddress
            self.workbook = excel.Workbook()
            self.sheetName = self.workbook.sheetnames[0]
            self.workbook.save(excelFileAddress)
        except Exception as e:
            print('Failure to create excelFile:', excelFileAddress)
            bResult = False
        return bResult

    def openExcelFile(self, excelFileAddress:str, read_only:bool = False)->bool:
        """
        --------------------------------------------------
        ExcelFile開く\n
        【引数 】\n
            excelFileAddress:ExcelFile格納場所\n
        【戻り値】\n
            bool:処理結果\n
        --------------------------------------------------
        """
        bResult:bool =  True
        try:
            self.excelFileAddress = excelFileAddress
            self.workbook = excel.load_workbook(excelFileAddress, read_only=read_only)
            self.sheetName = self.workbook.sheetnames[0]
        except Exception as e:
            print('Failure to open excelFile:', excelFileAddress)
            bResult = False
        return bResult

    
    def setWorkSheet(self, workbook:excel.Workbook|None = None, sheetName:str = '', sheetSearchFlg = False)->bool:
        """
        --------------------------------------------------
        WorkSheet設定\n
        【引数 】\n
            workbook:ExcelFileオブジェクト\n
            sheetName:シート名称\n
            sheetSearchFlg:検索方式(False:完全一致, True:シート名称に指定文字列含む)
        【戻り値】\n
            bool:処理結果\n
        --------------------------------------------------
        """
        if workbook is not None:
            self.workbook = workbook
        
        if self.workbook is None:
            print('workbook is None')
            return False

        if sheetName == '':
            self.sheetName = self.workbook.sheetnames[0]
            return True
        if sheetSearchFlg == False:
            #完全一致
            if sheetName in self.workbook.sheetnames:
                self.sheetName = sheetName
                return True
        else:
            for curSheetName in self.workbook.sheetnames:
                if curSheetName.find(sheetName) >= 0:
                    self.sheetName = curSheetName
                    return True
        print('sheetName is not in excelSheetList')
        return False

    def save(self, excelFileAddress:str = '') ->bool:
        """
        --------------------------------------------------
        Excelファイル内容保存処理\n
        【引数 】\n
            excelFileAddress:ExcelFile格納先\n
        【戻り値】\n
            bool:処理結果\n
        --------------------------------------------------
        """
        if excelFileAddress == '':
            excelFileAddress = self.excelFileAddress

        bResult =  True
        try:
            self.workbook.save(excelFileAddress)
        except Exception as e:
            print(f'excelFileAddress({excelFileAddress}) is not exsited??')
            bResult = False
        return bResult

    
    def modifySheetName(self,dstSheetName:str, srcSheetName:str= '')->bool:
        """
        --------------------------------------------------
        Excelファイルシート名称修正処理\n
        【引数 】\n
            dstSheetName:修正後シートファイル名称\n
            srcSheetName:修正前シートファイル名称\n
        【戻り値】\n
            bool:処理結果\n
        --------------------------------------------------
        """
        if self.workbook is None:
            print('workbook is None')
            return False

        if dstSheetName == '':
            print('dstSheetName is Null')
            return False
        if srcSheetName != '':
            if srcSheetName in self.workbook.sheetnames:
                self.sheetName = srcSheetName
            else:
                print(f'srcSheetName({srcSheetName}) is not exsited in excelSheetList')
                return False

        self.workbook[self.sheetName].title = dstSheetName
        self.sheetName = dstSheetName
        return True
    
    def createSheet(self, sheetName:str= '')->bool:
        if self.workbook is None:
            print('workbook is None')
            return False
        
        if sheetName == '':
            sheetIndex = len(self.workbook.sheetnames)
            self.workbook.create_sheet()
            self.sheetName = self.workbook.sheetnames[sheetIndex]
        else:
            sheetIndex = len(self.workbook.sheetnames)
            self.workbook.create_sheet(index = sheetIndex, title= sheetName)
            self.sheetName = sheetName
        return True
        


    def setColumnsWidth(self,columnIndex:int, endColumnIndex:int = 0, withValue:float|int = 3)->bool:
        if self.workbook is None:
            print('workbook is None')
            return False

        worksheet = self.workbook[self.sheetName]
        if columnIndex <= 0:
            return False
        if endColumnIndex == 0:
            endColumnIndex = columnIndex
        if endColumnIndex < columnIndex:
            return False
        while(columnIndex <= endColumnIndex):
            worksheet.column_dimensions[self.getColumnName(columnIndex)].width = str(withValue)
            columnIndex += 1
        return True
    
    # 罫線(外枠)を設定
    def setBorder(self,startRowIndex:int, endRowIndex:int, startColumnIndex:int, endColumnIndex:int, border:Border = defaultborder)->None:

        worksheet = self.workbook[self.sheetName]
        for rowIndex in range(startRowIndex,endRowIndex + 1):
            for columnIndex in range(startColumnIndex,endColumnIndex + 1):
                worksheet.cell(row=rowIndex ,column=columnIndex).border = border

    #背景色設定
    def setBackGroundColor(self,rowIndex:int,startColumnIndex:int, endColumnIndex:int, colorValue:str)->None:
        
        fillColor = PatternFill(patternType=FILL_SOLID, fgColor=colorValue, bgColor=colorValue)
        worksheet = self.workbook[self.sheetName]
        for columnIndex in range(startColumnIndex, endColumnIndex + 1):
            cellPos = self.getColumnName(columnIndex) + str(rowIndex)
            worksheet[cellPos].fill = fillColor
        return
    
    def setBackGroundColorByCellValue(self,startRowIndex:int, endRowIndex:int,startColumnIndex:int, endColumnIndex:int, cellValue:str, colorValue:str)->None:
        
        worksheet = self.workbook[self.sheetName]

        for rowIndex in range(startRowIndex,endRowIndex + 1):
            for columnIndex in range(startColumnIndex,endColumnIndex + 1):
                cellPos = self.getColumnName(columnIndex) + str(rowIndex)
                if worksheet[cellPos].value == cellValue:
                    self.setBackGroundColor(rowIndex, columnIndex, columnIndex, colorValue)
        return

    def addCellValue(self, rowIndex:int, columnIndex:int,  dataValue:int|bool|str)->None:
        worksheet = self.workbook[self.sheetName]
        cellPos = self.getColumnName(columnIndex) + str(rowIndex)
        worksheet[cellPos] = str(dataValue)
        return
    
    def mergeCells(self, startRowIndex:int, endRowIndex:int,startColumnIndex:int, endColumnIndex:int)->None:
        worksheet = self.workbook[self.sheetName]
        worksheet.merge_cells(start_row= startRowIndex, start_column= startColumnIndex, end_row=endRowIndex, end_column= endColumnIndex)
        return
        
