import re;
queryDict =  {};
network = {};

def displayDict(dict):
    for key in dict.keys():
        print dict[key];

# function to get arguments within a probability or a eu
def getarguments(line):
    pattern = re.compile(".*\((.*)\)");
    arguments = pattern.match(line).group(1);
    return arguments;

# function to get the argument array
def splitArgArray(arguments):
    args = arguments.split(", ");
    return args;

# function to get truth value assigned to a random variable.
def truthValueVar(arg):
    values = arg.split(" = ");
    return values;


# check if parent value is set in the query
def checkIfParent(arguments,variable):
   setVariables = {};
   for arg in arguments:
       result = truthValueVar(arg);
       for var in variable:
        if(var == result[0]):
            setVariables[var] = result[1];
   return setVariables;


def calculateParentwithParent(parent,arguments,fixedParameters):
    grandparent = network[parent]['parent'];
    grandparent = grandparent.split(" ");
    setVar = checkIfParent(arguments, grandparent);
    fixedParameters.update(setVar);
    # to keep checking parent of parentvariables
    positiveProb = probJointParent(parent,"+",grandparent, fixedParameters, arguments );
    negativeProb = probJointParent(parent,"-", grandparent, fixedParameters,arguments);
    return positiveProb, negativeProb;

def calculateParentProb(plusProb,negProb,parent,fixedParameters,arguments):
    parentProb = network[parent]['+'];
    negParentProb = 1 - parentProb;
    if parent in fixedParameters:
            if(fixedParameters[parent] == "+"):
                finalresult = plusProb;
            else:
                finalresult = negProb;
    else:
        # find sum of the terms for each value of the parent
        positiveterm = plusProb * parentProb;
        negativeterm = negProb * negParentProb;
        finalresult = positiveterm + negativeterm;
    return finalresult;

def calculateParentProb2(variable,value,parents,parentExists,arguments,fixedParameters):

    firstparent = 0;
    secondparent = 0;
    if(bool(parentExists)):
            for i, par in enumerate(parents):
                if par in parentExists:
                    if(i == 0):
                        firstparent = 1;
                    if(i == 1):
                        secondparent = 1;

            if(firstparent == 1 and secondparent == 0):

                fixedParameters = checkIfParent(arguments,parentExists[parents[0]]);
                parent1Pos = probJointParent(parents[0],"+",parentExists[parents[0]],fixedParameters,arguments);
                parent2pos = network[parents[1]]['+'];
                parent1Neg = 1 - parent1Pos;
                parent2Neg = 1 - parent2pos;

            elif( firstparent == 0 and secondparent == 1):
                fixedParameters = checkIfParent(arguments,parentExists[parents[1]]);
                parent1Pos = network[parents[0]]['+'];
                parent2pos = probJointParent(parents[1],"+",parentExists[parents[1]],fixedParameters,arguments);
                parent1Neg = 1 - parent1Pos;
                parent2Neg = 1 - parent2pos;
            else:
                fixedParameters1 = checkIfParent(arguments,parentExists[parents[0]]);
                fixedParameters2 = checkIfParent(arguments,parentExists[parents[1]]);

                fixedParameters.update(fixedParameters1);
                fixedParameters.update(fixedParameters2);
                parent1Pos = probJointParent(parents[0],"+",parentExists[parents[0]],fixedParameters,arguments);
                parent2pos = probJointParent(parents[1],"+",parentExists[parents[1]],fixedParameters,arguments);
                parent1Neg = 1 - parent1Pos;
                parent2Neg = 1 - parent2pos;
    else:

        parent1Pos = network[parents[0]]['+'];
        parent2pos = network[parents[1]]['+'];
        parent1Neg = 1 - parent1Pos;
        parent2Neg =  1 - parent2pos;

    if(value == "+"):
        firstterm = network[variable]["++"] * parent1Pos * parent2pos;
        secondterm = network[variable]["+-"] * parent1Pos * parent2Neg;
        thirdterm = network[variable]["-+"] * parent1Neg * (parent2pos);
        fourtterm = network[variable]["--"] * parent1Neg * parent2Neg;
        finalresult = firstterm + secondterm + thirdterm + fourtterm;
        return finalresult;
    else:
        firstterm = (1-network[variable]["++"]) * parent1Pos * parent2pos;
        secondterm = (1-network[variable]["+-"]) * parent1Pos * parent2Neg;
        thirdterm = (1-network[variable]["-+"]) * parent1Neg * (parent2pos);
        fourtterm = (1-network[variable]["--"]) * parent1Neg * parent2Neg;
        finalresult = firstterm + secondterm + thirdterm + fourtterm;
        return finalresult;

