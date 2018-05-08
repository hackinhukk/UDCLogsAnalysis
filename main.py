#!/usr/bin/env python3

import psycopg2
from decimal import *

DBNAME = "news"

sqlList = []
col1_header = []
col2_header = []
col3_header = []



def query1(sqlList):
# Query to the first question, query should return the three article titles with the most amount of views
# substr (arg, characters in /articles/, limit character query to length of the string)
#    string = "Question 1 table with article title, followed by the most amount of views"
#    sqlList.append(string)
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select title, count(*) as numofviews from articles, log where articles.slug = substring(log.path, 10, char_length(log.path)) group by articles.title limit 3) t order by numofviews desc")
    list1 = c.fetchall()
    col_names = [desc[0] for desc in c.description]
    sqlList.append(col_names + list1)
    col1_header.append(col_names)
    db.close()
    return sqlList

def query2(sqlList):
# Query to the second question, query should return the most popular article authors of all time

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select authors.name, count(*) as numofviews from articles join log on articles.slug = substring(log.path, 10, char_length(log.path)) join authors on articles.author = authors.id group by authors.name limit 5) t order by t.numofviews desc")
    list2 = c.fetchall()
    col_names = [desc[0] for desc in c.description]
    sqlList.append(col_names + list2)
    col2_header.append(col_names)
    db.close()
    return sqlList

def query3(sqlList):
# Query to the third question on which days did more of 1% requests lead to errors
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select day, errcount, okcount from (select day, count(case when t.status_code ='ok' then 'ok' end) as okcount, count(case when t.status_code = 'err' then 'err' end) as errcount from (select to_char(log.time::date,'DD mon YYYY') as day, case when log.status = '404 NOT FOUND' then 'err' when log.status = '200 OK' then 'ok' else 'baddata' end as status_code from log) t group by day) t2 where errcount > 0.01 * (errcount + okcount)")
    list3 = c.fetchall()
    col_names = [desc[0] for desc in c.description]
    sqlList.append(col_names + list3)
    col3_header.append(col_names[0])
    col3_header.append('error rate')
    db.close()

def formatList3(sqlList):

#    print type(sqlList)
#    print sqlList
    errcount = Decimal(sqlList[2][3][1])
#    print errcount
#    print type(errcount)
    okcount = Decimal(sqlList[2][3][2])
#    print okcount
    errrate = Decimal(errcount/(okcount + errcount))
    return errrate

#    print sqlList

def queryAll(sqlList):
    query1(sqlList)
    query2(sqlList)
    query3(sqlList)
    rate = formatList3(sqlList)
    return rate

def printTable1(table1):
    for l in table1:
        outerCount = 0
        for r in l:
            if outerCount > 2:
                print r
            elif outerCount > 1:
                print col1_header
            outerCount += 1

def printTable3(table3):

    #still needs to also only extract and print the date, then add the errrate
    for l in table3:
        outerCount = 0
        for r in l:
            if outerCount > 3:
                print r
            elif outerCount > 2:
                print col3_header
            outerCount += 1

def printOutput(sqlList):
    table1 = sqlList[0:1]
    table2 = sqlList[1:2]
    table3 = sqlList[2:3]
    print table1
    print table2
    print table3
    print col3_header

def main():

    getcontext().prec = 3
    rate = queryAll(sqlList)
    printOutput(sqlList)
    print rate


if __name__ =="__main__":
    main()
