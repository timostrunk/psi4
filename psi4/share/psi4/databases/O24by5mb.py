#
# @BEGIN LICENSE
#
# Psi4: an open-source quantum chemistry software package
#
# Copyright (c) 2007-2021 The Psi4 Developers.
#
# The copyrights for code used from other parties are included in
# the corresponding files.
#
# This file is part of Psi4.
#
# Psi4 is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3.
#
# Psi4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with Psi4; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# @END LICENSE
#

"""
| Database (O24) of interaction energies for small open-shell high-spin bimolecular complexes.
| Geometries taken from https://gitlab.com/piotr.zuchowski/o24x5/-/tree/4ec3cae0546b6ae4f4f2cf28482cd164c8323cc6.
| Reference interaction energies taken from J. Chem. Phys. 154, 134106 (2021) https://doi.org/10.1063/5.0043793.
| Variant with ghosted hydrogen as midbonds in the COM.
| 
| no | name           | subset
|  1 | CN   - He      | DD
|  2 | NH   - He      | DD
|  3 | C2H3 - C2H4    | DD
|  4 | O2   - H2      | DD
|  5 | NH   - Ar      | DD
|  6 | CN   - Ar      | DD
|  7 | O2   - N2      | DD
|  8 | H2O  - O2(sp)  | DD
|  9 | O2   - O2      | DD
| 10 | NH   - NH      | ED
| 11 | CH2O - NH2     | ED
| 12 | H2O  - Na      | ED
| 13 | H2O  - OH      | ED
| 14 | H2O  - O2H     | ED
| 15 | Li   - NH3(gm) | ED
| 16 | Li   - O2      | MX
| 17 | CN   - H2      | MX
| 18 | Li   - NH3(lm) | MX
| 19 | H2O  - O2(gm)  | MX
| 20 | Na   - Li      | MX
| 21 | CO2  - O2      | MX
| 22 | C2H3 - CO2     | MX
| 23 | He*  - He*     | MX
| 24 | HF   - CO+     | MX

- **cp**  ``'on'``

- **subset**
  - ``'DD'`` dispersion-dominated systems
  - ``'ED'`` electrostatically-dominated systems
  - ``'MX'`` mixed-interaction systems

"""

import re
import qcdb

# <<< O24by5 Database Module >>>
dbse = "O24by5mb"
isOS = "True"

# <<< Database Members >>>
DIST = ["-0.9", "-1.0", "-1.2", "-1.5", "-2.0"]
HRXN = [str(rxn) + d for rxn in range(1, 25) for d in DIST]
#HRXN_SM = []
#HRXN_LG = []
HRXN_DD = [str(rxn) + d for rxn in [1, 2, 3, 4, 5, 6, 7, 8, 9] for d in DIST]
HRXN_ED = [str(rxn) + d for rxn in [10, 11, 12, 13, 14, 15] for d in DIST]
HRXN_MX = [str(rxn) + d for rxn in [16, 17, 18, 19, 20, 21, 22, 23, 24] for d in DIST]


# <<< Chemical Systems Involved >>>
RXNM = {}  # reaction matrix of reagent contributions per reaction
ACTV = {}  # order of active reagents per counterpoise-corrected reaction
ACTV_CP = {}  # order of active reagents per counterpoise-corrected reaction
ACTV_SA = {}  # order of active reagents for non-supermolecular calculations
for rxn in HRXN:
    RXNM["%s-%s" % (dbse, rxn)] = {
        "%s-%s-dimer" % (dbse, rxn): +1,
        "%s-%s-monoA-CP" % (dbse, rxn): -1,
        "%s-%s-monoB-CP" % (dbse, rxn): -1,
    }

    ACTV["%s-%s" % (dbse, rxn)] = [
        "%s-%s-dimer" % (dbse, rxn),
        "%s-%s-monoA-CP" % (dbse, rxn),
        "%s-%s-monoB-CP" % (dbse, rxn),
    ]

    ACTV_SA["%s-%s" % (dbse, rxn)] = ["%s-%s-dimer" % (dbse, rxn)]

    ACTV_CP["%s-%s" % (dbse, rxn)] = [
        "%s-%s-dimer" % (dbse, rxn),
        "%s-%s-monoA-CP" % (dbse, rxn),
        "%s-%s-monoB-CP" % (dbse, rxn),
    ]

# <<< Reference Values  >>>
BIND = {}
# original publication values in CM^-1 TABLE IV
# 1
BIND["%s-%s" % (dbse, "1-0.9")] = +4.26
BIND["%s-%s" % (dbse, "1-1.0")] = -19.58
BIND["%s-%s" % (dbse, "1-1.2")] = -11.24
BIND["%s-%s" % (dbse, "1-1.5")] = -2.91
BIND["%s-%s" % (dbse, "1-2.0")] = -0.48
# 2
BIND["%s-%s" % (dbse, "2-0.9")] = -7.28
BIND["%s-%s" % (dbse, "2-1.0")] = -19.69
BIND["%s-%s" % (dbse, "2-1.2")] = -10.38
BIND["%s-%s" % (dbse, "2-1.5")] = -2.73
BIND["%s-%s" % (dbse, "2-2.0")] = -0.41
# 3
BIND["%s-%s" % (dbse, "3-0.9")] = +1.78
BIND["%s-%s" % (dbse, "3-1.0")] = -34.94
BIND["%s-%s" % (dbse, "3-1.2")] = -10.96
BIND["%s-%s" % (dbse, "3-1.5")] = +2.75
BIND["%s-%s" % (dbse, "3-2.0")] = +2.27
# 4
BIND["%s-%s" % (dbse, "4-0.9")] = -16.64
BIND["%s-%s" % (dbse, "4-1.0")] = -54.60
BIND["%s-%s" % (dbse, "4-1.2")] = -31.11
BIND["%s-%s" % (dbse, "4-1.5")] = -8.46
BIND["%s-%s" % (dbse, "4-2.0")] = -1.40
# 5
BIND["%s-%s" % (dbse, "5-0.9")] = -88.71
BIND["%s-%s" % (dbse, "5-1.0")] = -98.44
BIND["%s-%s" % (dbse, "5-1.2")] = -42.26
BIND["%s-%s" % (dbse, "5-1.5")] = -10.30
BIND["%s-%s" % (dbse, "5-2.0")] = -1.59
# 6
BIND["%s-%s" % (dbse, "6-0.9")] = +52.69
BIND["%s-%s" % (dbse, "6-1.0")] = -110.43
BIND["%s-%s" % (dbse, "6-1.2")] = -66.45
BIND["%s-%s" % (dbse, "6-1.5")] = -16.57
BIND["%s-%s" % (dbse, "6-2.0")] = -2.59
# 7
BIND["%s-%s" % (dbse, "7-0.9")] = -31.62
BIND["%s-%s" % (dbse, "7-1.0")] = -113.64
BIND["%s-%s" % (dbse, "7-1.2")] = -62.69
BIND["%s-%s" % (dbse, "7-1.5")] = -16.71
BIND["%s-%s" % (dbse, "7-2.0")] = -2.75
# 8
BIND["%s-%s" % (dbse, "8-0.9")] = -13.09
BIND["%s-%s" % (dbse, "8-1.0")] = -125.01
BIND["%s-%s" % (dbse, "8-1.2")] = -59.42
BIND["%s-%s" % (dbse, "8-1.5")] = -8.94
BIND["%s-%s" % (dbse, "8-2.0")] = +0.95
# 9 O2 - O2
BIND["%s-%s" % (dbse, "9-0.9")] = -66.46
BIND["%s-%s" % (dbse, "9-1.0")] = -134.40
BIND["%s-%s" % (dbse, "9-1.2")] = -71.34
BIND["%s-%s" % (dbse, "9-1.5")] = -19.24
BIND["%s-%s" % (dbse, "9-2.0")] = -3.15
# 10 NH - NH
BIND["%s-%s" % (dbse, "10-0.9")] = -465.81
BIND["%s-%s" % (dbse, "10-1.0")] = -697.47
BIND["%s-%s" % (dbse, "10-1.2")] = -459.91
BIND["%s-%s" % (dbse, "10-1.5")] = -205.70
BIND["%s-%s" % (dbse, "10-2.0")] = -76.67
# 11
BIND["%s-%s" % (dbse, "11-0.9")] = -762.53
BIND["%s-%s" % (dbse, "11-1.0")] = -1027.31
BIND["%s-%s" % (dbse, "11-1.2")] = -731.41
BIND["%s-%s" % (dbse, "11-1.5")] = -339.71
BIND["%s-%s" % (dbse, "11-2.0")] = -125.01
# 12
BIND["%s-%s" % (dbse, "12-0.9")] = -645.24
BIND["%s-%s" % (dbse, "12-1.0")] = -1791.08
BIND["%s-%s" % (dbse, "12-1.2")] = -1283.10
BIND["%s-%s" % (dbse, "12-1.5")] = -521.59
BIND["%s-%s" % (dbse, "12-2.0")] = -137.13
# 13
BIND["%s-%s" % (dbse, "13-0.9")] = -1431.56
BIND["%s-%s" % (dbse, "13-1.0")] = -1983.78
BIND["%s-%s" % (dbse, "13-1.2")] = -1352.50
BIND["%s-%s" % (dbse, "13-1.5")] = -598.20
BIND["%s-%s" % (dbse, "13-2.0")] = -206.86
# 14
BIND["%s-%s" % (dbse, "14-0.9")] = -2408.67
BIND["%s-%s" % (dbse, "14-1.0")] = -2647.19
BIND["%s-%s" % (dbse, "14-1.2")] = -1597.02
BIND["%s-%s" % (dbse, "14-1.5")] = -678.35
BIND["%s-%s" % (dbse, "14-2.0")] = -234.81
# 15
BIND["%s-%s" % (dbse, "15-0.9")] = -3965.73
BIND["%s-%s" % (dbse, "15-1.0")] = -5014.58
BIND["%s-%s" % (dbse, "15-1.2")] = -3810.80
BIND["%s-%s" % (dbse, "15-1.5")] = -1673.44
BIND["%s-%s" % (dbse, "15-2.0")] = -422.38
# 16 Li - O2
BIND["%s-%s" % (dbse, "16-0.9")] = -14.70
BIND["%s-%s" % (dbse, "16-1.0")] = -36.31
BIND["%s-%s" % (dbse, "16-1.2")] = -24.41
BIND["%s-%s" % (dbse, "16-1.5")] = -7.19
BIND["%s-%s" % (dbse, "16-2.0")] = -1.13
# 17
BIND["%s-%s" % (dbse, "17-0.9")] = -16.05
BIND["%s-%s" % (dbse, "17-1.0")] = -50.41
BIND["%s-%s" % (dbse, "17-1.2")] = -28.51
BIND["%s-%s" % (dbse, "17-1.5")] = -7.71
BIND["%s-%s" % (dbse, "17-2.0")] = -1.26
# 18
BIND["%s-%s" % (dbse, "18-0.9")] = -87.23
BIND["%s-%s" % (dbse, "18-1.0")] = -103.77
BIND["%s-%s" % (dbse, "18-1.2")] = -73.10
BIND["%s-%s" % (dbse, "18-1.5")] = -25.73
BIND["%s-%s" % (dbse, "18-2.0")] = -4.32
# 19 H2O - O2 (gm)
BIND["%s-%s" % (dbse, "19-0.9")] = -73.37
BIND["%s-%s" % (dbse, "19-1.0")] = -223.22
BIND["%s-%s" % (dbse, "19-1.2")] = -126.50
BIND["%s-%s" % (dbse, "19-1.5")] = -35.99
BIND["%s-%s" % (dbse, "19-2.0")] = -6.77
# 20 Na - Li
BIND["%s-%s" % (dbse, "20-0.9")] = -210.40
BIND["%s-%s" % (dbse, "20-1.0")] = -259.27
BIND["%s-%s" % (dbse, "20-1.2")] = -188.18
BIND["%s-%s" % (dbse, "20-1.5")] = -75.17
BIND["%s-%s" % (dbse, "20-2.0")] = -14.25
# 21
BIND["%s-%s" % (dbse, "21-0.9")] = -187.20
BIND["%s-%s" % (dbse, "21-1.0")] = -266.29
BIND["%s-%s" % (dbse, "21-1.2")] = -132.52
BIND["%s-%s" % (dbse, "21-1.5")] = -36.14
BIND["%s-%s" % (dbse, "21-2.0")] = -6.37
# 22
BIND["%s-%s" % (dbse, "22-0.9")] = -366.42
BIND["%s-%s" % (dbse, "22-1.0")] = -658.94
BIND["%s-%s" % (dbse, "22-1.2")] = -415.05
BIND["%s-%s" % (dbse, "22-1.5")] = -140.79
BIND["%s-%s" % (dbse, "22-2.0")] = -31.54
# 23
BIND["%s-%s" % (dbse, "23-0.9")] = -826.91
BIND["%s-%s" % (dbse, "23-1.0")] = -1018.90
BIND["%s-%s" % (dbse, "23-1.2")] = -790.24
BIND["%s-%s" % (dbse, "23-1.5")] = -341.29
BIND["%s-%s" % (dbse, "23-2.0")] = -74.18
# 24
BIND["%s-%s" % (dbse, "24-0.9")] = -8922.76
BIND["%s-%s" % (dbse, "24-1.0")] = -10324.99
BIND["%s-%s" % (dbse, "24-1.2")] = -7656.09
BIND["%s-%s" % (dbse, "24-1.5")] = -3703.01
BIND["%s-%s" % (dbse, "24-2.0")] = -1641.58

