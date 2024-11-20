#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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