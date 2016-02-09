
import sys;
import copy;
import os.path;
class Node:

    currsymbol = "";
    currValue = 0;
    level = 0;
    childNode = "";
    maxValue = -999;
    minValue = 999;


    def Node(self, Value, level):
        #self.currValue = Value;
        self.level = level;

# function to get the final list of nodes to conquer from a given position.
def opponentNodes(finalpos,playerSym,positions):
    finalstates = list();
    finalstates.append(finalpos);
    finalneighbor = adjacentPos(finalpos);
    finalvalid = validOpp(finalneighbor,finalpos, playerSym, positions);
    for i in finalvalid:
        finalstates.append(i);
    return finalstates;

def display(arg1):
    for keys in arg1:
        print arg1[keys];
# function to get the position of players on the grid, arg : position dictinory , symb : player symbol
def playerpos(arg, symb):
      playerPos = list();
      for keys in arg:
        for j in range(5):
            if(arg[keys][j] == symb):
                playerPos.append(keys + str(j));
      return playerPos;

# function to get maximum value from the grid
def maxEmptyValue(arg):
    emptyPositions= playerpos(arg, '*');
    maxvalue = 0;
    maxindex = list();
    for j in emptyPositions:
        if( values[j[0]][int(j[1])] >= maxvalue ):
            maxvalue = values[j[0]][int(j[1])];

    for i in emptyPositions:
         if( values[i[0]][int(i[1])] == maxvalue ):
             maxindex.append(i);

    maxIndexVal = minIndex(maxindex);
    return maxIndexVal;

# function to get the minimum index according to the positional ordering.
def minIndex(list):
    minright = 4;
    minimum = 'E5';
    for k in list:
        if(int(k[1]) < minright):
            minimum = k;
            minright = int(k[1]);
        elif(int(k[1]) == minright):
            if(minimum > k[0]):
                minimum = k;

    return minimum;

def positionalList(content):
    count = len(content);
    sortedlist = list();
    for i in range(count):
        j = minIndex(content);
        content.remove(j);
        sortedlist.append(j);
    return sortedlist;

# function to get the sum of values from player position on the board  arg: list of Player positions on the grid
def posValues(arg):
    value = 0;
    for i in arg:
        value += values[i[0]][int(i[1])];
    return value;

# function to find the adjacent positions of a square
def adjacentPos(square):

    poskey = square[0];
    posindex =  int(square[1]);

    # Get the top position
    if( posindex > 0):
        toppos = poskey + str(posindex - 1);
    else:
        toppos =  poskey + str(posindex);

    #Get the bottom position
    if(posindex < 4):
      bottompos = poskey + str(posindex + 1);
    else:
      bottompos =  poskey + str(posindex);

    leftposindex = chr(ord(poskey) - 1);
    rightposindex = chr(ord(poskey) + 1);

    # left position
    if (poskey == 'A'):
        leftpos = poskey + str(posindex)
    else:
        leftpos = leftposindex + str(posindex);

    #position
    if(poskey == 'E'):
        rightpos = poskey + str(posindex);
    else:
        rightpos = rightposindex + str(posindex);

    positions = list();
    positions =(leftpos,rightpos,toppos,bottompos);
    return  list(positions);

# function to get only those positions where we can keep our player in the free grid.
def validAdjacent(Neighbors, currentpos,positions):
        validNeighbors = list();
        for i in Neighbors:
            if(i == currentpos):
              continue;
            elif ( positions[i[0]][int(i[1])] == 'X' or positions[i[0]][int(i[1])] == 'O'):
              continue;
            else:
              validNeighbors.append(i);
        return validNeighbors;

# function to remove redudant valid positions.
def freePos(playerPos,positions):
    validNeighbors = list();
    for i in playerPos:
        Neighbors = adjacentPos(i);
        valid = validAdjacent(Neighbors, i,positions);
        for j in valid:
            if j not in validNeighbors:
                validNeighbors.append(j);

    return validNeighbors;

# function to get valid neighbors
def validOpp(neighbors, currentpos, playersym, positions):
     validOpponent = list();
     for j in neighbors:
            if (j == currentpos):
                continue;
            elif ( positions[j[0]][int(j[1])] == playersym or positions[j[0]][int(j[1])] == '*' ):
                 continue;
            else:
                validOpponent.append(j);
     return validOpponent;

# function to write to output file.
def filewrite(pos , f):

    if(algoChoice == 4):
        return;
    output = {};
    intermediate = positions;
    for i in pos:
        intermediate[i[0]][int(i[1])] = playerSym.rstrip('\r');

    for key in (sorted(intermediate)):
         for j in range (5):
             if j not in output:
                 output[j] = list();
             output[j].append(positions[key][j]);

    for key in sorted(output):
        line = "";
        line = str(output[key]);
        line = line.strip('[');
        line = line.strip(']');
        line = line.replace(',', '');
        line = line.replace('\'', '');
        line = line.replace(' ', '');
        line = line.rstrip('\r');
        line += "\n";
        f.write(line);


