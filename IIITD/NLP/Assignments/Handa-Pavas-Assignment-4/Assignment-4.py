import nltk
import six
from string import letters
import copy
import os.path
from node import Node
#python-2.7
sentences = []
#load the grammar
productions = {}
states = []
grammar = nltk.data.load("grammars/large_grammars/atis.cfg")
for i in range(len(grammar.productions())):
    key = grammar.productions()[i].lhs()
    key=str(key)
    value=list(grammar.productions()[i].rhs())
    for i in range(len(value)):
        if isinstance(value[i], (str, unicode)):
            value[i]="'"+value[i]+"'"
        else:
            value[i]=str(value[i])
    if key not in states:
        states.append(key)    
        productions[key]=[value]
    else:
        if value not in productions[key]:
            productions[key].append(value)
##productions ={}
##states = []
##with open('/home/pavas/Desktop/atis-grammar-original.cfg', 'r') as f:
##    text =f.read().split('\n')
##    text = text[0:len(text)-1]
##    for i in text:
##        split =i.split(" -> ")
##        key=split[0]
##        value=list(split[1].split())
##        for i in range(len(value)):
##            value[i]=str(value[i])
##            if productions[key]==None:
##                states.append(key)
##                productions[key]=[]
##            else:
##                if value not in productions[key]:
##                    productions[key].append(value)
##Rule_1: Modifying large rules to small ones
def large():
    count =0
    #Productions length change due to elimination,
    #thus need to maintain a copy of it.
    temp_dict = copy.deepcopy(productions)
    for key in temp_dict:
        values = temp_dict[key]
        for i in range(len(values)):
            # Check if we have a rule violation
            if len(values[i]) > 2:
            
                # A -> BCD gives 1) A-> BE (if E is the first "free"
                # letter from letters pool) and 2) E-> CD
                for j in range(0, len(values[i]) - 2):
                    # replace first rule
                    if j==0:
                        new = []
                        new .append(productions[key][i][0])
                        letter = 'A'+str(count)
                        new.append(letter)
                        count+=1
                        productions[key][i] = new
                    # add new productions
                    else:
                        new = []
                        new.append(values[i][j])
                        letter = 'A'+str(count)
                        new.append(letter)
                        count+=1
                        productions.setdefault(new_key, []).append(new)
                    states.append(letter)
                    # save letter, as it'll be used in next rule
                    new_key = copy.deepcopy(letter)
                    
                    
                # last 2 letters remain always the same
                productions[new_key]=[]
                productions[new_key].append(values[i][-2:])

    


    
###Rule_2: Eliminating Null Productions
##def eliminate_null():
##    #Productions length change due to elimination,
##    #thus need to maintain a copy of it.
##    temp_dict = productions.copy()
##    null_production_lhs = []
##    #traversing each item in dictionary
##    for i in temp_dict.items():
##        for j in i[1]:
##            if len(j)==1 and j == 'e' and i[0] not in null_production_lhs:
##                null_production_lhs.append(i[0])
##                productions[i[0]].remove(j)
##        if len(productions[i[0]]) == 0:
##            rhs.remove(i[0])
##            productions.pop(i[0], None)
##    # modified productions list with elimination of null productions partially
##    temp_dict = productions.copy()
##    # Modifying productions of form A->BC where either B is null and C not, or
##    # C is null and B not or of form A->BA where B is null and A->BB where B is null
##    for i in temp_dict.items():
##        for j in i[1]:
##            if len(j) == 2:
##                productions[i[0]] =[]
##                if j[0] == j[1] and j[0] in null_production_lhs:
##                    rhs.remove(i[0])
##                    productions(i[0]).pop(i[0], [])
##                elif j[0] in null_production_lhs:
##                    if i[0] != j[1]:
##                        productions(i[0]).append(j[1])
##                    else:
##                        rhs.remove(i[0])
##                        productions(i[0]).pop(i[0], [])
##                elif j[1] in null_production_lhs:
##                    if j[0]!= i[0]:
##                        productions(i[0]).append(j[0])
##                    else:
##                        rhs.remove(i[0])
##                        productions(i[0]).pop(i[0], [])

#Rule_3: Remove short productions (A->B)
def short():
    flag = 1
    count = 0
    while flag:
        count+=1
##        print(count)
        flag = 0
        temp_dict = copy.deepcopy(productions)
        for key in temp_dict:
            values = temp_dict[key]
            for i in range(len(values)):
                # Check if we have a rule violation
                if len(values[i])==1 and values[i][0] in states and values[i][0]!= key:
                    new = copy.deepcopy(values[i][0])
