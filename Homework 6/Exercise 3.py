"""
Exercise 3:
This exercise is not a jupyter notebook cause it kept running into problems and error when it was
    running in a notebook environment. So we moved the code to this environment to execute the
    code.
"""

# the code from the given file
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

# Task a) of the exercise: testing the functions with unittest

import unittest

class DeterminantTest(unittest.TestCase):
    """
    We'll define two tests for the two functions, using the TestCase method of unittest.
    """
    def test_matrix_get_submatrix(self):
        matrix1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        output_matrix1 = [[1, 2], [4, 5]]

        # to test the output of the function is correct
        self.assertEqual(matrix_get_submatrix(matrix1, 2, 2), output_matrix1)
    
    # raising an error for invalid indexes that do not exist in the matrix
    def test_matrix_get_submatrix_invalid_index(self):
        matrix = [[1, 2], [3, 4]]
        with self.assertRaises(AssertionError): 
            matrix_get_submatrix(matrix, 1, 4)
    
    # raising error for negative indexes
    def test_matrix_get_submatrix_negative_index(self):
        matrix = [[1, 2], [3, 4]]
        with self.assertRaises(AssertionError): 
            matrix_get_submatrix(matrix, -3, 1)

    def test_matrix_det(self):
        # setting some matrixes to test the function with
        matrix_1x1 = [[1]]
        matrix_3x3 = [[1, 2, 4], [5, 7, 9], [1, 4, 8]]
        matrix_4x4 = [[1, 4 ,3 ,6], [5, 2, 1, 8], [8, 2, 1, 5], [10, 7, 1, 2]]
        matrix_3x4 = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

        self.assertEqual(matrix_det(matrix_1x1), 1)
        self.assertEqual(matrix_det(matrix_3x3), 10)
        self.assertEqual(matrix_det(matrix_4x4), 486)
        # raising an error if the matrix is not a square, which was also in the function code
        with self.assertRaises(Exception):
            matrix_det(matrix_3x4)

if __name__ == "__main__":
    unittest.main()

# Task b) is fixing the bugs in the code
# By running the test, we can see that the matrix_det.() fails at a 4x4 matrix and a large matrix
# We need to fix the sign in the function by *= -1 , which is a common way of doing it in determinant calculations

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
        sum += sgn * m[0][i] * matrix_det(matrix_get_submatrix(m, 0, i))
        # here is the change
        sgn *= -1
    return sum

# running the test again to see if it's fixed
class DeterminantTest(unittest.TestCase):
    def test_matrix_det(self):
        matrix_1x1 = [[1]]
        matrix_3x3 = [[1, 2, 4], [5, 7, 9], [1, 4, 8]]
        matrix_4x4 = [[1, 4 ,6, 1], [5, -2, 1, 1], [8, -3, 1, 5], [7, 1, 1, 2]]
        matrix_3x4 = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

        self.assertEqual(matrix_det(matrix_1x1), 1)
        self.assertEqual(matrix_det(matrix_3x3), 10)
        self.assertEqual(matrix_det(matrix_4x4), -402)
        with self.assertRaises(Exception):
            matrix_det(matrix_3x4)

if __name__ == "__main__":
    unittest.main()

# This test will still fail, so I figured out that I there's a problem when it calls the matrix_get_submatrix.() function
# After taking a look at the logic of this function, we fixed it like so:

def matrix_get_submatrix(m, ii, jj):
    cols = len(m)     
    rows = len(m[0])  
    assert 0 <= ii < rows
    assert 0 <= jj < cols
    
    # changing the jj at the end of the code to ii
    return [m[i][0:jj] + m[i][jj+1:] for i in range(rows) if i != ii]

# So if now we run everything again, our test will be OK
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
        sum += sgn * m[0][i] * matrix_det(matrix_get_submatrix(m, 0, i))
        sgn *= -1
    return sum


class DeterminantTest(unittest.TestCase):
    def test_matrix_det(self):
        matrix_1x1 = [[1]]
        matrix_3x3 = [[1, 2, 4], [5, 7, 9], [1, 4, 8]]
        matrix_4x4 = [[1, 4 ,6, 1], [5, -2, 1, 1], [8, -3, 1, 5], [7, 1, 1, 2]]
        matrix_3x4 = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

        self.assertEqual(matrix_det(matrix_1x1), 1)
        self.assertEqual(matrix_det(matrix_3x3), 10)
        self.assertEqual(matrix_det(matrix_4x4), -402)
        with self.assertRaises(Exception):
            matrix_det(matrix_3x4)

if __name__ == "__main__":
    unittest.main()

# Task c) is calculating the average running time of matrix_det()
# for that we'll define two functions
import random
import time


def random_matrix(shape):
    """
    This function generates random matrices
    :param shape: the size of the matrix
    """
    matrix = [[random.randint(1, 10) for i in range(shape)] for i in range(shape)]
    return matrix

def average_execution_time():
    """
    This funciton calculates the average running time of the matrix_det() function
    We loop over the range of the 100 matrices and record the time before
        and after the process is done, and calculate the average running time
    In this function we call the previous random_matrix() and the matrix_det() functions
    """
    results = [] 
    for shape in range(1, 11):
        matrices = [random_matrix(shape) for _ in range(100)]
        
        start = time.time()
        for m in matrices:
            matrix_det(m)
        end = time.time()
        
        average_time = (end - start) / 100
        results.append((shape, average_time))
    return results

if __name__ == "__main__":
    times = average_execution_time()
    for shape, average in times:
        print(f"Average time of matrix {shape}x{shape} : {average:.8f} sec")

# This will return multiple average running times for each matrix shape

# also, running this code from top to bottom will run 4 tests and stop, I commented out old tests from the previous step 
#   while testing and writing the code to see the true results. We figure it's not the best practice but for the
#   purposes of this assignment, we kept it like this so the process would be clear