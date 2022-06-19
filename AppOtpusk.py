import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QFileDialog, QStyledItemDelegate
from PyQt5.QtCore import QDate, QFile, Qt, QRect
#import main
import AdUi
import NCMatrix
import PropertysWidget
import nRestsDialogWindow
import nRestsUi
import dellRestsDialogWindow
import changeDialogClass
import htmlViewClass
import listsAndRatingsClass
import sqlite3
from utils import makePage

nYearsDepth=4
#percent=20
#percentForManagers=8
gammaParametr=0.0005
rules={'percentRule':'Превышен процент одновременных отпусков',
       'percentRuleManagers':'Превышен процент одновременных отпусков руководителей',
       'crossInNCMatrix':'Запрещенное пересечение: ',
       'percenInMonthRule':'Превышен процент отдыхающих в месяце',
       'percenManagersInMonthRule':'Превышен процент руководителей отдыхающих в месяце'   }
virtGridShift=1




class NCMatrixclass(QtWidgets.QWidget, NCMatrix.Ui_FormNCMatrix):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setOnLoad()
    
    def setOnLoad(self):
        self.conn = sqlite3.connect("rest.db")
        res=self.makeSelectQuery("Select sirname from person order by sirname;")
        size=len(res)
        i=0
        for (name,) in res:
            self.comboBoxFirstEmployee.addItem(str(name))
            self.comboBoxSecondEmployee.addItem(str(name))
            self.tableWidgetNCM.setRowCount(size)
            self.tableWidgetNCM.setColumnCount(size)
            self.tableWidgetNCM.setVerticalHeaderItem(i,QTableWidgetItem(name))
            self.tableWidgetNCM.setHorizontalHeaderItem(i,QTableWidgetItem(name))
            self.tableWidgetNCM.setItem(i,i,QTableWidgetItem(""))
            self.tableWidgetNCM.item(i,i).setBackground(QtGui.QColor('grey'))    
            self.tableWidgetNCM.setRowHeight(i,19)
            self.tableWidgetNCM.setColumnWidth(i,70)
            i+=1
        
        for (rule,shorty) in self.makeSelectQuery("Select rule,shorty from NCMatrixRules ;"):    
            self.comboBoxRule.addItem(str(rule))
        
        for (name1,name2,shorty ) in self.makeSelectQuery("SELECT name1.SIRNAME, name2.SIRNAME,  NCMatrixRules.shorty "+
            "  from notCrossingMatrix join (select sirname,n from person) as name1 on notCrossingMatrix.id=name1.n "+
            " join (select sirname,n from person) as name2 on  notCrossingMatrix.blokingId=name2.n "+
            " join NCMatrixRules on NCMatrixRules.id=notCrossingMatrix.blockingRule ;"):
            for i in range(self.tableWidgetNCM.rowCount()):
                if self.tableWidgetNCM.horizontalHeaderItem(i).text()==name1:
                    idOne=i
                if self.tableWidgetNCM.horizontalHeaderItem(i).text()==name2:
                    idTwo=i
            self.tableWidgetNCM.setItem(idOne,idTwo,QTableWidgetItem(str(shorty)))
            
        
        self.pushButtonCreateNewRule.clicked.connect(self.onButtonCreateNewRule_click)
        self.pushButtonApplyRule.clicked.connect(self.onpushButtonApplyRule_click)
        self.pushButtonCancelRule.clicked.connect(self.onpushButtonCancelRule_click)
        
    def makeSelectQuery(self,Query):
        cursor = self.conn.cursor()
        sql = Query
        cursor.execute(sql)
        return cursor.fetchall() # or use fetchone()
    
    def makeChangingQuery(self,Query):    
        cursor = self.conn.cursor()
        
        try:
            cursor.executescript(Query)
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else:
            self.conn.commit()
            
    def onButtonCreateNewRule_click(self):
    
        if self.lineEditNewRule.text() and self.lineEditShorty.text():
            cursor = self.conn.cursor()
            try:
                cursor.execute('INSERT INTO NCMatrixRules (Rule,shorty )VALUES ( ?,? ); ',(self.lineEditNewRule.text(),self.lineEditShorty.text()))
            except sqlite3.DatabaseError as err:       
                print("Error: ", err)
            else:
                self.conn.commit()
                
            self.comboBoxRule.addItem(self.lineEditNewRule.text())
            self.lineEditNewRule.setText('')
            self.lineEditShorty.setText('')
    
    def onpushButtonApplyRule_click(self):
        
        [(idOne,)]=self.makeSelectQuery("select N from person where sirname='"+self.comboBoxFirstEmployee.currentText()+"' ;")
        [(idTwo,)]=self.makeSelectQuery("select N from person where sirname='"+self.comboBoxSecondEmployee.currentText()+"' ;")
        [(idRule, shorty)]=self.makeSelectQuery("select ID,shorty from NCMatrixRules where rule='"+self.comboBoxRule.currentText()+"' ;")
        #print(idOne, " base ", idTwo, " ",idRule, shorty)
        for i in range(self.tableWidgetNCM.rowCount()):
            if self.tableWidgetNCM.horizontalHeaderItem(i).text()==self.comboBoxFirstEmployee.currentText():
                idOneTable=i
            if self.tableWidgetNCM.horizontalHeaderItem(i).text()==self.comboBoxSecondEmployee.currentText():
                idTwoTable=i
        #print(idOneTable, " table ", idTwoTable)
        #print(self.makeSelectQuery('SELECT blockingRule FROM notCrossingMatrix where id='+str(idOne)+';'))
        if (idOne!=idTwo) and not self.makeSelectQuery('SELECT blockingRule FROM notCrossingMatrix where id='+str(idOne)+
                '  and blokingId='+str(idTwo)+';'):
            #print('in if')
            self.makeChangingQuery("INSERT INTO notCrossingMatrix (id, blokingId, blockingRule )  VALUES ( '"+str(idOne)+
            "', '"+str(idTwo)+"', '"+str(idRule)+"');")
            self.makeChangingQuery("INSERT INTO notCrossingMatrix (id, blokingId, blockingRule )  VALUES ( '"+str(idTwo)+
            "', '"+str(idOne)+"', '"+str(idRule)+"');")
            self.tableWidgetNCM.setItem(idOneTable,idTwoTable,QTableWidgetItem(str(shorty)))
            self.tableWidgetNCM.setItem(idTwoTable,idOneTable,QTableWidgetItem(str(shorty)))
        
    def onpushButtonCancelRule_click(self):
        [(idOne,)]=self.makeSelectQuery("select N from person where sirname='"+self.comboBoxFirstEmployee.currentText()+"' ;")
        [(idTwo,)]=self.makeSelectQuery("select N from person where sirname='"+self.comboBoxSecondEmployee.currentText()+"' ;")
        for i in range(self.tableWidgetNCM.rowCount()):
            if self.tableWidgetNCM.horizontalHeaderItem(i).text()==self.comboBoxFirstEmployee.currentText():
                idOneTable=i
            if self.tableWidgetNCM.horizontalHeaderItem(i).text()==self.comboBoxSecondEmployee.currentText():
                idTwoTable=i
        if (idOne!=idTwo) and self.makeSelectQuery('SELECT blockingRule FROM notCrossingMatrix where id='+str(idOne)+
                ' and blokingId='+str(idTwo)+';'):
            self.makeChangingQuery("DELETE FROM notCrossingMatrix WHERE id = '"+
                        str(idOne)+"' AND  blokingId = '"+str(idTwo)+"' ;")
            self.makeChangingQuery("DELETE FROM notCrossingMatrix WHERE id = '"+
                        str(idTwo)+"' AND  blokingId = '"+str(idOne)+"' ;")
            self.tableWidgetNCM.setItem(idOneTable,idTwoTable,QTableWidgetItem(""))
            self.tableWidgetNCM.setItem(idTwoTable,idOneTable,QTableWidgetItem(""))


