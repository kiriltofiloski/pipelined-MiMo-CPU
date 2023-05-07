import sys
import re

opcodeArr = {
    "mov" : 0,
    "mvn" : 1,
    "add" : 2,
    "sub" : 3,
    "rsb" : 4,
    "mul" : 5,
    "div" : 6,
    "rem" : 7,
    "and" : 8,
    "orr" : 9,
    "eor" : 10,
    "nand" : 11,
    "nor" : 12,
    "bic" : 13,
    "cmp" : 14,
    "cmn" : 15,
    "tst" : 16,
    "teq" : 17,
    "lsl" : 18,
    "lsr" : 19,
    "asr" : 20,
    "ror" : 21,
    "rol" : 22,
    "j" : 23,
    "b" : 24,
    "bl" : 25,
    "ldr" : 26,
    "str" : 27,
    "nop" : 28,
}

opcodeArgList = {
    0 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    1 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    2 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    3 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    4 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    5 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    6 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    7 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    8 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    9 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    10 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    11 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    12 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    13 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    14 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    15 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    16 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    17 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    18 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    19 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    20 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    21 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    22 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    23 : ["^\s*#-?[0-9]+\s*$", "^\s*\w+\s*$", "^\s*r[0-7]\s*$"],
    24 : ["^\s*#-?[0-9]+\s*$", "^\s*\w+\s*$", "^\s*r[0-7]\s*$"],
    25 : ["^\s*#-?[0-9]+\s*$", "^\s*\w+\s*$", "^\s*r[0-7]\s*$"],
    26 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"], 
    27 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    28 : ["\s*"]
}

# "^r[0-7],\s*r[0-7],\s*r[0-7]\s*$" this is r1,r2,r3
# "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$" this is r1,r2,#5
# This just checks if immediate is number, we have to afterwards check if it's in range -512 to 511
# "^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$" These are r1,r2 and r1,#5
# "^\s*#-?[0-9]+\s*$" just #5
# "^\s*\w+\s*$" any label 


condsArr = {
    "al" : 1,
    "eq" : 2,
    "ne" : 3,
    "cs" : 4,
    "cc" : 5,
    "mi" : 6,
    "pl" : 7,
    "vs" : 8,
    "vc" : 9,
    "hi" : 10,
    "ls" : 11,
    "ge" : 12,
    "lt" : 13,
    "gt" : 14,
    "le" : 15,
}
    
labelsArr = {}
linesClean = []
addressCounter = 0
markNextLine = False
label = ""

instructionsArr = []

