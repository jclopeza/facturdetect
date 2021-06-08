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


# Definimos funciones de ayuda para la fusión de líneas
def is_included_in(top1, bottom1, top2, bottom2):
    if bottom1 >= bottom2 and top2 >= top1:
        return True
    if bottom2 >= bottom1 and top1 >= top2:
        return True
    return False

# Definimos primero la función intersección
def is_intersection(top1, bottom1, top2, bottom2):
    if (top2 >= bottom1) or (top1 >= bottom2):
        return (False, 0)
    else:
        # Ahora tenemos que calcular el porcentaje de intersección entre las dos coordenadas
        percentage = 0
        if is_included_in(top1, bottom1, top2, bottom2):
            percentage = 100
        else:
            # Estudiemos ahora el caso en que no hay intersección total
            d1 = bottom1 - top1
            d2 = bottom2 - top2
            # Qué distancia es mayor?
            d = 0
            if d1 >= d2:
                d = 0
                if bottom2 >= bottom1:
                    d = bottom1 - top2
                else:
                    d = bottom2 - top1
                # El 100% = bottom2 - top2
                # Tenemos que ver si d es al menos el 80%
                percentage = d * 100 / d2
            else:
                d = 0
                if bottom1 >= bottom2:
                    d = bottom2 - top1
                else:
                    d = bottom1 - top2
                # El 100% = bottom2 - top2
                # Tenemos que ver si d es al menos el 80%
                percentage = d * 100 / d1
        return (True, percentage)


