# sections/data_quality.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def render(df_filtered: pd.DataFrame):
    """Data Quality & Ethics: missingness, duplicates, and validation checks."""
    st.subheader("🧪 Data Quality & Ethics")
    st.markdown(
        "- Document sampling and known caveats (Open Data portal).\n"
        "- Respect licenses (dataset vs. processed outputs).\n"
        "- Aggregate when needed to avoid re-identification.\n"
        "- Be transparent about uncertainty; avoid over-claiming causality.\n"
    )

    if df_filtered is None or df_filtered.empty:
        st.info("No data available after filtering.")
        return

    df = df_filtered.copy()

    # -----------------------------
    # 1) Missingness (key columns)
    # -----------------------------
    st.subheader("🔎 Missingness (key fields)")
    key_cols = [
        "lat", "lon", "arr_num",
        "en_name", "french_name", "genus_species",
        "height_m", "circumference_cm",
        "ownership", "growth_stage",
        "is_remarkable",
    ]
    present = [c for c in key_cols if c in df.columns]

    if not present:
        st.warning("⚠️ None of the expected key columns are present in the dataset.")
    else:
        miss = (
            df[present]
            .isna()
            .mean()
            .mul(100)
            .round(1)
            .reset_index()
            .rename(columns={"index": "column", 0: "missing_pct"})
            .sort_values("missing_pct", ascending=False)
        )

        if miss["missing_pct"].sum() == 0:
            st.success("✅ No missing values detected in key fields — data looks complete!")
        else:
            st.dataframe(
                miss.style.bar(subset=["missing_pct"], color="#e8b923"),
                use_container_width=True,
                hide_index=True,
            )
    
    # -----------------------------
    # 2) Duplicates
    # -----------------------------
    st.subheader("🧬 Potential Duplicates")
    if "tree_id" in df.columns:
        dup_mask = df["tree_id"].duplicated(keep=False)
        basis = "tree_id"
    else:
        subset = [c for c in ["lat", "lon", "genus_species", "french_name", "en_name", "arr_num"] if c in df.columns]
        dup_mask = df.duplicated(subset=subset, keep=False) if subset else pd.Series(False, index=df.index)
        basis = ", ".join(subset) if subset else "N/A"

    n_dups = int(dup_mask.sum())
    pct_dups = 100 * n_dups / len(df) if len(df) else 0
    c1, c2 = st.columns(2)
    c1.metric("Duplicate rows (candidates)", f"{n_dups:,}".replace(",", " "))
    c2.caption(f"Detected using: **{basis}**")
    if n_dups:
        st.dataframe(df.loc[dup_mask].head(50))
    else:
        st.info("No duplicate candidates found with the current heuristic.")

    # -----------------------------
    # 3) Validation checks
    # -----------------------------
    st.subheader("✅ Validation Checks")

    checks = []

    # Geography: Paris bounding box (approx)
    if {"lat", "lon"}.issubset(df.columns):
        invalid_lat = ~df["lat"].between(48.80, 48.92) & df["lat"].notna()
        invalid_lon = ~df["lon"].between(2.23, 2.48) & df["lon"].notna()
        checks.append(("Latitude in Paris [48.80–48.92]", invalid_lat))
        checks.append(("Longitude in Paris [2.23–2.48]", invalid_lon))

    # Arrondissement 1..20
    if "arr_num" in df.columns:
        inv_arr = df["arr_num"].notna() & ~df["arr_num"].between(1, 20)
        checks.append(("District number in [1–20]", inv_arr))

    # Physical bounds
    if "height_m" in df.columns:
        inv_h = df["height_m"].notna() & ~df["height_m"].between(0, 60)  # 0–60 m plausible
        checks.append(("Height (m) in [0–60]", inv_h))
    if "circumference_cm" in df.columns:
        inv_c = df["circumference_cm"].notna() & ~df["circumference_cm"].between(0, 2000)  # 0–2000 cm
        checks.append(("Circumference (cm) in [0–2000]", inv_c))

    # Allowed categories
    if "growth_stage" in df.columns:
        allowed_stage = {"Young", "Adult", "Mature", "Unknown"}
        inv_stage = df["growth_stage"].notna() & ~df["growth_stage"].astype(str).isin(allowed_stage)
        checks.append((f"Growth stage ∈ {sorted(allowed_stage)}", inv_stage))

    if "ownership" in df.columns:
        # derive allowed from current, but flag obvious blanks
        inv_owner = df["ownership"].astype(str).str.strip().eq("") | df["ownership"].isna()
        checks.append(("Ownership not empty", inv_owner))

    # Build summary table
    rows = []
    for name, mask in checks:
        fails = int(mask.sum())
        pct = round(100 * fails / len(df), 2) if len(df) else 0.0
        rows.append({"rule": name, "failures": fails, "share_%": pct})
    q = pd.DataFrame(rows).sort_values("share_%", ascending=False)

    st.dataframe(q, use_container_width=True)

    # Optional: inspect failing rows for a chosen rule
    if not q.empty:
        st.markdown("**Inspect failing rows (optional)**")
        rule_sel = st.selectbox("Pick a rule to preview failing rows", q["rule"].tolist())
        mask_sel = None
        for name, mask in checks:
            if name == rule_sel:
                mask_sel = mask
                break
        if mask_sel is not None and mask_sel.any():
            st.dataframe(df.loc[mask_sel].head(200))
        else:
            st.info("No failing rows for this rule.")

    st.subheader("🧩 Data Quality Notes")

    st.markdown("""
    We don’t see any missing values here — that’s because I cleaned the dataset beforehand.  

    For trees that had a **genus** but no **species**, I decided to keep them:  
    they still carry some biological meaning, and genus-level identification (e.g. *Acer* → maples) is often reliable enough for broad analysis.  

    However, trees that had only a **species name** but no **genus** or **common name** were removed.  
    The reason is practical — when mapping trees, I wanted each to be labeled by name, and a species alone can refer to several different trees.  
    For example, *sativa* could describe *Castanea sativa* (sweet chestnut) or *Quercus sativa* (oak).  
    Without the genus, the tree’s identity becomes ambiguous.  

    In total, **144 trees** were removed for that reason.  
    This may introduce a small bias — meaning some areas could appear slightly less populated — but the effect is minimal since **150,570 trees** remain after cleaning.
    """)

    st.markdown("""
    ### 🌍 Dataset Scope and Limitations

    Tree naming may still contain inconsistencies, since the original dataset was in French and I translated species names into English to keep the project consistent.  
    For example, *Prunus avium* corresponds to **Sweet Cherry** in English and **Merisier** in French.  
    However, in the dataset, the same species might appear under a different French label —  
    for instance, **Cerisier à fleurs**, which would then be literally translated as **Flowering Cherry**.  
    This means we could end up with **two different names for the same species**, which is not scientifically rigorous.  
    Using the **scientific name (genus + species)** is therefore the most reliable way to ensure consistency across languages and datasets.  
                

    The initial dataset contained **214,837 trees**, but some of them were **outside of Paris** — for example, in the *Parc de Sceaux* or surrounding suburbs.  
    After filtering for trees within the city limits, only **150,570 trees** remained.

    Yet, according to [official figures from Paris.fr](https://www.paris.fr/pages/dix-ans-de-plantations-a-paris-213-000-arbres-pour-une-ville-plus-resiliente-31389#:~:text=La%20capitale%20compte%20d%C3%A9sormais%20plus,rues%20et%20jardins%20intra%2Dmuros.),  
    Paris reportedly has **over 500,000 trees** today.  

    This suggests that our dataset is **incomplete**, and therefore the analysis may not fully represent the city’s entire canopy —  
    a reminder that even open data can hide its own blind spots. 🌳
    """, unsafe_allow_html=True)   
    
    st.subheader("🌱 Growth Stage Classification")

    st.markdown("""
    The dataset originally included several growth stages written in French, which I translated and standardized.  
    Here’s the correspondence I found:

    | Original (French)       | English Translation | Final Category Used |
    |--------------------------|--------------------|----------------------|
    | Jeune (arbre)           | Young tree         | **Young** |
    | Jeune (arbre)Adulte     | Young (adult) tree | **Adult** |
    | Adulte                  | Adult tree         | **Adult** |
    | Mature                  | Mature tree        | **Mature** |

    However, there was an ambiguity: the dataset contained a class called **“Young (adult) tree”**,  
    which didn’t clearly fit between *Young* and *Adult*.  
    Since I couldn’t find any official explanation or documentation for this label,  
    I made a **pragmatic decision** — treating *Young (adult) trees* as part of the **Adult** category.  

    My reasoning was simple: much like in human terms, a “young adult” is still an adult.  
    This choice simplifies visualization and avoids overcomplicating the growth distribution,  
    though it could slightly underestimate the number of younger trees in the city.
    """, unsafe_allow_html=True)

