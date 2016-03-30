
import re;
import copy;
import string

import sys

clauses = list();
global output;

global intermediate;
intermediate = {};

class outerloop(): pass;

# function to get the different query predicates and the predicate terms
def getQueryTerms(query):

    queryPremise = list();
    queryPredicate = list();
    queryPredicateTerms = list();
    queryPremise = query.split(' && ');
    # Contain the two seprate querys

    for k, predicate in enumerate(queryPremise):
        queryPredicate.append(predicate.split('('));

    for j in queryPredicate:
        # Contain the query predicates to search for.
        queryPredicateTerms.append(j[0]);

    return queryPremise , queryPredicateTerms;

# function to get the predicate term from the given term
def getPredicate(term):
    predicate = term.split('(');
    return predicate[0];

def getArguments(term):
    arguments = list();
    pattern = re.compile(".*\((.*)\)");
    arguments = pattern.match(term).group(1);
    arguments = arguments.split(', ');
    return arguments;

def getPremiseTerms(sentence):
    premise = sentence.split(" => ");
    terms =  premise[0].split(" && ");
    return terms;

def getImplicationTerm(sentence):
     premise = sentence.split(" => ");
     term = premise[1];
     return term;


# function to display the KB.
def displayKB(KB):
    for i in KB:
        print i + ": " , KB[i];

def filewrite(action , query):

    line = action + ": " + query + "\n";
    output.write(line);


def replaceVar(term):
    arg = getArguments(term);
    for i, var in enumerate(arg):
        if var.islower():
            term = SubstituteVal(term,var,"_");
            #term = term.replace(var, "_");
    return term;

def replaceSub(premiseterms,sub,predicate,term):

    arg = getArguments(term);
    if predicate in sub:
        values = sub[predicate];
        for i, val in enumerate(arg):
            for k, term in enumerate(premiseterms):
                if val.islower():
                    premiseterms[k] = SubstituteVal(premiseterms[k],val,values[i]);
                    term = SubstituteVal(term,val,values[i]);
                    #premiseterms[k] = premiseterms[k].replace(val,values[i]);
                    #term = term.replace(val,values[i]);

    return premiseterms,term;

