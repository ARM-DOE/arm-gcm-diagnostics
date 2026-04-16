import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import calendar
import math
import xarray as xr


def get_diurnal_cycle_seasons_xr(var, seasons, years, nhour=None):
    """
    Returns array with shape [nyears, nseasons, 365, nhour]
    Season slices:
      - ANN: first 365 days
      - MAM/JJA/SON/DJF: 90-day windows starting Mar1/Jun1/Sep1/Dec1
    Notes:
      - Leap years handled for indexing, but output always 365 days.
      - Input var is assumed to be 1D time series of length sum(year_days * nhour).
    """
    nyears = len(years)
    nseasons = len(seasons)
    t0 = 0
    time_length = len(var)

    if nhour is not None:
        print(f"Using user-specified nhour={nhour}")
    elif time_length % 24 == 0:
        nhour = 24
        print("Determined nhour=24 (hourly data)")
    elif time_length % 8 == 0:
        nhour = 8
        print("Determined nhour=8 (3-hourly data)")
    else:
        nhour = 24
        print(f"Warning: Could not determine hour resolution from data length {time_length}. Using nhour=24.")

    var_seasons = np.full((nyears, nseasons, 365, nhour), np.nan)

    for iyear in range(nyears):
        nday = 366 if calendar.isleap(int(years[iyear])) else 365
        ntime = int(nday * nhour)

        if t0 + ntime > len(var):
            print(f"Warning: Not enough data for year {years[iyear]}")
            break

        var1 = var[t0:t0 + ntime]
        var1_ext = np.concatenate((var1, var1), axis=0)  # for DJF window wrap
        t0 += ntime

        for iseason, season in enumerate(seasons):
            if season == "ANN":
                length = int(365 * nhour)
                var_seasons0 = var1[0:length]
                var_seasons1 = np.reshape(var_seasons0, (365, nhour))
                var_seasons[iyear, iseason, :, :] = var_seasons1
                continue

            if season == "MAM":
                t1 = 60 if nday == 366 else 59
            elif season == "JJA":
                t1 = 152 if nday == 366 else 151
            elif season == "SON":
                t1 = 244 if nday == 366 else 243
            elif season == "DJF":
                t1 = 335 if nday == 366 else 334
            else:
                print(f"Unrecognized season: {season}")
                continue

            var_seasons0 = var1_ext[int(t1 * nhour): int(t1 * nhour) + 90 * nhour]
            var_seasons1 = np.reshape(var_seasons0, (90, nhour))
            var_seasons[iyear, iseason, 0:90, :] = var_seasons1

    return var_seasons


