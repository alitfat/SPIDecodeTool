from Lib.FileSysProcess import FileSysProcess
from Lib.ExcelLib import ExcelLib
from Lib.StrLib import StrLib

from openpyxl.styles.borders import Border, Side,BORDER_THIN, BORDER_DOTTED
from openpyxl.styles.colors import BLACK

memoryBorderL1 = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                        bottom=Side(style=BORDER_THIN, color=BLACK), 
                        left=Side(style=BORDER_THIN, color=BLACK),
                        right=Side(style=BORDER_DOTTED, color=BLACK))
memoryBorderL2 = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                        bottom=Side(style=BORDER_THIN, color=BLACK), 
                        left=Side(style=BORDER_DOTTED, color=BLACK),
                        right=Side(style=BORDER_DOTTED, color=BLACK))
memoryBorderL3 = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                        bottom=Side(style=BORDER_THIN, color=BLACK), 
                        left=Side(style=BORDER_DOTTED, color=BLACK),
                        right=Side(style=BORDER_DOTTED, color=BLACK))
memoryBorderL4 = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                        bottom=Side(style=BORDER_THIN, color=BLACK), 
                        left=Side(style=BORDER_DOTTED, color=BLACK),
                        right=Side(style=BORDER_THIN, color=BLACK))

timerAddrBorderL1 = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                           bottom=Side(style=BORDER_THIN, color=BLACK), 
                           left=Side(style=BORDER_THIN, color=BLACK))
timerAddrBorderL23= Border(top=Side(style=BORDER_THIN, color=BLACK), 
                           bottom=Side(style=BORDER_THIN, color=BLACK))
timerAddrBorderL4 = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                           bottom=Side(style=BORDER_THIN, color=BLACK), 
                           right=Side(style=BORDER_THIN, color=BLACK))

timerBorderTop = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                        left=Side(style=BORDER_THIN, color=BLACK), 
                        right=Side(style=BORDER_THIN, color=BLACK))
timerBorderMid = Border(left=Side(style=BORDER_THIN, color=BLACK), 
                        right=Side(style=BORDER_THIN, color=BLACK))
timerBorderBtm = Border(left=Side(style=BORDER_THIN, color=BLACK), 
                        right=Side(style=BORDER_THIN, color=BLACK), 
                        bottom=Side(style=BORDER_THIN, color=BLACK))

