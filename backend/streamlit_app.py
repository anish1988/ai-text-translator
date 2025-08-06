import streamlit as st
import pandas as pd
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="LLM Translator", layout="wide")
st.title("🌍 LLM-based Text Translator")

# 🧠 Session state initialization
if "results" not in st.session_state:
    st.session_state["results"] = []

# 1️⃣ Language selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From Language", ["auto", "en", "fr", "es", "de"])
with col2:
    target_lang = st.selectbox("To Language", ["hi", "bn", "mr", "ta", "te", "fr", "es", "de", "tr"])

st.markdown("---")

mode = st.radio("Choose Input Mode", ["📝 Enter Text", "📁 Upload File"])

if mode == "📝 Enter Text":
    text_input = st.text_area("Enter Text (one sentence per line)", height=200)
    if st.button("Translate Text"):
        lines = [line.strip() for line in text_input.strip().split("\n") if line.strip()]
        if not lines:
            st.warning("⚠️ Please enter some text to translate.")
        else:
            st.session_state["results"] = []  # clear previous
            with st.status("🚀 Translating text...", expanded=True) as status:
                for idx, line in enumerate(lines, start=1):
                    st.write(f"🔄 Translating line {idx}: `{line}`")
                    try:
                        response = requests.post(f"{API_BASE}/translate/text", json={
                            "text": line,
                            "target_language": target_lang
                        })
                        translated = response.json().get("translation", "❌ Error")
                        st.session_state["results"].append({
                            "Sr. No": idx,
                            "Original Text": line,
                            "Translated Text": translated
                        })
                        st.success(f"✅ Line {idx} translated.")
                    except Exception as e:
                        st.error(f"❌ Error translating line {idx}: {e}")
                status.update(label="✅ Translation complete!", state="complete")

elif mode == "📁 Upload File":
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        col = st.selectbox("Select column to translate", df.columns)
        if st.button("Translate File"):
            st.session_state["results"] = []  # clear previous
            with st.status("🚀 Translating file content...", expanded=True) as status:
                for idx, text in enumerate(df[col].dropna().tolist(), start=1):
                    st.write(f"🔄 Translating row {idx}: `{text}`")
                    try:
                        response = requests.post(f"{API_BASE}/translate/text", json={
                            "text": text,
                            "target_language": target_lang
                        })
                        translated = response.json().get("translation", "❌ Error")
                        st.session_state["results"].append({
                            "Sr. No": idx,
                            "Original Text": text,
                            "Translated Text": translated
                        })
                        st.success(f"✅ Row {idx} translated.")
                    except Exception as e:
                        st.error(f"❌ Error translating row {idx}: {e}")
                status.update(label="✅ File translation complete!", state="complete")

# 3️⃣ Display Result
results = st.session_state["results"]

if results:
    df_result = pd.DataFrame(results)
    st.success("✅ Translation Completed!")
    st.dataframe(df_result, use_container_width=True)

    csv = df_result.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name="translated_output.csv", mime="text/csv")

# 4️⃣ SQL Generation (offline preview)
if results:
    with st.expander("🧾 Generate MySQL Insert Queries", expanded=True):
        table_name = st.text_input("Table Name", value="language_translation_table")
        lang_id = st.text_input("Target Language ID", value="9")

        if st.button("🛠 Generate SQL Statements"):
            st.subheader("📄 SQL Insert Statements")
            for row in results:
                original = row["Original Text"].replace("'", "\\'")
                translated = row["Translated Text"].replace("'", "\\'")
                insert_stmt = (
                    f"INSERT INTO {table_name} (language_id, original_text, translated_text) "
                    f"VALUES ({lang_id}, '{original}', '{translated}');"
                )
                st.code(insert_stmt, language="sql")
else:
    st.info("ℹ️ No translations to show yet. Submit some text or upload a file.")
