#!/usr/bin/env python2
# this is needed to get division to not return a 0
from __future__ import division
import psycopg2

DBNAME = "news"

# The PostGreSQL Statements in string format
SQLtext1 = """SELECT * FROM (SELECT title, count(*) AS numofviews
           FROM articles, log
           WHERE articles.slug = substring(log.path, 10,char_length(log.path))
           GROUP BY articles.title) t
           ORDER BY numofviews DESC LIMIT 3"""
SQLtext2 = """SELECT authors.name, count(*) AS numofviews
           FROM articles JOIN log
           ON articles.slug = substring(log.path, 10, char_length(log.path))
           JOIN authors
           ON articles.author = authors.id
           GROUP BY authors.name
           ORDER BY numofviews DESC"""
SQLtext3 = """SELECT day, errcount, okcount FROM
           (SELECT day, count(CASE WHEN t.status_code ='ok' THEN 'ok' END) AS okcount,
           count(CASE WHEN t.status_code = 'err' THEN 'err' END) AS errcount
           FROM (SELECT to_char(log.time::date,'DD mon YYYY') AS day, CASE
           WHEN log.status = '404 NOT FOUND' THEN 'err' WHEN log.status
           = '200 OK' THEN 'ok' ELSE 'baddata' END AS status_code FROM log) t
           GROUP BY day) t2 WHERE errcount > 0.01 * (errcount + okcount)"""


def queries():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    SQLList = [SQLtext1, SQLtext2, SQLtext3]

    for i, sql_txt in enumerate(SQLList):

        c.execute(sql_txt)
        SQLTable = []
        SQLTable = c.fetchall()
        if i == 0:
            print "Question: {}".format(str(i + 1))
            print "The Three most popular articles of all time"
            # () around print are neccessary to remove PEP8 warning
            # about under-indented lines
            print('\n'.join([str(element[0]) + ' -- ' + str(element[1])
                  + ' number of views.' for element in SQLTable]))
        elif i == 1:
            print "Question: {}".format(str(i + 1))
            print "The most popular article authors of all time"
            print('\n'.join([str(element[0]) + ' -- ' + str(element[1]) +
                  ' number of views.' for element in SQLTable]))
        elif i == 2:
            print "Question: {}".format(str(i + 1))
            print "The days on which requests errored more than 1%"
            print('\n'.join([str(element[0]) + ' -- ' +
                  str(round((element[1]/(element[1] + element[2])) * 100, 3)) +
                  '%' + ' error rate' for element in SQLTable]))
    c.close()


def main():
    queries()


if __name__ == "__main__":
    main()
