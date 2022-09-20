from dataset import Dataset

def test_keys_exist():
    fn1 = "dataset1.csv"
    ds = Dataset(fn1)
    assert ds.keys_exist("Anlagennummer")