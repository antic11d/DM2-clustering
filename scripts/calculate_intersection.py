import pandas as pd


def intersection(intersect, lst2):
    return set([value for value in lst2 if value in intersect])


def list_intersection(list_of_columns):
    intersect = set(list_of_columns[0])

    for csv in list_of_columns[1:]:
        intersect = intersection(intersect, csv)

    return intersect


def main():
    columns = []
    for i in range(1, 5):
        path = f'../data/group_{i}/columns_{i}.csv'
        df = pd.read_csv(path)
        cols = ['Unnamed: 0'] + list(df.columns)
        columns.append(cols)

    columns_intersected = list_intersection(columns)

    for i in range(1, 5):
        print(f'group_{i}')
        path = f'../data/group_{i}/data.csv'
        df = pd.read_csv(path)
        intersected = df[list(columns_intersected)]
        print(f'\tShape after intersection: {intersected.shape}')
        intersected.to_csv(f'../data/group_{i}/data_intersected.csv', index_label='Unnamed: 0', index=False)


if __name__ == '__main__':
    main()
