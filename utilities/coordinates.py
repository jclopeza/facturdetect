# Invoice number: in
in_percentage_inc_dec = 0.05  # 5% del ancho y alto total de la imagen
in_current_with = 0.11995754
in_current_height = 0.012003001
in_current_left = 0.4447983
in_current_top = 0.03675919
in_new_max_width = in_current_with * (1 + in_percentage_inc_dec)
in_new_max_height = in_current_height * (1 + in_percentage_inc_dec)
in_new_min_width = in_current_with * (1 - in_percentage_inc_dec)
in_new_min_height = in_current_height * (1 - in_percentage_inc_dec)
in_new_min_left = in_current_left - ((in_new_max_width - in_current_with) / 2)
in_new_min_top = in_current_top - ((in_new_max_height - in_current_height) / 2)
in_new_max_left = in_current_left + ((in_new_max_width - in_current_with) / 2)
in_new_max_top = in_current_top + ((in_new_max_height - in_current_height) / 2)


invoice_number = {
    "Type": "WORD",
    "Max_Width": in_new_max_width,
    "Max_Height": in_new_max_height,
    "Min_Width": in_new_min_width,
    "Min_Height": in_new_min_height,
    "Min_Left": in_new_min_left,
    "Min_Top": in_new_min_top,
    "Max_Left": in_new_max_left,
    "Max_Top": in_new_max_top
}

# Periodo de facturación: pf
ip_percentage_inc_dec = 0.05  # 5% del ancho y alto total de la imagen
ip_current_with = 0.12121994
ip_current_height = 0.011608486
ip_current_left = 0.447886
ip_current_top = 0.06431795
ip_new_max_width = ip_current_with * (1 + ip_percentage_inc_dec)
ip_new_max_height = ip_current_height * (1 + ip_percentage_inc_dec)
ip_new_min_width = ip_current_with * (1 - ip_percentage_inc_dec)
ip_new_min_height = ip_current_height * (1 - ip_percentage_inc_dec)
ip_new_min_left = ip_current_left - ((ip_new_max_width - ip_current_with) / 2)
ip_new_min_top = ip_current_top - ((ip_new_max_height - ip_current_height) / 2)
ip_new_max_left = ip_current_left + ((ip_new_max_width - ip_current_with) / 2)
ip_new_max_top = ip_current_top + ((ip_new_max_height - ip_current_height) / 2)


invoice_period = {
    "Type": "LINE",
    "Max_Width": ip_new_max_width,
    "Max_Height": ip_new_max_height,
    "Min_Width": ip_new_min_width,
    "Min_Height": ip_new_min_height,
    "Min_Left": ip_new_min_left,
    "Min_Top": ip_new_min_top,
    "Max_Left": ip_new_max_left,
    "Max_Top": ip_new_max_top
}
