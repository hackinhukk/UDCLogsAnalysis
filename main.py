import psycopg2

DBNAME = "news"

list = ()

def query1(list):
# need to get count from log table
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select title, count(*) as numofviews from articles, log where articles.slug = substring(log.path, articles.slug) group by articles.title limit 10) t order by numofviews desc")
    if list:
        list += c.fetchall()
    else:
        list = c.fetchall()
    db.close()
    return list

def query2(list):
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
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select day, errcount/(okcount + errcount) as errrate from (select day, count(case when t.status_code ='ok' then 'ok' end) as okcount, count(case when t.status_code = 'err' then 'err' end) as errcount from (select to_char(log.time::date,'DD mon YYYY') as day, case when log.status = '404 NOT FOUND' then 'err' when log.status = '200 OK' then 'ok' else 'baddata' end as status_code from log) t group by day) t2 where errcount > 0.01 * (errcount + okcount)")
#    c.execute;("select log.time::date as day, case when log.status = '404 NOT FOUND' then 'err' when log.status = '200 OK' then ok else 'baddata' end as connection, count(*) as num from log group by day, log.status")
    if list:
        list += c.fetchall()
    else:
        list = c.fetchall()
    db.close()
    return list

def main():
    result1 = query3(list)

    print(result1)


if __name__ =="__main__":
    main()
