import math
import csv
import os


def normdistances(points):
    dists = []
    normdist = []
    centx = sum(xlist) / len(xlist)
    centy = sum(ylist)/len(ylist)
    for coord in points:
        dists.append(((coord[0]-centx)**2 + (coord[1]-centy)**2)**.5)
    maxdist = max(dists)
    for dist in dists:
        normdist.append(dist/maxdist)
    return normdist


def entropy(dist):
    # dist sort is the distances from least to most
    # N is the number of normalized distances
    # dist is the array of all the normalized distances
    # binarray is the coresbonding bin number for each sorted distance
    # filledbins is the array of bins that are nonzero
    # bincounts is the corresponding amount in each bin in fillededbin
    # binavgs is the average value of each bin in order of filled bins
    # binvalues is a temporary variable for each bin to compute the average
    # edist is the quantinization error as in equation 6
    # Hsum is the sum of all the p(k) for each bin, equation 3
    # fJfirst is the list offirst term of f_{dist)(J) in equation 7
    # emax is the emax in euation 7
    # fj is the whole equation 7
    distsort = sorted(dist)
    n = len(dist)
    fjfirst = []
    elist = []
    fj = []
    for J in range(1, n+1):
        binarray = []
        for i in range(n):
            binnum = math.ceil(distsort[i] * (2**J))
            binarray.append(binnum)
        binavgs = []
        bincounts = []
        filledbins = list(dict.fromkeys(binarray))
        for i in range(len(filledbins)):
            bincounts.append(binarray.count(filledbins[i]))
            binsum = 0
            bincount = 0
            for j in range(n):
                if filledbins[i] == binarray[j]:
                    binsum += distsort[j]
                    bincount += 1
            binavgs.append(binsum/bincount)
        edist = 0
        for i in range(n):
            edist += (distsort[i] - binavgs[filledbins.index(binarray[i])]) ** 2
        edist = (edist/n)**.5
        hsum = 0
        for i in range(len(bincounts)):
            bincount = bincounts[i]/n
            hsum += bincount * (math.log2(bincount))
        fjfirst.append((0 - hsum) / (math.log2(n)))
        elist.append(edist)
    emax = .25
    for i in range(len(fjfirst)):
        fj.append(fjfirst[i] + (elist[i] / emax))
    return min(fj)


def threewayangle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang


def getangles(points):
    angles = []
    normangles = []
    for i in range(len(points)):
        if points[i] == points[0]:
            angles.append(threewayangle(points[-1], points[0], points[1]))
        elif points[i] == points[-1]:
            angles.append(threewayangle(points[-2], points[-1], points[0]))
        else:
            angles.append(threewayangle(points[i-1], points[i], points[i+1]))
    for angle in angles:
        if angle > 180:
            normangles.append((360-angle) / 180)
        else:
            normangles.append(angle / 180)
    return normangles


def smouthness(angles):
    psum = 0
    n = len(angles)
    for i in range(n):
        psum += (math.exp(0 - angles[i]) - math.exp(-1)) / (1 - math.exp(-1))
    return psum / n


def randoom(points):
    return 4 / (4 * (len(points)-1))


filenames = []
rowsoffinal = []
for root, dirs, files in os.walk(".", topdown=True):
    for name in files:
        if ".csv" in name:
            filenames.append(name)
for files in filenames:
    with open(files) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        coords = []
        xlist = []
        ylist = []
        for row in csv_reader:
            coords.append([float(row[0]), float(row[1])])
            xlist.append(float(row[0]))
            ylist.append(float(row[1]))
        cedist = entropy(normdistances(coords))
        ceangle = entropy(getangles(coords))
        psmouth = smouthness(getangles(coords))
        randomness = randoom(coords)
        a1 = 0.6
        a2 = 0.07
        a3 = 0.33
        complexity = ((1 + randomness) * (a1 * min([cedist, ceangle]))) + (a2 * max([cedist, ceangle])) + (a3 * psmouth)
        rowsoffinal.append([files, complexity, psmouth])
filename = input("who is it the file for?") + ".csv"
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rowsoffinal)
