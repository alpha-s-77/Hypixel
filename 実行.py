#ライブラリ
import requests
import os
import json
import datetime
# APIに接続するための情報
get_key = "https://api.hypixel.net/key"
####ここにAPIKEYを入力してください########################
API_key = "INPUT YOUR API KEY"
#########################################################
#ギルドの情報を入手する
print("昨日のGXPスコアを読み込みます。")
data = requests.get(
    url = "https://api.hypixel.net/guild",
    params = {
        "key": API_key,
####ここにギルドネームを入力してください。########################
        "name": "INPUT YOUR GUILD NAME"
#########################################################
    }
).json()

#テキストファイルを読み込む(score.json)
if(os.path.isfile("score.json")):
    print("score.jsonを読込中...")
    with open('score.json') as f:
        score = json.load(f)
else:
    print("ファイルが見つかりませんでした。score.jsonを作成しています.")
    score = {}

#今日の情報を取得
print("取得する日付を入力してください")
print("例) 1->01 / 31->31")
y = input("年>")
m = input("月>")
d = input("日>")

with open("アップロード.bat","w") as f:
    print("")
#GXP5000オーバーの人のスコア+1をする
############################################################
#必要なEXP量(数値)
need = NEED EXP(INT)
############################################################
for i in data['guild']['members']:
    if(i['expHistory'][y+"-"+m+"-"+d]>=need):
        uuid = i["uuid"]
        if(uuid in score.keys()):
            score[uuid]=score[uuid]+1
        else:
            score[uuid]=1
        datas = requests.get(
            url = "https://api.hypixel.net/player",
            params = {
                "key": API_key,
                "uuid": uuid
            }
        ).json()
        with open("アップロード.bat","a") as f:
            f.write(datas["player"]["displayname"]+": " + str(score[uuid])+"\n")
    else:
        uuid = i["uuid"]
        if(uuid in score.keys()):
            datas = requests.get(
                url = "https://api.hypixel.net/player",
                params = {
                    "key": API_key,
                    "uuid": uuid
                }
            ).json()
            with open("アップロード.bat","a") as f:
                f.write(datas["player"]["displayname"]+": " + str(score[uuid])+"\n")

#テキストファイルに書き込む(scote.json)
print("データを書き込み中...")
with open('score.json', 'w') as f:
    json.dump(score, f, indent=4)
##
print(">>> score.jsonを削除することでスコアを初期化します。")