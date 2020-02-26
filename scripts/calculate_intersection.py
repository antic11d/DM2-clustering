def intersection(intersect, lst2):
    return set([value for value in lst2 if value in intersect])


def list_intersection(list_of_columns):
    intersect = set(list_of_columns[0])

    for csv in list_of_columns[1:]:
        intersect = intersection(intersect, csv)

    return intersect


def main():
    


if __name__ == '__main__':
    main()