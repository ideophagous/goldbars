def add_node(finish,roads,path,paths):
    pass
    '''initial_path = path
    for road in roads:
        if((road[0]==path[-1]) and (road[1] not in path)):
            path.append(road[1])
            if(path[-1]==finish):
                print(path)
                paths.append(path)
                return paths,initial_path
            else:
                paths, initial_path=add_node(finish,roads,path,paths)
                
            
        elif((road[1]==path[-1]) and (road[0] not in path)):
            path.append(road[0])
            if(path[-1]==finish):
                print(path)
                paths.append(path)
                return paths,initial_path
            else:
                paths, initial_path = add_node(finish,roads,path,paths)
                
    return paths,initial_path'''


#building the list of all paths in the map from the source to the destination
'''def build_paths(start,finish,roads):
    print("start: "+start)
    print("finish: "+finish)
    #print("roads: "+str(roads))
    if(len(roads)==0):
        return []
    paths = []
    path = [start]
    for road in roads:
        #print(road)
        if(road[0]==start):
            path.append(road[1])
            if(path[-1]==finish):
                paths.append(path)
                path = [start]
            else:
                paths,initial_path =add_node(finish,roads,path,paths)
                print(initial_path)
                path = [start]
            
        elif(road[1]==start):
            path.append(road[0])
            if(path[-1]==finish):
                paths.append(path)
                path = [start]
            else:
                paths,initial_path= add_node(finish,roads,path,paths)
                print(initial_path)
                path = [start]
    return paths'''


def build_dict(roads,finish):
    nodes = set()
    for road in roads:
        nodes.add(road[0])
        nodes.add(road[1])
    nodes.remove(finish)
    nodes = list(nodes)
    d = {}
    for node in nodes:
        l = []
        for road in roads:
            if(road[0]==node):
                l.append(road)
            elif(road[1]==node):
                
                l.append(road[::-1]) #append the road in reverse order so the current node would be first
                
        d.update({node:l})
    return d

def add_next(path,d):
    paths = []
    for p in d[path[-1]]:
        if p[1] not in path:
            paths.append(path+[p[1]])
    return paths

def check_completed(finish,paths):
    for path in paths:
        if(finish not in path):
            return False
    return True

#checks if a path without the start position is a subpath of another path
def pseudo_subpath(p1,p2):
    i = 1
    while(i<len(p1)):
        while(j<len(p2)-len(p1)):
    

#remove inefficient paths, i.e. paths where at least one town or village is superfluous (can be avoided by taking a different path)
def reduced(paths):
    print("----------------")
    paths.sort(key = len) #sorting the paths by length
    i=0
    while i<len(paths):
        j=i+1
        while j<len(paths):            
            contained = True
            for k in range(1,len(paths[i])-1):
                    if(paths[i][k] not in paths[j]):
                        contained = False
            if(contained):
                del paths[j]
                j-=1
            print(paths)
            j+=1
        i+=1
            
    return paths
                    
        

def build_paths(finish,d,paths):
    done = True
    print(paths)
    for path in paths:
        if(finish not in path):
            paths+=add_next(path,d)
            paths.remove(path)   #paths that lead nowhere will be removed automatically as well
            done = False
    
    if not done:  
        paths = build_paths(finish,d,paths) #recursive call
    return paths

def get_total(value,cost):
    a = value//20
    b = value%20
    new_cost = a - cost
    if(b!=0):
        new_cost+=1
    if(new_cost!=0):
        return get_total(value+new_cost,new_cost+cost)
    else:
        return value+new_cost


def cheapest(paths,gold_bars):
    if(len(paths)==0):
        return gold_bars
    else:
        potentials = []
        for path in paths:
            total = gold_bars
            for i in range(1,len(path)):
                if(path[-i].isupper()):
                    total = get_total(total,0)
                else:
                    total+=1
            potentials.append(total)
                    
        return min(potentials)

if(__name__=='__main__'):    
    case_number  = 0
    gb_number = 0 #number of gold bars required to reach destination
    treated = False
    #reading the file, loading the input for treatment
    with open("delivery.txt",'r') as delivery:
        for i,line in enumerate(delivery):
            x = line.strip().split()
            if(len(x)==1):
                if(x[0]!="-1"):
                    try:
                        road_count = int(x[0])
                        if(road_count<0):
                            print("Delivery file structure is incorrect at line {}. The number of roads should not be negative!".format(i+1))
                            break
                    except Exception,e:
                        print("Delivery file structure is incorrect at line {}. Road count should be an integer value!".format(i+1))
                        print(str(e))
                        break
                    case_number+=1
                    roads = []
                    treated =  False
                else:
                    break
            elif(len(x)==2):
                if(treated):
                    road_count = 0
                    case_number+=1
                    treated = False
                    print("Warning: Delivery file structure is incorrect at line {}. Road count for case {} is probably missing!".format(i+1,case_number))
                if(not (x[0].isalpha() and x[1].isalpha())):
                    print("Delivery file structure is incorrect at line {}. Towns and villages should be represented with letters!".format(i+1))
                    break
                try:
                    roads.append([x[0],x[1]])
                except Exception,e:
                    print("Delivery file structure is incorrect at line {}. Road count is probably missing!".format(i+1))
                    print(str(e))
                    break
            elif(len(x)==3):
                try:
                    gold_bars = int(x[0])
                    if(gold_bars<0):
                        print("Delivery file structure is incorrect at line {}. The number of gold bars should not be negative!".format(i+1))
                        break
                    
                except Exception,e:
                    print("Delivery file structure is incorrect at line {}!".format(i+1))
                    print(str(e))
                    break
                if(not (x[1].isalpha() and x[2].isalpha())):
                    print("Delivery file structure is incorrect at line {}. Towns and villages should be represented with letters!".format(i+1))
                    break
                if(road_count!=len(roads)):
                    print("case {}: Warning! The declared number of roads does not \nmatch the road list count! {} vs {}".format(case_number,road_count,len(roads)))
                
                d = build_dict(roads,x[2])
                paths = build_paths(x[2],d,d[x[1]])
                paths = reduced(paths)
                print("paths :{}".format(paths))
                
                print("case {}: {}".format(case_number,cheapest(paths,gold_bars)))
                roads = []
                treated = True
            else:
                print("Delivery file structure is incorrect at line {}. Too many values or too few!".format(i+1))
                break

