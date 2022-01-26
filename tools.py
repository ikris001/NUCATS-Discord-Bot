import re
import discord
from discord.ext import commands
import mysql.connector
from mysql.connector import Error

log_channel = 872913487247052890

async def queryInsert(string):
    try:
        connection = mysql.connector.connect(host='*Removed so it can be uploaded on github*',
                                             database='*Removed so it can be uploaded on github*',
                                             user='*Removed so it can be uploaded on github*',
                                             password='*Removed so it can be uploaded on github*')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(string)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into table")
            cursor.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
            
async def querySelect(string):
    try:
        connection = mysql.connector.connect(host='*Removed so it can be uploaded on github*',
                                             database='*Removed so it can be uploaded on github*',
                                             user='*Removed so it can be uploaded on github*',
                                             password='*Removed so it can be uploaded on github*')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(string)
            result = cursor.fetchall()
            return result
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

async def log(client, value):
    l = client.get_channel(log_channel)
    await l.send(str(value))

async def checkUniversityUsername(m):
    if len(m) != 8:
        return False
    regex = r'^([A-C|a-c])\d{7}$'
    if re.match(regex, m):
        return True
    else:
        return False

async def userInputDM(client, ctx, str):
    while True:
        msg = await client.wait_for("message")
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if msg.content.lower() == str.lower() or re.match(str, msg.content.lower()):
                break
            else:
                await ctx.author.send("Invalid input, please try again")
    return msg