def Substitute(sentence, sub):


    newsentence = "";
    newSub = {};
    if '=>' in sentence:
        premise = getPremiseTerms(sentence);
        implication = getImplicationTerm(sentence);

        # get the premise terms and loop one by one
        for term in premise:

            predicate = getPredicate(term);
            # check if the predicate of premise is in sub
            if predicate in sub:


                 # if present get the arguments of the premise from the sentence.
                 arguments = getArguments(term);
                 # loop through the arguments one by one
                 for i,val in enumerate(arguments):
                     # if it is a standalone variable
                     if val.islower():
                         arguments[i] = sub[predicate][i];
                         if val not in newSub:
                             newSub[val] = sub[predicate][i];
                     else:
                         arguments[i] = val;


                 term = predicate + "(";
                 for j,value in enumerate(arguments):
                     if(j == 0 and len(arguments) == 1):
                         term = term + arguments[j]
                     elif( j == 0 and len(arguments) > 1):
                         term = term + arguments[j] + ",";
                     elif(j < len(arguments)-1 ):
                         term = term + " " +arguments[j] + ",";
                     else:
                         term = term + " " +arguments[j];

                 term = term + ")";



            if(newsentence == ""):
                newsentence = term;
            else:
                newsentence = newsentence + " && " + term;

        newsentence = newsentence + " => " + implication;


        arguments1 = list();
        newPremise = getPremiseTerms(newsentence);
        newImplication = getImplicationTerm(newsentence);
        newsentence = "";
        for newTerm in newPremise:
            for key in newSub:
                if key in newTerm:
                    arguments1 = getArguments(newTerm);
                    for j,arg in enumerate(arguments1):
                        if arg.islower() and arg ==key:
                            arguments1[j] = newSub[key];
                        else:
                            arguments1[j] = arg;

                    predicate = getPredicate(newTerm);
                    newTerm = predicate + "(";
                    for j,value in enumerate(arguments1):
                         if(j == 0 and len(arguments1) == 1):
                             newTerm =  newTerm + arguments1[j];
                         elif( j == 0 and len(arguments1) > 1):
                            newTerm =  newTerm + arguments1[j] + ",";
                         elif(j < len(arguments1)-1 ):
                            newTerm =  newTerm + " " +arguments1[j] + ",";
                         else:
                            newTerm =  newTerm + " " +arguments1[j];

                    newTerm =  newTerm + ")";

            if(newsentence == ""):
                newsentence = newTerm;
            else:
                newsentence = newsentence + " && " + newTerm;


        arguments1 = getArguments(newImplication);
        predicate = getPredicate(newImplication);
        for key in newSub:
            if key in newImplication:
                for i,arg in enumerate(arguments1):
                    if (arg.islower() and arg == key):
                        arguments1[i] = newSub[key];
                    else:
                        arguments1[i] = arg;



        newTerm = predicate + "(";
        for j,value in enumerate(arguments1):
            if(j == 0 and len(arguments1) == 1):
                 newTerm =  newTerm + arguments1[j];
            elif( j == 0 and len(arguments1) > 1):
                 newTerm =  newTerm + arguments1[j] + ",";
            elif(j < len(arguments1)-1 ):
                 newTerm =  newTerm + " " +arguments1[j] + ",";
            else:
                newTerm =  newTerm + " " +arguments1[j];

        newTerm =  newTerm + ")";


        newsentence = newsentence + " => " + newTerm
        return newsentence;

    else:
        predicate = getPredicate(sentence);
        arguments = getArguments(sentence);
        if predicate in sub:
            for i, arg in enumerate(arguments):
                if arg.islower():
                    arguments[i] = sub[predicate][i];
                else:
                    arguments[i] = arg;

        newTerm = predicate + "(";
        for j,value in enumerate(arguments):
            if(j == 0 and len(arguments) == 1):
                 newTerm =  newTerm + arguments[j];
            elif( j == 0 and len(arguments) > 1):
                 newTerm =  newTerm + arguments[j] + ",";
            elif(j < len(arguments)-1 ):
                 newTerm =  newTerm + " " +arguments[j] + ",";
            else:
                newTerm =  newTerm + " " +arguments[j];

        newTerm =  newTerm + ")";

        return newTerm;

def SubstituteVal(sentence,srcVal, subVal):
    if "=>" in sentence:
        premise = getPremiseTerms(sentence);
        implication = getImplicationTerm(sentence);
        newsentence = "";
        for term in premise:
            predicate = getPredicate(term);
            arguments = getArguments(term);
            for i, arg in enumerate(arguments):
                if arg.islower() and srcVal == arg:
                    arguments[i] = subVal;
                else:
                    arguments[i] = arg;

            newTerm = predicate + "(";
            for j,value in enumerate(arguments):
                if(j == 0 and len(arguments) == 1):
                    newTerm =  newTerm + arguments[j];
                elif( j == 0 and len(arguments) > 1):
                   newTerm =  newTerm + arguments[j] + ",";
                elif(j < len(arguments)-1 ):
                     newTerm =  newTerm + " " +arguments[j] + ",";
                else:
                    newTerm =  newTerm + " " +arguments[j];

            newTerm =  newTerm + ")";

            if(newsentence == ""):
              newsentence = newTerm;
            else:
              newsentence = newsentence + " && " + newTerm;


        arguments = getArguments(implication);
        predicate = getPredicate(implication);
        for i,arg in enumerate(arguments):
            if arg.islower() and arg == srcVal:
                arguments[i] = subVal;
            else:
                arguments[i] = arg;

            newTerm = predicate + "(";
            for j,value in enumerate(arguments):
                if(j == 0 and len(arguments) == 1):
                    newTerm =  newTerm + arguments[j];
                elif( j == 0 and len(arguments) > 1):
                   newTerm =  newTerm + arguments[j] + ",";
                elif(j < len(arguments)-1 ):
                     newTerm =  newTerm + " " +arguments[j] + ",";
                else:
                    newTerm =  newTerm + " " +arguments[j];

            newTerm =  newTerm + ")";

        newsentence = newsentence + " => " + newTerm
        return newsentence;
    else:
        predicate = getPredicate(sentence);
        arguments = getArguments(sentence);
        for i, arg in enumerate(arguments):
            if arg.islower() and arg == srcVal:
                arguments[i] = subVal;
            else:
                arguments[i] = arg;

            newTerm = predicate + "(";
            for j,value in enumerate(arguments):
                if(j == 0 and len(arguments) == 1):
                    newTerm =  newTerm + arguments[j];
                elif( j == 0 and len(arguments) > 1):
                   newTerm =  newTerm + arguments[j] + ",";
                elif(j < len(arguments)-1 ):
                     newTerm =  newTerm + " " +arguments[j] + ",";
                else:
                    newTerm =  newTerm + " " +arguments[j];

            newTerm =  newTerm + ")";

    return newTerm;

