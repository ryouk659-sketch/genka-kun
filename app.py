import streamlit as st
import google.generativeai as genai
import fitz

# 1. APIキーの設定
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYが設定されていません。")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. モデルの指定（最新の2.0 flashを使用）
# もしこれでもNotFoundが出る場合は 'gemini-2.0-flash-lite' に書き換えてみてください
model = genai.GenerativeModel('gemini-2.0-flash')

st.title("📊 原価計算AIクイズ")
st.write("PDFをアップロードして、AIにクイズを作らせよう！")

f = st.file_uploader("資料（PDF）を選択してください", type="pdf")

if f:
    try:
        # PDFの読み込み
        doc = fitz.open(stream=f.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        if st.button("クイズを生成する"):
            with st.spinner("AIが問題を考えています..."):
                # プロンプト（指示）
                prompt = f"以下の原価計算の資料に基づいて、学習用の3択クイズを3問作成してください。解説も付けてください。\n\n資料内容:\n{text[:5000]}" # 文字数制限対策
                
                res = model.generate_content(prompt)
                st.subheader("📝 AI作成クイズ")
                st.write(res.text)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
