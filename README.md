# EU Climate Hazard Indices — Data Analysis

Personal learning project exploring EU climate data ecosystems.
Part of an ongoing series on EU climate data, written publicly on LinkedIn.

## About this project

This repository contains data analysis and visualisations supporting
a series of LinkedIn articles on EU climate data and policy.

The analysis focuses on climate-related hazard indices as defined in:
> Crespi et al. (2020). Climate-related hazard indices for Europe.
> ETC/CCA Technical Paper 1/2020.
> DOI: 10.25424/cmcc/climate_related_hazard_indices_europe_2020

---

## Article 4 — Heatwave days based on apparent temperature

**Index #8:** Heatwave days based on apparent temperature (EuroHEAT definition)

### What this analysis covers
- European heatwave trends from 1986 to 2085
- Two emissions scenarios: RCP 4.5 (medium) and RCP 8.5 (high)
- Country-level comparison across 10 EU Member States
- Three visualisations: time series, spatial maps, country bar charts

### Key findings
- 1986 baseline: 3.2 heatwave days per year (European average)
- 2085 under RCP 4.5: 18.7 days — a 6x increase
- 2085 under RCP 8.5: 38.7 days — a 12x increase
- Strongest impacts: Greece (~57 days), Italy (~55 days), Spain (~48 days) under RCP 8.5

### Data source
- **Dataset:** Heat waves and cold spells in Europe derived from climate projections
- **Provider:** Copernicus Climate Change Service (C3S)
- **CDS identifier:** sis-heat-and-cold-spells
- **Definition used:** Health related (EuroHEAT)
- **Access:** https://cds.climate.copernicus.eu/datasets/sis-heat-and-cold-spells

### Files
- data/ — Raw NetCDF files from C3S
- notebooks/heatwave_days_analysis.ipynb — Full analysis notebook
- scripts/heatwave_days_analysis.py — Standalone Python script
- outputs/heatwave_timeseries_europe.png — Time series 1986-2085
- outputs/heatwave_map_europe.png — Spatial maps by period
- outputs/heatwave_by_country.png — Country comparison

### How to reproduce
1. Clone this repository
2. Install dependencies: pip install -r requirements.txt
3. Download data from CDS (free account required):
   https://cds.climate.copernicus.eu/datasets/sis-heat-and-cold-spells
4. Run the notebook or script

---

## Related LinkedIn articles
- Article 1: Where EU climate data comes from
- Article 2: What the Joint Research Centre (JRC) does
- Article 3: Eurostat data
- Article 4: Deep dive — Heatwave days based on apparent temperature (this analysis)

---

*Author: Galiya Ibragimova*
*Last updated: April 2026*
