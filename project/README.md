# Visualization of large data sets of oil analyses
    #### Video Demo:  <https://1drv.ms/v/s!Ah49GwRcwWoNgYEXFxP2Rq8LWOsXjQ?e=jD1MFe>
    #### Description:
    To monitor oil condition of machinery such as wind turbines, operators and service companies take oil samples and subject them to laboratory analyses. The laboratories, where these tests are performed, keep records of results and have therefore a large database of oil condition related parameters. However, learning about oil condition in machinery by examining raw data can be a tedious task for technicians and engineers. The purpose of this program is to enable graphic visualization of large data sets by plotting oil and machine operation parameters against each other regardless of whether they are independent variables.

    This version of the program parses "dataset4.csv" and "dataset5.csv", databases of test resuls of oil analyses, copies relevant data into dictionary data structures, processes that information generating 2D plots of selected parameters, and finally produces a report in pdf format including figures. The structure of the program is described in the following:

    project.py:
        def main():
            Can be called from the terminal with the command "python project.py".
            Creates a list of "Dataset" objects (see class Dataset), one object per input csv file.
            Iterates over the list of Datasets, for each Dataset reads specific oil parameters, e.g. "Wasser K. F." from the input, classifies them according to season of the oil sample (summer, fall, winter, spring), plots them against service time (days in the machine since last oil change) and generates a PDF report.

        def generate_PDFreport():
            Once plots exist in the form of PNG files which can be found in different folders (for example, plots of "H2O_vs_days_all" can be found in folder "data/water_KF"), this function generates a PDF report with a subset of those plots. The function list_files_pattern, which will be described next, specifies the subset of plots that are to be included in the PDF report.

        def list_files_pattern(dir, pattern):
            Returns a list of the file names in folder "dir" that include the str "pattern", a short text that corresponds to specific oil and machine operation parameters (e.g., "H2O_vs_days_all"). The file names in the list are given with their absolute path.

        def generate_report_param(p1, l1):
            Given a specific type of plot, "p1", e.g., "H2O_vs_days_all" and the corresponding list of file names, "l1", this function generates a PDF report. Each page of the report includes a header (see class PDF) and a maximum of 4 plots in a square array.

        def generate_header(p):
            Generates a report header, a title which is the same for each page of the report. The text of the title depends on the plot type "p" and is returned as a str.

    pdf.py:
        class PDF(FPDF):
            def header(self, title=""):
                Defines/Redefines the header method of the parent class FPDF. This method is used to add a title to each page of the PDF report.

    dataset.py
        class Dataset:
            def __init__(self, filename):
                A Dataset object can be initialized with a file name corresponding to an input csv file. The file name and the keys that can be extracted from the csv file are both properties of the object.

            def plot_param_t(self, season, param):
                Plots the data points of a given parameter (param) against service time of oil. The season in which the oil sample was taken (summer, fall,...) is specified by the parameter "season".
                The service time of oil might be given with the key "Einfülltage" in the raw data. Alternatively, it can be determined as the time since the last oil change: "Datum Probenentnahme"-"Datum letzter Ölwechsel" (see function "compute_days_in_service"). These dates are assumed to be in the format YYYY-MM-DD.
                Only data points are plotted that correspond to oil samples from wind turbines. No other sources for the samples are considered. The key corresponding to the source of the sample is "Probe aus". To select the rows, the presence of the key words: "wind", "wea", "wka", "éolienne" for "Probe aus" is verified. If any of them appear, the row is not discarded.
                Whether the data points correspond to the given season is verified considering the date the sample was taken, which corresponds to the key "Datum Probenentnahme". See validate_season(self, sample_date, season).
                There can be more than one oil in a Dataset. Iterating over the set of oils, the vectors "x" and "y" are generated, which correspond to the service time and oil parameter of interest (e.g. "Wasser K. F.") respectively.
                Given "x" an "y", 2D plots of "y" against "x" are generated and saved in .png files. The folder, where the .png images are saved depends on the specific parameter "y". For "Wasser K. F.", the images are saved in the folder "data/water_KF", for example.
                This function returns a dictionary with the following structure:
                d = {
                    "oil_name": oil_name,
                    "season": season,
                    "x_values": x,
                    "y_values": y,
                }

            def plot_param_t_all_seasons(self, p):
                While the previous function plots the data points of a specific season in each figure, this function plots the points of all seasons in the same figure. The word "all" appears in the file names of the plots to indicate that all seasons are considered. Different colors for the points in a figure indicate different seasons, as specified by the legends in the figures.
                For one oil parameter, this function calls plot_param_t(self, season, param) 4 times, 1 time for each season, and outputs dictionaries with information of data points, oil names and seasons (see plot_param_t(self, season, param)). Iterating over these dictionaries, the plots are generated and saved by means of this function. The folder, where the .png images are saved depends on the specific parameter "y". For "Wasser K. F.", the images are saved in the folder "data/water_KF", for example.

            def compute_days_in_service(self, date_sample, date_last_change):
                Returns days_in_service = date_sample - date_last_change
                It assumes that the dates are given in the format YYYY-MM-DD.

            def origin_sample(*arg):
                Returns True if the source of the oil sample, a str which corresponds to arg[1], contains any of the key words "wind", "wea", "wka", "éolienne" specified by arg[2]...arg[5].

            def validate_file_name(self, fn):
                replaces "/" and " " in a file name by "_".

            def validate_season(self, sample_date, season):
                Based on the date of the sample and a str representing the season (summer, fall, winter, spring), returns True if the date falls within that season. Otherwise, it returns False. It assumes that the date is given in the format YYYY-MM-DD.

    Folder data:
        Data generated by the program

        Folder water_KF:
            Contains png plots related to the following oil parameter: Water content in ppm according to the Karl-Fischer test.
        Folder AN:
            Contains png plots related to the following oil parameter: Acid number in mgkOH/gOil
        Folder ox:
            Contains png plots related to the following oil parameter: Oxidation in A/cm

    requirements.txt:
        Libraries required.

    test_project.py:
        Some of the tests required the program to be run first (See comments on test_project.py.



