import requests
import json
import os
from bson import ObjectId
from mongodb import db
from graphqlclient import GraphQLClient

client = GraphQLClient('http://localhost:8000/v1/graphql')

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
    
    def get_end_requests(self):
        res = client.execute('''
            query {
                getAllRequest(state: "END") {
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
            files = []
            for image in assigned['dataset']:
                i += 1
                img = db.image_dataset.find_one({"_id": ObjectId(image)})
                filename = os.path.join(folder, img['filename'])
                f = open(filename, "wb")
                print("[%d/%d] Download %s"%(i, len(assigned['dataset']), img['filename']))
                f.write(img['data'])
                f.close()
                files.append(filename)
            return files
        # 텍스트인 경우
        else:
            pass