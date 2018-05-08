#!/usr/bin/env python3

import psycopg2

DBNAME = "news"

list = []

def query1(list):
# Query to the first question, query should return the three article titles with the most amount of views
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select title, count(*) as numofviews from articles, log where articles.slug = substring(log.path, articles.slug) group by articles.title limit 3) t order by numofviews desc")
    if list:
        list += c.fetchall()
    else:
        list = c.fetchall()
    db.close()
    return list

def query2(list):
# Query to the second question, query should return the most popular article authors of all time
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select authors.name, count(*) as numofviews from articles join log on articles.slug = substring(log.path, articles.slug) join authors on articles.author = authors.id group by authors.name limit 5) t order by t.numofviews desc")
    if list:
        list += c.fetchall()
    else:
        list = c.fetchall()
    db.close()
    return list

def query3(list):
# Query to the third question on which days did more of 1% requests lead to errors
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select day, errcount, okcount from (select day, count(case when t.status_code ='ok' then 'ok' end) as okcount, count(case when t.status_code = 'err' then 'err' end) as errcount from (select to_char(log.time::date,'DD mon YYYY') as day, case when log.status = '404 NOT FOUND' then 'err' when log.status = '200 OK' then 'ok' else 'baddata' end as status_code from log) t group by day) t2 where errcount > 0.01 * (errcount + okcount)")
    if list:
        list += c.fetchall()
    else:
        list = c.fetchall()
    db.close()
    return list

def format(result):
    errcount = result[0][1]
    okcount = result[0][2]
    print(errcount)

def main():
#    result1 = query1(list)
#    result2 = query2(list)
    result3 = query3(list)
    format(result3)
#    print(result1 + result2 + result3)


if __name__ =="__main__":
    main()
