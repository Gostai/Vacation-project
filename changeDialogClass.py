import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
import changeDialogUi
import sqlite3

class changeRestWindow(QtWidgets.QDialog, changeDialogUi.Ui_Dialog):
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
        self.comboBoxPart.activated.connect(self.onPartChanged)
        self.horizontalSliderLength.valueChanged.connect(self.lcdNumberLength.display) 
        self.horizontalSliderWay.valueChanged.connect(self.lcdNumberWay.display)
        self.pushButtonOk.clicked.connect(self.onpushButtonOk_click)
        self.pushButtonCancel.clicked.connect(self.onpushButtonCancel_click)
        self.groupBoxWay.toggled.connect(self.waySliderHandler)
        self.dateEditStart.setDate(QDate(int(self.year)+1,1,1))
        res=self.makeSelectQuery("SELECT Person.SIRNAME  From person join p_rating on (person.n=p_rating.n$person and p_rating.year ="+str(self.year)+
            " )  ORDER BY Person.SIRNAME;")
        #print(res)
        for (name,) in res:
            self.comboBoxEmployee.addItem(str(name))
        self.setName(self.comboBoxEmployee.currentText())
    
    def waySliderHandler(self, checked):
        if not checked:
            self.horizontalSliderWay.setSliderPosition(0)

    
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
        global EmployeeN, nRests
        way=''
        if self.dateEditStart.date().year() != int(self.year)+1:
            month=self.dateEditStart.date().month()
            day=self.dateEditStart.date().day()
            self.dateEditStart.setDate(QDate(int(self.year)+1,month,day))
            #print("year edited")
        if self.horizontalSliderWay.value() % 2:
            msg = QMessageBox.information(self, "Ошибка", "Выбрано нечетное количество дней")
            return
        if self.horizontalSliderWay.value() :
            way = " и " + str(self.horizontalSliderWay.value())+ " суток дороги"
        nRest=self.comboBoxPart.currentText()
        if not nRest:
            nRest=1
        msg=("Вы выбрали отпуск в количестве "+str(self.horizontalSliderLength.value())+
                " суток с "+str(self.dateEditStart.date().toString("dd.MM.yyyy"))+ way)
                
        if QMessageBox.question(self, "Вопрос", msg
                , buttons=QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No),
                defaultButton=QMessageBox.NoButton)==QMessageBox.Yes: 
            SQLCheck=("select P_rests.date from  p_rests where year="+ str(1+int(self.year))+
                " and n_rest="+str(nRest)+" and N$person="+str(EmployeeN)+";")
            if self.makeSelectQuery(SQLCheck):
                print("updating...")
                SQL=( "Update P_RESTS SET DATE='"+
                str(self.dateEditStart.date().toString("yyyy-MM-dd"))+"', LENGTH="+
                str(self.horizontalSliderLength.value())+
                ", WAY_LENGTH="+str(self.horizontalSliderWay.value())+" where N$PERSON="+str(EmployeeN)+
                " and YEAR="+str(1+int(self.year))+
                " and N_REST="+str(nRest)+";")
            else:
                print("inserting...")
                SQL=( "INSERT INTO P_RESTS (N$PERSON, YEAR, N_REST, DATE,  LENGTH, WAY_LENGTH) VALUES  ("+
                str(EmployeeN)+","+str(1+int(self.year))+
                ","+str(nRest)+",'"+
                str(self.dateEditStart.date().toString("yyyy-MM-dd"))+"',"+
                str(self.horizontalSliderLength.value())+","+str(self.horizontalSliderWay.value())+");")
            #print(SQL)
            self.makeChangingQuery(SQL)
            
            #search for RestNum, if not add
            sql=("select Person.N , P_REST_NUM.REST_NUMBER From person join p_rating on (person.n=p_rating.n$person and p_rating.year ="+str(self.year)+
            " ) left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+str(1+int(self.year))+
            " ) where Person.n='"+ str(EmployeeN)+"' ;")
        
            print(sql)
            res=self.makeSelectQuery(sql)
            print(res)
            [(EmployeeN,nRests)]=res
            print(EmployeeN,nRests) 
            if not nRests:
                print('inserting Rests Number for '+str(1+int(self.year)))
                self.makeChangingQuery("INSERT INTO P_REST_NUM (N$PERSON, YEAR, REST_NUMBER) VALUES ( "+str(EmployeeN)+
                    ","+str(1+int(self.year))+",1 );")
            self.done(0)        
    
    def onpushButtonCancel_click(self):
        self.done(0)  
        
    def onNameChanged(self):
        self.setName(self.comboBoxEmployee.currentText())    
        
    def onPartChanged(self):
        self.setPart(self.comboBoxPart.currentText())
    
    def setPart(self, part):
        
        res=self.makeSelectQuery("select  strftime('%d',P_rests.date) as day, strftime('%m',P_rests.date) as month, "+
            #"(julianday(P_rests.date) - julianday('"+
            #str(1+int(self.year))+ "-01-01')) as fullday,"+
            " P_rests.length, P_rests.way_length"+
            #",strftime('%d', date(P_rests.date,'start of month','+1 month','-1 day')) as lastdayofmonth "+
            " from  p_rests where year="+
            str(1+int(self.year))+
            " and n_rest="+str(part)+
            " and N$person="+str(EmployeeN)+";")
        if res:
            [(day, month, length, way )]=res
            #print(res)
            #print(day, month, length, way)
            self.dateEditStart.setDate(QDate(int(self.year)+1,int(month),int(day)))
            self.horizontalSliderLength.setSliderPosition(int(length))
            if int(way):
                self.groupBoxWay.setChecked(True)
                self.horizontalSliderWay.setSliderPosition(int(way))
            else:
                self.groupBoxWay.setChecked(False)
    
    def setName(self,name):
        
        global EmployeeN, nRests
        sql=("select Person.N , P_REST_NUM.REST_NUMBER From person join p_rating on (person.n=p_rating.n$person and p_rating.year ="+str(self.year)+
            " ) left join p_rest_num on (person.n=p_rest_num.n$person and p_rest_num.year ="+str(1+int(self.year))+
            " ) where Person.SIRNAME='"+ name +"' ;")
        
        #print(sql)
        res=self.makeSelectQuery(sql)
        print(res)
        [(EmployeeN,nRests)]=res
        print(EmployeeN,nRests)
        self.comboBoxPart.clear()
        if nRests:
            for i in range(nRests):
                self.comboBoxPart.addItem(str(i+1))
            self.setPart(self.comboBoxPart.currentText())    
        else:
            self.comboBoxPart.addItem(str(1))