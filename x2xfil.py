import filters

filter = filters.Filters()

log_x = open('x.txt', 'r')
log_x2xfil = open('x2xfil.txt','r')

xfil = []
yfil = []

for row in log_x:
    row = row.split(' ')

    x2xfil_log = str(filter.lowpass(float(row[0]), )) + " " + str(filter.lowpass(float(row[1])))

    log_x2xfil.write(x2xfil_log)