def length2Prob(variable,value,parents,fixedParameters,arguments):
    firstString = 0;
    secondString = 0;

    parentExists = {};
    for i, parent in enumerate(parents):
       if 'parent' in network[parent]:
            parentExists[parent] = network[parent]['parent'].split(" ");
            for par in parentExists[parent]:
                par = par.split(" ");
                fixedParameters2 = checkIfParent(arguments,par);
                fixedParameters.update(fixedParameters2);


    for i, par in enumerate(parents):
        if par in fixedParameters:
            if( i == 0):
                firstString = fixedParameters[par];
            else:
                secondString = fixedParameters[par];

    if(firstString != 0 and secondString != 0):
             combined = firstString + secondString;
             varProb = network[variable][combined];
             return varProb;

    elif(firstString != 0):
        positive = firstString+"+";
        negative = firstString+"-";
        postiveProb = network[variable][positive];
        negativeProb = network[variable][negative];

        if parents[1] in parentExists:
            posParent = probJointParent(parents[1],"+",parentExists[parents[1]],fixedParameters,arguments);
            negParent = 1 - posParent;
        else:
            posParent = network[parents[1]]['+'];
            negParent = 1 - posParent;

        finalvalue = postiveProb * posParent + negativeProb * negParent;
        return finalvalue;

    elif(secondString != 0):
        positive = "+" + secondString;
        negative = "-" + secondString;
        postiveProb = network[variable][positive];
        negativeProb = network[variable][negative];

        if parents[0] in parentExists:
               posParent = probJointParent(parents[0],"+",parentExists[parents[0]],fixedParameters,arguments);
               negParent = 1 - posParent;
        else:
            posParent = network[parents[0]]['+'];
            negParent = 1 - posParent;
        finalvalue = postiveProb * posParent + negativeProb * negParent;
        return finalvalue;
    else:

        finalresult = calculateParentProb2(variable,value,parents,parentExists,arguments,fixedParameters);
        return finalresult;

# function to calculate probability over parent all values.
def probJointParent(variable,truthValue, parents,fixedParameters,arguments):
        # check first if the value of given variable is set to true or not set.
        if(truthValue == "+"):
            # check how many parents are there for the given child.


            length = len(parents);
            # if there is only one parent then get the positive and negative prob value for variable given the parent.
            if(length == 1):
                plusProb = network[variable]['+'];
                negProb = network[variable]['-'];

                # Next get the parent prob value
                parent = network[variable]['parent'];
                if "parent" in network[parent]:
                   if parent in fixedParameters:
                     if(fixedParameters[parent] == '+'):
                         return plusProb;
                     else:
                         return negProb;
                   else:
                       finalresult = calculateParentwithParent(parent,arguments);
                       firstVal = plusProb * finalresult[0];
                       secondVal = negProb * finalresult[1];
                       finalresult = firstVal + secondVal;
                       return finalresult;
                else:
                    finalresult = calculateParentProb(plusProb,negProb,parent,fixedParameters,arguments);
                    return finalresult;

            # if there are two parents.
            elif(length == 2):
                    finalresult = length2Prob(variable,"+",parents,fixedParameters,arguments);
                    return finalresult;

        else:

            length = len(parents);
            # if there is only one parent then get the positive and negative prob value for variable given the parent.
            if(length == 1):
                plusProb = 1 - network[variable]['+'];
                negProb = 1 - network[variable]['-'];
                parent = network[variable]['parent'];
                if "parent" in network[parent]:
                   if parent in fixedParameters:
                     if(fixedParameters[parent] == '+'):
                         return plusProb;
                     else:
                         return negProb;
                   else:
                        finalresult = calculateParentwithParent(parent,arguments,fixedParameters);
                        firstVal = plusProb * finalresult[0];
                        secondVal = negProb * finalresult[1];
                        finalresult = firstVal + secondVal;
                        return finalresult;
                else:
                    finalresult = calculateParentProb(plusProb,negProb,parent,fixedParameters,arguments);
                    return finalresult;

            elif(length == 2):
                    finalresult = length2Prob(variable,"-",parents,fixedParameters,arguments);
                    return finalresult;

def jointProbabilty(arguments):
    arguments = splitArgArray(arguments);
    # Enumerate through the arguments to finc the conditional probability of each of them and then multiply them together.
    finalproduct = 1;
    for k, arg in enumerate(arguments):
        # Get the variables and their set value.
        result = truthValueVar(arg);
        variable = result[0];
        truthVal = result[1];

        # check if the variable is standalone or single. If it is has a parent then we need to find it across all the values of its parent multiplied by the parent.
        if 'parent' in network[variable]:
            #get the parent values from the network.
            parents = network[variable]['parent'];
            parents = parents.split(" ");

            fixedValues = {};
            fixedValues = checkIfParent(arguments,parents);

            # if it is not present in the argument then we have to consider the coditional value of both the parents.
            result = probJointParent(variable,truthVal,parents,fixedValues,arguments);
            finalproduct = finalproduct * result;

        else:
            # get teh probability value of the standalone variable.
            probValue = network[variable]['+'];
            # if variable is set then just multiply them
            if(truthVal == "+"):
                finalproduct = finalproduct * probValue;
            else:
                finalproduct  = finalproduct * (1 - probValue);

    # round to two decimal points.
    return finalproduct;

