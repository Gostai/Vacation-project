import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem
from PyQt5.QtCore import QDate, Qt
import listAndReitingsUi
import sqlite3
#import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.model_selection import train_test_split
from sklearn import svm

class listAndReitingsWindow(QtWidgets.QDialog, listAndReitingsUi.Ui_Dialog):
   
   
    
    def __init__(self,year,nYearsDepth,gammaParametr):
        super().__init__()
        self.year=year
        self.nYearsDepth=nYearsDepth
        self.gammaParametr=gammaParametr
        self.daysForNewCoefs=np.zeros(2)
        self.coefsNew=np.zeros(2)
        self.setupUi(self)
        self.setOnLoad()
        
    
            
    def setOnLoad(self):
        self.conn = sqlite3.connect("rest.db")
        self.comboBoxChangeEmpl.activated.connect(self.setLevel)
        self.pushButtonDellOne.clicked.connect(self.dellOne)
        self.pushButtonAdd.clicked.connect(self.userAdd)
        self.pushButtonChange.clicked.connect(self.userChange)
        self.pushButtonDellAll.clicked.connect(self.dellAll)
        self.pushButtonCalcReite.clicked.connect(self.onCalcReiteClick)
        self.pushButtonCalcCoef.clicked.connect(self.onCalcCoefClick)
        self.pushButtonSaveCoef.clicked.connect(self.onSaveCoefClick)
        self.pushButtonSaveReit.clicked.connect(self.onSaveRateClick)
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.spinBoxYear.valueChanged.connect(self.onSpinYearChanged)
        self.spinBoxYear.setValue(int(self.year))
        self.loadCombos()
        self.tabChanged()
        #self.paintGraph(self.spinBoxYear.value())
    
    def loadCombos(self): 
        self.comboBoxChangeEmpl.clear()
        self.comboBoxDellEmpl.clear()
        res=self.makeSelectQuery("SELECT Person.SIRNAME  From person ORDER BY Person.SIRNAME;")
        #print(res)
        for (name,) in res:
            self.comboBoxChangeEmpl.addItem(str(name))
            self.comboBoxDellEmpl.addItem(str(name))
        self.setLevel()
    
    def setLevel(self):
        
        sql=("SELECT level  from person where sirname= '"+self.comboBoxChangeEmpl.currentText()+"' ;")
        #print(sql)
        res=self.makeSelectQuery(sql)
        if res :
            [(level,)]=res
            #print(level)
            self.spinBoxLevelChange.setValue(level)
    
    def userAdd(self):
        if not self.lineEdit.text():
            QMessageBox.information(self, "Ошибка", "Не указан сотрудник!")
            return
        SQL= ("INSERT INTO person (SIRNAME, Level) VALUES('" + self.lineEdit.text()+"',"+
            str(self.spinBoxLevelAdd.value())+");")
        self.makeChangingQuery(SQL)
        [(employeeN,)]=self.makeSelectQuery("SELECT N FROM Person where sirname='"+self.lineEdit.text()+"';")
        for y in range(int(self.year)-int(self.nYearsDepth),int(self.year)+1):
            print(y)
            self.makeChangingQuery("INSERT INTO P_RATING (   N$PERSON, YEAR, RATING )"
                     "VALUES ( "+str(employeeN)+", "+str(y)+", 0 );")
        self.spinBoxLevelAdd.setValue(0)
        self.lineEdit.setText("")
        self.loadCombos()
    
    def userChange(self):
        SQL= ("UPDATE person SET Level="+
            str(self.spinBoxLevelChange.value())+
            " WHERE sirname = '"+ self.comboBoxChangeEmpl.currentText() +"' ;")
        self.makeChangingQuery(SQL)
        
    
    def dellOne(self):
        if QMessageBox.question(self, "Предупреждение", "Данные сотрудника "+self.comboBoxDellEmpl.currentText()+
                    " будут сброшены, вы уверены что хотите продолжить?"
                    , buttons=QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No),
                    defaultButton=QMessageBox.NoButton)==QMessageBox.Yes:
            SQL=("INSERT INTO lost_persons (n, SIRNAME, Level)  Select n, sirname, level from person where sirname = '"+
            self.comboBoxDellEmpl.currentText() +"';")
            self.makeChangingQuery(SQL)
            
            SQL= ("DELETE FROM person  WHERE sirname = '"+ self.comboBoxDellEmpl.currentText() +"' ;")         
            self.makeChangingQuery(SQL)
            
            self.loadCombos()
            
            
    def dellAll(self):
        if QMessageBox.question(self, "Предупреждение", "Данные о всех сотрудниках "+self.comboBoxDellEmpl.currentText()+
                    " будут сброшены из базы данных, вы уверены что хотите продолжить?"
                    , buttons=QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No),
                    defaultButton=QMessageBox.NoButton)==QMessageBox.Yes:
            SQL=("INSERT INTO lost_persons (n,SIRNAME, Level)  Select n, sirname, level from person where sirname not NULL ;")
            self.makeChangingQuery(SQL)
            
            SQL=("DELETE FROM person WHERE Name not NULL ;")         
            self.makeChangingQuery(SQL)
            
            self.loadCombos()
    
    def tabChanged(self):
        #print(self.tabWidget.currentIndex())
        if self.tabWidget.currentIndex()==1:
            self.paintGrid(self.spinBoxYear.value(), self.nYearsDepth)
    
    def paintGrid(self,year,nYearsDepth):
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("Сотрудник"))
        self.tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem("Приоритет"))
        self.tableWidget.setHorizontalHeaderItem(6,QTableWidgetItem("Рассчитанный"))
        for y in range(nYearsDepth):
            self.tableWidget.setHorizontalHeaderItem(y+2,QTableWidgetItem(str(1+y+int(year)-int(nYearsDepth))))
        SQL=("SELECT  s1.sirname, s1.Level, s1.year,s1.rating,s2.year,s2.rating,s3.year,s3.rating,s4.year,s4.rating, s1.n"
            " from(select person.sirname, person.Level, p_rating.year, p_rating.rating, person.n FROM person "
            " left join  p_rating on (person.n=p_rating.n$person and p_rating.year ="+
            str(int(year)-int(nYearsDepth)+1)+ " )) as s1  left join (select * from p_rating) as s2 on (s1.n=s2.n$person and s2.year="+
            str(int(year)-int(nYearsDepth)+2)+" ) left join (select * from p_rating) as s3 on (s1.n=s3.n$person and s3.year="+
            str(int(year)-int(nYearsDepth)+3)+" ) left join (select * from p_rating) as s4 on (s1.n=s4.n$person and s4.year="+
            str(int(year)-int(nYearsDepth)+4)+") order by s1.level desc, s4.rating desc ;")
        res=self.makeSelectQuery(SQL)
        #print(res)
        rowsForEmployees=len(res)
        self.tableWidget.setRowCount(rowsForEmployees)
        for (i,(name, level, y1,r1,y2,r2,y3,r3,y4,r4,employeeN)) in enumerate(res):
            self.tableWidget.setItem(i,0,QTableWidgetItem(str(name)))
            self.tableWidget.setItem(i,1,QTableWidgetItem(str(level)))
            
            self.tableWidget.setItem(i,2,QTableWidgetItem(str(r1)))
            
            self.tableWidget.setItem(i,3,QTableWidgetItem(str(r2)))
            
            self.tableWidget.setItem(i,4,QTableWidgetItem(str(r3)))
            
            self.tableWidget.setItem(i,5,QTableWidgetItem(str(r4)))
            self.tableWidget.setItem(i,6,QTableWidgetItem(str("")))
            self.tableWidget.setItem(i,7,QTableWidgetItem(str(employeeN)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.hideColumn(7)
    
   
        
    
    def paintGraph(self,year):
        #print(year)
        self.mult=5
        self.multX=1.6
        self.digitHeight=15
        self.scene=QtWidgets.QGraphicsScene()
        months=('январь','февраль','март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь')
        if int(year)<=2020:
            sql="select (julianday('"+str(year)+"-03-01') - julianday('"+str(year)+"-02-01')) as febday;"
            #print(sql)
            [(febNumOfDays,)]=self.makeSelectQuery(sql)
            monthLengthList=(31,int(febNumOfDays),31,30,31,30,31,31,30,31,30,31)
       
            SQL=("select value, month from coefficient where year="+str(year)+" order by month")
            [(self.maxValue,self.minValue)]=self.makeSelectQuery("select max(value),min(value) from coefficient where year="+str(year)+" ;")
            res=self.makeSelectQuery(SQL)
            i=0
            
            if self.minValue and self.maxValue:
                for yAxisVal in range(round(self.minValue-1),round(self.maxValue+1)):
                    if not yAxisVal%3:
                        textItem= QtWidgets.QGraphicsTextItem()
                        textItem.setPlainText(str(yAxisVal))
                        self.scene.addItem(textItem)
                        textItem.setPos(-20,round(self.minValue-1)-yAxisVal*self.mult)
            for (value,month) in res:
                textItem= QtWidgets.QGraphicsTextItem()
                textItem.setPlainText(months[month-1])
                self.scene.addItem(textItem)
                textItem.setPos(i*self.multX,1)
                for day in range(monthLengthList[month-1]):
                    #print(i)
                    #ellipse=QtWidgets.QGraphicsEllipseItem(i*self.multX,minValue*self.mult-value*self.mult,3,3)
                    self.scene.addEllipse(i*self.multX,self.minValue*self.mult-value*self.mult,3,3,QtGui.QPen(Qt.green),QtGui.QBrush(Qt.green))
                    i+=1
        else:
            res=self.makeSelectQuery("select day,value from dayly_coefficient where year="+str(year)+";")
            if res:
                [(self.maxValue,self.minValue)]=self.makeSelectQuery("select max(value),min(value) from dayly_coefficient where year="+str(year)+" ;")
                if self.minValue and self.maxValue:
                    for yAxisVal in range(round(self.minValue-1),round(self.maxValue+1)):
                        if not yAxisVal%3:
                            textItem= QtWidgets.QGraphicsTextItem()
                            textItem.setPlainText(str(yAxisVal))
                            self.scene.addItem(textItem)
                            textItem.setPos(-20,round(self.minValue-1)-yAxisVal*self.mult+self.digitHeight)
                for (day,value) in res:
                    if not (day%31):
                        textItem= QtWidgets.QGraphicsTextItem()
                        #print(day//31)
                        textItem.setPlainText(months[day//31])
                        self.scene.addItem(textItem)
                        textItem.setPos(day*self.multX,1)
                    self.scene.addEllipse(day*self.multX,self.minValue*self.mult-value*self.mult,3,3,QtGui.QPen(Qt.green),QtGui.QBrush(Qt.green))
                    
        

        self.graphicsViewReiting.setScene(self.scene)
        self.graphicsViewReiting.show()    
        
        
        
    def onSpinYearChanged(self):
        self.daysForNewCoefs=np.zeros(2)
        self.coefsNew=np.zeros(2)
        self.paintGrid(self.spinBoxYear.value(), self.nYearsDepth)
        self.paintGraph(self.spinBoxYear.value())
    
    def oldReitCalc(self):
        mdays=[31,28,31,30,31,30,31,31,30,31,30,31]
        #print('rowcount:',self.tableWidget.rowCount())
        for i in range(self.tableWidget.rowCount()):
            
            calcdays=[0,0,0,0,0,0,0,0,0,0,0,0]
            SQL= ("select P_rests.date, strftime('%m',P_rests.date) as month, strftime('%d',P_rests.date) as day, P_rests.length, P_rests.way_length, strftime('%d', date('"+
                str(self.spinBoxYear.value())+"-02-01','+1 month','-1 day')) as fld From p_rests where year = "+
                str(self.spinBoxYear.value())+"  and n$person="+
                str(self.tableWidget.item(i,7).text())+";")
            res=self.makeSelectQuery(SQL)    
            print(res)
            for (date, month, day, length,way,febNumOfDays) in res:
                #print('res',self.tableWidget.item(i,7).text(),':',date, month, day, length,way,febNumOfDays)
                mdays[1]=int(febNumOfDays)
                for j in range(length+way):
                    #print(day,month,mdays[int(month)-1] )
                    if int(day)<=mdays[int(month)-1]:
                        calcdays[int(month)-1]+=1
                        day=int(day)+1
                    else:
                        month=int(month)+1
                        month=int(month)%13
                        calcdays[int(month)-1]+=1
                        day=1
                #print('calcd',calcdays)        
            sumDays=0
            rating=0
            SQL=("select value, month from coefficient where year="+str(self.spinBoxYear.value())+
                    " order by month")
            res=self.makeSelectQuery(SQL)
            
            for (coef,mnth) in res:
                #print('coef mnth',coef,mnth)
                sumDays+=calcdays[mnth-1]
                #print('days in month',calcdays[mnth-1])
                #print('rate',calcdays[mnth-1]*(coef/mdays[mnth-1]))
                
                rating+=calcdays[mnth-1]*(coef/mdays[mnth-1])
                #print('sum',sumDays)
                #print('ratesum',rating)
            #if sumDays: print(round(rating*(10**4))/(10**4)*sumDays)
            if sumDays: self.tableWidget.setItem(i,6,QTableWidgetItem(str(round(round(rating*(10**4))/((10**4)*sumDays),6))))
            else:self.tableWidget.setItem(i,6,QTableWidgetItem(""))
            
    def newRateCalc(self):
        SQL=("select value from dayly_coefficient where year="+str(self.spinBoxYear.value())+
                    " order by day")
        coefsRes=self.makeSelectQuery(SQL)
        #print('coefsRes:',coefsRes)
        #coefs=coefsRes[:0]
        #print('coefs:',coefs)
        for i in range(self.tableWidget.rowCount()):
            sql= ("select P_rests.date,  strftime('%j',P_rests.date) as day, P_rests.length, P_rests.way_length, strftime('%j','"+
                    str(self.spinBoxYear.value())+"-12-31') as lastYearDay From p_rests where year = "+
                    str(self.spinBoxYear.value())+"  and n$person="+
                    str(self.tableWidget.item(i,7).text())+";")
            restRes=self.makeSelectQuery(sql)
            
            #print('restRes',restRes)  
            print('-'*70)
            print('Person name',self.tableWidget.item(i,0).text())
            
            totalRating=0
            totalDays=0
            numRests=0
            
            for (date, day, length, way, lastYearDay) in restRes:
                
                rating=0
                numRests+=1
                print('Rest number',numRests,':',date, day, length, way, lastYearDay)
                totalDaysInRest=int(day)+int(length)+int(way)
                numDaysInRest=int(length)+int(way)
                print('numDaysInRest:',numDaysInRest)
                for d in range(int(day),totalDaysInRest):
                    #print('lastYearDay:', lastYearDay)
                    if d<=int(lastYearDay):
                        (coef,)=coefsRes[d]
                        print('coef:',coef/30)
                        #the coefs are averaged to 12 month one day coefficient
                        rating+=coef/30
                    print('rating:',rating)
                print('sumRating:',rating)
                rating=rating/numDaysInRest
                print("averageRating:", rating)  
                #totalDays+=numDaysInRest
                #print('totalDays:',totalDays)
                totalRating+=rating
                """
                if totalDaysInRest:
                    rating=rating/totalDays
                print('ratingDivided',rating)
                totalRating+=rating
                print("totalRating iteration:", totalRating)    
                """
            print('sumRating:',totalRating)
            print('totalrests for',self.tableWidget.item(i,0).text(),':' ,numRests)
            if numRests:
                totalRating=totalRating/numRests
                print("totalRating for",self.tableWidget.item(i,0).text(),':', totalRating)    
                self.tableWidget.setItem(i,6,QTableWidgetItem(str(round(totalRating,6))))
            else:
                print("There is no totalRating for",self.tableWidget.item(i,0).text())    
                self.tableWidget.setItem(i,6,QTableWidgetItem(''))
                
                
    def onCalcReiteClick(self): 
        if self.spinBoxYear.value()<=2020:
            self.oldReitCalc()
        else:
            self.newRateCalc()
    
    #def makeInDataForYear(self,currentYear):
        
    
    def makeNewCoefs(self):
        inputData=np.zeros(4)
        #print(inputData)
        
    
        year=int(self.spinBoxYear.value())
        for currentYear in range (year-self.nYearsDepth, year):
            [(employeeNumber,)]=self.makeSelectQuery("select count(1) from P_RESTS where year="+str(currentYear))
            #print('employeeNumber:',employeeNumber)
            print('Year for coefs:',currentYear)
            SQL=("select p_rests.N$PERSON, strftime('%d.%m.%Y',P_rests.date)as dat,strftime('%j',P_rests.date) as nDay, "
                " P_rests.length,P_rests.way_length,  p_rests.N_REST, p_rest_num.rest_number " 
                " From "
                " p_rest_num  left join p_rests on ( p_rests.n$person = p_rest_num.n$person and p_rests.year =p_rest_num.year and p_rest_num.year="+ str(currentYear)+ ")"
                " join (select * from p_rating where year between "+str(currentYear-self.nYearsDepth)+" and "+str(currentYear-1)+" ) as s2 on p_rests.n$person =s2.n$person  "
                " group by P_rests.date, p_rests.N$PERSON, p_rest_num.rest_number   ORDER BY  p_rests.N_REST , sum(s2.rating) DESC  ;")
            """SQL=("select Person.n,strftime('%d.%m.%Y',P_rests.date)as dat,strftime('%j',P_rests.date) as nDay,"
                " P_rests.length,P_rests.way_length,  p_rests.N_REST, p_rest_num.rest_number  From person left join p_rest_num on"
                " ( p_rest_num.n$person = person.n and p_rest_num.year= "
                + str(currentYear)+ " ) "
                " join (select * from p_rating where year between "+
                str(currentYear-self.nYearsDepth)+" and "+str(currentYear-1)+
                " ) as s2 on person.n=s2.n$person  left join p_rests on (person.n=p_rests.n$person and p_rests.year ="+
                str(currentYear)+
                " )  group by P_rests.date,person.N  ORDER BY  p_rests.N_REST, person.Level DESC,   sum(s2.rating) DESC ;")
            """
            #print(SQL)
            res=self.makeSelectQuery(SQL)
            employeeCount=0
            #print("n,date,month,length,way,nRest,restsNumber")
            for (n,date,nDay,length,way,nRest,restsNumber) in res:
                #print(employeeCount,n,date,nDay,length,way,nRest,restsNumber)
                #print('employeeCount:',employeeCount)
                if nDay and length:
                    for i in range(int(nDay),int(nDay)+int(length)+int(way)):
                        #print(i,(int(length)+int(way))/75,nRest/restsNumber,employeeCount/employeeNumber)
                        values=np.array([i,(int(length)+int(way))/75,nRest/restsNumber,employeeCount/employeeNumber])
                        #print(values)
                        inputData=np.vstack((inputData,values)) 
                        #print('inputData:',inputData)
                        
                    employeeCount+=1     
            
        #print('inputData:',inputData)
        inputData=np.delete(inputData, 0, 0)
        #print('inputData is the best:',inputData)
        print('inputData type:',type(inputData))
        print('inputData shape:',inputData.shape)
        (self.daysForNewCoefs,self.coefsNew)=self.makeML(inputData,self.gammaParametr)
        print('daysForCoefs type:',type(self.daysForNewCoefs),self.daysForNewCoefs.shape)
        print('coefs type:',type(self.coefsNew),self.coefsNew.shape)
        #np.savetxt("foo3.csv", inputData, delimiter=",")
        
                
    def makeML(self,inputData,gammaParametr):
        #starting mashine lerning
        #get days from first column
        X=inputData[:,0]
        #print(X)
        #print(X.shape)
        #make it one column, not row
        XX=X.reshape(-1, 1)
        #print(XX)
        #print(XX.shape)
        # gamma=0.0005
        machine = svm.SVR(kernel='rbf', C=15, gamma=gammaParametr)
        clusters_list=np.arange(12,24,1)
        max_score=0
        max_score_n_clusters=0
        for i in clusters_list:
            agg = AgglomerativeClustering(n_clusters=i, linkage='average')
            Y = agg.fit_predict(inputData)
            H=np.unique(Y, return_counts=True)
            #print(H)
            C=H[1]
            T=C[Y]
            sizeT=T.size
            T_avr=sizeT/(T)
            
            X_train, X_test, y_train, y_test = train_test_split(XX, T, random_state=0)
          
            machine.fit(X_train, y_train)
            #print("Accuracy on test set: {:.2f}".format(machine.score(X_test, y_test)))
            #print("machine.score:",machine.score(X_test, y_test))
            if machine.score(X_test, y_test) > max_score:
                max_score=machine.score(X_test, y_test)
                #print("max_score:",max_score)
                max_score_n_clusters = i

        print("Maximum Accuracy N Clusters: {:.2f}".format(max_score_n_clusters))
        coefsRatio=12/max_score_n_clusters
        print('coefsRatio:',coefsRatio)
        agg = AgglomerativeClustering(n_clusters=max_score_n_clusters, linkage='average')
        Y = agg.fit_predict(inputData)
        H=np.unique(Y, return_counts=True)
        #print(H)
        C=H[1]
        T=C[Y]
        sizeT=T.size
        T_avr=sizeT/(T)
        #print("Clusters X:",type(X),X.shape) 
        #print("Clusters:",type(T_avr),T_avr.shape)    
        X_train, X_test, y_train, y_test = train_test_split(XX, T, random_state=0)
          
        machine.fit(X_train, y_train)
        print("Accuracy on training set: {:.2f}".format(machine.score(X_train, y_train)))
        print("Accuracy on test set: {:.2f}".format(machine.score(X_test, y_test)))
        d = np.arange( 366 )
        dd=d.reshape(-1, 1)
        p=machine.predict(dd)
        p_avr=sizeT/(p)
        #print('coefs not modified',p_avr)
        p_avr=p_avr*coefsRatio
        T_avr=T_avr*coefsRatio
        #print('coefs modified',p_avr)
        #print("Coefs predicted dd:",type(d),d.shape)    
        #print("Coefs predicted:",type(p_avr),p_avr.shape)  
        self.printPointGraph(X,T_avr,Qt.red)
        self.printPointGraph(d,p_avr,Qt.blue)
        
        return (d,p_avr)
        
    def printPointGraph(self,X,Y,color):
        for pX,pY in zip(X,Y):
            self.scene.addEllipse(pX*self.multX,self.minValue*self.mult-pY*self.mult,3,3,QtGui.QPen(color),QtGui.QBrush(color))
        self.graphicsViewReiting.setScene(self.scene)
        self.graphicsViewReiting.show()           
    
    def onCalcCoefClick(self):
        self.makeNewCoefs()
        
    def onSaveCoefClick(self):
        if not self.daysForNewCoefs.any() or not self.coefsNew.any():
            print("Не рассчитаны коэфициенты")
            return
        for xP,yP in zip(self.daysForNewCoefs,self.coefsNew):
            res=self.makeSelectQuery("select value from dayly_coefficient where day="+str(xP)+" and year="+str(self.spinBoxYear.value())+";" )
            if res :
                #print('res:',res)
                sql=("update dayly_coefficient set value="+str(yP)+" where day="+str(xP)+" and year="+str(self.spinBoxYear.value())+";")
                #print(sql)
            else:
                #print("no res")
                sql=("insert into dayly_coefficient (year,day,value) values("+str(self.spinBoxYear.value())+","+
                    str(xP)+","+str(yP)+");")
            #print(sql)        
            self.makeChangingQuery(sql)
    
    def is_digit(self,string):
        if string.isdigit():
            return True
        else:
            try:
                float(string)
                return True
            except ValueError:
                return False
    
    def onSaveRateClick(self):
        for i in range(self.tableWidget.rowCount()):
            if not self.tableWidget.item(i,6).text():
                #print("no text",i)
                continue
            if not self.is_digit(self.tableWidget.item(i,6).text()):
                #print(self.tableWidget.item(i,6).text())
                #print("no digit",i)
                continue    
            res =self.makeSelectQuery("select rating from p_rating where year = "+str(self.spinBoxYear.value())+
                " and n$person = "+self.tableWidget.item(i,7).text()+" ;" )
            if res:
                #print(res)
                sql=("UPDATE p_rating SET rating = "+ self.tableWidget.item(i,6).text()+
                    " WHERE year = "+str(self.spinBoxYear.value())+
                    " AND n$person = "+self.tableWidget.item(i,7).text()+
                    ";")
                
            else:
                #print('no rate')
                sql=("INSERT INTO p_rating (year,n$person,rating) VALUES ( "+
                    str(self.spinBoxYear.value())+" , "+
                    self.tableWidget.item(i,7).text()+" ,  "+
                    self.tableWidget.item(i,6).text()+"  );")
                    
            #print(sql)
            self.makeChangingQuery(sql)
            
        self.paintGrid(self.spinBoxYear.value(), self.nYearsDepth)
        
    
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
        self.done(0)  
    
    def onpushButtonCancel_click(self):
        self.done(0)  