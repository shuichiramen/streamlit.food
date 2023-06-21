import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import re

import os
import openai

import settings

# APIキーの設定
openai.api_key = settings.AP


st.title("栄養データ検索サイト")



data = {'年代': ['18-29', '30-49', '50-64'],
        '男性': [2650, 2700, 2600],
        '女性': [2000, 2050, 1950]}
df = pd.DataFrame(data)

# セレクトボックスで性別と年齢範囲を選択
gender = st.selectbox("性別を選んでください", ['男性', '女性'])
age_group = st.selectbox("年代を選んでください", df['年代'].tolist())

# 選択された性別と年齢範囲のデータを抽出
filtered_data = df[(df['年代'] == age_group) & (df[gender] > 0)]

# 抽出されたデータを表示
if not filtered_data.empty:
    st.write("Filtered Data:")
    st.write(filtered_data)
else:
    st.write("No data available for the selected gender and age group.")

# 食品データを読み込む
df = pd.read_csv("菓子類1 csv.csv",float_precision='round_trip')

# ユーザーが入力したキーワードを受け取る
keyword = st.text_input("検索キーワードを入力してください*¹", "")
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


# # ユーザーが選択した栄養素を受け取る
selected_nutrient = st.selectbox("栄養素を選択してください *²", nutrients)

# フィルタリングされたデータを表示する
filtered_df = df[df["食品名"].str.contains(keyword)][["食品名", selected_nutrient]]
# st.table(filtered_df)

# def show_selected_row(row_index):
#     st.write("Selected Row:")
#     st.write(df.iloc[row_index])

# セレクトボックスを表示
selected_row = st.selectbox("Select a row",filtered_df["食品名"])
st.write(selected_row)
# 選択された行を表示
# show_selected_row(selected_row)
filtered_df=df[df["食品名"]==selected_row]


# データをグループ化し、棒グラフで表示する
grouped_df = filtered_df.groupby("食品名")[selected_nutrient].sum()
st.bar_chart(grouped_df)

st.write('*¹日本食品標準成分表2020年版(八訂)参照')
st.write('*²数値は可食部100g当たり')


if st.button("この後何を食べたらよい？"):
    # #試作用サンプルデータ
    protein=1
    th=0.5
    if  protein>th:
        x="タンパク質"
        input=f"{x}が少ない食事を提案してください"
        print("a")
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=1.0,#値が低いとランダム性が高くなる、確率の低いものも出る
        )
        ##openaiのapiを呼び出している
        # response = openai.ChatCompletion.create(
        #     model="text-davinci-003",
        #     messages=[
        #     {"role": "user", "content": "大谷翔平について教えて"},
        #     ],
        # )
        print("b")
    output=completions.choices[0].text#response.choices[0]["message"]["content"].strip()
    #     output=input
    

    st.write(output)
