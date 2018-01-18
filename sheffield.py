from Tkinter import Tk
from tkFileDialog import askopenfilename


# === Restructuring the map as a dictionary ===
def build_dict(roads,finish):
    
    """
    builds a dictionary containing the nodes as keys and
    the list of roads connected to each node as values
    
    Input:
    
    1. roads - a list of lists (each consisting of two values)
    - the list of roads in the map
    2. finish - a character representing a letter in the Latin
    alphabet - the node that represents the destination. This
    node will not be included as a key in the dictionary.
    
    Output:

    - d - dictionary -a dictionary representing the map.
    """
    
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

# === Building a path ===
def add_next(path,d):

    """
    Adds the next node on a path. Returns the list of all
    possible paths as a list.

    Input:

    1. path - list of characters - a list of nodes with
    path[0] = the start node, to which a node or nodes will
    be added.
    2. d - dictinary - the dictionary representing the map.

    Output:

    - paths - list of lists - the list of possible paths
    that can be constructed from path by adding all possible
    next nodes.
    """
    
    paths = []
    for p in d[path[-1]]:
        if p[1] not in path:
            paths.append(path+[p[1]])
    return paths

# === Checking the end of treatment ===
def check_completed(finish,paths):

    """
    Checks if all paths have reached the destination node.

    Input:

    1. finish - character - the destination node.
    2. paths - list of lists - the list of paths under
    construction.

    Output:

    - a boolean - with the value True if the destination node
    is contained in every path in paths, and False otherwise.
    """
    
    for path in paths:
        if(finish not in path):
            return False
    return True

# === Calculating the Pseudo-measure of a path ===
def pseudo_measure(path):

    """
    Returns the number of villages and towns on a path (not
    including the start and destination nodes) as a tuple.
    The pseudo-measure will be used to differentiate the
    paths whose cost will undoubtedly be too large to be
    included in the final list of paths, thus reducing the
    time and space complexity considerably, while fulfilling
    the aim of our program.
    A larger pseudo-measure for a given path implies that,
    regardless of the number of gold bars, the path will
    always be more or, at best, equally costly compared to
    other paths on the list.

    Input:

    - path - list of characters - a list of nodes which
    starts at the start node and ends at the destination
    node, and represents a path on the map.

    Output:

    - (villages,towns) - (integer,integer) - a tuple
    representing the number of villages and towns on the
    path, without including the start and destination
    nodes.    
    """
    
    villages = 0
    towns = 0
    for i in range(1,len(path)-1):
        if path[i].isupper():
            towns+=1
        else:
            villages+=1
    return villages,towns
    
        
# === Building the list of all relevant paths ===
def build_paths(finish,d,paths):
    
    """
    Builds the list of all relevant paths from the map.
    A "relevant path" is defined as a path whose
    pseudo-measure is not larger than any other path in
    the list, indicating that it has the potential to
    be the least costly path on the map, depending on
    the number of gold bars.
    
    Incomplete paths are systematically removed, as
    well as paths whose pseudo-measure is definitely
    higher.

    The function calls itself recursively until the
    condition "done" is fulfilled, i.e. every path
    in paths has reached the destination.
    
    Input:

    1. finish - character - the destination node.
    2. d - dictionary - the dictionary representing
    the map.
    3. paths - list of lists - the list of paths in
    the map which has to be filled.

    Output:

    - paths - list of lists - the list of paths in
    the map.
    """
    
    done = True
    for path in paths:
        if(finish not in path):
            paths+=add_next(path,d)
            paths.remove(path)   #paths that lead nowhere will be removed automatically as well
            done = False
        else:
            for lane in paths:
                if(lane!=path and finish in lane):
                    if(compare(lane,path)==-1):
                        paths.remove(path)
                    elif(compare(lane,path)==1):
                        paths.remove(lane)
    
    if not done:  
        paths = build_paths(finish,d,paths) #recursive call
    return paths

