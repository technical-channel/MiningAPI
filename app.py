# from ntpath import join
from flask import Flask, request
import pymongo
import string
import random
# http://127.0.0.1:5000/query_example?lang=rahul&web=www.rahul.com

weblink = "https://mining-self-vercel.app"
myclient = pymongo.MongoClient("mongodb+srv://dbUser:dEABN9gOCeCBhSgZ@cluster0.gofxaob.mongodb.net/")
mydb = myclient["usdtMining"]
mycol = mydb["invitesLinks"]

app = Flask(__name__)
# CORS(app)   




## For index page
@app.route('/')
def home():
    return "Hello World"


## generateLink
@app.route('/generateLink',methods=['GET','POST']) #http://127.0.0.1:5000/generateLink?userAddress=RAVI
def generateLink():
    userAddress = request.args.get('userAddress').upper()
    all_previous_invite_code = []
    for x in mycol.find():
        all_previous_invite_code.append(x['UnicCode'])

    # random invite code
    while True:
        InviteCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
        if InviteCode not in all_previous_invite_code:
            break
    ## check invite code present or not
    for x in mycol.find({ "Address":userAddress }):
        if x['UnicCode']:
            print("Unic Code Already Present : ",x['UnicCode'])
            link = weblink + "/"+ x['UnicCode']
            print("your link : ", link)
            return link
    else:
        print("Unic Code Not Present, New One Created: ",InviteCode)
        # insert new code in database
        mydict = { "Address": userAddress, "UnicCode": InviteCode, "Used" : False }
        mycol.insert_one(mydict)
        link = weblink + "/"+ InviteCode
        print("your link : ", link)
        return link


# generateLink("CHHIPA")

#joinLink
@app.route('/joinLink',methods=['GET','POST'])
def joinLink(): # http://127.0.0.1:5000/joinLink?joinnerAddress=RAWVI&UnicCode=DOC6TN2
    # http://127.0.0.1:5000/joinLink?joinnerAddress=RAVI&UnicCode=DOC6TN2
    joinnerAddress = request.args.get('joinnerAddress').upper()
    UnicCode = request.args.get('UnicCode').upper()


     ## check invite code present or not
    for x in mycol.find({ "UnicCode":UnicCode }):
        if x['UnicCode']:
            # print("Unic Code Present : ",x['UnicCode'])
            if x['Address'] == joinnerAddress:
                return "False"
            if x['Used'] == True:
                return "False"
            else:
                mycol.update_one({ "Used": "False" }, { "$set": { "Used": "True" } })
                return "True"
    else:
        return "False"


# getAddrByCode
@app.route('/getAddrByCode',methods=['GET','POST'])  #http://127.0.0.1:5000/getAddrByCode?UnicCode=DOC6TN2
def getAddrByCode():
    UnicCode = request.args.get('UnicCode').upper()
    zeroAddr = "0x0000000000000000000000000000000000000000"
    print("Code : ",UnicCode)
    for x in mycol.find({ "UnicCode":UnicCode }):
        print("for loop")
        if x['UnicCode']:
            print("UnicCode is : ",UnicCode)
            return x['Address']
    else:
        return zeroAddr


# getDataset
@app.route('/getDataset',methods=['GET','POST'])
def getDataset(): # http://127.0.0.1:5000/getDataset
    data = ""
    for x in mycol.find({}):
        print(x)
        data += str(x)
    return data


## test
@app.route('/test',methods=['GET','POST'])
def test(): # http://127.0.0.1:5000/test?data=testing%20data
    data = request.args['data'].upper()
    print("Data is : ",data)
    return data


if __name__ == "__main__":
    app.run(debug=True)