def constructTerm(predicate, arguments):

        newTerm = predicate + "(";
        for j,value in enumerate(arguments):
            if(j == 0 and len(arguments) == 1):
                 newTerm =  newTerm + arguments[j];
            elif( j == 0 and len(arguments) > 1):
                 newTerm =  newTerm + arguments[j] + ",";
            elif(j < len(arguments)-1 ):
                 newTerm =  newTerm + " " +arguments[j] + ",";
            else:
                newTerm =  newTerm + " " +arguments[j];

        newTerm =  newTerm + ")";
        return newTerm;

def Ask(KB,query):

    # Get the query terms
    result = getQueryTerms(query);
    queryComp = result[0];

    truth = 0;
    # for each query term if not an atomic query
    for comp in queryComp:
        substituition = {};
        # get the predicate symbol for the query.
        predicate = getPredicate(comp);
        query1 = replaceVar(comp);
        filewrite("Ask", query1);
        substituition = {};
        val = BackChainingOR(KB,predicate,comp);
        truthVal = val[0];
        sub = val[1];
        if(truthVal):
            comp = Substitute(comp,sub);
            arguments = getArguments(comp);
            variable = 1;
            for each in arguments:
                if each.islower():
                    variable = 0;
                    break;
                else:
                    continue;
            if(variable):
                filewrite("True", comp);
            truth = 1;

        else:
            comp = replaceVar(comp);
            filewrite("False",comp);
            truth = 0;
            break;


    if(truth):
        output.write("True");
    else:
        output.write("False");

