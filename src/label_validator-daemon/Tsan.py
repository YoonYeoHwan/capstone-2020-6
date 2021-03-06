import requests
import json
import os
from bson import ObjectId
from mongodb import db
from graphqlclient import GraphQLClient

client = GraphQLClient('http://tsan.tech/v1/graphql')

class Tsan:

    def __init__(self):
        self.token = ""
        self.requests = []

    def login(self, username, password):
        res = client.execute('''
            mutation ($username: String!, $password: String!){
                loginAccount(username: $username, password: $password) {
                    jwt
                }
            }
        ''',
        variables={
            "username": username,
            "password": password
        })
        data = json.loads(res)
        self.token = data['data']['loginAccount']['jwt']
    
    def get_reliability(self, username):
        res = client.execute('''
            mutation ($username: String!, $token: String!){
                updateReliability(
                    username: $username
                    token: $token
                ) {
                    message{
                        status
                        message
                    }
                    reliability
                }
            }
        ''',
        variables={
            "username": username,
            "token": self.token
        })
        data = json.loads(res)
        return data['data']['updateReliability']['reliability']
    
    def get_end_requests(self):
        res = client.execute('''
            query {
                getAllRequest(state: "VER") {
                    message {
                        status
                        message
                    }
                    requests {
                        idx
                        category {
                            idx
                            type
                            name
                        }
                        keywordSet {
                            idx
                            name
                        }
                        state
                        isRewarded
                    }
                }
            }
        ''')
        data = json.loads(res)
        self.requests = data['data']['getAllRequest']['requests']
        return self.requests
    
    def updateLabel(self, request, username, data):
        data_ = data.copy()
        del data_['_id']
        db.user_assigned.find_one_and_update({"request": request, "username": username}, {"$set": data_})
    
    def verifiedRequest(self, request):
        res = client.execute("""        
                mutation ($request: Int!, $token: String!){
                    verifiedRequest(
                        idx: $request
                        token: $token
                    ) {
                        message{
                            status
                            message
                        }
                    }
                }
            """, variables={
                "request": request,
                "token": self.token
            })
        data = json.loads(res)
        return data['data']['verifiedRequest']['message']

    def update_reliability(self, username, reliability):
        res = client.execute('''
            mutation ($token: String!, $username: String!, $reliability: Float!){
                updateReliability(
                    username: $username
                    reliability: $reliability
                    token: $token
                ) {
                    message{
                        status
                        message
                    }
                    reliability
                }
            }
        ''',
        variables={
            "token": self.token,
            "reliability": reliability,
            "username": username
        })
        data = json.loads(res)
        return data['data']['updateReliability']['reliability']
    
    def getLabels(self, request):
        labeled = []
        for label in db.user_assigned.find({"request": int(request['idx'])}):
            label['reliability'] = self.get_reliability(label['username'])
            labeled.append(label)
        return labeled
        # labeled = {}
        # for label in db.user_assigned.find({"request": int(request['idx'])}):
        #     labeled[label['username']] = {
        #         "dataset": {},
        #         "reliability": self.get_reliability(label['username'])
        #     }
        #     for x in label['dataset']:dataset
        #         labeled[label['username']]['dataset'][str(x['data'])] = x['label']
        # return labeled
    
    def save(self, request, answers):
        db.assigned_dataset.update_one(
            {
                "request": int(request)
            },
            {
                "$set":
                {
                    "answers": answers
                }
            }
        )
    
    def assigned_dataset(self, request):
        return db.assigned_dataset.find_one({"request": int(request['idx'])})
    
    def download(self, request):

        folder = "./tmp/%s/"%(request['idx'])

        try:
            os.makedirs(folder)
        except:
            pass

        assigned = db.assigned_dataset.find_one({"request": int(request['idx'])})

        # 이미지인 경우
        if request['category']['type'] == "image":
            i = 0
            files = {}
            for image in assigned['dataset']:
                i += 1
                img = db.image_dataset.find_one({"_id": ObjectId(image)})
                filename = os.path.join(folder, img['filename'])
                f = open(filename, "wb")
                print("[%d/%d] Download %s"%(i, len(assigned['dataset']), img['filename']))
                f.write(img['data'])
                f.close()
                files[str(image)] = filename
            return files

        # 텍스트인 경우
        else:
            i = 0
            files = {}
            for text in assigned['dataset']:
                i += 1
                txt = db.text_dataset.find_one({"_id": ObjectId(text)})
                filename = os.path.join(folder, str(text) + ".json")
                f = open(filename, "w")
                print("[%d/%d] Download %s"%(i, len(assigned['dataset']), filename))
                txt['_id'] = str(txt['_id'])
                json.dump(txt, f)
                f.close()
                files[str(text)] = filename
            return files
