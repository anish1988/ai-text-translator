import streamlit as st
import pandas as pd
import requests
from services.mysql_db_service import MySQLDBService
import traceback

from sqlalchemy.sql import text as sql_text  # for raw SQL query generation

API_BASE = "http://localhost:8000"  # or your Docker IP

st.set_page_config(page_title="LLM Translator", layout="wide")
st.title("🌍 LLM-based Text Translator")

# 1️⃣ Language selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From Language", ["auto", "en", "fr", "es", "de"])
with col2:
    target_lang = st.selectbox("To Language", ["hi", "bn", "mr", "ta", "te", "fr", "es", "de","tr"])

st.markdown("---")

# 2️⃣ User input: Text or File
mode = st.radio("Choose Input Mode", ["📝 Enter Text", "📁 Upload File"])
results = []

if mode == "📝 Enter Text":
    text_input = st.text_area("Enter Text (one sentence per line)", height=200)
    if st.button("Translate Text"):
        lines = [line.strip() for line in text_input.strip().split("\n") if line.strip()]
        for idx, line in enumerate(lines, start=1):
            response = requests.post(f"{API_BASE}/translate/text", json={
                "text": line,
                "target_language": target_lang
            })
            translated = response.json().get("translation", "❌ Error")
            results.append({"Sr. No": idx, "Original Text": line, "Translated Text": translated})

elif mode == "📁 Upload File":
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        col = st.selectbox("Select column to translate", df.columns)
        if st.button("Translate File"):
            for idx, text in enumerate(df[col].dropna().tolist(), start=1):
                response = requests.post(f"{API_BASE}/translate/text", json={
                    "text": text,
                    "target_language": target_lang
                })
                translated = response.json().get("translation", "❌ Error")
                results.append({"Sr. No": idx, "Original Text": text, "Translated Text": translated})

# 3️⃣ Display Result
if results:
    df_result = pd.DataFrame(results)
    st.success("✅ Translation Completed!")
    st.dataframe(df_result, use_container_width=True)

    csv = df_result.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name="translated_output.csv", mime="text/csv")

    # 4️⃣ Optional: Database Insertion
with st.expander("🔗 Save to MySQL (Optional)", expanded=False):
    db_host = st.text_input("MySQL Host", value="localhost")
    db_port = st.number_input("Port", value=3306)
    db_user = "root"  # make dynamic if needed
    db_pass = "root@123Abc"
    db_name = "asterisk"
    table_name = "vicidial_languages_pharases"
    target_lang_id = "9"

    if st.button("🧠 Generate & Insert SQL"):
        st.info("🔍 Starting DB connection and insertion...")

        if all([db_host, db_port, db_user, db_pass, db_name, table_name, target_lang_id]):
            try:
                st.write(f"🔗 Connecting to DB at {db_host}:{db_port}...")
                db_service = MySQLDBService(db_host, db_port, db_user, db_pass, db_name)
                engine = db_service.engine
                st.success("✅ Connection established.")

                with engine.connect() as conn:
                    st.write("📤 Inserting records into DB...")
                    for row in results:
                        original = row["Original Text"].replace("'", "\\'")
                        translated = row["Translated Text"].replace("'", "\\'")
                        insert_stmt = f"""
                        INSERT INTO {table_name} (language_id, original_text, translated_text)
                        VALUES ({target_lang_id}, '{original}', '{translated}')
                        """
                        st.write(f"📄 Executing: {insert_stmt.strip()}")
                        conn.execute(sql_text(insert_stmt))
                    conn.commit()
                    st.success("✅ Data inserted into database successfully.")
            except Exception as e:
                st.error("❌ Failed to insert into DB.")
                st.exception(e)
                st.text("Traceback:")
                st.code(traceback.format_exc())
        else:
            st.warning("⚠️ Please fill all DB fields.")