import requests
import json
import pandas as pd
import datetime

with open("reddit/reddit_credentials.json", "r") as file:
    creds = json.load(file)

APCA_API_KEY_ID = creds['CLIENT_ID']
APCA_API_SECRET_KEY = creds['CLIENT_SECRET']
password = creds['PASSWORD']

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'lilaoshidezhongwenke',
        'password': password}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/wallstreetbets/top/?t=all",
                   headers=headers)

# for post in res.json()['data']['children']:
#     print(post['data']['title'])
df = pd.DataFrame()  # initialize dataframe

# loop through each post retrieved from GET request
for post in res.json()['data']['children']:
    # append relevant data to dataframe
    # print(json.dumps(post, indent=4))
    # print(str(datetime.datetime.fromtimestamp(post['data']['created'])))
    # if "2018" in str(datetime.datetime.fromtimestamp(post['data']['created'])):
    # print(datetime.datetime.fromtimestamp(post['data']['created']))
    df = pd.concat(
        [df, pd.DataFrame({'subreddit': [post['data']['subreddit']],
                           'title': [post['data']['title']],
                           'selftext': [post['data']['selftext']],
                           'time': [datetime.datetime.fromtimestamp(
                               post['data']['created'])]})])
    # print(post)
# 'subreddit': post['data']['subreddit'],
# 'title': post['data']['title'],
# 'selftext': post['data']['selftext']
# 'upvote_ratio': post['data']['upvote_ratio'],
# 'ups': post['data']['ups'],
# 'downs': post['data']['downs'],
# 'score': post['data']['score']
# }, ignore_index=True)
# print(post)
# with open("reddit/wallstreetbets_info.json", "w") as file:
#     json.dump(df, file)


df.to_csv("reddit_posts.csv")
