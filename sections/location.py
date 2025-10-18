# sections/location.py
import streamlit as st
import pandas as pd
import plotly.express as px


def render(df_filtered: pd.DataFrame):
    """Show where trees are planted (ownership / land manager) with a benchmark line and insight."""
    st.subheader("🌳 Where Are Paris’s Trees Planted?")
    st.markdown(
        "From streets to parks and cemeteries, the city’s trees mirror how land is managed — "
        "and who gets to live under its canopy."
    )

    st.subheader("Distribution by Tree Location Type (Filtered)")

    if df_filtered is None or df_filtered.empty:
        st.info("No data available after filtering.")
        return

    if "ownership" not in df_filtered.columns:
        st.info("No ownership information available in the current dataset.")
        return

    df_f = df_filtered

    # Counts per ownership type (ascending for a horizontal bar chart)
    dom_counts = (
        df_f["ownership"].fillna("Unknown")
        .astype(str)
        .str.strip()
        .value_counts()
        .rename_axis("Ownership type")
        .reset_index(name="count")
        .sort_values("count", ascending=True)
    )

    if dom_counts.empty:
        st.info("No ownership distribution to display.")
        return

    # Reference: average count if distribution were even across categories
    ref_dom = len(df_f) / dom_counts.shape[0] if dom_counts.shape[0] else 0

    # Bar chart with a vertical reference line
    fig_dom = px.bar(
        dom_counts,
        x="count",
        y="Ownership type",
        orientation="h",
        title="Ownership — Comparison to the Average",
        labels={"count": "Number of Trees", "Ownership type": "Ownership type"},
        text="count",
    )

    if ref_dom > 0:
        fig_dom.add_vline(
            x=ref_dom,
            line_dash="dash",
            line_color="#FFFFFF",
            annotation_text="Average distribution (if evenly shared)",
            annotation_position="top left",
            annotation_font_color="#FFFFFF",
        )

    # Visual tweaks
    fig_dom.update_traces(
        textposition="inside",
        insidetextanchor="start",
        textfont_color="black",
        textfont_size=12,
        cliponaxis=False,
    )
    xmax = float(max(dom_counts["count"].max(), ref_dom)) * 1.05
    fig_dom.update_xaxes(range=[0, xmax], title=None, showgrid=False)
    fig_dom.update_layout(
        margin=dict(l=120, r=40, t=50, b=40),
        bargap=0.15,
        height=420,
        showlegend=False,
    )

    st.plotly_chart(fig_dom, use_container_width=True)

    # Dynamic insight (share of the leading ownership category)
    shares = df_f["ownership"].fillna("Unknown").astype(str).str.strip().value_counts(normalize=True) * 100
    if not shares.empty:
        top_dom = shares.index[0]
        share = shares.iloc[0]
        st.markdown(
            f"**Insight:** Most visible trees are managed under **{top_dom.lower()}** "
            f"({share:.1f}% of the current selection). "
            "This concentration suggests management driven by major public domains, "
            "while other areas may be comparatively less green."
        )
    else:
        st.info("No ownership data to generate an insight.")

    # Closing narrative
    st.markdown(
        """
        <div style="text-align: justify; font-size: 1.05rem; line-height: 1.6;">
        But knowing <b>where</b> trees grow also raises another question — <b>how old</b> are they?<br>
        The age of a tree tells us not only about the city’s past, but also about its capacity to <b>renew and adapt</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )
