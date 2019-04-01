import numpy as np
from collections import Counter


def read_csv(filepath, dtype):
    return np.loadtxt(
        filepath, delimiter=',', dtype=dtype)


def write_csv(filepath, ndarr, fmt):
    np.savetxt(filepath, ndarr, delimiter=',', fmt=fmt)


def total_of_each_column(ndarr):
    return np.sum(ndarr, axis=0).astype(int)


def counter(ndarr):
    return Counter(ndarr.tolist())


def remove_unique_feature(index, bag_of_paths):
    li = total_of_each_column(bag_of_paths).tolist()
    condition = [i for i, x in enumerate(li) if x == 1]

    write_csv(
        './data/index_rm_unq_f.csv',
        np.delete(index, condition, axis=0),
        fmt='%s')
    write_csv(
        './data/bag_of_paths_rm_unq_f.csv',
        np.delete(bag_of_paths, condition, axis=1),
        fmt='%d')


if __name__ == "__main__":
    index = read_csv('data/index.csv', 'unicode')
    bag_of_paths = read_csv('data/bag_of_paths.csv', int)
    remove_unique_feature(index, bag_of_paths)
    print('Created: index.csv ---> index_rm_unq_f.csv')
    print('Created: bag_of_paths.csv ---> bag_of_paths_rm_unq_f.csv')
