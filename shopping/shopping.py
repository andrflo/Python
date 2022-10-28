import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.2


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")        
        for row in reader:
            
            month = -1
            match row["Month"].lower():
                case "jan":
                    month = 0
                case "feb":
                    month = 1
                case "mar":
                    month = 2
                case "apr":
                    month = 3
                case "may":
                    month = 4    
                case "jun":
                    month = 5    
                case "jul":
                    month = 6   
                case "aug":
                    month = 7
                case "sep":
                    month = 8
                case "oct":
                    month = 9
                case "nov":
                    month = 10
                case "dec":
                    month = 11 

            returningVisitor = -1
            match row["VisitorType"].lower():
                case "returning_visitor":
                    returningVisitor = 1
                case "new_visitor":
                    returningVisitor = 0  

            weekend = -1
            match row["Weekend"].lower():
                case "false":
                    weekend = 0
                case "true":
                    weekend = 1       

            revenue = -1            
            match row["Revenue"].lower():
                case "false":
                    revenue = 0
                case "true":
                    revenue = 1

            evidence.append([int(row["Administrative"]), float(row["Administrative_Duration"]), 
            int(row["Informational"]), float(row["Informational_Duration"]), int(row["ProductRelated"]),
            float(row["ProductRelated_Duration"]), float(row["BounceRates"]), float(row["ExitRates"]),
            float(row["PageValues"]), float(row["SpecialDay"]), month, int(row["OperatingSystems"]), 
            int(row["Browser"]), int(row["Region"]), int(row["TrafficType"]), returningVisitor, weekend])
            labels.append(revenue)            
    return (evidence, labels)        


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    m = KNeighborsClassifier(n_neighbors=1)
    # Fit model
    return m.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """    
    num_positive_labels = 0
    num_negative_labels = 0   
    num_positive_labels1 = (labels == 1).sum()
    num_negative_labels1 = (labels == 0).sum()

    for l in labels:        
        if labels[l] == 1:
            num_positive_labels += 1
        else:
            num_negative_labels += 1

    print("npl", num_positive_labels)
    print("npl1", num_positive_labels1)
    print("nnl", num_negative_labels)
    print("nnl1", num_negative_labels1)
    num_positive_preds = 0
    num_negative_preds = 0
    for p in predictions:
        if predictions[p] == 1:
            num_positive_preds += 1
        else:
            num_negative_preds += 1  

    print("npp", num_positive_preds)
    print("nnp", num_negative_preds)         

    if num_positive_preds == 0 and num_positive_labels == 0:
        sensitivity = 1
    elif num_positive_preds != 0 and num_positive_labels == 0:
        sensitivity = 0
    else:
        sensitivity = float(num_positive_preds/num_positive_labels) 

    if num_negative_preds == 0 and num_negative_labels == 0:
        specificity = 1
    elif num_negative_preds != 0 and num_negative_labels == 0:  
        specificity = 0  
    else:    
        specificity = float(num_negative_preds/num_negative_labels)    
    
    return (sensitivity, specificity)     




if __name__ == "__main__":
    main()
