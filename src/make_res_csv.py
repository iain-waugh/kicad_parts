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

def schem2text(value):
    """Convert 4k7 to 4.7k, 1R to 1, 22M to 22M etc."""
    if value[-1] == "R":
        # If the last character is "R", then just strip it
        new_val = value[:-1]
    elif value[-1] in ["k","M"]:
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
        raise ValueError("Only numbers of the form x.y or x.yy are allowed; you need a decimal point")
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
        raise ValueError("Only numbers of the form x.y or x.yy are allowed; got: ", value)

def gen_range(min_val, max_val, value_list):
    """
    Generate a list of values at different magnitudes, based on a supplied set of values
    
    min_val : a schematic value string, like "10R"
    max_val : a schematic value string, like "10M""
    value_list : the e24 or e96 list, or a custom list
    
    This is really awkward because as soon as you start multiplying floating point
    numbers, you hit rounding precision and you get 8.19999999 instead of 8.2 (for example).
    
    So...  Do the maths in strings (!)  It's only x10, x100, anyway.
    """
    multipliers = [1,10,100]
    mags = ["R","k","M"]
    min_val = str2numeric(min_val, schem=True)
    max_val = str2numeric(max_val, schem=True)
    result = []

    for mag in mags:
        for m in multipliers:
            for v in value_list:
                text_num = str_mult(v, m)
                if "." in text_num:
                    sch_num = re.sub(r"\.", mag, text_num)
                else:                
                    sch_num = text_num + mag
                n = str2numeric(sch_num)
                if n >= min_val and n <= max_val:
                    result.append(sch_num)
    return result

# Define the data
heading = [
    'Part ID',
    'Description',
    'Value',
    'Power',
    'Tolerance',
    'Working Voltage',
    'Package',
    'Height',
    'Weight',
    'Min ℃',
    'Max ℃',
    'Symbols',
    'Footprints',
    'Manufacturers',
    'MPNs',
    'Prices',
    'Datasheet',
    'RoHS'
    ]

e24 = ["1.0", "1.1", "1.2", "1.3", "1.5", "1.6", "1.8", "2.0", "2.2", "2.4", "2.7", "3.0", "3.3", "3.6", "3.9", "4.3", "4.7", "5.1", "5.6", "6.2", "6.8", "7.5", "8.2", "9.1"]
e96 = [
  "1.00", "1.02", "1.05", "1.07", "1.10", "1.13", "1.15", "1.18", "1.21", "1.24", "1.27", "1.30", "1.33", "1.37", "1.40", "1.43", "1.47", "1.50", "1.54", "1.58", "1.62", "1.65", "1.69", "1.74", "1.78", "1.82", "1.87", "1.91", "1.96",
  "2.00", "2.05", "2.10", "2.15", "2.21", "2.26", "2.32", "2.37", "2.43", "2.49", "2.55", "2.61", "2.67", "2.74", "2.80", "2.87", "2.94",
  "3.01", "3.09", "3.16", "3.24", "3.32", "3.40", "3.48", "3.57", "3.65", "3.74", "3.83", "3.92",
  "4.02", "4.12", "4.22", "4.32", "4.42", "4.53", "4.64", "4.75", "4.87", "4.99",
  "5.11", "5.23", "5.36", "5.49", "5.62", "5.76", "5.90",
  "6.04", "6.19", "6.34", "6.49", "6.65", "6.81", "6.98",
  "7.15", "7.32", "7.50", "7.68", "7.87",
  "8.06", "8.25", "8.45", "8.66", "8.87",
  "9.09", "9.31", "9.53", "9.76"
  ]

