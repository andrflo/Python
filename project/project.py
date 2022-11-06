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
fn4 = os.path.join(path_proj, "dataset4.csv")  # dataset3 without the data poin of dataset5
fn5 = os.path.join(path_proj, "dataset5.csv")  # dataset4 + dataset5 = dataset3
fn6 = os.path.join(path_proj, "dataset6.csv")
fn7 = os.path.join(path_proj, "dataset7.csv")
fn8 = os.path.join(path_proj, "dataset8.csv")
fn9 = os.path.join(path_proj, "dataset9.csv")
fn10 = os.path.join(path_proj, "dataset10.csv")


fn_list = [fn8, fn10]


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

    identifyWindTurbineOil(ds_list[0], ds_list[1])

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
                            int(row["Schwefelgehalt"])
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
    model.evaluate(x_test,  y_test, verbose=2)

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
                            int(row["Schwefelgehalt"])
                        ]
                    )

    
    y_pred = np.argmax(model.predict(el_array_datapoint), axis=-1)
    #print(oil_name_int)
    response = "?"
    for o in oil_name_int:
        if oil_name_int[o] == y_pred[0]:
            response = o
    print("The oil is most likely", response)


def get_model_idOil(numOils):
    # Create a neural network
    model = tf.keras.models.Sequential([   

        # Add a hidden layer with x units, with ReLU activation
        tf.keras.layers.Dense(256, input_shape=(8,), activation="sigmoid"),           

        # Add a hidden layer 
        tf.keras.layers.Dense(64, activation="sigmoid"),  

        # Add a hidden layer 
        tf.keras.layers.Dense(64, activation="sigmoid"),  
            
        # Add an output layer with NUM_CATEGORIES output units
        tf.keras.layers.Dense(numOils, activation="softmax")
    ])

    # Train neural network
    model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
    )
    return model



if __name__ == "__main__":
    main()