with open(sys.argv[1]) as f:
    #First we remove multiline comments
    fClean = re.sub(r'/\*[\s\S]*?\*/', '', f.read())

    #First loop that looks for labels
    for line in fClean.splitlines():
        line = line.strip()
        line = line.lower()

        if "@" in line:
            line = line.split("@", 1)[0]    #if line contains comment, delete everythig after the comment

        if ":" in line:
            label = line.split(":", 1)[0]
            afterLabel = line.split(":", 1)[1]

            if afterLabel == "" and not markNextLine:   #if line is a label line only like ' lableName:   ' 
                markNextLine = True                     #mark the next line after to be marked
            elif afterLabel == "" and markNextLine:
                print("Error! Can't have label that points to other label") #in our first implementation we will not make nested lables possible, maybe later
                sys.exit()
            else:
                labelsArr[label] = addressCounter   #if label and instruction are on same line like ' lableName: add r1,r2,r3'
                addressCounter += 1  
                linesClean.append(afterLabel.strip())       #add the current address to the lablesArr and increase the counter
        elif markNextLine:
            labelsArr[label] = addressCounter       #next line after lable that is to be marked
            addressCounter += 1
            linesClean.append(line) 
            markNextLine = False
        elif line != "":                            #only increase addresscounter on non-blank lines
            addressCounter += 1                     #since we removed comments, all lines should either be instructions or labels
            linesClean.append(line) 
    
    #Second loop that decodes instructions
    for lineNum, line in enumerate(linesClean):
        firstWord = re.split(r'\s+', line, 1)[0]
        opcode = None
        condition = "al"
        setFlags = 0

        #Decode opeariotn first
        if firstWord in opcodeArr:  #check if whole word is just the opcode
            opcode = firstWord
        else:
            opcodeTemp = firstWord[:-2] #check if opcode plus condition
            condTemp = firstWord[-2:]
            if opcodeTemp in opcodeArr and condTemp in condsArr:
                opcode = opcodeTemp
                condition = condTemp
            else:
                if firstWord[-1:] == "s":
                    firstWord = firstWord[:-1]
                    opcodeTemp = firstWord[:-2]
                    condTemp = firstWord[-2:]
                    if opcodeTemp in opcodeArr and condTemp in condsArr:    #check if opcode plus condition plus S flag
                        opcode = opcodeTemp
                        condition = condTemp
                        setFlags = 1
                    elif firstWord in opcodeArr:   #check if opcode plus S flag
                        opcode = firstWord
                        setFlags = 1
                    else:
                        print("Error! Unknown instruction at line: '" + line + "'")
                        sys.exit()
                else:
                    print("Error! Unknown instruction at line: '" + line + "'")
                    sys.exit()
        
        #if cmp,cmn,tst,teq operation set flags is set by default
        if opcode in ["cmp", "cmn", "tst", "teq"]:
            setFlags = 1
        
        #Now we decode the arguments
        opcode = opcodeArr[opcode]
        if len(re.split(r'\s+', line, 1)) > 1:
            args = re.split(r'\s+', line, 1)[1]
        else:
            args = " "
        argsSyntaxRight = False
        Rd = 0
        Rs = 0
        Rt = 0
        immed = 0
        imload = 0
        label = None
        labelIsImmed = False

        #Check if argument syntax is correct for given operation
        argsRegexes = opcodeArgList[opcode]
        for regex in argsRegexes:
            if re.match(regex, args):
                argsSyntaxRight = True
                break
        
        if not argsSyntaxRight:
            print("Error! Incorrect argument syntax at line: '" + line + "'")
            sys.exit()
        
        #find immediate
        immedRegex = re.findall(r'#-?[0-9]+', args)
        if len(immedRegex) > 0:
            immed = immedRegex[0]
            immed = int(immed[1:])
            if immed >= -512 and immed <= 511:
                imload = 1   
            else:
                print("Error! Immediate out of range at line: '" + line + "'")
                sys.exit()     
        
        #find Rd, Rs, Rt
        registers = re.findall(r'r[0-7]', args)
        if len(registers) == 3:
            Rd = registers[0]
            Rd = Rd[1:]
            Rs = registers[1]
            Rs = Rs[1:]
            Rt = registers[2]
            Rt = Rt[1:]
        elif len(registers) == 2 and imload == 0:
            Rs = registers[0]
            Rs = Rs[1:]
            Rt = registers[1]
            Rt = Rt[1:]
        elif len(registers) == 2 and imload == 1:
            Rd = registers[0]
            Rd = Rd[1:]
            Rs = registers[1]
            Rs = Rs[1:]
        elif len(registers) == 1 and opcode in [opcodeArr["j"], opcodeArr["b"], opcodeArr["bl"]]:
            Rs = registers[0]
            Rs = Rs[1:]
        elif len(registers) == 1:
            Rd = registers[0]
            Rd = Rd[1:]
       
        #find label
        if re.match(r'^\s*\w+\s*$', args) and not re.match(r'^\s*r[0-7]\s*$', args):
            labelName = args.strip()
            if labelName not in labelsArr:
                print("Error! Unknown label at line: '" + line + "'")
                sys.exit()
            else:
                label = labelsArr[labelName]
                imload = 1
                labelIsImmed = True
        
        #Print out everything for testing
        print(str(lineNum) + ': ' + 'opcode: ' + str(opcode) + ', cond: ' + str(condition) + ', setFlags: ' + str(setFlags))
        print('Rd: ' + str(Rd) + ', Rs: ' + str(Rs) + ', Rt: ' + str(Rt) + ', immed: ' + str(immed) + ', label: ' + str(label))

        #Convert everything to binary strings and combine to form 32 bit instruction
        opcodeBin = '{0:07b}'.format(opcode)
        imloadBin = '{0:01b}'.format(imload)
        setFlagsBin = '{0:01b}'.format(setFlags)
        condBin = '{0:04b}'.format(condsArr[condition])
        RtBin = '{0:03b}'.format(int(Rt))
        RsBin = '{0:03b}'.format(int(Rs))
        RdBin = '{0:03b}'.format(int(Rd))
        if labelIsImmed:
            if label < 0:
                label *= -1
                immedBin = bin(label)[2:]
                immedBin = immedBin.rjust(10,'1')
            else:
                immedBin = '{0:010b}'.format(label)
        else:
            if immed < 0:
                immed *= -1
                immedBin = bin(immed)[2:]
                immedBin = immedBin.rjust(10,'1')
            else:
                immedBin = '{0:010b}'.format(immed)
        
        instrBin = opcodeBin + imloadBin + setFlagsBin + condBin + RtBin + RsBin + RdBin + immedBin

        #convert instruction to hex and add to instruction array
        instrHex = hex(int(instrBin, 2))
        instrHex = instrHex[2:]
        instructionsArr.append(instrHex)
        print(instrHex)

#write to output file
outfile = sys.argv[1]
outfile = re.sub(r'[.]{1}\w+$', ".ram", outfile)
with open(outfile, 'w') as f:
    f.write("v2.0 raw\n")
    for i in range(0, len(instructionsArr)):
        f.write(instructionsArr[i] + " ")
        if i % 8 == 7:
            f.write("\n")
    f.write("\n")
f.close()
sys.exit(0)