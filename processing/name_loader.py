import os
import csv
import pickle


def getNameList():
    if not os.path.exists('nepali_names.pickle'):
        print('nepali_names.pickle does not exist, generating')

        print('Extracting names from nepali_names.csv')
        namesDict = extractNamesDict()

        maleNames = list()
        femaleNames = list()

        print('Sorting Names')
        for name in namesDict:
            counts = namesDict[name]
            tuple = (name, counts[0], counts[1])
            if counts[0] > counts[1]:
                maleNames.append(tuple)
            elif counts[1] > counts[0]:
                femaleNames.append(tuple)

        names = (maleNames, femaleNames)

        print('Saving nepali_names.pickle')
        fw = open('nepali_names.pickle', 'wb')
        pickle.dump(names, fw, -1)
        fw.close()
        print('Saved nepali_names.pickle')
    else:
        print('nepali_names.pickle exists, loading data')
        f = open('nepali_names.pickle', 'rb')
        names = pickle.load(f)
        print('nepali_names.pickle loaded')

    print('%d male names loaded, %d female names loaded' % (len(names[0]), len(names[1])))

    return names


def extractNamesDict():
    names = dict()
    genderMap = {'M': 0, 'F': 1}

    file = open('new_names.csv', 'r')
    rows = csv.reader(file, delimiter=',')

    for row in rows:
        name = row[0].upper()
        gender = genderMap[row[1]]
        count = int(row[2])

        if name not in names:
            names[name] = [0, 0]
        names[name][gender] = names[name][gender] + count

    file.close()
    print('\tImported Nepali names file')

    return names


if __name__ == "__main__":
    getNameList()