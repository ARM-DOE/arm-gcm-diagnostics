#========================================================
# Diurnal metircs for land-atmosphere coupling
# The analysis is emphasized on the diurnal amplitudes 
#  of surface energy budget components
#========================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import xarray as xr

def derivative_with_missing(t, d):
    """Compute derivative of d(t), skipping NaNs."""
    t = np.asarray(t, dtype=float)
    d = np.asarray(d, dtype=float)
    n = len(t)
    deriv = np.full(n, np.nan)
    valid = ~np.isnan(d)
    idx = np.where(valid)[0]

    for i in idx:
        if i == 0:
            if valid[i + 1]:
                deriv[i] = (d[i + 1] - d[i]) / (t[i + 1] - t[i])
        elif i == n - 1:
            if valid[i - 1]:
                deriv[i] = (d[i] - d[i - 1]) / (t[i] - t[i - 1])
        else:
            if valid[i - 1] and valid[i + 1]:
                deriv[i] = (d[i + 1] - d[i - 1]) / (t[i + 1] - t[i - 1])
            elif valid[i - 1]:
                deriv[i] = (d[i] - d[i - 1]) / (t[i] - t[i - 1])
            elif valid[i + 1]:
                deriv[i] = (d[i + 1] - d[i]) / (t[i + 1] - t[i])

    return deriv

def derivative(t, d):
    """Derivative of d(t) with no missing values."""
    t = np.asarray(t, dtype=float)
    d = np.asarray(d, dtype=float)
    return np.gradient(d, t)

def diurnal_dcomp(d_in, hours_in):
    """
      Compute diurnal amplitude (max - min) for each full 24-hour block.
      Assumes consecutive hourly data.
    """
    d = np.asarray(d_in)
    n_full_days = d.size // 24
    if n_full_days == 0:
        return np.array([])

    am_d = np.full(n_full_days, np.nan)
    for i in range(n_full_days):
        i1, i2 = i * 24, (i + 1) * 24
        dd = d[i1:i2]
        if np.all(np.isnan(dd)):
            continue
        am_d[i] = np.nanmax(dd) - np.nanmin(dd)
    return am_d

def get_indices(years, months, target_years, target_months=None):
    years = np.asarray(years)
    months = np.asarray(months)
    if target_months is None:
        return np.where(np.isin(years, target_years))[0]
    else:
        return np.where(
            np.isin(years, target_years) & np.isin(months, target_months)
        )[0]

def prepare_diurnal_amplitudes(data, target_years, seasons, months_p, variables):
    """
    Compute diurnal amplitudes for listed variables and seasons.
    Returns dict with keys like "DJF_Am_net_srf".
    """
    diurnal_amp = {}
    years = data["year"]
    months = data["month"]
    hours = data["hour"]

    for season in seasons:
        if season == "ANN":
            # Annual, use all months for the target years
            ind = get_indices(years, months, target_years)
        else:
            # Use the months corresponding to this season
            # months_p is expected to be a dict like {"DJF": [12,1,2], ...}
            try:
                season_months = months_p[season]
            except (KeyError, TypeError):
                raise ValueError(
                    f"months_p must provide months for season '{season}'. "
                    f"Got months_p={months_p!r}"
                )
            ind = get_indices(years, months, target_years, season_months)

        for var in variables:
            vals = np.asarray(data[var])[ind]
            hrs = np.asarray(hours)[ind]
            n_full_days = len(vals) // 24
            if n_full_days == 0:
                diurnal_amp[f"{season}_Am_{var}"] = np.array([])
            else:
                vals_trunc = vals[: n_full_days * 24]
                hrs_trunc = hrs[: n_full_days * 24]
                amp = diurnal_dcomp(vals_trunc, hrs_trunc)
                diurnal_amp[f"{season}_Am_{var}"] = amp

    return diurnal_amp