def tracelog(pickedPos, playerSym, positions):


    output = {};
    intermediate = copy.deepcopy(positions);
    for i in pickedPos:
        intermediate[i[0]][int(i[1])] = playerSym.rstrip('\r');


    for key in (sorted(intermediate)):
         for j in range (5):
             if j not in output:
                 output[j] = list();
             output[j].append(intermediate[key][j]);

    for key in sorted(output):
        line = "";
        line = str(output[key]);
        line = line.strip('[');
        line = line.strip(']');
        line = line.replace(',', '');
        line = line.replace('\'', '');
        line = line.replace(' ', '');
        line = line.rstrip('\r');
        line += "\n";
        trace.write(line);


# function to output the file as it is.
def noWrite():
    if(algoChoice == 4):
        return;

    f = open ('next_state.txt', 'w');
    output = {};
    intermediate = positions;
    for key in (sorted(intermediate)):
         for j in range (5):
             if j not in output:
                 output[j] = list();
             output[j].append(positions[key][j]);


    for key in sorted(output):
        line = "";
        line = str(output[key]);
        line = line.strip('[');
        line = line.strip(']');
        line = line.rstrip('\r');
        line = line.replace(',', '');
        line = line.replace('\'', '');
        line = line.replace(' ', '');
        line += "\n";
        f.write(line);

    f.close();

# function to write to the traverse log
def traverselogwrite(Node , Depth , Value):

     if(algoChoice == 4):
        return;
     line = str(Node) + "," + str(Depth) + "," + str(Value) + "\n";
     line.rstrip('\r');
     traverse.write(line.strip('\r'));


def log(Node , Depth , Value, Alpha, Beta):

     if(algoChoice == 4):
        return;
     line = str(Node) + "," + str(Depth) + "," + str(Value) + "," + str(Alpha)+ "," + str(Beta) + "\n";
     line.rstrip('\r');
     logfile.write(line.strip('\r'));


# function to get the sneek positions.
def getSneekPositions(raidPositions):
     sneekpositions = list();
     empty = playerpos(positions , '*');
     for i in raidPositions:
        empty.remove(i);

     return sorted(empty);

def isempty(playersym, otherplayer,positions):

    # If there are no more moves left
    emptypos = playerpos(positions, '*');
    return  len(emptypos);

def evalCalculation1(level, cutoff, playersym, otherplayer, node, locations):

    myPlayerPositions = playerpos(locations, playersym);
    myPlayerVal = posValues(myPlayerPositions);

    opponentPlayerPositions = playerpos(locations, otherplayer);
    opponentPlayerVal =  posValues(opponentPlayerPositions);

    emptyPositions = playerpos(locations , '*');
    raidPositions = freePos(myPlayerPositions,locations);
    sneekPositions = getSneekPositions(raidPositions);


    # Get the list of positions in positional ordering.
    sortedList = positionalList(emptyPositions);
    evallist = {};


    # if it has reached the sorted list then the leave nodes have to be checked for positional ordering.
    for i in sortedList:
    # Check if i belongs to raid position or sneek position.

            if (i in raidPositions):
                # Compute the eval value if it is in the raid position
                value = myPlayerVal + values[i[0]][int(i[1])];
                opponentNeighbors = adjacentPos(i);
                validOpponent = validOpp(opponentNeighbors, i,playersym,locations);

                tmpOpponent = opponentPlayerVal;
                for j in validOpponent:
                        value += values[j[0]][int(j[1])];
                        tmpOpponent -= values[j[0]][int(j[1])];



                if(level % 2 == 1):
                        evalValue = value - tmpOpponent;
                elif (level % 2 == 0):
                        evalValue = tmpOpponent - value;

                # Create a dictionary to hold eval values of all the moves
                if evalValue not in evallist:
                        evallist[evalValue] = list();
                evallist[evalValue].append(i);
                k = int(i[1]) +1;
                # Keep updating the traverse log.
                traverselogwrite(i[0]+str(k), level, evalValue);
                if(level % 2 == 0):
                    if(evalValue < node.currValue):
                        node.childNode = i;
                        node.currValue = evalValue;
                elif(level % 2 == 1):
                    if(evalValue > node.currValue ):
                        node.childNode = i;
                        node.currValue = evalValue;


                if(node.currsymbol != "root"):
                    k = int(node.currsymbol[1]) + 1;
                    traverselogwrite(node.currsymbol[0]+str(k), node.level, node.currValue) ;
                else:
                    traverselogwrite(node.currsymbol, node.level, node.currValue) ;

            # repeat the process if it is a sneek position.
            elif (i in sneekPositions):
                    value = myPlayerVal + values[i[0]][int(i[1])];
                    if(level % 2 == 1):
                         evalValue = value - opponentPlayerVal;
                    elif (level % 2 == 0):
                        evalValue = opponentPlayerVal - value;

                    if evalValue not in evallist:
                        evallist[evalValue] = list();
                    evallist[evalValue].append(i);
                    k = int(i[1]) +1;
                    traverselogwrite(i[0]+str(k), level, evalValue);
                    if(level % 2 == 0):
                        if(evalValue < node.currValue):
                            node.childNode = i;
                            node.currValue = evalValue;
                    elif( level%2 == 1):
                        if(evalValue > node.currValue ):
                            node.childNode = i;
                            node.currValue = evalValue;

                    if(node.currsymbol != "root"):
                        k = int(node.currsymbol[1]) + 1;
                        traverselogwrite(node.currsymbol[0]+str(k), node.level, node.currValue) ;
                    else:
                        traverselogwrite(node.currsymbol, node.level, node.currValue) ;

    return  node;

