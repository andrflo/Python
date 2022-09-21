import csv
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from datetime import date, time, datetime


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
                fig, ax = plt.subplots()
                ax.plot(d1["x_values"], d1["y_values"], "mo")
                for d2 in ldspring:
                    if d2["oil_name"] == noil:
                        npoints += len(d2["x_values"])
                        ax.plot(d2["x_values"], d2["y_values"], "go")
                        for d3 in ldwinter:
                            if d3["oil_name"] == noil:
                                npoints += len(d3["x_values"])
                                ax.plot(d3["x_values"], d3["y_values"], "bo")
                                for d4 in ldsummer:
                                    if d4["oil_name"] == noil:
                                        npoints += len(d4["x_values"])
                                        ax.plot(d4["x_values"], d4["y_values"], "ro")
                plt.title(f"Season: all, {noil}, {npoints} points")
                if p == "Wasser K. F.":
                    plt.ylabel("Water K.F. in ppm")
                    save_name = f"H2O_vs_days_all_{noil}.png"
                elif p == "Neutralisationszahl":
                    plt.ylabel("Acid number in mgkOH/gOil")
                    save_name = f"AN_vs_days_all_{noil}.png"
                elif p == "Oxidation":
                    plt.ylabel("Oxidation in A/cm")
                    save_name = f"Ox_vs_days_all_{noil}.png"
                plt.xlabel("Days in service")

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

    def sort_by_param(self, param, oil_names):

        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            short_ds = []
            for oil_name in oil_names:
                for row1 in reader:
                    if row1["Ölbezeichnung"] == oil_name:
                        short_ds.append(row1)                        
            #return sorted(short_ds, key=lambda row: (row[param]))
            return sorted(float(row[param]) for row in short_ds)

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

    def plot_data_machine(self, param):

        oil_names = self.set_of_oils("wind turbine", "all_seasons", param)
        
        if self.keys_exist("Anlagennummer"):
            a = "Anlagennummer"
        elif self.keys_exist("Probenbezeichnung"):
            a = "Probenbezeichnung"    
        if self.keys_exist(a):
            data = self.sort_by_param(a, oil_names)

        print ("l oils:", len(oil_names), "l data:", len(data))    

        set_of_ids = set()
        for row in data:
            set_of_ids.add(row[a])

        n_el = []
        list_of_ids = []
        i = 0

        ok = True
        while i < len(data) and ok:
            machine_id = (data[i])[a]
            j = i
            k = 0
            while (data[j])[a] == machine_id and ok:

                if j + 1 < len(data):
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
            while k < n_sa:
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
                            while j < nop:
                                #print(i+s, l, k, j, nop)
                                row = data[i + s]
                                if not first_done:
                                    
                                    # Fill up x2 y2 only if the data has not been plotted before
                                    if l > k:
                                        # j increases only when the point is included to be plotted
                                        if not ("Einfülltage" in self.keys):
                                            if (
                                                len(row["Datum letzter Ölwechsel"]) > 0
                                                and len(row["Datum Probenentnahme"]) > 0
                                            ):
                                                days_service = self.compute_days_in_service(
                                                    row["Datum Probenentnahme"],
                                                    row["Datum letzter Ölwechsel"],
                                                )
                                                if days_service > 0 and len(row[param]) > 0:                                                    
                                                    x2.append(days_service)
                                                    y2.append(float(row[param]))
                                                    j += 1
                                        elif len(row["Einfülltage"]) > 0 and len(row[param]) > 0:
                                            x2.append(int(row["Einfülltage"]))
                                            y2.append(float(row[param]))
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
                                    if not ("Einfülltage" in self.keys):
                                        if (
                                            len(row["Datum letzter Ölwechsel"]) > 0
                                            and len(row["Datum Probenentnahme"]) > 0
                                        ):
                                            days_service = self.compute_days_in_service(
                                                row["Datum Probenentnahme"],
                                                row["Datum letzter Ölwechsel"],
                                            )
                                            if days_service > 0 and len(row[param]) > 0:
                                                x3.append(days_service)
                                                y3.append(float(row[param]))
                                                j += 1
                                    elif len(row["Einfülltage"]) > 0 and len(row[param]) > 0:
                                        x3.append(int(row["Einfülltage"]))
                                        y3.append(float(row[param]))
                                        j += 1                                
                                    if j == nop:
                                        k += 1
                                        l += 1
                                        machine_id2 = machine_id
                                        second_done = True
                                if l <= k:
                                   
                                    # add to x1, y1, increase j, if it is the case l but not k 
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
                                            if days_service > 0 and len(row[param]) > 0:
                                                #print(i+s, l, k, j, nop)                                                 
                                                x1.append(days_service)
                                                y1.append(float(row[param]))
                                                j += 1
                                            #print(j, (data[i])[a])
                                    elif len(row["Einfülltage"]) > 0 and len(row[param]) > 0:
                                        x1.append(int(row["Einfülltage"]))
                                        y1.append(float(row[param]))
                                        j += 1
                                    if j == nop:                                    
                                        l += 1
                                        
                                    
                                    

                                # s increases even if the point is not going to be plotted         
                                s += 1        
                            i += s
                            #print(i)
                            while (data[i])[a] == machine_id:                            
                                i += 1
                        # If 2 series have already been added or there are not enough points for a series,
                        # the rest of points are plotted black
                        else:                            
                            if not ("Einfülltage" in self.keys):
                                if (
                                    len((data[i])["Datum letzter Ölwechsel"]) > 0
                                    and len((data[i])["Datum Probenentnahme"]) > 0
                                ):                                
                                    days_service = self.compute_days_in_service(
                                        (data[i])["Datum Probenentnahme"],
                                        (data[i])["Datum letzter Ölwechsel"],
                                    )
                                    if days_service > 0 and len((data[i])[param]) > 0:
                                        x1.append(days_service)
                                        y1.append(float((data[i])[param]))
                            elif len((data[i])["Einfülltage"]) > 0 and len(data[i][param]) > 0:
                                x1.append(int((data[i])["Einfülltage"]))
                                #print((data[i])[a], (data[i])[param])
                                y1.append(float((data[i])[param]))
                            #print((data[i])[a], l)    
                            i += 1
                    else:
                        i = i+1        
                            
                # plot
                #print(x2, y2)
                fig, ax = plt.subplots()
                ax.plot(x1, y1, "ko")
                ax.plot(x2, y2, "go")
                ax.plot(x3, y3, "mo")
                plt.title(f"{oil_name}, {len(x1)+len(x2)+len(x3)} points")
                if param == "Wasser K. F.":
                    plt.ylabel("Water K.F. in ppm")
                    save_name = (
                        f"H2O_vs_days_{machine_id1}_{machine_id2}_{oil_name}.png"
                    )
                elif param == "Neutralisationszahl":
                    plt.ylabel("Acid number in mgkOH/gOil")
                    save_name = f"AN_vs_days_{machine_id1}_{machine_id2}_{oil_name}.png"
                elif param == "Oxidation":
                    plt.ylabel("Oxidation in A/cm")
                    save_name = f"Ox_vs_days_{machine_id1}_{machine_id2}_{oil_name}.png"
                plt.xlabel("Days in service")

                save_name = self.validate_file_name(save_name)
                if param == "Wasser K. F.":
                    plt.savefig(f"data/water_KF/ind_samples/{save_name}")
                elif param == "Neutralisationszahl":
                    plt.savefig(f"data/AN/ind_samples/{save_name}")
                elif param == "Oxidation":
                    plt.savefig(f"data/ox/ind_samples/{save_name}")
                plt.close(fig)

