import streamlit as st 
import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt 

st.title("栄養データ検索サイト")

import streamlit as st
import pandas as pd
import re


# st.set_option('deprecation.showPyplotGlobalUse', False) 
# data = pd.DataFrame({'year': [2015, 2016, 2017, 2018, 2019, 2020], 
# 'sales': [500, 600, 700, 800, 900, 10007] }) 
# st.title('Sales by Year') 
# st.bar_chart(data=data, x='year', y='sales')


# search_term = st.text_input("Search", "")
# data["sales"] = data["sales"].astype(str)
# #search_results = data[data["sales"].str.contains("500")]

# if st.button("button"):
#     search_results = data[data["sales"].str.contains(f"{search_term}")]#data[data["sales"].str.contains(search_term)] 
#     #st.dataframe
#     st.dataframe(search_results)

# # タイトルの表示
# st.title("Streamlitアプリのタイトル")

# # テキストの表示
# st.text("これはテキストです。")

# # ボタンの表示
# if st.button("ボタンをクリック"):
#     st.write("ボタンがクリックされました。")

# # ユーザーからのテキスト入力の取得
# user_input = st.text_input("名前を入力してください。")

# # ユーザーからの数字入力の取得
# user_number = st.number_input("年齢を入力してください。", min_value=0, max_value=100, step=1)

# #一つ目にやること　プロジェクト（Webapp）に移動:cd webapp　*lsで今いる場所が見れる
# #二つ目　venvに移動（activeに）：source web_env(今回のフォルダ名)/bin/activate
# #三つ目　streamlit起動：streamlit run app.py



 #ここから１回目(Kaggleデータ)＿＿＿

# データを読み込む
# df = pd.read_csv("nutrient_energy(Google翻訳後utf8).csv")

# # 正規表現検索ボックスを表示する
# search_term = st.text_input("食品名を入力してください（正規表現使用可）")

# # データをフィルタリングする
# if search_term:
#     pattern = re.compile(search_term)
#     df = df[df['食品名'].str.contains(pattern)]

# # データを表示する
# st.table(df)

# st.bar_chart(df)
#＿＿＿ここまで１回目

#ここから２回目＿＿＿

# 食品データを読み込む
df = pd.read_csv("菓子類1 csv.csv",float_precision='round_trip')

keyword = st.text_input("検索キーワードを入力してください", "")
filtered_df = df[df["食品名"].str.contains(keyword)]

cols = ["エネルギー kcal","たんぱく質 g", "脂質 g", "炭水化物(単糖当量) g", "炭水化物(質量計) g","食物繊維総量 g","食塩相当量 g"]
# 正規表現で数字のみを抽出する関数
def extract_numbers(x):
    numbers = re.findall(r'\d+\.\d+|\d+', str(x))
    if numbers:
        return float(numbers[0])
    else:
        return None

# 数字のみを抽出してfloat型に変換する
df[cols]= df[cols].applymap(extract_numbers)

df=df.fillna(0)
df[cols]=df[cols].abs()


df.to_csv("output.csv", index=False)
df = pd.read_csv( "output.csv",float_precision='round_trip')





# 栄養素のリストを作成する

nutrients = ["エネルギー kcal","たんぱく質 g", "脂質 g", "炭水化物(単糖当量) g", "炭水化物(質量計) g","食物繊維総量 g","食塩相当量 g"]

# ユーザーが入力したキーワードを受け取る

# # ユーザーが選択した栄養素を受け取る
selected_nutrient = st.selectbox("栄養素を選択してください", nutrients)

# フィルタリングされたデータを表示する
filtered_df = df[df["食品名"].str.contains(keyword)][["食品名", selected_nutrient]]
#st.table(filtered_df)
st.dataframe(filtered_df)

# データをグループ化し、棒グラフで表示する
grouped_df = filtered_df.groupby("食品名")[selected_nutrient].sum()
st.bar_chart(grouped_df)