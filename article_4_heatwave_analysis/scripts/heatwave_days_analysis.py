
# ============================================================
# Heatwave days in Europe — Analysis
# Index #8: Heatwave days based on apparent temperature
# EuroHEAT definition — ETC/CCA Technical Paper 1/2020
# Data source: Copernicus C3S, dataset: sis-heat-and-cold-spells
# Author: Galiya Ibragimova
# Date: April 2026
# ============================================================

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import os

# ── LOAD DATA ──
rcp45 = xr.open_dataset("heatwave_data/HWD_EU_health_rcp45_mean_v1.0.nc")
rcp85 = xr.open_dataset("heatwave_data/HWD_EU_health_rcp85_mean_v1.0.nc")

# ── CHART 1: TIME SERIES ──
years = rcp45.time.dt.year.values
mean_rcp45 = rcp45.HWD_EU_health.mean(dim=["lat", "lon"]).values
mean_rcp85 = rcp85.HWD_EU_health.mean(dim=["lat", "lon"]).values

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(years, mean_rcp45, color="#F0997B", linewidth=2.5, label="RCP 4.5 — medium emissions")
ax.plot(years, mean_rcp85, color="#D85A30", linewidth=2.5, label="RCP 8.5 — high emissions")
ax.fill_between(years, mean_rcp45, mean_rcp85, alpha=0.15, color="#D85A30", label="Difference between scenarios")
ax.axhline(y=mean_rcp45[0], color="gray", linestyle="--", linewidth=1, alpha=0.6, label=f"1986 baseline ({mean_rcp45[0]:.1f} days)")
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Heatwave days per year", fontsize=12)
ax.set_title("Heatwave days in Europe (1986–2085)\nBased on apparent temperature — EuroHEAT definition", fontsize=13, fontweight="bold")
ax.legend(loc="upper left", fontsize=10)
ax.set_xlim(1986, 2085)
ax.set_ylim(0, 45)
ax.grid(True, alpha=0.3)
fig.text(0.99, 0.01, "Source: Copernicus C3S · Dataset: sis-heat-and-cold-spells · ETC/CCA Technical Paper 1/2020", ha="right", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("heatwave_analysis/heatwave_timeseries_europe.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 1 saved")

# ── CHART 2: MAPS ──
periods = {"Recent past (1986)": 0, "Mid-century (2050)": 64, "End of century (2085)": 99}
fig, axes = plt.subplots(2, 3, figsize=(18, 10), subplot_kw={"projection": ccrs.PlateCarree()})
vmin, vmax = 0, 80
cmap = plt.cm.YlOrRd
for col, (period_name, time_idx) in enumerate(periods.items()):
    for row, (scenario, ds) in enumerate([("RCP 4.5 — medium emissions", rcp45), ("RCP 8.5 — high emissions", rcp85)]):
        ax = axes[row, col]
        data = ds.HWD_EU_health.isel(time=time_idx)
        im = ax.pcolormesh(ds.lon, ds.lat, data, transform=ccrs.PlateCarree(), cmap=cmap, vmin=vmin, vmax=vmax)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, color="gray")
        ax.add_feature(cfeature.BORDERS, linewidth=0.3, color="gray")
        ax.add_feature(cfeature.OCEAN, color="#EEF4FB", zorder=0)
        ax.add_feature(cfeature.LAND, color="#F5F5F5", zorder=0)
        ax.set_extent([-25, 35, 30, 72], crs=ccrs.PlateCarree())
        if row == 0:
            ax.set_title(period_name, fontsize=12, fontweight="bold", pad=8)
        if col == 0:
            ax.text(-0.08, 0.5, scenario, transform=ax.transAxes, fontsize=10, va="center", ha="right", rotation=90, fontweight="500")
cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label("Heatwave days per year", fontsize=11)
fig.suptitle("Heatwave days in Europe by region and emissions scenario\nBased on apparent temperature — EuroHEAT definition (Index #8, ETC/CCA Technical Paper 1/2020)", fontsize=13, fontweight="bold", y=1.01)
fig.text(0.5, -0.01, "Source: Copernicus C3S · Dataset: sis-heat-and-cold-spells · Processing: own analysis", ha="center", fontsize=9, color="gray")
plt.tight_layout(rect=[0, 0, 0.91, 1])
plt.savefig("heatwave_analysis/heatwave_map_europe.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 2 saved")

# ── CHART 3: BY COUNTRY ──
countries = {
    "Portugal":    [-9.5, -6.2, 37.0, 42.2],
    "Spain":       [-9.0,  3.3, 36.0, 43.8],
    "Italy":       [ 7.0, 18.5, 37.0, 47.1],
    "Greece":      [20.0, 26.5, 35.0, 42.0],
    "France":      [-5.0,  8.2, 42.3, 51.1],
    "Germany":     [ 6.0, 15.0, 47.3, 55.0],
    "Poland":      [14.1, 24.1, 49.0, 54.9],
    "Sweden":      [11.0, 24.2, 55.3, 69.1],
    "Belgium":     [ 2.5,  6.4, 49.5, 51.5],
    "Netherlands": [ 3.3,  7.2, 50.8, 53.6],
}
def country_mean(ds, bounds, time_idx):
    lon_min, lon_max, lat_min, lat_max = bounds
    subset = ds.HWD_EU_health.isel(time=time_idx).sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
    return float(subset.mean())
time_periods = {"1986": 0, "2050": 64, "2085": 99}
results_45 = {c: {p: country_mean(rcp45, b, i) for p, i in time_periods.items()} for c, b in countries.items()}
results_85 = {c: {p: country_mean(rcp85, b, i) for p, i in time_periods.items()} for c, b in countries.items()}
fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharey=True)
country_names = list(countries.keys())
x = np.arange(len(country_names))
width = 0.25
colors = {"1986": "#FDE8D8", "2050": "#F0997B", "2085": "#D85A30"}
for ax, (scenario_name, results) in zip(axes, [("RCP 4.5 — medium emissions", results_45), ("RCP 8.5 — high emissions", results_85)]):
    for i, (period, color) in enumerate(colors.items()):
        values = [results[c][period] for c in country_names]
        ax.bar(x + i * width, values, width, label=period, color=color, edgecolor="white", linewidth=0.5)
    ax.set_title(scenario_name, fontsize=12, fontweight="bold", pad=10)
    ax.set_xticks(x + width)
    ax.set_xticklabels(country_names, rotation=35, ha="right", fontsize=10)
    ax.set_ylabel("Heatwave days per year", fontsize=11)
    ax.legend(title="Period", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, 100)
fig.suptitle("Heatwave days per year by country and emissions scenario\nBased on apparent temperature — EuroHEAT definition (Index #8)", fontsize=13, fontweight="bold")
fig.text(0.5, -0.02, "Source: Copernicus C3S · Dataset: sis-heat-and-cold-spells · Processing: own analysis", ha="center", fontsize=9, color="gray")
plt.tight_layout()
plt.savefig("heatwave_analysis/heatwave_by_country.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 3 saved")

print("\n🎉 All charts regenerated successfully!")
