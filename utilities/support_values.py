# Lo siguiente es el texto que se buscará en el dataframe para
# identificar de qué empresa es la factura que se está analizando

companies = [
    {
        "code": "ibe",
        "text_to_find": "A-95758389",
        "power_contracted": {
            "n_page": 1,
            "words_to_find": ["Potencia", "facturada"],
            "pos_decimal_value": 0,
        },
        "duration": {
            "n_page": 1,
            "words_to_find": ["Potencia", "facturada"],
            "pos_decimal_value": 1,
        },
        "power_price": {
            "n_page": 1,
            "words_to_find": ["Potencia", "facturada"],
            "pos_decimal_value": 2,
        },
        "total_energy_consumed": {
            "n_page": 1,
            "words_to_find": ["Energía", "facturada", "kWh"],
            "pos_decimal_value": 0,
        },
        "energy_price": {
            "n_page": 1,
            "words_to_find": ["Energía", "facturada", "kWh"],
            "pos_decimal_value": 1,
        },
        "equipment_rental": {
            "n_page": 1,
            "words_to_find": ["Alquiler", "equipos", "medida"],
            "pos_decimal_value": 0,
        },
    },
    {
        "code": "edp",
        "text_to_find": "EDP",
        "power_contracted": {
            "n_page": 1,
            "words_to_find": ["día(s)", "kW", "día"],
            "pos_decimal_value": 1,
        },
        "duration": {
            "n_page": 1,
            "words_to_find": ["día(s)", "kW", "día"],
            "pos_decimal_value": 0,
        },
        "power_price": {
            "n_page": 1,
            "words_to_find": ["día(s)", "kW", "día"],
            "pos_decimal_value": 2,
        },
        "total_energy_consumed": {
            "n_page": 1,
            "words_to_find": ["-", "kWh", "€/kWh"],
            "pos_decimal_value": 0,
        },
        "energy_price": {
            "n_page": 1,
            "words_to_find": ["-", "kWh", "€/kWh"],
            "pos_decimal_value": 1,
        },
    },
    {
        "code": "hol",
        "text_to_find": "HolaLuz",
        "power_contracted": {
            "n_page": 0,
            "words_to_find": ["Potencia", "contratados", "día"],
            "pos_decimal_value": 0,
        },
        "duration": {
            "n_page": 0,
            "words_to_find": ["del", "mes"],
            "pos_decimal_value": 0,
        },
        "power_price": {
            "n_page": 0,
            "words_to_find": ["Potencia", "contratados", "día"],
            "pos_decimal_value": 1,
        },
        "total_energy_consumed": {
            "n_page": 0,
            "words_to_find": ["Energía", "(P1)", "kWh"],
            "pos_decimal_value": 0,
        },
        "energy_price": {
            "n_page": 0,
            "words_to_find": ["Energía", "(P1)", "kWh"],
            "pos_decimal_value": 1,
        },
    },
    {
        "code": "end",
        "text_to_find": "Endesa",
        "power_contracted": {
            "n_page": 1,
            "words_to_find": ["kW", "x", "Eur/kW"],
            "pos_decimal_value": 0,
        },
        "duration": {
            "n_page": 1,
            "words_to_find": ["kW", "x", "Eur/kW"],
            "pos_decimal_value": 2,
        },
        "power_price": {
            "n_page": 1,
            "words_to_find": ["kW", "x", "Eur/kW"],
            "pos_decimal_value": 1,
        },
         "total_energy_consumed": {
            "n_page": 1,
            "words_to_find": ["kWh", "Eur/kWh"],
            "pos_decimal_value": 0,
        },
        "energy_price": {
            "n_page": 1,
            "words_to_find": ["kWh", "Eur/kWh"],
            "pos_decimal_value": 1,
        },
   }
]