import csv
import sys
import re


def compare_dna(person_data, sequence):
    result = []
    for gene_name in person_data:

        # check the exact lenth of the gene inside the squance
        search_exact = re.search("("+gene_name+"){"+person_data[gene_name]+"}", sequence)

        # check if the sequance is more than exact
        search_more = re.search("("+gene_name+"){"+str(int(person_data[gene_name])+1)+",}", sequence)

        result.append((search_exact is not None) and not (search_more is not None))

    return result


# location of a file contains people genes codes
database_location = sys.argv[1]
# location of a file contains sequance to be cheked
sequance_location = sys.argv[2]

# open people database file
with open(database_location) as people_database_file:
    # read pople database file
    people_data = csv.DictReader(people_database_file, delimiter=',')

    # open unknown sequance file
    with open(sequance_location, "r") as sequance_file:

        # read sequance
        sequance = sequance_file.read()

        # to save matched name
        name = ''

        # loop over people to find the match one
        for person_data in people_data:

            # extract person name
            person_name = person_data.pop('name')

            # compare person dna with the sequance
            result = all(compare_dna(person_data, sequance))

            # match condition
            if result is True:
                name = person_name

        # print match condition result
        if name != '':
            print(name)
        else:
            print('No Match')

