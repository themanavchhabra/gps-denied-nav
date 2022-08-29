import matplotlib.pyplot as plt
import numpy as np

log_x = open('x2.txt', 'r')
log_xfil = open('x_filtered2.txt', 'r')

x = []
y = []

xfil = []
yfil = []

xact = []
yact = []

try:
    log_xact = open('x_actual2.txt', 'r')
except Exception as e:
    pass

for row in log_x:
    row = row.split(' ')
    x.append(float(row[0]))
    y.append(float(row[1]))

# print(x)

for row in log_xfil:
    row = row.split(' ')
    xfil.append(float(row[0]))
    yfil.append(float(row[1]))

# x = [0, 1, 2, 3, 4, 2, 0, -1, -2]

figure, axis = plt.subplots(1,2)

axis[0].plot(x)
axis[0].plot(xfil)
axis[0].set_title("distance in x")

axis[1].plot(y)
axis[1].plot(yfil)
axis[1].set_title("distance in y")

# axis[1,1].plot(y, yfil)
# axis[1,1].set_title("distance in y")

# plt.plot(y)
# plt.plot(yfil)
# plt.plot(xfil, label = "x filtered")
plt.show()