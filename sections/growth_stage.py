# sections/growth_stage.py
import streamlit as st
import pandas as pd
import plotly.express as px


def render(df_filtered: pd.DataFrame):
    """Distribution by growth stage + insight, adapté à 'growth_stage'."""
    st.subheader("🧭 How old is Paris’s urban forest?")
    st.markdown(
        """
        <div style="text-align: justify; font-size: 1.05rem; line-height: 1.6; max-width: 1200px;">
        Most of Paris’s trees are at an adult stage — a sign of a well-established canopy, yet a reminder that renewal must soon take root.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Distribution by Growth Stage (Filtered)")

    if df_filtered is None or df_filtered.empty:
        st.info("No data available after filtering.")
        return

    if "growth_stage" not in df_filtered.columns:
        st.info("No growth stage information available in the dataset.")
        return

    df_f = df_filtered.copy()

    # Comptages par stade (on masque 'Unknown' dans le graphe)
    st_counts = (
        df_f["growth_stage"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .value_counts()
        .rename_axis("stage")
        .reset_index(name="count")
    )

    # Supprimer Unknown pour la visualisation
    st_counts = st_counts[st_counts["stage"].str.lower() != "unknown"]

    # Ordre fixe
    order = ["Young tree", "Adult", "Mature"]
    st_counts["stage"] = pd.Categorical(st_counts["stage"], categories=order, ordered=True)
    st_counts = st_counts.sort_values("stage")

    if st_counts.empty:
        st.info("No growth stage distribution to display.")
        return

    # Graphique
    fig_st = px.bar(
        st_counts,
        x="count",
        y="stage",
        orientation="h",
        title="Tree Growth Stage",
        labels={"count": "Number of Trees", "stage": ""},
        text="count",
    )
    fig_st.update_traces(textposition="inside", insidetextanchor="start", textfont_color="black", cliponaxis=False)
    xmax = float(st_counts["count"].max()) * 1.05
    fig_st.update_xaxes(range=[0, xmax], showgrid=False)
    fig_st.update_layout(margin=dict(l=90, r=40, t=50, b=40), height=380, showlegend=False)

    st.plotly_chart(fig_st, use_container_width=True)

    # Insight dynamique (sur toutes les valeurs, Unknown compris si présent)
    shares = (
        df_f["growth_stage"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .value_counts(normalize=True) * 100
    )
    if not shares.empty:
        top_stage = shares.index[0]
        share = shares.iloc[0]
        st.markdown(
            f"**Insight:** The urban forest is mostly composed of **{top_stage.lower()} trees** "
            f"({share:.1f}% of the filtered selection), reflecting a balance between stability "
            "and the need for renewal."
        )
    else:
        st.info("No data available for growth stage.")

    # Bloc narratif de clôture
    st.markdown(
        """
        <div style="text-align: justify; font-size: 1.05rem; line-height: 1.6;">
        Across districts, species, and ages, the same pattern emerges — 
        nature in Paris is unevenly shared.<br>
        And that imbalance leads us to one final question.
        </div>
        """,
        unsafe_allow_html=True,
    )