##                    print(key,values[i])
                    productions[key].remove(values[i])
                    new_value = productions[new]
                    for j in range(len(new_value)):
                        productions[key].append(new_value[j])
        
        for key in productions:
            values = productions[key]
            for k in range(len(values)):
                # Check if we have a rule violation
                if len(values[k])==1 and values[k][0] in states and values[k][0]!= productions[values[k][0]]:
                    flag=1
                    break
            if flag:
                break
        
    

 
# Print productions
def print_rules(a):
   
    with open('/home/pavas/IIITD/NLP/Assignments/'+a+'.txt', 'w')as f:
        count = 0
        for key in productions:
            values = productions[key]
            for i in range(len(values)):
                string =""
                count+=1
                string+=key+'->'+str(values[i])+'\n'
                f.write(string)
        print(count)


def remove():
    #Remmoving Duplicacy
    temp_dict = copy.deepcopy(productions)
    for key in temp_dict:
        values = temp_dict[key]
        new =[]
        for i in values:
            if i in new:
                productions[key].remove(i)
            else:
                new.append(i)
def parser(sen):
    n = len(sen)
    for i in range(len(sen)):
        sen[i]="'"+sen[i]+"'"
    matrix = [[[] for i in range(n)] for j in range(n)]
    back_tracker = [[[] for i in range(n)] for j in range(n)]
    # Not considering 0,0 thus j starts from 1
    for j in range(1, n):
        for key in productions:
            val  = productions[key]
            for i in val:
                if len(i)==1 and sen[j-1]==i[0]:
                    matrix[j-1][j].append(key)
                    back_tracker[j - 1][j].append(Node(key, None, None, sen[j - 1]))
        #traversing in reverse form
        for i in reversed(range(0, j - 1)):
            for k in range(i + 1, j):
                for key in productions:
                    values = productions[key]
                    for v in range(len(values)) :
                        if len(values[v]) == 2:
                            first = values[v][0]
                            second = values[v][1]
                            if first in matrix[i][k] and second in matrix[k][j]:
                                matrix[i][j].append(key)
                                for b in back_tracker[i][k]:
                                    for c in back_tracker[k][j]:
                                        if b.root == first and c.root == second:
##                                            print(b, c)
                                            back_tracker[i][j].append(Node(key, b, c, None))
##    print(back_tracker)
    return back_tracker[0][n-1]
        
def tree(root, ind):
    if root.status:
        return '(' + root.root + ' ' + root.terminal + ')'
    
    l = ind + 2 + len(root.left.root) 
    r = ind + 2 + len(root.right.root) 
    left = tree(root.left, l)
    right = tree(root.right, r)
    return '(' + root.root + ' ' + left + '\n' + ' '*ind + right + ')'
def main():

    print '\nRules after loading initial productions from ATIS'
    print_rules('1')
    # remove large productions and print new productions
    print '\nRules after large productions removal'
    large()
    print_rules('2')
    
        

    # remove empty productions and print new productions
    #print '\nRules after empty productions removal'
    #empty()
    #print_rules()
    

    print '\nRules after short productions removal i.e. final cnf form'
    short()
    #remove()
    print_rules('3')
    
    #implementing CKY parser
    #For CKY we require two things grammar and sentence
    ### load the raw sentences
    s = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "raw")
    ### extract the test sentences
    t = nltk.parse.util.extract_test_sentences(s)
    
    for sentence in t:
        sentences.append(sentence[0])
    sen_count=95
##        with open("/home/pavas/IIITD/NLP/Assignments/Parses_counts.txt", 'w') as f:
##            with open("/home/pavas/IIITD/NLP/Assignments/Parse_trees.txt", 'w')as t:
##                for sen in sentences:
    sen = sentences[95]
    back_tracker=parser(sen)
##      print(back_tracker)
    start = str(grammar.start())
    flag = 0
    count =0
    
    sen_count+=1
    for node in back_tracker:
##            print(node)
        if node.root == start:
            count+=1
            print("Parse trees for sentence "+str(sen_count)+":\n")
            print(tree(node, 3))
            print("\n-------------------------------------------*-----------------------------------------------\n")
            flag = 1

    if flag==0:
            print('Sentence not recognizable\n')
    sentence=""
    for i in sen:
        sentence+=i
    print("Sentence_"+str(sen_count))
    print('\t')
    print(str(count))
    print("\n")
    print(count)
                    

main()
