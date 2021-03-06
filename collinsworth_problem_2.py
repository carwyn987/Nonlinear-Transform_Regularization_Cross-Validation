# -*- coding: utf-8 -*-
"""Collinsworth_Problem_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MaKUQJvqpN4I8rcDjq_njWQeEE9ccN8R
"""

### Carwyn Collinsworth
# Stony Brook University
# CSE353 Assignment 6 - Problem 2: Regularization
# Professor Yin

# Imports

# Firstly we need pandas to load the dataset in to our notebook
import pandas as pd
# Import numpy to work with matricies (transpose, multiply, etc.)
import numpy as np
# Import matplotlib.pyplot to chart results at the end
import matplotlib.pyplot as plt
# Import scipy.optimize.minimize to solve for the regularized regression
from scipy.optimize import minimize
# Import Math to use Math.abs in regularization
import math

# Mount google drive for reading from datafiles
from google.colab import drive
drive.mount('/content/drive')

# Define global variables

# Note to Grader: Data directory must be changed for the appropriate location if testing code. TotalPath should point to the data directory.
totalPath = "/content/drive/MyDrive/Stony Brook/Classes/Year 3/Semester 1/CSE353 - Machine Learning/Assignment 6/data/"
xDataFileName = "TrainingData_x.txt"
yDataFileName = "TrainingData_y.txt"
xTestingData = "TestingData_x.txt"
yTestingData = "TestingData_y.txt"

# First of all, we want to load the datasets in and get them into the correct format

# Load data
xdata = pd.read_csv(totalPath + xDataFileName, sep=",", header=None).to_numpy()
ydata = pd.read_csv(totalPath + yDataFileName, sep=",", header=None).to_numpy().T

# Reformat xdata
xdata = xdata.T
ydata = ydata.T

print("X Data: ", xdata.shape)
print(xdata)
print("Y Data: ", ydata.shape)
print(ydata)

# Let us also define our N : the number of elements in our dataset
N = xdata.size

# Our x array now has 1 row and 20 columns, y array has 20 rows, 1 column.

# Next, we want to transform our dataset along the guidelines of the question (i.e)
# z_n = phi_Q (X_n) = [1, x_n, x^2_n, x^3_n, x^4_n, ..., x^Q_n]
# Therefore, Q is the number of terms in our polynomial transform 
# (hence why it is called a Q-th order polynomial transform)

# Let us define the Q value we want to use
Q = 6

# So we create our Z matrix where Z = [z^T_1; z^T_2; ...; z^T_N]
Z = np.zeros((N,Q))

# Now we want to fill our Z matrix with the correct z^T_n elements
# As is defined: Z = [z^T_1; z^T_2; ...; z^T_N]

for i in range(N):
  #calculate z^T_i
  #z_i = [1, x_i, x^2_i, x^3_i, x^4_i, ..., x^Q_i]

  # Initialize z_temp_i array
  z_temp_i = np.zeros((1,Q))
  # Fill array
  for j in range(Q):
    z_temp_i[0,j] = xdata[0,i]**j
  # Set array into Z
  Z[i,:] = z_temp_i

# Let us visualize our Z matrix (just the first row)
print(Z[0,:])
print("Shape of Z: " + str(Z.shape))

### Now we want to solve for w_poly by performing regularized linear regression
# To do this, solve for min_w_regpoly||Z @ w_regpoly - y||^2 + lambda||w_regpoly^2||

# Define lam
lam = 0.1

def min_w_regpoly(w_regpoly):
  return np.linalg.norm(Z @ w_regpoly - np.ravel(ydata))**2  + lam * np.linalg.norm(w_poly)**2

# We will use scipy.optimize.minimize
w_poly = minimize(min_w_regpoly, np.zeros((Q,1)))
print("Optimizer exited successfully?: ", str(w_poly.success), ", Message: ", w_poly.message)
w_poly = w_poly.x
w_poly

# Visualize w_poly, which should have shape (Q,1)
print(w_poly)
print(w_poly.shape)

# Now that we have calculated w_poly, we need to calculate the testing error
# We use the formula err_sqr = sum_n=1^N (w^T_poly @ phi(x_n) - y_n)^2

# initialize err_sqr
err_sqr = 0

# calculate the error of each point and add it to this sum
for n in range(N):
  err_sqr += (np.transpose(w_poly) @ Z[n,:] - ydata[n])**2

print("Training Error: " + str(err_sqr))

# Testing error

# Set N for testing data
N = 40

# Load data
xTestdata = pd.read_csv(totalPath + xTestingData, sep=",", header=None).to_numpy()
yTestdata = pd.read_csv(totalPath + yTestingData, sep=",", header=None).to_numpy().T

# Reformat xdata
xTestdata = xTestdata.T
yTestdata = yTestdata.T

# So we create our Z matrix where Z = [z^T_1; z^T_2; ...; z^T_N]
Z_test = np.zeros((N,Q))

# Now we want to fill our Z matrix with the correct z^T_n elements
for i in range(N):
  # Initialize z_temp_i array
  z_temp_i = np.zeros((1,Q))
  # Fill array
  for j in range(Q):
    z_temp_i[0,j] = xTestdata[0,i]**j
  # Set array into Z
  Z_test[i,:] = z_temp_i

# initialize err_sqr
err_sqr_test = 0

# calculate the error of each point and add it to this sum
for n in range(N):
  err_sqr_test += (np.transpose(w_poly) @ Z_test[n,:] - yTestdata[n])**2

print("Testing Error: " + str(err_sqr_test))

# Define our function for taking in x value and regressing to estimate y
def hypo_function(x):
  # generate phi(x)
  phi_x = np.zeros((1,Q))
  # Fill array
  for j in range(Q):
    phi_x[0,j] = x**j
  # Transpose phi_x
  phi_x = np.transpose(phi_x)
  return np.transpose(w_poly) @ phi_x

# Plot the training and testing sample points, and the estimated curve
# Equation for hypothesis curve: g(x) = w_poly^T @ phi(x)

# Create array that is the conglomeration of test and train for both x,y
x_plot = np.concatenate((xdata[0], xTestdata[0]));
print("X data shape: " + str(x_plot.shape) + ", X data in total: ", x_plot)

y_plot = np.concatenate((ydata[:,0],yTestdata[:,0]))
print("Y data shape: " + str(y_plot.shape) + ", Y data in total: ", y_plot)

plt.plot(x_plot, y_plot, 'o')

# Find the range of x data
min_xdata = min(x_plot)
max_xdata = max(x_plot)
print("X data totality ranges from " + str(min_xdata) + " to " + str(max_xdata))

x_hypothesis_function = np.linspace(min_xdata - .1,max_xdata + .1, 200)
y_hypothesis_function = np.zeros((1,x_hypothesis_function.size))

# fill y data hypothesis function
for i in range(x_hypothesis_function.size):
  y_hypothesis_function[0,i] = hypo_function(x_hypothesis_function[i])

# Reformat data for visualization
y_hypothesis_function = np.ravel(y_hypothesis_function[0,:])
print(y_hypothesis_function[100:120])

# Set plot ranges
plt.xlim(-15, 15)
plt.ylim(-20, 20)

plt.plot(x_hypothesis_function,y_hypothesis_function)

### With the regularization in place, we have optimized the function at Q=6.
# We now have error rates of 95.76071044 for training and 207.84533215 for testing.
# With the low lambda value, these are almost identical with our linear regression
# without regularization

### With a lambda of 100, our error rates slightly fell
# training: 95.76071043, testing: 207.84535233