# EXP-007 Results — Alternative Coding Schemes

## Headline

Base selection was performed independently for each scheme using training moduli only. The held-out and replication sets were not used to select a base.

| Coding scheme | Training-selected base | Held-out mean (selected) | Held-out mean (base 9) | Replication mean (selected) | Replication mean (base 9) |
|---|---:|---:|---:|---:|---:|
| gamma_metadata_fixed_coefficients | 9 | 262.750 | 262.750 | 538.938 | 538.938 |
| gamma_metadata_gamma_coefficients | 9 | 359.750 | 359.750 | 774.500 | 774.500 |
| delta_metadata_fixed_coefficients | 9 | 261.125 | 261.125 | 537.250 | 537.250 |
| delta_metadata_gamma_coefficients | 9 | 358.125 | 358.125 | 772.813 | 772.813 |

## Training selection

- **gamma_metadata_fixed_coefficients** selected base **9**; training mean = 132.125 bits.
- **gamma_metadata_gamma_coefficients** selected base **9**; training mean = 171.250 bits.
- **delta_metadata_fixed_coefficients** selected base **9**; training mean = 132.250 bits.
- **delta_metadata_gamma_coefficients** selected base **9**; training mean = 171.375 bits.

## Held-out comparisons

### gamma_metadata_fixed_coefficients

| Base | Held-out mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 262.750 | 390 |
| 10 | 279.125 | 714 |
| 2 | 363.625 | 738 |

### gamma_metadata_gamma_coefficients

| Base | Held-out mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 359.750 | 574 |
| 10 | 388.375 | 1062 |
| 2 | 510.375 | 1110 |

### delta_metadata_fixed_coefficients

| Base | Held-out mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 261.125 | 388 |
| 10 | 277.625 | 711 |
| 2 | 361.875 | 735 |

### delta_metadata_gamma_coefficients

| Base | Held-out mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 358.125 | 572 |
| 10 | 386.875 | 1059 |
| 2 | 508.625 | 1107 |

## Independent replication

### gamma_metadata_fixed_coefficients

| Base | Replication mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 538.938 | 804 |
| 10 | 795.063 | 1486 |
| 2 | 826.938 | 1482 |

### gamma_metadata_gamma_coefficients

| Base | Replication mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 774.500 | 1171 |
| 10 | 1173.938 | 2266 |
| 2 | 1211.625 | 2262 |

### delta_metadata_fixed_coefficients

| Base | Replication mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 537.250 | 802 |
| 10 | 793.563 | 1485 |
| 2 | 825.688 | 1481 |

### delta_metadata_gamma_coefficients

| Base | Replication mean bits | Maximum bits |
|---:|---:|---:|
| 9 | 772.813 | 1169 |
| 10 | 1172.438 | 2265 |
| 2 | 1210.375 | 2261 |

## Interpretation

The training-selected base is **9, 9, 9, 9** across the four schemes, respectively. All four coding combinations select base 9 on training data. This is evidence about robustness within this small, predeclared coding grid only. It does not imply universal optimality, and the four schemes are not independent datasets: they encode the same mathematical objects with different costs.

## Data

- Search/held-out CSV rows: 2240.
- Replication CSV rows: 192.
- Full component-level accounting is retained for each row.