class SPIDecodeLib(object):
    
    def __init__(self)->None:
        super(SPIDecodeLib, self).__init__()
        self.FileSysProcess = FileSysProcess()
        self.StrLib = StrLib()
        self.ExcelLib = ExcelLib() 
        return
    
    def SPIDecodeLib_Process(self, srcFileAddr:str, dstFileAddrList:list[str]) -> bool:
        """
        --------------------------------------------------
        SPIDecodeLib処理\n
        【引数 】\n
            srtFileAddr:読取対象ファイル\n
            dstFileAddrList:生成結果対象ファイル\n
        【戻り値】\n
            bool:処理結果\n
        --------------------------------------------------
        """
        srcfileComment:list[str] = []
        dstAddrData:dict[int, list[str]] ={}
        dstTimerData:dict[int, list[str]] ={}
        dstMemoryDataList:dict[str, list[str]] ={}
        dstFileComment:list[str] = []

        #対象ファイル内容取得処理
        bResult = self.FileSysProcess.getFileComment(srcFileAddr, srcfileComment)
        if bResult == False:
            return bResult
        
        #対象ファイルからメモリ内容取得
        bResult = self.__analyseSrcData(srcfileComment, dstAddrData, dstTimerData)
        if bResult == False:
            return bResult
        
        #出力メモリ内容フォーマット作成
        self.__createMemoryList(dstAddrData, dstMemoryDataList)

        #メモリテキスト出力フォーマット作成
        self.__createMemoryTextFile(dstMemoryDataList, dstFileComment)
        #メモリテキストファイル出力
        bResult = self.FileSysProcess.writeFileComment(dstFileAddrList[0], dstFileComment)

        #タイムテキスト出力フォーマット作成
        #timer1
        self.__createTimer1TextFile(dstTimerData, dstFileComment)
        #タイムテキストテキストファイル出力
        bResult = self.FileSysProcess.writeFileComment(dstFileAddrList[1], dstFileComment)

        #timer2
        self.__createTimer2TextFile(dstTimerData, dstFileComment)
        #タイムテキストテキストファイル出力
        bResult = self.FileSysProcess.writeFileComment(dstFileAddrList[2], dstFileComment)

        #Excelファイル出力
        bResult = self.__CreateExcelFile(dstFileAddrList[3], dstMemoryDataList, dstTimerData)
        return bResult
    
    def __analyseSrcData(self,srcfileComment:list[str], dstAddrData:dict[int, list[str]], dstTimerData:dict[int, list[str]]) -> bool:
        analyseStrList:list[list[str]] = []
        memroryDataBase:dict[int, list[str]] = {}
        memroryDataSort:dict[int, list[str]] = {} 
        #ファイル内容分割処理
        bResult = self.StrLib.splitFileComment(srcfileComment, analyseStrList, ",")
        if bResult == False:
            return bResult
        
        startIndex:int = 0
        for index in range(len(analyseStrList)):
            if analyseStrList[index][0] == 'Time':
                startIndex = index + 1
                break
        dstTimerData.clear()
        for analyseStr in analyseStrList[startIndex:len(analyseStrList):1]:
            #行内容取得
            strTime = analyseStr[0]
            strMOSI = analyseStr[1]
            strMISO = analyseStr[2]
            #行内容split
            strTimeList = self.StrLib.splitString(strTime, "e")
            strMOSIList = self.StrLib.splitString(strMOSI, " ")
            strMISOList = self.StrLib.splitString(strMISO, " ")
            #time計算
            baseTime = float(strTimeList[0])
            eoffset = 10 + int(strTimeList[1])
            timer = int( baseTime * (10 ** eoffset))
            dstTimerData[timer] = []
            #アドレス格納(strMOSIList[0]はアドレスバイト個数)
            dstTimerData[timer].append(strMOSIList[0])
            dstTimerData[timer].append(strMOSIList[1])
            dstTimerData[timer].append(strMOSIList[2])
            dstTimerData[timer].append(strMOSIList[3])

            #アドレス計算
            memoryAddr = int(strMOSIList[1]+strMOSIList[2]+strMOSIList[3], 16)
            memroryDataBase[memoryAddr] = []

            #アドレスデータ取得
            for memoryData in strMISOList[4:len(strMISOList):1]:
                memroryDataBase[memoryAddr].append(memoryData)
                dstTimerData[timer].append(memoryData)
        
        self.StrLib.sortDict(memroryDataBase, memroryDataSort)

        dstAddrData.clear()
        curBaseAddr = 0
        curEndAddr = 0
        for address, valueList in memroryDataSort.items():
            if address != curEndAddr :
                curBaseAddr = address
                dstAddrData[curBaseAddr] = []
                curEndAddr = address + len(valueList)
            else:
                curEndAddr += len(valueList)
            for value in valueList:
                dstAddrData[curBaseAddr].append(value)

        return bResult
    
    def __createMemoryList(self,dstResult:dict[int, list[str]],dstMemoryDataList:dict[str, list[str]] ) -> None:
        dstMemoryDataList.clear()
        hexAddress_old = ""
        for decStartAddress, valueList in dstResult.items():
            startIndex = decStartAddress % 16
            curAddress = decStartAddress - startIndex
            hexAddress = format(curAddress, "06X")

            if hexAddress != hexAddress_old:
                dstMemoryDataList[hexAddress] = []
                self.__createXXDataList(dstMemoryDataList[hexAddress])
                hexAddress_old = hexAddress

            valueIndex = 0
            curIndex = startIndex
            valueLength = len(valueList)
            while(valueIndex < valueLength):

                if curIndex < 16:
                    dstMemoryDataList[hexAddress][curIndex] = valueList[valueIndex]
                else:
                    curIndex = 0
                    curAddress += 16
                    hexAddress = format(curAddress, "06X")
                    dstMemoryDataList[hexAddress] = []
                    hexAddress_old = hexAddress
                    self.__createXXDataList(dstMemoryDataList[hexAddress])
                    dstMemoryDataList[hexAddress][curIndex] = valueList[valueIndex]
                curIndex += 1
                valueIndex += 1

        return
    
    def __createXXDataList(self, dataList:list[str])->None:
        dataList.clear()
        for index in range(16):
            dataList.append('xx')
        return
    
    def __createMemoryTextFile(self, dstMemoryDataList:dict[str, list[str]], textFileComment:list[str]) -> None:
        textFileComment.clear()
        #タイトル作成
        lineStr = 'Address\t'
        lineStr += '00\t'+'01\t'+'02\t'+'03\t'+'04\t'+'05\t'+'06\t'+'07\t'
        lineStr += '08\t'+'09\t'+'0A\t'+'0B\t'+'0C\t'+'0D\t'+'0E\t'+'0F\n'
        textFileComment.append(lineStr)
        #メモリデータ内容取得
        for address, valueList in dstMemoryDataList.items():
            lineStr = address + "\t"
            for value in valueList:
                lineStr += value + "\t"
            lineStr =lineStr[:-1]
            lineStr +="\n"
            textFileComment.append(lineStr)
        return
    
    def __createTimer1TextFile(self, dstTimerData:dict[int, list[str]], textFileComment:list[str]) -> None:
        textFileComment.clear()
        #タイトル作成
        lineStr = 'Timer(ms)\t'
        lineStr += 'Address\t'
        lineStr += '00\t'+'01\t'+'02\t'+'03\t'+'04\t'+'05\t'+'06\t'+'07\t'
        lineStr += '08\t'+'09\t'+'0A\t'+'0B\t'+'0C\t'+'0D\t'+'0E\t'+'0F\t'
        lineStr += '10\t'+'11\t'+'12\t'+'13\t'+'14\t'+'15\t'+'16\t'+'17\t'
        lineStr += '18\t'+'19\t'+'1A\t'+'1B\t'+'1C\t'+'1D\t'+'1E\t'+'1F\t'
        lineStr += '20\t'+'21\t'+'22\t'+'23\t'+'24\t'+'25\t'+'26\t'+'27\t'
        lineStr += '28\t'+'29\t'+'2A\t'+'2B\t'+'2C\t'+'2D\t'+'2E\t'+'2F\t'
        lineStr += '30\t'+'31\t'+'32\t'+'33\t'+'34\t'+'35\t'+'36\t'+'37\t'
        lineStr += '38\t'+'39\t'+'3A\t'+'3B\t'+'3C\t'+'3D\t'+'3E\t'+'3F\n'

        textFileComment.append(lineStr)
        TimerLsb = 10 ** 7
        #メモリデータ内容取得
        for timer, valueList in  dstTimerData.items():

            lineStr = format(timer/TimerLsb, 'f') + "\t"
            for index , (value) in enumerate(valueList):
                if index == 0:
                    continue
                lineStr += value
                if index >= 3:
                    lineStr +=  "\t"
            lineStr =lineStr[:-1]
            lineStr +="\n"
            textFileComment.append(lineStr)
        return
    
    def __createTimer2TextFile(self, dstTimerData:dict[int, list[str]], textFileComment:list[str]) -> None:
        textFileComment.clear()
        #タイトル作成
        lineStr = 'Timer(ms)\t'
        lineStr += 'Address\t'
        lineStr += '00\t'+'01\t'+'02\t'+'03\t'+'04\t'+'05\t'+'06\t'+'07\t'
        lineStr += '08\t'+'09\t'+'0A\t'+'0B\t'+'0C\t'+'0D\t'+'0E\t'+'0F\n'

        textFileComment.append(lineStr)
        TimerLsb = 10 ** 7
        hexAddr = ""
        #メモリデータ内容取得
        for timer, valueList in  dstTimerData.items():
            hexAddr = ""
            lineStr = format(timer/TimerLsb, 'f') + "\t"
            for index , (value) in enumerate(valueList):
                if index == 0:
                    continue
                lineStr += value
                if index < 3:
                    hexAddr += value
                    continue

                if index == 3:
                    hexAddr += value
                    lineStr +=  "\t"
                    continue

                if (index - 3) % 16 == 0 and index != len(valueList) - 1:
                    decAddr = int(hexAddr, 16) + 16
                    hexAddr = format(decAddr, "06X")
                    lineStr +="\n"
                    lineStr +="        \t" + hexAddr + "\t"
                    continue

                lineStr +=  "\t"
  
            lineStr =lineStr[:-1]
            lineStr +="\n"

            textFileComment.append(lineStr)
        return
    
    def __CreateExcelFile(self,dstFileAddr:str, dstMemoryDataList:dict[str, list[str]], dstTimerData:dict[int, list[str]]) ->bool:
        #ExcelFile作成
        bResult = self.ExcelLib.createExcelFile(dstFileAddr)
        bResult = self.ExcelLib.setWorkSheet()
        fileName:list[str] = []
        self.FileSysProcess.getFileNameInfoByFileFullAddr(dstFileAddr,fileName)

        #Memoryシート作成
        self.ExcelLib.modifySheetName(dstSheetName=fileName[1] + '_Memory')
        self.__CreateExcelFile_MemoryDataSheet(dstMemoryDataList)
        #Timerシート作成
        self.ExcelLib.createSheet(fileName[1] + '_Timer1')
        self.__CreateExcelFile_Timer1DataSheet(dstTimerData)
        self.ExcelLib.createSheet(fileName[1] + '_Timer2')
        self.__CreateExcelFile_Timer2DataSheet(dstTimerData)
        #ExcelFile保存
        self.ExcelLib.save()
        return True
    
    def __CreateExcelFile_MemoryDataSheet(self,dstMemoryDataList:dict[str, list[str]]) ->None:
        #タイトル作成
        rowIndex = 2
        colIndex = 2
        self.ExcelLib.addCellValue(rowIndex,colIndex,'Address')
        colIndex += 1
        colDataIndex = 0
        while(colDataIndex < 16):
            self.ExcelLib.addCellValue(rowIndex,colIndex,format(colDataIndex, "02X"))
            colIndex += 1
            colDataIndex += 1
        
        #列幅設定
        self.ExcelLib.setColumnsWidth(2,2, 9)
        self.ExcelLib.setColumnsWidth(3,18, 3.5)

        #メモリデータ内容出力
        for address, valueList in dstMemoryDataList.items():
            rowIndex += 1
            colIndex = 2
            self.ExcelLib.addCellValue(rowIndex,colIndex, address)
            colIndex += 1
            for value in valueList:
                self.ExcelLib.addCellValue(rowIndex,colIndex, value)
                colIndex += 1

        #枠線設定
        self.ExcelLib.setBorder(2,rowIndex, 2, 2)
        self._SetRowAddrDataBorder(2, rowIndex, 3)

        #タイトル背景色設定
        colorValue = 'B4E6A0'
        self.ExcelLib.setBackGroundColor(2, 2, 18, colorValue)
        colorValue = 'C0C0C0'
        self.ExcelLib.setBackGroundColorByCellValue(3, rowIndex, 3, 18,'xx', colorValue)
        return
    
    def __CreateExcelFile_Timer1DataSheet(self,dstTimerData:dict[int, list[str]]) ->None:
        #タイトル作成
        rowIndex = 2
        colIndex = 2
        self.ExcelLib.addCellValue(rowIndex,colIndex,'Timer(ms)')
        colIndex += 1
        self.ExcelLib.addCellValue(rowIndex,colIndex,'Address')
        colIndex += 3
        colDataIndex = 0
        while(colDataIndex < 64):
            self.ExcelLib.addCellValue(rowIndex,colIndex,format(colDataIndex, "02X"))
            colIndex += 1
            colDataIndex += 1
        
        #列幅設定
        self.ExcelLib.setColumnsWidth(2,2, 9)
        self.ExcelLib.setColumnsWidth(3,69, 3.5)

        #タイトル背景色設定
        colorValue = 'B4E6A0'
        self.ExcelLib.setBackGroundColor(rowIndex, rowIndex, 69, colorValue)

        TimerLsb = 10 ** 7
        colorValue = 'C0C0C0'
        #メモリデータ内容出力
        for timer, valueList in dstTimerData.items():
            rowIndex += 1
            colIndex = 2
            self.ExcelLib.addCellValue(rowIndex,colIndex, format(timer/TimerLsb, 'f'))
            colIndex += 1
            for value in valueList[1:len(valueList):1]:
                self.ExcelLib.addCellValue(rowIndex,colIndex, value)
                colIndex += 1
            self.ExcelLib.setBackGroundColor(rowIndex, colIndex, 69, colorValue)

        #枠線設定
        self.ExcelLib.setBorder(2,rowIndex, 2, 2)
        self.__SetTimerAddrBorder(2, rowIndex, 3)
        self.ExcelLib.setBorder(2,rowIndex, 6, 69)
        return
    
    def __CreateExcelFile_Timer2DataSheet(self,dstTimerData:dict[int, list[str]]) ->None:
        #タイトル作成
        rowIndex = 2
        colIndex = 2
        self.ExcelLib.addCellValue(rowIndex,colIndex,'Timer(ms)')
        colIndex += 1
        self.ExcelLib.addCellValue(rowIndex,colIndex,'Address')
        colIndex += 3
        colDataIndex = 0
        while(colDataIndex < 16):
            self.ExcelLib.addCellValue(rowIndex,colIndex,format(colDataIndex, "02X"))
            colIndex += 1
            colDataIndex += 1
        
        #列幅設定
        self.ExcelLib.setColumnsWidth(2,2, 9)
        self.ExcelLib.setColumnsWidth(3,21, 3.5)

        #タイトル背景色設定
        colorValue = 'B4E6A0'
        self.ExcelLib.setBackGroundColor(rowIndex, rowIndex, 21, colorValue)

        TimerLsb = 10 ** 7
        colorValue = 'C0C0C0'
        #メモリデータ内容出力
        for timer, valueList in dstTimerData.items():
            rowIndex += 1
            startRowIndex = rowIndex
            colIndex = 2
            self.ExcelLib.addCellValue(rowIndex,colIndex, format(timer/TimerLsb, 'f'))
            colIndex += 1
            hexAddr = ''
            for value in valueList[1:len(valueList):1]:
                if colIndex < 6 :
                    hexAddr += value

                if colIndex == 22 :
                    
                    decAddr = int(hexAddr, 16) + 16
                    hexAddr = format(decAddr, "06X")

                    rowIndex += 1
                    colIndex = 3
                    self.ExcelLib.addCellValue(rowIndex,colIndex, hexAddr[0:2])
                    colIndex += 1
                    self.ExcelLib.addCellValue(rowIndex,colIndex, hexAddr[2:4])
                    colIndex += 1
                    self.ExcelLib.addCellValue(rowIndex,colIndex, hexAddr[4:6])
                    colIndex += 1

                self.ExcelLib.addCellValue(rowIndex,colIndex, value)
                colIndex += 1
            
            #タイマー枠線設定
            self.__SetTimerBorder(startRowIndex, rowIndex, 2)
            self.ExcelLib.setBackGroundColor(rowIndex, colIndex, 21, colorValue)

        #枠線設定
        self.ExcelLib.setBorder(2,2, 2, 2)
        self.__SetTimerAddrBorder(2, rowIndex, 3)
        self._SetRowAddrDataBorder(2, rowIndex, 6)
        return

    def __SetTimerBorder(self, startRowIndex:int, endRowIndex:int, columnIndex:int) ->None:
        rowIndex = startRowIndex
        if rowIndex == endRowIndex:
            self.ExcelLib.setBorder(rowIndex, rowIndex, columnIndex, columnIndex)
            return
        
        self.ExcelLib.setBorder(rowIndex, rowIndex, columnIndex, columnIndex, timerBorderTop)
        rowIndex += 1
        while rowIndex < endRowIndex :
            self.ExcelLib.setBorder(rowIndex, rowIndex, columnIndex, columnIndex, timerBorderMid)
            rowIndex += 1
        self.ExcelLib.setBorder(rowIndex, rowIndex, columnIndex, columnIndex, timerBorderBtm)
        return
    
    def __SetTimerAddrBorder(self, startRowIndex:int, endRowIndex:int, columnIndex:int) ->None:
        self.ExcelLib.setBorder(startRowIndex,endRowIndex, columnIndex, columnIndex, timerAddrBorderL1)
        columnIndex += 1
        self.ExcelLib.setBorder(startRowIndex,endRowIndex, columnIndex, columnIndex, timerAddrBorderL23)
        columnIndex += 1
        self.ExcelLib.setBorder(startRowIndex,endRowIndex, columnIndex, columnIndex, timerAddrBorderL4)
        return

    def _SetRowAddrDataBorder(self, startRowIndex:int, endRowIndex:int, columnIndex:int) ->None:
        self.__SetAddrDataBorder(startRowIndex, endRowIndex, columnIndex)
        columnIndex += 4
        self.__SetAddrDataBorder(startRowIndex, endRowIndex, columnIndex)
        columnIndex += 4
        self.__SetAddrDataBorder(startRowIndex, endRowIndex, columnIndex)
        columnIndex += 4
        self.__SetAddrDataBorder(startRowIndex, endRowIndex, columnIndex)
        return

    def __SetAddrDataBorder(self, startRowIndex:int, endRowIndex:int, columnIndex:int) ->None:
        rowIndex = endRowIndex
        self.ExcelLib.setBorder(startRowIndex, rowIndex, columnIndex, columnIndex, memoryBorderL1)
        columnIndex += 1
        self.ExcelLib.setBorder(startRowIndex, rowIndex, columnIndex, columnIndex, memoryBorderL2)
        columnIndex += 1
        self.ExcelLib.setBorder(startRowIndex, rowIndex, columnIndex, columnIndex, memoryBorderL3)
        columnIndex += 1
        self.ExcelLib.setBorder(startRowIndex, rowIndex, columnIndex, columnIndex, memoryBorderL4)
        return
