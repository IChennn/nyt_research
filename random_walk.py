import sys,argparse
import numpy as np
from numpy import linalg as LA

def read_sim_matrix(input_file):
	mtx = np.loadtxt(input_file)
	return mtx

# def read_sim_matrix(input_file):
# 	weightMtx = []
# 	for line in file(input_file).readlines():
# 		weightMtx.append(np.array(map(float, line.split())))
# 	return np.array(weightMtx)

def remove_diag(matrix):
	num_row, num_col = np.shape(matrix)
	for i in range(0, num_row):
		matrix[i][i] = 0
	return matrix

def row_normalize(matrix):
	sum = np.sum(matrix, 1)
	return (matrix/sum[:, np.newaxis]).T

parser = argparse.ArgumentParser()
parser.add_argument('W11')
parser.add_argument('W22')
parser.add_argument('W12')
parser.add_argument('-w',type=float,default=0.9)
args = parser.parse_args()

E11 = remove_diag(read_sim_matrix(args.W11))
E22 = remove_diag(read_sim_matrix(args.W22))
E12 = read_sim_matrix(args.W12)
E21 = E12.T
num1 = np.shape(E11)[0]
num2 = np.shape(E22)[0]

L11 = row_normalize(E11)
L22 = row_normalize(E22)
L12 = row_normalize(E21)
L21 = row_normalize(E12)

S1 = np.ones(num1)/num1
S1 = S1[:, np.newaxis]
S2 = np.ones(num2)/num2
S2 = S2[:, np.newaxis]

former = (1 - args.w) * S1 + args.w * (1 - args.w) * np.dot(L11, np.dot(L12, S2))
latter = args.w * args.w * np.dot(L11, np.dot(L12, np.dot(L22, L21)))
combine = former * np.ones(num1) + latter
w, v = LA.eig(combine)
score1 = abs(v[:, 0])/sum(abs(v[:, 0]))
score2 = (1 - args.w) * S2 + args.w * np.dot(L22, np.dot(L21, S1))

op = open('Score_layer_1.txt', 'w')
for i in range(0, num1):
	op.write("%f " %score1[i])
op = open('Score_layer_2.txt', 'w')
for i in range(0, num2):
	op.write("%f " %score2[i])