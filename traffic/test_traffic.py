from traffic import load_data
import os

def test_load_data():
    dir_name = "gtsrb"
    path_proj = os.path.abspath(os.getcwd())
    l = [str(x) for x in range(43)]
    l1 = [f"{path_proj}/{dir_name}/{str(x)}" for x in range(43)]
    l.sort()
    l1.sort()
    assert (load_data(dir_name)[0] == l1 and load_data(dir_name)[1] == l)
