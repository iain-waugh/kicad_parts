# KiCad Parts

Because a good part library is invaluable when you're designing circuit boards.

## Fields

```
Part ID,Text Description,<Specifics>,Package,Height,Weight,Temperature Range,Symbols,Footprints,Manufacturers,MPNs,Prices,Datasheet,RoHS
```

Where `Specifics` are things directly related to the type of part, like "Voltage", "Current", "Power", etc.

## Text Descriptions

The descriptions are strings with no spaces in them. They are used on the BoM and accurately describe the main parameters of the part (but not the manufacturer).

### Resistor Descriptions (R)

```
RES <type> <value> <tolerance> <power> <package> [RoHS values]
```

Where:

* `<type>` is one of: `CHIP`,`MF`,`WW` (see [Resistor Materials]([Resistor Materials | Resistor Guide](https://eepower.com/resistor-guide/resistor-materials/)))
* `<value>` is a human-readable value like `1.8uF`, `100pF`, etc.
* `<tolerance>` is a percentage value, like `5%`
* `<power>` is a human-readable value like `100V`, `1.5kV`, etc.
* `<package>` describes the package, lie `1206`, `0603`, etc.

Add `/`-separated RoHS values if the part is not RoHS compliant, such as:

* Pb/Hg/Cr6+

Examples:

* `RES CHIP 1.0MOhm 5% 0.5W 0805`
* `RES MF 4.7kOhm 5% 0.25W 6.5mm Pb/Hg`

### Resistor Network Descriptions (RN)

```
RESNET <type> <count> <value> <tolerance> <power> <package> [RoHS values]
```

Where:

- `<type>` is one of: `CHIP`,`ARRAY`
- `<count>` is the number of resistors in the package, 2, 4, 8, etc.
- `<value>` is a human-readable value like `1.8uF`, `100pF`, etc.
- `<tolerance>` is a percentage value, like `5%`
- `<power>` is a human-readable value like `100V`, `1.5kV`, etc.
- `<package>` describes the package, lie `1206`, `0603`, etc.

Add `/`-separated RoHS values if the part is not RoHS compliant, such as:

- Pb/Hg/Cr6+

Examples:

- `RES CHIP 1.0MOhm 5% 0.5W 0805`
- `RES MF 4.7kOhm 5% 0.25W 6.5mm Pb/Hg`

### Capacitor Decriptions (C)

```
CAP <type> <value> <tolerance> <voltage> <package> <material> [RoHS values]
```

Where:

* `<type>` is one of: `CERAMIC`,`TANTALUM`,`ELECTROLYTIC`
* `<value>` is a human-readable value like `1.8uF`, `100pF`, etc.
* `<tolerance>` is a percentage value, like `5%`
* `<voltage>` is a human-readable value like `100V`, `1.5kV`, etc.
* `<package>` describes the package, lie `1206`, `0603`, etc.
* `<material>` is `NPO`, `COG`, `Y5R`, etc.

Add `/`-separated RoHS values if the part is not RoHS compliant, such as:

* Pb/Hg/Cr6+

Examples:

* `CAP CERAMIC 1nF 5% 100V 0805 C0G`

### Inductor Descriptions (L)

```
IND <type> <value> <tolerance> <peak current> <avg current> <power> <package> [RoHS values]
```

Where:

* `<type>` is one of: `POWER`,`RF`
* `<value>` is a human-readable value like `1.8uH`, `100pH`, etc.
* `<tolerance>` is a percentage value, like `5%`
* `<peak current>` is a human-readable value like `5A`, `250mA`, etc.
* `<avg current>` is a human-readable value like `1.5A`, `50mA`, etc.
* `<power>` is a human-readable value like `100V`, `1.5kV`, etc.
* `<package>` describes the package, lie `1206`, `0603`, etc.

Add `/`-separated RoHS values if the part is not RoHS compliant, such as:

* Pb/Hg/Cr6+

Examples:

* `IND POWER 1nH 5% 10A 5A 0805`

### Connectors (J)

```
CON <type> <mounting> PART_NO [RoHS values]
```

### IC Descriptions (U)

```
IC <type> PART_NO <description> [RoHS values]
```

### Optoelectronics Descriptions (O)

```
OPTO <type> PART_NO <description> [RoHS values]
```