# === Getting the previous gold bar count ===
def get_total(value,cost):

    """
    Gets total number of gold bars before taxation
    at a town (for a village the calculation is
    straightforward).
    Calls itself recursively until no more cost
    can be added.(new_cost == 0)

    Input:

    1. value - an integer - the gold bar count after
    taxation or from a previous iteration of the function.
    2. cost - an integer - the amount of tax from a
    previous iteration of the function, calculated as the
    value/20 rounded up. It's initialized to zero when the
    function is called for the first time.

    Output:

    - an integer - the total number of gold bars before
    taxation, calculated as the sum of value and the
    final cost(amount of taxation).
    """
    a = value//20
    b = value%20
    new_cost = a - cost
    if(b!=0):
        new_cost+=1
    if(new_cost!=0):
        return get_total(value+new_cost,new_cost+cost) #recursive call
    else:
        return value+new_cost

# === Comparing the pseudo-measures of two paths ===
def compare(p1,p2):

    """
    Compares two paths by pseudo-measure and returns 1
    if p1 is more costly than p2, -1 if p1 is less costly
    than p2 and 0 if it's undecided.
    The comparison rules were inferred from mathematical
    formulas that are shown and explained in the document
    "Mathematics of Sheffield".

    Input:

    1. p1 - a path
    2. p2 - another path

    Output:

    - an integer - whose value = 1 if p1 > p2 ,
    -1 if p1 < p2 and 0 if neither can be definitely
    shown to be larger or smaller in terms of cost.
    """
    
    m,n = pseudo_measure(p1)
    mprime,nprime = pseudo_measure(p2)

    if(m<=mprime and n==0):
        return -1
    elif(mprime<m and nprime==0):
        return 1
    elif(m==0 and mprime==0):
        if(n<=nprime):
            return -1
        else:
            return 1
    elif(m==0 and n<=nprime and 18*mprime>=19*n):
        return -1        
    elif(mprime==0 and nprime<=n and 18*m>=19*nprime):
        return 1
    elif(mprime == 1 and m==1):
        if(n<nprime):
            return -1
        elif(nprime<n):
            return 1
    elif(n==1 and nprime==1 and m<=mprime):
        if(mprime-m>=1+(mprime-1)/20):
            return -1
        elif(m>=19 and mprime-m<=(m+1)/20+1):
            return 1
    elif(m==1 and n==0 and mprime==0 and nprime==1):
        return -1
    elif(m==0 and n==1 and mprime==1 and nprime==0):
        return 1
    else:
        return 0
        

# === Calculating the lowest number of gold bars ===
def cheapest(paths,gold_bars):

    """
    Returns the total number of gold bars needed at the
    starting position, if the path with the lowest cost
    is taken.
    Checks every path in paths, calculates its gold bar
    total and returns the minimum.

    lowest = 1535
    the above line would cause trouble if the number of
    final gold bars exceeded 1000 and/or the number of
    towns and villages was more than 26 each.
    A detailed explanation for how the exact value was
    obtained is in the document "Mathematics of Sheffield"

    Input:

    1. paths - list of lists - list of relevant paths on
    the map
    2. gold_bars - integer - number of gold bars at the
    destination.

    Output:

    - lowest - integer - minimum number of gold bars needed
    to reach the destination.
    """
    
    if(len(paths)==0):
        return gold_bars
    else:
        lowest = 2000
        for path in paths:
            total = gold_bars
            for i in range(1,len(path)):
                if(path[-i].isupper()):
                    total = get_total(total,0)
                else:
                    total+=1
            if(total<lowest):
                lowest = total
                    
        return lowest