def plot_compare_scatters(
    ifig,
    fig_config,
    diurnal_obs,
    diurnal_mod,
    fig_dir="./",
    cutoff_x=-1.0e9,
    cutoff_y=-1.9,
    seasons_for_plots=None,
):

    # Determine season
    # We now expect exactly one season, but fall back to DJF if not provided.
    if seasons_for_plots is None or len(seasons_for_plots) == 0:
        seasons = ["DJF"]
    else:
        seasons = list(seasons_for_plots)

    season = seasons[0]

    vars_pair = fig_config["vars"]
    labels = fig_config["labels"]

    # Variable names for this season
    var_x = f"{season}_Am_{vars_pair[0]}"
    var_y = f"{season}_Am_{vars_pair[1]}"

    # Retrieve data
    x_obs = diurnal_obs.get(var_x, np.array([])).copy()
    y_obs = diurnal_obs.get(var_y, np.array([])).copy()
    x_mod = diurnal_mod.get(var_x, np.array([])).copy()
    y_mod = diurnal_mod.get(var_y, np.array([])).copy()

    # Basic validity checks
    if (
        x_obs.size == 0
        or y_obs.size == 0
        or x_mod.size == 0
        or y_mod.size == 0
        or x_obs.shape != y_obs.shape
        or x_mod.shape != y_mod.shape
    ):
        print(
            f"No valid data for season {season} "
            f"({var_x}, {var_y}); skipping figure {ifig}"
        )
        return

    # Apply cutoffs
    mask_obs = (x_obs > cutoff_x) & (y_obs > cutoff_y)
    mask_mod = (x_mod > cutoff_x) & (y_mod > cutoff_y)
    x_obs, y_obs = x_obs[mask_obs], y_obs[mask_obs]
    x_mod, y_mod = x_mod[mask_mod], y_mod[mask_mod]

    if x_obs.size == 0 and x_mod.size == 0:
        print(
            f"All points filtered out for season {season} "
            f"({var_x}, {var_y}); skipping figure {ifig}"
        )
        return

    # Single panel figure
    fig, ax = plt.subplots(figsize=(5, 4))

    color_obs = "black"
    color_mod = "red"

    # Scatter points
    if x_obs.size > 0:
        ax.scatter(x_obs, y_obs, color=color_obs, s=5, label="Obs")
    if x_mod.size > 0:
        ax.scatter(x_mod, y_mod, color=color_mod, s=5, label="Model")

    # Regression lines
    if len(x_obs) > 1:
        slope, intercept, *_ = linregress(x_obs, y_obs)
        ax.plot(x_obs, intercept + slope * x_obs, color=color_obs)

    if len(x_mod) > 1:
        slope, intercept, *_ = linregress(x_mod, y_mod)
        ax.plot(x_mod, intercept + slope * x_mod, color=color_mod)

    # Labels and titles
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.legend()

    title = (
        f"{season} "
    )
    ax.set_title(title, fontsize=12)

    # File name includes season
    all_labels = "_".join(vars_pair)
    fig_name = os.path.join(
        fig_dir, f"Diurnal_amplitude_{season}_{all_labels}.png"
    )

    plt.tight_layout()
    plt.savefig(fig_name, dpi=300, bbox_inches="tight")
    #print(f"Saved figure: {fig_name}")
    plt.close(fig)

def read_and_derive(fin):
    to_np = np.array

    T_srf      = to_np(fin["T_srf"].values)
    T_skin     = to_np(fin["T_skin"].values)
    LH         = to_np(fin["LH"].values)
    SH         = to_np(fin["SH"].values)
    sw_dn_srf  = to_np(fin["sw_dn_srf"].values)
    sw_up_srf  = to_np(fin["sw_up_srf"].values)
    lw_dn_srf  = to_np(fin["lw_dn_srf"].values)
    lw_up_srf  = to_np(fin["lw_up_srf"].values)
    pbl        = to_np(fin["pbl"].values)
    time       = to_np(fin["time"].values)
    year       = to_np(fin["year"].values)
    month      = to_np(fin["month"].values)
    day        = to_np(fin["day"].values)

    # If time is datetime64, convert to hours and then take modulo 24
    if np.issubdtype(time.dtype, np.datetime64):
        # Option A: hours since first time stamp
        t0 = time[0]
        time_hours = (time - t0) / np.timedelta64(1, "h")
        hour = time_hours % 24

        # If you prefer local clock hour instead of hours since start, use:
        # import pandas as pd
        # hour = pd.to_datetime(time).hour.values.astype(float)
    else:
        # Original behavior for numeric time (e.g., hours since a reference)
        hour = time % 24

    LHSH = LH + SH
    sw_net_srf = sw_dn_srf - sw_up_srf
    lw_net_srf = lw_up_srf - lw_dn_srf
    rad_net_srf = sw_net_srf - lw_net_srf
    net_srf = rad_net_srf - LHSH

    if np.any(np.isnan(T_skin)):
        dTsdt = derivative_with_missing(time, T_skin)
    else:
        dTsdt = derivative(time, T_skin)

    data = {
        "time": time,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "T_srf": T_srf,
        "T_skin": T_skin,
        "LH": LH,
        "SH": SH,
        "sw_dn_srf": sw_dn_srf,
        "sw_up_srf": sw_up_srf,
        "lw_dn_srf": lw_dn_srf,
        "lw_up_srf": lw_up_srf,
        "sw_net_srf": sw_net_srf,
        "lw_net_srf": lw_net_srf,
        "rad_net_srf": rad_net_srf,
        "pbl": pbl,
        "LHSH": LHSH,
        "net_srf": net_srf,
        "dTsdt": dTsdt,
    }
    return data