def minfunction(level, cutoff, playersym, otherplayer, parentnode, positions):

    count = isempty(playersym,otherplayer,positions);
    if(count == 1):
        node = copy.deepcopy(parentnode);
        node.currValue = 999;
        node = evalCalculation1(level,cutoff, otherplayer, playersym, node, positions);
        return node;

    if(level == cutoff):
        node = copy.deepcopy(parentnode);
        node.currValue = 999;
        childnode = evalCalculation1(level, cutoff, otherplayer, playersym, node , positions);
        return childnode;

    elif(level < cutoff):

        parentnode.currValue = 999;
        myPlayerPositions = playerpos(positions, otherplayer);
        emptyPositions = playerpos(positions , '*');
        raidPositions = freePos(myPlayerPositions,positions);
        sneekPositions = getSneekPositions(raidPositions);
        for i in positionalList(emptyPositions):
            tmpPositions = copy.deepcopy(positions);
            if i in raidPositions:
                neighbors = adjacentPos(i);
                finalneighbors = validOpp(neighbors, i, otherplayer , positions);
                tmpPositions[i[0]][int(i[1])] = otherplayer.strip('\r');
                for j in finalneighbors:
                    tmpPositions[j[0]][int(j[1])] = otherplayer.strip('\r');
            elif i in sneekPositions:
                    tmpPositions[i[0]][int(i[1])] = otherplayer.strip('\r');


            node = Node();
            node.currsymbol = i;
            node.level =  level;
            k = int(i[1]) + 1;
            traverselogwrite(i[0]+str(k), level, "-Infinity");
            childnode = maxfunction(level+1, cutoff, playersym, otherplayer, node, tmpPositions);
            if(parentnode.currValue > childnode.currValue):
                parentnode.currValue = childnode.currValue;
                parentnode.childNode = childnode.currsymbol;

            k = int(parentnode.currsymbol[1]) + 1;
            traverselogwrite(parentnode.currsymbol[0]+str(k), parentnode.level, parentnode.currValue);


    return parentnode;

#function for max calling.
def maxfunction(level, cutoff, playersym, otherplayer, parentnode, positions):

    count = isempty(playersym,otherplayer,positions);

    if(count == 1):
        node = copy.deepcopy(parentnode);
        node.currValue = -999;
        node = evalCalculation1(level,cutoff, playersym, otherplayer, node, positions);
        return node;


    if(level == cutoff and level == 1):
        traverselogwrite(parentnode.currsymbol, parentnode.level, "-Infinity" );
        node = copy.deepcopy(parentnode);
        node.currValue = -999;
        node = evalCalculation1(level, cutoff, playersym, otherplayer, node, positions);
        return node;

    elif(level < cutoff):

        parentnode.currValue = -999;
        if(parentnode.currsymbol == "root"):
            traverselogwrite(parentnode.currsymbol, parentnode.level, "-Infinity" );
        myPlayerPositions = playerpos(positions, playersym);
        emptyPositions = playerpos(positions , '*');
        raidPositions = freePos(myPlayerPositions,positions);
        sneekPositions = getSneekPositions(raidPositions);

        for i in positionalList(emptyPositions):
            tmpPositions = copy.deepcopy(positions);
            if i in raidPositions:
                neighbors = adjacentPos(i);
                finalneighbors = validOpp(neighbors, i, playersym, positions);
                tmpPositions[i[0]][int(i[1])] = playersym.strip('\r');
                for j in finalneighbors:
                    tmpPositions[j[0]][int(j[1])] = playersym.strip('\r');
            elif i in sneekPositions:
                    tmpPositions[i[0]][int(i[1])] = playersym.strip('\r');


            node = Node();
            node.currsymbol = i;
            node.level =  level;
            k = int(i[1]) + 1;
            traverselogwrite(i[0]+str(k), level, "Infinity");
            childnode = minfunction(level+1, cutoff, playersym, otherplayer, node, tmpPositions);
            if(parentnode.currValue < childnode.currValue):
                parentnode.currValue = childnode.currValue;
                parentnode.childNode = childnode.currsymbol;

            if (parentnode.currsymbol != "root"):
                k = int(parentnode.currsymbol[1]) + 1;
                traverselogwrite(parentnode.currsymbol[0] + str(k), parentnode.level, parentnode.currValue);
            else:
                traverselogwrite(parentnode.currsymbol, parentnode.level, parentnode.currValue);


    elif(level == cutoff):
        node = copy.deepcopy(parentnode);
        node.currValue = -999;
        childnode = evalCalculation1(level, cutoff, playersym, otherplayer, node, positions);
        return childnode;

    return parentnode;

