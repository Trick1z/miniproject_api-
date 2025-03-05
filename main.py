from typing import Union
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, File, Response, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os
import base64
from dateutil import parser
import pytz
import io
import csv
from openpyxl import load_workbook
import hashlib
from bs4 import BeautifulSoup
load_dotenv()


# get DB
def get_DB():
    # deploy docker
    # connector = mysql.connector.connect(
    #     host='host.docker.internal',
    #     user='root',
    #     database='mydb'
    # )

    # localhost
    connector = mysql.connector.connect(
        host='localhost',
        user='root',
        database='games_news'
    )

    return connector


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # Angular's dev server runs on port 4200
    allow_origins=["*", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class query():
    def get(order: str):
        cnx = get_DB()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(order)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return rows

    def post(order: str):
        cnx = get_DB()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(order)

        # rows = cursor.fetchall()
        # cursor.close()
        # cnx.close()
#
        # cnx.commit()
        # cursor.close()
        # cnx.close()
#
        # cnx.commit()
        # id = cursor.lastrowid
        # cursor.close()
        # cnx.close()
        # return {"message": 200, "ID": id}

    def put(order: String):
        cnx = get_DB()
        cursor = cnx.cursor()
        cursor.execute(order)
        cnx.commit()
        cursor.close()
        cnx.close()

        return {"status": 200, "msg": 'update has change'}

