import pandas as pd
import streamlit as st
from sections.intro import render as intro_render
from sections.overview import render as overview_render
from sections.conclusion import render as conclusion_render
from sections.distribution import render as distribution_render
from sections.diversity import render as diversity_render
from sections.location import render as location_render
from sections.growth_stage import render as growth_stage_render
from sections.data_quality import render as dq_render

from utils.io import load_data
from utils.prep import clean_trees
from utils.viz import map_points

# --- Page config ---
st.set_page_config(page_title="🌳 Paris Trees Explorer", layout="wide")

# --- Load & clean ---
@st.cache_data(show_spinner=False)
def get_data():
    df_raw = load_data("data/data.csv")  # ';' sep handled in utils/io.py
    df = clean_trees(df_raw).copy()
    return df

df = get_data()

# --- Header ---
intro_render()
st.divider()

# --- Validate required columns ---
required_for_map = {"lat", "lon"}
missing = [c for c in required_for_map if c not in df.columns]
if missing:
    st.error(f"Missing required columns for the map: {missing}.")
    st.stop()

# --- Normalize arrondissement number (create 'arr_num') ---
if "district" not in df.columns:
    st.error("The column 'district' is missing from the dataset.")
    st.stop()

df["arr_num"] = (
    df["district"].astype(str)
      .str.extract(r"(\d{1,2})", expand=False)
      .astype("Int64")
)

# --- Normalize boolean 'is_remarkable' from 'remarkable' (OUI/NON only) ---
df["is_remarkable"] = (
    df.get("remarkable", "NON")
      .astype(str).str.strip().str.upper()
      .eq("OUI")
)

# ======================
# SIDEBAR — SEARCH FIRST
# ======================

