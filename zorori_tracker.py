import streamlit as st
import matplotlib.pyplot as plt

# --- ゾロリ書籍リスト ---
books = [
    "かいけつゾロリのドラゴンたいじ", "かいけつゾロリのきょうふのやかた", "かいけつゾロリのまほうつかいのでし",
    # ...（中略）...
    "かいけつゾロリいただき!! なぞのどデカダイアモンド"
]

st.set_page_config(page_title="ゾロリ読書記録", layout="centered")
st.title("📚 一真くんの かいけつゾロリ 読書記録")

# 状態保存（読了チェック）
if "read_status" not in st.session_state:
    st.session_state.read_status = [False] * len(books)

# 読書進捗を集計
read_count = sum(st.session_state.read_status)
unread_count = len(books) - read_count
rate = read_count / len(books)

st.subheader(f"✅ {len(books)}冊中 {read_count}冊 読了！")

# --- ドーナツグラフの描画 ---
fig, ax = plt.subplots()
colors = ['#87cefa', '#dcdcdc']  # 青 / 灰
ax.pie(
    [read_count, unread_count],
    labels=["読んだ", "未読"],
    colors=colors,
    startangle=90,
    wedgeprops=dict(width=0.4)  # ドーナツにする
)
ax.axis("equal")  # 円形にする
st.pyplot(fig)

# --- チェックリストの表示 ---
for i, title in enumerate(books):
    st.session_state.read_status[i] = st.checkbox(
        f"{i+1}巻: {title}",
        value=st.session_state.read_status[i]
    )