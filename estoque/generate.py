import numpy as np
import pandas as pd
from products import ACTIVE_PRODUCTS


def only_digits(value: str):
    return "".join(filter(lambda i: i.isdigit(), value))


class EmptyDataFrame(Exception):
    pass


class Results:
    def __init__(self, company_name):
        self.company_name = company_name
        self.products = ACTIVE_PRODUCTS
        super().__init__()

    def define_header(self):
        df = pd.read_csv("base_app/distribuidores.csv", delimiter=";")
        df = df[df["Distribuidor"] == self.company_name]
        df["CNPJ"] = df["CNPJ"].apply(only_digits)

        return df

    def _prepare_data(self):
        df = pd.read_csv(f"base_app/{self.company_name}.csv", delimiter=";")
        df = df[df["Distribuidor"] == self.company_name]

        df["CNPJ"] = df["CNPJ"].apply(only_digits)
        df["Cidade"] = df["Cidade"].apply(str)
        df["Cod. Filial"] = df["Cod. Filial"].apply(str)

        for index, row in df.iterrows():
            if row["Unidade"] != "KG/L":
                product_id = row["Cod Produto"]
                factor = self.products[product_id]["FATOR"]
                df.at[index, "kgpos"] = round(row["Pos. Contabil"] * factor, 3)
                df.at[index, "kg1"] = round(row["1 Contagem"] * factor, 3)
                df.at[index, "kg2"] = round(row["2 Contagem"] * factor, 3)
                df.at[index, "kg3"] = round(row["3 Contagem"] * factor, 3)
                df.at[index, "kgdiv"] = round(row["Divergencia"] * factor, 3)
            else:
                df.at[index, "kgpos"] = round(row["Pos. Contabil"], 3)
                df.at[index, "kg1"] = round(row["1 Contagem"], 3)
                df.at[index, "kg2"] = round(row["2 Contagem"], 3)
                df.at[index, "kg3"] = round(row["3 Contagem"], 3)
                df.at[index, "kgdiv"] = round(row["Divergencia"], 3)

        return df

    def define_data(self):
        header = self.define_header()
        sanitized_data = self._prepare_data()
        full_data = []

        for index, row in header.iterrows():
            cod_filial = row["Cod. Filial"]
            city = row["Cidade"]
            cnpj = row["CNPJ"]

            city_data = sanitized_data[
                (sanitized_data["Cod. Filial"] == cod_filial)
                & (sanitized_data["Cidade"] == city)
                & (sanitized_data["CNPJ"] == cnpj)
            ]

            if city_data.empty:
                raise EmptyDataFrame(cod_filial, city, cnpj)

            for id_onix, value in self.products.items():
                product_data = city_data[city_data["Cod Produto"] == id_onix]

                cont1 = None
                cont2 = None
                cont3 = None
                pos_cont = None
                diverg = None
                just = None

                if not product_data.empty:
                    cont1 = product_data.iloc[0]["kg1"]
                    cont2 = product_data.iloc[0]["kg2"]
                    cont3 = product_data.iloc[0]["kg3"]
                    pos_cont = product_data.iloc[0]["kgpos"]
                    diverg = product_data.iloc[0]["kgdiv"]
                    just = product_data.iloc[0]["Justificativa"]

                full_data.append(
                    {
                        "Cod Filial": cod_filial,
                        "Cidade": city,
                        "CNPJ": cnpj,
                        "Id Onix": id_onix,
                        "Descrição": value["DESCRIÇÃO"],
                        "1 Cont": cont1,
                        "2 Cont": cont2,
                        "3 Cont": cont3,
                        "Pos Cont": pos_cont,
                        "Divergência": diverg,
                        "Justificativa": just,
                    }
                )

        df = pd.DataFrame(full_data)
        df = df.replace({np.nan: None})
        return df

    def export_headers(self, writer=None):
        if not writer:
            writer = f"pre_results/{self.company_name}.xlsx"

        headers = self.define_header()

        headers.to_excel(
            excel_writer=writer,
            sheet_name="Filiais",
            na_rep=None,
            float_format="%.2f",
            columns=[
                "Distribuidor",
                "CNPJ",
                "Cidade",
                "UF",
                "Cod. Filial",
                "Última NF",
                "Data Visita",
                "Hora Inicial",
                "Hora Final",
                "Endereço",
                "Colaborador Onix.1",
                "Responsável Local",
            ],
            header=True,
            index=False,
        )

    def export_data(self, writer):
        if not writer:
            writer = f"pre_results/{self.company_name}.xlsx"

        data = self.define_data()

        data.to_excel(
            excel_writer=writer,
            sheet_name="Base",
            na_rep=None,
            float_format="%.2f",
            header=True,
            index=False,
        )

    def export_all(self):
        with pd.ExcelWriter(f"pre_results/{self.company_name}.xlsx") as writer:

            self.export_headers(writer)
            self.export_data(writer)


if __name__ == "__main__":
    company_name = input("Razão Social: ")
    results = Results(company_name=company_name)
    results.export_all()
    print("--> Finalizado")
