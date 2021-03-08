from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import *
import psycopg2
import datetime
import os

app = FastAPI()


def db_connect():
    con = psycopg2.connect(
        host="ec2-52-213-167-210.eu-west-1.compute.amazonaws.com",
        database=os.environ.get("DB"),
        user=os.environ.get("DB_user"),
        port="5432",
        password=os.environ.get("DB_pass")
    )
    cur = con.cursor()
    return con, cur


def error_log(error):  # просто затычка, будет дописано
    try:
        print(error)
    except Exception as e:
        print(e)
        print("Возникла ошибка при обработке errorLog (Это вообще как?)")


@app.get("/api/reports")
def get_all_reports(sorted_by: Optional[str] = None):
    try:
        connect, cursor = db_connect()
        order = f" ORDER BY {sorted_by}" if sorted_by else ""
        cursor.execute(f"SELECT * FROM reports{order}")
        res = cursor.fetchall()
        res_dict = {}
        for j in res:
            res_dict.update({"id": j[0], "date": j[1], "title": j[2], "archived": j[3],
                             "assigners": {"reporter": j[4], "implementer": j[5]}, "text": j[6]})
        cursor.close()
        connect.close()
        return res_dict
    except Exception as e:
        error_log(e)


@app.post("/api/reports")
def create_report(text: Text, implementer: Optional[str] = None):
    try:
        if text.text == '' or text.text is None:
            return JSONResponse(status_code=400)
        connect, cursor = db_connect()
        cursor.execute("SELECT MAX(id) FROM reports")
        try:
            report_id = int(cursor.fetchone()[0]) + 1
        except:
            report_id = 0
        report = Assignees
        report.Implementer = implementer if implementer else ""
        report.Reporter = ""
        date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        archived = False
        title = text.title
        cursor.execute(f"INSERT INTO reports VALUES({report_id}, to_timestamp('{date}', 'DD.MM.YYYY HH24:MI:SS'), "
                       f"{title}, {archived}, '{report.Reporter}', '{report.Implementer}', '{text.text}')")
        connect.commit()
        cursor.close()
        connect.close()
        return {"id": report_id,
                "date": date,
                "title": title,
                "archived": archived,
                "assignees": {"reporter": report.Reporter, "implementer": report.Implementer},
                "text": text.text}
    except Exception as e:
        error_log(e)


@app.get("/api/reports/archived")
def get_archived_reports():
    try:
        connect, cursor = db_connect()
        cursor.execute(f"SELECT * FROM reports WHERE archived=true")
        res = cursor.fetchall()
        res_dict = {}
        for j in res:
            res_dict.update({"id": j[0], "date": j[1],  "title": j[2], "archived": j[3],
                             "assigners": {"reporter": j[4], "implementer": j[5]}, "text": j[6]})
        cursor.close()
        connect.close()
        return res_dict
    except Exception as e:
        error_log(e)


@app.get("/api/reports/{employee}")
def get_report(employee, dateBegin: Optional[str] = None, dateEnd: Optional[str] = None):
    try:
        connect, cursor = db_connect()
        begin = f" and date>to_timestamp('{dateBegin}', 'DD.MM.YYYY HH24:MI:SS')" if dateBegin else ""
        end = f" and date>to_timestamp('{dateEnd}', 'DD.MM.YYYY HH24:MI:SS')" if dateEnd else ""
        cursor.execute(f"SELECT * FROM reports WHERE implementer='{employee}'{begin}{end}")
        res = cursor.fetchall()
        res_dict = {}
        for j in res:
            res_dict.update({"id": j[0], "date": j[1], "title": j[2], "archived": j[3],
                             "assigners": {"reporter": j[4], "implementer": j[5]}, "text": j[6]})
        cursor.close()
        connect.close()
        return res_dict
    except Exception as e:
        error_log(e)


@app.get("/api/reports/{id}")
def get_report(id):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"SELECT * FROM reports WHERE id={id}")
        res = cursor.fetchone()
        cursor.close()
        connect.close()
        return {"id": res[0],
                "date": res[1],
                "title": res[2],
                "archived": res[3],
                "assignees": {"reporter": res[4], "implementer": res[5]},
                "text": res[6]}
    except Exception as e:
        error_log(e)


@app.put("/api/reports/{id}")
def update_report(text: Text, id):
    try:
        if text.text == '' or text.text is None:
            return JSONResponse(status_code=400)
        connect, cursor = db_connect()
        cursor.execute(f"UPDATE reports SET text='{text}' WHERE id={id}")
        connect.commit()
        cursor.execute(f"SELECT * FROM reports WHERE id={id}")
        res = cursor.fetchone()
        cursor.close()
        connect.close()
        return {"id": res[0],
                "date": res[1],
                "title": res[2],
                "archived": res[3],
                "assignees": {"reporter": res[4], "implementer": res[5]},
                "text": res[6]}
    except Exception as e:
        error_log(e)


@app.delete("/api/reports/{id}")
def delete_report(id):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"DELETE FROM reports WHERE id={id}")
        connect.commit()
        cursor.close()
        connect.close()
        return "some body"
    except Exception as e:
        error_log(e)
