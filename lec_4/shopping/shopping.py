import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


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


    month_dict = {
        "Jan": 1,

        "Feb": 2,

        "Mar": 3,

        "Apr": 4,

        "May": 5,

        "June": 6,

        "Jul": 7,

        "Aug": 8,

        "Sep": 9,

        "Oct": 10,

        "Nov": 11,

        "Dec": 12,
    }

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidences = []

        labels = []

        for row in reader:
            evidence = []
            for cell in row[:17]:
                if cell in month_dict:
                    evidence.append(month_dict[cell])
                elif cell == "Returning_Visitor":
                    evidence.append(1)
                elif cell == "New_Visitor" or cell == "Other":
                    evidence.append(0)
                elif cell == "FALSE":
                    evidence.append(0)
                elif cell == "TRUE":
                    evidence.append(1)
                else:
                    evidence.append(float(cell))

            if row[17] == "TRUE":
                label = 1
            elif row[17] == "FALSE":
                label = 0

            evidences.append(evidence)
            labels.append(label)
            

    return evidences,labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    model.fit(evidence, labels)

    return model




def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    identified_positive_value = 0
    true_positive_value = 0
    identified_negative_value = 0
    true_negative_value = 0


    for x,y in zip(labels, predictions):
        if y == 1:
            true_positive_value += 1
            if x == 1:
                identified_positive_value += 1

        elif y == 0:
            true_negative_value += 1
            if x == 0:
                identified_negative_value += 1

    return (identified_positive_value/true_positive_value,
            identified_negative_value/true_negative_value)


if __name__ == "__main__":
    main()
