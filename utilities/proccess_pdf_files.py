import pdfplumber
import pandas as pd
from decimal import Decimal, InvalidOperation
from utilities.support_values import companies


# Auxiliary functions

def number_of_characters(text):
    return len(text)


def is_decimal(text):
    # Aqui tenemos que tener cuidado con números elevados
    if text.count(".") > 1:
        return False
    text = text.replace(",", ".")
    text = text.replace(".", "", text.count(".") - 1)
    try:
        number = Decimal(text)
        return True
    except InvalidOperation:
        return False


def get_score(df, electrica):
    return 1 if df[df["text"].str.contains(electrica)].shape[0] > 0 else 0


# Método para filtrar el dataframe por ciertos campos y varios valores de texto
def get_filtered_data(df, num_page, field, text):
    mask1 = df["n_page"] == num_page
    mask2 = df[field] == text
    filtered_data = df[mask1 & mask2]
    return filtered_data


# Método para filtrar el dataframe por ciertos campos y devolver índices
def get_filtered_indexes(df, num_page, field, text):
    mask1 = df["n_page"] == num_page
    mask2 = df[field] == text
    indexes = df.index[mask1 & mask2]
    return indexes.tolist()

# Metodo para obtener la intersección de dos listas
def interseccion(lst1, lst2):
	return list(set(lst1) & set(lst2))


# Método para filtrar el dataframe por ciertos campos y varios valores de texto
# get_lines_with(df, 1, "text", ["Potencia", "facturada"])
# Devuelve una lista, por ejemplo [27]
def get_lines_with(df, num_page, field, text):
    mask1 = df["n_page"] == num_page
    filtered_data = df[mask1]
    list_n_fila = filtered_data["n_fila"].unique().tolist()
    for i in range(len(text)):
        mask2 = df[field] == text[i]
        filtered_data = df[mask1 & mask2]
        list_n_fila = interseccion(list_n_fila, filtered_data["n_fila"].unique().tolist())
    return list_n_fila


