# -*- coding: utf-8 -*-
"""
Copyright (c) 2025 Iain Waugh
All rights reserved.

A script to create a CSV file of available resistors and their characteristics.
The "availability" is based on Yageo's standard part list.

This script deals with 3 different representations of values:
    Schematic value (string): 4R7, 10M, 1k5, etc.
    Text value      (string): 4.7, 10M, 1.5k, etc.
    Numeric value   (number): 4.7, 10000000, 1500, etc.
"""
import re
import pandas as pd


def schem2text(value):
    """Convert 4k7 to 4.7k, 1R to 1, 22M to 22M etc."""
    if value[-1] == "R":
        # If the last character is "R", then just strip it
        new_val = value[:-1]
    elif value[-1] in ["k", "M"]:
        # If the last character is "k" or "M", then leave it
        new_val = value
    else:
        new_val = re.sub(r"(\d+)([RkM])(\d+)", r"\1.\3\2", value)
        if new_val[-1] == "R":
            new_val = new_val[:-1]
    return new_val


def str2numeric(value, schem=True):
    if schem:
        value = schem2text(value)

    if value[-1] == "k":
        return float(value[:-1]) * 1000
    elif value[-1] == "M":
        return float(value[:-1]) * 1000000
    return float(value)


def str_mult(value, mult):
    """Multiply a numeric string by 1, 10 or 100."""
    l = len(value)
    if value[1] != ".":
        raise ValueError(
            "Only numbers of the form x.y or x.yy are allowed; you need a decimal point"
        )
    if mult == 1:
        return value
    elif mult == 10 and l == 3:
        return value[0] + value[2]
    elif mult == 10 and l == 4:
        return value[0] + value[2] + "." + value[3]
    elif mult == 100 and l == 3:
        return value[0] + value[2] + "0"
    elif mult == 100 and l == 4:
        return value[0] + value[2:]
    else:
        raise ValueError(
            "Only numbers of the form x.y or x.yy are allowed; got: ", value
        )


def yageo_code(size, tol, value, power):
    tol_lookup = {
        "0.1%": "B",
        "0.5%": "D",
        "1%": "F",
        "5%": "J",
        "10%": "K",
        "20%": "M",
    }
    tol_code = tol_lookup[tol]

    if size in ["2010"]:
        packaging_code = "K"
    else:
        packaging_code = "R"

    if power == "1/8W":
        reel_code = "7W"
    else:
        reel_code = "07"

    code = (
        "RC"
        + size
        + tol_code
        + packaging_code
        + "-"
        + reel_code
        + value.upper().rstrip("0")
        + "L"
    )

    return code


# Weight will be rounded up/down to a precision of 1mg
#   so values of 0402 and smaller will be 0
#   (a through hole via weighs more)
weights_g = {
    #    "0075" : "0.0", # "0.00004",
    "0100": "0.0",  # "0.0001",
    "0201": "0.0",  # "0.0002",
    "0402": "0.0",  # "0.0006",
    "0603": "0.002",
    "0805": "0.004",
    "1206": "0.010",
    "1210": "0.016",
    "1812": "0.027",
    "2010": "0.027",
    "2220": "0.027",
    "2512": "0.045",
}

# Use standard KiCad SMD resistor footprints
footprints_tbl = {
    #    "0075" : "Capacitor_SMD:R_unavailable",
    "0201": "Capacitor_SMD:C_0201_0603Metric;Capacitor_SMD:C_0201_0603Metric_Pad0.64x0.40mm_HandSolder",
    "0402": "Capacitor_SMD:C_0402_1005Metric;Capacitor_SMD:C_0402_1005Metric_Pad0.74x0.62mm_HandSolder",
    "0603": "Capacitor_SMD:C_0603_1608Metric;Capacitor_SMD:C_0603_1608Metric_Pad1.08x0.95mm_HandSolder",
    "0805": "Capacitor_SMD:C_0805_2012Metric;Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
    "1206": "Capacitor_SMD:C_1206_3216Metric;Capacitor_SMD:C_1206_3216Metric_Pad1.33x1.80mm_HandSolder",
    "1210": "Capacitor_SMD:C_1210_3225Metric;Capacitor_SMD:C_1210_3225Metric_Pad1.33x2.70mm_HandSolder",
    "1812": "Capacitor_SMD:C_1812_4532Metric;Capacitor_SMD:C_1812_4532Metric_Pad1.57x3.40mm_HandSolder",
    "2220": "Capacitor_SMD:C_2220_5750Metric;Capacitor_SMD:C_2220_5750Metric_Pad1.97x5.40mm_HandSolder",
}

