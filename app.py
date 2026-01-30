import streamlit as st
import google.generativeai as genai
import fitz

# 設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

st.title("📊 原価計算AIクイズ")
f = st.file_uploader("PDFをアップロード", type="pdf")

if f:
    doc = fitz.open(stream=f.read(), filetype="pdf")
    text = "".join([p.get_text() for p in doc])
    if st.button("クイズを生成"):
        res = model.generate_content(f"以下の資料から3問クイズを作って：{text}")
        st.write(res.text)
