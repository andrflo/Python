import os
import csv
import numpy as np
from dataset import Dataset
from pdf import PDF
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
TEST_SIZE = 0.4


path_proj = os.path.abspath(os.getcwd())
fn1 = os.path.join(path_proj, "dataset1.csv")
fn2 = os.path.join(path_proj, "dataset2.csv")
# fn3 = f"{path_proj}/project/dataset3.csv"
fn3 = os.path.join(path_proj, "dataset3.csv")
fn4 = os.path.join(
    path_proj, "dataset4.csv"
)  # dataset3 without the data poin of dataset5
fn5 = os.path.join(path_proj, "dataset5.csv")  # dataset4 + dataset5 = dataset3
fn6 = os.path.join(path_proj, "dataset6.csv")
fn7 = os.path.join(path_proj, "dataset7.csv")
fn8 = os.path.join(path_proj, "dataset8.csv")
fn9 = os.path.join(path_proj, "dataset9.csv")
fn10 = os.path.join(path_proj, "dataset10.csv")
fn11 = os.path.join(path_proj, "dataset11.csv")
fn12 = os.path.join(path_proj, "dataset12.csv")
fn13 = os.path.join(path_proj, "dataset13.csv")
fn14 = os.path.join(path_proj, "dataset14.csv")

fn_list = [fn11, fn12]


def main():
    ds_list = []
    for fn in fn_list:
        ds = Dataset(fn)
        ds_list.append(ds)
        # ds.plot_param_t_all_seasons("Wasser K. F.")
        # ds.plot_param_t_all_seasons("Neutralisationszahl")
        # ds.plot_param_t_all_seasons("Oxidation")
        # ds.plot_param_t("all_seasons", "Wasser K. F.")
        # ds.plot_param_gral_ev(3, "Neutralisationszahl")
        # ds.plot_param_gral_ev_all("Neutralisationszahl")
        # ds.plot_param_gral_ev_all("Wasser K. F.")
        # ds.plot_data_machine("time", "Wasser K. F.")
        # ds.plot_data_machine("time", "Viskosität bei 40°C")
        # ds.plot_data_machine("time", "Viskosität bei 100°C")
        # ds.plot_data_machine("time", "FE")
        # ds.plot_data_machine("time", "P")
        # ds.plot_data_machine("FE", "Neutralisationszahl")
        # ds.plot_data_machine("CU", "Neutralisationszahl")
        # ds.plot_data_machine("Neutralisationszahl")
        # ds.plot_data_machine("Anlagengöße [kW]", "Ölmenge im System")

    # identifyWindTurbineOil(ds_list[0], ds_list[1])
    trafficLightIndication(ds_list[0], ds_list[1])

    p1 = "H2O_vs_days_all"
    p2 = "AN_vs_days_all"
    p3 = "Ox_vs_days_all"
    p4 = "H2O_vs_days_all_seasons"
    # generate_PDFreport(p4)


def generate_PDFreport(p):

    match p:
        case "H2O_vs_days_all" | "H2O_vs_days_all_seasons":
            l = list_files_pattern("data/water_KF", p)
            if len(l) > 0:
                generate_report_param(p, l)

        case "AN_vs_days_all":
            l = list_files_pattern("data/AN", p)
            if len(l) > 0:
                generate_report_param(p, l)

        case "Ox_vs_days_all":
            l = list_files_pattern("data/ox", p)
            if len(l) > 0:
                generate_report_param(p, l)


def list_files_pattern(dir, pattern):
    lfiles = []
    entries = os.listdir(dir)
    path_proj = os.path.abspath(os.getcwd())
    for f in entries:
        if pattern in f:
            lfiles.append(f"{path_proj}/{dir}/{f}")
    return lfiles


def generate_report_param(p1, l1):

    pdf = PDF(orientation="P", unit="mm", format="A4")

    pdf.add_page()
    pdf.header(generate_header(p1))
    counter = 0

    path_proj = os.path.abspath(os.getcwd())
    deltax = 0
    deltay = 0

    # print(l1)
    for file in l1:
        print(file)
        pdf.image(file, x=10 + deltax, y=50 + deltay, w=pdf.epw / 2)
        counter += 1
        if counter % 4 == 0:
            pdf.add_page()
            pdf.header(generate_header(p1))
            deltax = 0
            deltay = 0
        elif counter % 2 == 0:
            deltax = 0
            deltay = 80
        elif counter % 2 == 1:
            deltax = pdf.epw / 2

    pdf.output(f"report_{p1}.pdf")


def generate_header(p):
    match p:
        case "H2O_vs_days_all" | "H2O_vs_days_all_seasons":
            return "Water content in ppm according to Karl-Fischer test, oil samples from wind turbines, all seasons"
        case "AN_vs_days_all":
            return (
                "Acid number in mgkOH/gOil, oil samples from wind turbines, all seasons"
            )
        case "Ox_vs_days_all":
            return "Oxidation in A/cm, oil samples from wind turbines, all seasons"


