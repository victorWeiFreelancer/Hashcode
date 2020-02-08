import sys
import math
from time import gmtime, strftime
sys.dont_write_bytecode = True

def distance(startR, startC, endR, endC):
    return abs(startR - endR) + abs(startC - endC)

def priority(rideL, bonus, wait, distArrive):
    return (rideL+bonus)/(1+distArrive)/(1+wait)

def priorityFleetTakeRide(fleet, ride, B):
    disToStartPoint = distance(fleet[0], fleet[1], ride[0], ride[1])
    fleetCanArriveAt = fleet[2] + disToStartPoint
    if fleetCanArriveAt + ride[6] > ride[5]:
        # if ride can't finish on time, give lowest score
        return [0, 0]
    if fleetCanArriveAt <= ride[4]:
        # can arrive on time
        FleetArriveAndWaitTime = ride[4] - fleetCanArriveAt
        return [priority(ride[6], B, FleetArriveAndWaitTime, disToStartPoint), disToStartPoint + ride[6]]
    else:
        ClientWaitTime = fleetCanArriveAt - ride[4]
        return [priority(ride[6], 0, ClientWaitTime, disToStartPoint), disToStartPoint + ride[6]]

def bestFleetForRide(fleets, ride, B):
    max = 0
    best = 0
    bestFleetFinish = 0
    for i, f in enumerate(fleets):
        score, finishTime = priorityFleetTakeRide(f, ride, B)
        if score > max:
            max = score
            best = i
            bestFleetFinish = finishTime
    return [max, best, bestFleetFinish]


def iParent(i):
    return (i-1)//2

def iLeftChild(i):
    return 2*i + 1

def iRightChild(i):
    return 2*i + 2

def siftDown(h, start):
    end = len(h)
    root = start
    while iLeftChild(root) < end:
        child = iLeftChild(root)
        swap = root
        if h[swap][1] < h[child][1]:
            swap = child 
        if child+1 < end and h[swap][1] < h[child+1][1]:
            swap = child+1
        if swap == root:
            return
        else:
            h[root], h[swap] = h[swap], h[root]
            root = swap

def siftUp(h, end):
    child = end
    while child > 0:
        parent = iParent(child)
        if h[parent][1] < h[child][1]:
            h[parent], h[child] = h[child], h[parent]
        else:
            return

def heapify(h):
    l = len(h)
    start = iParent(l-1)
    while start >=0:
        siftDown(h, start)
        start -= 1


def scheduling(schedule, fleets, rides, F, N, B, T):
    RidesHeap = []
    for r in range(N):
        max, f, finishDuration = bestFleetForRide(fleets, rides[r], B)
        RidesHeap.append([r, max, f, finishDuration])
    heapify(RidesHeap)
    # print(RidesHeap)
    # fleetToTake = RidesHeap[0][2]
    
    while len(RidesHeap)>0 and RidesHeap[0][1]>0:
        # print(len(RidesHeap))
        schedule[RidesHeap[0][2]].append(RidesHeap[0][0])
        fleetToTake = RidesHeap[0][2]
        print(f"fleet to take {fleetToTake}, ride taken {RidesHeap[0][0]}")
        # update the fleet that takes the ride at top of the heap
        fleets[fleetToTake][0] = rides[RidesHeap[0][0]][2]
        fleets[fleetToTake][1] = rides[RidesHeap[0][0]][3]
        fleets[fleetToTake][2] += RidesHeap[0][3]
        RidesHeap[-1],  RidesHeap[0] =  RidesHeap[0], RidesHeap[-1]
        del RidesHeap[-1]
        siftDown(RidesHeap, 0)
        for i, h in enumerate(RidesHeap):
            if fleetToTake != h[2]:
                score, finishTime = priorityFleetTakeRide(fleets[fleetToTake], rides[h[0]], B)
                # print(f"score {score}, h[1] {h[1]}")
                if score > h[1]:
                    h[1] = score
                    h[2] = fleetToTake
                    h[3] = finishDuration
                    siftUp(RidesHeap, i)
            else:
                update_max, update_f, update_duration = bestFleetForRide(fleets, rides[h[0]], B)
                h[1] = update_max
                h[2] = update_f
                h[3] = update_duration
        # heapify(RidesHeap)

def main():
    Rides = []
    Fleets = []
    Schedule = []
    # print(sys.argv)
    startT = strftime("%H:%M:%S", gmtime())
    if(len(sys.argv)==1):
        R, C, F, N, B, T = list(map(int, input().split()))
        for i in range(F):
            # fleet [posR, posC, nextAvailableTime]
            Fleets.append([0, 0, 0])
            Schedule.append([i+1])
        for i in range(N):
            # each ride is a list [startR, startC, endR, endC, earliestStart, latestEnd, distance, score]
            Rides.append(list(map(int, input().split())))
            Rides[i].append(distance(Rides[i][0], Rides[i][1], Rides[i][2], Rides[i][3]))
        scheduling(Schedule, Fleets, Rides, F, N, B, T)
        for s in Schedule:
            print(" ".join(map(str, s)))
    else:
        with open(sys.argv[1], 'r') as fo:
            R, C, F, N, B, T = list(map(int, fo.readline().split()))
            for i in range(F):
                # fleet [posR, posC, nextAvailableTime]
                Fleets.append([0, 0, 0])
                Schedule.append([i+1])
            for i in range(N):
                # each ride is a list [startR, startC, endR, endC, earliestStart, latestEnd, distance, score]
                Rides.append(list(map(int, fo.readline().split())))
                Rides[i].append(distance(Rides[i][0], Rides[i][1], Rides[i][2], Rides[i][3]))
        scheduling(Schedule, Fleets, Rides, F, N, B, T)
        finishT = strftime("%H:%M:%S", gmtime())
        fw = open(" ".join([sys.argv[1].split('.')[0], startT, finishT, ".out"]),'w')
        for s in Schedule:
            fw.write(" ".join(map(str, s))+'\n')


if __name__ == '__main__':
    main()