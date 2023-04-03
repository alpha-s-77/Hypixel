# ライブラリ
import requests
import os
import json
import sys


def save_data():
    print("[設定変更]")
    print("APIキーを入力してください。")
    print("APIキーはHypixelサーバーで/api newを入力して入手可能です。")
    apikey = input("API KEY>")
    guild_name = input("ギルド名>")
    need_exp = input("必要なEXP>")
    print("保存しています...")
    data = {"api": apikey, "guild": guild_name, "exp": need_exp}
    with open("設定.json", "w") as f:
        json.dump(data, f, indent=4)
    print("保存完了!")
    print("この後, 例外処理が発生します。再度実行をやり直すことでカウントを開始できます。")


def load_data():
    if os.path.isfile("設定.json"):
        with open('設定.json') as f:
            datas = json.load(f)
            return datas
    else:
        print("ファイルが見つかりませんでした")
        save_data()
        load_data()


def search():
    if os.path.isfile("uuidmcid.json"):
        with open('uuidmcid.json') as f:
            userinfo = json.load(f)
        print("UUIDに[]は含まれません。")
        string = input("検索項目>")
        for uuid, mcid in userinfo.items:
            if mcid in string:
                print(mcid)
                print("UUID: [" + uuid + "] ")
    else:
        print("ファイルが見つかりませんでした")
        print("最初にカウントを実行してください。")


def remove_score():
    uuidch = input("特定の人のUUID>")
    print("1点減点する場合: 1　1点加点する場合: -1です")
    removescore = input("減点するスコア>")
    if os.path.isfile("score.json"):
        print("score.jsonを読込中...")
        with open('score.json') as f:
            score = json.load(f)
        for i in score.keys():
            if i == uuidch:
                score[i] = score[i] - int(removescore)
                if score[i] < 0:
                    print(uuidch + "-- 警告: これを実行したことにより得点は-1以下になりました")
                print("減少させました!")
                print(uuidch + "-->" + str(score[i]) + "pts")
        with open('score.json', "w") as f:
            json.dump(score, f, indent=4)
        print("完了!")
        print("次回のカウント時に反映されます。")
    else:
        print("ファイルが見つかりませんでした。")


def count():
    print("セーブデータをロード中...")
    savedata = load_data()
    api_key = savedata["api"]
    # ギルドの情報を入手する
    data = requests.get(
        url="https://api.hypixel.net/guild",
        params={
            "key": api_key,
            "name": savedata["guild"]
        }
    ).json()

    # テキストファイルを読み込む(score.json)
    if os.path.isfile("score.json"):
        print("score.jsonを読込中...")
        with open('score.json') as f:
            score = json.load(f)
    else:
        print("ファイルが見つかりませんでした。score.jsonを作成しています...")
        score = {}

    # 今日の情報を取得
    print("取得する日付を入力してください")
    print("例) 1->01 / 31->31")
    y = input("年>")
    m = input("月>")
    d = input("日>")

    with open("アップロード.bat", "w"):
        print("")
    # GXP5000オーバーの人のスコア+1をする
    ############################################################
    # 必要なEXP量(数値)
    need = int(savedata["exp"])
    ############################################################
    print("APIから情報を取得し, 条件を確認しています...")
    playerinfo = {}
    count = 0
    total = len(data['guild']['members'])
    for i in data['guild']['members']:
        count += 1
        progress = count / total * 100
        sys.stdout.write(f"\rProgress: [{int(progress)}%] {'='*int(progress/2)}{' '*(50-int(progress/2))}")
        sys.stdout.flush()
        if i['expHistory'][y + "-" + m + "-" + d] >= need:
            uuid = i["uuid"]
            if uuid in str(score.keys()):
                score[uuid] = score[uuid] + 1
            else:
                score[uuid] = 1
            datas = requests.get(
                url="https://api.hypixel.net/player",
                params={
                    "key": api_key,
                    "uuid": uuid
                }
            ).json()
            playerinfo[uuid] = (datas["player"]["displayname"])
            with open("アップロード.bat", "a") as f:
                f.write(datas["player"]["displayname"] + ": " + str(score[uuid]) + "\n")
        else:
            uuid = i["uuid"]
            if uuid in str(score.keys()):
                datas = requests.get(
                    url="https://api.hypixel.net/player",
                    params={
                        "key": api_key,
                        "uuid": uuid
                    }
                ).json()
                playerinfo[uuid] = (datas["player"]["displayname"])
                with open("アップロード.bat", "a") as f:
                    f.write(datas["player"]["displayname"] + ": " + str(score[uuid]) + "\n")
    sys.stdout.write(f"\rProgress: [100%] {'='*50}")
    print("")
    print("uuidとmcidについてそれぞれを紐づけ中...")
    with open("uuidmcid.json", 'w') as f:
        json.dump(playerinfo, f, indent=4)

    # テキストファイルに書き込む(scote.json)
    print("データを書き込み中...")
    with open('score.json', 'w') as f:
        json.dump(score, f, indent=4)
    ##sort開始
    print("並び替え中です...")
    sort_results()
    print("正常にすべての動作を完了しました。")
    print(">>> score.jsonを削除することでスコアを初期化します。")

def sort_results():
    with open('アップロード.bat', 'r') as f:
        lines = f.readlines()

    # プレイヤー名のリストを取得し、アルファベット順にソートする（大文字小文字を区別しない）
    players = [line.split(',')[0].lower() for line in lines]
    sorted_players = sorted(players)

    # 行ごとにプレイヤー名を置換して、アップロード.batファイルに書き込む
    with open('アップロード.bat', 'w') as f:
        for player in sorted_players:
            for line in lines:
                if line.lower().startswith(player):
                    f.write(line)
                    break

def main(args):
    print("[System] 引数を受け取っています...")
    if args[1] == "count":
        count()
    elif args[1] == "option":
        save_data()
    elif args[1] == "remove":
        remove_score()
    elif args[1] == "mcid":
        search()
    else:
        print("引数が無効です。")


if __name__ == "__main__":
    main(sys.argv)
