from typing import Optional
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import psycopg2
from fastapi.security import OAuth2PasswordBearer


class User(BaseModel):
    user_id: int
    score: int


app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")


def db_connect():
    con = psycopg2.connect(
        host="ec2-99-80-200-225.eu-west-1.compute.amazonaws.com",
        database="d5ppvv9153vvm5",
        user="zecuqgzzqzqckp",
        port="5432",
        password="6f7405fe16301e491c64acd59f74881ec9a405ad70293f3d9bbbcd02875e4b22"
    )
    cur = con.cursor()
    return con, cur


@app.get("/create")
def create_tables():
    try:
        con, cur = db_connect()
        cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, score INTEGER)")
        con.commit()
        cur.close()
        con.close()
        return "Success"
    except Exception:
        return "Failed"


@app.get("/get/users/new_user")
def insert_user(user_id: int):
    try:
        con, cur = db_connect()
        cur.execute(f"INSERT INTO users VALUES ('{user_id}', '{0}')")
        con.commit()
        con.close()
        return "Success"
    except Exception:
        return "Failed"


@app.get("/get/users/score")
def get_user_score(user_id: int):
    try:
        con, cur = db_connect()
        cur.execute(f"SELECT score FROM users WHERE user_id={user_id}")
        res = cur.fetchone()[0]
        cur.close()
        con.close()
        return res
    except Exception:
        return "Failed"


@app.get("/get/users/top")
def get_user(token: str = Depends(oauth2)):
    try:
        print(token)
        con, cur = db_connect()
        cur.execute(f"SELECT * FROM users ORDER BY score LIMIT 20")
        res = cur.fetchall()
        res_dict = {}
        for j in res:
            res_dict.update({f"user {j[0]}": {"username": j[0], "score": j[1]}})
        con.close()
        return res_dict
    except Exception:
        return "Failed"


@app.get("/update/users/score")
def fff(user_id: int):
    try:
        con, cur = db_connect()
        cur.execute(f"UPDATE users SET score=score+1 WHERE user_id={user_id}")
        cur.close()
        con.close()
        return "Success"
    except Exception:
        return "Failed"
