import sqlite3

def makeSelectQuery(Query):
    conn = sqlite3.connect("rest.db")
    cursor = conn.cursor()
    sql = Query
    cursor.execute(sql)
    #conn.close()
    return cursor.fetchall() 
    conn.close()
    
def makeChangingQuery(Query):    
    conn = sqlite3.connect("rest.db")
    cursor = self.conn.cursor()
        
    try:
        cursor.executescript(Query)
    except sqlite3.DatabaseError as err:       
        print("Error: ", err)
    else:
        conn.commit()
        conn.close()

def makePage(year,nYearsDepth):
    conn = sqlite3.connect("rest.db")
    cursor = conn.cursor()
    page=""
    page+='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"> \n'
    page+= ('<html><head> <style type=\"text/css\"> '+
            " table { border-color: black; border-style:  solid; border-collapse: collapse;} "+
            ' td, th {border: thin dotted gray;padding: 5px;} '+
            " </style> </head>")
    page+="<body> \n"
    months=('январь','февраль','март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь')

    SQL=("select max(rest_in_month) from(select strftime('%m',P_rests.date),count(*) as rest_in_month from p_rests where year="+
        str(int(year)+1)+" group by strftime('%m',P_rests.date));")
    cursor.execute(SQL)
    [(rows,)] =cursor.fetchall()
    #print(rows)
    if not rows:
        conn.close()
        return 0
    HtmlContent=[]
    #HtmlContent.append(rows)
    r=[0,0,0,0,0,0,0,0,0,0,0,0]
    #L=['','','']
    for row in range(rows):
        HtmlContent.append([])
        #print(HtmlContent)
        #print('')
        for l in range(12):
            HtmlContent[row].append([])
            #print(HtmlContent)
            #print('')
            for k in range(3):
                HtmlContent[row][l].append('')
                #print(HtmlContent)
                #print('')
    
    
    #print(HtmlContent)
    
    SQL=("select Person.SIRNAME,strftime('%d.%m.%Y',P_rests.date)as dat,strftime('%m',P_rests.date) as month, P_rests.length,P_rests.way_length,Person.N From person join (select * from p_rating where year between "+
        str(int(year)-nYearsDepth+1)+" and "+str(year)+
        " ) as s2 on person.n=s2.n$person  left join p_rests on (person.n=p_rests.n$person and p_rests.year ="+
        str(int(year)+1)+
        " ) WHERE person.Level>1 group by P_rests.date,person.N  ORDER BY  person.Level DESC, p_rests.N_REST,  sum(s2.rating) DESC ;")
    cursor.execute(SQL)
    res=cursor.fetchall()
    #print(res)
    for (name,date,month,length,way,employeeN) in res:
        #print(name,date,month,length,way,employeeN)
        if date:
            wayStr='' if not way else '+'+str(way)
            #print('r:',r[int(month)-1])
            #print('m:',int(month)-1)
            HtmlContent[r[int(month)-1]][int(month)-1][0]=str(name)
            #print(HtmlContent[r[int(month)-1]][int(month)-1][0])
            HtmlContent[r[int(month)-1]][int(month)-1][1]=str(length)+ wayStr
            HtmlContent[r[int(month)-1]][int(month)-1][2]=str(date)
            r[int(month)-1]+=1
            #print (r)
            #print(HtmlContent)
    SQL=("select Person.SIRNAME,strftime('%d.%m.%Y',P_rests.date)as dat,strftime('%m',P_rests.date) as month, P_rests.length,P_rests.way_length,Person.N From person join (select * from p_rating where year between "+
        str(int(year)-nYearsDepth+1)+" and "+str(year)+
        " ) as s2 on person.n=s2.n$person  left join p_rests on (person.n=p_rests.n$person and p_rests.year ="+
        str(int(year)+1)+
        " ) WHERE person.Level<=1 group by P_rests.date,person.N  ORDER BY  p_rests.N_REST, person.Level DESC,   sum(s2.rating) DESC ;")
    cursor.execute(SQL)
    res=cursor.fetchall()
    for (name,date,month,length,way,employeeN) in res:
        if date:
            wayStr='' if not way else '+'+str(way)
            HtmlContent[r[int(month)-1]][int(month)-1][0]=str(name)
            HtmlContent[r[int(month)-1]][int(month)-1][1]=str(length)+ wayStr
            HtmlContent[r[int(month)-1]][int(month)-1][2]=str(date)
            r[int(month)-1]+=1
    
    #print(HtmlContent)
    page+="<table> \n"
    for s in range(3):
        page+="<tr> \n"
        for i in range(4):
            page+="<td colspan='3'>"+months[i+4*s]+"</td> \n"
        page+="</tr> \n"
        for j in range(rows):
            page+="<tr> \n"
            for i in range(4):
                for p in range(3):
                    page+="<td>"+HtmlContent[j][i+4*s][p]+"</td> \n"
            page+="</tr> \n"
    page+="</table> \n </body> \n </html>"
    
    
    #print(page)
    
    conn.close()
    return page