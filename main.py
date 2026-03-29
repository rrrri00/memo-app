import json
import os
from datetime import datetime


USER_FILE = "users.json"
MEMO_FILE = "memo.json"

#---------共通処理--------------------------
def load_json(file):
    if os.path.exists(file):
        with open(file,"r",encoding="utf-8") as f:
            return json.load(f)
        return {}

def save_json(file,data):
    with open(file,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

#--------ユーザー処理------------------------
def register():
    users=load_json(USER_FILE)
    username=input("ユーザー名:")
    password=input("パスワード:")

    if username in users:
        print("そのユーザーは既に存在します")
        return None

    users[username]=password
    save_json(USER_FILE,users)
    print("登録完了！ログインしてください")
    return None

def login():
    users=load_json(USER_FILE)
    username=input("ユーザー名:")
    password=input("パスワード:")

    if users.get(username) == password:
        print("ログイン成功！")
        return username
    else:
        print("ログイン失敗")
        return None

#------------メモ処理---------------------
def add_memo(username):
    memos=load_json(MEMO_FILE)
    if memos is None:
        memos = {}
    memo=input("メモ内容:")

    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    memo_text=f"[{now}] {memo}"


    memos.setdefault(username,[]).append(memo_text)
    save_json(MEMO_FILE,memos)
    print("保存しました")

def view_memos(username):
    memos=load_json(MEMO_FILE)
    if memos is None:
        memos = {}  
    user_memos=memos.get(username,[])

    if not user_memos:
        print("メモはありません")
        return
    
    for i, memo in enumerate(user_memos):
        print(f"{i+1}:{memo}")

def delete_memo(username):
    memos=load_json(MEMO_FILE)
    if memos is None:
        memos = {}  
    user_memos=memos.get(username,[])

    view_memos(username)
    if not user_memos:
        return
    num=int(input("削除する番号:"))-1
    if 0 <=num < len(user_memos):
       user_memos.pop(num)
       memos[username]=user_memos
       save_json(MEMO_FILE,memos)
       print("削除しました")

#---------メニュー----------------------
def memo_menu(username):
    while True:
        print("\n1. メモ追加\n2.メモ表示\n3.メモ削除\n4.ログアウト")
        choice=input("選択:")
        if choice=="1":
            add_memo(username)
        elif choice=="2":
            view_memos(username)
        elif choice=="3":
            delete_memo(username)
        elif choice=="4":
            print("ログアウトしました")
            break
        else:
            print("無効な選択です")

#---------メイン----------------------
def main():
    while True:
        print("\n1. ユーザー登録\n2. ログイン\n3. 終了")
        choice = input("選択:")
        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                memo_menu(username)
        elif choice == "3":
            print("終了します")
            break
        else:
            print("無効な選択です")

if __name__ == "__main__":
    main()