# scale back to kcal/mol
KCALMOL2WAVENUMBERS = 349.7551
for key, value in BIND.items():
    BIND[key] = value / KCALMOL2WAVENUMBERS

# <<< Comment Lines >>>
TAGL = {}
TAGL["%s-%s" % (dbse, "1-0.9")] = """ CN He R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "1-0.9")] = """Dimer from CN - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "1-0.9")] = """Monomer A CN - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "1-0.9")] = """Monomer B CN - He"""
TAGL["%s-%s" % (dbse, "1-1.0")] = """ CN He R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "1-1.0")] = """Dimer from CN He"""
TAGL["%s-%s-monoA-CP" % (dbse, "1-1.0")] = """Monomer A CN - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "1-1.0")] = """Monomer B CN - He"""
TAGL["%s-%s" % (dbse, "1-1.2")] = """ CN He R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "1-1.2")] = """Dimer from CN He"""
TAGL["%s-%s-monoA-CP" % (dbse, "1-1.2")] = """Monomer A CN - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "1-1.2")] = """Monomer B CN - He"""
TAGL["%s-%s" % (dbse, "1-1.5")] = """ CN He R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "1-1.5")] = """Dimer from CN - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "1-1.5")] = """Monomer A CN - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "1-1.5")] = """Monomer B CN - He"""
TAGL["%s-%s" % (dbse, "1-2.0")] = """ CN He R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "1-2.0")] = """Dimer from CN - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "1-2.0")] = """Monomer A CN - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "1-2.0")] = """Monomer B CN - He"""
TAGL["%s-%s" % (dbse, "2-0.9")] = """ NH He R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "2-0.9")] = """Dimer from NH - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "2-0.9")] = """Monomer A NH - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "2-0.9")] = """Monomer B NH - He"""
TAGL["%s-%s" % (dbse, "2-1.0")] = """ NH He """
TAGL["%s-%s-dimer" % (dbse, "2-1.0")] = """Dimer from NH - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "2-1.0")] = """Monomer A NH - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "2-1.0")] = """Monomer B NH - He"""
TAGL["%s-%s" % (dbse, "2-1.2")] = """ NH He R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "2-1.2")] = """Dimer from NH - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "2-1.2")] = """Monomer A NH - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "2-1.2")] = """Monomer B NH - He"""
TAGL["%s-%s" % (dbse, "2-1.5")] = """ NH He R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "2-1.5")] = """Dimer from NH - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "2-1.5")] = """Monomer A NH - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "2-1.5")] = """Monomer B NH - He"""
TAGL["%s-%s" % (dbse, "2-2.0")] = """ NH He R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "2-2.0")] = """Dimer from NH - He"""
TAGL["%s-%s-monoA-CP" % (dbse, "2-2.0")] = """Monomer A NH - He"""
TAGL["%s-%s-monoB-CP" % (dbse, "2-2.0")] = """Monomer B NH - He"""
TAGL["%s-%s" % (dbse, "3-0.9")] = """ C2H3 - C2H4 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "3-0.9")] = """Dimer from C2H3 - C2H4"""
TAGL["%s-%s-monoA-CP" % (dbse, "3-0.9")] = """Monomer A C2H3 - C2H4"""
TAGL["%s-%s-monoB-CP" % (dbse, "3-0.9")] = """Monomer B C2H3 - C2H4"""
TAGL["%s-%s" % (dbse, "3-1.0")] = """ C2H3 - C2H4 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "3-1.0")] = """Dimer from C2H3 - C2H4"""
TAGL["%s-%s-monoA-CP" % (dbse, "3-1.0")] = """Monomer A C2H3 - C2H4"""
TAGL["%s-%s-monoB-CP" % (dbse, "3-1.0")] = """Monomer B C2H3 - C2H4"""
TAGL["%s-%s" % (dbse, "3-1.2")] = """ C2H3 - C2H4 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "3-1.2")] = """Dimer from C2H3 - C2H4"""
TAGL["%s-%s-monoA-CP" % (dbse, "3-1.2")] = """Monomer A C2H3 - C2H4"""
TAGL["%s-%s-monoB-CP" % (dbse, "3-1.2")] = """Monomer B C2H3 - C2H4"""
TAGL["%s-%s" % (dbse, "3-1.5")] = """C2H3 C2H4 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "3-1.5")] = """Dimer from C2H3 - C2H4"""
TAGL["%s-%s-monoA-CP" % (dbse, "3-1.5")] = """Monomer A C2H3 - C2H4"""
TAGL["%s-%s-monoB-CP" % (dbse, "3-1.5")] = """Monomer B C2H3 - C2H4"""
TAGL["%s-%s" % (dbse, "3-2.0")] = """ C2H3 C2H4 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "3-2.0")] = """Dimer from C2H3 - C2H4"""
TAGL["%s-%s-monoA-CP" % (dbse, "3-2.0")] = """Monomer A C2H3 - C2H4"""
TAGL["%s-%s-monoB-CP" % (dbse, "3-2.0")] = """Monomer B C2H3 - C2H4"""
TAGL["%s-%s" % (dbse, "4-0.9")] = """ O2 H2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "4-0.9")] = """Dimer from O2 - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "4-0.9")] = """Monomer A O2 - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "4-0.9")] = """Monomer B O2 - H2"""
TAGL["%s-%s" % (dbse, "4-1.0")] = """ O2 H2 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "4-1.0")] = """Dimer from O2 - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "4-1.0")] = """Monomer A O2 - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "4-1.0")] = """Monomer B O2 - H2"""
TAGL["%s-%s" % (dbse, "4-1.2")] = """ O2 H2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "4-1.2")] = """Dimer from O2 - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "4-1.2")] = """Monomer A O2 - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "4-1.2")] = """Monomer B O2 - H2"""
TAGL["%s-%s" % (dbse, "4-1.5")] = """ O2 H2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "4-1.5")] = """Dimer from O2 - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "4-1.5")] = """Monomer A O2 - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "4-1.5")] = """Monomer B O2 - H2"""
TAGL["%s-%s" % (dbse, "4-2.0")] = """ O2 H2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "4-2.0")] = """Dimer from O2 - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "4-2.0")] = """Monomer A O2 - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "4-2.0")] = """Monomer B O2 - H2"""
TAGL["%s-%s" % (dbse, "5-0.9")] = """ NH Ar R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "5-0.9")] = """Dimer from NH - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "5-0.9")] = """Monomer A NH - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "5-0.9")] = """Monomer B NH - Ar"""
TAGL["%s-%s" % (dbse, "5-1.0")] = """ NH Ar R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "5-1.0")] = """Dimer from NH - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "5-1.0")] = """Monomer A NH - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "5-1.0")] = """Monomer B NH - Ar"""
TAGL["%s-%s" % (dbse, "5-1.2")] = """ NH Ar R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "5-1.2")] = """Dimer from NH - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "5-1.2")] = """Monomer A NH - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "5-1.2")] = """Monomer B NH - Ar"""
TAGL["%s-%s" % (dbse, "5-1.5")] = """ NH Ar R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "5-1.5")] = """Dimer from NH - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "5-1.5")] = """Monomer A NH - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "5-1.5")] = """Monomer B NH - Ar"""
TAGL["%s-%s" % (dbse, "5-2.0")] = """ NH Ar R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "5-2.0")] = """Dimer from NH - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "5-2.0")] = """Monomer A NH - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "5-2.0")] = """Monomer B NH - Ar"""
TAGL["%s-%s" % (dbse, "6-0.9")] = """ CN Ar R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "6-0.9")] = """Dimer from CN - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "6-0.9")] = """Monomer A CN - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "6-0.9")] = """Monomer B CN - Ar"""
TAGL["%s-%s" % (dbse, "6-1.0")] = """ CN Ar R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "6-1.0")] = """Dimer from CN - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "6-1.0")] = """Monomer A CN - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "6-1.0")] = """Monomer B CN - Ar"""
TAGL["%s-%s" % (dbse, "6-1.2")] = """ CN Ar R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "6-1.2")] = """Dimer from CN - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "6-1.2")] = """Monomer A CN - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "6-1.2")] = """Monomer B CN - Ar"""
TAGL["%s-%s" % (dbse, "6-1.5")] = """ CN Ar R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "6-1.5")] = """Dimer from CN - Ar"""
TAGL["%s-%s-monoA-CP" % (dbse, "6-1.5")] = """Monomer A CN - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "6-1.5")] = """Monomer B CN - Ar"""
TAGL["%s-%s" % (dbse, "6-2.0")] = """ CN Ar R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "6-2.0")] = """Dimer from CN - Ar """
TAGL["%s-%s-monoA-CP" % (dbse, "6-2.0")] = """Monomer A CN - Ar"""
TAGL["%s-%s-monoB-CP" % (dbse, "6-2.0")] = """Monomer B CN - Ar"""
TAGL["%s-%s" % (dbse, "7-0.9")] = """ O2 N2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "7-0.9")] = """Dimer from O2 - N2"""
TAGL["%s-%s-monoA-CP" % (dbse, "7-0.9")] = """Monomer A O2 - N2"""
TAGL["%s-%s-monoB-CP" % (dbse, "7-0.9")] = """Monomer B O2 - N2"""
TAGL["%s-%s" % (dbse, "7-1.0")] = """ O2 N2 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "7-1.0")] = """Dimer from O2 - N2"""
TAGL["%s-%s-monoA-CP" % (dbse, "7-1.0")] = """Monomer A O2 - N2"""
TAGL["%s-%s-monoB-CP" % (dbse, "7-1.0")] = """Monomer B O2 - N2"""
TAGL["%s-%s" % (dbse, "7-1.2")] = """ O2 N2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "7-1.2")] = """Dimer from O2 - N2"""
TAGL["%s-%s-monoA-CP" % (dbse, "7-1.2")] = """Monomer A O2 - N2"""
TAGL["%s-%s-monoB-CP" % (dbse, "7-1.2")] = """Monomer B O2 - N2"""
TAGL["%s-%s" % (dbse, "7-1.5")] = """ O2 N2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "7-1.5")] = """Dimer from O2 - N2"""
TAGL["%s-%s-monoA-CP" % (dbse, "7-1.5")] = """Monomer A O2 - N2"""
TAGL["%s-%s-monoB-CP" % (dbse, "7-1.5")] = """Monomer B O2 - N2"""
TAGL["%s-%s" % (dbse, "7-2.0")] = """ O2 N2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "7-2.0")] = """Dimer from O2 - N2"""
TAGL["%s-%s-monoA-CP" % (dbse, "7-2.0")] = """Monomer A O2 - N2"""
TAGL["%s-%s-monoB-CP" % (dbse, "7-2.0")] = """Monomer B O2 - N2"""
TAGL["%s-%s" % (dbse, "8-0.9")] = """ H2O O2 (sp) R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "8-0.9")] = """Dimer from H2O - O2 (sp)"""
TAGL["%s-%s-monoA-CP" % (dbse, "8-0.9")] = """Monomer A H2O - O2 (sp)"""
TAGL["%s-%s-monoB-CP" % (dbse, "8-0.9")] = """Monomer B H2O - O2 (sp)"""
TAGL["%s-%s" % (dbse, "8-1.0")] = """ H2O O2 (sp) R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "8-1.0")] = """Dimer from H2O - O2 (sp)"""
TAGL["%s-%s-monoA-CP" % (dbse, "8-1.0")] = """Monomer A H2O - O2 (sp)"""
TAGL["%s-%s-monoB-CP" % (dbse, "8-1.0")] = """Monomer B H2O - O2 (sp)"""
TAGL["%s-%s" % (dbse, "8-1.2")] = """ H2O O2 (sp) R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "8-1.2")] = """Dimer from H2O - O2 (sp)"""
TAGL["%s-%s-monoA-CP" % (dbse, "8-1.2")] = """Monomer A H2O - O2 (sp)"""
TAGL["%s-%s-monoB-CP" % (dbse, "8-1.2")] = """Monomer B H2O - O2 (sp)"""
TAGL["%s-%s" % (dbse, "8-1.5")] = """ H2O O2 (sp) R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "8-1.5")] = """Dimer from H2O - O2 (sp)"""
TAGL["%s-%s-monoA-CP" % (dbse, "8-1.5")] = """Monomer A H2O - O2 (sp)"""
TAGL["%s-%s-monoB-CP" % (dbse, "8-1.5")] = """Monomer B H2O - O2 (sp)"""
TAGL["%s-%s" % (dbse, "8-2.0")] = """ H2O O2 (sp) R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "8-2.0")] = """Dimer from H2O - O2 (sp)"""
TAGL["%s-%s-monoA-CP" % (dbse, "8-2.0")] = """Monomer A H2O - O2 (sp)"""
TAGL["%s-%s-monoB-CP" % (dbse, "8-2.0")] = """Monomer B H2O - O2 (sp)"""
TAGL["%s-%s" % (dbse, "9-0.9")] = """ O2 O2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "9-0.9")] = """Dimer from O2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "9-0.9")] = """Monomer A O2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "9-0.9")] = """Monomer B O2 - O2"""
TAGL["%s-%s" % (dbse, "9-1.0")] = """ O2 O2 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "9-1.0")] = """Dimer from O2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "9-1.0")] = """Monomer A O2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "9-1.0")] = """Monomer B O2 - O2"""
TAGL["%s-%s" % (dbse, "9-1.2")] = """ O2 O2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "9-1.2")] = """Dimer from O2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "9-1.2")] = """Monomer A O2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "9-1.2")] = """Monomer B O2 - O2"""
TAGL["%s-%s" % (dbse, "9-1.5")] = """ O2 O2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "9-1.5")] = """Dimer from O2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "9-1.5")] = """Monomer A O2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "9-1.5")] = """Monomer B O2 - O2"""
TAGL["%s-%s" % (dbse, "9-2.0")] = """ O2 O2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "9-2.0")] = """Dimer from O2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "9-2.0")] = """Monomer A O2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "9-2.0")] = """Monomer B O2 - O2"""
TAGL["%s-%s" % (dbse, "10-0.9")] = """ NH NH R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "10-0.9")] = """Dimer from NH - NH"""
TAGL["%s-%s-monoA-CP" % (dbse, "10-0.9")] = """Monomer A NH - NH"""
TAGL["%s-%s-monoB-CP" % (dbse, "10-0.9")] = """Monomer B NH - NH"""
TAGL["%s-%s" % (dbse, "10-1.0")] = """ NH NH R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "10-1.0")] = """Dimer from NH - NH"""
TAGL["%s-%s-monoA-CP" % (dbse, "10-1.0")] = """Monomer A NH - NH"""
TAGL["%s-%s-monoB-CP" % (dbse, "10-1.0")] = """Monomer B NH - NH"""
TAGL["%s-%s" % (dbse, "10-1.2")] = """ NH NH R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "10-1.2")] = """Dimer from NH - NH"""
TAGL["%s-%s-monoA-CP" % (dbse, "10-1.2")] = """Monomer A NH - NH"""
TAGL["%s-%s-monoB-CP" % (dbse, "10-1.2")] = """Monomer B NH - NH"""
TAGL["%s-%s" % (dbse, "10-1.5")] = """ NH NH R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "10-1.5")] = """Dimer from NH - NH"""
TAGL["%s-%s-monoA-CP" % (dbse, "10-1.5")] = """Monomer A NH - NH"""
TAGL["%s-%s-monoB-CP" % (dbse, "10-1.5")] = """Monomer B NH - NH"""
TAGL["%s-%s" % (dbse, "10-2.0")] = """ NH NH R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "10-2.0")] = """Dimer from NH - NH"""
TAGL["%s-%s-monoA-CP" % (dbse, "10-2.0")] = """Monomer A NH - NH"""
TAGL["%s-%s-monoB-CP" % (dbse, "10-2.0")] = """Monomer B NH - NH"""
TAGL["%s-%s" % (dbse, "11-0.9")] = """ CH2O NH2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "11-0.9")] = """Dimer from CH2O - NH2 """
TAGL["%s-%s-monoA-CP" % (dbse, "11-0.9")] = """Monomer A CH2O - NH2  """
TAGL["%s-%s-monoB-CP" % (dbse, "11-0.9")] = """Monomer B CH2O - NH2  """
TAGL["%s-%s" % (dbse, "11-1.0")] = """ CH2O NH2 R=1.1"""
TAGL["%s-%s-dimer" % (dbse, "11-1.0")] = """Dimer from CH2O - NH2 """
TAGL["%s-%s-monoA-CP" % (dbse, "11-1.0")] = """Monomer A CH2O - NH2  """
TAGL["%s-%s-monoB-CP" % (dbse, "11-1.0")] = """Monomer B CH2O - NH2  """
TAGL["%s-%s" % (dbse, "11-1.2")] = """ CH2O NH2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "11-1.2")] = """Dimer from CH2O - NH2 """
TAGL["%s-%s-monoA-CP" % (dbse, "11-1.2")] = """Monomer A CH2O - NH2  """
TAGL["%s-%s-monoB-CP" % (dbse, "11-1.2")] = """Monomer B CH2O - NH2  """
TAGL["%s-%s" % (dbse, "11-1.5")] = """ CH2O NH2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "11-1.5")] = """Dimer from CH2O - NH2 """
TAGL["%s-%s-monoA-CP" % (dbse, "11-1.5")] = """Monomer A CH2O - NH2  """
TAGL["%s-%s-monoB-CP" % (dbse, "11-1.5")] = """Monomer B CH2O - NH2  """
TAGL["%s-%s" % (dbse, "11-2.0")] = """ CH2O NH2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "11-2.0")] = """Dimer from CH2O - NH2 """
TAGL["%s-%s-monoA-CP" % (dbse, "11-2.0")] = """Monomer A CH2O - NH2  """
TAGL["%s-%s-monoB-CP" % (dbse, "11-2.0")] = """Monomer B CH2O - NH2  """
TAGL["%s-%s" % (dbse, "12-0.9")] = """ H2O Na R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "12-0.9")] = """Dimer from H2O - Na"""
TAGL["%s-%s-monoA-CP" % (dbse, "12-0.9")] = """Monomer A H2O - Na"""
TAGL["%s-%s-monoB-CP" % (dbse, "12-0.9")] = """Monomer B H2O - Na"""
TAGL["%s-%s" % (dbse, "12-1.0")] = """ H2O Na R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "12-1.0")] = """Dimer from H2O - Na"""
TAGL["%s-%s-monoA-CP" % (dbse, "12-1.0")] = """Monomer A H2O - Na"""
TAGL["%s-%s-monoB-CP" % (dbse, "12-1.0")] = """Monomer B H2O - Na"""
TAGL["%s-%s" % (dbse, "12-1.2")] = """ H2O Na R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "12-1.2")] = """Dimer from H2O - Na"""
TAGL["%s-%s-monoA-CP" % (dbse, "12-1.2")] = """Monomer A H2O - Na"""
TAGL["%s-%s-monoB-CP" % (dbse, "12-1.2")] = """Monomer B H2O - Na"""
TAGL["%s-%s" % (dbse, "12-1.5")] = """ H2O Na R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "12-1.5")] = """Dimer from H2O - Na"""
TAGL["%s-%s-monoA-CP" % (dbse, "12-1.5")] = """Monomer A H2O - Na"""
TAGL["%s-%s-monoB-CP" % (dbse, "12-1.5")] = """Monomer B H2O - Na"""
TAGL["%s-%s" % (dbse, "12-2.0")] = """ H2O Na R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "12-2.0")] = """Dimer from H2O - Na"""
TAGL["%s-%s-monoA-CP" % (dbse, "12-2.0")] = """Monomer A H2O - Na"""
TAGL["%s-%s-monoB-CP" % (dbse, "12-2.0")] = """Monomer B H2O - Na"""
TAGL["%s-%s" % (dbse, "13-0.9")] = """ H2O OH R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "13-0.9")] = """Dimer from H2O - OH"""
TAGL["%s-%s-monoA-CP" % (dbse, "13-0.9")] = """Monomer A H2O - OH"""
TAGL["%s-%s-monoB-CP" % (dbse, "13-0.9")] = """Monomer B H2O - OH"""
TAGL["%s-%s" % (dbse, "13-1.0")] = """ H2O OH """
TAGL["%s-%s-dimer" % (dbse, "13-1.0")] = """Dimer from H2O - OH"""
TAGL["%s-%s-monoA-CP" % (dbse, "13-1.0")] = """Monomer A H2O - OH"""
TAGL["%s-%s-monoB-CP" % (dbse, "13-1.0")] = """Monomer B H2O - OH"""
TAGL["%s-%s" % (dbse, "13-1.2")] = """ H2O OH R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "13-1.2")] = """Dimer from H2O - OH"""
TAGL["%s-%s-monoA-CP" % (dbse, "13-1.2")] = """Monomer A H2O - OH"""
TAGL["%s-%s-monoB-CP" % (dbse, "13-1.2")] = """Monomer B H2O - OH"""
TAGL["%s-%s" % (dbse, "13-1.5")] = """ H2O OH R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "13-1.5")] = """Dimer from H2O - OH"""
TAGL["%s-%s-monoA-CP" % (dbse, "13-1.5")] = """Monomer A H2O - OH"""
TAGL["%s-%s-monoB-CP" % (dbse, "13-1.5")] = """Monomer B H2O - OH"""
TAGL["%s-%s" % (dbse, "13-2.0")] = """ H2O OH R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "13-2.0")] = """Dimer from H2O - OH"""
TAGL["%s-%s-monoA-CP" % (dbse, "13-2.0")] = """Monomer A H2O - OH"""
TAGL["%s-%s-monoB-CP" % (dbse, "13-2.0")] = """Monomer B H2O - OH"""
TAGL["%s-%s" % (dbse, "14-0.9")] = """ H2O O2H R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "14-0.9")] = """Dimer from H2O - O2H"""
TAGL["%s-%s-monoA-CP" % (dbse, "14-0.9")] = """Monomer A H2O - O2H"""
TAGL["%s-%s-monoB-CP" % (dbse, "14-0.9")] = """Monomer B H2O - O2H"""
TAGL["%s-%s" % (dbse, "14-1.0")] = """ H2O O2H R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "14-1.0")] = """Dimer from H2O - O2H"""
TAGL["%s-%s-monoA-CP" % (dbse, "14-1.0")] = """Monomer A H2O - O2H"""
TAGL["%s-%s-monoB-CP" % (dbse, "14-1.0")] = """Monomer B H2O - O2H"""
TAGL["%s-%s" % (dbse, "14-1.2")] = """ H2O O2H R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "14-1.2")] = """Dimer from H2O - O2H"""
TAGL["%s-%s-monoA-CP" % (dbse, "14-1.2")] = """Monomer A H2O - O2H"""
TAGL["%s-%s-monoB-CP" % (dbse, "14-1.2")] = """Monomer B H2O - O2H"""
TAGL["%s-%s" % (dbse, "14-1.5")] = """ H2O O2H R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "14-1.5")] = """Dimer from H2O - O2H"""
TAGL["%s-%s-monoA-CP" % (dbse, "14-1.5")] = """Monomer A H2O - O2H"""
TAGL["%s-%s-monoB-CP" % (dbse, "14-1.5")] = """Monomer B H2O - O2H"""
TAGL["%s-%s" % (dbse, "14-2.0")] = """ H2O O2H R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "14-2.0")] = """Dimer from H2O - O2H"""
TAGL["%s-%s-monoA-CP" % (dbse, "14-2.0")] = """Monomer A H2O - O2H"""
TAGL["%s-%s-monoB-CP" % (dbse, "14-2.0")] = """Monomer B H2O - O2H"""
TAGL["%s-%s" % (dbse, "15-0.9")] = """ Li NH3 (gm) R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "15-0.9")] = """Dimer from Li NH3 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "15-0.9")] = """Monomer A Li NH3 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "15-0.9")] = """Monomer B Li NH3 (gm)"""
TAGL["%s-%s" % (dbse, "15-1.0")] = """ Li NH3 (gm) R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "15-1.0")] = """Dimer from Li - NH3 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "15-1.0")] = """Monomer A Li - NH3 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "15-1.0")] = """Monomer B Li - NH3 (gm"""
TAGL["%s-%s" % (dbse, "15-1.2")] = """ Li NH3 (gm) R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "15-1.2")] = """Dimer from Li - NH3 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "15-1.2")] = """Monomer A Li - NH3 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "15-1.2")] = """Monomer B Li - NH3 (gm)"""
TAGL["%s-%s" % (dbse, "15-1.5")] = """ Li NH3 (gm) R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "15-1.5")] = """Dimer from Li - NH3 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "15-1.5")] = """Monomer A Li - NH3 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "15-1.5")] = """Monomer B Li - NH3 (gm)"""
TAGL["%s-%s" % (dbse, "15-2.0")] = """ Li NH3 (gm) R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "15-2.0")] = """Dimer from Li NH3 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "15-2.0")] = """Monomer A Li NH3 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "15-2.0")] = """Monomer B Li NH3 (gm)"""
TAGL["%s-%s" % (dbse, "16-0.9")] = """ Li O2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "16-0.9")] = """Dimer from Li - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "16-0.9")] = """Monomer A Li - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "16-0.9")] = """Monomer B Li - O2"""
TAGL["%s-%s" % (dbse, "16-1.0")] = """ Li O2 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "16-1.0")] = """Dimer from Li - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "16-1.0")] = """Monomer A Li - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "16-1.0")] = """Monomer B Li - O2"""
TAGL["%s-%s" % (dbse, "16-1.2")] = """ Li O2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "16-1.2")] = """Dimer from Li - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "16-1.2")] = """Monomer A Li - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "16-1.2")] = """Monomer B Li - O2"""
TAGL["%s-%s" % (dbse, "16-1.5")] = """ Li O2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "16-1.5")] = """Dimer from Li - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "16-1.5")] = """Monomer A Li - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "16-1.5")] = """Monomer B Li - O2"""
TAGL["%s-%s" % (dbse, "16-2.0")] = """ Li O2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "16-2.0")] = """Dimer from Li - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "16-2.0")] = """Monomer A Li - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "16-2.0")] = """Monomer B Li - O2"""
TAGL["%s-%s" % (dbse, "17-0.9")] = """ CN H2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "17-0.9")] = """Dimer from CN - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "17-0.9")] = """Monomer A CN - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "17-0.9")] = """Monomer B CN - H2"""
TAGL["%s-%s" % (dbse, "17-1.0")] = """ CN H2 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "17-1.0")] = """Dimer from CN - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "17-1.0")] = """Monomer A CN - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "17-1.0")] = """Monomer B CN - H2"""
TAGL["%s-%s" % (dbse, "17-1.2")] = """ CN H2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "17-1.2")] = """Dimer from CN - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "17-1.2")] = """Monomer A CN - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "17-1.2")] = """Monomer B CN - H2"""
TAGL["%s-%s" % (dbse, "17-1.5")] = """ CN H2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "17-1.5")] = """Dimer from CN - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "17-1.5")] = """Monomer A CN - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "17-1.5")] = """Monomer B CN - H2"""
TAGL["%s-%s" % (dbse, "17-2.0")] = """ CN H2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "17-2.0")] = """Dimer from CN - H2"""
TAGL["%s-%s-monoA-CP" % (dbse, "17-2.0")] = """Monomer A CN - H2"""
TAGL["%s-%s-monoB-CP" % (dbse, "17-2.0")] = """Monomer B CN - H2"""
TAGL["%s-%s" % (dbse, "18-0.9")] = """ Li NH3 (lm) R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "18-0.9")] = """Dimer from Li NH3 (lm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "18-0.9")] = """Monomer A Li NH3 (lm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "18-0.9")] = """Monomer B Li NH3 (lm)"""
TAGL["%s-%s" % (dbse, "18-1.0")] = """ Li NH3 (lm) R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "18-1.0")] = """Dimer from Li NH3 (lm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "18-1.0")] = """Monomer A Li NH3 (lm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "18-1.0")] = """Monomer B Li NH3 (lm)"""
TAGL["%s-%s" % (dbse, "18-1.2")] = """ Li NH3 (lm) R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "18-1.2")] = """Dimer from Li NH3 (lm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "18-1.2")] = """Monomer A Li NH3 (lm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "18-1.2")] = """Monomer B Li NH3 (lm)"""
TAGL["%s-%s" % (dbse, "18-1.5")] = """ Li NH3 (lm) R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "18-1.5")] = """Dimer from Li NH3 (lm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "18-1.5")] = """Monomer A Li NH3 (lm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "18-1.5")] = """Monomer B Li NH3 (lm)"""
TAGL["%s-%s" % (dbse, "18-2.0")] = """ Li NH3 (lm) R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "18-2.0")] = """Dimer from Li NH3 (lm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "18-2.0")] = """Monomer A Li NH3 (lm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "18-2.0")] = """Monomer B Li NH3 (lm)"""
TAGL["%s-%s" % (dbse, "19-0.9")] = """ H2O O2 (gm) R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "19-0.9")] = """Dimer from H2O - O2 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "19-0.9")] = """Monomer A H2O - O2 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "19-0.9")] = """Monomer B H2O - O2 (gm)"""
TAGL["%s-%s" % (dbse, "19-1.0")] = """ H2O O2 (gm) R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "19-1.0")] = """Dimer from H2O - O2 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "19-1.0")] = """Monomer A H2O - O2 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "19-1.0")] = """Monomer B H2O - O2 (gm)"""
TAGL["%s-%s" % (dbse, "19-1.2")] = """ H2O O2 (gm) R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "19-1.2")] = """Dimer from H2O - O2 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "19-1.2")] = """Monomer A H2O - O2 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "19-1.2")] = """Monomer B H2O - O2 (gm)"""
TAGL["%s-%s" % (dbse, "19-1.5")] = """ H2O O2 (gm) R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "19-1.5")] = """Dimer from H2O - O2 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "19-1.5")] = """Monomer A H2O - O2 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "19-1.5")] = """Monomer B H2O - O2 (gm)"""
TAGL["%s-%s" % (dbse, "19-2.0")] = """ H2O O2 (gm) R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "19-2.0")] = """Dimer from H2O - O2 (gm)"""
TAGL["%s-%s-monoA-CP" % (dbse, "19-2.0")] = """Monomer A H2O - O2 (gm)"""
TAGL["%s-%s-monoB-CP" % (dbse, "19-2.0")] = """Monomer B H2O - O2 (gm)"""
TAGL["%s-%s" % (dbse, "20-0.9")] = """ Na Li R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "20-0.9")] = """Dimer from Na - Li"""
TAGL["%s-%s-monoA-CP" % (dbse, "20-0.9")] = """Monomer A Na - Li"""
TAGL["%s-%s-monoB-CP" % (dbse, "20-0.9")] = """Monomer B Na - Li"""
TAGL["%s-%s" % (dbse, "20-1.0")] = """ Na Li R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "20-1.0")] = """Dimer from Na - Li"""
TAGL["%s-%s-monoA-CP" % (dbse, "20-1.0")] = """Monomer A Na - Li"""
TAGL["%s-%s-monoB-CP" % (dbse, "20-1.0")] = """Monomer B Na - Li"""
TAGL["%s-%s" % (dbse, "20-1.2")] = """ Na Li R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "20-1.2")] = """Dimer from Na - Li"""
TAGL["%s-%s-monoA-CP" % (dbse, "20-1.2")] = """Monomer A Na - Li"""
TAGL["%s-%s-monoB-CP" % (dbse, "20-1.2")] = """Monomer B Na - Li"""
TAGL["%s-%s" % (dbse, "20-1.5")] = """ Na Li R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "20-1.5")] = """Dimer from Na - Li"""
TAGL["%s-%s-monoA-CP" % (dbse, "20-1.5")] = """Monomer A Na - Li"""
TAGL["%s-%s-monoB-CP" % (dbse, "20-1.5")] = """Monomer B Na - Li"""
TAGL["%s-%s" % (dbse, "20-2.0")] = """ Na Li """
TAGL["%s-%s-dimer" % (dbse, "20-2.0")] = """Dimer from Na - Li"""
TAGL["%s-%s-monoA-CP" % (dbse, "20-2.0")] = """Monomer A Na - Li"""
TAGL["%s-%s-monoB-CP" % (dbse, "20-2.0")] = """Monomer B Na - Li"""
TAGL["%s-%s" % (dbse, "21-0.9")] = """ CO2 O2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "21-0.9")] = """Dimer from CO2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "21-0.9")] = """Monomer A CO2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "21-0.9")] = """Monomer B CO2 - O2"""
TAGL["%s-%s" % (dbse, "21-1.0")] = """ CO2 O2 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "21-1.0")] = """Dimer from CO2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "21-1.0")] = """Monomer A CO2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "21-1.0")] = """Monomer B CO2 - O2"""
TAGL["%s-%s" % (dbse, "21-1.2")] = """ CO2 O2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "21-1.2")] = """Dimer from CO2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "21-1.2")] = """Monomer A CO2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "21-1.2")] = """Monomer B CO2 - O2"""
TAGL["%s-%s" % (dbse, "21-1.5")] = """ CO2 O2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "21-1.5")] = """Dimer from CO2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "21-1.5")] = """Monomer A CO2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "21-1.5")] = """Monomer B CO2 - O2"""
TAGL["%s-%s" % (dbse, "21-2.0")] = """ CO2 - O2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "21-2.0")] = """Dimer from CO2 - O2"""
TAGL["%s-%s-monoA-CP" % (dbse, "21-2.0")] = """Monomer A CO2 - O2"""
TAGL["%s-%s-monoB-CP" % (dbse, "21-2.0")] = """Monomer B CO2 - O2"""
TAGL["%s-%s" % (dbse, "22-0.9")] = """ C2H3 CO2 R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "22-0.9")] = """Dimer from C2H3 - CO2"""
TAGL["%s-%s-monoA-CP" % (dbse, "22-0.9")] = """Monomer A C2H3 - CO2"""
TAGL["%s-%s-monoB-CP" % (dbse, "22-0.9")] = """Monomer B C2H3 - CO2"""
TAGL["%s-%s" % (dbse, "22-1.0")] = """ C2H3 CO2 R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "22-1.0")] = """Dimer from C2H3 - CO2"""
TAGL["%s-%s-monoA-CP" % (dbse, "22-1.0")] = """Monomer A C2H3 - CO2"""
TAGL["%s-%s-monoB-CP" % (dbse, "22-1.0")] = """Monomer B C2H3 - CO2"""
TAGL["%s-%s" % (dbse, "22-1.2")] = """ C2H3 CO2 R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "22-1.2")] = """Dimer from C2H3 - CO2"""
TAGL["%s-%s-monoA-CP" % (dbse, "22-1.2")] = """Monomer A C2H3 - CO2"""
TAGL["%s-%s-monoB-CP" % (dbse, "22-1.2")] = """Monomer B C2H3 - CO2"""
TAGL["%s-%s" % (dbse, "22-1.5")] = """ C2H3 CO2 R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "22-1.5")] = """Dimer from C2H3 - CO2"""
TAGL["%s-%s-monoA-CP" % (dbse, "22-1.5")] = """Monomer A C2H3 - CO2"""
TAGL["%s-%s-monoB-CP" % (dbse, "22-1.5")] = """Monomer B C2H3 - CO2"""
TAGL["%s-%s" % (dbse, "22-2.0")] = """ C2H3 CO2 R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "22-2.0")] = """Dimer from C2H3 - CO2"""
TAGL["%s-%s-monoA-CP" % (dbse, "22-2.0")] = """Monomer A C2H3 - CO2"""
TAGL["%s-%s-monoB-CP" % (dbse, "22-2.0")] = """Monomer B C2H3 - CO2"""
TAGL["%s-%s" % (dbse, "23-0.9")] = """ He* He* R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "23-0.9")] = """Dimer from He* - He*"""
TAGL["%s-%s-monoA-CP" % (dbse, "23-0.9")] = """Monomer A He* - He*"""
TAGL["%s-%s-monoB-CP" % (dbse, "23-0.9")] = """Monomer B He* - He*"""
TAGL["%s-%s" % (dbse, "23-1.0")] = """ He* He* R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "23-1.0")] = """Dimer from He* - He*"""
TAGL["%s-%s-monoA-CP" % (dbse, "23-1.0")] = """Monomer A He* - He*"""
TAGL["%s-%s-monoB-CP" % (dbse, "23-1.0")] = """Monomer B He* - He*"""
TAGL["%s-%s" % (dbse, "23-1.2")] = """ He* He* R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "23-1.2")] = """Dimer from He* - He*"""
TAGL["%s-%s-monoA-CP" % (dbse, "23-1.2")] = """Monomer A He* - He*"""
TAGL["%s-%s-monoB-CP" % (dbse, "23-1.2")] = """Monomer B He* - He*"""
TAGL["%s-%s" % (dbse, "23-1.5")] = """ He* He* R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "23-1.5")] = """Dimer from He* - He*"""
TAGL["%s-%s-monoA-CP" % (dbse, "23-1.5")] = """Monomer A He* - He*"""
TAGL["%s-%s-monoB-CP" % (dbse, "23-1.5")] = """Monomer B He* - He*"""
TAGL["%s-%s" % (dbse, "23-2.0")] = """ He* He* R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "23-2.0")] = """Dimer from He* - He*"""
TAGL["%s-%s-monoA-CP" % (dbse, "23-2.0")] = """Monomer A He* - He*"""
TAGL["%s-%s-monoB-CP" % (dbse, "23-2.0")] = """Monomer B He* - He*"""
TAGL["%s-%s" % (dbse, "24-0.9")] = """ HF CO+ R=0.9"""
TAGL["%s-%s-dimer" % (dbse, "24-0.9")] = """Dimer from HF - CO+"""
TAGL["%s-%s-monoA-CP" % (dbse, "24-0.9")] = """Monomer A HF - CO+"""
TAGL["%s-%s-monoB-CP" % (dbse, "24-0.9")] = """Monomer B HF - CO+"""
TAGL["%s-%s" % (dbse, "24-1.0")] = """ HF CO+ R=1.0"""
TAGL["%s-%s-dimer" % (dbse, "24-1.0")] = """Dimer from HF - CO+"""
TAGL["%s-%s-monoA-CP" % (dbse, "24-1.0")] = """Monomer A HF - CO+"""
TAGL["%s-%s-monoB-CP" % (dbse, "24-1.0")] = """Monomer B HF - CO+"""
TAGL["%s-%s" % (dbse, "24-1.2")] = """ HF CO+ R=1.2"""
TAGL["%s-%s-dimer" % (dbse, "24-1.2")] = """Dimer from HF - CO+"""
TAGL["%s-%s-monoA-CP" % (dbse, "24-1.2")] = """Monomer A HF - CO+"""
TAGL["%s-%s-monoB-CP" % (dbse, "24-1.2")] = """Monomer B HF - CO+"""
TAGL["%s-%s" % (dbse, "24-1.5")] = """ HF CO+ R=1.5"""
TAGL["%s-%s-dimer" % (dbse, "24-1.5")] = """Dimer from HF - CO+"""
TAGL["%s-%s-monoA-CP" % (dbse, "24-1.5")] = """Monomer A HF - CO+"""
TAGL["%s-%s-monoB-CP" % (dbse, "24-1.5")] = """Monomer B HF - CO+"""
TAGL["%s-%s" % (dbse, "24-2.0")] = """ HF CO+ R=2.0"""
TAGL["%s-%s-dimer" % (dbse, "24-2.0")] = """Dimer from HF - CO+"""
TAGL["%s-%s-monoA-CP" % (dbse, "24-2.0")] = """Monomer A HF - CO+"""
TAGL["%s-%s-monoB-CP" % (dbse, "24-2.0")] = """Monomer B HF - CO+"""

