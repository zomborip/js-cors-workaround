from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import request as req
import requests as r
import json as j

app = Flask(__name__)
api = Api(app)

urlParser = reqparse.RequestParser()
urlParser.add_argument("url", type=str, help="URL")
urlParser.add_argument("data", type=dict, help="DATA\{\}")

class Test(Resource):
  def get(self):
    return {"msg": "OK"}

class CorsWorkAround(Resource):
  def post(self):
    args = urlParser.parse_args()
    
    if args['url'] is None or args['data'] is None:
      return {"error": 1, "message": "anyad", "msg": "error",
              "reqBody" : args}
    
    h = {'Content-Type': 'application/json'}

    resRaw = r.request("POST", args["url"], headers=h, data=j.dumps(args["data"]))
    resJson = resRaw.json()

    print("*", args["data"])
    print("*", args["url"])

    return {"reqbody":
            {"url": args["url"], 
             "data": args["data"]
             }, "resbody": resJson}
  
  def put(self):
    args = urlParser.parse_args()
    
    if args['url'] is None:
      return {"error": 1, "message": "anyad", "msg": "error",
              "reqBody" : args}
    
    resRaw = r.request("GET", args["url"])
    resJson = resRaw.json()

    return {"resbody": resJson}

    

api.add_resource(Test, "/")
api.add_resource(CorsWorkAround, "/api")

if __name__ == "__main__":
  app.run(debug=True, port=32015)