def diurnal_amplitude_plot(parameter):
    """
    Main driver for diurnal amplitude scatter plots.

    Seasons are taken from parameter.season (string or list).
    Years are fixed to [2010, 2011, 2012, 2013].

    This version saves separate figures for each season, instead of
    multi-panel plots with all seasons.
    """
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    output_path = parameter.output_path
    test_model = parameter.test_data_set

    # These must exist in your parameter object
    sites = parameter.sites          # string or list of site IDs
    seasons_param = parameter.season # string or list of seasons

    # Normalize sites to a list; use the first site
    site = sites[0] if isinstance(sites, (list, tuple)) else sites

    # Normalize seasons to a list
    if isinstance(seasons_param, str):
        seasons = [seasons_param]
    else:
        seasons = list(seasons_param)

    # Month mapping only for standard seasons; ANN is handled separately
    season_months_map = {
        "DJF": [12, 1, 2],
        "MAM": [3, 4, 5],
        "JJA": [6, 7, 8],
        "SON": [9, 10, 11],
    }

    # Fixed years for both obs and model
    years_obs = [2010, 2011, 2012, 2013]
    years_mod = [2010, 2011, 2012, 2013]

    # Build file paths; adjust to your naming convention if needed
    datafile_mod = os.path.join(
        test_path, f"{site[:3]}{test_model}1hrLAcouplingC1.c1.nc"
    )
    datafile_obs = os.path.join(
        obs_path, f"{site[:3]}armdiagsLAcouplingC1_add_more_vars.c1.nc"
    )

    print(f"Model file: {datafile_mod}")
    print(f"Obs file:   {datafile_obs}")

    with xr.open_dataset(datafile_mod) as fin_mod, xr.open_dataset(datafile_obs) as fin_obs:
        data_obs = read_and_derive(fin_obs)
        data_mod = read_and_derive(fin_mod)
    scatter_vars = [
        "net_srf",
        "dTsdt",
        "sw_dn_srf",
        "sw_up_srf",
        "T_skin",
        "T_srf",
        "LHSH",
        "pbl",
    ]

    diurnal_obs = prepare_diurnal_amplitudes(
        data_obs, years_obs, seasons, season_months_map, scatter_vars
    )
    diurnal_mod = prepare_diurnal_amplitudes(
        data_mod, years_mod, seasons, season_months_map, scatter_vars
    )

    # Scatter plot configurations
    fig_scatter1 = {
        "vars": ["net_srf", "dTsdt"],
        "labels": ["net_srf_flux amplitude (W/m2)", "dTs/dt amplitude (K/hr)"],
    }
    fig_scatter2 = {
        "vars": ["sw_dn_srf", "sw_up_srf"],
        "labels": ["sw_dn_srf amplitude (W/m2)", "sw_up_srf amplitude (W/m2)"],
    }
    fig_scatter3 = {
        "vars": ["T_skin", "T_srf"],
        "labels": ["Ts amplitude (C)", "Tair amplitude (C)"],
    }
    fig_scatter4 = {
        "vars": ["LHSH", "pbl"],
        "labels": ["(LH + SH) amplitude (W/m2)", "PBLH amplitude (m)"],
    }

    figs_scat = [fig_scatter1, fig_scatter2, fig_scatter3, fig_scatter4]

    fig_dir = os.path.join(output_path, "figures", site)
    os.makedirs(fig_dir, exist_ok=True)

    # New: loop over seasons, make separate figures
    for season in seasons:
        seasons_for_plots = [season]

        for i, fig_cfg in enumerate(figs_scat, start=1):
            # Unique ID that includes the season
            fig_id = f"{i}_{season}"

            plot_compare_scatters(
                fig_id,
                fig_cfg,
                diurnal_obs,
                diurnal_mod,
                seasons_for_plots=seasons_for_plots,
                fig_dir=fig_dir,
            )

    print("diurnal_amplitude_plot: Done.")
