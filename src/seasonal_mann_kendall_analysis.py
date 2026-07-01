import numpy as np
import pymannkendall as mk
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

# ✅ File paths
rf_files = [
    "C:/Radiative forcing/output/RF_Matrix_1980_1991.npy",
    "C:/Radiative forcing/output/RF_Matrix_1992_2000.npy",
    "C:/Radiative forcing/output/RF_Matrix_2001_2010.npy",
    "C:/Radiative forcing/output/RF_Matrix_2011_2024.npy"
]

# ✅ Define seasons
season_indices = {
    "Winter": [11, 0, 1],
    "Pre-Monsoon": [2, 3, 4],
    "Monsoon": [5, 6, 7, 8],
    "Post-Monsoon": [9, 10]
}

# ✅ Initialize
rf_seasonal_series = {season: [] for season in season_indices}
grid_shape = None

# ✅ Load & compute seasonal means
for file in rf_files:
    rf_matrix = np.load(file)
    if grid_shape is None:
        grid_shape = rf_matrix.shape[:2]
    for season, indices in season_indices.items():
        if rf_matrix.shape[2] <= max(indices):
            continue
        seasonal_mean = np.nanmean(rf_matrix[:, :, indices, :], axis=(2, 3))
        rf_seasonal_series[season].append(seasonal_mean)

# ✅ Stack time series
for season in rf_seasonal_series:
    rf_seasonal_series[season] = np.stack(rf_seasonal_series[season], axis=0)

# ✅ Mann-Kendall trend analysis
tau_values = {}
p_values = {}

for season in season_indices:
    tau = np.full(grid_shape, np.nan)
    p = np.full(grid_shape, np.nan)
    data = rf_seasonal_series[season]

    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            ts = data[:, i, j]
            if not np.isnan(ts).all():
                result = mk.original_test(ts)
                tau[i, j] = result.Tau
                p[i, j] = result.p

    tau_values[season] = tau
    p_values[season] = p

# ✅ Plot all seasons in one figure
fig, axes = plt.subplots(2, 2, figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})
fig.suptitle("Seasonal Kendall's Tau Trend of Radiative Forcing over India (1980–2024)", fontsize=18)

cmap = "coolwarm"
lon_min, lon_max = 40, 100
lat_min, lat_max = 0, 40
season_list = list(season_indices.keys())

for idx, season in enumerate(season_list):
    ax = axes[idx // 2, idx % 2]
    ax.set_title(season, fontsize=14)

    im = ax.imshow(
        tau_values[season],
        extent=[lon_min, lon_max, lat_min, lat_max],
        cmap=cmap,
        vmin=-1,
        vmax=1,
        origin='lower'
    )

    # Overlay significant points
    sig_mask = p_values[season] < 0.05
    y, x = np.where(sig_mask)
    ax.scatter(
        lon_min + (x * (lon_max - lon_min) / grid_shape[1]),
        lat_min + (y * (lat_max - lat_min) / grid_shape[0]),
        s=2, color='black'
    )

    # Add borders and coastlines
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

    # ✅ Add latitude and longitude gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 8}
    gl.ylabel_style = {"size": 8}

# ✅ Add single colorbar
cbar_ax = fig.add_axes([0.25, 0.08, 0.5, 0.02])
fig.colorbar(im, cax=cbar_ax, orientation='horizontal', label="Kendall's Tau (Trend Strength)")

# ✅ Save the combined figure
output_path = "C:/Radiative forcing/plots/Seasonal_Kendall_Tau_Combined.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Combined seasonal MK trend plot saved at: {output_path}")
