import streamlit as st
import pandas as pd
import plotly.express as px


def map_points(df_geo, style: str = "carto-darkmatter", zoom: int = 11.5, height: int = 600):
    """
    Interactive Plotly map:
    - Green = regular trees, Gold = remarkable trees
    - Custom tooltip: English name, scientific name, French name, district, stage, height, circumference
    """

    # --- Safety checks ---
    if df_geo is None or df_geo.empty or not {"lat", "lon"}.issubset(df_geo.columns):
        st.info("No geolocated trees available after applying filters.")
        return

    g = df_geo.copy()

    # --- Color mapping ---
    if "is_remarkable" in g.columns:
        g["color_cat"] = g["is_remarkable"].map({True: "Remarkable", False: "Ordinary"})
    else:
        g["color_cat"] = "Ordinary"

    cmap = {"Ordinary": "#509C6F", "Remarkable": "#F2B705"}  # green / gold

    # --- Base map ---
    fig = px.scatter_mapbox(
        g,
        lat="lat",
        lon="lon",
        color="color_cat",
        color_discrete_map=cmap,
        hover_name="en_name" if "en_name" in g.columns else None,
        hover_data=None,
        zoom=zoom,
        height=height,
    )

    # --- Tooltip order & formatting ---
    ordered_cols = [
        "genus_species",      # Scientific name
        "french_name",        # French common name
        "height_m",
        "circumference_cm",
        "growth_stage",
        "arr_num",
    ]

    for c in ordered_cols:
        if c not in g.columns:
            g[c] = ""

    g["_height"] = g["height_m"].apply(lambda x: "" if pd.isna(x) else f"{float(x):g}")
    g["_circ"] = g["circumference_cm"].apply(lambda x: "" if pd.isna(x) else f"{float(x):g}")

    custom_cols = ["genus_species", "french_name", "_height", "_circ", "growth_stage", "arr_num"]

    fig.update_traces(
        marker=dict(size=7, opacity=0.9, symbol="circle", allowoverlap=True),
        customdata=g[custom_cols].to_numpy(),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"              # English name
            "<i>%{customdata[0]}</i><br>"          # Scientific name
            "French: %{customdata[1]}<br>"
            "District: %{customdata[5]}<br>"
            "Stage: %{customdata[4]}<br>"
            "Height: %{customdata[2]} m<br>"
            "Circumference: %{customdata[3]} cm<extra></extra>"  # remove gray box
        ),
    )

    # --- Layout ---
    fig.update_layout(
        mapbox_style=style,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,  # 👈 disable built-in Plotly legend
        )

    st.plotly_chart(fig, use_container_width=True)

    # --- Legend counts ---
    n_gold = int((g["color_cat"] == "Remarkable").sum())
    n_green = int((g["color_cat"] == "Ordinary").sum())

    st.markdown(
        f"""
        <div style="display:flex; gap:24px; align-items:center; font-size:0.95rem; margin-top:6px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="width:14px; height:14px; background:#3D7F58; display:inline-block; border-radius:3px; border:1px solid rgba(255,255,255,0.5);"></span>
                <span>Regular trees <small>({n_green})</small></span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="width:14px; height:14px; background:#F2B705; display:inline-block; border-radius:3px; border:1px solid rgba(255,255,255,0.5);"></span>
                <span>Remarkable trees <small>({n_gold})</small></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
