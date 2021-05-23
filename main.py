import matplotlib.pyplot as plt
import numpy as np
import random

GRID_SIZE = 50
ROOMS = 16
MIN_DISTANCE = 8
BORDER = 2

def GetEuclidianDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

MAX_TRY = 1000
def GetPoint(l):
    for t in range(MAX_TRY):
        p = [random.randrange(0+BORDER,GRID_SIZE-BORDER), random.randrange(0+BORDER,GRID_SIZE-BORDER)]
        flag = True
        for i in l:
            if GetEuclidianDistance(p, i) <= MIN_DISTANCE:
                flag = False
        if flag:
            return p
    raise Exception("Room couldn't be created. returning error")

def SaveFig(map, name):
    plt.imshow(map, interpolation='none')
    plt.savefig(name)
    plt.clf()

def DecideNeighbor(map, idx, idy):
    if   idx > 0           and map[idx-1, idy] != map[idx, idy]:
        return True
    elif idy > 0           and map[idx, idy-1] != map[idx, idy]:
        return True
    elif idx < GRID_SIZE-1 and map[idx+1, idy] != map[idx, idy]:
        return True
    elif idy < GRID_SIZE-1 and map[idx, idy+1] != map[idx, idy]:
        return True
    else:
        return False

def GetManhattanLine(p1, p2):
    flag = False
    if (p1[0] > p2[0]):
        p1, p2 = p2, p1
        flag = True
    res = []
    if p1[0] == p2[0]: # grad = inf
        for i in range(p1[1], p2[1]+1):
            res.append([p1[0], i])
        return res
    elif p1[1] == p2[1]: # grad = 0
        for i in range(p1[0], p2[0]+1):
            res.append([i, p1[1]])
        return res
    # gradient has value
    grad = (p1[1]+1/2 - (p2[1]+1/2)) / (p1[0]+1/2 - (p2[0]+1/2))

    if grad > 0:
        for idx in range(p1[0], p2[0]+1):
            for idy in range(p1[1], p2[1]+1):
                    g1 = (p1[1]+1/2 - idy)     / (p1[0]+1/2 - (idx+1))
                    g2 = (p1[1]+1/2 - (idy+1)) / (p1[0]+1/2 - idx)
                    
                    if g1 <= grad and grad <= g2:
                        res.append([idx, idy])
                    elif idx == p1[0] and g1 <= grad:
                        res.append([idx, idy])
                    elif idy == p1[1] and g2 >= grad:
                        res.append([idx, idy])
    else:
        for idx in range(p1[0], p2[0]+1):
            for idy in range(p2[1], p1[1]+1):
                g1 = (p1[1]+1/2 - idy) / (p1[0]+1/2 - idx)
                g2 = (p1[1]+1/2 - (idy+1)) / (p1[0]+1/2 - (idx+1))

                if g1 <= grad and grad <= g2:
                    res.append([idx, idy])
                elif idx == p1[0] and g1 <= grad: # TODO : Fix this 
                    res.append([idx, idy])
                elif idy == p2[1] and g2 >= grad:
                    res.append([idx, idy])
            
            
            #elif (idx == p1[0] or idy == p1[1]) and g2 * g1 < 0:
    if flag:
        res.reverse()
    return res

if __name__ == "__main__":
    
    map = np.zeros((GRID_SIZE,GRID_SIZE),dtype=int)

    points = []

    for i in range(ROOMS):
        p = GetPoint(points)
        points.append(p)
        map[p[0],p[1]] = -1
    
    print("Points Generated: %s"%points)
    
    SaveFig(map, "Step_1.png")

    for idx in range(GRID_SIZE):
        for idy in range(GRID_SIZE):
            minidp = 0
            minval = 9999
            for idp in range(ROOMS):
                distance = GetEuclidianDistance(points[idp], [idx, idy])
                if distance < minval:
                    minidp = idp
                    minval = distance
            map[idx, idy] = minidp

    SaveFig(map, "Step_2.png")
    
    rmlist = []
    for idx in range(GRID_SIZE):
        for idy in range(GRID_SIZE):
            if DecideNeighbor(map, idx, idy):
                rmlist.append([idx, idy])
    
    # Finding neighbor
    neighbor = set()
    for idn in range(ROOMS):
        for idm in range(ROOMS):
            if idn == idm:
                continue
            l = GetManhattanLine(points[idn], points[idm])
            emp = set()
            for i in l:
                emp.add(map[i[0], i[1]])
            if len(emp) < 3:
                if idn > idm:
                    idn, idm = idm, idn
                neighbor.add((idn, idm))
    print("neighbors:%s"%neighbor)

    map = np.zeros((GRID_SIZE,GRID_SIZE),dtype=int)
    for i in rmlist:
        map[i[0],i[1]] = 1

    SaveFig(map, "Step_3.png")
    # Make paths

    neighbor = list(neighbor)
    complete = set()
    real_path = set()

    # Add First Path
    rnd_path = neighbor[random.randrange(0,len(neighbor))]
    real_path.add(rnd_path)
    complete.add(rnd_path[0])
    complete.add(rnd_path[1])
    neighbor.remove(rnd_path)
    print("First Path:",rnd_path)
    print("Complete:",complete)


    while len(complete) < ROOMS:
        candidate = []
        for i in neighbor:
            for j in complete:
                if j in i:
                    candidate.append(i)
        # print(candidate)
        rnd_path = candidate[random.randrange(0,len(candidate))]

        real_path.add(rnd_path)
        complete.add(rnd_path[0])
        complete.add(rnd_path[1])
        # print(complete)
        neighbor.remove(rnd_path)
    # print(real_path)

    for r in real_path:
        l = GetManhattanLine(points[r[0]], points[r[1]])
        # k is for temp line
        # k = []
        
        # for i in l:
        #     k.append([i[0], i[1]+1])
        for i in l:
            map[i[0],i[1]] = 0
        # for i in k:
        #     map[i[0],i[1]] = 0

    
    SaveFig(map, "Step_4.png")