

def build_matrix(num_rows, num_cols):
    # construct a matrix
    my_matrix = []
    for row in range(num_rows):
        new_row = []
        for col in range(num_cols):
            new_row.append(row * col)
        my_matrix.append(new_row)

    return my_matrix


def trace(matrix):
    width = len(matrix[0])
    height = len(matrix)
    print('height ', height)
    print('width: ', width)
    if height == width:
        sum_val = 0
        for idx, row in enumerate(matrix):
            row = matrix[idx]
            sum_val += row[idx]
        return sum_val


matrix_a = [[0, 1, 2], [4, 5, 6], [7, 8, 9]]
print('test: ', trace(matrix_a))
print('check cell val', matrix_a[2][0])

print('a: ', trace(build_matrix(5, 5)))
print('b: ', trace(build_matrix(25, 25)))
