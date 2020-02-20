import sys
import math
from time import gmtime, strftime
sys.dont_write_bytecode = True

class Video:
    def __init__(self, id, size, cached=False):
        super().__init__()
        self.id, self.size, self.cached = id, size, cached
        self.requestFromEP = {} # { endPointId: requestedNumber }
        self.cacheUtilityMap = {}   # { cacheId : utility }
        self.prefCacheList = []
    def __str__(self):
        return str(self.id)
    def __repr__(self):
        return str(self.id)


class Cache:
    def __init__(self, id, cap=math.inf):
        super().__init__()
        self.id, self.cap = id, cap
        self.prefVideoList = []
        self.videoUtilityMap = {}
        self.videos = []
        self.endPointLatency = {} # { endPointId : latency}
    def __str__(self):
        return str(self.id) + " " + " ".join(map(str, self.videos))
    def __repr__(self):
        return str(self.id) + " " + " ".join(map(str, self.videos))


class Endpoint:
    def __init__(self, id, latency, numCache):
        super().__init__()
        self.id, self.centerLatency, self.numCache = id, latency, numCache
        self.cachMapList = []
        self.reqs = {} # { videoId : requestedNumber}
    def __str__(self):
        return "Endpoint " + str(self.id) + " ".join(self.caches)
    def __repr__(self):
        return "Endpoint " + str(self.id) + " ".join(self.caches)

class Request:
    def __init__(self, videoId, endPointId, times):
        super().__init__()
        self.videoId, self.endPointId, self.times = videoId, endPointId, times
    def __str__(self):
        return "Request video" + str(self.videoId) + " from endpoint " + str(self.endPointId) + " for " + str(self.times) + " times"
    def __repr__(self):
        return "Request video" + str(self.videoId) + " from endpoint " + str(self.endPointId) + " for " + str(self.times) + " times"

def readInput(videos, endPoints, requests, caches):
    if(len(sys.argv)==1):
        V, E, R, C, X = list(map(int, input().split()))
        videoSizes = list(map(int, input().split()))
        for i, vs in enumerate(videoSizes):
            videos.append(Video(i, vs))
        for i in range(C):
            caches.append(Cache(i, X))
        centerCache = Cache(C)
        caches.append(centerCache)
        for i in range(E):
            endPointInfo = list(map(int, input().split()))
            ep = Endpoint(i, endPointInfo[0], endPointInfo[1])
            for j in range(ep.numCache):
                cacheInfo = list(map(int, input().split()))
                ep.cachMapList.append( [cacheInfo[0], cacheInfo[1]] )
                caches[cacheInfo[0]].endPointLatency[i]=cacheInfo[1]
            endPoints.append(ep)
            caches[C].endPointLatency[i]=ep.centerLatency
        for _ in range(R):
            rInfo = list(map(int, fo.readline().split()))
            r = Request( rInfo[0], rInfo[1], rInfo[2] )
            requests.append( r )
            if r.videoId not in endPoints[r.endPointId].reqs:
                endPoints[r.endPointId].reqs[r.videoId]=r.times
            else:
                endPoints[r.endPointId].reqs[r.videoId]+=r.times
            if r.endPointId not in videos[r.videoId].requestFromEP:
                videos[r.videoId].requestFromEP[r.endPointId] = r.times
            else:
                videos[r.videoId].requestFromEP[r.endPointId] += r.times
    else:
        with open(sys.argv[1], 'r') as fo:
            V, E, R, C, X = list(map(int, fo.readline().split()))
            videoSizes = list(map(int, fo.readline().split()))
            for i, vs in enumerate(videoSizes):
                videos.append(Video(i, vs))
            for i in range(C):
                caches.append(Cache(i, X))
            centerCache = Cache(C)
            caches.append(centerCache)
            for i in range(E):
                endPointInfo = list(map(int, fo.readline().split()))
                ep = Endpoint(i, endPointInfo[0], endPointInfo[1])
                for j in range(endPointInfo[1]):
                    cacheInfo = list(map(int, fo.readline().split()))
                    ep.cachMapList.append( [cacheInfo[0], cacheInfo[1]] )
                    caches[cacheInfo[0]].endPointLatency[i]=cacheInfo[1]
                endPoints.append(ep)
                caches[C].endPointLatency[i]=ep.centerLatency
            for _ in range(R):
                rInfo = list(map(int, fo.readline().split()))
                r = Request( rInfo[0], rInfo[1], rInfo[2] )
                requests.append( r )
                if r.videoId not in endPoints[r.endPointId].reqs:
                    endPoints[r.endPointId].reqs[r.videoId]=r.times
                else:
                    endPoints[r.endPointId].reqs[r.videoId]+=r.times
                if r.endPointId not in videos[r.videoId].requestFromEP:
                    videos[r.videoId].requestFromEP[r.endPointId] = r.times
                else:
                    videos[r.videoId].requestFromEP[r.endPointId] += r.times
    return V, E, R, C, X