def evalCalculationAlpha(level, cutoff, playersym, otherplayer, node, locations):
    myPlayerPositions = playerpos(locations, playersym);
    myPlayerVal = posValues(myPlayerPositions);


    opponentPlayerPositions = playerpos(locations, otherplayer);
    opponentPlayerVal =  posValues(opponentPlayerPositions);


    emptyPositions = playerpos(locations , '*');
    raidPositions = freePos(myPlayerPositions,locations);
    sneekPositions = getSneekPositions(raidPositions);

    # Get the list of positions in positional ordering.
    sortedList = positionalList(emptyPositions);
    evallist = {};

    if(node.maxValue == -999 or node.maxValue == "-Infinity"):
        node.maxValue = str("-Infinity");
    if(node.minValue == 999 or  node.minValue == "Infinity"):
        node.minValue = str("Infinity");


    # if it has reached the sorted list then the leave nodes have to be checked for positional ordering.
    for i in sortedList:
    # Check if i belongs to raid position or sneek position.

            if (i in raidPositions):
                # Compute the eval value if it is in the raid position
                value = myPlayerVal + values[i[0]][int(i[1])];
                opponentNeighbors = adjacentPos(i);
                validOpponent = validOpp(opponentNeighbors, i,playersym,locations);

                tmpOpponent = opponentPlayerVal;
                for j in validOpponent:
                        value += values[j[0]][int(j[1])];
                        tmpOpponent -= values[j[0]][int(j[1])];


                if(level % 2 == 1):
                        evalValue = value - tmpOpponent;
                elif (level % 2 == 0):
                        evalValue = tmpOpponent - value;



                # Create a dictionary to hold eval values of all the moves
                if evalValue not in evallist:
                        evallist[evalValue] = list();
                evallist[evalValue].append(i);
                k = int(i[1]) +1;
                log(i[0]+str(k), level, evalValue, node.maxValue, node.minValue);

                currentmin = node.minValue;
                currentmax = node.maxValue;
                if(level % 2 == 0):
                    if(evalValue < node.currValue):
                        node.childNode = i;
                        node.currValue = evalValue;
                        if(node.minValue == "Infinity"):
                            node.minValue = 999;
                        if(node.minValue > evalValue):
                            node.minValue  = evalValue;

                elif(level % 2 == 1):
                    if(evalValue > node.currValue ):
                        node.childNode = i;
                        node.currValue = evalValue;
                        if(node.maxValue == "-Infinity"):
                            node.maxValue = -999;
                        if(node.maxValue < evalValue):
                            node.maxValue = evalValue;

                if( evalValue <= node.maxValue and node.maxValue != "-Infinity" and level%2 == 0):
                            node.minValue = currentmin;

                if( evalValue >= node.minValue and node.minValue != "Infinity" and level%2 == 1):
                            node.maxValue = currentmax;

                if(node.currsymbol != "root"):
                    k = int(node.currsymbol[1]) + 1;
                    log(node.currsymbol[0]+str(k), node.level, node.currValue, node.maxValue, node.minValue ) ;
                else:
                    log(node.currsymbol, node.level, node.currValue, node.maxValue, node.minValue);


            elif (i in sneekPositions):
                    value = myPlayerVal + values[i[0]][int(i[1])];
                    if(level % 2 == 1):
                         evalValue = value - opponentPlayerVal;
                    elif (level % 2 == 0):
                        evalValue = opponentPlayerVal - value;



                    if evalValue not in evallist:
                        evallist[evalValue] = list();
                    evallist[evalValue].append(i);
                    k = int(i[1]) +1;
                    log(i[0]+str(k), level, evalValue, node.maxValue, node.minValue);

                    currentmin = node.minValue;
                    currentmax = node.maxValue;
                    if(level % 2 == 0):
                        if(evalValue < node.currValue):
                            node.childNode = i;
                            node.currValue = evalValue;
                            if(node.minValue == "Infinity"):
                                node.minValue = 999;
                            if(node.minValue > evalValue):
                                node.minValue  = evalValue;


                    elif( level%2 == 1):
                        if(evalValue > node.currValue ):
                            node.childNode = i;
                            node.currValue = evalValue;
                            if(node.maxValue == "-Infinity"):
                                node.maxValue = -999;
                            if(node.maxValue < evalValue):
                                 node.maxValue = evalValue;


                    if( evalValue <= node.maxValue and node.maxValue != "-Infinity" and level%2 == 0):
                            node.minValue = currentmin;

                    if( evalValue >= node.minValue and node.minValue != "Infinity" and level%2 == 1):
                            node.maxValue = currentmax;



                    if(node.currsymbol != "root"):
                        k = int(node.currsymbol[1]) + 1;
                        log(node.currsymbol[0]+str(k), node.level, node.currValue, node.maxValue, node.minValue);
                    else:
                        log(node.currsymbol, node.level, node.currValue, node.maxValue, node.minValue );

            if(node.maxValue != "-Infinity" and evalValue <= node.maxValue and level%2 == 0):
                        break;

            if(node.minValue != "Infinity" and evalValue >= node.minValue and level%2 == 1):
                        break;


    return  node;

