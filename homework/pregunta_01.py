"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import os
import pandas as pd


def pregunta_01():
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)

    df.dropna(inplace=True)

    def limpiar_monto(val):
        if pd.isna(val):
            return val
        val = str(val).strip().replace("$", "").replace(",", "").replace(" ", "")
        try:
            return int(float(val))
        except ValueError:
            return pd.NA

    df["monto_del_credito"] = df["monto_del_credito"].apply(limpiar_monto)

    def parsear_fecha(val):
        if pd.isna(val):
            return pd.NaT
        val = str(val).strip()
        for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return pd.to_datetime(val, format=fmt)
            except ValueError:
                continue
        return pd.NaT

    df["fecha_de_beneficio"] = (
        df["fecha_de_beneficio"]
        .apply(parsear_fecha)
        .dt.strftime("%d/%m/%Y")
    )

    df["barrio"] = (
        df["barrio"]
        .str.replace("antonio nari\xbfo", "antonio nariño", regex=False)
        .str.replace("bel\xbfn", "belén", regex=False)
    )

    text_cols = [c for c in df.select_dtypes(include="object").columns
                 if c != "fecha_de_beneficio"]

    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
        df[col] = df[col].replace("nan", pd.NA)

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)