class ExampleApp(QtWidgets.QMainWindow, AdUi.Ui_MainWindow):
    
    conn = 0
    columnsInYear=0
    rowsForEmployees=0
    virtualGrid=[]
    currentEmployeeId=0
    currentNumRest=0
    
    #rules using global variables
    rulesUseDict={'usingRulePersentInMonth':0,
                  'usingRuleManagersPersentInMonth':0,
                  'usingRuleCrossInNCMatrix':0,
                  'notifyPersentExceed':0,
                  'notifyManagersPersentExceed':0,
                  'percent':20,
                  'percentForManagers':8,
                  'gammaParametr':0.0005}
    
    months=('январь','февраль','март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь')
    
    monthsStartingCounter=[0,0,0,0,0,0,0,0,0,0,0,0]
    monthsStartingManagerCounter=[0,0,0,0,0,0,0,0,0,0,0,0]
    def resetMonthCounters(self):
        
        for i in range (12):
            self.monthsStartingCounter[i]=0
            self.monthsStartingManagerCounter[i]=0
        #print('coutersAreReseted',self.monthsStartingCounter,self.monthsStartingManagerCounter)    
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setOnLoad()
        
    def getYearsInControl(self):
        index=self.comboBoxYear.currentIndex()
        if index<0:
            index=0
        #print(index)
        self.comboBoxYear.clear()
        for (row,) in self.makeSelectQuery("Select year from p_rating group by year order by year desc;"):
           self.comboBoxYear.addItem(str(row))
        self.comboBoxYear.setCurrentIndex(index)   
    
    def setOnLoad(self):
        self.conn = sqlite3.connect("rest.db")
        #for (row,) in self.makeSelectQuery("Select year from p_rating group by year order by year desc;"):
        #    self.comboBoxYear.addItem(str(row))
        #self.setCurrentYear()
        self.getYearsInControl()
        year=self.comboBoxYear.currentText()
        self.labelBanner.setText("Выбор отпуска на "+str(int(self.comboBoxYear.currentText())+1)+" год")
        self.setParamsFromStore(year)        
        self.dateEdit.setDate(QDate(int(year)+1,1,1))
        self.horizontalSliderNumParts.valueChanged.connect(self.lcdNumberNP.display) 
        self.horizontalSliderRestLength.valueChanged.connect(self.lcdNumberLength.display) 
        self.horizontalSliderRestWayLength.valueChanged.connect(self.lcdNumberWay.display)
        self.groupBoxWay.toggled.connect(self.waySliderHandler)
        self.pushButtonSetRest.clicked.connect(self.onButtonSetRest_click)
        self.tableWidget.cellClicked.connect(self.onTableClick)
        self.actionDelAll.triggered.connect(self.dellAll)
        self.actionNotCrossingMatrix.triggered.connect(self.showNCMatrix)
        self.actionOptions.triggered.connect(self.showPropertys)
        self.actionChangeOneNumRests.triggered.connect(self.showNRestsDialog)
        self.actionDelOneRest.triggered.connect(self.showDelOneDialog)
        self.actionChangeOneRest.triggered.connect(self.showChangeDialog)
        self.actionPreShowGraph.triggered.connect(self.showHtmlView)
        self.actionSaveGraph.triggered.connect(self.saveGraph)
        self.actionSaveExcelView.triggered.connect(self.saveExcelView)
        self.actionListsAndRatings.triggered.connect(self.showListsAndRatings)
        self.comboBoxYear.activated.connect(self.onYearChanged)
        self.paintGrid(year)
        self.getNextEmployeeToChoose(year)
    
    def onYearChanged(self):
        self.setParamsFromStore(self.comboBoxYear.currentText()) 
        
        self.paintGrid(self.comboBoxYear.currentText())
        self.pushButtonSetRest.setEnabled(True)
        self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
        self.labelBanner.setText("Выбор отпуска на "+str(int(self.comboBoxYear.currentText())+1)+" год")
        
    
    def getNextEmployeeToChoose(self, year):
        
        def setUiEmployeeToChose(name,totalNumRests, futureNumRest, employeeId):
            sql=("select REST_NUMBER from P_REST_NUM where N$person = "+ str(employeeId)+
                " AND YEAR = "+str(1+int(year))+";")
            #print(sql)
            res=self.makeSelectQuery(sql)
            #print(res)
            if res:
                [(res,)]=res
                #print(res)
                self.horizontalSliderNumParts.setSliderPosition(res)
                self.groupBoxNumParts.setEnabled(False)
            else:
                self.groupBoxNumParts.setEnabled(True)
                #print('enabled')
                self.horizontalSliderNumParts.setSliderPosition(1)
            self.labelName.setText(name)
            self.pushButtonSetRest.setEnabled(True)
            self.horizontalSliderRestLength.setSliderPosition(0)
            self.groupBoxWay.setChecked(False)
            
            
            if totalNumRests: self.horizontalSliderNumParts.setSliderPosition(totalNumRests)
            self.statusBar.showMessage("Сотрудник "+name+" должен выбрать "+str(futureNumRest)+
                    " часть отпуска")
            
            
        
        sql=("select s1.N, s1.sirname, s1.Num, s1.REST_NUMBER, s1.Level , sum(s2.RATING) from( select Person.N, Person.sirname, p_rest_num.REST_NUMBER, person.Level ,count(1) as Num from person left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+
             str(1+int(year))+" ) left join p_rests on (person.n=p_rests.n$person and p_rests.year ="+
             str(1+int(year))+" ) group by person.n having person.Level>1 ) as s1 left join (select * from p_rating where year between "+
             str(int(year)-nYearsDepth+1)+" and "+year+
             " ) as s2 on S1.n=s2.n$person group by s2.n$person ORDER BY s1.Level DESC, sum(s2.rating) DESC;")
        #print(sql)
        res =  self.makeSelectQuery(sql)
        #print(res)
        for (employeeId,employee,currentNumRest, totalNumRests, employeeLevel, emplRating) in res:
            i= 1 if not totalNumRests else currentNumRest+1 # current num rest fo r emmployee choosing
            if not totalNumRests or totalNumRests>=i:
                setUiEmployeeToChose(employee,totalNumRests,i,employeeId)
                self.currentEmployeeId=employeeId
                #print(self.currentEmployeeId)
                #print(currentNumRest)
                self.currentNumRest=i
                #print(self.currentNumRest)
                return employeeId
            #else:
                #something to do self.pushButtonSetRest.enabled=False
            #    self.statusBar.showMessage("Сотрудники 1 закончились")
                
        epochOfRestChoose=1
        #print('1 :',epochOfRestChoose)
        while True:
            sql=("select s1.N, s1.sirname, s1.Num, s1.REST_NUMBER, s1.Level , sum(s2.RATING) from( select Person.N, Person.sirname,p_rest_num.REST_NUMBER, person.Level ,count(1) as Num from person left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+
                   str(1+int(year))+" ) left join p_rests on (person.n=p_rests.n$person and p_rests.year ="+
                   str(1+int(year))+" ) group by person.n having person.Level<=1 )AS s1 left join (select * from p_rating where year between "+
                   str(int(year)-nYearsDepth+1 )+" and "+str(year)+
                   " ) as s2 on s1.n=s2.n$person group by s2.n$person  ORDER BY s1.Level DESC, sum(s2.rating) DESC;")
            res =  self.makeSelectQuery(sql)
            #print(sql)
            #print(res)
            for (employeeId,employee,currentNumRest, totalNumRests, employeeLevel, emplRating) in res:
                #print(employeeId,employee,currentNumRest, totalNumRests, employeeLevel, emplRating)
                i= 1 if not totalNumRests else currentNumRest+1
                #print('next rest',i)
                #print('epoch in cicle',epochOfRestChoose)
                if not totalNumRests or (totalNumRests>=i and i==epochOfRestChoose):
                    setUiEmployeeToChose(employee,totalNumRests,i,employeeId)
                    self.currentEmployeeId=employeeId
                    #print(self.currentEmployeeId)
                    #print(currentNumRest)
                    self.currentNumRest=i
                    #print(self.currentNumRest)
                    #print('out for')
                    return employeeId
                #else:
                    #set all clean self.pushButtonSetRest.enabled=False
                    #self.statusBar.showMessage("Сотрудники 0 закончились")
            sql_epochs="select MAX(p_rest_num.REST_NUMBER) from p_rest_num where p_rest_num.year ="+str(1+int(year))+";"
            [(numOfEpochsForChoose,)]=self.makeSelectQuery(sql_epochs)
            #print ('numOfEpochsForChoose',numOfEpochsForChoose)
            
            epochOfRestChoose+=1
            #print('epoch after inc :',epochOfRestChoose)
            #HERE MODIFIED!!!!(if epochOfRestChoose>=numOfEpochsForChoose :)
            if epochOfRestChoose>numOfEpochsForChoose :
                #print('out while')
                break
        self.statusBar.showMessage("Выбор отпусков закончен")
        self.pushButtonSetRest.setEnabled(False)
        self.labelName.setText("")
        return 0
    
    def paintGrid(self, year):
        self.virtualGrid=[]
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.resetMonthCounters()
        self.paintCalendar(int(year)+1)
        self.paintEmployeeList(year)
        restList=self.makeRestList(year)
        #print(restList)
        for rest in restList:
            (level,restNumberTotal, numRestCurrent, date, month, dayFromFirstJan, length, wayLength, employeeId) = rest
            self.putRestInVirtualGrid(dayFromFirstJan, length, wayLength, employeeId, month)
            
        self.printVirtualGrid()
        delegate=self.headerDelegate()
        self.tableWidget.setItemDelegate(delegate)
        #self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.resizeRowsToContents()
    
    class headerDelegate(QStyledItemDelegate):
        def paint(self,painter,option,index):
            tupleForRow = index.model().data(index,Qt.DecorationRole)
            if tupleForRow is None:
                super().paint(painter,option, index)
                return
            
            rect=option.rect
            painter.save()
            
            painter.setPen(QtGui.QColor('red'))
            painter.drawText(rect,Qt.AlignRight,str(tupleForRow.count('red')))
            
            rect=QRect(rect.x(),rect.y(), rect.width()-15, rect.height())
            painter.setPen(QtGui.QColor('orange'))
            painter.drawText(rect,Qt.AlignRight,str(tupleForRow.count('yellow')))
            
            rect=QRect(rect.x(),rect.y(), rect.width()-15, rect.height())
            painter.setPen(QtGui.QColor('green'))
            painter.drawText(rect,Qt.AlignRight,str(tupleForRow.count('green')))
            
            painter.restore()
            super().paint(painter, option, index)
            
        
    def printVirtualGrid(self):
        for i in range(self.rowsForEmployees):
            self.tableWidget.item(i+3,0).setData(Qt.DecorationRole,None)
            for j in range(1,self.columnsInYear):
                dictionary=self.virtualGrid[i][j]
                if (dictionary):
                    if not self.tableWidget.item(i+3,0).data(Qt.DecorationRole):
                        tupleForRow=()
                        tupleForRow+=(dictionary['color'],)
                    else:
                        tupleForRow=self.tableWidget.item(i+3,0).data(Qt.DecorationRole)+(dictionary['color'],)
                        
                    self.tableWidget.item(i+3,0).setData(Qt.DecorationRole,tupleForRow)
                    self.tableWidget.setItem(i+3,j,QTableWidgetItem(''))
                    self.tableWidget.item(i+3,j).setBackground(QtGui.QColor(dictionary['color'])) 
                else: 
                    self.tableWidget.setItem(i+3,j,QTableWidgetItem(''))
                    self.tableWidget.item(i+3,j).setBackground(QtGui.QColor('white')) 
    
    def putRestInVirtualGrid( self, dayFromFirstJan, length, wayLength, employeeId, month=False, delete=False):
        
        def findRow(employeeId):
            #print(self.virtualGrid)
            for i in range(len(self.virtualGrid)):
                #print('each',i)
                if self.virtualGrid[i][0]==employeeId:
                    #print('match',i)
                    return i
                
        #(level,restNumberTotal, numRestCurrent, date, month, dayFromFirstJan, length, wayLength, employeeId) = rest
        #print(level,restNumberTotal, numRestCurrent, date, month, dayFromFirstJan, length, wayLength, employeeId)
        #print( dayFromFirstJan, length, wayLength, employeeId)
        row=findRow(employeeId)
        #print(employeeId)
        #print(row)
        rulesMatchSet=set()
        
        #Number of employees starting in one month section
        
        if month and not delete:
            percent=self.rulesUseDict['percent']
            #print("percent:",percent)
            percentForManagers=self.rulesUseDict['percentForManagers']
            #print("percentForManagers:",percentForManagers)
            month=int(month)-1
            level=self.returnLevel(employeeId)
            self.monthsStartingCounter[month]+=1
            if level>0:self.monthsStartingManagerCounter[month]+=1
            #print('month,level,self.monthsStartingCounter,self.monthsStartingManagerCounter:',month,level,self.monthsStartingCounter,self.monthsStartingManagerCounter) 
            if (self.rulesUseDict['usingRulePersentInMonth']) and (self.monthsStartingCounter[month]>self.rowsForEmployees*percent/100):
                rulesMatchSet.add('percenInMonthRule')
                self.monthsStartingCounter[month]-=1
                #print('self.monthsStartingCounter[month]:',self.monthsStartingCounter[month])
            if (self.rulesUseDict['usingRuleManagersPersentInMonth'])and(self.monthsStartingManagerCounter[month]>self.rowsForEmployees*percentForManagers/100):
                rulesMatchSet.add('percenManagersInMonthRule')    
                self.monthsStartingManagerCounter[month]-=1
                #print('self.monthsStartingManagerCounter[month]',self.monthsStartingManagerCounter[month])
        
        dayIter=0
        if (wayLength):
            for i in range(wayLength//2):
                if int(dayFromFirstJan)+dayIter<self.columnsInYear:
                    if not delete : 
                        dayDict=self.chekRules(employeeId,row,int(dayFromFirstJan)+dayIter+virtGridShift,'way')
                        #print(dayDict['error'])
                        if 'error' in dayDict.keys(): rulesMatchSet.add(dayDict['error'])
                        if 'percenInMonthRule' in rulesMatchSet:dayDict['color']='red'
                        if 'percenManagersInMonthRule' in rulesMatchSet:dayDict['color']='red'
                        self.virtualGrid[row][int(dayFromFirstJan)+dayIter+virtGridShift]=dayDict
                    else:
                        self.virtualGrid[row][int(dayFromFirstJan)+dayIter+virtGridShift]=None
                    dayIter=dayIter+1
        if (length):
            for i in range(length):
                if int(dayFromFirstJan)+dayIter<self.columnsInYear:
                    if not delete : 
                        dayDict=self.chekRules(employeeId,row,int(dayFromFirstJan)+dayIter+virtGridShift,'day')
                        if 'error' in dayDict.keys(): rulesMatchSet.add(dayDict['error'])
                        if 'percenInMonthRule' in rulesMatchSet:dayDict['color']='red'
                        if 'percenManagersInMonthRule' in rulesMatchSet:dayDict['color']='red'
                        self.virtualGrid[row][int(dayFromFirstJan)+dayIter+virtGridShift]=dayDict
                    else:
                        self.virtualGrid[row][int(dayFromFirstJan)+dayIter+virtGridShift]=None
                    dayIter=dayIter+1
        if (wayLength):
            for i in range(wayLength//2):
                if int(dayFromFirstJan)+dayIter<self.columnsInYear:
                    if not delete : 
                        dayDict=self.chekRules(employeeId,row,int(dayFromFirstJan)+dayIter+virtGridShift,'way')
                        if 'error' in dayDict.keys(): rulesMatchSet.add(dayDict['error'])
                        if 'percenInMonthRule' in rulesMatchSet:dayDict['color']='red'
                        if 'percenManagersInMonthRule' in rulesMatchSet:dayDict['color']='red'
                        self.virtualGrid[row][int(dayFromFirstJan)+dayIter+virtGridShift]=dayDict
                    else:
                        self.virtualGrid[row][int(dayFromFirstJan)+dayIter+virtGridShift]=None
                    dayIter=dayIter+1
        
        return rulesMatchSet    
    
    def returnLevel(self,employeeId):
        sql="select level from person where N="+str(employeeId)
        [(level,)]=self.makeSelectQuery(sql)
        return level
    
    
    def chekRules(self,employeeId,row,day,dayWayProp):
        percent=self.rulesUseDict['percent']
        level=self.returnLevel(employeeId)    
        #paint red anyway, notify if setted
        if not  self.percentRule(day,row,percent): 
            ret={'color':'red', 'level':str(level), 'id':str(employeeId)}
            if self.rulesUseDict['notifyPersentExceed']:
                ret['error']='percentRule'
            return ret
            
        #paint red anyway, notify if setted
        
        if self.rulesUseDict['notifyManagersPersentExceed']:
            if not  self.percentRuleManagers(day,row,percent,employeeId): 
                ret={'color':'red', 'level':str(level), 'id':str(employeeId)}
            
                ret['error']='percentRuleManagers'
                return ret
        
        
        if (self.rulesUseDict['usingRuleCrossInNCMatrix'])and(self.isCrossInNCMatrixRule(day,row,employeeId)):
            return {'color':'red', 'error':'crossInNCMatrix', 'level':str(level), 'id':str(employeeId)}
            
        if dayWayProp=='way': return {'color':'yellow','level':str(level), 'id':str(employeeId)}
        else: return {'color':'green','level':str(level), 'id':str(employeeId)}
    
    def percentRule(self, day,row,percent):
        count=1
        #print('row:',row)
        #modified here change row fo rowsForEmployees
        for i in range(self.rowsForEmployees):
            #print('vG:',self.virtualGrid[i][day])
            if self.virtualGrid[i][day] :
                count+=1
        #print('count:',count)
        #print('persent:',self.rowsForEmployees*percent/100)
        if count>self.rowsForEmployees*percent/100:
            return False
        return True
        
    def percentRuleManagers(self, day,row,percent,employeeId):
        level=self.returnLevel(employeeId)
        percentForManagers=self.rulesUseDict['percentForManagers']
        #print ("levelM:",level)
        if level:
            count=1
            #print('rowM:',row)
            #modified here change row fo rowsForEmployees
            for i in range(self.rowsForEmployees):
                #print('vGM:',self.virtualGrid[i][day])
                if self.virtualGrid[i][day]:
                    #print('levelInGrid:',self.virtualGrid[i][day]['level'])
                    if int(self.virtualGrid[i][day]['level'])>0 :
                        count+=1
            #print('countM:',count)
            #print('persentM:',self.rowsForEmployees*percentForManagers/100)
            if count>self.rowsForEmployees*percentForManagers/100:
                return False
        return True
    
    def isCrossInNCMatrixRule(self,day,row,employeeId):
        for i in range(row):
            #print('vG:',self.virtualGrid[i][day])
            if self.virtualGrid[i][day] :
                res=self.makeSelectQuery("SELECT rule  FROM notCrossingMatrix join NCMatrixRules on notCrossingMatrix.blockingRule=NCMatrixRules.ID "+
                        "where notCrossingMatrix.id = "+str(employeeId)+
                        " and notCrossingMatrix.blokingId="+self.virtualGrid[i][day]['id']+" ;")
                if res :        
                    [(blockingRule)]=res
                    #print('blockingrule:',blockingRule)
                    return blockingRule
        return False    
        
    def makeRestList(self, year):
        sql=("select Person.level , P_REST_NUM.REST_NUMBER, P_rests.N_rest, P_rests.date, strftime('%m',P_rests.date) as month, (julianday(P_rests.date) - julianday('" +
            str(1+int(year))+
            "-01-01')) as day, P_rests.length, P_rests.way_length, Person.N From person left join (select * from p_rating where year between "+
            str(int(year)-nYearsDepth+1)+" and "+str(year)+
            " ) as s2 on person.n=s2.n$person left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+
            str(1+int(year))+
            " ) left join p_rests on (person.n=p_rests.n$person and p_rests.year ="+str(1+int(year))+
            " ) where Person.level>1  group by  P_rests.date, person.n ORDER BY person.Level DESC, sum(s2.rating) DESC, P_rests.N_rest ;")
            
        res =  self.makeSelectQuery(sql)
        
        sql=("select Person.level , P_REST_NUM.REST_NUMBER, P_rests.N_rest, P_rests.date, strftime('%m',P_rests.date) as month, (julianday(P_rests.date) - julianday('"+str(1+int(year))+
            "-01-01')) as day, P_rests.length, P_rests.way_length, Person.N From person left join (select * from p_rating where year between "+
            str(int(year)-nYearsDepth+1)+" and "+str(year)+
            "  ) as s2 on person.n=s2.n$person  left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+
            str(1+int(year))+" ) left join p_rests on (person.n=p_rests.n$person and p_rests.year ="+
            str(1+int(year))+" ) where Person.level<=1 group by P_rests.date, person.n ORDER BY P_rests.N_rest, person.Level DESC, sum(s2.rating) DESC ;")
      
        res=res + self.makeSelectQuery(sql)
        #level,restNumberTotal, numRestCurrent, date, month, dayFromFirstJan, length, wayLength, employeeId
        return res
        
        
    def paintEmployeeList(self, year):
        sql=("select s_per.sirname,round(sum(s_rate.rating),3),s_per.N from ((select * from person) as s_per left join (select * from p_rating where year between "+
            str(1+int(year)-nYearsDepth)+" and "+ str(year) +
            " ) as s_rate on s_per.n=s_rate.n$person) group by s_rate.n$person ORDER BY s_per.Level DESC, sum(s_rate.rating) DESC;")
        #print(sql)
        res =  self.makeSelectQuery(sql)
        #print(res)
        rowsForEmployees=len(res)
        self.tableWidget.setRowCount(3+rowsForEmployees)
        i=3
        for (emplyee,emplRating,employeeId) in res:
            self.tableWidget.setVerticalHeaderItem(i,QTableWidgetItem(emplyee))
            self.tableWidget.setItem(i,0,QTableWidgetItem(str(emplRating)))
            L=[]
            L.append(employeeId)
            for c in range(self.columnsInYear):
                L.append(None)
            self.virtualGrid.append(L)           
            self.tableWidget.setRowHeight(i,20)
            i=i+1
        self.rowsForEmployees=rowsForEmployees
        
	
        
    def paintCalendar(self, year):
        sql="select  strftime('%w','"+str(year)+"-01-01'),(julianday('"+str(year)+"-03-01') - julianday('"+str(year)+"-02-01')) as febday;"
        #print(sql)
        
        [(firstJanDayOfWeek,febNumOfDays)]=self.makeSelectQuery(sql)
        #print(febNumOfDays)
        #print(firstJanDayOfWeek)
        self.tableWidget.setRowCount(3)
        columnsInYear=366-27+int(febNumOfDays)
        self.tableWidget.setColumnCount(columnsInYear)
        self.tableWidget.horizontalHeader().hide()
        monthLengthList=(31,int(febNumOfDays),31,30,31,30,31,31,30,31,30,31)
        weekdayLbl=('ВС','ПН','ВТ','СР','ЧТ','ПТ','СБ')
        months=('январь','февраль','март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь')
        i=1
        counter=0
        savedMonthBorder=1
        for monthLength in monthLengthList:
            for day in range(1,monthLength+1):
                weekday=(i-1+int(firstJanDayOfWeek))%7
                self.tableWidget.setItem(0,i,QTableWidgetItem(str(day)))
                self.tableWidget.setItem(1,i,QTableWidgetItem(weekdayLbl[weekday]))
                self.tableWidget.setColumnWidth(i,25)
                i=i+1
            self.tableWidget.setSpan(2,savedMonthBorder,1,i-savedMonthBorder)    
            self.tableWidget.setItem(2,savedMonthBorder,QTableWidgetItem(months[counter]))
            savedMonthBorder=i
            counter=counter+1
        for row in range(3):
            self.tableWidget.setVerticalHeaderItem(row,QTableWidgetItem(""))
            self.tableWidget.setRowHeight(row,20)
        self.columnsInYear=columnsInYear
        #print(self.columnsInYear)

    def setParamsFromStore(self,year):
        res = self.makeSelectQuery("SELECT parametr,value FROM pyParams where year="+str(year)+";")
        if not res:
            self.rulesUseDict['usingRulePersentInMonth']=0
            self.rulesUseDict['usingRuleManagersPersentInMonth']=0
            self.rulesUseDict['usingRuleCrossInNCMatrix']=0
            self.rulesUseDict['notifyPersentExceed']=0
            self.rulesUseDict['notifyManagersPersentExceed']=0
            self.rulesUseDict['percent']=20
            self.rulesUseDict['percentForManagers']=8
            self.rulesUseDict['gammaParametr']=0.0005
            
            #print('rules nuled',self.rulesUseDict)
            for rule in self.rulesUseDict:
                #print (rule)
                self.makeChangingQuery("INSERT INTO pyParams ( parametr, value, year ) VALUES ( '"+
                        rule+"','"+
                        str(self.rulesUseDict[rule])+"','"+
                        str(year)+"');")
        else:
            for (rule,value) in res:
                self.rulesUseDict[rule]=value
                #print(rule, value)
        
    def makeSelectQuery(self,Query):
        cursor = self.conn.cursor()
        sql = Query
        cursor.execute(sql)
        return cursor.fetchall() # or use fetchone()
    
    def makeChangingQuery(self,Query):    
        cursor = self.conn.cursor()
        sql = Query
        try:
            cursor.executescript(sql)
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else:
            self.conn.commit()
        
        
    
    def onButtonSetRest_click(self):
        #print("clicked!",self.tryRestInVirtualGrid())
        if self.tryRestInVirtualGrid():
            self.putRestInDb(int(self.comboBoxYear.currentText()))
            self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
            
    def onTableClick(self,row,column):
        #print ("Click on " + str(row) + " " + str(column))
        #self.dateEdit.setDate(int(self.comboBoxYear.currentText())+1,self.months.index(,self.tableWidget.item(3,column).text(),self.tableWidget.item(0,column).text()))
        self.dateEdit.setDate(QDate(int(self.comboBoxYear.currentText())+1,1,1).addDays(column-1))
        #print(self.tableWidget.item(2,column).text())
    
    def dellAll(self):
        if QMessageBox.question(self, "Предупреждение", "Все отпуска всех сотрудников будут сброшены, вы уверены что хотите начать заполнение таблицы заново?"
                , buttons=QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No),
                defaultButton=QMessageBox.NoButton)==QMessageBox.Yes: 
            sql= ("DELETE FROM P_RESTS WHERE ( Year = " + str(int(self.comboBoxYear.currentText())+1) + ") ;"+
                "DELETE FROM P_REST_NUM WHERE ( Year = " + str(int(self.comboBoxYear.currentText())+1) + ") ;")
            self.makeChangingQuery(sql)
            #self.virtualGrid=[]
            #self.resetMonthCounters()
            self.paintGrid(self.comboBoxYear.currentText())
            self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
    
    def showNCMatrix(self):
        self.NCMatrixFrame = NCMatrixclass()
        self.NCMatrixFrame.show()
        self.paintGrid(self.comboBoxYear.currentText())
        self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
        
    def showPropertys(self):
        self.PropertysWindow=PropertysWidget.PropertysWidget(self.comboBoxYear.currentText())
        self.PropertysWindow.exec()
        
        self.setParamsFromStore(self.comboBoxYear.currentText())
        self.paintGrid(self.comboBoxYear.currentText())
        self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
        
    def showNRestsDialog(self):
        self.nRestsWindow = nRestsDialogWindow.nRestsWindow(self.comboBoxYear.currentText())
        self.nRestsWindow.exec()
        
        self.paintGrid(self.comboBoxYear.currentText())
        self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
        
    def showDelOneDialog(self):
        self.dellRestsWindow = dellRestsDialogWindow.dellRestsWindow(self.comboBoxYear.currentText())
        self.dellRestsWindow.exec()
        
        self.paintGrid(self.comboBoxYear.currentText())
        self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
    
    def showChangeDialog(self):
        self.changeRestWindow = changeDialogClass.changeRestWindow(self.comboBoxYear.currentText())
        self.changeRestWindow.exec()
        
        self.paintGrid(self.comboBoxYear.currentText())
        self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
        
    def showHtmlView(self):
        page=makePage(self.comboBoxYear.currentText(),nYearsDepth)
        #print(page)
        if page :
            self.htmlViewWindow=htmlViewClass.htmlViewWindow(page)
            self.htmlViewWindow.exec()
    

    def saveGraph(self):
        page=makePage(self.comboBoxYear.currentText(),nYearsDepth)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Сохранить в файл","График отпусков_"+str(1+int(self.comboBoxYear.currentText()))+".html","HTML (*.html)","", options=options)
        if fileName:
            file=QFile(fileName)
            if file.exists():
                file.remove()
            file=open(fileName,'w')
            file.write(page)
            file.close()
    
    def saveExcelView(self):
        #print(self.virtualGrid)
        page=""
        playceholder={'yellow':'д','green':'о','red':'о'}
        for r in range(3):
            if self.tableWidget.verticalHeaderItem(r):
                page+=self.tableWidget.verticalHeaderItem(r).text()
            page+=";"    
            for c in range(1,self.tableWidget.columnCount()):
                if self.tableWidget.item(r,c):
                    page+=self.tableWidget.item(r,c).text()
                page+=";"    
            page+="\n"    
        for r in range(3, self.tableWidget.rowCount()):
            #print(r)
            #print(self.tableWidget.verticalHeaderItem(r))
            if self.tableWidget.verticalHeaderItem(r):
                #print(self.tableWidget.verticalHeaderItem(r).text())
                page+=self.tableWidget.verticalHeaderItem(r).text()
            page+=";"
            for c in range(1,self.tableWidget.columnCount()):
                #print(self.virtualGrid[r-3][c])
                if self.virtualGrid[r-3][c]:
                    #print(playceholder[self.virtualGrid[r-3][c]['color']])
                    page+=playceholder[self.virtualGrid[r-3][c]['color']]
                page+=";"    
            page+="\n"      
            
        #print(page)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Сохранить в файл","Представление_года_"+str(1+int(self.comboBoxYear.currentText()))+".csv","CSV (*.csv)","", options=options)
        if fileName:
            file=QFile(fileName)
            if file.exists():
                file.remove()
            file=open(fileName,'w')
            file.write(page)
            file.close()  

    def showListsAndRatings(self):
        #print("showListsAndRatings")
        self.listsAndRatingsWindow=listsAndRatingsClass.listAndReitingsWindow(self.comboBoxYear.currentText(),nYearsDepth,self.rulesUseDict['gammaParametr'])
        self.listsAndRatingsWindow.exec()
        
        self.getYearsInControl()
        self.paintGrid(self.comboBoxYear.currentText())
        self.getNextEmployeeToChoose(self.comboBoxYear.currentText())
        
    def waySliderHandler(self, checked):
        if not checked:
            self.horizontalSliderRestWayLength.setSliderPosition(0)
    
    def putRestInDb(self,year):
    #print(year)
        sql=("INSERT INTO P_RESTS (N$PERSON, YEAR, N_REST, DATE,  LENGTH, WAY_LENGTH) VALUES  ("+
                str(self.currentEmployeeId)+","+str(1+int(year))+","+str(self.currentNumRest)+",'"+
                str(self.dateEdit.date().toString("yyyy-MM-dd"))+"',"+
                str(self.horizontalSliderRestLength.value())+","+str(self.horizontalSliderRestWayLength.value())+");")
        #print(sql)
        self.makeChangingQuery(sql)
        sql=("select count(REST_NUMBER) from P_REST_NUM where N$person = "+ str(self.currentEmployeeId)+
                " AND YEAR = "+str(1+int(year))+";")
        #print(sql)
        #print(self.makeSelectQuery(sql))
        [(res,)]=self.makeSelectQuery(sql)
        #print(res)
        if not res:
            sql=("INSERT INTO P_REST_NUM (N$PERSON, YEAR, REST_NUMBER) VALUES ("+
                    str(self.currentEmployeeId)+","+str(1+int(year))+","+ str(self.horizontalSliderNumParts.value())+");")
            #print(sql)
            self.makeChangingQuery(sql)
        
        
    def tryRestInVirtualGrid(self):
        way=''
        if self.dateEdit.date().year() != int(self.comboBoxYear.currentText())+1:
            month=self.dateEdit.date().month()
            day=self.dateEdit.date().day()
            self.dateEdit.setDate(QDate(int(self.comboBoxYear.currentText())+1,month,day))
            #print("year edited")
        if self.horizontalSliderRestWayLength.value() % 2:
            msg = QMessageBox.information(self, "Ошибка", "Выбрано нечетное количество дней")
            return False
        if self.horizontalSliderRestWayLength.value() :
            way = " и " + str(self.horizontalSliderRestWayLength.value())+ " суток дороги"
        
        msg=("Вы выбрали отпуск в количестве "+str(self.horizontalSliderRestLength.value())+
                " суток с "+str(self.dateEdit.date().toString("dd.MM.yyyy"))+ way)
                
        if QMessageBox.question(self, "Вопрос", msg
                , buttons=QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No),
                defaultButton=QMessageBox.NoButton)==QMessageBox.Yes: 
            #(dayFromFirstJan, length, wayLength, employeeId)
            #print(self.currentEmployeeId, "fuck")
            #print(str(self.dateEdit.date().toString("dd.MM.yyyy")))
            #print(self.dateEdit.date().dayOfYear())
            rulesErrorSet=self.putRestInVirtualGrid(self.dateEdit.date().dayOfYear()-1,
                    self.horizontalSliderRestLength.value(),
                    self.horizontalSliderRestWayLength.value(),
                    self.currentEmployeeId,
                    self.dateEdit.date().month())
            
            #remove this
            #print(rulesErrorSet)
            #print(self.virtualGrid)
            self.printVirtualGrid()
            if(rulesErrorSet) :
                mStr=""
                for x in rulesErrorSet:
                    mStr+=rules[x]+", "
                msg=QMessageBox.information(self, "Ошибка", mStr )
                self.putRestInVirtualGrid(self.dateEdit.date().dayOfYear()-1,
                    self.horizontalSliderRestLength.value(),
                    self.horizontalSliderRestWayLength.value(),
                    self.currentEmployeeId,delete=True)
                #print(self.virtualGrid)
                
                return False
            return True
        return False
            
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()
    

    

if __name__ == '__main__':
    main()
