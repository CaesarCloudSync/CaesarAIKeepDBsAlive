import os
import io
import json
import base64
import hashlib
import asyncio 
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesarhash import CaesarHash
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
import json
import asyncio
from CaesarAICronEmail.CaesarAIEmail import CaesarAIEmail
load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("CaesarSQLDB/env.json") as f:
    dbdata = json.load(f)["databases"]


#maturityjwt = CaesarJWT(caesarcrud)

JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
table = "caesaraiworldmodels"


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIWorld!"
@app.post('/makealive')# GET # allow all origins all methods.
async def makealive(data : JSONStructure = {}):
    target_success = len(dbdata)
    result_success = 0
   
    for db in dbdata:
        try:
            caesarcrud = CaesarCRUD(db["HOST"],db["USERNAMESQL"],db["PASSWORD"],db["DBNAME"])
            caesarcreatetables = CaesarCreateTables()
            caesarcreatetables.create(caesarcrud)
            res = caesarcrud.post_data(("firstname","lastname"),("keep","alive"),"keepalive")
            #await asyncio.sleep(1)
            res = caesarcrud.caesarsql.run_command("DROP TABLE keepalive;",result_function=caesarcrud.caesarsql.fetch)
            caesarcrud.caesarsql.disconnect()
            result_success += 1
            
        except Exception as ex:
            CaesarAIEmail.send(email="revisionbankedu@gmail.com",subject=f"{db['DBROLE']} PlanetScale Keep Alive Error - {db['PLANETSCALE_EMAIL']}",message=f"{type(ex)} - {ex}")
    if result_success == target_success:
        if not data.get("quiet"): 
            CaesarAIEmail.send(email="revisionbankedu@gmail.com",subject=f"PlanetScale Keep Alive Success",message=f"Success")
        return {"message":"success"}
    else:
        CaesarAIEmail.send(email="revisionbankedu@gmail.com",subject=f"PlanetScale Keep Alive Error Successful keep alive attempts: {result_success}/{target_success}",message=f"Successful keep alive attempts: {result_success}/{target_success}")
        return {"message":"error"}

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())