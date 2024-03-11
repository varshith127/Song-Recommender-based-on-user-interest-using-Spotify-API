from dotenv import load_dotenv
import os
from requests import post , get
import base64
import json
from flask import Flask , render_template
# from views import views


# app.register_blueprint(views, url_prefix = "/")

 
load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" :  "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url,headers = headers,data = data)
    json_result=json.loads(result.content)
    token = json_result["access_token"]
    return token

def auth_header(token):
    return {"Authorization" : "Bearer " + token}

def search_artist(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url,headers = headers)
    json_result=json.loads(result.content)["artists"]["items"]

    if( len(json_result) == 0 ):
        print("NOT FOUND!!")
        return None
    return json_result[0]

def related_artists(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = auth_header(token)
    headers["Content-Type"] = "application/json"
    # print(headers)
    result = get(url,headers = headers)
    json_result=json.loads(result.content)["artists"]
    return(json_result)


token = get_token()
artist = input("Enter the name of Artist: ")
search = search_artist(token,artist)
artist_id = search["id"]
artist_image = search["images"][0]["url"]
recommended_artists = related_artists(token,artist_id)



urls=[]
for index,art in enumerate(recommended_artists):
    print(f"{index+1}. {art['name']}")
    urls.append(art["images"][0]["url"])
    if(index==4):
        break   

# print(urls)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",url = artist_image,name = "Varshith")

if __name__ == '__main__':
    app.run(debug=False, port=8000)
