import os
import json
import streamlit as st
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
plt.rcParams['font.family'] = 'sans-serif'

# --- ゾロリ書籍リスト ---
books = [
    "かいけつゾロリのドラゴンたいじ", "かいけつゾロリのきょうふのやかた", "かいけつゾロリのまほうつかいのでし",
    "かいけつゾロリの大かいぞく", "かいけつゾロリのゆうれいせん", "かいけつゾロリのチョコレートじょう",
    "かいけつゾロリの大きょうりゅう", "かいけつゾロリのきょうふのゆうえんち", "かいけつゾロリのママだーいすき",
    "かいけつゾロリの大かいじゅう", "かいけつゾロリのなぞのうちゅうじん", "かいけつゾロリのきょうふのプレゼント",
    "かいけつゾロリのなぞなぞ大さくせん", "かいけつゾロリのきょうふのサッカー", "かいけつゾロリつかまる!!",
    "かいけつゾロリとなぞのひこうき", "かいけつゾロリのおばけ大さくせん", "かいけつゾロリのにんじゃ大さくせん",
    "かいけつゾロリけっこんする!?", "かいけつゾロリ大けっとう!ゾロリじょう", "かいけつゾロリのきょうふのカーレース",
    "かいけつゾロリのきょうふの大ジャンプ", "かいけつゾロリの大金持ち", "かいけつゾロリのテレビゲームききいっぱつ",
    "かいけつゾロリのきょうふの宝さがし", "かいけつゾロリちきゅうさいごの日", "かいけつゾロリのめいたんていとうじょう",
    "かいけつゾロリぜったいぜつめい", "かいけつゾロリのきょうふのカーニバル", "かいけつゾロリあついぜ!ラーメンたいけつ",
    "かいけつゾロリのてんごくとじごく", "かいけつゾロリのじごくりょこう", "かいけつゾロリのようかい大リーグ",
    "かいけつゾロリとなぞのまほう少女", "かいけつゾロリとまほうのへや", "かいけつゾロリたべられる!!",
    "かいけつゾロリの大どろぼう", "かいけつゾロリのなぞのおたから大さくせん前編", "かいけつゾロリのなぞのおたから大さくせん後編",
    "かいけつゾロリまもるぜ！きょうりゅうのたまご", "かいけつゾロリたべるぜ!大ぐいせんしゅけん",
    "かいけつゾロリやせるぜ！ダイエット大さくせん", "かいけつゾロリカレー VS ちょうのうりょく",
    "かいけつゾロリイシシ・ノシシ大ピンチ!!", "かいけつゾロリきょうふのちょうとっきゅう",
    "かいけつゾロリきょうふのようかいえんそく", "かいけつゾロリのだ・だ・だ・だいぼうけん!前編",
    "かいけつゾロリのだ・だ・だ・だいぼうけん!後編", "かいけつゾロリのはちゃめちゃテレビ局",
    "かいけつゾロリはなよめとゾロリじょう", "かいけつゾロリのメカメカ大さくせん",
    "かいけつゾロリなぞのスパイとチョコレート", "かいけつゾロリなぞのスパイと100本のバラ",
    "かいけつゾロリのまほうのランプ〜ッ", "かいけつゾロリの大まじんを探せ!!", "かいけつゾロリのクイズ王",
    "かいけつゾロリのようかい大うんどうかい", "消えた!?かいけつゾロリ", "かいけつゾロリのおいしい金メダル",
    "かいけつゾロリの王子さまになるほうほう", "かいけつゾロリのかいていたんけん", "かいけつゾロリのちていたんけん",
    "かいけつゾロリのドラゴンたいじ2", "かいけつゾロリロボット大さくせん", "かいけつゾロリうちゅう大さくせん",
    "かいけつゾロリスターたんじょう", "かいけつゾロリのレッドダイヤをさがせ!!", "かいけつゾロリきょうふのエイリアン",
    "かいけつゾロリのゾワゾワゾクゾクようかいまつり", "かいけつゾロリきょうふのダンジョン",
    "かいけつゾロリにんじゃおばけあらわる！", "かいけつゾロリきょうりゅうママをすくえ!",
    "かいけつゾロリいきなり王さまになる？", "かいけつゾロリノシシいきなり王さまになる！",
    "かいけつゾロリいただき!! なぞのどデカダイアモンド"
]

st.set_page_config(page_title="ゾロリ読書記録", layout="centered")
st.title("📚 かいけつゾロリ 読書メーター")

# グラフ描画用のプレースホルダーを作成
graph_placeholder = st.empty()
count_placeholder = st.empty()

# Google Sheets から読了データを読み込む
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gspread"], scope)
client = gspread.authorize(creds)

# シート名: "zorori_read_status"
sheet = client.open("zorori_read_status").sheet1
# Google Sheets から読了データを読み込む（初回のみ）
if "read_status" not in st.session_state:
    values = sheet.col_values(1)
    if values:
        st.session_state.read_status = [v == "TRUE" for v in values]
    else:
        st.session_state.read_status = [False] * len(books)

updated_read_status = []
for i, title in enumerate(books):
    checked = st.checkbox(f"{i+1}巻: {title}", value=st.session_state.read_status[i], key=f"book_{i}")
    updated_read_status.append(checked)
st.session_state.read_status = updated_read_status

# Google Sheets へ保存
sheet.update('A1:A{}'.format(len(books)), [[str(v)] for v in st.session_state.read_status])

# 読了冊数とグラフを即時反映
read_count = sum(st.session_state.read_status)
unread_count = len(books) - read_count

fig, ax = plt.subplots()
colors = ['#87cefa', '#dcdcdc']
ax.pie(
    [read_count, unread_count],
    labels=["Read", "Unread"],
    colors=colors,
    startangle=90,
    wedgeprops=dict(width=0.4)
)
ax.axis("equal")

graph_placeholder.pyplot(fig)
count_placeholder.subheader(f"✅ {len(books)}冊中 {read_count}冊 読了！")
