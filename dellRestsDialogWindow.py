import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import dellRestsUi
import sqlite3

class dellRestsWindow(QtWidgets.QDialog, dellRestsUi.Ui_Dialog):
    
    EmployeeN=0
    nRests=0
    
    def __init__(self,year):
        super().__init__()
        self.year=year
        self.setupUi(self)
        self.setOnLoad()
        
    
            
    def setOnLoad(self):
        self.conn = sqlite3.connect("rest.db")
        self.comboBoxEmployee.activated.connect(self.onNameChanged)
        self.pushButtonDell.clicked.connect(self.onpushButtonDell_click)
        self.pushButtonCancel.clicked.connect(self.onpushButtonCancel_click)
        res=self.makeSelectQuery("SELECT Person.SIRNAME  From person join p_rating on (person.n=p_rating.n$person and p_rating.year ="+str(self.year)+
            " )  ORDER BY Person.SIRNAME;")
        #print(res)
        for (name,) in res:
            self.comboBoxEmployee.addItem(str(name))
        self.setName(self.comboBoxEmployee.currentText())
    
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
    
    def onpushButtonDell_click(self):
        if nRests:
            if QMessageBox.question(self, "Предупреждение", "Все отпуска ("+str(nRests)+
                    ") сотрудника будут сброшены, вы уверены что хотите продолжить?"
                    , buttons=QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No),
                    defaultButton=QMessageBox.NoButton)==QMessageBox.Yes:
                self.makeChangingQuery("DELETE FROM P_RESTS WHERE ( Year = "+ str(1+int(self.year)) +
                    " AND N$PERSON = "+ str(EmployeeN) + " );" ) 
                self.makeChangingQuery("DELETE FROM P_REST_NUM  WHERE ( Year = "+
                    str(1+int(self.year)) + " AND N$PERSON = "+ str(EmployeeN) + " );" )
            self.done(0)        
    
    def onpushButtonCancel_click(self):
        self.done(0)  
        
    def onNameChanged(self):
        self.setName(self.comboBoxEmployee.currentText())    
        
    def setName(self,name):
        
        global EmployeeN, nRests
        sql=("select Person.N , P_REST_NUM.REST_NUMBER From person join p_rating on (person.n=p_rating.n$person and p_rating.year ="+str(self.year)+
            " ) left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+str(1+int(self.year))+
            " ) where Person.SIRNAME='"+ name +"' ;")
        
        #print(sql)
        res=self.makeSelectQuery(sql)
        #print(res)
        [(EmployeeN,nRests)]=res
        #print(EmployeeN,nRests)