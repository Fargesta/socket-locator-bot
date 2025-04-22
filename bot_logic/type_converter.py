def type_to_name(abbr):
    switcher = {
        "220V": "Satandard 2 Pin 220V",
        "4PIN": "Red 4 Pin 380V",
        "5PIN": "Red 5 Pin 380V",
        "UNKN": "Unknown"
    }
    # Use get() to provide a default message for unknown abbreviations
    return switcher.get(abbr.upper(), "Unknown abbreviation")