def identifyWindTurbineOil(dataset, dataoil):
    # returns the oil name given data oil and dataset
    # data oil specifies the content of Ca, Mg, B, Zn, Mo, P, Ba, S in the oil sample
    # data set has information of the element content of multiple oils
    el_array_ds = []
    oil_name_int = dict()
    label_array_ds = []
    numoils = 0

    with open(dataset.filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        if dataset.keys_exist(
            "CA", "MG", "B", "ZN", "MO", "P", "BA", "Schwefelgehalt", "Ölbezeichnung"
        ):
            oil_names = dataset.set_of_oils(
                "wind", "all seasons", "P"
            )  # set of wind turbine oils
            numoils = len(oil_names)
            oil_name_int = dict(
                zip(sorted(list(oil_names)), [x for x in range(len(oil_names))])
            )
            for row in reader:
                if (
                    row["Ölbezeichnung"] in oil_names
                    and row["CA"].isnumeric()
                    and row["MG"].isnumeric()
                    and row["B"].isnumeric()
                    and row["ZN"].isnumeric()
                    and row["MO"].isnumeric()
                    and row["P"].isnumeric()
                    and row["BA"].isnumeric()
                    and row["Schwefelgehalt"].isnumeric()
                ):
                    el_array_ds.append(
                        [
                            int(row["CA"]),
                            int(row["MG"]),
                            int(row["B"]),
                            int(row["ZN"]),
                            int(row["MO"]),
                            int(row["P"]),
                            int(row["BA"]),
                            int(row["Schwefelgehalt"]),
                        ]
                    )
                    label_array_ds.append(oil_name_int[row["Ölbezeichnung"]])
                   
    # Split data into training and testing sets
    label_array_ds = tf.keras.utils.to_categorical(label_array_ds)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(el_array_ds), np.array(label_array_ds), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model_idOil(numoils)

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    el_array_datapoint = []

    with open(dataoil.filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        if dataoil.keys_exist(
            "CA", "MG", "B", "ZN", "MO", "P", "BA", "Schwefelgehalt", "Ölbezeichnung"
        ):
            for row in reader:
                if (
                    row["CA"].isnumeric()
                    and row["MG"].isnumeric()
                    and row["B"].isnumeric()
                    and row["ZN"].isnumeric()
                    and row["MO"].isnumeric()
                    and row["P"].isnumeric()
                    and row["BA"].isnumeric()
                    and row["Schwefelgehalt"].isnumeric()
                ):
                    el_array_datapoint.append(
                        [
                            int(row["CA"]),
                            int(row["MG"]),
                            int(row["B"]),
                            int(row["ZN"]),
                            int(row["MO"]),
                            int(row["P"]),
                            int(row["BA"]),
                            int(row["Schwefelgehalt"]),
                        ]
                    )

    y_pred = np.argmax(model.predict(el_array_datapoint), axis=-1)
    # print(oil_name_int)
    response = "?"
    for o in oil_name_int:
        if oil_name_int[o] == y_pred[0]:
            response = o
    print("The oil is most likely", response)


def get_model_idOil(numOils):
    # Create a neural network
    model = tf.keras.models.Sequential(
        [
            # Add a hidden layer with x units, with ReLU activation
            tf.keras.layers.Dense(256, input_shape=(8,), activation="sigmoid"),
            # Add a hidden layer
            tf.keras.layers.Dense(64, activation="sigmoid"),
            # Add a hidden layer
            tf.keras.layers.Dense(64, activation="sigmoid"),
            # Add an output layer with NUM_CATEGORIES output units
            tf.keras.layers.Dense(numOils, activation="softmax"),
        ]
    )

    # Train neural network
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def trafficLightIndication(dataset, dataoil):
    # returns traffic light indication according to oil condition parameters of sample (dataoil)
    # Dataset contains oil condition parameters of several oil samples and the corresponding traffic light indication
    # 1: good condition, 3: bad condition
    # The training of the model is performed only with oils of the same type (known)
    # The traffic light indication is based on the following parameters:
    # Fe, Cr, Sn, Al, Ni, Cu, Pb, Mo, Si, K, Na, Viskosität bei 40°C, Viskosität bei 100°C, Oxidation,
    # Ca, Mg, B, Zn, P, Ba, Schwefelgehalt, Neutralisationszahl, >4µm (ISO), >6µm (ISO), >14µm (ISO), Wasser K.F., time in service

    param_array_ds = []
    label_array_ds = []
    numstates = 3
    oil_name = ""

    param_array_datapoint = []

    with open(dataoil.filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        if dataoil.keys_exist(
            "FE",
            "CR",
            "SN",
            "AL",
            "NI",
            "CU",
            "PB",
            "SI",
            "K",
            "NA",
            "Viskosität bei 40°C",
            "Viskosität bei 100°C",
            "Oxidation",
            "CA",
            "MG",
            "B",
            "ZN",
            "MO",
            "P",
            "BA",
            "Schwefelgehalt",
            "Ölbezeichnung",
            "Neutralisationszahl",
            ">4µm (ISO)",
            ">6µm (ISO)",
            ">14µm (ISO)",
            "Wasser K. F.",
            "Datum Probenentnahme",
        ) and (
            dataoil.keys_exist("Datum letzter Ölwechsel", "Datum Probenentnahme")
            or dataoil.keys_exist("Einfülltage")
        ):            
            
            for row in reader:
                days_service = 0                
                if dataoil.keys_exist("Einfülltage"):
                    if len(row["Einfülltage"]) > 0:
                        days_service = int(row["Einfülltage"])
                if days_service == 0 and dataoil.keys_exist(
                    "Datum letzter Ölwechsel", "Datum Probenentnahme"
                ):
                    if (
                        len(row["Datum letzter Ölwechsel"]) > 0
                        and len(row["Datum Probenentnahme"]) > 0
                    ):
                        days_service = dataoil.compute_days_in_service(
                            row["Datum Probenentnahme"],
                            row["Datum letzter Ölwechsel"],
                        )                       
                print("days service", days_service)
                if (
                    days_service > 0
                    and row["FE"].isnumeric()
                    and row["CR"].isnumeric()
                    and row["SN"].isnumeric()
                    and row["AL"].isnumeric()
                    and row["NI"].isnumeric()
                    and row["CU"].isnumeric()
                    and row["PB"].isnumeric()
                    and row["SI"].isnumeric()
                    and row["K"].isnumeric()
                    and row["NA"].isnumeric()
                    and row["Viskosität bei 40°C"] != ""
                    and row["Viskosität bei 100°C"] != ""
                    and row["Oxidation"].isnumeric()
                    and row["CA"].isnumeric()
                    and row["MG"].isnumeric()
                    and row["B"].isnumeric()
                    and row["ZN"].isnumeric()
                    and row["MO"].isnumeric()
                    and row["P"].isnumeric()
                    and row["BA"].isnumeric()
                    and row["Schwefelgehalt"].isnumeric()
                    and row["Ölbezeichnung"] != ""
                    and row["Datum Probenentnahme"] != ""
                    and row["Neutralisationszahl"] != ""
                    and row[">4µm (ISO)"].isnumeric()
                    and row[">6µm (ISO)"].isnumeric()
                    and row[">14µm (ISO)"].isnumeric()
                    and row["Wasser K. F."].isnumeric()
                ):                    
                    oil_name = row["Ölbezeichnung"]
                    param_array_datapoint.append(
                        [
                            int(row["FE"]),
                            int(row["CR"]),
                            int(row["SN"]),
                            int(row["AL"]),
                            int(row["NI"]),
                            int(row["CU"]),
                            int(row["PB"]),
                            int(row["SI"]),
                            int(row["K"]),
                            int(row["NA"]),
                            int(round(float(row["Viskosität bei 40°C"]), 0)),
                            int(round(float(row["Viskosität bei 100°C"]), 0)),
                            int(row["Oxidation"]),
                            int(row["CA"]),
                            int(row["MG"]),
                            int(row["B"]),
                            int(row["ZN"]),
                            int(row["MO"]),
                            int(row["P"]),
                            int(row["BA"]),
                            int(row["Schwefelgehalt"]),
                            float(row["Neutralisationszahl"]),
                            int(row[">4µm (ISO)"]),
                            int(row[">6µm (ISO)"]),
                            int(row[">14µm (ISO)"]),
                            int(row["Wasser K. F."]),
                            days_service,
                            dataoil.num_season(row["Datum Probenentnahme"]),
                        ]
                    )                    
    print(len(param_array_datapoint))
    with open(dataset.filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        if dataset.keys_exist(
            "FE",
            "CR",
            "SN",
            "AL",
            "NI",
            "CU",
            "PB",
            "SI",
            "K",
            "NA",
            "Viskosität bei 40°C",
            "Viskosität bei 100°C",
            "Oxidation",
            "CA",
            "MG",
            "B",
            "ZN",
            "MO",
            "P",
            "BA",
            "Schwefelgehalt",
            "Ölbezeichnung",
            "Neutralisationszahl",
            ">4µm (ISO)",
            ">6µm (ISO)",
            ">14µm (ISO)",
            "Wasser K. F.",
            "Gesamtbewertung",
            "Datum Probenentnahme",
        ) and (
            dataset.keys_exist("Datum letzter Ölwechsel", "Datum Probenentnahme")
            or dataset.keys_exist("Einfülltage")
        ):

            for row in reader:
                days_service = 0
                if dataset.keys_exist("Einfülltage"):
                    if len(row["Einfülltage"]) > 0:
                        days_service = int(row["Einfülltage"])
                if days_service == 0 and dataset.keys_exist(
                    "Datum letzter Ölwechsel", "Datum Probenentnahme"
                ):
                    if (
                        len(row["Datum letzter Ölwechsel"]) > 0
                        and len(row["Datum Probenentnahme"]) > 0
                    ):
                        days_service = dataset.compute_days_in_service(
                            row["Datum Probenentnahme"],
                            row["Datum letzter Ölwechsel"],
                        )
                if (
                    days_service > 0
                    and row["Ölbezeichnung"] == oil_name
                    and row["FE"].isnumeric()
                    and row["CR"].isnumeric()
                    and row["SN"].isnumeric()
                    and row["AL"].isnumeric()
                    and row["NI"].isnumeric()
                    and row["CU"].isnumeric()
                    and row["PB"].isnumeric()
                    and row["SI"].isnumeric()
                    and row["K"].isnumeric()
                    and row["NA"].isnumeric()
                    and row["Viskosität bei 40°C"] != ""
                    and row["Viskosität bei 100°C"] != ""
                    and row["Oxidation"].isnumeric()
                    and row["CA"].isnumeric()
                    and row["MG"].isnumeric()
                    and row["B"].isnumeric()
                    and row["ZN"].isnumeric()
                    and row["MO"].isnumeric()
                    and row["P"].isnumeric()
                    and row["BA"].isnumeric()
                    and row["Schwefelgehalt"].isnumeric()
                    and row["Neutralisationszahl"] != ""
                    and row[">4µm (ISO)"].isnumeric()
                    and row[">6µm (ISO)"].isnumeric()
                    and row[">14µm (ISO)"].isnumeric()
                    and row["Wasser K. F."].isnumeric()
                    and row["Gesamtbewertung"].isnumeric()
                    and row["Datum Probenentnahme"] != ""
                ):
                    param_array_ds.append(
                        [
                            int(row["FE"]),
                            int(row["CR"]),
                            int(row["SN"]),
                            int(row["AL"]),
                            int(row["NI"]),
                            int(row["CU"]),
                            int(row["PB"]),
                            int(row["SI"]),
                            int(row["K"]),
                            int(row["NA"]),
                            int(round(float(row["Viskosität bei 40°C"]), 0)),
                            int(round(float(row["Viskosität bei 100°C"]), 0)),
                            int(row["Oxidation"]),
                            int(row["CA"]),
                            int(row["MG"]),
                            int(row["B"]),
                            int(row["ZN"]),
                            int(row["MO"]),
                            int(row["P"]),
                            int(row["BA"]),
                            int(row["Schwefelgehalt"]),
                            float(row["Neutralisationszahl"]),
                            int(row[">4µm (ISO)"]),
                            int(row[">6µm (ISO)"]),
                            int(row[">14µm (ISO)"]),
                            int(row["Wasser K. F."]),
                            days_service,
                            dataset.num_season(row["Datum Probenentnahme"]),
                        ]
                    )
                    label_array_ds.append(int(row["Gesamtbewertung"])-1)
    
    count1= 0
    count2= 0
    count3= 0  
    for l in label_array_ds:
        if l==0:
            count1 += 1
        elif l==1:
            count2 += 1
        elif l==2:
            count3 += 1   
    print("count1", count1)
    print("count2", count2)
    print("count3", count3)

    # Split data into training and testing sets
    label_array_ds = tf.keras.utils.to_categorical(label_array_ds)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(param_array_ds), np.array(label_array_ds), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model_traffic_light(numstates)

    print(len(x_train), len(y_train))

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    y_pred = np.argmax(model.predict(param_array_datapoint), axis=-1)
      
    print("Traffic light indication: ", y_pred[0]+1)
    
def get_model_traffic_light(numstates):
    # Create a neural network
    model = tf.keras.models.Sequential(
        [
            # Add a hidden layer with x units, with ReLU activation
            tf.keras.layers.Dense(256, input_shape=(28,), activation="sigmoid"),
            # Add a hidden layer
            tf.keras.layers.Dense(64, activation="sigmoid"),
            # Add a hidden layer
            tf.keras.layers.Dense(64, activation="sigmoid"),
            # Add an output layer with NUM_CATEGORIES output units
            tf.keras.layers.Dense(numstates, activation="softmax"),
        ]
    )

    # Train neural network
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model

if __name__ == "__main__":
    main()