def BackChainingOR(KB, predicate, query):

   predicates = list();
   substituition = {};
   multipleUnifiers = {};

   if predicate not in KB:
       return False,substituition;


   # Get the first sentence for the given predicate and start making inferences from that predicate.
   for component in (KB[predicate]):

      # Rule matching in the KB.
      sentence = KB[predicate][component]['sentence'];
      arguments = KB[predicate][component]['arguments'];

      # Get the argument from the query.
      arg = getArguments(query);

      if "=>" in sentence:
        #replace the known variables in the sentence from the query
        for i, comp in enumerate(arguments):
            if len(arg[i]) > 1:
               sentence = SubstituteVal(sentence, comp , arg[i]);
               #sentence = sentence.replace(comp,arg[i]);

        # Get the premise terms from the implication.
        premiseTerms = getPremiseTerms(sentence);
        implicationTerm = getImplicationTerm(sentence)


        continueValue = 0;
        implicationArguments  = getArguments(implicationTerm);
        argumentsQuery  = getArguments(query);
        for t1, args in enumerate(argumentsQuery):
            if args[0].isupper():
                if( args == implicationArguments[t1]):
                        continue;
                else:
                    if(component +1 < len(KB[predicate])):
                        continueValue = 1;
                        break;
                    else:
                        return False,substituition,multipleUnifiers;


        if(continueValue):
            continue;





        returnValues = BackChainingAnd(KB, premiseTerms,implicationTerm,sentence);

        # Get back the truth value and the valid substiution.
        truthVal = returnValues[0];
        sub = returnValues[1];
        multipleUnifiers = returnValues[2];
        termNum = returnValues[3];

        if(truthVal):
            #sentence = sentence.replace(j,sub[val][k]);
            sentence = Substitute(sentence,sub);
            if(len(multipleUnifiers)):
               if "sentences" not in multipleUnifiers:
                   multipleUnifiers["sentences"] = {};
               length = len(multipleUnifiers['sentences']);
               multipleUnifiers['sentences'][length] = implicationTerm;
               print multipleUnifiers;

            part = sentence.split( " => " );
            lpart = part[0];
            rpart = part[1];

            val1 = getPredicate(rpart);

            arg = getArguments(rpart);
            if val1 not in sub:
                sub[val1] = list();
            sub[val1] = arg;

            return truthVal,sub,multipleUnifiers;
        else:

            if(component + 1 < len(KB[predicate])):

                implication = getImplicationTerm(sentence);
                argumentsImplication = getArguments(implication);
                for i,a in enumerate(argumentsImplication):
                    if a.islower():
                        implication = SubstituteVal(implication,a,"_");

                implication = replaceVar(implication);
                filewrite("Ask",implication);
                continue;

            else:
                if(len(multipleUnifiers)):
                    for position, unifier in enumerate(multipleUnifiers["unifiers"]):
                        try:

                            filewrite("Ask",multipleUnifiers["parent"]);
                            parent = multipleUnifiers["parent1"];
                            sen = multipleUnifiers['parent'];
                            predicate = getPredicate(sen);
                            term = constructTerm(predicate,unifier);
                            filewrite("True",term);
                            arguments = getArguments(parent);
                            substiute = "";
                            for i,var1 in enumerate(arguments):
                                if var1.islower():
                                    substiute = multipleUnifiers["unifiers"][position][i];
                                    currentSub = multipleUnifiers["ParentSub"][i];

                            print currentSub;

                            lengthSen = len(multipleUnifiers["sentences"]);

                            for number,sent in enumerate(multipleUnifiers["sentences"]):
                               if(number+1 < lengthSen):
                                    sentenceSeq = multipleUnifiers["sentences"][sent];
                                    predicate1 = getPredicate(sentenceSeq);
                                    argumentsSeq = getArguments(sentenceSeq);

                                    for value, argu in enumerate(argumentsSeq):
                                        if argu.islower():
                                            argumentsSeq[value] = substiute;

                                        else:
                                            argumentsSeq[value] = argu;
                                    newterm = constructTerm(predicate1,argumentsSeq);
                                    filewrite("True", newterm);
                               else:
                                   finalSent = multipleUnifiers["sentences"][sent];
                                   predicateFinal = getPredicate(finalSent);
                                   argument1 = getArguments(finalSent);
                                   print argument1;
                                   for i,arg in enumerate(argument1):
                                       if arg.islower():
                                           argument1[i] = substiute;

                                   term = constructTerm(predicateFinal,argument1);

                                   filewrite("Ask",term);
                                   for terms in  KB[predicateFinal]:
                                       if(term == KB[predicateFinal][terms]["sentence"]):
                                           filewrite("True",term);
                                           newPremises = list();
                                           for i,variable in enumerate(premiseTerms):
                                               if i <= termNum:
                                                   continue;
                                               else:
                                                   variable = variable.replace(currentSub,substiute);
                                                   newPremises.append(variable);

                                           print newPremises,sentence;

                                           values = BackChainingAnd(KB,newPremises,implicationTerm,sentence);
                                           truth = values[0];
                                           if(truth):
                                               return True,substituition,multipleUnifiers;
                                           else:
                                               raise outerloop();
                                   else:
                                       filewrite("False",term);
                                       continue;
                                   filewrite("False",term);

                        except outerloop:
                            pass;
                    return truthVal,sub,multipleUnifiers;
                else:
                    return truthVal,sub,multipleUnifiers;
      else:
          print sentence,query;

          sentenceArg = getArguments(sentence);
          lengthArg = len(sentenceArg);
          print sentenceArg;
          queryArguments = getArguments(query);
          lengthQuery = len(queryArguments);
          print queryArguments;
          truthAtomic = 0;

          if(sentence == query):
              return True,substituition,multipleUnifiers;
          elif(lengthQuery == lengthArg and sentence!=query):
              for k,each in enumerate(queryArguments):
                  if each.islower() or each == sentenceArg[k]:
                      truthAtomic = 1;

                  else:
                      truthAtomic = 0;
                      break;

              if(truthAtomic):
                  filewrite("True",sentence);
                  return True,substituition,multipleUnifiers;
              else:
                  if(component +1 <len(KB[predicate])):
                      continue;
                  else:
                    return False,substituition,multipleUnifiers;

          else:
              return False,substituition,multipleUnifiers;

