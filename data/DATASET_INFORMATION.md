# Dataset Information

## Dataset

This project uses the **NASA Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2)** atmospheric reanalysis dataset to analyze long-term trends in aerosol radiative forcing over the Indian subcontinent.

---

## Data Source

**NASA Goddard Earth Sciences Data and Information Services Center (GES DISC)**

Website:
https://disc.gsfc.nasa.gov/

**NASA’s Giovanni platform**

Website:
https://giovanni.gsfc.nasa.gov/giovanni/



---

## Study Region

- **Region:** Indian Subcontinent
- **Latitude:** 0°N – 40°N
- **Longitude:** 40°E – 100°E

---

## Study Period

**January 1980 – December 2024**

**45 Years**

---

## Variables Used

## MERRA-2 Variables

The aerosol radiative forcing analysis was derived from radiative flux variables available in the NASA MERRA-2 atmospheric reanalysis dataset.

### Surface Radiative Flux Variables

| Variable | Description |
|----------|-------------|
| SWGNTCLR | Surface net downward shortwave flux under clear-sky conditions |
| SWGNTCLRCLN | Surface net downward shortwave flux under clear-sky conditions without aerosols |
| LWGNTCLR | Surface net downward longwave flux under clear-sky conditions |
| LWGNTCLRCLN | Surface net downward longwave flux under clear-sky conditions without aerosols |

### Top of Atmosphere (TOA) Radiative Flux Variables

| Variable | Description |
|----------|-------------|
| SWTNTCLR | TOA net downward shortwave flux under clear-sky conditions |
| SWTNTCLRCLN | TOA net downward shortwave flux under clear-sky conditions without aerosols |
| LWTUPCLR | TOA upwelling longwave flux under clear-sky conditions |
| LWTUPCLRCLN | TOA upwelling longwave flux under clear-sky conditions without aerosols |

---

## Aerosol Radiative Forcing Calculation

For this repository, the seasonal trend analysis is based on **Aerosol Radiative Forcing at surface-of-atmosphere (SOA)**, which was calculated as:

\[
SOA = (SWGNTCLR + LWGNTCLR) - (SWGNTCLRCLN + LWGNTCLRCLN)
\]

where:

- **SWGNTCLR + LWGNTCLR** represents the total clear-sky surface radiative flux including aerosol effects.
- **SWGNTCLRCLN + LWGNTCLRCLN** represents the equivalent clear-sky surface radiative flux assuming aerosol-free conditions.

The difference between these quantities provides the aerosol-induced radiative forcing at the Earth's surface.

Monthly SOA fields were subsequently aggregated into seasonal means (Winter, Pre-Monsoon, Monsoon, and Post-Monsoon) before applying the Mann–Kendall trend test to quantify long-term seasonal trends across the Indian subcontinent (1980–2024).

Although TOA radiative flux variables were also downloaded from the MERRA-2 dataset, they are **not used in the present trend analysis**, which focuses exclusively on surface aerosol radiative forcing.

## Seasonal Classification

| Season | Months |
|---------|--------|
| Winter (DJF) | December, January, February |
| Pre-Monsoon (MAM) | March, April, May |
| Monsoon (JJAS) | June, July, August, September |
| Post-Monsoon (ON) | October, November |

---

## Trend Analysis


Seasonal aerosol radiative forcing time series were generated for each spatial grid point across India.

The **Mann–Kendall trend test** was then applied independently at every grid location to evaluate long-term monotonic trends.

For each grid point, the following statistical quantities were computed:

- Kendall's Tau
- p-value

Grid cells with **p < 0.05** were considered statistically significant.


---

## Data Format

- NetCDF (.nc)
- NumPy (.npy)

---

## Data Availability

The original MERRA-2 datasets are not included in this repository because of their large size.

Users can download the required datasets from NASA GES DISC's Giovanni Platform and reproduce the complete analysis using the Python scripts provided in the `src` directory.
