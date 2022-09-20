import os
from dataset import Dataset
from pdf import PDF


fn1 = "dataset1.csv"
fn2 = "dataset2.csv"
fn3 = "dataset3.csv"

fn_list = [fn3, fn1, fn2]

def main():
    ds_list = []
    for fn in fn_list:
        ds = Dataset(fn)
        ds_list.append(ds)
        ds.plot_param_t_all_seasons("Wasser K. F.")
        ds.plot_param_t_all_seasons("Neutralisationszahl")
        ds.plot_param_t_all_seasons("Oxidation")
    generate_PDFreport()


def generate_PDFreport():
    p1 = "H2O_vs_days_all"
    p2 = "AN_vs_days_all"
    p3 = "Ox_vs_days_all"

    l1 = list_files_pattern("data/water_KF", p1)
    if len(l1) > 0:
        generate_report_param(p1, l1)

    l2 = list_files_pattern("data/AN", p2)
    if len(l2) > 0:
        generate_report_param(p2, l2)

    l3 = list_files_pattern("data/ox", p3)
    if len(l3) > 0:
        generate_report_param(p3, l3)


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

    #print(l1)
    for file in l1:
        print(file)
        pdf.image(file, x=10+deltax, y=50+deltay, w=pdf.epw/2)
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
            deltax = pdf.epw/2


    pdf.output(f"report_{p1}.pdf")


def generate_header(p):
    match p:
        case "H2O_vs_days_all":
            return "Water content in ppm according to Karl-Fischer test, oil samples from wind turbines, all seasons"
        case "AN_vs_days_all":
            return "Acid number in mgkOH/gOil, oil samples from wind turbines, all seasons"
        case "Ox_vs_days_all":
            return "Oxidation in A/cm, oil samples from wind turbines, all seasons"


if __name__ == "__main__":
    main()