def BackChainingAnd(KB, premiseTerms,implicationTerm,sentence):
    substituition = {};
    # Get each of the premise term which will act as a query
    predicateAnd = "";
    premises ="";
    multipleUnifiers = {};
    termNum = 0;
    for termNum, term in enumerate(premiseTerms):

      if "unifiers" not in multipleUnifiers:
          multipleUnifiers = {};

      if len(multipleUnifiers):
          if "sentences" in multipleUnifiers:
              length = len(multipleUnifiers["sentences"]);
              premises = getPremiseTerms(sentence);
              multipleUnifiers["sentences"][length] = premises[termNum];

      # premise term,predicate
      predicateAnd = getPredicate(term);
      argumentsAnd = getArguments(term);

      # substitute variable arguments with underscore;
      substitutedTerm = term;
      for val in argumentsAnd:
          if val[0].islower():
              substitutedTerm  = SubstituteVal(term,val,"_");
              #substitutedTerm = term.replace(val,"_");



      substitutedTerm = replaceVar(substitutedTerm);

      filewrite("Ask", substitutedTerm);

      if predicateAnd not in KB:
          filewrite("False",substitutedTerm);
          return False,substituition,multipleUnifiers,termNum;

      # loop through all the sentences that belong to the given predicate
      for j, iter in enumerate(KB[predicateAnd]):

         length = len(KB[predicateAnd]);
         # check if the sentence in the knowledge base is atomic or not
         if(KB[predicateAnd][iter]['type'] == "atomic"):
            # if atomic and term matches the sentence in KB, then the truth value is success
            if((term == KB[predicateAnd][iter]['sentence'])):
                    filewrite("True", KB[predicateAnd][iter]['sentence']);
                    if predicateAnd not in substituition:
                        substituition[predicateAnd] = list();
                        substituition[predicateAnd] = (KB[predicateAnd][iter]['arguments']);
                        break;

            elif(len(argumentsAnd) == KB[predicateAnd][iter]['number'] and (term != KB[predicateAnd][iter]['sentence']) ):
                  truthVal = 0;
                  for k, each in enumerate(argumentsAnd):
                        if( each.islower() or each == KB[predicateAnd][iter]['arguments'][k] ):
                                truthVal = 1;
                        else:
                                truthVal = 0;
                                break;

                  if(truthVal):

                      if predicateAnd not in substituition:
                        if not multipleUnifiers:
                              filewrite("True", KB[predicateAnd][iter]['sentence']);
                              substituition[predicateAnd] = list();
                              substituition[predicateAnd] = (KB[predicateAnd][iter]['arguments']);
                              multipleUnifiers['parent'] = substitutedTerm;
                              multipleUnifiers['parent1'] = term;
                              multipleUnifiers['ParentSub'] = KB[predicateAnd][iter]['arguments'];
                        else:
                              if "unifiers" not in multipleUnifiers:
                                  multipleUnifiers["unifiers"] = list();
                              multipleUnifiers["unifiers"].append(KB[predicateAnd][iter]['arguments']);
                              continue;



                      else:
                          if not multipleUnifiers:
                              filewrite("True", KB[predicateAnd][iter]['sentence']);
                              multipleUnifiers['parent'] = substitutedTerm;
                              multipleUnifiers['parent1'] = term;
                              multipleUnifiers['ParentSub'] = KB[predicateAnd][iter]['arguments'];
                          else:
                              if "unifiers" not in multipleUnifiers:
                                  multipleUnifiers["unifiers"] = list();
                              multipleUnifiers["unifiers"].append(KB[predicateAnd][iter]['arguments']);
                              continue;

                          arguments = getArguments(term);
                          implicationargu = getArguments(implicationTerm);
                          for i, impArg in  enumerate(implicationargu):
                            if impArg.islower():
                                if impArg in arguments:
                                    substituition[predicateAnd] = KB[predicateAnd][iter]['arguments'];

                  else:
                      if(j + 1 < len(KB[predicateAnd])):
                          continue;
                      else:

                        if(len(multipleUnifiers)):
                           if "sentences" in multipleUnifiers:
                                 termVal = replaceVar(term);
                                 filewrite("False", termVal );
                                 return False,substituition,multipleUnifiers,termNum;
                           else:
                               break;

                        else:
                            termVal = replaceVar(term);
                            filewrite("False", termVal );
                            return False,substituition,multipleUnifiers,termNum;
            else:

                termVal = replaceVar(term);
                filewrite("False", termVal );
                return False,substituition,multipleUnifiers,termNum;

         # if the senentence matches to an implication.
         elif(KB[predicateAnd][iter]['type'] == "implication"):
             #get the predicate of the component term which is implication in the KB
             predicate = getPredicate(term);
             value = BackChainingOR(KB,predicate,term);
             # the substiution and the truth value for the given implication from the KB
             sub = value[1];
             truth = value[0];
             multipleUnifiers = value[2];


             # Get the arguments and the predicate for the given component term in the query
             predi = getPredicate(term);
             argu  = getArguments(term);


             # if there is a substitution for the given predicate then enter the condition.
             if predi in sub:
                   # get the substitutions for the predicate.
                   substituition[predi] = sub[predi];
                   values =  sub[predi];
                   # loop through each of the individual values of arguments
                   for m,val1 in enumerate(argu):
                       #loop through the premise terms
                       for t,term1 in enumerate(premiseTerms):
                           # only if it is a variable argument replace occurence with ones from substitutions.
                           if(val1.islower()):
                             premiseTerms[t] = SubstituteVal(premiseTerms[t],val1,values[m]);
                             term = SubstituteVal(term,val1,values[m]);
                            #premiseTerms[t] = premiseTerms[t].replace(val1, values[m]);
                            #term = term.replace(val1,values[m]);

             if(truth):
                filewrite("True",term);
                break;
             else:
                 term = replaceVar(term);
                 filewrite("False",term);
                 return False,substituition,multipleUnifiers,termNum;

      # Arguments of the predicate term
      returnValues = replaceSub(premiseTerms,substituition,predicateAnd,term);
      premiseTerms = returnValues[0];
      term = returnValues[1];

    return True,substituition,multipleUnifiers,termNum;

