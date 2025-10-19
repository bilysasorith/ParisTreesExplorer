import pandas as pd
import numpy as np

def clean_trees(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw dataset:
      1️⃣ Standardize column names
      2️⃣ Extract lat/lon from 'geo_point_2d'
    """
    df = df.copy()

    # 1) Standardize column names (explicit mapping + fallback)
    rename_map = {
        "IDBASE": "tree_id",
        "TYPE EMPLACEMENT": "location_type",
        "DOMANIALITE": "ownership",
        "ARRONDISSEMENT": "district",
        "COMPLEMENT ADRESSE": "address_complement",
        "LIEU / ADRESSE": "address",
        "IDEMPLACEMENT": "location_id",
        "LIBELLE FRANCAIS": "french_name",
        "GENRE": "genus",
        "ESPECE": "species",
        "VARIETE OU CULTIVAR": "variety",
        "CIRCONFERENCE (cm)": "circumference_cm",
        "HAUTEUR (m)": "height_m",
        "STADE DE DEVELOPPEMENT": "growth_stage",
        "REMARQUABLE": "remarkable",
        "geo_point_2d": "geo_point_2d",
    }
    df.rename(columns=rename_map, inplace=True)

    # 2) Extract lat/lon from "geo_point_2d" (format: "lat, lon")
    if "geo_point_2d" in df.columns:
        lat, lon = [], []
        for val in df["geo_point_2d"].astype(str):
            parts = [p.strip() for p in val.split(",")]
            if len(parts) == 2:
                try:
                    lat.append(float(parts[0]))
                    lon.append(float(parts[1]))
                except ValueError:
                    lat.append(np.nan); lon.append(np.nan)
            else:
                lat.append(np.nan); lon.append(np.nan)
        df["lat"] = lat
        df["lon"] = lon

    # 3) Translate tree

    translation_map = {
    "Platane": "Plane tree",
    "Tilleul": "Linden",
    "Micocoulier": "Hackberry",
    "Arbre aux quarante écus": "Ginkgo",
    "Fevier": "Honey locust",
    "Marronnier": "Horse chestnut",
    "Merisier": "Wild cherry",
    "Erable": "Maple",
    "Cerisier à fleurs": "Flowering cherry",
    "Poirier à fleurs": "Flowering pear",
    "Frêne": "Ash",
    "If": "Yew",
    "Faux-cyprès": "False cypress",
    "Pin": "Pine",
    "Peuplier": "Poplar",
    "Noyer": "Walnut",
    "Chêne": "Oak",
    "Laurier du caucase": "Caucasian laurel",
    "Saule": "Willow",
    "Robinier": "Black locust",
    "Lilas de Perse": "Persian lilac",
    "Pommier à fruits": "Apple tree",
    "Filaire": "Phillyrea",
    "Parrotie de Perse - Arbre de fer": "Persian ironwood",
    "Bouleau": "Birch",
    "Noisetier de Byzance": "Turkish hazel",
    "Amélanchier": "Serviceberry",
    "Orme de Sibérie": "Siberian elm",
    "Cèdre": "Cedar",
    "Hêtre": "Beech",
    "Sophora": "Pagoda tree",
    "Pommier à fleurs": "Flowering apple",
    "Charme-Houblon": "Hop hornbeam",
    "Libocèdre": "Incense cedar",
    "Cabrillet": "Cabrillet",
    "Lithocarpus": "Stone oak",
    "Non spécifié": "Unspecified",
    "Ailante": "Tree of heaven",
    "Catalpa": "Catalpa",
    "Paulownia": "Empress tree",
    "Palmier": "Palm",
    "Savonnier": "Golden rain tree",
    "Chicot du Canada": "Kentucky coffeetree",
    "Arbre à soie": "Silk tree",
    "Clerodendron": "Clerodendrum",
    "Tulipier": "Tulip tree",
    "Orme": "Elm",
    "Prunier à fleurs": "Flowering plum",
    "Plaqueminier": "Persimmon",
    "Charme": "Hornbeam",
    "Copalme": "Sweetgum",
    "Magnolia": "Magnolia",
    "Aubépine": "Hawthorn",
    "Thuya": "Thuja",
    "Poirier à fruits": "Pear tree",
    "Frêne à fleurs": "Flowering ash",
    "Parrotie de Perse": "Persian ironwood",
    "Cyprès": "Cypress",
    "Pterocarya": "Wingnut",
    "Aulne": "Alder",
    "Arbre à savon": "Soap tree",
    "Cornouiller": "Dogwood",
    "Sequoia": "Sequoia",
    "Pommier": "Apple tree",
    "Mûrier": "Mulberry",
    "Arbre de Judée": "Judas tree",
    "Metaséquoia": "Dawn redwood",
    "Mimosa": "Mimosa",
    "Prunier à fruits": "Plum tree",
    "Cerisier à fleurs, cerisier griotte": "Flowering cherry",
    "Prunus n. sp.": "Prunus",
    "Virgilier": "Yellowwood",
    "Lilas des indes": "Crape myrtle",
    "Troene": "Privet",
    "Sorbier": "Rowan",
    "Chèvrefeuille": "Honeysuckle",
    "Cedrele": "Toon tree",
    "Aria edulis": "Whitebeam",
    "Olivier": "Olive tree",
    "Laurier du Portugal": "Portuguese laurel",
    "Houx": "Holly",
    "Châtaignier": "Chestnut",
    "Eleagnus - Chalef": "Oleaster",
    "Cerisier à grappes": "Bird cherry",
    "Troëne": "Privet",
    "Alisier": "Whitebeam",
    "Oranger des Osages": "Osage orange",
    "Noisetier": "Hazel",
    "Cyprès Chauve": "Bald cypress",
    "Figuier": "Fig tree",
    "Arbre à miel": "Bee tree",
    "Buis": "Boxwood",
    "Amandier": "Almond tree",
    "Sterculier": "Sterculia",
    "Epicéa": "Spruce",
    "Pteroceltis": "Blue sandalwood",
    "Eucalyptus": "Eucalyptus",
    "Cytise": "Laburnum",
    "Sapin Douglas": "Douglas fir",
    "Aria edulis ''Magnifica''": "Whitebeam",
    "Viorne": "Viburnum",
    "Pêcher": "Peach tree",
    "Fontanesia": "Fontanesia",
    "Aubepine": "Hawthorn",
    "Abricotier": "Apricot tree",
    "Poirier": "Pear tree",
    "Arbre à caramel": "Katsura tree",
    "Arbre à Gutta-Percha": "Gutta-percha tree",
    "Sapin": "Fir",
    "Tupélo": "Tupelo",
    "Argousier": "Sea buckthorn",
    "Phellodendron": "Cork tree",
    "Arbousier": "Strawberry tree",
    "Néflier": "Medlar",
    "Sureau": "Elder",
    "Cognassier": "Quince",
    "Alangium": "Alangium",
    "Cerisier à fruits": "Cherry tree",
    "Nothofagus": "Southern beech",
    "Idesia": "Idesia",
    "Sumac": "Sumac",
    "Fusain": "Spindle tree",
    "Platycarya": "Platycarya",
    "Néflier commun": "Medlar",
    "Laurier-Cerise": "Cherry laurel",
    "Laurier sauce": "Bay laurel",
    "Photinia": "Photinia",
    "Mélèze": "Larch",
    "Laurier des Iroquois": "Spicebush",
    "Cotoneaster": "Cotoneaster",
    "Prunus Fruit n. sp.": "Prunus (fruit)",
    "Citronnier": "Lemon tree",
    "Chitalpa": "Chitalpa",
    "Tsuga": "Hemlock",
    "Parrotie": "Ironwood",
    "Callistemon": "Bottlebrush",
    "Céphalotaxe": "Plum yew",
    "Rhododendron": "Rhododendron",
    "Gainier": "Redbud",
    "Amelanchier": "Serviceberry",
    "Chimonanthe": "Wintersweet",
    "Fremontia": "Flannel bush",
    "Poivrier": "Pepper tree",
    "Genévrier": "Juniper",
    "Bourdaine": "Alder buckthorn",
    "Prunellier": "Blackthorn",
    "Araucaria": "Araucaria",
    "Caryer": "Hickory",
    "Prunus Fleur n. sp.": "Prunus (flowering)",
    "Olivier odorant": "Fragrant olive",
    "Tamaris": "Tamarisk",
    "Asiminier": "Pawpaw",
    "Kaki": "Persimmon",
    "Lilas": "Lilac",
    "Heptacodion de Chine": "Seven-son flower",
    "Arbre aux mouchoirs": "Dove tree",
    "Angélique": "Angelica tree",
    "Pterostyrax": "Epaulette tree",
    "Orme de Samarie": "Siberian elm",
    "Althéa": "Rose of Sharon",
    "Ginkgo": "Ginkgo",
    "Faux dattier": "Date plum",
    "Poliothyrsis": "Poliothyrsis",
    "Aria edulis ''Majestica''": "Whitebeam",
    "Cryptomeria": "Japanese cedar",
    "Arbre à perruque": "Smoke tree",
    "Abricotier fruit": "Apricot tree",
    "Nerprun": "Buckthorn",
    "Ormeau épineux": "Spiny elm",
    "Staphylier": "Bladdernut",
    "Camphrier": "Camphor tree",
    "Grenadier": "Pomegranate",
    "Podocarpus": "Podocarpus",
    "Paliurus": "Christ’s thorn",
    "Cormier": "Service tree",
    "Hiba": "Hiba arborvitae",
    "Muscadier": "Nutmeg tree",
    "Myrte du Chili": "Chilean myrtle",
    "Erable de Freeman Armstrong": "Freeman maple",
    "Raisinier": "Raisin tree",
    "Seringas": "Mock orange",
    "Caragana": "Caragana",
    "Sophora flavescens": "Shrubby sophora",
    "Ostryer": "Hop hornbeam",
    "Laurier": "Laurel",
    "Belle Josephine": "Belle Josephine",
    "Daphniphyllum": "Daphniphyllum",
    "Gainier de Chine Shirobana": "Chinese redbud",
    "Cunninghamia": "Chinese fir",
    "Noisetier fruit": "Hazel",
    "Laurier des Açores": "Azores laurel",
    "Hamamélis": "Witch hazel",
    "Kétéleeria": "Keteleeria",
    "Chionanthe": "Fringe tree",
    "Caroubier": "Carob tree",
    "Taiwania": "Taiwania",
    "Sycoparrotia": "Sycoparrotia",
    "Caraganier": "Caragana",
    "Cordyline": "Cabbage tree",
    "Aubépine hybride": "Hybrid hawthorn",
    "Lindera": "Spicebush",
    "Pistachier": "Pistachio tree",
    "Ficus": "Fig tree",
    "Bischofia": "Bishop wood",
    "Cudranier": "Cudrania",
    "Brucea javanica": "Javanese brucea",
    "Buddleja": "Butterfly bush",
    "Genêt": "Broom",
    "Fustet d' Amérique": "American smoke tree",
    "Stachyurus": "Stachyurus",
    "Halesia": "Silverbell",
    "Sycopsis": "Sycopsis",
    "Styphnolobium microphylla ''Hilsop''": "Small-leaved pagoda tree",
    "Abelia": "Abelia",
    "Maackie": "Maackia",
    "Garrya": "Silk tassel",
    "Andromède": "Pieris",
    "Arbre à soie Summer Chocolate": "Silk tree",
    "Styrax": "Snowbell",
    "Aronie": "Chokeberry",
    "Oranger de Chine": "Orange jasmine",
    "Goyavier": "Guava",
    "Euscaphis": "Euscaphis",
    "Parrotiopsis": "Parrotiopsis",
    "Kalopanax": "Castor aralia",
    "Glycine": "Wisteria",
    "Arbre aux perles": "Pearl tree",
    "Castanopsis": "Chinquapin",
    "Papayer": "Papaya",
}
    if "french_name" in df.columns:
        df["en_name"] = df["french_name"].map(translation_map).fillna(df["french_name"])

        # --- inside clean_trees(df) ---
    if "growth_stage" in df.columns:
        map_growth = {
            None: None,
            "Adulte": "Adult",
            "Jeune (arbre)": "Young tree",
            "Jeune (arbre)Adulte": "Adult",  # your choice
            "Mature": "Mature",
        }

        # Replace the original column with English equivalents
        df["growth_stage"] = df["growth_stage"].map(map_growth).fillna(df["growth_stage"])

    # --- inside clean_trees(df) ---

    # Build "genus_species" as a simple "Genus species" concatenation.
    # Robust to missing columns / NaNs / extra spaces.
    g = df["genus"].astype(str).str.strip() if "genus" in df.columns else ""
    s = df["species"].astype(str).str.strip() if "species" in df.columns else ""

    if isinstance(g, str):  # means column is missing -> create empty series
        g = pd.Series("", index=df.index)
    if isinstance(s, str):
        s = pd.Series("", index=df.index)

    df["genus_species"] = (
        (g.fillna("") + " " + s.fillna(""))
        .str.replace(r"\s+", " ", regex=True)   # collapse multiple spaces
        .str.strip()
    )

    # Optional: if you prefer an empty string when both are missing
    df.loc[df["genus_species"].isin(["", "nan", "none"]), "genus_species"] = ""

    # --- Standardize and translate ownership (domanialité) ---
    OWNERSHIP_MAP = {
        "Alignement": "Street alignment",
        "Jardin": "Gardens",
        "CIMETIERE": "Cemeteries",
        "PERIPHERIQUE": "Ring road",
        "DASCO": "Schools",
        "DJS": "Youth & Sports facilities",
        "DAC": "Cultural venues",
        "DFPE": "Early childhood facilities",
        "DASES": "Social & Health services",
        "DEVE": "Green spaces & environment",
        "DPE": "Sanitation, Water & Streets",
        "DVD": "Roads & Mobility",
    }

    if "ownership" in df.columns:
        df["ownership"] = (
            df["ownership"]
            .astype(str)
            .str.strip()
            .replace(OWNERSHIP_MAP)
        )


        # -----------------------------------------------------
    # Manual name fixes from genus_species
    # -----------------------------------------------------
    # Dictionnaire extensible : clés = genus_species (insensible à la casse)
    MANUAL_NAMES = {
        "prunus serrulata": {"french_name": "Cerisier du Japon", "en_name": "East Asian cherry"},
        "salix pyrifolia": {"french_name": "Saule à feuilles de poirier", "en_name": "Balsam willow"},
        "pyrus pyrifolia": {"french_name": "Poirier asiatique", "en_name": "Asian pear"},
        "populus n. sp.": {"french_name": "Peuplier (espèce non spécifiée)", "en_name": "Poplar (unspecified species)"},
        "prunus x hillieri": {"french_name": "Cerisier d’Hillier", "en_name": "Hillier cherry"},
        "acer platanoides": {"french_name": "Érable plane", "en_name": "Norway maple"},
        "cedrus atlantica": {"french_name": "Cèdre de l’Atlas", "en_name": "Atlas cedar"},

        # 🌿 Nouveaux ajouts :
        "sorbus aria": {"french_name": "Alisier blanc", "en_name": "Whitebeam"},
        "catalpa speciosa": {"french_name": "Catalpa commun", "en_name": "Northern catalpa"},
        "olea europaea": {"french_name": "Olivier", "en_name": "Olive tree"},
        "platanus x hispanica": {"french_name": "Platane commun", "en_name": "London plane"},
        "prunus avium": {"french_name": "Merisier", "en_name": "Wild cherry"},
        "cupressus sempervirens": {"french_name": "Cyprès toujours vert", "en_name": "Italian cypress"},
        "prunus domestica": {"french_name": "Prunier domestique", "en_name": "European plum"},
        "crataegus laevigata": {"french_name": "Aubépine à deux styles", "en_name": "Midland hawthorn"},
        "malus domestica": {"french_name": "Pommier domestique", "en_name": "Apple tree"},
                "olea europea": {
            "french_name": "Olivier",
            "en_name": "Olive tree",
        },
        "prunus n. sp.": {
            "french_name": "Prunier (espèce non spécifiée)",
            "en_name": "Plum (unspecified species)",
        },
        "malus floribunda": {
            "french_name": "Pommier florifère",
            "en_name": "Japanese flowering crabapple",
        },
        "malus communis": {
            "french_name": "Pommier commun",
            "en_name": "Common apple tree",
        },
        "gleditsia triacanthos f. inermis": {
            "french_name": "Févier sans épines",
            "en_name": "Thornless honey locust",
        },
        "poncirus trifoliata": {
            "french_name": "Oranger trifolié",
            "en_name": "Trifoliate orange",
        },
        "ulmus minor": {
            "french_name": "Orme champêtre",
            "en_name": "Field elm",
        },
        "acer n. sp.": {
            "french_name": "Érable (espèce non spécifiée)",
            "en_name": "Maple (unspecified species)",
        },
        "rhamnus alaternus": {
            "french_name": "Nerprun alaterne",
            "en_name": "Italian buckthorn",
        },
                "magnolia x loebneri": {
            "french_name": "Magnolia de Loebner",
            "en_name": "Loebner magnolia",
        },
        "tilia x flavescens": {
            "french_name": "Tilleul jaune",
            "en_name": "Yellow linden",
        },
        "betula n. sp.": {
            "french_name": "Bouleau (espèce non spécifiée)",
            "en_name": "Birch (unspecified species)",
        },
        "styphnolobium japonica": {
            "french_name": "Sophora du Japon",
            "en_name": "Japanese pagoda tree",
        },
        "populus canadensis": {
            "french_name": "Peuplier du Canada",
            "en_name": "Canadian poplar",
        },
        "pistacia sp.": {
            "french_name": "Pistachier (espèce non spécifiée)",
            "en_name": "Pistachio (unspecified species)",
        },
        "malus toringoides": {
            "french_name": "Pommier du Tibet",
            "en_name": "Tibetan crabapple",
        },
        "ulmus parviflora": {
            "french_name": "Orme de Chine",
            "en_name": "Chinese elm",
        },
        "prunus pendula": {
            "french_name": "Cerisier pleureur",
            "en_name": "Weeping cherry",
        },
        "x chitalpa sp.": {
            "french_name": "Chitalpa (hybride)",
            "en_name": "Chitalpa (hybrid)",
        },
        "fraxinus americana": {
            "french_name": "Frêne d’Amérique",
            "en_name": "White ash",
        },
        "malus spectabilis": {
            "french_name": "Pommier à fleurs",
            "en_name": "Chinese flowering crabapple",
        },
        "ulmus minor var. vulgaris": {
            "french_name": "Orme champêtre (variété commune)",
            "en_name": "Field elm (common variety)",
        },
        "platanus acerifolia": {
            "french_name": "Platane à feuilles d’érable",
            "en_name": "Maple-leaved plane",
        },
        "sorbus sp.": {
            "french_name": "Alisier (espèce non spécifiée)",
            "en_name": "Whitebeam (unspecified species)",
        },
        "prunus sp.": {
            "french_name": "Prunier (espèce non spécifiée)",
            "en_name": "Plum (unspecified species)",
        },
        "eriolobus trilobata": {
            "french_name": "Pommier à trois lobes",
            "en_name": "Three-lobed apple tree",
        },
                "ehretia macrophylla": {
            "french_name": "Ehretia à grandes feuilles",
            "en_name": "Large-leaved ehretia",
        },
        "ilex aquifolium": {
            "french_name": "Houx commun",
            "en_name": "Common holly",
        },
        "sorbus torminalis": {
            "french_name": "Alisier torminal",
            "en_name": "Wild service tree",
        },
        "halesia carolina": {
            "french_name": "Arbre aux clochettes",
            "en_name": "Carolina silverbell",
        },
        "crataegus japonicum": {
            "french_name": "Aubépine du Japon",
            "en_name": "Japanese hawthorn",
        },
        "styphnolobium n. sp.": {
            "french_name": "Sophora (espèce non spécifiée)",
            "en_name": "Pagoda tree (unspecified species)",
        },
        "quercus robur": {
            "french_name": "Chêne pédonculé",
            "en_name": "English oak",
        },
        "sorbus aucuparia": {
            "french_name": "Sorbier des oiseleurs",
            "en_name": "Rowan tree",
        },
        "ilex sp.": {
            "french_name": "Houx (espèce non spécifiée)",
            "en_name": "Holly (unspecified species)",
        },
        "eriobotrya sp.": {
            "french_name": "Néflier (espèce non spécifiée)",
            "en_name": "Loquat (unspecified species)",
        },
        "malus baccata": {
            "french_name": "Pommier de Sibérie",
            "en_name": "Siberian crabapple",
        },
        "prunus spinosa": {
            "french_name": "Prunellier",
            "en_name": "Blackthorn",
        },
        "ficus n. sp.": {
            "french_name": "Figuier (espèce non spécifiée)",
            "en_name": "Fig tree (unspecified species)",
        },
                "pinus n. sp.": {
            "french_name": "Pin (espèce non spécifiée)",
            "en_name": "Pine (unspecified species)",
        },
        "prunus americana": {
            "french_name": "Prunier d'Amérique",
            "en_name": "American plum",
        },
        "zanthoxylum n. sp.": {
            "french_name": "Clavalier (espèce non spécifiée)",
            "en_name": "Prickly ash (unspecified species)",
        },
        "taxus x media": {
            "french_name": "If hybride",
            "en_name": "Hybrid yew",
        },
        "eriobotrya japonicum": {
            "french_name": "Néflier du Japon",
            "en_name": "Japanese loquat",
        },
        "prunus glandulosa": {
            "french_name": "Amandier à fleurs",
            "en_name": "Dwarf flowering almond",
        },
        "ulmus glabra": {
            "french_name": "Orme de montagne",
            "en_name": "Wych elm",
        },
        "phellodendron japonicum": {
            "french_name": "Arbre-liège du Japon",
            "en_name": "Japanese cork tree",
        },
        "magnolia sp.": {
            "french_name": "Magnolia (espèce non spécifiée)",
            "en_name": "Magnolia (unspecified species)",
        },
        "crataegus prunifolia": {
            "french_name": "Aubépine à feuilles de prunier",
            "en_name": "Plumleaf hawthorn",
        },
        "betula albosinensis": {
            "french_name": "Bouleau de Chine",
            "en_name": "Chinese red birch",
        },
        "corylus colurna": {
            "french_name": "Noisetier de Byzance",
            "en_name": "Turkish hazel",
        },
        "robinia hispida": {
            "french_name": "Robinier hérissé",
            "en_name": "Bristly locust",
        },
        "ulmus x hollandica": {
            "french_name": "Orme de Hollande",
            "en_name": "Dutch elm",
        },
        "ulmus parvifolia": {
            "french_name": "Orme de Chine",
            "en_name": "Chinese elm",
        },
                "salix x pendulina": {
            "french_name": "Saule pleureur",
            "en_name": "Weeping willow",
        },
        "paulownia tomentosa": {
            "french_name": "Paulownia impérial",
            "en_name": "Princess tree",
        },
        "ulmus n. sp.": {
            "french_name": "Orme (espèce non spécifiée)",
            "en_name": "Elm (unspecified species)",
        },
        "phoenix sp.": {
            "french_name": "Palmier (espèce non spécifiée)",
            "en_name": "Palm tree (unspecified species)",
        },
        "prunus padus": {
            "french_name": "Merisier à grappes",
            "en_name": "Bird cherry",
        },
        "cotoneaster franchetii": {
            "french_name": "Cotoneaster de Franchet",
            "en_name": "Franchet's cotoneaster",
        },
        "carpinus carpinifolia": {
            "french_name": "Charme à feuilles de charme",
            "en_name": "Hornbeam",
        },
        "robinia ornus": {
            "french_name": "Robinier orne",
            "en_name": "Robinia ornis (hybrid)",
        },
        "robinia x margaretta": {
            "french_name": "Robinier de Margaretta",
            "en_name": "Margaretta locust",
        },
        "prunus cerasifera": {
            "french_name": "Prunier-cerise",
            "en_name": "Cherry plum",
        },
        "acer sp.": {
            "french_name": "Érable (espèce non spécifiée)",
            "en_name": "Maple (unspecified species)",
        },
        "ligustrum vulgaris": {
            "french_name": "Troène commun",
            "en_name": "Common privet",
        },
        "crataegus n. sp.": {
            "french_name": "Aubépine (espèce non spécifiée)",
            "en_name": "Hawthorn (unspecified species)",
        },
        "sorbus padus": {
            "french_name": "Sorbier des oiseleurs à grappes",
            "en_name": "European bird cherry",
        },
        "pyrus sp.": {
            "french_name": "Poirier (espèce non spécifiée)",
            "en_name": "Pear tree (unspecified species)",
        },
                "ilex latifolia": {
            "french_name": "Houx à larges feuilles",
            "en_name": "Lusterleaf holly",
        },
        "robinia pseudocamellia": {
            "french_name": "Robinier faux-camélia",
            "en_name": "False camellia locust",
        },
        "picea glauca": {
            "french_name": "Épinette blanche",
            "en_name": "White spruce",
        },
        "platanus n. sp.": {
            "french_name": "Platane (espèce non spécifiée)",
            "en_name": "Plane tree (unspecified species)",
        },
        "alangium sinensis": {
            "french_name": "Alangium de Chine",
            "en_name": "Chinese alangium",
        },
    }
        # colonne clé normalisée (sans espaces superflus, sans casse)
    if "genus_species" in df.columns:
        gs_key = (
            df["genus_species"]
            .astype(str)
            .str.strip()
            .str.casefold()
        )
        def _blank(s):
            return s.isna() | s.astype(str).str.strip().eq("")

        for key, names in MANUAL_NAMES.items():
            m = gs_key.eq(key)
            if "french_name" in df.columns and "french_name" in names:
                df.loc[m & _blank(df["french_name"]), "french_name"] = names["french_name"]
            if "en_name" in df.columns and "en_name" in names:
                df.loc[m & _blank(df["en_name"]), "en_name"] = names["en_name"]


        # Remplissage générique quand species est vide/NaN mais genus présent
    GENUS_FALLBACK = {
        "taxus": {"french_name": "If", "en_name": "Yew"},
        "styphnolobium": {"french_name": "Arbre aux pagodes", "en_name": "Japanese pagoda tree"},
        "prunus": {"french_name": "Cerisier / Prunier", "en_name": "Cherry / Plum tree"},
        "pyrus": {"french_name": "Poirier", "en_name": "Pear tree"},
        "celtis": {"french_name": "Micocoulier", "en_name": "Hackberry"},
        "carpinus": {"french_name": "Charme", "en_name": "Hornbeam"},
        "ulmus": {"french_name": "Orme", "en_name": "Elm"},
        "cupressus": {"french_name": "Cyprès", "en_name": "Cypress"},
        "fraxinus": {"french_name": "Frêne", "en_name": "Ash tree"},
        "aesculus": {"french_name": "Marronnier", "en_name": "Horse chestnut"},
        "crataegus": {"french_name": "Aubépine", "en_name": "Hawthorn"},
        "malus": {"french_name": "Pommier", "en_name": "Apple tree"},
        "paulownia": {"french_name": "Paulownia", "en_name": "Princess tree"},
        "sorbus": {"french_name": "Sorbier", "en_name": "Rowan / Mountain ash"},
        "acer": {"french_name": "Érable", "en_name": "Maple"},
        "morus": {"french_name": "Mûrier", "en_name": "Mulberry"},
        "zelkova":      {"french_name": "Zelkova",            "en_name": "Zelkova"},
        "lagerstroemia":{"french_name": "Lilas des Indes",    "en_name": "Crape myrtle"},
        "magnolia":     {"french_name": "Magnolia",           "en_name": "Magnolia"},
        "ilex":         {"french_name": "Houx",               "en_name": "Holly"},
        "tilia":        {"french_name": "Tilleul",            "en_name": "Linden"},
        "toona":        {"french_name": "Cédrèle",            "en_name": "Toona / Chinese cedar"},
        "x chitalpa":   {"french_name": "Chitalpa (hybride)", "en_name": "Chitalpa (hybrid)"},
        "chitalpa":     {"french_name": "Chitalpa",           "en_name": "Chitalpa"},
        "robinia":      {"french_name": "Robinier",           "en_name": "Locust"},
        "pinus":        {"french_name": "Pin",                "en_name": "Pine"},
        "salix":        {"french_name": "Saule",              "en_name": "Willow"},
        "olea":         {"french_name": "Olivier",            "en_name": "Olive tree"},
        "populus":      {"french_name": "Peuplier",           "en_name": "Poplar"},
        "thuja":       {"french_name": "Thuya",              "en_name": "Thuja / Arborvitae"},
        "cornus":      {"french_name": "Cornouiller",        "en_name": "Dogwood"},
        "koelreuteria": {"french_name": "Savonnier",         "en_name": "Golden rain tree"},
        "platanus":    {"french_name": "Platane",            "en_name": "Plane tree"},
        "cedrus":      {"french_name": "Cèdre",              "en_name": "Cedar"},
        "quercus":     {"french_name": "Chêne",              "en_name": "Oak"},
        "ligustrum":   {"french_name": "Troène",             "en_name": "Privet"},
        "tamarix":     {"french_name": "Tamaris",            "en_name": "Tamarisk"},
        "ailanthus":   {"french_name": "Ailante",            "en_name": "Tree of Heaven"},
        "sambucus":    {"french_name": "Sureau",             "en_name": "Elder / Elderberry"},
        "betula":      {"french_name": "Bouleau",            "en_name": "Birch"},
        "gleditsia":   {"french_name": "Févier",             "en_name": "Honey locust"},
        "albizia":       {"french_name": "Albizia / Arbre à soie", "en_name": "Silk tree / Albizia"},
        "clerodendrum":  {"french_name": "Clérodendron",           "en_name": "Clerodendrum"},
        "alnus":         {"french_name": "Aulne",                  "en_name": "Alder"},
        "poncirus":      {"french_name": "Poncirus / Oranger trifolié", "en_name": "Trifoliate orange"},
        "cydonia":       {"french_name": "Cognassier",             "en_name": "Quince tree"},
        "cephalotaxus":  {"french_name": "Cephalotaxus / If à prunes", "en_name": "Plum yew"},
        "amelanchier":   {"french_name": "Amélanchier",            "en_name": "Serviceberry"},
        "viburnum":      {"french_name": "Viorne",                 "en_name": "Viburnum"},
        "phillyrea":     {"french_name": "Filaire",                "en_name": "Phillyrea / Mock privet"},
        "eriolobus":   {"french_name": "Cormier / Alisier",             "en_name": "Service tree"},
        "gymnocladus": {"french_name": "Gymnocladus / Arbre aux haricots", "en_name": "Kentucky coffeetree"},
        "elaeagnus":   {"french_name": "Éléagnus",                      "en_name": "Oleaster / Silverberry"},
        "liquidambar": {"french_name": "Copalme d'Amérique",            "en_name": "Sweetgum"},
        "eucalyptus":  {"french_name": "Eucalyptus",                    "en_name": "Eucalyptus"},
        "parrotia":    {"french_name": "Parrotie de Perse",             "en_name": "Persian ironwood"},
        "styrax":      {"french_name": "Styrax",                        "en_name": "Snowbell tree"},
        "photinia":    {"french_name": "Photinia",                      "en_name": "Photinia"},
        "zanthoxylum": {"french_name": "Clavalier / Poivrier du Sichuan","en_name": "Prickly ash / Sichuan pepper tree"},
        "fontanesia":  {"french_name": "Fontanésia",                    "en_name": "Fontanesia"},
        "laurus":      {"french_name": "Laurier",                       "en_name": "Bay laurel"},
        "ehretia":        {"french_name": "Ehretia",                   "en_name": "Ehretia"},
        "ficus":          {"french_name": "Figuier",                   "en_name": "Fig tree"},
        "pterocarya":     {"french_name": "Ptérocarier",               "en_name": "Wingnut tree"},
        "ostrya":         {"french_name": "Charme houblon",            "en_name": "Hop-hornbeam"},
        "chamaecyparis":  {"french_name": "Faux-cyprès",               "en_name": "False cypress"},
        "sequoiadendron": {"french_name": "Séquoia géant",             "en_name": "Giant sequoia"},
        "abies":          {"french_name": "Sapin",                     "en_name": "Fir"},
        "platycladus":    {"french_name": "Thuya de Chine",            "en_name": "Chinese arborvitae"},
        "broussonetia":   {"french_name": "Mûrier à papier",           "en_name": "Paper mulberry"},
        "melia":          {"french_name": "Mélié / Lilas de Perse",    "en_name": "Chinaberry / Persian lilac"},
        "cryptomeria":    {"french_name": "Cryptoméria du Japon",      "en_name": "Japanese cedar"},
        "fagus":          {"french_name": "Hêtre",                     "en_name": "Beech"},
        "vitex":          {"french_name": "Gattilier",                 "en_name": "Chaste tree"},
        "wisteria":       {"french_name": "Glycine",                   "en_name": "Wisteria"},
        "buxus":          {"french_name": "Buis", "en_name": "Boxwood"},

        }

    genus_key = df["genus"].astype(str).str.strip().str.casefold()
    no_species = df["species"].isna() | df["species"].astype(str).str.strip().eq("")
    no_name = _blank(df["french_name"]) & _blank(df["en_name"])

    for g, names in GENUS_FALLBACK.items():
        m = no_species & no_name & genus_key.eq(g)
        hits = int(m.sum())
        if hits:
            print(f"↳ Genus fallback '{g}': {hits} rows")
            if "french_name" in names:
                df.loc[m, "french_name"] = names["french_name"]
            if "en_name" in names:
                df.loc[m, "en_name"] = names["en_name"]


        # -----------------------------------------------------
    # 🧹 Remove rows with no usable identification
    #   Règle: (pas de nom FR ET pas de nom EN) ET (pas de genus)
    # -----------------------------------------------------
    initial_n = len(df)

    def _blank(s):
        return s.isna() | s.astype(str).str.strip().eq("")

    cond_no_name = _blank(df["french_name"]) & _blank(df["en_name"])

    # "no genus" = NaN / vide / "Non spécifié" (insensible à la casse)
    cond_no_genus = (
        df["genus"].isna()
        | df["genus"].astype(str).str.strip().eq("")
        | df["genus"].astype(str).str.strip().str.casefold().eq("non spécifié")
    )

    drop_mask = cond_no_name & cond_no_genus
    n_drop = int(drop_mask.sum())

    if n_drop > 0:
        pct_drop = (n_drop / max(initial_n, 1)) * 100
        print(f"🪓 Dropped {n_drop:,} rows ({pct_drop:.2f}% of dataset) with no FR/EN name and no genus.")
        df = df.loc[~drop_mask].copy()
    else:
        print("✅ No rows dropped: every row has either a name (FR/EN) or a genus.")

    # colonne clé normalisée (sans espaces superflus, sans casse)
    if "genus_species" in df.columns:
        gs_key = (
            df["genus_species"]
            .astype(str)
            .str.strip()
            .str.casefold()
        )
        # helpers "champ vide"
        def _blank(s):
            return s.isna() | s.astype(str).str.strip().eq("")

        # boucle d'application : on complète seulement les vides
        for key, names in MANUAL_NAMES.items():
            m = gs_key.eq(key)
            if "french_name" in df.columns and "french_name" in names:
                df.loc[m & _blank(df["french_name"]), "french_name"] = names["french_name"]
            if "en_name" in df.columns and "en_name" in names:
                df.loc[m & _blank(df["en_name"]), "en_name"] = names["en_name"]

    
    return df

def pick_common_name_col(df):
    """Return the common-name column to use, preferring English then French; None if absent."""
    if "en_name" in df.columns:
        return "en_name"
    if "french_name" in df.columns:
        return "french_name"
    return None
