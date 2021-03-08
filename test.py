import psycopg2


def db_connect():
    con = psycopg2.connect(
        host="ec2-52-213-167-210.eu-west-1.compute.amazonaws.com",
        database="d2c0pa2od76s0h",
        user="ygfmgmclajbdwt",
        port="5432",
        password="75047d007fbada55ac72abf0f233aeefe1f6109f8ccfcc669d59cd537f15b675"
    )
    cur = con.cursor()
    cur.execute("select column_name,data_type from information_schema.columns where table_name = 'reports'")
    print(cur.fetchall())
    return con, cur


db_connect()