def minfunctionAlpha(level, cutoff, playersym, otherplayer, parentnode, positions):

    count = isempty(playersym,otherplayer,positions);
    if(count == 1):
        node = copy.deepcopy(parentnode);
        node.currValue = 999;
        node = evalCalculationAlpha(level,cutoff, otherplayer, playersym, node, positions);
        return node;

    if(level == cutoff):
        node = copy.deepcopy(parentnode);
        node.currValue = 999;
        childnode = evalCalculationAlpha(level, cutoff, otherplayer, playersym, node , positions);
        return childnode;

    elif(level < cutoff):

        parentnode.currValue = 999;
        myPlayerPositions = playerpos(positions, otherplayer);
        emptyPositions = playerpos(positions , '*');
        raidPositions = freePos(myPlayerPositions,positions);
        sneekPositions = getSneekPositions(raidPositions);

        for i in positionalList(emptyPositions):
            if(parentnode.maxValue == -999):
                parentnode.maxValue = "-Infinity";
            if(parentnode.minValue == 999):
                parentnode.maxValue = "Infinity";

            tmpPositions = copy.deepcopy(positions);
            if i in raidPositions:
                neighbors = adjacentPos(i);
                finalneighbors = validOpp(neighbors, i, otherplayer , positions);
                tmpPositions[i[0]][int(i[1])] = otherplayer.strip('\r');
                for j in finalneighbors:
                    tmpPositions[j[0]][int(j[1])] = otherplayer.strip('\r');
            elif i in sneekPositions:
                    tmpPositions[i[0]][int(i[1])] = otherplayer.strip('\r');


            node = Node();
            node.currsymbol = i;
            node.level =  level;
            node.minValue = parentnode.minValue;
            node.maxValue = parentnode.maxValue;
            k = int(i[1]) + 1;
            log(i[0]+str(k), level, "-Infinity",parentnode.maxValue, parentnode.minValue);

            currentminValue = parentnode.minValue;
            childnode = maxfunctionAlphaBeta(level+1, cutoff, playersym,otherplayer,  node, tmpPositions);
            if(parentnode.currValue > childnode.currValue):
                parentnode.currValue = childnode.currValue;
                parentnode.childNode = childnode.currsymbol;
                if(parentnode.minValue == "Infinity"):
                    parentnode.minValue = 999;
                if(childnode.currValue < parentnode.minValue):
                    parentnode.minValue = childnode.currValue;

            if(parentnode.maxValue == "-Infinity"):
                parentnode.maxValue = -999;

            if(childnode.currValue <= parentnode.maxValue):
                parentnode.minValue = currentminValue;

            if(parentnode.maxValue == -999):
                parentnode.maxValue = "-Infinity";
            k = int(parentnode.currsymbol[1]) + 1;
            log(parentnode.currsymbol[0]+str(k), parentnode.level, parentnode.currValue,parentnode.maxValue,parentnode.minValue);
            if(parentnode.maxValue == "-Infinity"):
                parentnode.maxValue = -999;
            if(childnode.currValue <= parentnode.maxValue):
                break;

    return parentnode;