# <<< Geometry Specification Strins >>>
GEOS = {}

GEOS["%s-%s-dimer" % (dbse, "1-0.9")] = qcdb.Molecule(
    """
0   2
C        -0.664078525     0.000000000     1.259898914
N         0.292558536     0.000000000     1.928630081
--
0   1
He        0.149064407     0.000000000    -1.619916319
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "1-1.0")] = qcdb.Molecule(
    """
0   2
C        -0.680641237     0.000000000     1.439889616
N         0.275995824     0.000000000     2.108620783
--
0   1
He        0.165627119     0.000000000    -1.799907021
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "1-1.2")] = qcdb.Molecule(
    """
0   2
C        -0.713766661     0.000000000     1.799871020
N         0.242870401     0.000000000     2.468602187
--
0   1
He        0.198752542     0.000000000    -2.159888425
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "1-1.5")] = qcdb.Molecule(
    """
0   2
C        -0.763454796     0.000000000     2.339843127
N         0.193182265     0.000000000     3.008574293
--
0   1
He        0.248440678     0.000000000    -2.699860531
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "1-2.0")] = qcdb.Molecule(
    """
0   2
C        -0.846268356     0.000000000     3.239796637
N         0.110368706     0.000000000     3.908527804
--
0   1
He        0.331254237     0.000000000    -3.599814042
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "2-0.9")] = qcdb.Molecule(
    """
0   3
N         0.000000000    -1.324613470    -0.800832434
H         0.000000000    -1.324613470     0.235137867
--
0   1
He        0.000000000     1.324613470     0.731287250
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "2-1.0")] = qcdb.Molecule(
    """
0   3
N         0.000000000    -1.471792745    -0.882086573
H         0.000000000    -1.471792745     0.153883728
--
0   1
He        0.000000000     1.471792745     0.812541389
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "2-1.2")] = qcdb.Molecule(
    """
0   3
N         0.000000000    -1.766151294    -1.044594851
H         0.000000000    -1.766151294    -0.008624550
--
0   1
He        0.000000000     1.766151294     0.975049667
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "2-1.5")] = qcdb.Molecule(
    """
0   3
N         0.000000000    -2.207689117    -1.288357268
H         0.000000000    -2.207689117    -0.252386967
--
0   1
He        0.000000000     2.207689117     1.218812083
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "2-2.0")] = qcdb.Molecule(
    """
0   3
N         0.000000000    -2.943585490    -1.694627962
H         0.000000000    -2.943585490    -0.658657661
--
0   1
He        0.000000000     2.943585490     1.625082778
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "3-0.9")] = qcdb.Molecule(
    """
0   2
H         0.905020870     1.257212446    -1.980000000
H         0.905020870    -1.206707554    -1.980000000
H        -0.942899130    -1.206707554    -1.980000000
C        -0.018939130     0.692432446    -1.980000000
C        -0.018939130    -0.641927554    -1.980000000
--
0   1
H        -0.939455652     1.252621093     1.980000000
H         0.908464348     1.252621093     1.980000000
H         0.908464348    -1.211298907     1.980000000
H        -0.939455652    -1.211298907     1.980000000
C        -0.015495652     0.687841093     1.980000000
C        -0.015495652    -0.646518907     1.980000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "3-1.0")] = qcdb.Molecule(
    """
0   2
H         0.906742609     1.254916769    -2.200000000
H         0.906742609    -1.209003231    -2.200000000
H        -0.941177391    -1.209003231    -2.200000000
C        -0.017217391     0.690136769    -2.200000000
C        -0.017217391    -0.644223231    -2.200000000
--
0   1
H        -0.941177391     1.254916769     2.200000000
H         0.906742609     1.254916769     2.200000000
H         0.906742609    -1.209003231     2.200000000
H        -0.941177391    -1.209003231     2.200000000
C        -0.017217391     0.690136769     2.200000000
C        -0.017217391    -0.644223231     2.200000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "3-1.2")] = qcdb.Molecule(
    """
0   2
H         0.910186087     1.250325416    -2.640000000
H         0.910186087    -1.213594584    -2.640000000
H        -0.937733913    -1.213594584    -2.640000000
C        -0.013773913     0.685545416    -2.640000000
C        -0.013773913    -0.648814584    -2.640000000
--
0   1
H        -0.944620869     1.259508123     2.640000000
H         0.903299131     1.259508123     2.640000000
H         0.903299131    -1.204411877     2.640000000
H        -0.944620869    -1.204411877     2.640000000
C        -0.020660869     0.694728123     2.640000000
C        -0.020660869    -0.639631877     2.640000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "3-1.5")] = qcdb.Molecule(
    """
0   2
H         0.915351305     1.243438385    -3.300000000
H         0.915351305    -1.220481615    -3.300000000
H        -0.932568695    -1.220481615    -3.300000000
C        -0.008608695     0.678658385    -3.300000000
C        -0.008608695    -0.655701615    -3.300000000
--
0   1
H        -0.949786086     1.266395154     3.300000000
H         0.898133914     1.266395154     3.300000000
H         0.898133914    -1.197524846     3.300000000
H        -0.949786086    -1.197524846     3.300000000
C        -0.025826086     0.701615154     3.300000000
C        -0.025826086    -0.632744846     3.300000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "3-2.0")] = qcdb.Molecule(
    """
0   2
H         0.923960000     1.231960000    -4.400000000
H         0.923960000    -1.231960000    -4.400000000
H        -0.923960000    -1.231960000    -4.400000000
C         0.000000000     0.667180000    -4.400000000
C         0.000000000    -0.667180000    -4.400000000
--
0   1
H        -0.958394782     1.277873539     4.400000000
H         0.889525218     1.277873539     4.400000000
H         0.889525218    -1.186046461     4.400000000
H        -0.958394782    -1.186046461     4.400000000
C        -0.034434782     0.713093539     4.400000000
C        -0.034434782    -0.621266461     4.400000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "4-0.9")] = qcdb.Molecule(
    """
0   3
O        -0.330467500     0.000000000    -1.475595000
O         0.871232500     0.000000000    -1.475595000
--
0   1
H        -0.270382500    -0.371400000     1.475595000
H        -0.270382500     0.371400000     1.475595000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "4-1.0")] = qcdb.Molecule(
    """
0   3
O        -0.300425000     0.000000000    -1.639550000
O         0.901275000     0.000000000    -1.639550000
--
0   1
H        -0.300425000    -0.371400000     1.639550000
H        -0.300425000     0.371400000     1.639550000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "4-1.2")] = qcdb.Molecule(
    """
0   3
O        -0.240340000     0.000000000    -1.967460000
O         0.961360000     0.000000000    -1.967460000
--
0   1
H        -0.360510000    -0.371400000     1.967460000
H        -0.360510000     0.371400000     1.967460000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "4-1.5")] = qcdb.Molecule(
    """
0   3
O        -0.150212500     0.000000000    -2.459325000
O         1.051487500     0.000000000    -2.459325000
--
0   1
H        -0.450637500    -0.371400000     2.459325000
H        -0.450637500     0.371400000     2.459325000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "4-2.0")] = qcdb.Molecule(
    """
0   3
O         0.000000000     0.000000000    -3.279100000
O         1.201700000     0.000000000    -3.279100000
--
0   1
H        -0.600850000    -0.371400000     3.279100000
H        -0.600850000     0.371400000     3.279100000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "5-0.9")] = qcdb.Molecule(
    """
0   3
N        -0.056490403     0.000000000     1.724989690
H         0.854426530     0.000000000     1.228991525
--
0   1
Ar       -0.004659888     0.000000000    -1.691693095
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "5-1.0")] = qcdb.Molecule(
    """
0   3
N        -0.055972638     0.000000000     1.912955590
H         0.854944296     0.000000000     1.416957424
--
0   1
Ar       -0.005177654     0.000000000    -1.879658994
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "5-1.2")] = qcdb.Molecule(
    """
0   3
N        -0.054937107     0.000000000     2.288887388
H         0.855979826     0.000000000     1.792889223
--
0   1
Ar       -0.006213184     0.000000000    -2.255590793
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "5-1.5")] = qcdb.Molecule(
    """
0   3
N        -0.053383811     0.000000000     2.852785087
H         0.857533122     0.000000000     2.356786921
--
0   1
Ar       -0.007766480     0.000000000    -2.819488491
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "5-2.0")] = qcdb.Molecule(
    """
0   3
N        -0.050794984     0.000000000     3.792614584
H         0.860121949     0.000000000     3.296616418
--
0   1
Ar       -0.010355307     0.000000000    -3.759317989
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "6-0.9")] = qcdb.Molecule(
    """
0   2
C        -0.427112733     0.000000000     2.134178904
N         0.427713476     0.000000000     1.339428634
--
0   1
Ar       -0.033090602     0.000000000    -1.706317987
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "6-1.0")] = qcdb.Molecule(
    """
0   2
C        -0.423436000     0.000000000     2.323769791
N         0.431390210     0.000000000     1.529019521
--
0   1
Ar       -0.036767336     0.000000000    -1.895908875
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "6-1.2")] = qcdb.Molecule(
    """
0   2
C        -0.416082533     0.000000000     2.702951566
N         0.438743677     0.000000000     1.908201296
--
0   1
Ar       -0.044120803     0.000000000    -2.275090650
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "6-1.5")] = qcdb.Molecule(
    """
0   2
C        -0.405052332     0.000000000     3.271724229
N         0.449773878     0.000000000     2.476973959
--
0   1
Ar       -0.055151004     0.000000000    -2.843863312
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "6-2.0")] = qcdb.Molecule(
    """
0   2
C        -0.386668664     0.000000000     4.219678666
N         0.468157545     0.000000000     3.424928396
--
0   1
Ar       -0.073534672     0.000000000    -3.791817750
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "7-0.9")] = qcdb.Molecule(
    """
0   3
O        -0.600850000     0.000000000    -1.548000000
O         0.600850000     0.000000000    -1.548000000
--
0   1
N         0.000000000    -0.548400000     1.548000000
N         0.000000000     0.548400000     1.548000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "7-1.0")] = qcdb.Molecule(
    """
0   3
O        -0.600850000     0.000000000    -1.720000000
O         0.600850000     0.000000000    -1.720000000
--
0   1
N         0.000000000    -0.548400000     1.720000000
N         0.000000000     0.548400000     1.720000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "7-1.2")] = qcdb.Molecule(
    """
0   3
O        -0.600850000     0.000000000    -2.064000000
O         0.600850000     0.000000000    -2.064000000
--
0   1
N         0.000000000    -0.548400000     2.064000000
N         0.000000000     0.548400000     2.064000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "7-1.5")] = qcdb.Molecule(
    """
0   3
O        -0.600850000     0.000000000    -2.580000000
O         0.600850000     0.000000000    -2.580000000
--
0   1
N         0.000000000    -0.548400000     2.580000000
N         0.000000000     0.548400000     2.580000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "7-2.0")] = qcdb.Molecule(
    """
0   3
O        -0.600850000     0.000000000    -3.440000000
O         0.600850000     0.000000000    -3.440000000
--
0   1
N         0.000000000    -0.548400000     3.440000000
N         0.000000000     0.548400000     3.440000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "8-0.9")] = qcdb.Molecule(
    """
0   1
O        -1.602354754    -0.131587291     0.000000000
H        -0.911985371     0.483604683     0.000000000
H        -0.875976531    -0.823928533     0.000000000
--
0   3
O         1.447979736     0.699599572     0.000000000
O         1.598198061    -0.427792115     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "8-1.0")] = qcdb.Molecule(
    """
0   1
O        -1.771586854    -0.146687705     0.000000000
H        -1.081217471     0.468504269     0.000000000
H        -1.045208631    -0.839028947     0.000000000
--
0   3
O         1.617211836     0.714699987     0.000000000
O         1.767430161    -0.412691700     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "8-1.2")] = qcdb.Molecule(
    """
0   1
O        -2.110051054    -0.176888534     0.000000000
H        -1.419681671     0.438303440     0.000000000
H        -1.383672831    -0.869229776     0.000000000
--
0   3
O         1.955676036     0.744900815     0.000000000
O         2.105894361    -0.382490872     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "8-1.5")] = qcdb.Molecule(
    """
0   1
O        -2.617747353    -0.222189777     0.000000000
H        -1.927377970     0.393002197     0.000000000
H        -1.891369130    -0.914531019     0.000000000
--
0   3
O         2.463372335     0.790202058     0.000000000
O         2.613590660    -0.337189629     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "8-2.0")] = qcdb.Molecule(
    """
0   1
O        -3.463907853    -0.297691848     0.000000000
H        -2.773538470     0.317500126     0.000000000
H        -2.737529630    -0.990033090     0.000000000
--
0   3
O         3.309532834     0.865704130     0.000000000
O         3.459751159    -0.261687557     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "9-0.9")] = qcdb.Molecule(
    """
0   3
O         0.601000000    -1.485000000     0.000000000
O        -0.601000000    -1.485000000     0.000000000
--
0   3
O         0.000000000     1.485000000     0.601000000
O         0.000000000     1.485000000    -0.601000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "9-1.0")] = qcdb.Molecule(
    """
0   3
O         0.601000000    -1.650000000     0.000000000
O        -0.601000000    -1.650000000     0.000000000
--
0   3
O         0.000000000     1.650000000     0.601000000
O         0.000000000     1.650000000    -0.601000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "9-1.2")] = qcdb.Molecule(
    """
0   3
O         0.601000000    -1.980000000     0.000000000
O        -0.601000000    -1.980000000     0.000000000
--
0   3
O         0.000000000     1.980000000     0.601000000
O         0.000000000     1.980000000    -0.601000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "9-1.5")] = qcdb.Molecule(
    """
0   3
O         0.601000000    -2.475000000     0.000000000
O        -0.601000000    -2.475000000     0.000000000
--
0   3
O         0.000000000     2.475000000     0.601000000
O         0.000000000     2.475000000    -0.601000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "9-2.0")] = qcdb.Molecule(
    """
0   3
O         0.601000000    -3.300000000     0.000000000
O        -0.601000000    -3.300000000     0.000000000
--
0   3
O         0.000000000     3.300000000     0.601000000
O         0.000000000     3.300000000    -0.601000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "10-0.9")] = qcdb.Molecule(
    """
0   3
N        -1.644614308     0.000000000     0.000000000
H        -0.607614308     0.000000000     0.000000000
--
0   3
N         1.505385692     0.000000000     0.000000000
H         2.542385692     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "10-1.0")] = qcdb.Molecule(
    """
0   3
N        -1.819614308     0.000000000     0.000000000
H        -0.782614308     0.000000000     0.000000000
--
0   3
N         1.680385692     0.000000000     0.000000000
H         2.717385692     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "10-1.2")] = qcdb.Molecule(
    """
0   3
N        -2.169614308     0.000000000     0.000000000
H        -1.132614308     0.000000000     0.000000000
--
0   3
N         2.030385692     0.000000000     0.000000000
H         3.067385692     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "10-1.5")] = qcdb.Molecule(
    """
0   3
N        -2.694614308     0.000000000     0.000000000
H        -1.657614308     0.000000000     0.000000000
--
0   3
N         2.555385692     0.000000000     0.000000000
H         3.592385692     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "10-2.0")] = qcdb.Molecule(
    """
0   3
N        -3.569614308     0.000000000     0.000000000
H        -2.532614308     0.000000000     0.000000000
--
0   3
N         3.430385692     0.000000000     0.000000000
H         4.467385692     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "11-0.9")] = qcdb.Molecule(
    """
0   1
C        -0.101334404     1.309903834     0.000000000
H         0.475160596     1.401144834     0.932814000
H         0.475160596     1.401144834    -0.932814000
O        -1.294782404     1.126008834     0.000000000
--
0   2
N         0.727791868    -1.144301441     0.000000000
H        -0.255227132    -1.433449441     0.000000000
H         1.246142868    -2.027340441     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "11-1.0")] = qcdb.Molecule(
    """
0   1
C        -0.178952268     1.445241696     0.000000000
H         0.397542732     1.536482696     0.932814000
H         0.397542732     1.536482696    -0.932814000
O        -1.372400268     1.261346696     0.000000000
--
0   2
N         0.805409732    -1.279639304     0.000000000
H        -0.177609268    -1.568787304     0.000000000
H         1.323760732    -2.162678304     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "11-1.2")] = qcdb.Molecule(
    """
0   1
C        -0.334187997     1.715917421     0.000000000
H         0.242307003     1.807158421     0.932814000
H         0.242307003     1.807158421    -0.932814000
O        -1.527635997     1.532022421     0.000000000
--
0   2
N         0.960645461    -1.550315029     0.000000000
H        -0.022373539    -1.839463029     0.000000000
H         1.478996461    -2.433354029     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "11-1.5")] = qcdb.Molecule(
    """
0   1
C        -0.567041589     2.121931008     0.000000000
H         0.009453411     2.213172008     0.932814000
H         0.009453411     2.213172008    -0.932814000
O        -1.760489589     1.938036008     0.000000000
--
0   2
N         1.193499054    -1.956328616     0.000000000
H         0.210480054    -2.245476616     0.000000000
H         1.711850054    -2.839367616     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "11-2.0")] = qcdb.Molecule(
    """
0   1
C        -0.955130911     2.798620321     0.000000000
H        -0.378635911     2.889861321     0.932814000
H        -0.378635911     2.889861321    -0.932814000
O        -2.148578911     2.614725321     0.000000000
--
0   2
N         1.581588375    -2.633017928     0.000000000
H         0.598569375    -2.922165928     0.000000000
H         2.099939375    -3.516056928     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "12-0.9")] = qcdb.Molecule(
    """
0   2
Na        0.000008510     0.000000000    -1.099330219
--
0   1
O        -0.000060510     0.000000000     1.036566937
H         0.000404197     0.758137925     1.597462474
H         0.000404197    -0.758137925     1.597462474
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "12-1.0")] = qcdb.Molecule(
    """
0   2
Na        0.000009456     0.000000000    -1.221478021
--
0   1
O        -0.000061456     0.000000000     1.158714739
H         0.000403251     0.758137925     1.719610276
H         0.000403251    -0.758137925     1.719610276
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "12-1.2")] = qcdb.Molecule(
    """
0   2
Na        0.000011347     0.000000000    -1.465773625
--
0   1
O        -0.000063347     0.000000000     1.403010344
H         0.000401360     0.758137925     1.963905880
H         0.000401360    -0.758137925     1.963905880
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "12-1.5")] = qcdb.Molecule(
    """
0   2
Na        0.000014184     0.000000000    -1.832217032
--
0   1
O        -0.000066184     0.000000000     1.769453750
H         0.000398523     0.758137925     2.330349286
H         0.000398523    -0.758137925     2.330349286
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "12-2.0")] = qcdb.Molecule(
    """
0   2
Na        0.000018912     0.000000000    -2.442956042
--
0   1
O        -0.000070912     0.000000000     2.380192760
H         0.000393795     0.758137925     2.941088297
H         0.000393795    -0.758137925     2.941088297
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "13-0.9")] = qcdb.Molecule(
    """
0   1
O         0.000000000     0.040866260     1.250060902
H         0.758711083    -0.281411037     1.745206735
H        -0.758711083    -0.281411037     1.745206735
--
0   2
O         0.000000000    -0.005751238    -1.363141746
H         0.000000000     0.010232468    -0.389972999
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "13-1.0")] = qcdb.Molecule(
    """
0   1
O         0.000000000     0.041400034     1.395112780
H         0.758711083    -0.280877264     1.890258613
H        -0.758711083    -0.280877264     1.890258613
--
0   2
O         0.000000000    -0.006285012    -1.508193624
H         0.000000000     0.009698694    -0.535024877
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "13-1.2")] = qcdb.Molecule(
    """
0   1
O         0.000000000     0.042467581     1.685216535
H         0.758711083    -0.279809716     2.180362369
H        -0.758711083    -0.279809716     2.180362369
--
0   2
O         0.000000000    -0.007352559    -1.798297380
H         0.000000000     0.008631147    -0.825128632
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "13-1.5")] = qcdb.Molecule(
    """
0   1
O         0.000000000     0.044068902     2.120372169
H         0.758711083    -0.278208395     2.615518002
H        -0.758711083    -0.278208395     2.615518002
--
0   2
O         0.000000000    -0.008953881    -2.233453013
H         0.000000000     0.007029825    -1.260284266
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "13-2.0")] = qcdb.Molecule(
    """
0   1
O         0.000000000     0.046737771     2.845631558
H         0.758711083    -0.275539526     3.340777391
H        -0.758711083    -0.275539526     3.340777391
--
0   2
O         0.000000000    -0.011622750    -2.958712403
H         0.000000000     0.004360956    -1.985543655
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "14-0.9")] = qcdb.Molecule(
    """
0   1
O         0.009168889    -0.062647918    -1.355472454
H         0.035272725    -0.935983853    -1.711786553
H        -0.174773578     0.520586925    -2.074053757
--
0   2
H         0.007562952     0.395572349     0.203044832
O         0.006757459     0.633252986     1.127049552
O        -0.007931101    -0.495446570     1.780564418
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "14-1.0")] = qcdb.Molecule(
    """
0   1
O         0.009206439    -0.071412233    -1.512762672
H         0.035310275    -0.944748168    -1.869076771
H        -0.174736028     0.511822610    -2.231343975
--
0   2
H         0.007525402     0.404336664     0.360335050
O         0.006719909     0.642017300     1.284339770
O        -0.007968651    -0.486682255     1.937854636
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "14-1.2")] = qcdb.Molecule(
    """
0   1
O         0.009281538    -0.088940863    -1.827343108
H         0.035385374    -0.962276797    -2.183657207
H        -0.174660929     0.494293980    -2.545924411
--
0   2
H         0.007450302     0.421865294     0.674915486
O         0.006644810     0.659545930     1.598920206
O        -0.008043751    -0.469153625     2.252435072
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "14-1.5")] = qcdb.Molecule(
    """
0   1
O         0.009394188    -0.115233807    -2.299213762
H         0.035498024    -0.988569742    -2.655527861
H        -0.174548279     0.468001035    -3.017795065
--
0   2
H         0.007337653     0.448158238     1.146786139
O         0.006532160     0.685838875     2.070790860
O        -0.008156400    -0.442860681     2.724305726
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "14-2.0")] = qcdb.Molecule(
    """
0   1
O         0.009581937    -0.159055382    -3.085664852
H         0.035685773    -1.032391316    -3.441978951
H        -0.174360530     0.424179461    -3.804246155
--
0   2
H         0.007149904     0.491979813     1.933237229
O         0.006344411     0.729660449     2.857241950
O        -0.008344149    -0.399039106     3.510756816
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "15-0.9")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000     0.863512817
H         0.937314431     0.000000000     1.245069906
H        -0.468657216    -0.811738109     1.245069906
H        -0.468657216     0.811738109     1.245069906
--
0   2
Li        0.000000000     0.000000000    -0.931259424
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "15-1.0")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000     0.966986086
H         0.937314431     0.000000000     1.348543175
H        -0.468657216    -0.811738109     1.348543175
H        -0.468657216     0.811738109     1.348543175
--
0   2
Li        0.000000000     0.000000000    -1.034732694
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "15-1.2")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000     1.173932625
H         0.937314431     0.000000000     1.555489714
H        -0.468657216    -0.811738109     1.555489714
H        -0.468657216     0.811738109     1.555489714
--
0   2
Li        0.000000000     0.000000000    -1.241679233
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "15-1.5")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000     1.484352433
H         0.937314431     0.000000000     1.865909522
H        -0.468657216    -0.811738109     1.865909522
H        -0.468657216     0.811738109     1.865909522
--
0   2
Li        0.000000000     0.000000000    -1.552099041
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "15-2.0")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000     2.001718780
H         0.937314431     0.000000000     2.383275869
H        -0.468657216    -0.811738109     2.383275869
H        -0.468657216     0.811738109     2.383275869
--
0   2
Li        0.000000000     0.000000000    -2.069465388
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "16-0.9")] = qcdb.Molecule(
    """
0   3
O         0.000000000     0.603367899    -2.143167858
O         0.000000000    -0.603367899    -2.143167858
--
0   2
Li        0.000000000     0.000000000     2.143167858
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "16-1.0")] = qcdb.Molecule(
    """
0   3
O         0.000000000     0.603367899    -2.381297620
O         0.000000000    -0.603367899    -2.381297620
--
0   2
Li        0.000000000     0.000000000     2.381297620
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "16-1.2")] = qcdb.Molecule(
    """
0   3
O         0.000000000     0.603367899    -2.857557145
O         0.000000000    -0.603367899    -2.857557145
--
0   2
Li        0.000000000     0.000000000     2.857557145
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "16-1.5")] = qcdb.Molecule(
    """
0   3
O         0.000000000     0.603367899    -3.571946431
O         0.000000000    -0.603367899    -3.571946431
--
0   2
Li        0.000000000     0.000000000     3.571946431
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "16-2.0")] = qcdb.Molecule(
    """
0   3
O         0.000000000     0.603367899    -4.762595241
O         0.000000000    -0.603367899    -4.762595241
--
0   2
Li        0.000000000     0.000000000     4.762595241
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "17-0.9")] = qcdb.Molecule(
    """
0   2
C        -1.595250000    -0.609996639     0.000000000
N        -1.595250000     0.560603361     0.000000000
--
0   1
H         1.595250000    -0.020206341     0.371400000
H         1.595250000    -0.020206341    -0.371400000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "17-1.0")] = qcdb.Molecule(
    """
0   2
C        -1.772500000    -0.607751490     0.000000000
N        -1.772500000     0.562848510     0.000000000
--
0   1
H         1.772500000    -0.022451490     0.371400000
H         1.772500000    -0.022451490    -0.371400000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "17-1.2")] = qcdb.Molecule(
    """
0   2
C        -2.127000000    -0.603261192     0.000000000
N        -2.127000000     0.567338808     0.000000000
--
0   1
H         2.127000000    -0.026941788     0.371400000
H         2.127000000    -0.026941788    -0.371400000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "17-1.5")] = qcdb.Molecule(
    """
0   2
C        -2.658750000    -0.596525745     0.000000000
N        -2.658750000     0.574074255     0.000000000
--
0   1
H         2.658750000    -0.033677235     0.371400000
H         2.658750000    -0.033677235    -0.371400000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "17-2.0")] = qcdb.Molecule(
    """
0   2
C        -3.545000000    -0.585300000     0.000000000
N        -3.545000000     0.585300000     0.000000000
--
0   1
H         3.545000000    -0.044902980     0.371400000
H         3.545000000    -0.044902980    -0.371400000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "18-0.9")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000    -1.994044328
H         0.937314431     0.000000000    -1.612487239
H        -0.468657216    -0.811738109    -1.612487239
H        -0.468657216     0.811738109    -1.612487239
--
0   2
Li        0.000000000     0.000000000     1.926297720
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "18-1.0")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000    -2.208077408
H         0.937314431     0.000000000    -1.826520319
H        -0.468657216    -0.811738109    -1.826520319
H        -0.468657216     0.811738109    -1.826520319
--
0   2
Li        0.000000000     0.000000000     2.140330800
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "18-1.2")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000    -2.636143568
H         0.937314431     0.000000000    -2.254586479
H        -0.468657216    -0.811738109    -2.254586479
H        -0.468657216     0.811738109    -2.254586479
--
0   2
Li        0.000000000     0.000000000     2.568396960
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "18-1.5")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000    -3.278242808
H         0.937314431     0.000000000    -2.896685719
H        -0.468657216    -0.811738109    -2.896685719
H        -0.468657216     0.811738109    -2.896685719
--
0   2
Li        0.000000000     0.000000000     3.210496200
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "18-2.0")] = qcdb.Molecule(
    """
0   1
N         0.000000000     0.000000000    -4.348408208
H         0.937314431     0.000000000    -3.966851119
H        -0.468657216    -0.811738109    -3.966851119
H        -0.468657216     0.811738109    -3.966851119
--
0   2
Li        0.000000000     0.000000000     4.280661600
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "19-0.9")] = qcdb.Molecule(
    """
0   1
H        -2.342136430     0.069282299     0.000000000
O        -1.395456186    -0.083638660     0.000000000
H        -1.010361619     0.794850735     0.000000000
--
0   3
O         1.303480449     0.616939606     0.000000000
O         1.550272430    -0.565075397     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "19-1.0")] = qcdb.Molecule(
    """
0   1
H        -2.500678256     0.066400954     0.000000000
O        -1.553998012    -0.086520005     0.000000000
H        -1.168903446     0.791969390     0.000000000
--
0   3
O         1.462022276     0.619820951     0.000000000
O         1.708814256    -0.562194052     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "19-1.2")] = qcdb.Molecule(
    """
0   1
H        -2.817761909     0.060638264     0.000000000
O        -1.871081665    -0.092282694     0.000000000
H        -1.485987099     0.786206700     0.000000000
--
0   3
O         1.779105929     0.625583641     0.000000000
O         2.025897910    -0.556431362     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "19-1.5")] = qcdb.Molecule(
    """
0   1
H        -3.293387389     0.051994230     0.000000000
O        -2.346707145    -0.100926729     0.000000000
H        -1.961612579     0.777562666     0.000000000
--
0   3
O         2.254731409     0.634227675     0.000000000
O         2.501523389    -0.547787328     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "19-2.0")] = qcdb.Molecule(
    """
0   1
H        -4.086096522     0.037587505     0.000000000
O        -3.139416278    -0.115333454     0.000000000
H        -2.754321712     0.763155941     0.000000000
--
0   3
O         3.047440541     0.648634400     0.000000000
O         3.294232522    -0.533380603     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "20-0.9")] = qcdb.Molecule(
    """
0   2
Na       -2.124000000     0.000000000     0.000000000
--
0   2
Li        2.124000000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "20-1.0")] = qcdb.Molecule(
    """
0   2
Na       -2.360000000     0.000000000     0.000000000
--
0   2
Li        2.360000000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "20-1.2")] = qcdb.Molecule(
    """
0   2
Na       -2.832000000     0.000000000     0.000000000
--
0   2
Li        2.832000000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "20-1.5")] = qcdb.Molecule(
    """
0   2
Na       -3.540000000     0.000000000     0.000000000
--
0   2
Li        3.540000000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "20-2.0")] = qcdb.Molecule(
    """
0   2
Na       -4.720000000     0.000000000     0.000000000
--
0   2
Li        4.720000000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "21-0.9")] = qcdb.Molecule(
    """
0   1
C        -1.523106993     0.306968024     0.000000000
O        -1.523106993     1.466968024     0.000000000
O        -1.523106993    -0.853031976     0.000000000
--
0   3
O         1.260813349     0.116735356     0.000000000
O         1.785400638    -0.730671405     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "21-1.0")] = qcdb.Molecule(
    """
0   1
C        -1.692341104     0.341075582     0.000000000
O        -1.692341104     1.501075582     0.000000000
O        -1.692341104    -0.818924418     0.000000000
--
0   3
O         1.430047459     0.082627798     0.000000000
O         1.954634748    -0.764778963     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "21-1.2")] = qcdb.Molecule(
    """
0   1
C        -2.030809325     0.409290699     0.000000000
O        -2.030809325     1.569290699     0.000000000
O        -2.030809325    -0.750709301     0.000000000
--
0   3
O         1.768515680     0.014412682     0.000000000
O         2.293102969    -0.832994079     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "21-1.5")] = qcdb.Molecule(
    """
0   1
C        -2.538511656     0.511613373     0.000000000
O        -2.538511656     1.671613373     0.000000000
O        -2.538511656    -0.648386627     0.000000000
--
0   3
O         2.276218011    -0.087909993     0.000000000
O         2.800805300    -0.935316754     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "21-2.0")] = qcdb.Molecule(
    """
0   1
C        -3.384682208     0.682151165     0.000000000
O        -3.384682208     1.842151164     0.000000000
O        -3.384682208    -0.477848835     0.000000000
--
0   3
O         3.122388563    -0.258447784     0.000000000
O         3.646975852    -1.105854545     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)


