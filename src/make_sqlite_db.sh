rm kicad_parts.sqlite3
python make_res_csv.py
sqlite3 kicad_parts.sqlite3 << 'EOS'
.mode csv
CREATE TABLE Resistors (
    [Part ID]     TEXT PRIMARY KEY,
    Description   TEXT,
    Value         TEXT,
    Tolerance     TEXT,
    Power         TEXT,
    Package       TEXT,
    Height        TEXT,
    Weight        TEXT,
    [Temp (min)]  TEXT,
    [Temp (max)]  TEXT,
    Voltage       TEXT,
    Symbols       TEXT,
    Footprints    TEXT,
    Manufacturers TEXT,
    MPNs          TEXT,
    Prices        TEXT,
    Datasheet     TEXT,
    RoHS          TEXT
);
.import '| tail -n +2 Resistors.csv' Resistors
EOS
