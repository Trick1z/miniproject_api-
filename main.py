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
        database='miniproject'
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
        cnx.commit()
        id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return {"message": 200, "ID": id}

    def put(order: String):
        cnx = get_DB()
        cursor = cnx.cursor()
        cursor.execute(order)
        cnx.commit()
        cursor.close()
        cnx.close()

        return {"status": 200, "msg": 'update has change'}

# service


class Services:
    def time(self):
        # Get current date and time
        current_day_time = datetime.now()
        formatted_time = current_day_time.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time


# Create an instance of Services
service = Services()
# app


class task (BaseModel):
    name: str
    desc: str


@app.post('/post.todolist')
def post_todotask(task: task):
    time = service.time()
    try:
        res = query.post(
            f"INSERT INTO todolist (task_name, task_desc,create_date) VALUES ('{task.name}', '{task.desc}' ,'{time}')")

        return {'msg': res}
    except Exception as e:
        return e


@app.get('/get.todolist')
def get_todotask():

    try:
        # res = query.post(f"SELECT task_name , task_desc FROM todolist WHERE del_frag ='N' AND succ_frag = 'N'")

        res = query.get(
            f"SELECT task_id,task_name, task_desc FROM todolist WHERE del_frag = 'N' AND succ_frag = 'N'")

        return {'data': res}
    except Exception as e:
        return e


@app.get('/get.succ_todolist')
def get_todotask():

    try:
        # res = query.post(f"SELECT task_name , task_desc FROM todolist WHERE del_frag ='N' AND succ_frag = 'N'")

        res = query.get(
            f"SELECT task_name, task_desc , succ_date FROM todolist WHERE del_frag = 'N' AND succ_frag = 'Y' ")

        return {'data': res}
    except Exception as e:
        return e


@app.put('/delete.todolist/{id}')
def delete_todolist(id: int):
    try:
        res = query.put(
            f"UPDATE todolist SET del_frag = 'Y' WHERE task_id = {id}")

        return res
    except Exception as e:
        return e


@app.put('/success.todolist/{id}')
def delete_todolist(id: int):
    time = service.time()
    try:
        res = query.put(
            f"UPDATE todolist SET succ_frag = 'Y' , succ_date = '{time}' WHERE task_id = {id}")

        return res
    except Exception as e:
        return e


@app.put('/edit.todolist/{id}')
def delete_todolist(id: int, task: task):
    try:
        res = query.put(
            f"UPDATE todolist SET task_name = '{task.name}' , task_desc = '{task.desc}' WHERE task_id = {id}")

        return res
    except Exception as e:
        return e
    
    
# chatroom
@app.get('/get.chatroom')
def get_chatroom():
    try:
        
        res = query.get(f"SELECT room_id , room_name , room_desc FROM chatroom WHERE del_frag = 'N'")
        return {"data" : res}
    except Exception as e:
        return e
    

class msg (BaseModel) :
    username:str
    msg: str
    room_id : int    
@app.post('/post.msg')
def post_chatroom(data : msg):
    time = service.time()
    
    try:
        
        res = query.post(f"INSERT INTO chatroom_room (msg_username , msg_msg ,create_date,room_id) VALUES ('{data.username}' , '{data.msg}' , '{time}',{data.room_id}) ")
        return {"data" : res}
    except Exception as e:
        return e
    
@app.get('/get.chats/roomid={id}')
def get_chatroom(id :int):

    try:
        
        res = query.get(f"SELECT msg_username , msg_msg , create_date FROM chatroom_room WHERE del_frag = 'N' AND room_id = {id}")
        return {"data" : res}
    except Exception as e:
        return e

# @app.get('/test')
# def test():
#     res = service.time()
#     return res
