def matrix_get_submatrix(m, ii, jj):
    cols = len(m)     
    rows = len(m[0])  
    assert 0 <= ii < rows
    assert 0 <= jj < cols
    
    return [m[i][0:jj] + m[i][jj+1:] for i in range(rows) if i != jj]

def matrix_det(m):
    rows = len(m)     # number of rows of m
    assert rows > 0
    cols = len(m[0])  # number of cols of m
    if rows != cols:
        raise Exception("matrix must be square")
    if rows == 1:
        return m[0][0]
    elif rows == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    elif rows == 3:
        return m[0][0]*m[1][1]*m[2][2] + m[0][1]*m[1][2]*m[2][0] + m[0][2]*m[1][0]*m[2][1] - m[2][0]*m[1][1]*m[0][2] - m[2][1]*m[1][2]*m[0][0] - m[2][2]*m[1][0]*m[0][1]    
    sgn = 1
    sum = 0
    for i in range(cols):
        sum += sgn * m[0][i] * matrix_det(matrix_get_submatrix(m, i, 0))
    return sum

import unittest

class DeterminantTest(unittest.TestCase):

    def test_matrix_get_submatrix(self):
        matrix = [[1, 2, 4], [5, 7, 9], [1, 4, 8]]

        self.assertEqual(matrix_get_submatrix(matrix, 2, 2), [[1, 2], [5, 7]])
        with  self.assertRaises(Exception): matrix_get_submatrix(matrix, 3, 1)
        with self.assertRaises(Exception): matrix_get_submatrix(matrix, 0, -1)

    def test_matrix_det(self):
        matrix_1x1 = [[1]]
        matrix_3x3 = [[1, 2, 4], [5, 7, 9], [1, 4, 8]]
        matrix_4x4 = [[1, 2,3 ,4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        matrix_3x4 = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

        self.assertEqual(matrix_det(matrix_1x1), 1)
        self.assertEqual(matrix_det(matrix_3x3), 10)
        self.assertEqual(matrix_det(matrix_4x4), 0)
        with self.assertRaises(Exception):
            matrix_det(matrix_3x4)

if __name__ == "__main__":
    unittest.main()