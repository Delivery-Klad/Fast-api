from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2


class User(BaseModel):
    username: str
    name: str
    surname: str
    group: str
    user_id: int


app = FastAPI()


def db_connect():
    con = psycopg2.connect(
        host="ec2-52-70-67-123.compute-1.amazonaws.com",
        database="d68nmk23reqak4",
        user="egnnjetsqjwwji",
        port="5432",
        password="dcf3bd216bd19303409eb66b094b902d35610feb0fab452eb46365592829061b"
    )
    cur = con.cursor()
    return con, cur


@app.post("/users/insert")
def insert_user(user: User):
    con, cur = db_connect()
    cur.execute(f"INSERT INTO users VALUES ('{user.username}', '{user.name}', '{user.surname}',"
                f"'{user.group}', {user.user_id})")
    con.commit()
    con.close()
    return user


@app.get("/users/del/{user_id}")
def delete_user(user_id: int):
    con, cur = db_connect()
    cur.execute(f"DELETE FROM users WHERE ids={user_id}")
    con.commit()
    con.close()
    return "Success"


@app.get("/users/get/{user_id}")
def get_user(user_id: int):
    con, cur = db_connect()
    cur.execute(f"SELECT * FROM users WHERE ids={user_id}")
    res = cur.fetchall()
    res_dict = {}
    for j in res:
        res_dict.update({f"user {j[0]}": {"username": j[0], "name": j[1], "surname": j[2],
                                          "group": j[3], "user_id": j[4]}})
    con.close()
    return res_dict


@app.get("/users/get")
def get_users():
    con, cur = db_connect()
    cur.execute("SELECT * FROM users")
    res = cur.fetchall()
    _dict = [{"user": "null"}]
    for j in range(len(res)):
        res_dict = {"username": res[j][0], "name": res[j][1], "surname": res[j][2], "group": res[j][3],
                    "user_id": res[j][4]}
        _dict[j]["user"] = res_dict
        _dict.append({"user": "null"})
    con.close()
    return _dict[:-1]