# Define ranges of Yageo resistors
#   From Table 2 of Yageo RC_L series datasheet
ranges = {
    "0075,1/50W,5%,10V,-55,125": ["10R","1M"],
    "0075,1/50W,1%,10V,-55,125": ["10R","1M"],

    "0100,1/32W,5%,15V,-55,125": ["1R0","22M"],
    "0100,1/32W,1%,15V,-55,125": ["1R0","10M"],
    "0100,1/32W,0.5%,15V,-55,125": ["33R","470k"],

    "0201,1/20W,5%,25V,-55,125": ["1R0","10M"],
    "0201,1/20W,1%,25V,-55,125": ["1R0","10M"],
    "0201,1/20W,0.5%,25V,-55,125": ["10R","1M"],
    "0201,1/20W,0.1%,25V,-55,125": ["10R","1M"],

    "0402,1/16W,5%,50V,-55,155": ["1R0","10M"],
    "0402,1/16W,1%,50V,-55,155": ["1R0","10M"],
    "0402,1/16W,0.5%,50V,-55,155": ["10R","1M"],
    "0402,1/16W,0.1%,50V,-55,155": ["10R","1M"],
    "0402,1/8W,5%,50V,-55,155": ["1R0","1M"],
    "0402,1/8W,1%,50V,-55,155": ["1R0","1M"],

    "0603,1/10W,5%,75V,-55,155": ["1R","22M"],
    "0603,1/10W,1%,75V,-55,155": ["1R","10M"],
    "0603,1/10W,0.5%,75V,-55,155": ["10R","1M"],
    "0603,1/10W,0.1%,75V,-55,155": ["10R","1M"],
    "0603,1/5W,5%,75V,-55,155": ["1R","1M"],
    "0603,1/5W,1%,75V,-55,155": ["1R","1M"],

    "0805,1/8W,5%,150V,-55,155": ["1R","100M"],
    "0805,1/8W,1%,150V,-55,155": ["1R","10M"],
    "0805,1/8W,0.5%,150V,-55,155": ["10R","1M"],
    "0805,1/8W,0.1%,150V,-55,155": ["10R","1M"],
    "0805,1/8W,10%,150V,-55,155": ["24M","100M"],
    "0805,1/8W,20%,150V,-55,155": ["24M","100M"],
    "0805,1/4W,5%,150V,-55,155": ["1R","1M"],
    "0805,1/4W,1%,150V,-55,155": ["1R","1M"],

    "1206,1/4W,5%,200V,-55,155": ["1R","100M"],
    "1206,1/4W,1%,200V,-55,155": ["1R","10M"],
    "1206,1/4W,0.5%,200V,-55,155": ["10R","1M"],
    "1206,1/4W,0.1%,200V,-55,155": ["10R","1M"],
    "1206,1/4W,10%,200V,-55,155": ["24M","100M"],
    "1206,1/4W,20%,200V,-55,155": ["24M","100M"],
    "1206,1/2W,5%,200V,-55,155": ["1R","1M"],
    "1206,1/2W,1%,200V,-55,155": ["1R","1M"],

    "1210,1/2W,5%,200V,-55,155": ["1R","22M"],
    "1210,1/2W,1%,200V,-55,155": ["1R","10M"],
    "1210,1/2W,0.5%,200V,-55,155": ["10R","1M"],
    "1210,1/2W,0.1%,200V,-55,155": ["10R","1M"],

    "1218,1W,5%,200V,-55,155": ["1R","1M"],
    "1218,1W,1%,200V,-55,155": ["1R","1M"],
    "1218,1W,0.5%,200V,-55,155": ["10R","1M"],
    "1218,1W,0.1%,200V,-55,155": ["10R","1M"],

    "2010,3/4W,5%,200V,-55,155": ["1R","22M"],
    "2010,3/4W,1%,200V,-55,155": ["1R","10M"],
    "2010,3/4W,0.5%,200V,-55,155": ["10R","1M"],
    "2010,3/4W,0.1%,200V,-55,155": ["10R","1M"],

    "2512,1W,5%,200V,-55,155": ["1R","22M"],
    "2512,1W,1%,200V,-55,155": ["1R","10M"],
    "2512,1W,0.5%,200V,-55,155": ["10R","1M"],
    "2512,1W,0.1%,200V,-55,155": ["10R","1M"],
    "2512,2W,5%,200V,-55,155": ["1R","1M"],
    "2512,2W,1%,200V,-55,155": ["1R","11M"]
    }

heights = {
    "0075" : "0.10",
    "0100" : "0.13",
    "0201" : "0.23",
    "0402" : "0.35",
    "0603" : "0.45",
    "0805" : "0.50",
    "1206" : "0.55",
    "1210" : "0.50",
    "1218" : "0.55",
    "2010" : "0.55",
    "2512" : "0.55",
    }

# Weight will be rounded up/down to a precision of 1mg
#   so values of 0402 and smaller will be 0
weights_g = {
    "0075" : "0.0", # "0.00004",
    "0100" : "0.0", # "0.0001",
    "0201" : "0.0", # "0.0002",
    "0402" : "0.0", # "0.0006",
    "0603" : "0.002",
    "0805" : "0.004",
    "1206" : "0.010",
    "1210" : "0.016",
    "1218" : "0.027",
    "2010" : "0.027",
    "2512" : "0.045",
    }

part_id_prefix = "PR1-"
part_id_num = 0

csv_file = []
for key in ranges:
    size,power,tol,voltage,minC,maxC = key.split(",")
    min_val,max_val = ranges[key]
    if tol == "5%":
        part_list = gen_range(min_val, max_val, e24)
    else:
        part_list = gen_range(min_val, max_val, e96)
    height=heights[size]
    weight=weights_g[size]
    for part in part_list:
        part_id = str(f"{part_id_prefix}%05d" % part_id_num)
        part_id_num = part_id_num + 1
        csv_file.append([part_id,size,part,power,tol,voltage,minC,maxC,height,weight])

