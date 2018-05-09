#!/usr/bin/env python2
# this is needed to get division to not return a 0
from __future__ import division
import psycopg2

DBNAME = "news"

# The PostGreSQL Statements in string format
SQLtext1 = """select * from (select title, count(*) as numofviews from
           articles, log where articles.slug = substring(log.path, 10,
           char_length(log.path)) group by articles.title limit 3) t
           order by numofviews desc"""
SQLtext2 = """select * from (select authors.name, count(*) as numofviews
           from articles join log on articles.slug = substring(log.path,
           10, char_length(log.path)) join authors on articles.author =
           authors.id group by authors.name limit 5) t
           order by t.numofviews desc"""
SQLtext3 = """select day, errcount, okcount from (select day,
           count(case when t.status_code ='ok' then 'ok' end) as okcount,
           count(case when t.status_code = 'err' then 'err' end) as errcount
           from (select to_char(log.time::date,'DD mon YYYY') as day, case
           when log.status = '404 NOT FOUND' then 'err' when log.status
           = '200 OK' then 'ok' else 'baddata' end as status_code from log) t
           group by day) t2 where errcount > 0.01 * (errcount + okcount)"""


def queryFinal():
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
                  str(round((element[1]/element[2]) * 100, 3)) +
                  '%' + ' error rate' for element in SQLTable]))
    c.close()


def main():
    queryFinal()


if __name__ == "__main__":
    main()
