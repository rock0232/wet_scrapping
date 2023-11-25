import json
import os
import pypyodbc
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template  # , request, session, redirect
import pyodbc

app = Flask(__name__)
connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};Server=DESKTOP-0SBGOOB;Database=rockdatabase;Trusted_Connection=yes'


@app.route("/", methods=['GET'])
def home():
    return render_template("customer.html", returnValue='hello')


@app.route("/register", methods=['POST'])
def register():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    if request.method == "POST":
        returnValue = 0
        fname = request.form.get('First-Name')
        lname = request.form.get('Last-Name')
        useremail = request.form.get('Email')
        userphone = request.form.get('Phone')
        usercity = request.form.get('City')
        isdelete = 1

        if fname and lname and useremail and userphone and usercity and isdelete is not None:
            # print(fname)
            # print(lname)
            # print(useremail)
            # print(userphone)
            # print(usercity)
            # print(isdelete)
            # data = cursor.procedures("[dbo].[registeruser]")
            sql = """\
            SET NOCOUNT ON;
            EXEC [rockdatabase].[dbo].[RegisterUser] ?, ?, ?, ?, ?, ?, ?;
            """
            values = (fname, lname, useremail, usercity, userphone, returnValue, isdelete)
            # cursor.execute("""call [rockdatabase].[dbo].[RegisterUser] ?, ?, ?, ?, ?, ?;""",(fname, lname, useremail, usercity,userphone,returnValue))
            cursor.execute(sql, values)
            returnValue = (cursor.fetchval())
            print(returnValue)
            cursor.commit()
            cursor.close()
            connection.close()

            # Process the return value
            if returnValue == 1011:
                returnValue = "User already exists."
            elif returnValue == 111:
                returnValue = "User registered successfully."
            else:
                returnValue = "An error occurred."

            return render_template("customer.html", returnValue=returnValue)
        else:
            return render_template("customer.html", returnValue="Please Enter Value")
    else:
        return redirect("/")


@app.route("/record")
def displayrecord():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute("select * from tblcustomer where isdeleted = 0")
    records = cursor.fetchall()
    cursor.commit()
    cursor.close()
    connection.close()
    return render_template("record.html", records=records)


@app.route("/delete/<string:id>", methods=['POST'])
def deleterecord(id):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute(f"update tblcustomer set isdeleted = 1 where ID = '{id}'")
    # cursor.execute("select * from tblcustomer where isdeleted = 0")
    # records = cursor.fetchall()
    cursor.commit()
    cursor.close()
    connection.close()
    # return render_template("record.html", records=records)
    return render_template("response.html", returnValue="record deleted successfully")


if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