# custom HTML title with a tooltip (CSS hover)
st.sidebar.markdown(
    """
    <style>
    /* Allow sidebar overflow */
    section[data-testid="stSidebar"] {
        overflow: visible !important;
    }

    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }

    /* Tooltip rendered on top of the entire page */
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 270px;
        background-color: rgba(30,30,30,0.95);
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: fixed; /* 👈 instead of absolute */
        z-index: 99999;  /* 👈 renders above everything */
        top: 80px;       /* distance from top of window */
        left: 340px;     /* adjust if sidebar width changes */
        opacity: 0;
        transition: opacity 0.3s ease;
        font-size: 0.85rem;
        line-height: 1.3;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        pointer-events: none;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
        pointer-events: auto;
    }
    </style>

    <div style="display:flex; align-items:center; justify-content:space-between;">
        <h3 style="margin-bottom:0;">🔍 Search</h3>
        <div class="tooltip">❓
            <span class="tooltiptext">
                Filter trees by their <b>common name</b> (e.g., Plane tree, Maple) 
                or by their <b>scientific name</b> (e.g., <i>Acer platanoides</i>).<br><br>
                You can select one or multiple names, and the map will update instantly.
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mode de recherche
search_mode = st.sidebar.radio(
    "Search by",
    ["Common name", "Scientific name"],
    index=0,
)

search_col = "en_name" if search_mode == "Common name" else "genus_species"

# Auto-suggest list
if search_col not in df.columns:
    search_options = []
else:
    search_options = (
        df[search_col]
        .dropna()
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

picked_values = st.sidebar.multiselect(
    "Pick one or more values",
    options=search_options,
    default=[],
    placeholder="Type to search...",
)

st.sidebar.markdown("---")

# ======================
# SIDEBAR — FILTERS
# ======================
st.sidebar.header("Filters")

# Sample size
max_points = st.sidebar.slider(
    "Number of points to display (sample size)",
    min_value=1000, max_value=30000, value=10000, step=1000,
    help="For performance reasons, a random subset is displayed on the map."
)

# Remarkable toggle
only_remarkable = st.sidebar.checkbox(
    "Show only remarkable trees",
    value=False,
    help="Remarkable trees are special specimens recognized for their size, age, or history."
)

# Districts
arr_options = sorted(df["arr_num"].dropna().unique().astype(int).tolist())
if not arr_options:
    st.warning("No valid arrondissement values were found in the data.")
    st.stop()

selected_arrs = st.sidebar.multiselect(
    "Districts",
    options=arr_options,
    default=arr_options,
    format_func=lambda x: f"{x}e",
)

# Ownership filter
if "ownership" in df.columns:
    owner_options = (
        df["ownership"].dropna().astype(str).str.strip().drop_duplicates().sort_values().tolist()
    )
    selected_owners = st.sidebar.multiselect(
        "Ownership type",
        options=owner_options,
        default=owner_options,   # by default: keep all
        placeholder="Select ownership types…",
        help="Filter by who manages the trees or land (e.g., Street alignment, Gardens, Cemeteries, Schools, etc.).",
    )
else:
    selected_owners = []  # column missing -> no filtering

# Growth stage filter
if "growth_stage" in df.columns:
    stage_options = (
        df["growth_stage"].dropna().astype(str).str.strip().drop_duplicates().sort_values().tolist()
    )
    selected_stages = st.sidebar.multiselect(
        "Growth stage",
        options=stage_options,
        default=stage_options,   # by default: keep all
        placeholder="Select growth stages…",
        help="Filter by tree maturity level (e.g., Young, Adult, Mature).",

    )
else:
    selected_stages = []  # column missing -> no filtering


# ======================
# APPLY FILTERS
# ======================
if len(selected_arrs) == 0:
    st.info("Select at least one district in the sidebar to display the map.")
    st.stop()

df_filtered = (
    df[df["arr_num"].isin(selected_arrs)]
      .dropna(subset=["lat", "lon"])
)

if only_remarkable:
    df_filtered = df_filtered[df_filtered["is_remarkable"]]

# Filter by ownership
if "ownership" in df_filtered.columns and selected_owners:
    df_filtered = df_filtered[
        df_filtered["ownership"].astype(str).str.strip().isin(selected_owners)
    ]

# Filter by growth stage
if "growth_stage" in df_filtered.columns and selected_stages:
    df_filtered = df_filtered[
        df_filtered["growth_stage"].astype(str).str.strip().isin(selected_stages)
    ]

# Apply search filter if any values picked
if picked_values and search_col in df_filtered.columns:
    df_filtered = df_filtered[
        df_filtered[search_col].astype(str).str.strip().isin(picked_values)
    ]

# ======================
# MAP SECTION
# ======================
st.subheader("🌳 Map of Paris Trees (Filtered)")
st.caption("Use the sidebar to search and filter the dataset.")

needed_cols = [
    "lat", "lon",
    "district", "arr_num",
    "french_name", "en_name",
    "genus_species",
    "height_m", "circumference_cm",
    "ownership", "location_type",
    "growth_stage", "remarkable", "is_remarkable",
]
cols_present = [c for c in needed_cols if c in df_filtered.columns]

if df_filtered.empty:
    st.info("No data to display with the current settings.")
else:
    sample_n = int(min(max_points, df_filtered.shape[0]))
    geo_view = df_filtered[cols_present].sample(sample_n, random_state=42)
    # --- Metrics section ---
    overview_render(df_filtered)
    map_points(geo_view)

distribution_render(df_filtered)
st.divider()

diversity_render(df_filtered, label_mode="Common name")
st.divider()
location_render(df_filtered)

st.divider()
growth_stage_render(df_filtered)

st.divider()
st.markdown("<br>", unsafe_allow_html=True)
conclusion_render()

with st.expander("Data Quality", expanded=False):
    dq_render(df_filtered)


# Optional preview
with st.expander("Preview dataset", expanded=False):
    st.dataframe(df.head())
with st.expander("Quick stats", expanded=False):
    st.write(df.describe(include="all"))