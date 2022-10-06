import csv
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import os
from datetime import date, time, datetime
from decimal import *


class Dataset:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            self.keys = reader.fieldnames

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if filename.endswith("csv"):
            self._filename = filename
        else:
            raise ValueError

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, keys):
        if len(keys) > 0:
            self._keys = keys
        else:
            raise ValueError

    def plot_param_t(self, season, param):
        if self.keys_exist(
            param, "Probe aus", "Datum letzter Ölwechsel", "Datum Probenentnahme"
        ) or self.keys_exist(param, "Probe aus", "Einfülltage"):

            oil_names = self.set_of_oils("wind turbine", season, param)

            listd = []
            for oil_name in oil_names:
                x = []
                y = []

                with open(self.filename) as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=";")
                    for row in reader:
                        if not ("Einfülltage" in self.keys):

                            if (
                                self.validate_season(
                                    row["Datum Probenentnahme"], season
                                )
                                and len(row["Datum letzter Ölwechsel"]) > 0
                                and row["Ölbezeichnung"] == oil_name
                                and self.origin_sample(
                                    row["Probe aus"], "wind", "wea", "wka", "éolienne"
                                )
                            ):
                                days_service = self.compute_days_in_service(
                                    row["Datum Probenentnahme"],
                                    row["Datum letzter Ölwechsel"],
                                )
                                if days_service > 0 and len(row[param]) > 0:

                                    x.append(days_service)
                                    y.append(float(row[param]))
                        else:
                            if (
                                len(row["Einfülltage"]) > 0
                                and row["Ölbezeichnung"] == oil_name
                                and self.origin_sample(
                                    row["Probe aus"], "wind", "wea", "wka", "éolienne"
                                )
                                and self.validate_season(
                                    row["Datum Probenentnahme"], season
                                )
                            ):
                                days_service = int(row["Einfülltage"])
                                if days_service > 0 and len(row[param]) > 0:
                                    x.append(days_service)
                                    y.append(float(row[param]))

                    # fig, ax = plt.subplots()
                    # ax.plot(x, y)
                    # plt.show()
                    # plt.plot([1,2,3])
                d = {
                    "oil_name": oil_name,
                    "season": season,
                    "x_values": x,
                    "y_values": y,
                }
                listd.append(d)
                if len(x) > 3:
                    fig, ax = plt.subplots()
                    match season:
                        case "summer":
                            ax.plot(x, y, "ro")
                        case "fall":
                            ax.plot(x, y, "mo")
                        case "winter":
                            ax.plot(x, y, "bo")
                        case "spring":
                            ax.plot(x, y, "go")
                        case _:
                            ax.plot(x, y, "ko")
                    # plt.plot(x, y, 'bo')
                    # print("oil: ", oil_name)
                    plt.title(f"Season: {season}, {oil_name}, {len(x)} points")
                    if param == "Wasser K. F.":
                        plt.ylabel("Water K.F. in ppm")
                        save_name = f"H2O_vs_days_{season}_{oil_name}.png"
                    elif param == "Neutralisationszahl":
                        plt.ylabel("Acid number in mgkOH/gOil")
                        save_name = f"AN_vs_days_{season}_{oil_name}.png"
                    elif param == "Oxidation":
                        plt.ylabel("Oxidation in A/cm")
                        save_name = f"Ox_vs_days_{season}_{oil_name}.png"
                    plt.xlabel("Days in service")

                    save_name = self.validate_file_name(save_name)
                    if param == "Wasser K. F.":
                        plt.savefig(f"data/water_KF/{save_name}")
                    elif param == "Neutralisationszahl":
                        plt.savefig(f"data/AN/{save_name}")
                    elif param == "Oxidation":
                        plt.savefig(f"data/ox/{save_name}")
                    plt.close(fig)
                    # plt.show()

            return listd

    def plot_param_t_all_seasons(self, p):

        ldfall = self.plot_param_t("fall", p)
        ldspring = self.plot_param_t("spring", p)
        ldwinter = self.plot_param_t("winter", p)
        ldsummer = self.plot_param_t("summer", p)

        if ldfall and ldspring and ldwinter and ldsummer:

            for d1 in ldfall:
                noil = d1["oil_name"]
                npoints = len(d1["x_values"])

                fig = plt.figure(figsize=(6, 3))
                gs = fig.add_gridspec(1, 5, width_ratios=(4, 0.5, 0.5, 0.5, 0.5),
                left=0.15, right=0.85, bottom=0.15, top=0.85,
                wspace=0.05, hspace=0.05)
                ax = fig.add_subplot(gs[0, 0])                    
                ax_histy_summer = fig.add_subplot(gs[0, 1], sharey=ax)  
                ax_histy_fall = fig.add_subplot(gs[0, 2], sharey=ax) 
                ax_histy_winter = fig.add_subplot(gs[0, 3], sharey=ax) 
                ax_histy_spring = fig.add_subplot(gs[0, 4], sharey=ax) 

                ax_histy_summer.tick_params(axis="y", labelleft=False)
                ax_histy_fall.tick_params(axis="y", labelleft=False)
                ax_histy_winter.tick_params(axis="y", labelleft=False)
                ax_histy_spring.tick_params(axis="y", labelleft=False)

                ylabelstr = ""


                binwidth = 0
                if p == "Wasser K. F.":
                    ylabelstr = "Water K.F. in ppm"
                    save_name = f"H2O_vs_days_all_{noil}.png"
                    ax.set_xlim(-50, 4000)
                    ax.set_ylim(0, 600)
                    if len(d1["x_values"]) > 150:
                        binwidth = 20
                    else:
                        binwidth = 25
                elif p == "Neutralisationszahl":
                    ylabelstr = "Acid number in mgkOH/gOil"
                    save_name = f"AN_vs_days_all_{noil}.png"
                elif p == "Oxidation":
                    ylabelstr = "Oxidation in A/cm"
                    save_name = f"Ox_vs_days_all_{noil}.png"
                #plt.xlabel("Days in service")
                ax.set_xlabel("Days in service")
                ax.set_ylabel(ylabelstr)

                # summer_patch = mpatches.Patch(color='red', label='Summer')
                summer_point = mlines.Line2D(
                    [],
                    [],
                    linewidth=0,
                    color="red",
                    marker="o",
                    markersize=7,
                    label="Summer",
                )
                # fall_patch = mpatches.Patch(color='magenta', label='Fall')
                fall_point = mlines.Line2D(
                    [],
                    [],
                    linewidth=0,
                    color="m",
                    marker="o",
                    markersize=7,
                    label="Fall",
                )
                # winter_patch = mpatches.Patch(color='blue', label='Winter')
                winter_point = mlines.Line2D(
                    [],
                    [],
                    linewidth=0,
                    color="blue",
                    marker="o",
                    markersize=7,
                    label="Winter",
                )
                # spring_patch = mpatches.Patch(color='green', label='Spring')
                spring_point = mlines.Line2D(
                    [],
                    [],
                    linewidth=0,
                    color="green",
                    marker="o",
                    markersize=7,
                    label="Spring",
                )
                ax.legend(
                    handles=[summer_point, fall_point, winter_point, spring_point]
                )



                #fig, ax = plt.subplots()
                ax.plot(d1["x_values"], d1["y_values"], "mo")
                if len(d1["x_values"]) > 0:                    
                    xymax = max(np.max(np.abs(d1["x_values"])), np.max(np.abs(d1["y_values"])))
                    lim = (int(xymax/binwidth) + 1) * binwidth
                    bins = np.arange(-lim, lim + binwidth, binwidth)                        
                    ax_histy_fall.hist(d1["y_values"], bins=bins, color="m", orientation='horizontal')
                
                for d2 in ldspring:
                    if d2["oil_name"] == noil:
                        npoints += len(d2["x_values"])
                        ax.plot(d2["x_values"], d2["y_values"], "go")
                        if len(d2["x_values"]) > 0:                    
                            xymax = max(np.max(np.abs(d2["x_values"])), np.max(np.abs(d2["y_values"])))
                            lim = (int(xymax/binwidth) + 1) * binwidth
                            bins = np.arange(-lim, lim + binwidth, binwidth)                                
                            ax_histy_spring.hist(d2["y_values"], bins=bins, color="green", orientation='horizontal')

                        for d3 in ldwinter:
                            if d3["oil_name"] == noil:
                                npoints += len(d3["x_values"])
                                ax.plot(d3["x_values"], d3["y_values"], "bo")
                                if len(d3["x_values"]) > 0:                                    
                                    xymax = max(np.max(np.abs(d3["x_values"])), np.max(np.abs(d3["y_values"])))
                                    lim = (int(xymax/binwidth) + 1) * binwidth
                                    bins = np.arange(-lim, lim + binwidth, binwidth)                                        
                                    ax_histy_winter.hist(d3["y_values"], bins=bins, color="blue", orientation='horizontal')
                                
                                for d4 in ldsummer:
                                    if d4["oil_name"] == noil:
                                        npoints += len(d4["x_values"])
                                        ax.plot(d4["x_values"], d4["y_values"], "ro")
                                        if len(d4["x_values"]) > 0:                    
                                            xymax = max(np.max(np.abs(d4["x_values"])), np.max(np.abs(d4["y_values"])))
                                            lim = (int(xymax/binwidth) + 1) * binwidth
                                            bins = np.arange(-lim, lim + binwidth, binwidth)                                                
                                            ax_histy_summer.hist(d4["y_values"], bins=bins, color="red", orientation='horizontal')
                                            break
                                        
                ax.set_title(f"Season: all, {noil}, {npoints} points")               



                save_name = self.validate_file_name(save_name)
                if p == "Wasser K. F.":
                    plt.savefig(f"data/water_KF/{save_name}")
                elif p == "Neutralisationszahl":
                    plt.savefig(f"data/AN/{save_name}")
                elif p == "Oxidation":
                    plt.savefig(f"data/ox/{save_name}")
                plt.close(fig)

    def compute_days_in_service(self, date_sample, date_last_change):

        ds = date.fromisoformat(date_sample)
        dlc = date.fromisoformat(date_last_change)
        if ds > dlc:
            deltaDays = (ds - dlc).days
            # print(deltaDays, str(ds))
            return deltaDays
        else:
            return -1

    def origin_sample(*arg):
        read_txt = arg[1]
        for t in range(len(arg) - 2):
            if arg[t + 2] in read_txt.lower():
                return True
        return False

    def validate_file_name(self, fn):
        if "/" in fn:
            fn = fn.replace("/", "_")
        if " " in fn:
            fn = fn.replace(" ", "_")
        return fn

    def validate_season(self, sample_date, season):
        try:
            sd = date.fromisoformat(sample_date)
            match season.lower():
                case "summer":
                    return True if 6 <= sd.month <= 8 else False
                case "fall":
                    return True if 9 <= sd.month <= 11 else False
                case "winter":
                    return True if 0 <= sd.month % 12 <= 2 else False
                case "spring":
                    return True if 3 <= sd.month <= 5 else False
                case _:
                    return True
        except ValueError:
            return False

    def keys_exist(*arg):
        for t in range(len(arg) - 1):
            if not (arg[t + 1] in arg[0].keys):
                return False
        return True

    def sort_by_param(self, param, oil_names, app):

        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            short_ds = []         
         
            for row1 in reader:                
                if app == "wind turbine":
                    
                    if row1["Ölbezeichnung"] in oil_names and (self.origin_sample(
                        row1["Probe aus"], "wind", "wea", "wka", "éolienne") 
                        or self.origin_sample(
                        row1["Komponente"], "wind", "wea", "wka", "éolienne")):                        
                        short_ds.append(row1)                    
                        
            return sorted(short_ds, key=lambda row: (row[param]))
            
    def set_of_oils(self, source, season, param):
        oil_names = set()
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                if "wind" in source.lower():
                    if (
                        row["Ölbezeichnung"] != ""
                        and self.origin_sample(
                            row["Probe aus"], "wind", "wea", "wka", "éolienne"
                        )
                        and len(row[param]) > 0
                        and self.validate_season(row["Datum Probenentnahme"], season)
                    ):
                        oil_names.add(row["Ölbezeichnung"])
        return oil_names

    def plot_data_machine(self, paramx, paramy):

        oil_names = self.set_of_oils("wind turbine", "all_seasons", paramy)
        
        if self.keys_exist("Anlagennummer"):
            a = "Anlagennummer"
        elif self.keys_exist("Probenbezeichnung"):
            a = "Probenbezeichnung"    
        if self.keys_exist(a):
            data = self.sort_by_param(a, oil_names, "wind turbine")    
     

        set_of_ids = set()
        for row in data:
            set_of_ids.add(row[a])

        # Number of samples for each machine
        n_el = []
        # List of machine ids
        list_of_ids = []
        i = 0

        ok = True
        while i < len(data) and ok:
            machine_id = (data[i])[a]
            j = i
            k = 0
            while (data[j])[a] == machine_id and ok:

                if j + 1 < len(data):
                    if paramx == "time":
                        if self.keys_exist("Einfülltage"):
                            if (not (len((data[j])["Einfülltage"]) > 0)) or (not (self.origin_sample(
                                (data[j])["Probe aus"], "wind", "wea", "wka", "éolienne"))):
                                k += 1
                        elif self.keys_exist(
                            "Datum letzter Ölwechsel", "Datum Probenentnahme"
                        ):

                            if (not (
                                (len((data[j])["Datum letzter Ölwechsel"]) > 0)
                                and (len((data[j])["Datum Probenentnahme"]) > 0)) or (not (self.origin_sample(
                                (data[j])["Probe aus"], "wind", "wea", "wka", "éolienne")))
                            ):
                                k += 1
                            else:
                                if self.compute_days_in_service((data[j])["Datum Probenentnahme"], (data[j])["Datum letzter Ölwechsel"]) < 0:   
                                    k += 1
                    else:
                        if (not (self.origin_sample((data[j])["Probe aus"], "wind", "wea", "wka", "éolienne"))):
                            k += 1                        
                    j = j + 1
                else:
                    ok = False

            if not ok:
                j = j + 1
            n_el.append(j - i - k)
            list_of_ids.append(machine_id)

            i = j

        res = dict(zip(list_of_ids, n_el))

        n_sa = 0
        for el in n_el:
            if el > 3:
                n_sa += 1
        
        
        for oil_name in oil_names:
            
            # k: data series that have been included in plots already
            k = 0
            print(oil_name, len(data), n_sa)
            ok1 = True
            while k < n_sa and ok1:
                x1 = []
                y1 = []
                x2 = []
                y2 = []
                x3 = []
                y3 = []

                # l counts the next data series to be plotted
                l = 1
                i = 0

                first_done = False
                second_done = False
                machine_id1 = ""
                machine_id2 = ""
                # Go through all rows
                
                while i < len(data):
                    
                    if (data[i])["Ölbezeichnung"] == oil_name and self.origin_sample((data[i])["Probe aus"], "wind", "wea", "wka", "éolienne"):
                        machine_id = (data[i])[a]
                        nop = res[machine_id]
                        
                            
                        if nop > 3 and (not first_done or not second_done):
                            
                            j = 0
                            s = 0
                            while j < nop and i+s < len(data):
                                #print(i+s, l, k, j, nop)
                                row = data[i + s]
                                if not first_done:                                    
                                    # Fill up x2 y2 only if the data has not been plotted before
                                    if l > k:
                                        # j increases only when the point is included to be plotted
                                        if paramx == "time":
                                            if not ("Einfülltage" in self.keys):
                                                if (
                                                    len(row["Datum letzter Ölwechsel"]) > 0
                                                    and len(row["Datum Probenentnahme"]) > 0
                                                ):
                                                    days_service = self.compute_days_in_service(
                                                        row["Datum Probenentnahme"],
                                                        row["Datum letzter Ölwechsel"],
                                                    )
                                                    if days_service > 0 and len(row[paramy]) > 0:                                                    
                                                        x2.append(days_service)
                                                        y2.append(float(row[paramy]))
                                                        j += 1
                                            elif len(row["Einfülltage"]) > 0 and len(row[paramy]) > 0:
                                                x2.append(int(row["Einfülltage"]))
                                                y2.append(float(row[paramy]))
                                                j += 1
                                        elif self.keys_exist(paramx, paramy) and len(row[paramx]) > 0 and len(row[paramy]) > 0:
                                            x2.append(float(row[paramx]))
                                            y2.append(float(row[paramy]))
                                            j += 1

                                        # if all of the points of the series have been already included                                      
                                        if j == nop:
                                            # increase the number of series k and the next series to be plotted l                                       
                                            k += 1
                                            machine_id1 = machine_id
                                            first_done = True
                                            l += 1                                            
                                # if l < k, first_done should be false and it would not go through the following elif
                                elif not second_done:
                                    if paramx == "time":
                                        if not ("Einfülltage" in self.keys):
                                            if (
                                                len(row["Datum letzter Ölwechsel"]) > 0
                                                and len(row["Datum Probenentnahme"]) > 0
                                            ):
                                                days_service = self.compute_days_in_service(
                                                    row["Datum Probenentnahme"],
                                                    row["Datum letzter Ölwechsel"],
                                                )
                                                if days_service > 0 and len(row[paramy]) > 0:
                                                    x3.append(days_service)
                                                    y3.append(float(row[paramy]))
                                                    j += 1
                                        elif len(row["Einfülltage"]) > 0 and len(row[paramy]) > 0:
                                            x3.append(int(row["Einfülltage"]))
                                            y3.append(float(row[paramy]))
                                            j += 1
                                    elif self.keys_exist(paramx, paramy) and len(row[paramx]) > 0 and len(row[paramy]) > 0:
                                            x3.append(float(row[paramx]))
                                            y3.append(float(row[paramy]))
                                            j += 1                                        
                                    if j == nop:
                                        k += 1
                                        l += 1
                                        machine_id2 = machine_id
                                        second_done = True
                                if l <= k:
                                   
                                    # add to x1, y1, increase j, if it is the case l but not k 
                                    if paramx == "time":
                                        if not ("Einfülltage" in self.keys):  
                                            #print(i, (data[i])[a], nop)     
                                                                            
                                            if (
                                                len(row["Datum letzter Ölwechsel"]) > 0
                                                and len(row["Datum Probenentnahme"]) > 0
                                            ):
                                                
                                                days_service = self.compute_days_in_service(
                                                    row["Datum Probenentnahme"],
                                                    row["Datum letzter Ölwechsel"],
                                                )
                                                #print(i+s, l, k, j, nop, row["Datum Probenentnahme"], row["Datum letzter Ölwechsel"], days_service)
                                                if days_service > 0 and len(row[paramy]) > 0:
                                                    #print(i+s, l, k, j, nop)                                                 
                                                    x1.append(days_service)
                                                    y1.append(float(row[paramy]))
                                                    j += 1
                                                #print(j, (data[i])[a])
                                        elif len(row["Einfülltage"]) > 0 and len(row[paramy]) > 0:
                                            x1.append(int(row["Einfülltage"]))
                                            y1.append(float(row[paramy]))
                                            j += 1
                                    elif self.keys_exist(paramx, paramy) and len(row[paramx]) > 0 and len(row[paramy]) > 0:
                                            x1.append(float(row[paramx]))
                                            y1.append(float(row[paramy]))
                                            j += 1        
                                    if j == nop:                                    
                                        l += 1                                   
                                                                   

                                # s increases even if the point is not going to be plotted         
                                s += 1        
                            i += s
                            #print(i)
                            if i < len(data):
                                ok2 = True
                                while (data[i])[a] == machine_id and ok2:                            
                                    i += 1
                                    if not (i < len(data)):
                                        ok2 = False
                        # If 2 series have already been added or there are not enough points from a series,
                        # the rest of points are plotted black
                        else:    
                            if paramx == "time":                        
                                if not ("Einfülltage" in self.keys):
                                    if (
                                        len((data[i])["Datum letzter Ölwechsel"]) > 0
                                        and len((data[i])["Datum Probenentnahme"]) > 0
                                    ):                                
                                        days_service = self.compute_days_in_service(
                                            (data[i])["Datum Probenentnahme"],
                                            (data[i])["Datum letzter Ölwechsel"],
                                        )
                                        if days_service > 0 and len((data[i])[paramy]) > 0:
                                            x1.append(days_service)
                                            y1.append(float((data[i])[paramy]))
                                elif len((data[i])["Einfülltage"]) > 0 and len(data[i][paramy]) > 0:
                                    x1.append(int((data[i])["Einfülltage"]))
                                    #print((data[i])[a], (data[i])[param])
                                    y1.append(float((data[i])[paramy]))
                            elif self.keys_exist(paramx, paramy) and len(row[paramx]) > 0 and len(row[paramy]) > 0:
                                    x1.append(float(row[paramx]))
                                    y1.append(float(row[paramy]))                                           
                            #print((data[i])[a], l)    
                            i += 1
                    else:
                        i += 1        
                            
                # plot
                #print(x2, y2)
                
                if (machine_id1 != "" or machine_id2 != "") and len(x1) > 16:
                    #fig, ax = plt.subplots()
                    fig = plt.figure(figsize=(6, 6))
                    #gs = fig.add_gridspec(1, 2, width_ratios=(4, 1),
                     # left=0.1, right=0.9, bottom=0.1, top=0.9,
                      #wspace=0.05, hspace=0.05)
                    if paramx == "time":  
                        gs = fig.add_gridspec(1, 2, width_ratios=(4, 1),
                        left=0.15, right=0.85, bottom=0.1, top=0.9,
                        wspace=0.05, hspace=0.05)
                        ax = fig.add_subplot(gs[0, 0])                    
                        ax_histy = fig.add_subplot(gs[0, 1], sharey=ax)  
                        ax_histy.tick_params(axis="y", labelleft=False)

                    else:
                        gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                        left=0.15, right=0.85, bottom=0.1, top=0.9,
                        wspace=0.05, hspace=0.05)
                        ax = fig.add_subplot(gs[1, 0])                    
                        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)  
                        ax_histy.tick_params(axis="y", labelleft=False)
                        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
                        ax_histx.tick_params(axis="x", labelbottom=False)
    
                        


                    ax.plot(x1, y1, "ko")
                    ax.plot(x2, y2, "go")
                    ax.plot(x3, y3, "mo")

                    ylabelstr = ""
                    xlabelstr = "Days in service"

                    if paramx != "time":
                        if paramx == "Wasser K. F." or paramx == "Viskosität bei 40°C" or paramx == "Viskosität bei 100°C":
                            binwidthx = round((np.max(np.abs(x1)) - np.min(np.abs(x1))) / round(Decimal(len(x1)).sqrt()))
                        else:     
                            binwidthx = (np.max(np.abs(x1)) - np.min(np.abs(x1))) / round(Decimal(len(x1)).sqrt())
                    
                    if paramy == "Wasser K. F." or paramy == "Viskosität bei 40°C" or paramy == "Viskosität bei 100°C":
                        binwidthy = round((np.max(np.abs(y1)) - np.min(np.abs(y1))) / round(Decimal(len(x1)).sqrt()))
                    else:     
                        binwidthy = (np.max(np.abs(y1)) - np.min(np.abs(y1))) / round(Decimal(len(x1)).sqrt())

                    save_name = ""
                    xax = "days"
                    ax.set_xlim(-50, 4000)

                    match paramx:
                        case "Wasser K. F.":
                            xlabelstr = "Water K.F. in ppm"                            
                            ax.set_xlim(0, 1000)
                            if len(x1) > 150:
                                binwidthx = 25
                            else:
                                binwidthx = 50
                        case "Neutralisationszahl":
                            xlabelstr = "Acid number in mgkOH/gOil"                            
                            ax.set_xlim(0, 3)
                            if binwidthx < 0.15:
                                binwidthx = 0.15
                            #binwidth = 0.25
                        case "Oxidation":
                            xlabelstr = "Oxidation in A/cm"                            
                        case "Viskosität bei 40°C":
                            xlabelstr = "Viscosity at 40°C in mm^2/s"                            
                            ax.set_xlim(200, 400)                            
                            if len(x1) > 150:
                                binwidthx = 4
                            else:
                                binwidthx = 5      
                        case "Viskosität bei 100°C":
                            xlabelstr = "Viscosity at 100°C in mm^2/s"                            
                            ax.set_xlim(10, 75)                            
                            if len(x1) > 150:
                                binwidthx = 1
                            else:
                                binwidthx = 2
                        case "FE":
                            xlabelstr = "Fe content in ppm"                            
                            ax.set_xlim(0, 200)                            
                            if len(x1) > 150:
                                binwidthx = 2
                            else:
                                binwidthx = 3
                        case "P":
                            xlabelstr = "P content in ppm"                            
                            ax.set_xlim(0, 3000)                            
                            if len(x1) > 150:
                                binwidthx = 5
                            else:
                                binwidthx = 10   
                        case "Ölmenge im System":
                            xlabelstr = "Oil volume in L"                            
                            ax.set_xlim(0, 500)                                                     
                            binwidthx = 100 
                        case "Anlagengöße [kW]":
                            xlabelstr = "Power in kW"                            
                            ax.set_xlim(0, 4000)                                            
                            binwidthx = 50             

                    if paramx != "time":
                        xax = paramx.replace(".", "").replace("°C", "").replace("bei","")

                    match paramy:
                        case "Wasser K. F.":
                            ylabelstr = "Water K.F. in ppm"
                            save_name = (
                            f"H2O_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"
                            )                            
                            ax.set_ylim(0, 1000)
                            if len(x1) > 150:
                                binwidthy = 25
                            else:
                                binwidthy = 50
                        case "Neutralisationszahl":
                            ylabelstr = "Acid number in mgkOH/gOil"                            
                            ax.set_ylim(0, 3)
                            save_name = f"AN_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"
                            if binwidthy < 0.15:
                                binwidthy = 0.15
                            #binwidth = 0.25
                        case "Oxidation":
                            ylabelstr = "Oxidation in A/cm"
                            save_name = f"Ox_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"
                        case "Viskosität bei 40°C":
                            ylabelstr = "Viscosity at 40°C in mm^2/s"
                            if paramx == "time":
                                ax.set_xlim(-50, 3000)
                            ax.set_ylim(200, 400)
                            save_name = f"v40_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"
                            if len(x1) > 150:
                                binwidthy = 4
                            else:
                                binwidthy = 5      
                        case "Viskosität bei 100°C":
                            ylabelstr = "Viscosity at 100°C in mm^2/s"
                            if paramx == "time":
                                ax.set_xlim(-50, 3000)
                            ax.set_ylim(10, 75)
                            save_name = f"v100_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"
                            if len(x1) > 150:
                                binwidthy = 1
                            else:
                                binwidthy = 2  
                        case "FE":
                            ylabelstr = "Fe content in ppm"                            
                            ax.set_ylim(0, 200)         
                            save_name = f"Fe_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"                   
                            if len(x1) > 150:
                                binwidthy = 2
                            else:
                                binwidthy = 3   
                        case "P":
                            ylabelstr = "P content in ppm"                            
                            ax.set_ylim(0, 3000)         
                            save_name = f"P_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"                   
                            if len(x1) > 150:
                                binwidthy = 5
                            else:
                                binwidthy = 10   
                        case "Ölmenge im System":
                            ylabelstr = "Oil volume in L"                            
                            ax.set_ylim(0, 500)         
                            save_name = f"Oilvol_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"                   
                            binwidthy = 100                             
                        case "Anlagengöße [kW]":
                            ylabelstr = "Power in kW"                            
                            ax.set_ylim(0, 4000)         
                            save_name = f"Power_vs_{xax}_{machine_id1}_{machine_id2}_{oil_name}.png"                   
                            binwidthy = 50
                            
                    print("binwidthy:", binwidthy)
                    #xymax = max(np.max(np.abs(x1)), np.max(np.abs(y1)))
                    ymax = np.max(np.abs(y1))
                    #lim = (int(xymax/binwidthy) + 1) * binwidthy
                    lim = (int(ymax/binwidthy) + 1) * binwidthy

                    bins = np.arange(-lim, lim + binwidthy, binwidthy)
                    
                    ax_histy.hist(y1, bins=bins, orientation='horizontal')

                    if paramx != "time":                        
                        xmax = np.max(np.abs(x1))
                        lim = (int(xmax/binwidthx) + 1) * binwidthx
                        bins = np.arange(-lim, lim + binwidthx, binwidthx)                    
                        ax_histx.hist(x1, bins=bins)
                        ax_histx.set_title(f"{oil_name}, {len(x1)+len(x2)+len(x3)} points")

                    
                    #plt.title(f"{oil_name}, {len(x1)+len(x2)+len(x3)} points")
                    if  paramx == "time":
                        ax.set_title(f"{oil_name}, {len(x1)+len(x2)+len(x3)} points")

                    path_proj = os.path.abspath(os.getcwd())
                    
                    ax.set_xlabel(xlabelstr)
                    ax.set_ylabel(ylabelstr)

                     # winter_patch = mpatches.Patch(color='blue', label='Winter')
                    A_point = mlines.Line2D(
                        [],
                        [],
                        linewidth=0,
                        color="green",
                        marker="o",
                        markersize=7,
                        label="Machine id: A",
                    )
                    # spring_patch = mpatches.Patch(color='green', label='Spring')
                    B_point = mlines.Line2D(
                        [],
                        [],
                        linewidth=0,
                        color="m",
                        marker="o",
                        markersize=7,
                        label="Machine id: B",
                    )
                    ax.legend(
                        handles=[A_point, B_point]
                    )

                    save_name = self.validate_file_name(save_name)
                    match paramy:
                        case "Wasser K. F.":                    
                            #plt.savefig(f"{path_proj}/project/data/water_KF/ind_samples/{save_name}")
                            plt.savefig(f"data/water_KF/ind_samples/{save_name}")
                        case "Neutralisationszahl":
                            plt.savefig(f"data/AN/ind_samples/{save_name}")
                        case "Oxidation":
                            plt.savefig(f"data/ox/ind_samples/{save_name}")
                        case "Viskosität bei 40°C":
                            plt.savefig(f"data/viscosity/40/{save_name}")
                        case "Viskosität bei 100°C":
                            plt.savefig(f"data/viscosity/100/{save_name}")   
                        case "FE":
                            plt.savefig(f"data/elements/Fe/{save_name}")  
                        case "P":
                            plt.savefig(f"data/elements/P/{save_name}")
                        case "Ölmenge im System" | "Anlagengöße [kW]":
                            plt.savefig(f"data/machine/{save_name}")          
                    plt.close(fig)

                elif machine_id1 == "" and machine_id2 == "":
                    ok1 = False

