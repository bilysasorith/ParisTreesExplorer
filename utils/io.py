import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """
    Charge un fichier CSV (séparateur ;) ou Excel selon l'extension.
    Retourne un DataFrame pandas.
    """
    if path.endswith(".csv"):
        return pd.read_csv(path, sep=";")
    elif path.endswith(".xlsx"):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Format non pris en charge : {path}")
