🌳 Paris Trees Explorer
Beneath the Same Sky — Unequal Shades in Paris

A data storytelling project built with Streamlit to explore the distribution, diversity, and equity of Paris’s urban forest.
The app uses the official open dataset from the City of Paris (Open Data, ODbL License) and reveals how nature, too, draws its own borders in the city.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🧭 Overview

Paris hosts more than 150,000 catalogued trees — each one carrying a small story about urban ecology, inequality, and renewal.
This dashboard lets you explore:

🌿 Where trees are planted (streets, gardens, cemeteries, etc.)

🌳 Which species dominate Paris’s canopy

🪵 How old the city’s trees are (growth stages)

🗺️ Which districts enjoy more greenery than others

The goal: to question green equity — do all Parisians breathe under the same shade?

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📊 Key Features

✅ Interactive map with filters (district, type, species, remarkable trees)
✅ Bar charts and summaries per arrondissement and species
✅ Data quality checks (missing values, duplicates, validation)
✅ Transparent documentation of cleaning and assumptions
✅ English narrative designed for data storytelling

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🧩 Project Structure

app.py
├── sections/
│   ├── intro.py
│   ├── overview.py
│   ├── deep_dives.py
│   └── conclusions.py
├── utils/
│   ├── io.py          # load_data() from Open Data portal
│   ├── prep.py        # cleaning and harmonization
│   └── viz.py         # Plotly visualizations
├── data/              # optional local cache
└── assets/            # icons, images, logos
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
⚙️ Installation & Run Instructions

1️⃣ Clone the repository
git clone https://github.com/bilysasorith/ParisTreesExplorer.git
cd ParisTreesExplorer

2️⃣ Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
streamlit run app.py

Once launched, open your browser at http://localhost:8501

Link to the video : https://www.youtube.com/watch?v=FqpQB3f18X8
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
👤 Author

Name: SASORITH Bily
University: EFREI Paris — Data Visualization & Storytelling Project
Contact: bily.sasorith@efrei.net