class Invoice():

    pdf_file_name = None
    df = pd.DataFrame()
    n_pages = 0
    imagenes = []
    row_coordinates = {}
    idx_company = None
    company = None
    rows_to_join = None
    reprocessing_is_necessary = True

    # Datos a completar de las facturas
    power_contracted = None
    duration = None
    power_price = None
    total_energy_consumed = None
    total_energy_consumed_p1 = None
    total_energy_consumed_p2 = None
    energy_price = None
    energy_price_p1 = None
    energy_price_p2 = None
    equipment_rental = None
    electricity_tax_percentage = Decimal(5.11269632)
    electricity_tax = None
    energy_cost = None
    energy_cost_p1 = None
    energy_cost_p2 = None
    power_cost = None
    iva_percentage = Decimal(21)
    iva_tax = None
    tax_base = None
    total_invoice = None

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

    def delete_vertical_text(self):
        self.df.drop(self.df[self.df["upright"] == False].index, inplace=True)

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

    def fix_holaluz_duration(self):
        df = self.df
        list_id_rows = df[df["text"].str.match("\(\d{2}$")].index.to_list()
        if len(list_id_rows) == 1:
            # Eliminamos el primer paréntesis
            new_text = self.df.loc[list_id_rows[0], "text"][1:]
            self.df.loc[list_id_rows[0], "text"] = new_text

    def add_is_decimal_to_df(self):
        self.df["is_decimal"] = self.df.apply(lambda x: is_decimal(x["text"]), axis=1)
    
    # Con esta función tratamos de igual el valor top y bottom
    # de las distintas filas antes de calcular la intersección
    def set_min_and_max_per_row(self):
        df = self.df
        df["min_fila"] = 0
        df["max_fila"] = 0
        for n_page in range(self.n_pages):
            mask_n_page = df["n_page"] == n_page
            df_page = df[mask_n_page]
            for n_fila in df_page["n_fila"].unique():
                mask_n_fila = df["n_fila"] == n_fila
                minimo = df[mask_n_page & mask_n_fila]["top"].min()
                maximo = df[mask_n_page & mask_n_fila]["bottom"].max()
                # Ahora me queda crear dos nuevas columnas con el maximo y minimo de las filas
                df.loc[df[mask_n_page & mask_n_fila].index, "min_fila"] = minimo
                df.loc[df[mask_n_page & mask_n_fila].index, "max_fila"] = maximo

    # Con esta función calculamos las filas que deben unirse si hay
    # un cierto porcentaje de solapamiento, por ejemplo el 80%
    def set_rows_to_join(self):
        df = self.df
        rows_to_join = []
        for n_page in range(self.n_pages):
            mask_n_page = df["n_page"] == n_page
            df_page = df[mask_n_page].sort_values(["n_fila"]).sort_index(axis=0)
            df_filas = df_page["n_fila"].unique()
            for idx, n_fila in enumerate(df_filas):
                if not idx > 0:  # Me interesa tomar las filas de dos en dos
                    continue
                mask_n_fila = df_page["n_fila"] == n_fila
                mask_n_fila_anterior = df_page["n_fila"] == df_filas[idx - 1]
                # Vamos a obtener el máximo y el mínimo de la fila, valores x0 y x1
                top = df_page.loc[df_page[mask_n_fila].index[0], "min_fila"]
                bottom = df_page.loc[df_page[mask_n_fila].index[0], "max_fila"]
                top_anterior = df_page.loc[df_page[mask_n_fila_anterior].index[0], "min_fila"]
                bottom_anterior = df_page.loc[df_page[mask_n_fila_anterior].index[0], "max_fila"]
                res_intersection = is_intersection(top_anterior, bottom_anterior, top, bottom)
                # Nos quedamos con la intersección si al menos se supera el 80%
                if res_intersection[0] and res_intersection[1] >= 100:
                    # print(f"Hay intersección entre las filas {df_filas[idx]} y {df_filas[idx - 1]}")
                    rows_to_join.append([n_page, df_filas[idx], df_filas[idx - 1]])
        self.rows_to_join = rows_to_join


    def join_rows(self):
        self.set_min_and_max_per_row()
        self.set_rows_to_join()
        while(self.reprocessing_is_necessary):
            df = self.df
            self.reprocessing_is_necessary = False
            for idx, data in enumerate(self.rows_to_join):
                try:
                    if data[1] == self.rows_to_join[idx + 1][2]:
                        self.reprocessing_is_necessary = True
                except IndexError:
                    pass
                # Hacemos la actualización asignando la fila menor
                mask_n_page = df["n_page"] == data[0]
                mask_n_fila = (df["n_fila"] == data[1]) | (df["n_fila"] == data[2])
                df.loc[df[mask_n_page & mask_n_fila].index, "n_fila"] = data[2]
            if self.reprocessing_is_necessary:
                self.set_rows_to_join()


    def get_df_shape(self):
        return (self.df.shape[0], self.df.shape[1])

    # Obtenemos el idx de la compañía eléctrica
    def set_index_company(self):
        for idx, company in enumerate(companies):
            score = get_score(self.df, company["text_to_find"])
            if score == 1:
                self.idx_company = idx
                self.company = company["code"]
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

    def get_power_price(self):
        # Debemos saber si el precio facilitado en la factura
        # es anual o no
        cd = companies[self.idx_company]
        power_price = self.get_attribute("power_price")
        if any("año" in s for s in cd["power_price"]["words_to_find"]):
            power_price = round(power_price / 365, 6)
        return power_price

    def get_total_energy_consumed(self):
        cd = companies[self.idx_company]
        energy, energy_p1, energy_p2 = None, None, None
        if "total_energy_consumed" in cd:
            energy = self.get_attribute("total_energy_consumed")
        else:
            energy_p1 = self.get_attribute("total_energy_consumed_p1")
            energy_p2 = self.get_attribute("total_energy_consumed_p2")
        # Devolvemos la terna de valores
        return energy, energy_p1, energy_p2

    def get_energy_price(self):
        cd = companies[self.idx_company]
        price, price_p1, price_p2 = None, None, None
        if "energy_price" in cd:
            price = self.get_attribute("energy_price")
        else:
            price_p1 = self.get_attribute("energy_price_p1")
            price_p2 = self.get_attribute("energy_price_p2")
        return price, price_p1, price_p2

    # Establecemos los valores
    def set_power_contracted(self):
        self.power_contracted = self.get_attribute("power_contracted")
    def set_duration(self):
        self.duration = self.get_attribute("duration")
    def set_power_price(self):
        self.power_price = self.get_power_price()
    def set_total_energy_consumed(self):
        energy, energy_p1, energy_p2 = self.get_total_energy_consumed()
        self.total_energy_consumed = energy
        self.total_energy_consumed_p1 = energy_p1
        self.total_energy_consumed_p2 = energy_p2
    def set_energy_price(self):
        price, price_p1, price_p2 = self.get_energy_price()
        self.energy_price = price
        self.energy_price_p1 = price_p1
        self.energy_price_p2 = price_p2
    def set_equipment_rental(self):
        self.equipment_rental = self.get_attribute("equipment_rental")
    def set_electricity_tax(self):
        self.electricity_tax = self.get_attribute("electricity_tax")
    def set_energy_cost(self):
        if self.total_energy_consumed is not None and self.energy_price is not None:
            self.energy_cost = round(self.total_energy_consumed * self.energy_price, 2)
        elif self.total_energy_consumed_p1 is not None and self.energy_price_p1 is not None and self.total_energy_consumed_p2 is not None and self.energy_price_p2 is not None:
            # Estamos en el caso de unos precios detallados en consumo pico y consumo valle
            self.energy_cost_p1 = round(self.total_energy_consumed_p1 * self.energy_price_p1, 2)
            self.energy_cost_p2 = round(self.total_energy_consumed_p2 * self.energy_price_p2, 2)
            self.energy_cost = self.energy_cost_p1 + self.energy_cost_p2
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
            self.tax_base = a + b + c + d
            self.iva_tax = round(self.tax_base * self.iva_percentage / 100, 2)

    def set_total_invoice(self):
        if self.tax_base is not None and self.iva_tax is not None:
            self.total_invoice = self.tax_base + self.iva_tax

    def detail_energy_consumed(self):
        if self.total_energy_consumed is not None:
            print(f"Total energy consumed = {self.total_energy_consumed}")
        elif self.total_energy_consumed_p1 is not None and self.total_energy_consumed_p2 is not None:
            print(f"Total energy consumed P1 = {self.total_energy_consumed_p1}")
            print(f"Total energy consumed P2 = {self.total_energy_consumed_p2}")

    def detail_energy_price(self):
        if self.energy_price is not None:
            print(f"Energy price = {self.energy_price}")
        elif self.energy_price_p1 is not None and self.energy_price_p2 is not None:
            print(f"Energy price P1 = {self.energy_price_p1}")
            print(f"Energy price P2 = {self.energy_price_p2}")


def proccess_invoice_electric(file):
    miInvoice = Invoice(file)
    miInvoice.create_dataframe()
    miInvoice.set_index_company()
    if companies[miInvoice.idx_company]["code"] == "hol":
        miInvoice.fix_holaluz_duration()
    miInvoice.delete_vertical_text()
    miInvoice.add_row_number_to_df()
    miInvoice.add_length_word_to_df()
    miInvoice.add_is_decimal_to_df()
    miInvoice.join_rows()
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
    miInvoice.detail_energy_consumed()
    # print(f"Total energy consumed = {miInvoice.total_energy_consumed}")
    miInvoice.set_energy_price()
    miInvoice.detail_energy_price()
    # print(f"Energy price = {miInvoice.energy_price}")
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
    miInvoice.set_total_invoice()
    print(f"Total invoice = {miInvoice.total_invoice} €")
    return miInvoice
