import sys
from PyQt5 import QtWidgets
import propertysDialogUi
import AppOtpusk
import sqlite3

class PropertysWidget(QtWidgets.QDialog, propertysDialogUi.Ui_Dialog):
    rulesUseDict={}
    
    def __init__(self, year):
        super().__init__()
        self.year=year
        self.setupUi(self)
        self.setOnLoad()
    
    def setOnLoad(self):
        self.conn = sqlite3.connect("rest.db")
        self.horizontalSliderPercent.valueChanged.connect(self.lcdNumberPercent.display) 
        self.horizontalSliderManagerPercent.valueChanged.connect(self.lcdNumberManagerPercent.display) 
        self.pushButtonOk.clicked.connect(self.onpushButtonOk_click)
        self.pushButtonCancel.clicked.connect(self.onpushButtonCancel_click) 
        res = self.makeSelectQuery("SELECT parametr,value FROM pyParams where year="+str(self.year)+";")
        if res:
            for (rule,value) in res:
                self.rulesUseDict[rule]=value
        #print(self.rulesUseDict)
        self.checkBoxPercentInMonth.setChecked(self.rulesUseDict['usingRulePersentInMonth'])
        self.checkBoxPercentManagerInMonth.setChecked(self.rulesUseDict['usingRuleManagersPersentInMonth'])
        self.checkBoxNCMatrix.setChecked(self.rulesUseDict['usingRuleCrossInNCMatrix']) 
        self.checkBoxPercent.setChecked(self.rulesUseDict['notifyPersentExceed'])
        self.checkBoxPercentManager.setChecked(self.rulesUseDict['notifyManagersPersentExceed'])
        self.horizontalSliderPercent.setValue(self.rulesUseDict['percent'])
        self.lcdNumberPercent.display(self.rulesUseDict['percent'])
        self.horizontalSliderManagerPercent.setValue(self.rulesUseDict['percentForManagers'])
        self.lcdNumberManagerPercent.display(self.rulesUseDict['percentForManagers'])
        self.doubleSpinBoxGamma.setValue(self.rulesUseDict['gammaParametr'])
        
        
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
            
    def onpushButtonOk_click(self):
        self.rulesUseDict['usingRulePersentInMonth']=int(self.checkBoxPercentInMonth.isChecked())
        self.rulesUseDict['usingRuleManagersPersentInMonth']=int(self.checkBoxPercentManagerInMonth.isChecked())
        self.rulesUseDict['usingRuleCrossInNCMatrix']=int(self.checkBoxNCMatrix.isChecked())
        self.rulesUseDict['notifyPersentExceed']=int(self.checkBoxPercent.isChecked())
        self.rulesUseDict['notifyManagersPersentExceed']=int(self.checkBoxPercentManager.isChecked())
        self.rulesUseDict['percent']=self.horizontalSliderPercent.value()
        self.rulesUseDict['percentForManagers']=self.horizontalSliderManagerPercent.value()
        self.rulesUseDict['gammaParametr']=self.doubleSpinBoxGamma.value()
        for rule in self.rulesUseDict:
            #print (rule)
            self.makeChangingQuery("UPDATE pyParams SET value = "+
            str(self.rulesUseDict[rule])+" WHERE parametr = '"+
            rule+"'  AND   year = "+
            str(self.year)+" ;")
        self.close()        
    
    def onpushButtonCancel_click(self):
        self.close()        
        
        
        
        