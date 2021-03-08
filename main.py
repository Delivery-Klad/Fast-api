from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import *
import psycopg2
import datetime


app = FastAPI()


def db_connect():
    con = psycopg2.connect(
        host="ec2-52-213-167-210.eu-west-1.compute.amazonaws.com",
        database="d2c0pa2od76s0h",
        user="ygfmgmclajbdwt",
        port="5432",
        password="75047d007fbada55ac72abf0f233aeefe1f6109f8ccfcc669d59cd537f15b675"
    )
    cur = con.cursor()
    return con, cur


@app.get("/api/reports")
def get_all_reports(sorted_by: Optional[str] = None):
    return {'id': '#present',
            'date': '#present',
            'archived': False,
            'assignees': {'reporter': '', 'implementer': ''},
            'text': "some text"}


@app.post("/api/reports")
def create_report(text: Text, implementer: Optional[str] = None):
    if text.text == '' or text.text is None:
        return JSONResponse(status_code=400)
    report = Assignees
    report.Implementer = implementer if implementer else ""
    report.Reporter = ""
    return {'id': '123',
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'archived': False,
            'assignees': {'reporter': report.Reporter, 'implementer': report.Implementer},
            'text': text.text}


@app.get("/api/reports/archived")
def get_archived_reports():
    connect, cursor = db_connect()
    cursor.close()
    connect.close()


@app.get("/api/reports/{employee}")
def get_report(employee, dateBegin: Optional[str] = None, dateEnd: Optional[str] = None):
    pass


@app.get("/api/reports/{id}")
def get_report(id):
    pass


@app.put("/api/reports/{id}")
def update_report(id):
    pass


@app.delete("/api/reports/{id}")
def delete_report(id):
    pass


"""
("/api/reports/employee/{employee}", getEmployeeReports).Methods("GET").Queries("dateBegin","{dateBegin}", "dateEnd", "{dateEnd}")
("/api/reports/employee/{employee}", getEmployeeReports).Methods("GET")
"""
