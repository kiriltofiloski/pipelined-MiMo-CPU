import sys
import re

opcodeArr = {
    "add" : 0
}

opcodeArgList = {
    0 : ["r,r,r", "r,r,i"] #these will be filled with proper regex mathing phrases
}

labelsArr = {
    "labelName" : 4 #address location
}

condsArr = {
    "al" : 0,
    "eq" : 1
}

allLines = []
addressCounter = 0
markNextLine = False
label = ''

#First loop that looks for labels
for line in allLines:
    line = line.stripLeadingAndTrailingSpaces()
    if line.contains('@'):          #if line contains comment, delete evrythig after the comment
        line = line.before('@')
        allLines[line] = line       #strip comment for later too so we don't do it again in next loop

    if line.contains(':'):
        label = line.before(':')
        if line.after(':').isBlank() and not markNextLine:   #if line is a label line only like ' lableName:   ' 
            markNextLine = True                              #mark the next line after to be marked
        elif line.after(':').isBlank() and markNextLine:
            print("Error! Can't have label that points to other label") 
            break                                          #in our first implementation we will not make nested lables possible, maybe later
        else:
            labelsArr[label] = addressCounter   #if label and instruction are on same line like ' lableName: add r1,r2,r3'
            addressCounter += 1                 #add the current address to the lablesArr and increase the counter
    elif markNextLine:
        labelsArr[label] = addressCounter   #next line after lable that is to be marked
        addressCounter += 1
    elif line.isNotBlank():
        addressCounter += 1                 #only increase addresscounter on non-blank lines
                                            #since we removed comments, all lines should either be instructions or labels


#Second loop that decodes instructions
for line in allLines:
    firstWord = line.before("first white space")
    opcode = None
    condition = "al"
    setFlags = 0

    if firstWord.inside(opcodeArr): #check if whole word is just the opcode
        opcode = firstWord
    else:
        opcodeMaybe = firstWord.before('last 2 letters') #check if opcode plus condition
        conditionMaybe = firstWord('last 2 letters')
        if opcodeMaybe.inside(opcodeArr) and conditionMaybe.inside(condsArr):
            opcode = opcodeMaybe
            condition = conditionMaybe
        else:
            if firstWord.lastLetter == 's':         
                firstWord = firstWord.before("last letter")
                opcodeMaybe = firstWord.before('last 2 letters')
                conditionMaybe = firstWord('last 2 letters')
                if opcodeMaybe.inside(opcodeArr) and conditionMaybe.inside(condsArr):  #check if opcode plus condition plus S flag
                    opcode = opcodeMaybe
                    condition = conditionMaybe
                    setFlags = 1
                elif firstWord.inside(opcodeArr):   #check if opcode plus S flag
                    opcode = firstWord
                    setFlags = 1
                else:
                    print("Error! Unknown instruction at line: '" + line + "'")
                    break
            else:
                print("Error! Unknown instruction at line: '" + line + "'")
                break
    #Now we have to get the arguments for the operation
    args = line.after("first white space")
    rd = 0
    rs = 0
    rt = 0
    immed = 0
    label = 0
    
    if args.matchAnyIn(opcodeArgList, opcode):
        rd = args.GetInInst("regex to find proper one") 
        rs = args.GetInInst("regex to find proper one")
        rt = args.GetInInst("regex to find proper one") 
        immed = args.GetInInst("regex to find proper one")
        label = args.GetInInst("regex to find proper one")  
    else:
        print("Error! Improper arguments at line: '" + line + "'")
    #Then we just convert everything to pseudo code and write this instruction