def buildPrefList(videos, endPoints, requests, caches):
    # print("videos prefs for caches")
    for v in videos:
        for epId in v.requestFromEP:
            for c in endPoints[epId].cachMapList:
                if c[0] not in v.cacheUtilityMap:
                    v.cacheUtilityMap[c[0]] = ( endPoints[epId].centerLatency - c[1] )*v.requestFromEP[epId]/v.size
                else:
                    v.cacheUtilityMap[c[0]] += ( endPoints[epId].centerLatency - c[1] )*v.requestFromEP[epId]/v.size
        v.prefCacheList.extend([ [k, v] for k, v in v.cacheUtilityMap.items() ])
        v.prefCacheList.sort( key = lambda cl:cl[1], reverse=True) 
        # print("video", v.id, v.prefCacheList)
    # print("caches prefs for videos")
    for c in caches:
        for epId in c.endPointLatency:
            for v in endPoints[epId].reqs:
                if v not in c.videoUtilityMap:
                    c.videoUtilityMap[v] = ( endPoints[epId].centerLatency - c.endPointLatency[epId])*endPoints[epId].reqs[v]/videos[v].size
                else:
                    c.videoUtilityMap[v] += ( endPoints[epId].centerLatency - c.endPointLatency[epId])*endPoints[epId].reqs[v]/videos[v].size
        c.prefVideoList.extend( [ [k, v] for k, v in c.videoUtilityMap.items()] )
        c.prefVideoList.sort(key = lambda vu:vu[1], reverse=True)
        # print("cache", c.id, c.prefVideoList)
    # for c in caches:
    #     for ep in c.endPointLatency:
    #     utility = endPointLatency

def cacheLoad(videos, cache):
    return sum([ videos[v].size for v in cache.videos ])

def stableMatching(videos, endPoints, requests, caches):
    while( any( (not v.cached) and len(v.prefCacheList)>1 for v in videos ) ):
        vToCache = next( v for v in videos if (not v.cached) and len(v.prefCacheList)>1 )
        firstMatchCache = caches[ vToCache.prefCacheList[0][0] ] 
        # print(firstMatchCache)
        cLoad = cacheLoad(videos, firstMatchCache)
        vToCacheIndex = next( v[0] for v in firstMatchCache.prefVideoList if v[0]==vToCache.id )
        if cLoad + vToCache.size <= firstMatchCache.cap:
            firstMatchCache.videos.append(vToCache.id)
            for i in range(len(firstMatchCache.prefVideoList)-1, vToCacheIndex, -1):
                vToDeleteId = firstMatchCache.prefVideoList.pop(i)[0]
                videos[vToDeleteId].prefCacheList.remove([firstMatchCache.id, videos[vToDeleteId].cacheUtilityMap[firstMatchCache.id]])
            vToCache.cached = True
        else:
            # compare utility
            accumU = 0
            accumSize = 0
            for i in range( len(firstMatchCache.videos) - 1, -1):
                accumU += firstMatchCache.videoUtilityMap[firstMatchCache.videos[i]]
                vISize = videos[firstMatchCache.videos[i]].size
                accumSize += vISize
                if vToCache.prefCacheList[0][1] >= accumU:
                    if ( cLoad + vToCache.size - accumSize )<= firstMatchCache.cap:
                        vToPopId = firstMatchCache.videos.pop(i)
                        videos[vToPopId].cached = False
                        videos[vToPopId].prefCacheList.remove(firstMatchCache.id)
                        if not vToCache.cached:
                            vToCache.cached = True
                            firstMatchCache.videos.append(vToCache.id)
                    else:
                        break
                else:
                    break          
            if not vToCache.cached:
                for i in range(len(firstMatchCache.prefVideoList)-1, vToCacheIndex-1, -1):
                    vToDeleteId = firstMatchCache.prefVideoList.pop(i)[0]
                    videos[vToDeleteId].prefCacheList.remove([firstMatchCache.id, videos[vToDeleteId].cacheUtilityMap[firstMatchCache.id]])
                del vToCache.prefCacheList[0]

def main():
    videos = []
    endPoints = []
    requests = []
    caches = []
    startT = strftime("%H:%M:%S")
    V, E, R, C, X = readInput(videos, endPoints, requests, caches)

    buildPrefList(videos, endPoints, requests, caches)

    stableMatching(videos, endPoints, requests, caches)

    finishT = strftime("%H:%M:%S")
 
    # finishT = strftime("%H:%M:%S")
    fw = open(" ".join([sys.argv[1].split('.')[0], startT, finishT, ".out"]),'w')
    numUsedCache = sum(1 for c in caches[0:-1] if len(c.videos)>0 )
    fw.write( str(numUsedCache)+'\n')
    for c in caches[0:-1]:
        if len(c.videos)>0:
            fw.write( str(c.id)+" " + " ".join(map(str, c.videos))+'\n')


if __name__ == '__main__':
    main()