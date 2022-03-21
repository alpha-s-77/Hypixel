#ライブラリ
import requests
import os
import json
import sys
def main(args):
    print("CMD.EXEからの引数を受け取っています...")
    if(args[1]=="count"):
        count()
    elif(args[1]=="option"):
        savedata()
    elif(args[1]=="remove"):
        removescore()
    elif(args[1]=="mcid"):
        search()

def savedata():
    print("[設定変更]")
    print("APIKEYを入力してください。")
    print("APIキーはHypixelサーバーで/api newを入力して入手可能です。")
    API_Key = input("API KEY>")
    guild_name = input("ギルド名>")
    NEED_EXP = input("必要なEXP>")
    print("保存しています...")
    savedata = {"api":API_Key,"guild":guild_name,"exp":NEED_EXP}
    with open("設定.json","w") as f:
        json.dump(savedata, f, indent=4)
    print("保存完了!")
    print("")
def loaddata():
    if(os.path.isfile("設定.json")):
        with open('設定.json') as f:
            savedatas = json.load(f)
            return savedatas
    else:
        print("ファイルが見つかりませんでした")
        savedata()
        loaddata()
def search():
    if(os.path.isfile("uuidmcid.json")):
        with open('uuidmcid.json') as f:
            userinfo = json.load(f)
        print("UUIDに[]は含まれません。")
        string = input("検索項目>")
        for uuid, mcid in userinfo.items:
            if mcid in string:
                print(mcid)
                print("UUID: ["+uuid+"] ")
    else:
        print("ファイルが見つかりませんでした")
        print("最初にカウントを実行してください。")

def removescore():
    uuidch=input("特定の人のUUID>")
    print("1点減点する場合: 1　1点加点する場合: -1です")
    removescore=input("減点するスコア>")
    if(os.path.isfile("score.json")):
        print("score.jsonを読込中...")
        with open('score.json') as f:
            score = json.load(f)
            for i in score.keys():
                if(i==uuidch):
                    score[i]-=int(removescore)
        with open('score.json',"w") as f:
            json.dump(score, f, indent=4)
        print("完了!")
    else:
        print("ファイルが見つかりませんでした。")
def count():
    print("セーブデータをロード中...")
    savedata =loaddata()
    API_key =savedata["api"]
    #ギルドの情報を入手する
    data = requests.get(
        url = "https://api.hypixel.net/guild",
        params = {
            "key": API_key,
            "name":savedata["guild"]
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
    need = int(savedata["exp"])
    ############################################################
    playerinfo = {}
    for i in data['guild']['members']:
        if(i['expHistory'][y+"-"+m+"-"+d]>=need):
            uuid = i["uuid"]
            if(uuid in score,keys):
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
            playerinfo[uuid]=(datas["player"]["displayname"])
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
                playerinfo[uuid]=(datas["player"]["displayname"])
                with open("アップロード.bat","a") as f:
                    f.write(datas["player"]["displayname"]+": " + str(score[uuid])+"\n")
                    
    with open("uuidmcid.json",'w') as f:
        json.dump(playerinfo,f,indent=4)

    #テキストファイルに書き込む(scote.json)
    print("データを書き込み中...")
    with open('score.json', 'w') as f:
        json.dump(score, f, indent=4)
    ##
    print(">>> score.jsonを削除することでスコアを初期化します。")
if(__name__=="__main__"):
    main(sys.argv)

