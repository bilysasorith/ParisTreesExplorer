# sections/distribution.py
import streamlit as st
import pandas as pd
import plotly.express as px


def render(df_filtered: pd.DataFrame):
    """Show distribution of trees by district (arrondissement) with auto insights."""
    st.subheader("Tree Distribution by District")
    st.markdown("**Outer districts host the majority of Paris’s trees, revealing clear environmental inequalities.**")

    if "arr_num" not in df_filtered.columns or df_filtered["arr_num"].dropna().empty:
        st.info("No district data available after filtering.")
        return

    # --- Data aggregation ---
    arr_counts = (
        df_filtered.dropna(subset=["arr_num"])
        .assign(arr=lambda d: d["arr_num"].astype("Int64"))
        .groupby("arr", as_index=False)
        .size()
        .rename(columns={"size": "tree_count"})
        .sort_values("tree_count", ascending=False)
    )

    # --- Format district labels like '12th', '19th', etc. ---
    def ordinal(n):
        return f"{n}{'th' if 10 <= n % 100 <= 20 else {1:'st',2:'nd',3:'rd'}.get(n % 10, 'th')}"

    arr_counts["arr_label"] = arr_counts["arr"].apply(ordinal)

    # --- Bar chart ---
    fig_arr = px.bar(
        arr_counts,
        x="tree_count",
        y="arr_label",
        orientation="h",
        title="Number of Trees by District (after filters)",
        labels={"tree_count": "Number of Trees", "arr_label": "District"},
        text="tree_count",
    )

    xmax = float(arr_counts["tree_count"].max()) * 1.08
    fig_arr.update_traces(textposition="outside", cliponaxis=False)
    fig_arr.update_xaxes(range=[0, xmax], showgrid=False)
    fig_arr.update_layout(
        margin=dict(l=90, r=30, t=50, b=40),
        height=520,
        showlegend=False,
        yaxis=dict(categoryorder="array", categoryarray=arr_counts["arr_label"][::-1]),
    )

    st.plotly_chart(fig_arr, use_container_width=True)

    # --- Helper functions for insight formatting ---
    def _fmt_n(n):
        try:
            return f"{int(n):,}".replace(",", " ")
        except Exception:
            return "0"

    def _pct(x):
        try:
            return f"{x * 100:.1f}%"
        except Exception:
            return "0%"

    def _safe_div(num, den):
        return (float(num) / float(den)) if (den not in (0, None) and pd.notna(den)) else 0.0

    # --- Dynamic textual insight ---
    if arr_counts.empty:
        st.info("No district data available after filtering.")
        return

    total = int(pd.to_numeric(arr_counts["tree_count"], errors="coerce").fillna(0).sum())
    n_arr = len(arr_counts)

    if total == 0:
        st.info("No trees available in the current selection (total = 0).")
        return

    if n_arr == 1:
        only = arr_counts.iloc[0]
        lbl = only["arr_label"]
        share = _safe_div(only["tree_count"], total)
        st.markdown(
            f"**Insight:** Only district **{lbl}** appears in the current selection, "
            f"with **{_fmt_n(only['tree_count'])} trees** ({_pct(share)})."
        )
    else:
        arr_counts = arr_counts.sort_values("tree_count", ascending=False)
        top = arr_counts.iloc[0]
        bot = arr_counts.iloc[-1]

        k = min(3, n_arr)
        topk_share = _safe_div(arr_counts.head(k)["tree_count"].sum(), total)
        top_share = _safe_div(top["tree_count"], total)
        bot_share = _safe_div(bot["tree_count"], total)

        median = float(pd.to_numeric(arr_counts["tree_count"], errors="coerce").median())
        gap_vs_median = _safe_div(top["tree_count"] - median, median) if n_arr >= 3 and median > 0 else None

        insight = (
            f"**Insight:** District **{top['arr_label']}** leads with "
            f"**{_fmt_n(top['tree_count'])} trees** ({_pct(top_share)} of the selection). "
            f"The **top {k} districts** hold **{_pct(topk_share)}** of all trees, "
            f"while **{bot['arr_label']}** accounts for only **{_pct(bot_share)}**."
        )

        if gap_vs_median is not None:
            if gap_vs_median >= 0.5:
                insight += f" The top district stands **well above the median** (+{gap_vs_median*100:.0f}%)."
            elif gap_vs_median >= 0.2:
                insight += f" The leader is **clearly above the median** (+{gap_vs_median*100:.0f}%)."

        st.markdown(insight)
