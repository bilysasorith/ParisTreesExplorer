# sections/diversity.py
import streamlit as st
import pandas as pd
import plotly.express as px


def render(df_filtered: pd.DataFrame, label_mode: str = "Common name"):
    """
    Diversity section:
    - Title + context
    - Top-20 species bar chart (with average reference line)
    - Dynamic insight text about concentration/diversity
    - Closing narrative block

    label_mode: "Common name" -> uses 'en_name' (fallback to 'french_name')
                "Scientific name" -> uses 'genus_species'
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
    else:
        # Common name mode (English preferred; fallback to French if missing)
        if "en_name" in df_filtered.columns:
            label_col = "en_name"
            title_label = "Common name"
        elif "french_name" in df_filtered.columns:
            label_col = "french_name"
            title_label = "Common name (FR)"
        else:
            st.info("No common name column found ('en_name' or 'french_name').")
            return

    # ---- Top species (Top 20) ----
    top_species = (
        df_filtered.groupby(label_col)
        .size()
        .sort_values(ascending=False)
        .head(20)
        .rename("count")
        .reset_index()
    )

    st.subheader("Dominant Species in the Selected Area")
    if top_species.empty:
        st.info("No species available for the current selection.")
    else:
        n_unique = df_filtered[label_col].nunique(dropna=True)
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
                annotation_position="top right",     # place le texte à droite
                annotation_font_color="#FFFFFF",
                annotation_textangle=0,              # empêche la rotation
                annotation_xshift=40,                # décale horizontalement vers la droite
                annotation_yshift=10,                # légère marge verticale
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

        # Optional: quick headline about the leading species
        lead = top_species.iloc[0]
        share = (df_filtered[label_col].eq(lead[label_col]).mean() * 100) if len(df_filtered) else 0

    # ---- Dynamic insight about concentration / diversity ----
    if label_col in df_filtered.columns and not df_filtered.empty:
        species_counts = df_filtered[label_col].value_counts(normalize=True)
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
