"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import streamlit as st
from pathlib import Path
import sqlite3, pandas as pd

st.set_page_config(page_title="CIEL Memory Dashboard", layout="wide")
st.title("CIEL-Memory Dashboard")

db_path = Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db")
if not db_path.exists():
    st.warning("No SQLite ledger found. Run some TMP flows first.")
else:
    with sqlite3.connect(str(db_path)) as conn:
        df = pd.read_sql_query("SELECT * FROM memories ORDER BY created_at DESC LIMIT 2000", conn)
    st.subheader("Latest memories (TSM)")
    st.dataframe(df, use_container_width=True)
