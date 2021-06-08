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
        "equipment_rental": {
            "n_page": 1,
            "words_to_find": ["Alquiler", "equipos"],
            "pos_decimal_value": 0,
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
            "words_to_find": ["del", "mes", "días)"],
            "pos_decimal_value": 0,
        },
        "power_price": {
            "n_page": 0,
            "words_to_find": ["Potencia", "contratados", "día"],
            "pos_decimal_value": 1,
        },
        "total_energy_consumed_p1": {
            "n_page": 0,
            "words_to_find": ["Energía", "(P1)", "disfrutados"],
            "pos_decimal_value": 0,
        },
        "total_energy_consumed_p2": {
            "n_page": 0,
            "words_to_find": ["Energía", "(P2)", "disfrutados"],
            "pos_decimal_value": 0,
        },
        "energy_price_p1": {
            "n_page": 0,
            "words_to_find": ["Energía", "(P1)", "disfrutados"],
            "pos_decimal_value": 1,
        },
        "energy_price_p2": {
            "n_page": 0,
            "words_to_find": ["Energía", "(P2)", "disfrutados"],
            "pos_decimal_value": 1,
        },
        "equipment_rental": {
            "n_page": 0,
            "words_to_find": ["Alquiler", "del", "contador"],
            "pos_decimal_value": 0,
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
        "equipment_rental": {
            "n_page": 1,
            "words_to_find": ["Alquiler", "equipos", "medida"],
            "pos_decimal_value": 1,
        },
    },
    {
        "code": "rep",
        "text_to_find": "Repsol",
        "power_contracted": {
            "n_page": 0,
            "words_to_find": ["Término", "potencia"],
            "pos_decimal_value": 0,
        },
        "duration": {
            "n_page": 0,
            "words_to_find": ["Término", "potencia"],
            "pos_decimal_value": 1,
        },
        "power_price": {
            "n_page": 0,
            # Aquí vamos a utilizar la palabra "año" que aparece en la
            # busqueda para dar cierta lógica y determinar que el precio
            # debe dividirse por 365
            "words_to_find": ["Término", "potencia", "€/kWaño"],
            "pos_decimal_value": 2,
        },
        "total_energy_consumed_p1": {
            "n_page": 0,
            "words_to_find": ["Consumo", "(P1)"],
            "pos_decimal_value": 0,
        },
        "total_energy_consumed_p2": {
            "n_page": 0,
            "words_to_find": ["Consumo", "(P2)"],
            "pos_decimal_value": 0,
        },
        "energy_price_p1": {
            "n_page": 0,
            "words_to_find": ["Consumo", "(P1)"],
            "pos_decimal_value": 1,
        },
        "energy_price_p2": {
            "n_page": 0,
            "words_to_find": ["Consumo", "(P2)"],
            "pos_decimal_value": 1,
        },
        "equipment_rental": {
            "n_page": 0,
            "words_to_find": ["Equipos", "medida"],
            "pos_decimal_value": 0,
        },
    }
]