def maxfunctionAlphaBeta(level, cutoff, playersym, otherplayer, parentnode, positions):

    count = isempty(playersym, otherplayer, positions);
    if( count == 1):
        node = copy.deepcopy(parentnode);
        node.currValue = -999;
        node = evalCalculationAlpha(level, cutoff, playersym, otherplayer, node, positions);
        return node;

    if (level == cutoff and level == 1):
        log(parentnode.currsymbol, parentnode.level, "-Infinity", "-Infinity", "Infinity" );
        node = copy.deepcopy(parentnode);
        node.currValue = -999;
        node = evalCalculationAlpha(level, cutoff, playersym, otherplayer, node, positions);
        return node;

    elif (level < cutoff):
        parentnode.currValue = -999;

        if(parentnode.currsymbol == "root"):
            parentnode.maxValue = "-Infinity";
            parentnode.minValue = "Infinity";
            log(parentnode.currsymbol, parentnode.level, "-Infinity","-Infinity", "Infinity" );

        myPlayerPositions = playerpos(positions, playersym);
        emptyPositions = playerpos(positions , '*');
        raidPositions = freePos(myPlayerPositions,positions);
        sneekPositions = getSneekPositions(raidPositions);

        for i in positionalList(emptyPositions):

            if(parentnode.maxValue == -999):
                parentnode.maxValue = "-Infinity";
            if(parentnode.minValue == 999):
                parentnode.maxValue = "Infinity";

            tmpPositions = copy.deepcopy(positions);
            if i in raidPositions:
                neighbors = adjacentPos(i);
                finalneighbors = validOpp(neighbors, i, playersym, positions);
                tmpPositions[i[0]][int(i[1])] = playersym.strip('\r');
                for j in finalneighbors:
                    tmpPositions[j[0]][int(j[1])] = playersym.strip('\r');
            elif i in sneekPositions:
                    tmpPositions[i[0]][int(i[1])] = playersym.strip('\r');


            node = Node();
            node.currsymbol = i;
            node.level =  level;
            node.maxValue = parentnode.maxValue;
            node.minValue = parentnode.minValue;

            k = int(i[1]) + 1;
            log(i[0]+str(k), level, "Infinity",parentnode.maxValue, parentnode.minValue);

            currentmaxValue = parentnode.maxValue;
            childnode = minfunctionAlpha(level+1, cutoff, playersym, otherplayer, node, tmpPositions);
            if(parentnode.currValue < childnode.currValue):
                parentnode.currValue = childnode.currValue;
                parentnode.childNode = childnode.currsymbol;
                if(parentnode.maxValue == "-Infinity"):
                    parentnode.maxValue = -999;
                if(childnode.currValue > parentnode.maxValue):
                      parentnode.maxValue = childnode.currValue;


            if(childnode.currValue >= parentnode.minValue):
                    parentnode.maxValue = currentmaxValue;

            if (parentnode.currsymbol != "root"):
                k = int(parentnode.currsymbol[1]) + 1;
                log(parentnode.currsymbol[0] + str(k), parentnode.level, parentnode.currValue,parentnode.maxValue,parentnode.minValue);
            else:
                log(parentnode.currsymbol, parentnode.level, parentnode.currValue,parentnode.maxValue,parentnode.minValue);

            if( childnode.currValue >= parentnode.minValue ):
                break;


    elif(level == cutoff):
        node = copy.deepcopy(parentnode);
        node.currValue = -999;
        childnode = evalCalculationAlpha(level, cutoff, playersym, otherplayer, node, positions);
        return childnode;

    return parentnode;

