import concurrent
import random
from threading import Thread
from concurrent.futures.thread import ThreadPoolExecutor

THREADS_COUNT = 4
ROWSm1, COLSm1 = 4, 3
ROWSm2, COLSm2 = 3, 4
TASK = 1

X = [[random.randrange(0, 10) for _ in range(COLSm1)] for _ in range(ROWSm1)]

Y = [[random.randrange(0, 10) for _ in range(COLSm2)] for _ in range(ROWSm2)]

result = [[0 for cols in Y[0]] for rows in X]


def compute_element_of_resulting_matrix(row, column):
    #computes the element from pos "row","col" in the resulting matrix
    for pos in range(len(X[row])):
        result[row][column] += X[row][pos] * Y[pos][column]


#  start = tuple  (row,column)
def task_rows(start, number_of_elements):
    #task 1 - compute the sum taking each element row by row
    for _ in range(number_of_elements):
        compute_element_of_resulting_matrix(*start)
        start = next_index_rows(start)


def task_cols(start, number_of_elements):
    #task 2 - compute the sum taking each element column by column
    for _ in range(number_of_elements):
        compute_element_of_resulting_matrix(*start)
        start = next_index_columns(start)


def task_k(start):
    #task 3 - compute the sum taking each k-th element
    while start != (-1, -1):
        compute_element_of_resulting_matrix(*start)
        start = next_index_rows(start, THREADS_COUNT)


def next_index_rows(start, pas=1):
    #get linear index
    linear_index = len(result[0]) * start[0] + start[1]
    linear_index += pas

    #check if end of matrix
    if linear_index >= len(result) * len(result[0]):
        return -1, -1

    #convert back to row,col index
    row = linear_index // len(result[0])
    column = linear_index % len(result[0])
    return row, column


def next_index_columns(start, pas=1):

    #get linear index
    linear_index = len(result) * start[1] + start[0]
    linear_index += pas

    #check if end of matrix
    if linear_index >= len(result) * len(result[0]):
        return -1, -1

    #convert back to row,col index
    column = linear_index // len(result[0])
    row = linear_index % len(result[0])
    return row, column


def regular_threads():
    #how many numbers the first n-1 threads will have to compute
    nice_numbers = ROWSm1 * COLSm2 // THREADS_COUNT
    #computes how many numbers remained for the last thread
    last_numbers = ROWSm1 * COLSm2 - nice_numbers * (THREADS_COUNT - 1)
    threads = []
    start = (0, 0)

    if TASK == 1:
        for i in range(THREADS_COUNT - 1):

            threads.append(Thread(target=task_rows, args=(start, nice_numbers)))
            start = next_index_rows(start, nice_numbers)
        threads.append(Thread(target=task_rows, args=(start, last_numbers)))

    if TASK == 2:
        for i in range(THREADS_COUNT - 1):
            threads.append(Thread(target=task_cols, args=(start, nice_numbers)))
            start = next_index_columns(start, nice_numbers)
        threads.append(Thread(target=task_cols, args=(start, last_numbers)))

    if TASK == 3:
        for i in range(THREADS_COUNT):
            threads.append(Thread(target=task_k, args=(start,)))
            start = next_index_rows(start)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def pool_threads():
    nice_numbers = ROWSm1 * COLSm2 // THREADS_COUNT
    last_numbers = ROWSm1 * COLSm2 - nice_numbers * (THREADS_COUNT - 1)
    start = (0, 0)

    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=THREADS_COUNT) as executor:
        if TASK == 1:
            for i in range(THREADS_COUNT - 1):
                #submit first n-1 threads that has the same amount of numbers to compute
                executor.submit(task_rows, start, nice_numbers)
                start = next_index_rows(start, nice_numbers)
            #submit the last thread that has to compute the remaining numbers
            executor.submit(task_rows, start, last_numbers)
        if TASK == 2:
            for i in range(THREADS_COUNT - 1):
                # submit first n-1 threads that has the same amount of numbers to compute
                executor.submit(task_cols, start, nice_numbers)
                start = next_index_columns(start, nice_numbers)
            executor.submit(task_cols, start, last_numbers)

        if TASK == 3:
            for i in range(THREADS_COUNT):

                executor.submit(task_k, start)
                start = next_index_rows(start)


def print_matrix(matrix):
    for line in matrix:
        print(line)
    print("\n")


if __name__ == '__main__':
    print_matrix(X)
    print_matrix(Y)

    #regular_threads()
    pool_threads()

    print_matrix(result)

