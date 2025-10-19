# sections/overview.py
import streamlit as st
import pandas as pd
from utils.prep import pick_common_name_col  # si tu l'as mis dans prep.py


def render(df_filtered: pd.DataFrame):
    """Display key summary metrics based on the filtered dataset."""
    st.markdown("### Key Figures")

    if df_filtered is None or df_filtered.empty:
        st.info("No data available to display metrics.")
        return
    
    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    df_f = df_filtered  # alias for clarity

    # 🌳 Total number of displayed trees
    c1.metric("🌳 Total Trees", format(len(df_f), ",d").replace(",", " "))

    # 🌿 Unique species count (choose french_name or en_name if exists)
    species_col = pick_common_name_col(df_f)
    if species_col is None:
        c2.metric("🌿 Species Diversity", "N/A")
    else:
        n_species = (
            df_f[species_col]
            .astype(str).str.strip()
            .replace({"": pd.NA})
            .dropna()
            .nunique()
        )
        c2.metric("🌿 Species Diversity", n_species)

    # 🌟 Percentage of remarkable trees
    if "is_remarkable" in df_f.columns:
        pct_rem = df_f["is_remarkable"].mean() * 100
    else:
        pct_rem = (
            df_f.get("remarkable", "")
            .astype(str)
            .str.upper()
            .eq("OUI")
            .mean() * 100
        )
    c3.metric("🌟 Remarkable Trees", f"{pct_rem:.1f}%")

    # 🕰️ Dominant growth stage (most frequent)
    if "growth_stage" in df_f.columns and not df_f["growth_stage"].dropna().empty:
        dominant_stage = (
            df_f["growth_stage"]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .idxmax()
        )
    else:
        dominant_stage = "Unknown"

    c4.metric("🕰️ Dominant Growth Stage", dominant_stage)