def solveQuery(queries):
    # loop through queries one by one.
    for i, query in enumerate(queries):
        # Check what type of query it is
        print queries[query];
        if(queries[query]['type'] == 'probability'):

            #Now check what type of probability we want to calculate.
            if(queries[query]['argType'] == "joint"):
                   # Get the joint probability arguments and send it to a function to calculate the joint probability.
                   arguments = queries[query]['arg'];
                   result = jointProbabilty(arguments);
                   print '{0:.2f}'.format(round(result, 2));
            elif(queries[query]['argType'] == "margin"):
                    arguments = queries[query]['arg'];
                    result = jointProbabilty(arguments);
                    print '{0:.2f}'.format(round(result, 2));
            elif(queries[query]['argType'] == "conditional"):
                    arguments = queries[query]['arg'];
                    arguments = arguments.split(" | ");
                    query = arguments[0];
                    evidence = arguments[1];
                    query1 = splitArgArray(query);
                    evidence1 = splitArgArray(evidence);

                    print query;
                    print evidence;
                    listVar = query1 + evidence1;

                    arguments = listVar[0];
                    for i in range(1,len(listVar)):
                            arguments = arguments + ", " + listVar[i];



                    result1 = jointProbabilty(arguments);
                    result2 = jointProbabilty(evidence);

                    finalresult = result1 / result2;
                    print '{0:.2f}'.format(round(finalresult, 2));
                    quit();

def main():

    # open file to read data
    inputFile = open("sample.txt", "r");
    querySeprator = 0;
    node = 1;
    for i, line in enumerate(inputFile):
        line = line.strip('\n');
        line = line.strip('\r');

        # Read the queries line
        if(line != "******" and querySeprator == 0):
             if i not in queryDict:
                 queryDict[i] = {};
             queryDict[i]['q'] = line;

             # Get the arguments from each query
             arguments = getarguments(line);
             queryDict[i]['arg'] = arguments;

            # Get the type of arguments
             if '|' not in line and ',' not in line:
                 queryDict[i]['argType'] = "margin";
             elif '|' in line:
                 queryDict[i]['argType'] = "conditional";
             else:
                 queryDict[i]['argType'] = "joint";

             # Get the type of query
             if(line[0] == "P"):
                queryDict[i]['type'] = "probability";
             elif(line[0] == "EU"):
                queryDict[i]['type'] = "utility";
             elif(line[0] == "MEU"):
                 queryDict[i]['type'] = "max utility";
        elif(querySeprator == 0 and line == "******"):
            querySeprator = 1;
            continue;

        # Get the bayesian network contents
        if(querySeprator == 1):
            if(line != "***"):
                # if the node is a child node
                if '|' in line:
                    # Split the node into child and parent node
                    nodeDiv = line.split(' |');
                    # Make the child node as the key in the network dict.
                    if nodeDiv[0] not in network:
                            network[nodeDiv[0]] = {};
                    # Add the parent node in the dict
                    nodeDiv[1] = nodeDiv[1].lstrip();
                    network[nodeDiv[0]]['parent'] = nodeDiv[1];
                    # The given node is the current node.
                    node = nodeDiv[0];
                # if the node is a parent node or standalone node.
                elif "0" not in line and "1" not in line and 'decision' not in line:
                    # if node is not in network add it to the network
                    if line not in network:
                        network[line] = {};
                    # Node is the current node
                    node = line;
                # No read the probability values from the file.
                else:

                    if (line == "decision"):

                    # if node does not have a parent then it is a standalone node. Just add single value.(+)
                    elif 'parent' not in network[node] and line != "decision":
                        network[node]['+'] = float(line);
                    # if node has multiple parents add for different combination of parent nodes the probability.
                    else:
                        parent = network[node]['parent'];
                        length = len(parent.split(' '));
                        # Split the line to get the prob value and the combination of parent nodes.
                        prob = line.split(' ');

                        # Make a string from the combination of parent nodes.
                        i = 2;
                        probStr = prob[1];
                        while(i <= length):
                             probStr += prob[i];
                             i= i+1;

                        # Add the prob value to the table.
                        network[node][probStr] = float(prob[0]);
            else:
                # if query seprator is encountered just move ahead
                continue;

    print network;
    quit();
    solveQuery(queryDict);

main();