temperatures_tbl = {
    "NP0": ["-55", "125", "30ppm/C"],
    "X5R": ["-55", "85", "15%"],
    "X7R": ["-55", "125", "15%"],
    "Y5V": ["-30", "85", "+22% -82%"],
}

datasheet_table = {
    "NP0": "https://www.yageo.com/upload/media/product/products/datasheet/mlcc/UPY-GP_NP0_16V-to-250V_19.pdf",
    "X5R": "https://www.yageo.com/upload/media/product/products/datasheet/mlcc/UPY-GPHC_X5R_4V-to-50V_30.pdf",
    "X7R": "https://www.yageo.com/upload/media/product/products/datasheet/mlcc/UPY-GPHC_X7R_6.3V-to-250V_26.pdfhttps://www.yageo.com/upload/media/product/products/datasheet/mlcc/UPY-GPHC_X7R_6.3V-to-250V_26.pdf",
    "Y5V": "https://www.yageo.com/upload/media/product/products/datasheet/mlcc/UPY-GPHC_Y5V_6.3V-to-50V_14.pdf",
}

part_id_prefix = "PC1-"
part_id_num = 0

csv_columns = [
    [
        "Part ID",
        "Description",
        "Value",
        "Tolerance",
        "Dielectric",
        "Package",
        "Height",
        "Weight",
        "Temp (min)",
        "Temp (max)",
        "Voltage",
        "Symbols",
        "Footprints",
        "Manufacturers",
        "MPNs",
        "Prices",
        "Datasheet",
        "RoHS",
    ]
]
csv_data = csv_columns

# Load the CSV file
df = pd.read_csv("cap_chip_tables.csv", dtype=str, skip_blank_lines=True)

capacitors = []

for _, row in df.iterrows():
    for col in df.columns:
        if "V" in col and col != "Value":
            voltage = col.replace(" ", "")
            value = row[col] if not pd.isna(row[col]) else None
            if value is not None:
                capacitors.append(
                    {
                        "Type": row["Type"],
                        "Dielectric": row["Dielecrtric"],
                        "Package": row["Package"],
                        "Value": row["Value"].replace(" ", ""),
                        "Voltage": voltage,
                        "Height": value,
                    }
                )

for cap in capacitors:
    value = cap["Value"]
    package = cap["Package"]
    dielectric = cap["Dielectric"]
    tol = temperatures_tbl[dielectric][2]
    voltage = cap["Package"]
    minC = temperatures_tbl[dielectric][0]
    maxC = temperatures_tbl[dielectric][1]
    height = cap["Height"]
    weight = weights_g[package]
    symbols = "Passives:C"
    footprints = footprints_tbl[package]
    prices = "100:0.01;20000:0.0003"
    datasheet = datasheet_table[cap["Dielectric"]]
    RoHS = "OK"
    part_id = str(f"{part_id_prefix}%05d" % part_id_num)
    part_id_num = part_id_num + 1
    description = " ".join(["CAP", "CHIP", value, tol, package])
    manufacturers = "Yageo"
    mpns = ""  # yageo_code(package, tol, value, dielectric)
    csv_data.append(
        [
            part_id,
            description,
            value,
            tol,
            dielectric,
            package,
            height,
            weight,
            minC,
            maxC,
            voltage,
            symbols,
            footprints,
            manufacturers,
            mpns,
            prices,
            datasheet,
            RoHS,
        ]
    )

# with open('Resistors.csv', 'w', newline='') as csv_file:
#     writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
#     writer.writerows(csv_data)

csv_df = pd.DataFrame(csv_data, columns=csv_columns)
csv_df.set_index("Part ID")
csv_df.to_csv("Capacitors.csv",header=True)