def diurnal_cycle_LAcoupling_plot(parameter):
    variables = parameter.variables
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    output_path = parameter.output_path
    sites = parameter.sites
    units = parameter.units
    seasons = parameter.season

    nseasons = len(seasons)
    nvariables = len(variables)

    print("test_path: ", test_path)

    fig_dir = os.path.join(output_path, "figures", sites[0])
    os.makedirs(fig_dir, exist_ok=True)

    test_file = glob.glob(
        os.path.join(test_path, f"{sites[0][:3]}testmodel3hrLAcoupling{sites[0][3:5].upper()}*.nc")
    )
    print("Processing test_file: ", test_file)
    if not test_file:
        print(f"No test files found for {sites[0]}")
        return
    test_ds = xr.open_dataset(test_file[0], decode_times=False)

    obs_file = glob.glob(
        os.path.join(obs_path, f"{sites[0][:3]}armdiagsLAcoupling{sites[0][3:5].upper()}*c1.nc")
    )
    print("Processing obs_file", obs_file)
    if not obs_file:
        print(f"No observation files found for {sites[0]}")
        test_ds.close()
        return
    obs_ds = xr.open_dataset(obs_file[0], decode_times=False)

    print("OBS vars:", list(obs_ds.data_vars))
    print("TEST vars:", list(test_ds.data_vars))

    try:
        for ivar in range(nvariables):
            varname = variables[ivar]
            print(f"Processing variable: {varname}")

            # -------------------------
            # OBS processing (required)
            # -------------------------
            if varname not in obs_ds:
                print(f"Variable {varname} not found in observation dataset. Skipping.")
                continue

            try:
                var = obs_ds[varname].values
                years_obs = list(range(2004, 2016))
                nyears_obs = len(years_obs)
                nhour_obs = 24

                var_seasons = get_diurnal_cycle_seasons_xr(var, seasons, years_obs, nhour=nhour_obs)

                if var_seasons.shape[3] != nhour_obs:
                    print(f"Warning: OBS nhour mismatch for {varname}, expected {nhour_obs}, got {var_seasons.shape[3]}. Skipping.")
                    continue

                narray_obs = nyears_obs * 365
                var_seasons1 = np.full((nseasons, narray_obs, nhour_obs), np.nan)
                var_array = np.full((nseasons, nhour_obs), np.nan)
                var_array_err = np.full((nseasons, nhour_obs), np.nan)

                for iseason in range(nseasons):
                    for iyear in range(nyears_obs):
                        for iday in range(365):
                            var_seasons1[iseason, 365 * iyear + iday, :] = var_seasons[iyear, iseason, iday, :]

                    array_tmp = var_seasons1[iseason, :, :]
                    std0 = np.nanstd(array_tmp, axis=0)
                    var_array_err[iseason, :] = std0 / math.sqrt(narray_obs)
                    var_array[iseason, :] = np.nanmean(array_tmp, axis=0)

            except Exception as e:
                print(f"Error processing observation data for {varname}: {e}")
                continue  # without OBS, no point plotting

            # -------------------------
            # MOD processing (optional)
            # -------------------------
            have_mod = False
            nhour_mod = 8
            var_mod_array = np.full((nseasons, nhour_mod), np.nan)
            var_mod_array_err = np.full((nseasons, nhour_mod), np.nan)

            if varname in test_ds:
                try:
                    var_mod = test_ds[varname].values
                    years_mod = list(range(2003, 2015))
                    nyears_mod = len(years_mod)

                    var_mod_seasons = get_diurnal_cycle_seasons_xr(var_mod, seasons, years_mod, nhour=nhour_mod)

                    if var_mod_seasons.shape[3] != nhour_mod:
                        print(f"Warning: MOD nhour mismatch for {varname}, expected {nhour_mod}, got {var_mod_seasons.shape[3]}. Plotting OBS only.")
                        have_mod = False
                    else:
                        narray_mod = nyears_mod * 365
                        var_mod_seasons1 = np.full((nseasons, narray_mod, nhour_mod), np.nan)

                        for iseason in range(nseasons):
                            for iyear in range(nyears_mod):
                                for iday in range(365):
                                    var_mod_seasons1[iseason, 365 * iyear + iday, :] = var_mod_seasons[iyear, iseason, iday, :]

                            array_tmp = var_mod_seasons1[iseason, :, :]
                            std0 = np.nanstd(array_tmp, axis=0)
                            var_mod_array_err[iseason, :] = std0 / math.sqrt(narray_mod)
                            var_mod_array[iseason, :] = np.nanmean(array_tmp, axis=0)

                        have_mod = True

                except Exception as e:
                    print(f"Error processing model data for {varname}: {e}")
                    have_mod = False
            else:
                print(f"Variable {varname} not found in test model dataset. Will plot OBS only.")
                have_mod = False

            # -------------------------
            # Plotting
            # -------------------------
            for iseason in range(nseasons):
                fig = plt.figure(figsize=[8, 4], dpi=100)

                # OBS (always)
                xax = np.arange(26) - 0.5

                y_data = np.full(26, np.nan)
                y_data[0:19] = var_array[iseason, 5:24]
                y_data[19:26] = var_array[iseason, 0:7]

                e_data = np.full(26, np.nan)
                e_data[0:19] = var_array_err[iseason, 5:24]
                e_data[19:26] = var_array_err[iseason, 0:7]

                plt.errorbar(xax, y_data, e_data, color="black", label="OBS", linewidth=2)

                # MOD (optional)
                if have_mod:
                    if varname in ("SH", "LH"):
                        xax1 = np.arange(10) * 3 - 1.5
                    else:
                        xax1 = np.arange(10) * 3 - 3.0

                    y1_data = np.full(10, np.nan)
                    y1_data[0:7] = var_mod_array[iseason, 1:8]
                    y1_data[7:10] = var_mod_array[iseason, 0:3]

                    e1_data = np.full(10, np.nan)
                    e1_data[0:7] = var_mod_array_err[iseason, 1:8]
                    e1_data[7:10] = var_mod_array_err[iseason, 0:3]

                    plt.errorbar(xax1, y1_data, e1_data, color="red", label="MOD", linewidth=2)

                plt.ylabel(units[ivar], fontsize=12)
                plt.title(f"{varname} ({seasons[iseason]})", fontsize=14)
                plt.xticks(
                    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
                    ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"],
                )
                plt.xlabel("LST (hour)", fontsize=12)
                plt.xlim([-0.1, 24.1])
                if varname == "pbl":
                    plt.xlim([7.4, 17.6])

                plt.legend()

                fig_path = os.path.join(fig_dir, f"Diurnal_cycle_{seasons[iseason]}_{varname}_{sites[0]}.png")
                plt.savefig(fig_path)
                plt.close()

    finally:
        # Always close datasets
        try:
            obs_ds.close()
        except Exception:
            pass
        try:
            test_ds.close()
        except Exception:
            pass
