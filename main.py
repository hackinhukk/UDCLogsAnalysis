#!/usr/bin/env python3

import psycopg2


DBNAME = "news"

data1 = []
data2 = []
data3 = []
sqlList = []
# To gather the headers for each list
col1_header = []
col2_header = []
col3_header = []
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

# Query Functions


def query1(sqlList):
    # Query to the first question, query should return
    # the three article titles with the most amount of views
    # substr (arg, characters in /articles/,
    # limit character query to length of the string)
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(SQLtext1)
    list1 = c.fetchall()
    col_names = [desc[0] for desc in c.description]
    sqlList.append(col_names + list1)
    col1_header.append(col_names)
    db.close()


def query2(sqlList):
    # Query to the second question, query should return
    # the most popular article authors of all time
    # substr (arg, characters in /articles/, limit character
    # query to length of the string
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(SQLtext2)
    list2 = c.fetchall()
    col_names = [desc[0] for desc in c.description]
    sqlList.append(col_names + list2)
    col2_header.append(col_names)
    db.close()


def query3(sqlList):
    # Query to the third question on which days did more of
    # 1% requests lead to errors
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(SQLtext3)
    list3 = c.fetchall()
    col_names = [desc[0] for desc in c.description]
    sqlList.append(col_names + list3)
    col3_header.append(col_names[0])
    col3_header.append('error rate in %')
    db.close()


def formatList3(sqlList):
    errcount = float(sqlList[2][3][1])
    okcount = float(sqlList[2][3][2])
    errrate = round((errcount/(okcount + errcount)), 4)
    return errrate


def queryAll(sqlList):
    query1(sqlList)
    query2(sqlList)
    query3(sqlList)
    rate = formatList3(sqlList)
    return rate

    # Print Table/Output Functions


def printTableReg(table, col_header):
    for l in table:
        outerCount = 0
        for r in l:
            if outerCount > 1:
                print r
            elif outerCount > 0:
                print col_header[0]
            outerCount += 1


def printTable1(table1):
    printTableReg(table1, col1_header)


def printTable2(table2):
    printTableReg(table2, col2_header)


def printTable3(table3, errrate):
    print col3_header
    for l in table3:
        outerCount = 0
        for r in l:
            if outerCount > 2:
                templist = []
                templist.append(r[0])
                templist.append(errrate * 100)
                print templist
            outerCount += 1


def printOutput(sqlList, errrate):
    table1 = sqlList[0:1]
    table2 = sqlList[1:2]
    table3 = sqlList[2:3]
    printTable1(table1)
    print "\n"
    printTable2(table2)
    print "\n"
    printTable3(table3, errrate)

    # Main Function


def main():
    rate = queryAll(sqlList)
    printOutput(sqlList, rate)


if __name__ == "__main__":
    main()