def main():

    KB = {};

    #open input file to read data
    fhandle = open("sample.txt","r");
    #fhandle = open(sys.argv[2], "r");

    for i, line in enumerate(fhandle):
        line = line.strip('\n');
        line = line.strip('\r');

        # to read the first line from the input file . Query that needs to be checked.
        if(i == 0):
            query = line;

        if(i == 1):
            # Number of Clauses that are there in the knowledge base
            numberClauses = int(line);

        if(i>=2 and i<2+numberClauses):
            clauses.append(line);

            # if the sentence is an implication.
            if '=>' in line:
                # split the term into premise and conclusion.
                keyword = line.split(' => ');
                premiseTerm = keyword[0];
                implicationTerm = keyword[1];
                keyword = keyword[1].split('(');


                if keyword[0] not in KB:
                    # Declare another dictionary for each predicate.
                    KB[keyword[0]] = {};

                # Keep assigning sentences according to increasing lenth for each predicate keyword.
                length = len(KB[keyword[0]]);
                if length not in KB[keyword[0]]:
                    KB[keyword[0]][length] = dict();
                # Assign the sentence where we found this keyword.
                KB[keyword[0]][length]['sentence'] = line;

                 # Find the arguments in the predicate
                arguments = list();
                pattern = re.compile(".*\((.*)\)");
                arguments = pattern.match(implicationTerm).group(1);
                arguments = arguments.split(', ');

                for k, arg in enumerate(arguments):
                    if arg[0].islower():
                        arguments[k] = arg;

                # Assign the arguments to the keyword.
                KB[keyword[0]][length]['arguments'] = arguments;

                # Number of aguments of each predicate
                numberArg = len(arguments);
                KB[keyword[0]][length]['number'] = numberArg;


                #Get the truth value. If the sentence just has constant terms then it will have a truth value have 1
                #if it contains any variable, then it has a truth of -1. If the sentence is a negation then it will have a value of 0.
                truthvalue = 1;
                for i in arguments:
                    if i[0].isupper():
                        continue;
                    elif i[0].islower():
                        truthvalue = -1;
                        break;

                if '~' in keyword[0]:
                    truthvalue = 0;
                KB[keyword[0]][length]['truth'] = truthvalue;

                # Type of the clause . Is it implication or an atomic sentence.
                KB[keyword[0]][length]['type'] = "implication";

                premisePredicates = premiseTerm.split(' && ');
                KB[keyword[0]][length]['premise'] = premisePredicates;

            else:
                # if it is just an atomic sentence.(No implication)
                # First get the predicate term that will be the keyword. If we split the first term in the split will be the predicate.
                keyword = line.split('(');
                if keyword[0] not in KB:
                    # Declare another dictionary for each predicate.
                    KB[keyword[0]] = {};

                # Keep assigning sentences according to increasing lenth for each predicate keyword.
                length = len(KB[keyword[0]]);
                if length not in KB[keyword[0]]:
                    KB[keyword[0]][length] = dict();
                # Assign the sentence where we found this keyword.
                KB[keyword[0]][length]['sentence'] = line;

                # Find the arguments in the predicate
                arguments = list();
                pattern = re.compile(".*\((.*)\)");
                arguments = pattern.match(line).group(1);
                arguments = arguments.split(', ');

                #standarize the arguments as seprate variables for each clause.
                for k, arg in enumerate(arguments):
                    if arg[0].islower():
                        arguments[k] = arg;

                # Assign the arguments to the keyword.
                KB[keyword[0]][length]['arguments'] = arguments;

                # Number of aguments of each predicate
                numberArg = len(arguments);
                KB[keyword[0]][length]['number'] = numberArg;

                #Get the truth value. If the sentence just has constant terms then it will have a truth value have 1
                #if it contains any variable, then it has a truth of -1. If the sentence is a negation then it will have a value of 0.
                truthvalue = 1;
                for i in arguments:
                    if i[0].isupper():
                        continue;
                    elif i[0].islower():
                        truthvalue = -1;
                        break;

                if '~' in keyword[0]:
                    truthvalue = 0;
                KB[keyword[0]][length]['truth'] = truthvalue;

                # Type of the clause . Is it implication or an atomic sentence.
                KB[keyword[0]][length]['type'] = "atomic";

    global output;
    output = open("output.txt", "w");
    #print(KB);
    Ask(KB,query);

    output.close();
main();
