#!/usr/bin/env python3

import psycopg2
from decimal import *

DBNAME = "news"

sqlList = []

def query1(sqlList):
# Query to the first question, query should return the three article titles with the most amount of views
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select title, count(*) as numofviews from articles, log where articles.slug = substring(log.path, articles.slug) group by articles.title limit 3) t order by numofviews desc")
    if sqlList:
        sqlList += c.fetchall()
    else:
        sqlList = c.fetchall()
    db.close()
    return sqlList

def query2(sqlList):
# Query to the second question, query should return the most popular article authors of all time
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select authors.name, count(*) as numofviews from articles join log on articles.slug = substring(log.path, articles.slug) join authors on articles.author = authors.id group by authors.name limit 5) t order by t.numofviews desc")
    if sqlList:
        sqlList += c.fetchall()
    else:
        sqlList = c.fetchall()
    db.close()
    return sqlList

def query3(sqlList):
# Query to the third question on which days did more of 1% requests lead to errors
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select day, errcount, okcount from (select day, count(case when t.status_code ='ok' then 'ok' end) as okcount, count(case when t.status_code = 'err' then 'err' end) as errcount from (select to_char(log.time::date,'DD mon YYYY') as day, case when log.status = '404 NOT FOUND' then 'err' when log.status = '200 OK' then 'ok' else 'baddata' end as status_code from log) t group by day) t2 where errcount > 0.01 * (errcount + okcount)")
    if sqlList:
        list3 = c.fetchall()
        sqlList.extend(list3)
    else:
        newlist = c.fetchall()
        sqlList.extend(newlist)
    db.close()

def formatList(sqlList):
    print type(sqlList)
    print sqlList
    errcount = Decimal(sqlList[0][1])
    print errcount
    okcount = Decimal(sqlList[0][2])
    print okcount
    errrate = Decimal(errcount/(okcount + errcount))
    print errrate
    sqlList.append(float(errrate))
    print(sqlList)

def main():
    getcontext().prec = 3
#    result1 = query1(list)
#    result2 = query2(list)
    query3(sqlList)
    formatList(sqlList)
#    print(result1 + result2 + result3)


if __name__ =="__main__":
    main()
