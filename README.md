# KiCad Parts

Because a good part library is invaluable when you're designing.

## Text Descriptions

The descriptions are strings with no spaces in them. They are used on hte BoM to accurately describe the main parameters of the part.

### Resistor Descriptions

```
RES,<type>,<value>,<power>,<package>,<tolerance>,[RoHS values]
```

Where:

* `<type>` is one of: `CHIP`,`MF`,`WW`
* `<value>` is a human-readable value like `1.8uF`, `100pF`, etc.
* `<voltage>` is a human-readable value like `100V`, `1.5kV`, etc.
* `<dielectric>` is `NPO`, `COG`, `Y5R`, etc.
* `<tolerance>` is a percentage value, like `5%`

Add `/`-separated RoHS values if the part is not RoHS compliant, such as:

* Pb/Hg/Cr6+

Examples:

* `RES,CHIP,1.0MOhm,0.5W,0805,5%`
* `RES,AXIAL,4.7kOhm,0.25W,0805,5%,Pb/Hg`

### Capacitor Decriptions

```
CAP,<type>,<value>,<voltage>,<package>,<dielectric>,<tolerance>,[RoHS values]
```

Where:

* `<type>` is one of: `CERAMIC`,`TANTALUM`,`ELECTROLYTIC`
* `<value>` is a human-readable value like `1.8uF`, `100pF`, etc.
* `<voltage>` is a human-readable value like `100V`, `1.5kV`, etc.
* `<dielectric>` is `NPO`, `COG`, `Y5R`, etc.
* `<tolerance>` is a percentage value, like `5%`

Add `/`-separated RoHS values if the part is not RoHS compliant, such as:

* Pb/Hg/Cr6+

Examples:

* `CAP,CERAMIC,1nF,100V,0805,C0G,5%`
