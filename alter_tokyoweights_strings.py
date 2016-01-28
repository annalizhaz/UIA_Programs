import numpy as np
import csv
import sys

def read_csv(filename):

    '''
    Read in csv file (filename) and create array from it.

    Returns numpy array
    '''
    with open(filename, "r") as f:
        reader = csv.reader(f)
        data_in_lists = list(reader)

    empty_rows_removed = []

    for row in data_in_lists:
        if len(row) != 0:
            empty_rows_removed.append(row)

    data_array = np.array(empty_rows_removed[1:]) #removes header row
    header_row = np.array(empty_rows_removed[0])
    return data_array, header_row

def edit_strings(data_array):
    '''
    Alter amenity labels to match other YP_KRN labels, format YP_###_KRN
    '''
    amenity_column = list(data_array[:, 15])
    new_labels = []
    skipped_amenities = []

    for i, label in enumerate(amenity_column):

        #first part is collecting missing labels

        if i!=0:
            if int(label)!=int(amenity_column[i-1])+1:
                for j in range(int(amenity_column[i-1])+1, int(amenity_column[i])):
                    skipped_amenity = "YP_" + str(j) + "_KRN"
                    skipped_amenities.append(skipped_amenity)
        str_label = str(label)
        if len(str_label) == 1:
            new_label = "YP_00" + str_label + "_KRN"
            new_labels.append(new_label)
        if len(str_label) == 2:
            new_label = "YP_0" + str_label + "_KRN"
            new_labels.append(new_label)
        if len(str_label) == 3:
            new_label = "YP_" + str_label + "_KRN"
            new_labels.append(new_label)
    return new_labels, skipped_amenities

def write_new_csv(data_array, new_labels, header_row, skipped_amenities):

    array_labels_chopped = data_array[:, :15]
    new_label_column = np.array(new_labels).reshape(361, 1)

    labels_replaced = np.hstack((array_labels_chopped, new_label_column))
    data = np.vstack((header_row, labels_replaced))

    with open("relabelled_tokyoedits.csv", 'w') as csvfile:
        mywriter = csv.writer(csvfile, dialect='excel')

        for row in data:
            mywriter.writerow(list(row))

    with open("tokyoedits_skipped_amenities.csv", 'w') as csvfile:
        otherwriter = csv.writer(csvfile, dialect='excel')

        for item in skipped_amenities:
            otherwriter.writerow([item])



def go(filename):
    data_array, header_row = read_csv(filename)
    new_labels, skipped_amenities = edit_strings(data_array)
    write_new_csv(data_array, new_labels, header_row, skipped_amenities)

if __name__ == "__main__":
    usage = "python3 alter_tokyoweights_strings.py <'filename'>"
    args_len = len(sys.argv)
    if args_len != 2:
        raise ValueError("Incorrect number of arguments provided")
        print(usage)
        sys.exit(0)
    else:

        filename = sys.argv[1]

        go(filename)

        print(usage)    
        sys.exit(0)