def main():
    # open the input file to read the data.
    #fhandle = open(sys.argv[2], "r");
    fhandle = open("input.txt","r");

    # structure to hold values from the text file.

    charArray = ['A','B','C','D','E'];
    global values;
    values = {};
    global positions;
    positions = {};
    global playerSym;
    global otherPlayer;
    global algoChoice;

    for i, line in enumerate(fhandle):
        # Get the value of the algorithm to read
        if (i == 0):
          line = line.strip('\n');
          line = line.strip('\r');
          algoChoice = line;
          algoChoice = int(algoChoice);


        if (algoChoice == 4):

            if(i == 1):
                line = line.strip('\n');
                line = line.strip('\r');
                firstplayer = line;


            if(i == 2):
                line = line.strip('\n');
                line = line.strip('\r');
                firstplayerAlgo = line;


            if(i == 3):
                line = line.strip('\n');
                line = line.strip('\r');
                firstplayercutoff = line;
                firstplayercutoff = int(firstplayercutoff);


            if(i == 4):
                line = line.strip('\n');
                line = line.strip('\r');
                secondPlayer = line;


            if(i == 5):
                line = line.strip('\n');
                line = line.strip('\r');
                secondplayerAlgo = line;



            if(i == 6):
                line = line.strip('\n');
                line = line.strip('\r');
                secondPlayercutoff = line;
                secondPlayercutoff = int(secondPlayercutoff);



            if(i>=7 and i<=11):
                 line = line.strip('\n');
                 line = line.strip('\r');
                 Strvalue = line.split(' ');
                 value = list();
                 for i in Strvalue:
                    value.append(int(i));


                 for j in range(5):
                    if charArray[j] not in values:
                        values[charArray[j]] = list();
                    values[charArray[j]].append(value[j]);

            if(i>=12 and i<=16):
                 line = line.strip('\n');
                 line = line.strip('\r');

                 for j in range(5):
                        if charArray[j] not in positions:
                            positions[charArray[j]] = list();
                        positions[charArray[j]].append(line[j]);
        else:
            # Get the player symbol from the file.
            if(i == 1):

                line = line.strip('\n');
                line = line.strip('\r');
                playerSym = line;




                global otherPlayer;
                if(playerSym == 'X'):
                    otherPlayer = 'O';
                else:
                    otherPlayer = 'X';


            # Cut off depth to consider
            if (i == 2):
                 line = line.strip('\n');
                 line = line.strip('\n');
                 line = line.strip('\r');
                 cutDepth = line;

            # Dictionary to hold the values according to the positions.
            value = [];
            if( i >= 3 and i<=7 ):
                 line = line.strip('\n');
                 line = line.strip('\r');
                 Strvalue = line.split(' ');
                 value = list();
                 for i in Strvalue:
                    value.append(int(i));


                 for j in range(5):
                    if charArray[j] not in values:
                        values[charArray[j]] = list();
                    values[charArray[j]].append(value[j]);

            # Dictionary to hold the positions of the players.
            position = [];

            if( i >= 8 and i<=12 ):
                 line = line.strip('\n');
                 line = line.strip('\r');
                 for j in range(5):
                        if charArray[j] not in positions:
                            positions[charArray[j]] = list();
                        positions[charArray[j]].append(line[j]);


    if(algoChoice == 1):
        greedybestfirst(values, positions, playerSym, otherPlayer);
    elif (algoChoice == 2):
        minmax(values, positions, playerSym, cutDepth, otherPlayer);
    elif(algoChoice == 3):
        alphabeta(values, positions, playerSym, cutDepth, otherPlayer);

    elif(algoChoice == 4):
        global trace;
        trace = open ('trace_state.txt', 'w');
        tmppositions = copy.deepcopy(positions);
        count = isempty(firstplayer, secondPlayer, tmppositions);
        location = list();
        while( count > 0 ):
            if(firstplayerAlgo == "1"):
                location = greedybestfirst(values,tmppositions,firstplayer,secondPlayer);
            elif(firstplayerAlgo == "2"):
                location = minmax(values,tmppositions,firstplayer,firstplayercutoff, secondPlayer);
            elif(firstplayerAlgo == "3"):
                location = alphabeta(values,tmppositions,firstplayer,firstplayercutoff,secondPlayer);

            for i in location:
                tmppositions[i[0]][int(i[1])] = firstplayer.strip('\r');

            if(secondplayerAlgo == "1"):
                location = greedybestfirst(values,tmppositions,secondPlayer,firstplayer);
            elif(secondplayerAlgo == "2"):
                location = minmax(values,tmppositions,secondPlayer,secondPlayercutoff,firstplayer);
            elif(secondplayerAlgo == "3"):
                location = alphabeta(values,tmppositions,secondPlayer,secondPlayercutoff,firstplayer);

            for i in location:
                tmppositions[i[0]][int(i[1])] = secondPlayer.strip('\r');

            count = isempty(firstplayer, secondPlayer, tmppositions);
        trace.close();

