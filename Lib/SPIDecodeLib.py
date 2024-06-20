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

timerBorderTop = Border(top=Side(style=BORDER_THIN, color=BLACK), 
                        left=Side(style=BORDER_THIN, color=BLACK), 
                        right=Side(style=BORDER_THIN, color=BLACK))
timerBorderMid = Border(left=Side(style=BORDER_THIN, color=BLACK), 
                        right=Side(style=BORDER_THIN, color=BLACK))
timerBorderBtm = Border(left=Side(style=BORDER_THIN, color=BLACK), 
                        right=Side(style=BORDER_THIN, color=BLACK), 
                        bottom=Side(style=BORDER_THIN, color=BLACK))

class SPI_CMD(int):
    SPI_CONTINUE = 0x00   #前コメントを続きて実施する
    SPI_PP = 0x02         #ページプログラム
    SPI_READ = 0x03       #読み出し
    SPI_RDSR1 = 0x05      #ステータス レジスタ1 読み出し
    SPI_WREN  = 0x06      #WriteEnable
    SPI_FAST_READ = 0x0B  #高速読み出し
    SPI_RDSR3 = 0x15      #ステータス レジスタ3 読み出し
    SPI_RDCR2 = 0x35      #ステータス レジスタ2 読み出し
    SPI_RSFDP = 0x5A      #SFDP読み出し
    
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
        dstTimerData:dict[str, list[str]] ={}
        dstMemoryDataList:dict[str, list[str]] ={}
        dstMemoryFileComment:list[str] = []
        dstTimer1FileComment:list[str] = []
        dstTimer2FileComment:list[str] = []
        dstExcelSheetComment:list[list[str]] = []


        #対象ファイル内容取得処理
        bResult = self.FileSysProcess.getFileComment(srcFileAddr, srcfileComment)
        if bResult == False:
            return bResult
        
        #対象ファイルからメモリ内容取得
        csvType = self.__analyseSrcData(srcfileComment, dstAddrData, dstTimerData)
        if csvType == 0:
            return False
        
        #出力メモリ内容フォーマット作成
        self.__createMemoryList(dstAddrData, dstMemoryDataList)

        #メモリテキスト出力フォーマット作成
        self.__createMemoryTextFile(dstMemoryDataList, dstMemoryFileComment)
        #メモリテキストファイル出力
        bResult = self.FileSysProcess.writeFileComment(dstFileAddrList[0], dstMemoryFileComment)
        #タイムテキスト出力フォーマット作成
        #timer1
        self.__createTimer1TextFile(dstTimerData, dstTimer1FileComment, csvType)
        #タイムテキストテキストファイル出力
        bResult = self.FileSysProcess.writeFileComment(dstFileAddrList[1], dstTimer1FileComment)
        #timer2
        self.__createTimer2TextFile(dstTimerData, dstTimer2FileComment, csvType)
        #タイムテキストテキストファイル出力
        bResult = self.FileSysProcess.writeFileComment(dstFileAddrList[2], dstTimer2FileComment)
        if len(dstFileAddrList) >= 4 :
            dstExcelSheetComment.clear()
            dstExcelSheetComment.append(dstMemoryFileComment)
            dstExcelSheetComment.append(dstTimer1FileComment)
            dstExcelSheetComment.append(dstTimer2FileComment)
            #Excelファイル出力
            bResult = self.__CreateExcelFile(dstFileAddrList[3], dstExcelSheetComment)
        return bResult
    
    def __analyseSrcData(self,srcfileComment:list[str], dstAddrData:dict[int, list[str]], dstTimerData:dict[str, list[str]]) -> int:
        analyseStrList:list[list[str]] = []
        csvType = 0
        #ファイル内容分割処理
        bResult = self.StrLib.splitFileComment(srcfileComment, analyseStrList, ",")
        if bResult == False:
            return csvType
        if len(analyseStrList[0]) == 7:
            csvType = 2
            bResult = self.__analyseSrcData_Type2(analyseStrList, dstAddrData, dstTimerData)
        else:
            csvType = 1
            bResult = self.__analyseSrcData_Type1(analyseStrList, dstAddrData, dstTimerData)
        return csvType

    def __analyseSrcData_Type1(self, analyseStrList:list[list[str]], dstAddrData:dict[int, list[str]], dstTimerData:dict[str, list[str]]) -> bool:
        
        memroryDataBase:dict[int, list[str]] = {}

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
            strMOSIList = self.StrLib.splitString(strMOSI, " ")
            strMISO = analyseStr[2]
            strMISOList = self.StrLib.splitString(strMISO, " ")

            #time変換
            strTimeList = self.StrLib.splitString(strTime, "e")
            baseTime = float(strTimeList[0])
            eoffset = 10 + int(strTimeList[1])
            strTime = str(int( baseTime * (10 ** eoffset)))

            memoryAddr = self.__addMemroyData(dstTimerData, strTime, strMOSIList, strMISOList, memroryDataBase, SPI_CMD.SPI_PP)
        
        self.__createDstAddrData(memroryDataBase, dstAddrData)

        return True

    def __analyseSrcData_Type2(self,analyseStrList:list[list[str]], dstAddrData:dict[int, list[str]], dstTimerData:dict[str, list[str]]) -> bool:
        memroryDataBase:dict[int, list[str]] = {}
        memoryAddr = 0x000000
        spiCMDList:list[int] = []
        bResult = True
        dstTimerData.clear()
        spiCMDList.clear()
        preDataLen = 0
        preSpiCMD =-1
        for analyseRowDataList in analyseStrList:
            dataLen = int(analyseRowDataList[4])
            if dataLen <= 4 :
                continue
            #行内容取得
            strTime = analyseRowDataList[1].replace('"','')
            strMOSI = analyseRowDataList[6].replace('"','').strip(" ")
            strMOSIList = self.StrLib.splitString(strMOSI, " ")
            strMISO = analyseRowDataList[5].replace('"','').strip(" ")
            strMISOList = self.StrLib.splitString(strMISO, " ")

            curSpiCMD = int(strMOSIList[0], 16)
            spiCMDList.append(curSpiCMD)

            match curSpiCMD :
                # 0x02 :ページプログラム
                case SPI_CMD.SPI_PP:
                    memoryAddr = self.__addMemroyData(dstTimerData, strTime, strMOSIList, strMISOList, memroryDataBase, curSpiCMD)

                # 0x03 :読み出し
                case SPI_CMD.SPI_READ:
                    memoryAddr = self.__addMemroyData(dstTimerData, strTime, strMOSIList, strMISOList, memroryDataBase, curSpiCMD)

                # 0x0B :高速読み出し
                case SPI_CMD.SPI_FAST_READ:
                    memoryAddr = self.__addMemroyData(dstTimerData, strTime, strMOSIList, strMISOList, memroryDataBase, curSpiCMD)

                # 0x00 :前コメントを引き続き実施する 
                case SPI_CMD.SPI_CONTINUE:
                    if preSpiCMD != SPI_CMD.SPI_CONTINUE:
                        memoryAddr =  memoryAddr + preDataLen -4
                    else :
                        memoryAddr =  memoryAddr + preDataLen

                    strMemoryAddr = format(memoryAddr, "06X")
                    dstTimerData[strTime] = []
                    dstTimerData[strTime].append(strMOSIList[0])
                    dstTimerData[strTime].append(strMemoryAddr[0:2])
                    dstTimerData[strTime].append(strMemoryAddr[2:4])
                    dstTimerData[strTime].append(strMemoryAddr[4:6])
                    self.__addMemoryData2MemoryList(memroryDataBase, strMISOList, memoryAddr)
                    self.__addMemoryData2TimerDataList(dstTimerData, strTime, strMISOList)

                case _:
                    continue

            preDataLen = dataLen
            preSpiCMD  = curSpiCMD
        self.__createDstAddrData(memroryDataBase, dstAddrData)
        return bResult
    
    def __addMemroyData(self,dstTimerData:dict[str, list[str]], strTime:str, strMOSIList:list[str], strMISOList:list[str], memroryDataBase:dict[int, list[str]], spiCmd:SPI_CMD ) ->int:
        #アドレス計算
        memoryAddr = int(strMOSIList[1]+strMOSIList[2]+strMOSIList[3], 16)

        dstTimerData[strTime] = []
        dstTimerData[strTime].append(strMOSIList[0])
        dstTimerData[strTime].append(strMOSIList[1])
        dstTimerData[strTime].append(strMOSIList[2])
        dstTimerData[strTime].append(strMOSIList[3])
        if spiCmd == SPI_CMD.SPI_READ :
            strMISOList.pop(0)
            strMISOList.pop(0)
            strMISOList.pop(0)
            strMISOList.pop(0)
        elif spiCmd == SPI_CMD.SPI_FAST_READ :
            strMISOList.pop(0)
            strMISOList.pop(0)
            strMISOList.pop(0)
            strMISOList.pop(0)
            strMISOList.pop(0)
        elif spiCmd == SPI_CMD.SPI_PP :
            strMISOList = strMOSIList
            strMISOList.pop(0)
            strMISOList.pop(0)
            strMISOList.pop(0)
            strMISOList.pop(0)
        else: pass

        self.__addMemoryData2MemoryList(memroryDataBase, strMISOList, memoryAddr)
        self.__addMemoryData2TimerDataList(dstTimerData, strTime, strMISOList)
        return memoryAddr

    def __addMemoryData2MemoryList(self, memroryDataBase:dict[int, list[str]], strMISOList:list[str],  memoryAddr:int) ->None:
        memroryDataBase[memoryAddr] = []
        #アドレスデータ取得
        for memoryData in strMISOList:
            memroryDataBase[memoryAddr].append(memoryData)
        return
    
    def __addMemoryData2TimerDataList(self,dstTimerData:dict[str, list[str]], strTime:str,  strMISOList:list[str]) ->None:
        #アドレスデータ取得
        for memoryData in strMISOList:
            dstTimerData[strTime].append(memoryData)
        return


    def __createDstAddrData(self, memroryDataBase:dict[int, list[str]], dstAddrData:dict[int, list[str]]) ->None:
        memroryDataSort:dict[int, list[str]] = {} 
        self.StrLib.sortDict(memroryDataBase, memroryDataSort)

        dstAddrData.clear()
        curBaseAddr = -1
        curEndAddr = -1
        for address, valueList in memroryDataSort.items():
            if address != curEndAddr :
                curBaseAddr = address
                dstAddrData[curBaseAddr] = []
                curEndAddr = address + len(valueList)
            else:
                curEndAddr += len(valueList)
            for value in valueList:
                dstAddrData[curBaseAddr].append(value)  
        return
    
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
    
    def __createTimer1TextFile(self, dstTimerData:dict[str, list[str]], textFileComment:list[str], csvType:int ) -> None:
        textFileComment.clear()
        #タイトル作成
        if csvType == 1 :
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
        else:
            lstMemoryData = list(dstTimerData.values())
            lstMemoryCount = [len(MemoryCount) for MemoryCount in lstMemoryData]
            maxCount = max(lstMemoryCount) - 4
            lineStr = 'Timer       \t'
            lineStr += 'Address\t'
            
            index = 0
            while index <maxCount :
                hexIndex = format(index, "03X")
                lineStr = lineStr + hexIndex + '\t'
                index += 1
            lineStr = lineStr[:-1] + "\n"

        textFileComment.append(lineStr)
        TimerLsb = 10 ** 7
        #メモリデータ内容取得
        for timer, valueList in  dstTimerData.items():
            if csvType == 1 :
                lineStr = format(int(timer)/TimerLsb, 'f') + "\t"
            else :
                lineStr = timer + "\t"
            
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
    
    def __createTimer2TextFile(self, dstTimerData:dict[str, list[str]], textFileComment:list[str], csvType:int ) -> None:
        textFileComment.clear()
        #タイトル作成
        if csvType == 1 :
            lineStr = 'Timer(ms)\t'
        else:
            lineStr = 'Timer       \t'

        lineStr += 'Address\t'
        lineStr += '00\t'+'01\t'+'02\t'+'03\t'+'04\t'+'05\t'+'06\t'+'07\t'
        lineStr += '08\t'+'09\t'+'0A\t'+'0B\t'+'0C\t'+'0D\t'+'0E\t'+'0F\n'

        textFileComment.append(lineStr)
        TimerLsb = 10 ** 7
        hexAddr = ""
        #メモリデータ内容取得
        for timer, valueList in  dstTimerData.items():
            hexAddr = ""
            if csvType == 1 :
                lineStr = format(int(timer)/TimerLsb, 'f') + "\t"
            else :
                lineStr = timer + "\t"

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
                    if csvType == 1 :
                        lineStr += "        \t" + hexAddr + "\t"
                    else:
                        lineStr += "            \t" + hexAddr + "\t"
                    continue

                lineStr +=  "\t"
  
            lineStr =lineStr[:-1]
            lineStr +="\n"

            textFileComment.append(lineStr)
        return
    
    def __CreateExcelFile(self,dstFileAddr:str, dstExcelSheetComment:list[list[str]]) ->bool:
        dstMemoryFileComment = dstExcelSheetComment[0]
        dstTimer1FileComment = dstExcelSheetComment[1]
        dstTimer2FileComment = dstExcelSheetComment[2]

        #ExcelFile作成
        bResult = self.ExcelLib.createExcelFile(dstFileAddr)
        bResult = self.ExcelLib.setWorkSheet()
        fileName:list[str] = []
        self.FileSysProcess.getFileNameInfoByFileFullAddr(dstFileAddr,fileName)

        #Memoryシート作成
        self.ExcelLib.modifySheetName(dstSheetName=fileName[1] + '_Memory')
        self.__CreateExcelFile_MemoryDataSheet(dstMemoryFileComment)

        #Timerシート作成
        self.ExcelLib.createSheet(fileName[1] + '_Timer1')
        self.__CreateExcelFile_Timer1DataSheet(dstTimer1FileComment)

        self.ExcelLib.createSheet(fileName[1] + '_Timer2')
        self.__CreateExcelFile_Timer2DataSheet(dstTimer2FileComment)

        #ExcelFile保存
        self.ExcelLib.save()
        return True
    
    def __CreateExcelFile_MemoryDataSheet(self,dstMemoryFileComment:list[str]) ->None:
        
        rowIndex = 2

        #列幅設定
        self.ExcelLib.setColumnsWidth(2,2, 9)
        self.ExcelLib.setColumnsWidth(3,18, 3.5)

        #タイトル背景色設定
        colorValue = 'B4E6A0'
        self.ExcelLib.setBackGroundColor(2, 2, 18, colorValue)

        #セルデータ入力
        for rowStrComment in dstMemoryFileComment:
            colIndex = 2
            rowStrComment = rowStrComment.replace('\n', '')
            rowStrList = rowStrComment.split('\t')
            for rowStr in rowStrList:
                self.ExcelLib.addCellValue(rowIndex,colIndex, rowStr.strip(" "))
                colIndex += 1
            rowIndex += 1

        #枠線設定
        rowIndex -= 1
        self.ExcelLib.setBorder(2,rowIndex, 2, 2)
        self._SetRowAddrDataBorder(2, rowIndex, 3)
        colorValue = 'C0C0C0'
        self.ExcelLib.setBackGroundColorByCellValue(3, rowIndex, 3, 18,'xx', colorValue)
        return
    
    def __CreateExcelFile_Timer1DataSheet(self, dstTimer1FileComment:list[str]) ->None:

        rowIndex = 2

        colValueEndIndex = len(dstTimer1FileComment[0].split('\t')) + 1

        #列幅設定
        self.ExcelLib.setColumnsWidth(2,3, 12)
        self.ExcelLib.setColumnsWidth(4,colValueEndIndex, 3.5)

        #タイトル背景色設定
        colorValue = 'B4E6A0'
        self.ExcelLib.setBackGroundColor(2, 2, colValueEndIndex, colorValue)

        #セルデータ入力
        colorValue = 'C0C0C0'
        for rowStrComment in dstTimer1FileComment:
            colIndex = 2
            rowStrComment = rowStrComment.replace('\n', '')
            rowStrList = rowStrComment.split('\t')
            for rowStr in rowStrList:
                self.ExcelLib.addCellValue(rowIndex,colIndex, rowStr.strip(" "))
                colIndex += 1
            
            if colIndex > colValueEndIndex:
                colIndex = colValueEndIndex
            if colIndex != colValueEndIndex:   
                self.ExcelLib.setBackGroundColor(rowIndex, colIndex, colIndex, colorValue)
            self.ExcelLib.setBorder(rowIndex,rowIndex, 2, colIndex)

            rowIndex += 1

        return
    
    def __CreateExcelFile_Timer2DataSheet(self, dstTimer2FileComment:list[str]) ->None:
        #タイトル作成
        rowIndex = 2
        colValueEndIndex = len(dstTimer2FileComment[0].split('\t')) + 1

        #列幅設定
        self.ExcelLib.setColumnsWidth(2,3, 12)
        self.ExcelLib.setColumnsWidth(4,colValueEndIndex, 3.5)

        #タイトル背景色設定
        colorValue = 'B4E6A0'
        self.ExcelLib.setBackGroundColor(2, 2, colValueEndIndex, colorValue)

        #セルデータ入力
        colorValue = 'C0C0C0'
        for oneRowStrComment in dstTimer2FileComment:
            startRowIndex = rowIndex
            rowStrCommentList =  oneRowStrComment[:-1].split('\n')
            for rowStrComment in rowStrCommentList:
                colIndex = 2
                rowStrList = rowStrComment.split('\t')
                for rowStr in rowStrList:
                    self.ExcelLib.addCellValue(rowIndex,colIndex, rowStr.strip(" "))
                    colIndex += 1
                rowIndex += 1
            #タイマー枠線設定
            self.__SetTimerBorder(startRowIndex, rowIndex - 1, 2)
            self.ExcelLib.setBackGroundColor(rowIndex - 1, colIndex, colValueEndIndex, colorValue)

        #枠線設定
        rowIndex -= 1
        self.ExcelLib.setBorder(2,rowIndex, 3, 3)
        self._SetRowAddrDataBorder(2, rowIndex, 4)
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
