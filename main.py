import psycopg2

DBNAME = "news"

list = ()

def query1(list):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select author from articles")
    if list:
        list += c.fetchall()
    else:
        list = c.fetchall()
    db.close()
    return list

def query2(list):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select title from articles")
    if list:
        list += c.fetchall()
    else:
        list = c.fetchall()
    db.close()
    return list

def main():
    result1 = query1(list)
    print(result1)


if __name__ =="__main__":
    main()
