#!/usr/bin/env python3

import psycopg2
from decimal import *

DBNAME = "news"

sqlList = []

def query1(sqlList):
# Query to the first question, query should return the three article titles with the most amount of views
# substr (arg, characters in /articles/, limit character query to length of the string)
#    string = "Question 1 table with article title, followed by the most amount of views"
#    sqlList.append(string)
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select title, count(*) as numofviews from articles, log where articles.slug = substring(log.path, 10, char_length(log.path)) group by articles.title limit 3) t order by numofviews desc")
    if sqlList:
        list1 = c.fetchall()
        col_names = [desc[0] for desc in c.description]
        print col_names
        sqlList.append(col_names + list1)
    else:
        newlist = c.fetchall()
        col_names = [desc[0] for desc in c.description]
        print col_names
        sqlList.append(col_names + newlist)
    db.close()
    return sqlList

def query2(sqlList):
# Query to the second question, query should return the most popular article authors of all time

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select authors.name, count(*) as numofviews from articles join log on articles.slug = substring(log.path, 10, char_length(log.path)) join authors on articles.author = authors.id group by authors.name limit 5) t order by t.numofviews desc")
    if sqlList:
        list2 = c.fetchall()
        sqlList.append(list2)
    else:
        newlist = c.fetchall()
        sqlList.append(newlist)
    db.close()
    return sqlList

def query3(sqlList):
# Query to the third question on which days did more of 1% requests lead to errors
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select day, errcount, okcount from (select day, count(case when t.status_code ='ok' then 'ok' end) as okcount, count(case when t.status_code = 'err' then 'err' end) as errcount from (select to_char(log.time::date,'DD mon YYYY') as day, case when log.status = '404 NOT FOUND' then 'err' when log.status = '200 OK' then 'ok' else 'baddata' end as status_code from log) t group by day) t2 where errcount > 0.01 * (errcount + okcount)")
    if sqlList:
        list3 = c.fetchall()
        sqlList.append(list3)
    else:
        newlist = c.fetchall()
        sqlList.append(newlist)
    db.close()

def formatList3(sqlList):

    print type(sqlList)
    print sqlList
    errcount = Decimal(sqlList[2][0][1])
    print errcount
    print type(errcount)
    okcount = Decimal(sqlList[2][0][2])
    print okcount
    errrate = Decimal(errcount/(okcount + errcount))
    print errrate
    sqlList.append(float(errrate)* 100.0)
    print sqlList

def queryAll(sqlList):
    query1(sqlList)
    query2(sqlList)
    query3(sqlList)
    formatList3(sqlList)

def main():
    getcontext().prec = 3
    queryAll(sqlList)


if __name__ =="__main__":
    main()
