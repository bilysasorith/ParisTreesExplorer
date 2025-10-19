# sections/diversity.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.prep import pick_common_name_col  # helper: choose en_name else french_name


def render(df_filtered: pd.DataFrame, label_mode: str = "Common name"):
    """
    Diversity section:
    - Title + context
    - Top-20 species bar chart (with average reference line)
    - Dynamic insight text about concentration/diversity
    - Closing narrative block

    label_mode:
        - "Common name"      -> uses 'en_name' (fallback to 'french_name')
        - "Scientific name"  -> uses 'genus_species'
    """
    st.subheader("🌿 Diversity in Disguise")
    st.markdown("**A city rich in trees, yet poor in variety — a handful of species dominate Paris’s urban canopy, leaving it fragile against heat and disease.**")

    if df_filtered is None or df_filtered.empty:
        st.info("No data available to analyze species diversity after filtering.")
        return

    # ---- Choose the display column based on label_mode ----
    if label_mode == "Scientific name":
        if "genus_species" not in df_filtered.columns:
            st.info("Scientific name column ('genus_species') is missing.")
            return
        label_col = "genus_species"
        title_label = "Scientific name"
        series = (
            df_filtered[label_col]
            .astype(str).str.strip()
            .replace({"": pd.NA})
            .dropna()
        )
    else:
        # Common-name mode, aligned with overview: prefer en_name then french_name
        label_col = pick_common_name_col(df_filtered)
        if label_col is None:
            st.info("No common name column found ('en_name' or 'french_name').")
            return
        title_label = "Common name"
        series = (
            df_filtered[label_col]
            .astype(str).str.strip()
            .replace({"": pd.NA})
            .dropna()
        )

    # ---- Top species (Top 20) ----
    top_species = (
        series.to_frame(name=label_col)
        .groupby(label_col).size()
        .sort_values(ascending=False)
        .head(20)
        .rename("count")
        .reset_index()
    )

    st.subheader("Dominant Species in the Selected Area")
    if top_species.empty:
        st.info("No species available for the current selection.")
    else:
        # n_unique & reference line computed on the non-empty series
        n_unique = series.nunique()
        ref = (len(df_filtered) / n_unique) if n_unique else 0

        fig = px.bar(
            top_species,
            x="count",
            y=label_col,
            orientation="h",
            title=f"Top 20 — {title_label}",
            labels={"count": "Number of Trees", label_col: title_label},
            text="count",
        )

        # Reference line (average per species across the selection)
        if ref > 0:
            fig.add_vline(
                x=ref,
                line_dash="dash",
                line_color="#FFFFFF",
                annotation_text="Average threshold across all species",
                annotation_position="top right",
                annotation_font_color="#FFFFFF",
                annotation_textangle=0,
                annotation_xshift=40,
                annotation_yshift=10,
            )

        # Value labels & layout tweaks
        fig.update_traces(
            textposition="inside",
            insidetextanchor="start",
            textfont_color="black",
            textfont_size=12,
            cliponaxis=False,
        )
        xmax = float(max(top_species["count"].max(), ref)) * 1.05 if len(top_species) else 1.0
        fig.update_xaxes(range=[0, xmax], title=None, showgrid=False)
        fig.update_layout(
            yaxis_side="left",
            margin=dict(l=100, r=40, t=50, b=40),
            bargap=0.15,
            height=420,
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Optional: quick headline about the leading species (not displayed, but kept if needed)
        # lead = top_species.iloc[0]
        # share = (series.eq(lead[label_col]).mean() * 100) if len(series) else 0

    # ---- Dynamic insight about concentration / diversity ----
    if not series.empty:
        species_counts = series.value_counts(normalize=True)
        n_species = species_counts.size
        top5_share = species_counts.head(5).sum() * 100 if n_species else 0
        lead_species = species_counts.index[0] if n_species else ""
        lead_share = species_counts.iloc[0] * 100 if n_species else 0

        if n_species <= 3:
            st.markdown(
                f"**Insight:** Few species are present in the current selection ({n_species}). "
                f"**{lead_species}** dominates with **{lead_share:.1f}%** of trees. "
                "Limited diversity weakens local resilience."
            )
        elif n_species <= 10:
            st.markdown(
                f"**Insight:** The tree population is concentrated: **{lead_species}** is most frequent "
                f"({lead_share:.1f}%), and the top 5 species account for **{top5_share:.1f}%** of the total. "
                "This dependence reduces resilience to diseases and climate stress."
            )
        else:
            st.markdown(
                f"**Insight:** Despite good diversity ({n_species} species identified), a few species still dominate, "
                f"led by **{lead_species}** ({lead_share:.1f}% of trees). "
                "Balancing density and diversity remains key to long-term urban resilience."
            )
    else:
        st.info("No data available to generate a diversity insight.")

    # ---- Closing narrative ----
    st.markdown(
        """
        <div style="text-align: justify; font-size: 1.05rem; line-height: 1.6;">
        Yet diversity is not just about species.<br>
        It’s also about <b>where</b> trees take root — in parks, along streets, or behind school walls — 
        a reflection of how space, power, and nature are distributed across the city.
        </div>
        """,
        unsafe_allow_html=True,
    )
