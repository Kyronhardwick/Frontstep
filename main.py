from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
import os
from dotenv import load_dotenv, dotenv_values


dbpassword=os.environ.get('DB_PASSWORD')
dbhost=os.environ.get('DB_HOST')
dbuser=os.environ.get('DB_USER')
db=os.environ.get('DB')

# MySQL connection
mydb = mysql.connector.connect(
  host=dbhost,
  user=dbuser,
  password=dbpassword,
  database=db)

myfirst=os.environ.get('DB_PASSWORD')
print(myfirst)
cursor = mydb.cursor()

app = FastAPI()

# Contact Pydantic model
class Contact(BaseModel):
    idcontact:int
    contactname:str
    contactemail:str
    contactdate:str
    contactinfo: str
   

# Get all students
@app.get("/Contacts")
def get_contact():
    cursor.execute("SELECT * FROM frontstep.contact")
    contacts = cursor.fetchall()
    print(myfirst)
    return {"contacts": contacts}

@app.get("/Contacts/{id}")
def get_contact_by_id(id:int):
    cursor.execute("SELECT * FROM frontstep.contact where idcontact=%s",(id,))
    contacts = cursor.fetchone()
    return {"contacts": contacts}

@app.post("/Contacts/")
def post_contact(contacts:Contact):
    cursor.execute("insert into frontstep.contact (idcontact,contactname,contactemail,contactdate,contactinfo)values (%s,%s,%s,%s,%s)",(contacts.idcontact,contacts.contactname,contacts.contactemail,contacts.contactdate,contacts.contactinfo))
    mydb.commit()
    return {"contacts": contacts}

@app.delete("/Contacts/{id}")
def delete_contact(id:int):
  """Deletes a contact based on their ID"""
  cursor.execute("DELETE FROM frontstep.contact WHERE idcontact = %s", (id,))
  mydb.commit()
  return {"message": f"Contact with ID {id} deleted successfully."}


@app.put("/Contacts/")
def update_contact(contacts:Contact):
    cursor.execute("UPDATE frontstep.contact set idcontact = %s, contactname = %s, contactemail = %s, contactdate = %s, contactinfo = %s where idcontact = %s",(contacts.idcontact,contacts.contactname,contacts.contactemail,contacts.contactdate,contacts.contactinfo,contacts.idcontact))
    mydb.commit()
    return {"message": "Contact with ID updated successfully."}