class Invoice():

    pdf_file_name = None
    df = pd.DataFrame()
    n_pages = 0
    imagenes = []
    row_coordinates = {}
    idx_company = None

    # Datos a completar de las facturas
    power_contracted = None
    duration = None
    power_price = None
    total_energy_consumed = None
    energy_price = None
    equipment_rental = None
    electricity_tax_percentage = Decimal(5.11269632)
    electricity_tax = None
    energy_cost = None
    power_cost = None
    iva_percentage = Decimal(21)
    iva_tax = None

    def __init__(self, pdf_file_name):
        self.pdf_file_name = pdf_file_name

    def create_dataframe(self):
        with pdfplumber.open(self.pdf_file_name) as pdf:
            for idx, page in enumerate(pdf.pages):
                df_page = pd.DataFrame(data=page.extract_words())
                df_page["n_page"] = idx
                self.df = self.df.append(df_page, ignore_index=True)
                self.imagenes.append(page.to_image())
            self.n_pages = len(pdf.pages)

    def add_row_number_to_df(self):
        self.df["n_fila"] = 0
        for idx in range(self.n_pages):
            row_coordinates_this_page = []
            # Obtenemos un dataframe cuyo número de página coincida con idx
            df_page_idx = self.df[self.df["n_page"] == idx]
            # Obtenemos los bottom ordenados de menor a mayor
            bottom_values = df_page_idx["bottom"].sort_values()
            bottom_values.sort_index(inplace=True)
            bottom_values = bottom_values.unique()
            # Tengo ya un array cuyo id del elemento es el número de fila
            for i in range(len(bottom_values)):
                mask1 = self.df["n_page"] == idx
                # filtramos el df por el campo bottom == i
                self.df.loc[(self.df["bottom"] == bottom_values[i]) & (self.df["n_page"] == idx), "n_fila"] = i
                mask2 = self.df["n_fila"] == i
                min_value = self.df[mask1 & mask2]["x0"].min()
                max_value = self.df[mask1 & mask2]["x1"].max()
                top_value = self.df[mask1 & mask2]["top"].min()
                dicc = {"n_page": idx, "n_fila": i, "min_value": min_value, "max_value": max_value, "top_value": top_value, "bottom_value": bottom_values[i]}
                row_coordinates_this_page.append(dicc)
            self.row_coordinates[idx] = row_coordinates_this_page
    
    def add_length_word_to_df(self):
        self.df["length_word"] = self.df.apply(lambda x: number_of_characters(x["text"]), axis=1)

    def add_is_decimal_to_df(self):
        self.df["is_decimal"] = self.df.apply(lambda x: is_decimal(x["text"]), axis=1)

    def get_df_shape(self):
        return (self.df.shape[0], self.df.shape[1])

    # Obtenemos el idx de la compañía eléctrica
    def set_index_company(self):
        for idx, company in enumerate(companies):
            score = get_score(self.df, company["text_to_find"])
            if score == 1:
                self.idx_company = idx
                return

    # Establecemos el atributo correspondiente
    def get_attribute(self, attribute):
        # Dependiendo de la empresa debemos buscar campos y páginas distintas
        # company dictionary
        cd = companies[self.idx_company]
        n_page = cd[attribute]["n_page"]
        words_to_find = cd[attribute]["words_to_find"]
        pos_decimal_value = cd[attribute]["pos_decimal_value"]
        lines = get_lines_with(self.df, n_page, "text", words_to_find)
        if len(lines) != 1:
            return
        # Asignamos la variable power_contracted
        try:
            value = self.df[
                (self.df["n_page"] == n_page) &
                (self.df["n_fila"] == lines[0]) &
                (self.df["is_decimal"] == True)
            ]["text"].to_list()[pos_decimal_value]
            value = value.replace(",", ".")
            value = Decimal(value)
        except (IndexError, InvalidOperation):
            value = None
        return value

    # Establecemos los valores
    def set_power_contracted(self):
        self.power_contracted = self.get_attribute("power_contracted")
    def set_duration(self):
        self.duration = self.get_attribute("duration")
    def set_power_price(self):
        self.power_price = self.get_attribute("power_price")
    def set_total_energy_consumed(self):
        self.total_energy_consumed = self.get_attribute("total_energy_consumed")
    def set_energy_price(self):
        self.energy_price = self.get_attribute("energy_price")
    def set_equipment_rental(self):
        self.equipment_rental = self.get_attribute("equipment_rental")
    def set_electricity_tax(self):
        self.electricity_tax = self.get_attribute("electricity_tax")
    def set_energy_cost(self):
        if self.total_energy_consumed is not None and self.energy_price is not None:
            self.energy_cost = round(self.total_energy_consumed * self.energy_price, 2)
    def set_power_cost(self):
        a = self.power_contracted
        b = self.duration
        c = self.power_price
        if a is not None and b is not None and c is not None:
            self.power_cost = round(a * b * c, 2)
    def set_electricity_tax(self):
        a = self.power_cost
        b = self.energy_cost
        c = self.electricity_tax_percentage
        if a is not None and b is not None and c is not None:
            self.electricity_tax = round((a + b) * c / 100, 2)
    def set_iva_tax(self):
        a = self.power_cost
        b = self.energy_cost
        c = self.electricity_tax
        d = self.equipment_rental
        if a is not None and b is not None and c is not None and d is not None:
            self.iva_tax = round((a + b + c + d) * self.iva_percentage / 100, 2)




def proccess_invoice_electric(file):
    miInvoice = Invoice(file)
    miInvoice.create_dataframe()
    miInvoice.set_index_company()
    if miInvoice.idx_company is None:
        return False
    miInvoice.add_row_number_to_df()
    miInvoice.add_length_word_to_df()
    miInvoice.add_is_decimal_to_df()
    print(f"Total de páginas leídas = {miInvoice.n_pages}")
    print(f"Total de filas = {miInvoice.df.shape[0]}")
    print(f"Total de columnas = {miInvoice.df.shape[1]}")
    print(f"ID empresa = {miInvoice.idx_company}")
    print("---------")
    miInvoice.set_power_contracted()
    print(f"Power contracted = {miInvoice.power_contracted}")
    miInvoice.set_duration()
    print(f"Duration = {miInvoice.duration}")
    miInvoice.set_power_price()
    print(f"Power price = {miInvoice.power_price}")
    miInvoice.set_total_energy_consumed()
    print(f"Total energy consumed = {miInvoice.total_energy_consumed}")
    miInvoice.set_energy_price()
    print(f"Energy price = {miInvoice.energy_price}")
    miInvoice.set_equipment_rental()
    print(f"Equipment rental = {miInvoice.equipment_rental}")
    print("---------")
    print("         ")
    print("Campos calculados")
    print("-----------------")
    miInvoice.set_energy_cost()
    print(f"Energy cost = {miInvoice.energy_cost} €")
    miInvoice.set_power_cost()
    print(f"Power cost = {miInvoice.power_cost} €")
    miInvoice.set_electricity_tax()
    print(f"Electricity tax = {miInvoice.electricity_tax} €")
    miInvoice.set_iva_tax()
    print(f"Iva tax = {miInvoice.iva_tax} €")
