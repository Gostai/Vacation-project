import sys
from PyQt5 import QtWidgets

import nRestsUi
import sqlite3

class nRestsWindow(QtWidgets.QDialog, nRestsUi.Ui_Dialog):
    EmployeeN=0
    nRests=0
    def __init__(self,year):
        super().__init__()
        self.year=year
        self.setupUi(self)
        self.setOnLoad()
        
    def setNRestSlider(self,name):
        global EmployeeN,nRests
        sql=("select Person.N , P_REST_NUM.REST_NUMBER From person join p_rating on (person.n=p_rating.n$person and p_rating.year ="+str(self.year)+
            " ) left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+str(1+int(self.year))+
            " ) where Person.SIRNAME='"+ name +"' ;")
        
        print(sql)
        res=self.makeSelectQuery(sql)
        print(res)
        [(EmployeeN,nRests)]=res
        print(nRests)
        if nRests:
            self.horizontalSliderNumRests.setValue(nRests)
            self.lcdNumberNRest.display(nRests)
        else:
            self.horizontalSliderNumRests.setValue(1)
            self.lcdNumberNRest.display(1)
            
    def setOnLoad(self):
        self.conn = sqlite3.connect("rest.db")
        self.horizontalSliderNumRests.valueChanged.connect(self.lcdNumberNRest.display) 
        self.comboBoxEmployee.activated.connect(self.onNameChanged)
        self.pushButtonOk.clicked.connect(self.onpushButtonOk_click)
        self.pushButtonCancel.clicked.connect(self.onpushButtonCancel_click)
        res=self.makeSelectQuery("SELECT Person.SIRNAME  From person join p_rating on (person.n=p_rating.n$person and p_rating.year ="+str(self.year)+
            " )  ORDER BY Person.SIRNAME;")
        #print(res)
        for (name,) in res:
            self.comboBoxEmployee.addItem(str(name))
        self.setNRestSlider(self.comboBoxEmployee.currentText())
        
    def onNameChanged(self):
        self.setNRestSlider(self.comboBoxEmployee.currentText())
    
    def makeSelectQuery(self,Query):
        cursor = self.conn.cursor()
        sql = Query
        cursor.execute(sql)
        return cursor.fetchall() 
    
    def makeChangingQuery(self,Query):    
        cursor = self.conn.cursor()
        
        try:
            cursor.executescript(Query)
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else:
            self.conn.commit()
    
    def onpushButtonOk_click(self):
        nRests=self.horizontalSliderNumRests.value()
        sql="DELETE FROM P_RESTS WHERE ( Year = "+ str(1+int(self.year)) + " AND N$PERSON = "+ str(EmployeeN) +" AND N_Rest>"+ str(nRests)+" );"
        self.makeChangingQuery(sql)
        restProba=self.makeSelectQuery("SELECT REST_NUMBER FROM P_REST_NUM where N$PERSON="+str(EmployeeN)+" AND  YEAR="+str(1+int(self.year))+" ;")
        if restProba:
            sql=( "UPDATE  P_REST_NUM SET REST_NUMBER="+str(nRests) +
            " WHERE ( Year = "+ str(1+int(self.year)) + " AND N$PERSON = "+ str(EmployeeN) + " );")
        else:
            sql=( "INSERT INTO P_REST_NUM (N$PERSON, YEAR, REST_NUMBER) VALUES ( "+str(EmployeeN)+
                    ","+str(1+int(self.year))+","+str(nRests)+" );")
        self.makeChangingQuery(sql)
        self.done(0)        
    
    def onpushButtonCancel_click(self):
        self.done(0)      
           