GEOS["%s-%s-dimer" % (dbse, "22-0.9")] = qcdb.Molecule(
    """
0   2
C        -1.221104626    -0.694508536    -0.323156022
C        -1.684033576     0.465731104     0.078533898
H        -1.480567976    -1.736096366    -0.211354942
H        -2.573907146     0.530613704     0.705730008
H        -1.204305196     1.400456624    -0.192333322
--
0   1
C         1.480747026     0.092766498     0.096716376
O         1.276359406     1.181647978    -0.260855354
O         1.699999106    -0.991806182     0.456111446
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "22-1.0")] = qcdb.Molecule(
    """
0   2
C        -1.386232505    -0.704989974    -0.333975938
C        -1.849161455     0.455249666     0.067713982
H        -1.645695855    -1.746577804    -0.222174858
H        -2.739035025     0.520132266     0.694910092
H        -1.369433075     1.389975186    -0.203153238
--
0   1
C         1.645874905     0.103247936     0.107536292
O         1.441487285     1.192129416    -0.250035438
O         1.865126985    -0.981324744     0.466931362
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "22-1.2")] = qcdb.Molecule(
    """
0   2
C        -1.716488264    -0.725952849    -0.355615769
C        -2.179417214     0.434286791     0.046074151
H        -1.975951614    -1.767540679    -0.243814689
H        -3.069290784     0.499169391     0.673270261
H        -1.699688834     1.369012311    -0.224793069
--
0   1
C         1.976130664     0.124210811     0.129176123
O         1.771743044     1.213092291    -0.228395607
O         2.195382744    -0.960361869     0.488571193
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "22-1.5")] = qcdb.Molecule(
    """
0   2
C        -2.211871902    -0.757397162    -0.388075516
C        -2.674800852     0.402842478     0.013614404
H        -2.471335252    -1.798984992    -0.276274436
H        -3.564674422     0.467725078     0.640810514
H        -2.195072472     1.337567998    -0.257252816
--
0   1
C         2.471514302     0.155655124     0.161635870
O         2.267126682     1.244536604    -0.195935860
O         2.690766382    -0.928917556     0.521030940
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "22-2.0")] = qcdb.Molecule(
    """
0   2
C        -3.037511299    -0.809804349    -0.442175095
C        -3.500440249     0.350435291    -0.040485175
H        -3.296974649    -1.851392179    -0.330374015
H        -4.390313819     0.415317891     0.586710935
H        -3.020711869     1.285160811    -0.311352395
--
0   1
C         3.297153699     0.208062311     0.215735449
O         3.092766079     1.296943791    -0.141836281
O         3.516405779    -0.876510369     0.575130519
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "23-0.9")] = qcdb.Molecule(
    """
0   3
He       -1.738350000     0.000000000     0.000000000
--
0   3
He        1.738350000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "23-1.0")] = qcdb.Molecule(
    """
0   3
He       -1.931500000     0.000000000     0.000000000
--
0   3
He        1.931500000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "23-1.2")] = qcdb.Molecule(
    """
0   3
He       -2.317800000     0.000000000     0.000000000
--
0   3
He        2.317800000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "23-1.5")] = qcdb.Molecule(
    """
0   3
He       -2.897250000     0.000000000     0.000000000
--
0   3
He        2.897250000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "23-2.0")] = qcdb.Molecule(
    """
0   3
He       -3.863000000     0.000000000     0.000000000
--
0   3
He        3.863000000     0.000000000     0.000000000
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "24-0.9")] = qcdb.Molecule(
    """
1   2
C         0.000000000    -0.436434806     0.497570949
O         0.000000000     0.196238679     1.420138459
--
0   1
F         0.000000000     0.109938945    -0.992070159
H         0.000000000    -0.582542676    -1.636605903
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "24-1.0")] = qcdb.Molecule(
    """
1   2
C         0.000000000    -0.444773807     0.611409007
O         0.000000000     0.187899678     1.533976518
--
0   1
F         0.000000000     0.118277946    -1.105908217
H         0.000000000    -0.574203674    -1.750443962
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "24-1.2")] = qcdb.Molecule(
    """
1   2
C         0.000000000    -0.461451810     0.839085125
O         0.000000000     0.171221675     1.761652635
--
0   1
F         0.000000000     0.134955949    -1.333584335
H         0.000000000    -0.557525671    -1.978120079
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "24-1.5")] = qcdb.Molecule(
    """
1   2
C         0.000000000    -0.486468814     1.180599300
O         0.000000000     0.146204671     2.103166811
--
0   1
F         0.000000000     0.159972954    -1.675098511
H         0.000000000    -0.532508667    -2.319634255
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

GEOS["%s-%s-dimer" % (dbse, "24-2.0")] = qcdb.Molecule(
    """
1   2
C         0.000000000    -0.528163822     1.749789594
O         0.000000000     0.104509663     2.672357104
--
0   1
F         0.000000000     0.201667961    -2.244288804
H         0.000000000    -0.490813659    -2.888824548
--
Gh(H)     0.000000000     0.000000000     0.000000000

units angstrom
no_reorient
no_com
symmetry c1
"""
)

# <<< Derived Geometry Strings >>>
for rxn in HRXN:
    GEOS["%s-%s-monoA-CP" % (dbse, rxn)] = GEOS[
        "%s-%s-dimer" % (dbse, rxn)
    ].extract_fragments(1, [2, 3])
    GEOS["%s-%s-monoB-CP" % (dbse, rxn)] = GEOS[
        "%s-%s-dimer" % (dbse, rxn)
    ].extract_fragments(2, [1, 3])
