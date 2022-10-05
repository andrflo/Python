from dataset import Dataset

def test_keys_exist():
    fn1 = "dataset1.csv"
    ds = Dataset(fn1)
    assert ds.keys_exist("Anlagennummer", "Wasser K. F.")

def test_sort_by_param():
    fn3 = "dataset3.csv"
    ds = Dataset(fn3)
    oil_names = ds.set_of_oils("wind turbine", "all_seasons", "Viskosität bei 100°C")
    data = ds.sort_by_param("Probenbezeichnung", oil_names, "wind turbine")

    for row in data:
        print(row["Probenbezeichnung"])