def greedybestfirst(values, positions, playerSym,otherPlayer):


    statefile = open("next_state.txt",'w');

    # Conditions when there are no pieces on the board.
    myPlayerPos = playerpos(positions,playerSym);
    if not myPlayerPos:
        pos = list();
        emptypos = playerpos(positions, '*');
        if not emptypos:
            noWrite();
            exit();
        else:
            pos.append(maxEmptyValue(positions));
            filewrite(pos,statefile);
            exit();

    # If there are no more moves left
    emptypos = playerpos(positions, '*');
    if not emptypos:
        noWrite();
        exit();



    myPlayerPos = playerpos(positions,playerSym);
    myPlayerVal = posValues(myPlayerPos);
    otherPlayerPos = playerpos(positions,otherPlayer);
    otherPlayerVal = posValues(otherPlayerPos);

    #Call to get valid position where we can keeep our player piece.
    validPos = freePos(myPlayerPos,positions);


    # To get the state values for the valid raid moves
    states = {};
    tmpval=0;
    for i in validPos:
        # value of current player
        tmpval = values[i[0]][int(i[1])] + myPlayerVal;

        # Get the valid opponent squares.
        opponentNeighbors = adjacentPos(i);
        validOpponent = validOpp(opponentNeighbors, i, playerSym, positions);

        # Get the squares to be conquered. But this is not used
        conqSquares = list();
        tmpOppval = otherPlayerVal;
        for j in validOpponent:
            tmpval += values[j[0]][int(j[1])];
            tmpOppval -= values[j[0]][int(j[1])];
            conqSquares.append(j);


        # Calculate the eval function. And create a dictionary out of the utility with different squares as values.
        evalVal = tmpval - tmpOppval;
        if evalVal not in states:
            states[evalVal] = list();
        states[evalVal].append(i);

    finalstates = list();
    # get the max key from the states
    maxKey = max(states.keys());
    # get the min index according to positional ordering from the list
    maxVal = states[maxKey];
    finalpos = minIndex(maxVal);

    # Append that square to the final list
    finalstates.append(finalpos);

    # find the valid opponent neighbor for that state. This we call to get the opponent nodes for the raid that we will be doing.
    finalneighbor = adjacentPos(finalpos);
    finalvalid = validOpp(finalneighbor,finalpos, playerSym, positions);
    for i in finalvalid:
        finalstates.append(i);



    # Get the value of maximum unoccupied square by functional call maxEmpty
    maxindexValue =  maxEmptyValue(positions);
    value = values[maxindexValue[0]][int(maxindexValue[1])];

    # Compute the difference that is there in the existing board.
    diff = myPlayerVal - otherPlayerVal;
    # Compute the sneek value by adding the square to it.
    sneekVal = value + diff;




    pickedPos = list();
    if( sneekVal > maxKey):
        pickedPos.append(maxindexValue);
    elif(sneekVal == maxKey):
        sortlist= list();
        sortlist.append(maxindexValue);
        for i in finalstates:
            sortlist.append(i);
        pickedPos.append(minIndex(sortlist));
    else:
        pickedPos = finalstates;


    if(algoChoice == 4):
        tracelog(pickedPos,playerSym, positions);
        return pickedPos;
    else:
        filewrite(pickedPos,statefile);
        statefile.close();
        exit();

def minmax(values, positions, playerSym, cutDepth, otherPlayer):


    global traverse;
    statefile = open("next_state.txt",'w');
    traverse =  open("traverse_log.txt", 'w');
    myPlayerPositions = playerpos(positions,playerSym);
    myPlayerVal = posValues(myPlayerPositions);


    opponentPlayerPositions = playerpos(positions, otherPlayer );
    opponentPlayerVal =  posValues(opponentPlayerPositions);


    emptyPositions = playerpos(positions , '*');
    raidPositions = freePos(myPlayerPositions,positions);
    sneekPositions = getSneekPositions(raidPositions);

    level = 1;
    parentNode = Node();
    parentNode.currValue = -999;
    parentNode.currsymbol = "root";
    parentNode.level = 0;
    cutDepth = int(cutDepth);
    traverselogwrite("Node","Depth","Value");
    count = isempty(playerSym, otherPlayer, positions);
    if(count == 0):
        noWrite();
        exit();

    location = maxfunction(level, cutDepth, playerSym, otherPlayer, parentNode, positions);
    locations = list();
    if location.childNode in raidPositions:
        locations = opponentNodes(location.childNode, playerSym, positions);
    else:
        locations.append(location.childNode);

    if(algoChoice == 4):
        tracelog(locations,playerSym, positions);
        return locations;
    else:
        filewrite(locations,statefile);
        statefile.close();
        traverse.close();
        exit();

def alphabeta(values, positions, playerSym, cutDepth, otherPlayer):


    global logfile
    statefile = open("next_state.txt",'w');
    logfile =  open("traverse_log.txt", 'w');
    myPlayerPositions = playerpos(positions,playerSym);
    myPlayerVal = posValues(myPlayerPositions);


    opponentPlayerPositions = playerpos(positions, otherPlayer );
    opponentPlayerVal =  posValues(opponentPlayerPositions);


    emptyPositions = playerpos(positions , '*');
    raidPositions = freePos(myPlayerPositions,positions);
    sneekPositions = getSneekPositions(raidPositions);

    level = 1;
    parentNode = Node();
    parentNode.currValue = -999;
    parentNode.currsymbol = "root";
    parentNode.level = 0;
    cutDepth = int(cutDepth);
    log("Node","Depth","Value","Alpha","Beta");
    count = isempty(playerSym, otherPlayer, positions);
    if(count == 0):
        noWrite();
        exit()
    location = maxfunctionAlphaBeta(level, cutDepth, playerSym, otherPlayer, parentNode, positions);
    locations = list();
    if location.childNode in raidPositions:
        locations = opponentNodes(location.childNode,playerSym,positions);
    else:
        locations.append(location.childNode);

    if(algoChoice == 4):
        tracelog(locations,playerSym, positions);
        return locations;
    else:
        filewrite(locations,statefile);
        statefile.close();
        logfile.close();
        exit();


if __name__ == "__main__":
    main()