# === Main section of the program ===
if(__name__=='__main__'):

    """
    In this section, the program will get the delivery
    file needed for treatment, using Tkinter so the user
    can browse for the file they want.
    It will then parse the file and print error or
    warning messages when its structure does not follow
    the expectation.
    

    If everything is okay, the program will get the
    values of:

    1. delivery_file - string - path of the file to
    be treated.
    2. case_number - integer - this will be incremented
    with each new case.
    3. road_count - integer - the number of roads in
    the map. This variable is redundant, and will only
    be useful to check if the file structure is correct,
    so the user would get the result they likely expect.
    4. roads - a list of lists each having two values,
    each representing a character of the Latin alphabet
    - list of roads on the map. Each road is a connection
    between two nodes, and each node can be a towns or a
    village.
    5. gold_bars - integer - the number of gold bars to be
    delivered to the destination
    6. start and finish - two characters - these are
    retrieved from lines with two character values

    Additional variables used:

    7. d - dictionary - a dictionary representing the
    map, which is calculated using build_dict function
    8. treated - boolean - set to False when a new
    treatment starts, and to True when it's finished
    without incident. If there's a file stucture problem,
    it is used to ensure that we do not proceed with the
    next case until we deal with potential errors and the
    previous case is done.
    9. paths - list of lists - will contain the relevant
    paths in the map.


    -- If an error found, the program will print the
    error message, and exit. Only the results of cases
    treated until the error line will be shown on the
    console.
    The user has to fix the problem, and then launch the
    program once again to obtain the rest of the results.

    --- List of errors:

    - road_count is negative or equal to zero.
    - road_count is not an integer.
    - a general error when adding a new value to the
    list of roads.
    - a node (town or village) is not represented by a
    letter from the Latin alphabet.
    - a road lists the same node as its start and finish,
    e.g. A A or b b.
    - the number of gold bars is negative or zero.
    - the number of gold bars exceeds 1000.
    - the value entered for gold_bar is not an integer.
    - the number of space-saparated values on a given
    line is either 0 or larger then 3.
    - general error if the function call of build_dict
    or build_paths fails or generates an error for an
    unexpected reason.
    
    -- A warning message is shown if the structure of
    the file is incorrect, but the problem would not affect
    the treatment of the cases. For example: if the road
    count is missing, the program can still calculate it
    by counting the number of listed roads.
    -- If the -1 at the end of file is not included,
    the program will not do anything, since its presence
    or lack thereof does not affect its execution.
    

    --- List of warnings:

    - Road_count is probably missing, but otherwise all data
    can be retrieved and treated.
    - The road_count (intended number of roads) listed does
    not match the number of roads retrieved from the file
    for a given case. The program will use the length of the
    road list as the actual road count.
    
    
    """
    
    case_number  = 0
    treated = False
    #to avoid opening the main window -->
    Tk().withdraw() 
    delivery_file = askopenfilename()
    #reading the file, loading the input for treatment -->
    with open(delivery_file,'r') as delivery:
        for i,line in enumerate(delivery):
            x = line.strip().split()
            if(len(x)==1):
                if(x[0]!="-1"):
                    try:
                        road_count = int(x[0])
                        if(road_count<=0):
                            print("Delivery file structure is incorrect at line {}. The number of roads should not be negative or zero!".format(i+1))
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
                if(x[0]==x[1]):
                    print("Delivery file structure is incorrect at line {}. A road should not start and end at the same node!".format(i+1))
                    break
                try:
                    roads.append([x[0],x[1]])
                except Exception,e:
                    print("Delivery file structure is incorrect at line {}.".format(i+1))
                    print(str(e))
                    break
            elif(len(x)==3):
                try:
                    gold_bars = int(x[0])
                    if(gold_bars<=0):
                        print("Delivery file structure is incorrect at line {}. The number of gold bars should not be negative or zero!".format(i+1))
                        break
                    elif(gold_bars>1000):
                        print("The use of a gold bars number exceeding 1000 is not accepted!")
                        break
                    
                except Exception,e:
                    print("Delivery file structure is incorrect at line {}! The number of gold bars must be an integer!".format(i+1))
                    print(str(e))
                    break
                if(not (x[1].isalpha() and x[2].isalpha())):
                    print("Delivery file structure is incorrect at line {}. Towns and villages should be represented with letters!".format(i+1))
                    break
                if(road_count!=len(roads)):
                    print("case {}: Warning! The declared number of roads does not \nmatch the road list count! {} vs {}".format(case_number,road_count,len(roads)))

                try:
                    #a direct path between the starting and finishing
                    #positions is always the best -->
                    if([x[1],x[2]] in roads or [x[2],x[1]] in roads): 
                        paths = [[x[1],x[2]]]
                    else:
                        d = build_dict(roads,x[2])
                        paths = build_paths(x[2],d,d[x[1]])
                
                    print("case {}: {}".format(case_number,cheapest(paths,gold_bars)))
                except Exception,e:
                    print("Unexpected behavior at line {}. Please check the structure of the file!".format(i+1))
                    print(str(e))
                roads = []
                treated = True
                
            else:
                print("Delivery file structure is incorrect at line {}. Too many values or too few!".format(i+1))
                break

