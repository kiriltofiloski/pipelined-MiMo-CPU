from msilib import datasizemask
import sys
import re
from binascii import hexlify

opcodeArr = {
    "nop" : 0,
    "mov" : 1,
    "mvn" : 2,
    "add" : 3,
    "sub" : 4,
    "rsb" : 5,
    "mul" : 6,
    "div" : 7,
    "rem" : 8,
    "and" : 9,
    "orr" : 10,
    "eor" : 11,
    "nand" : 12,
    "nor" : 13,
    "bic" : 14,
    "cmp" : 15,
    "cmn" : 16,
    "tst" : 17,
    "teq" : 18,
    "lsl" : 19,
    "lsr" : 20,
    "asr" : 21,
    "ror" : 22,
    "rol" : 23,
    "j" : 24,
    "b" : 25,
    "bl" : 26,
    "rts" : 27,
    "str" : 28,
    "ldr" : 29,
}

opcodeArgList = {
    0 : ["\s*"],
    1 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    2 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
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
    14 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    15 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    16 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    17 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    18 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    19 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    20 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    21 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    22 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    23 : ["^r[0-7],\s*r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$"],
    24 : ["^\s*#-?[0-9]+\s*$", "^\s*\w+\s*$", "^\s*r[0-7]\s*$"],
    25 : ["^\s*#-?[0-9]+\s*$", "^\s*\w+\s*$", "^\s*r[0-7]\s*$"],
    26 : ["^\s*#-?[0-9]+\s*$", "^\s*\w+\s*$", "^\s*r[0-7]\s*$"],
    27 : ["\s*"],
    28 : ["^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$"],
    29 : ["^r[0-7],\s*\[r[0-7]\]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$", "^r[0-7],\s*\[r[0-7],\s*r[0-7]\]\s*$", "^r[0-7],\s*\[r[0-7],\s*#-?[0-9]+\]\s*$"],
}

# "^r[0-7],\s*r[0-7],\s*r[0-7]\s*$" this is r1,r2,r3
# "^r[0-7],\s*r[0-7],\s*#-?[0-9]+\s*$" this is r1,r2,#5
# This just checks if immediate is number, we have to afterwards check if it's in range -512 to 511
# "^r[0-7],\s*r[0-7]\s*$", "^r[0-7],\s*#-?[0-9]+\s*$" These are r1,r2 and r1,#5
# "^\s*#-?[0-9]+\s*$" just #5
# "^\s*\w+\s*$" any label 
# "^r[0-7],\s*\[r[0-7]\]\s*$" - match expresions like ldr r1 [r2] - for ldr only
#"^r[0-7],\s*\[r[0-7],\s*r[0-7]\]\s*$" - match expressions like ldr r1, [r1, r3] - for ldr only
#"^r[0-7],\s*\[r[0-7],\s*#-?[0-9]+\]\s*$" - match expressions like ldr r1, [r1, #5] - for ldr only


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
instrLines = []
instrLinesClean = []
addressCounter = 0
markNextLine = False
label = ""

instructionsArr = []
operandData = ""

with open(sys.argv[1]) as f:
    #First we remove multiline comments
    fClean = re.sub(r'/\*[\s\S]*?\*/', '', f.read())

    #First loop that cleans comments
    for line in fClean.splitlines():
        line = line.strip()
        line = line.lower()

        if "@" in line:
            line = line.split("@", 1)[0]    #if line contains comment, delete everythig after the comment
            line = line.strip()
        if line != "":
            linesClean.append(line) 
    
    #Second loop that checks for .data section and stores it to operand RAM
    dataSection = False
    instrSection = False
    for lineNum, line in enumerate(linesClean):
        if line == '.data':             #declares start of .data section
            dataSection = True
            instrSection = False
        elif line == '.text':             #declares start of instruction section
            dataSection = False
            instrSection = True
        elif instrSection:              #add the line to the instruction lines to be processed in the next loop
            instrLines.append(line)
        elif dataSection:
            firstWord = re.split(r'\s+', line, 1)[0]

            if firstWord == '.word':        #if it is a .word directive
                words = re.split(r'\s+', line, 1)[1]
                words = re.split(r'\s*,\s*', words)
                for word in words:
                    if word[:2] == '0x':        #if it's in hex, check if valid hex numebr than append to data
                        try:
                            int(word[2:], 16)
                            operandData += word[2:].zfill(8)    #zfill is used to pad to word length, so it is aligned
                        except ValueError:
                            print("Error! Invalid number given at line: '" + line + "'")
                            sys.exit()
                    elif not word.isnumeric():     #if not hex check if numeric
                        print("Error! Invalid number given at line: '" + line + "'")
                        sys.exit()
                    else:                           #if numeric and not in hex, convert to hex then append
                        word = str(hex(int(word)))
                        word = word[2:].zfill(8)
                        operandData += str(word)
            elif firstWord == '.ascii':             #if it is an ascii string directive
                strngs = re.split(r'\s+', line, 1)[1]
                strngs = re.split(r'\s*,\s*', strngs)
                for strng in strngs:
                    if strng[:1] != "\"" and strng[-1:] != "\"": #if it doesn't start and end with ""
                        print("Error! Invalid string given at line: '" + line + "'")
                        sys.exit()
                    else:
                        strng = strng.replace('"', '')          #remove unnecesary ""
                        strng = hexlify(strng.encode("ascii"))  #convert to hex
                        strng = str(strng)                  
                        strng = strng[2:-1]                     #remove unnecesary b' and ' at start and end of bute stream
                        operandData += strng
            elif firstWord == '.asciiz':            #same as ascii but we add terminating null character to end of each string
                strngs = re.split(r'\s+', line, 1)[1]
                strngs = re.split(r'\s*,\s*', strngs)
                for strng in strngs:
                    if strng[:1] != "\"" and strng[-1:] != "\"": #if it doesn't start and end with ""
                        print("Error! Invalid string given at line: '" + line + "'")
                        sys.exit()
                    else:
                        strng = strng.replace('"', '')          #remove unnecesary ""
                        strng += '\0'                           #add terminating null character
                        strng = hexlify(strng.encode("ascii"))  #convert to hex
                        strng = str(strng)
                        strng = strng[2:-1]                     #remove unnecesary b' and ' at start and end of bute stream
                        operandData += strng
            elif firstWord == '.space':
                space = re.split(r'\s+', line, 1)[1]
                if not space.isnumeric():
                    print("Error! Invalid number given at line: '" + line + "'")
                    sys.exit()
                else:
                    spacesToAdd = int(space) * '00'   #add amount of empty butes specified by number after .space
                    operandData += spacesToAdd


    #Third loop that looks for labels
    for lineNum, line in enumerate(instrLines):
        if ":" in line:
            label = line.split(":", 1)[0]
            afterLabel = line.split(":", 1)[1]

            if afterLabel == "" and not markNextLine:   #if line is a label line only like ' lableName:   ' 
                markNextLine = True                     #mark the next line after to be marked
            elif afterLabel == "" and markNextLine:
                print("Error! Can't have label that points to other label at line: '" + line + "'") #in our first implementation we will not make nested lables possible, maybe later
                sys.exit()
            else:
                labelsArr[label] = addressCounter   #if label and instruction are on same line like ' lableName: add r1,r2,r3'
                addressCounter += 1 
                instrLinesClean.append(afterLabel.strip())  #add the current address to the lablesArr and increase the counter
        elif markNextLine:
            labelsArr[label] = addressCounter       #next line after lable that is to be marked
            addressCounter += 1
            instrLinesClean.append(line)  
            markNextLine = False
        elif line != "":                            #only increase addresscounter on non-blank lines
            instrLinesClean.append(line)            #add the instruction to instrLinesClean
            addressCounter += 1                     #since we removed comments and data, all lines should either be instructions or labels
    
    #Fourth loop that decodes instructions
    for lineNum, line in enumerate(instrLinesClean):
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
        
        #for ldr decode into specific ldr instruction
        if opcode == opcodeArr["ldr"]:                      #find better way to do this maybe?
            if re.match("^r[0-7],\s*\[r[0-7]\]\s*$", args):
                opcode = 30
            elif re.match("^r[0-7],\s*\[r[0-7],\s*r[0-7]\]\s*$", args) or re.match("^r[0-7],\s*\[r[0-7],\s*#-?[0-9]+\]\s*$", args):
                opcode = 31

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
        elif len(registers) == 2 and (opcode == 30 or opcode == 28):
            Rd = registers[0]
            Rd = Rd[1:]
            Rs = registers[1]
            Rs = Rs[1:]
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
        elif len(registers) == 1 and opcode in [opcodeArr["mov"], opcodeArr["mvn"]]:
            Rd = registers[0]
            Rd = Rd[1:]
        elif len(registers) == 1:
            Rs = registers[0]
            Rs = Rs[1:]
       
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
                immedBin = bin(label % (1<<10))
                immedBin = immedBin[2:]
            else:
                immedBin = '{0:010b}'.format(label)
        else:
            if immed < 0:
                immedBin = bin(immed % (1<<10))
                immedBin = immedBin[2:]
            else:
                immedBin = '{0:010b}'.format(immed)
        
        instrBin = opcodeBin + imloadBin + setFlagsBin + condBin + RtBin + RsBin + RdBin + immedBin

        #convert instruction to hex and add to instruction array
        instrHex = hex(int(instrBin, 2))
        instrHex = instrHex[2:]
        instructionsArr.append(instrHex)
        print(instrHex)

#write to instruction output file
outfile = sys.argv[1]
outfile = re.sub(r'[.]{1}\w+$', ".iram", outfile)
with open(outfile, 'w') as f:
    f.write("v2.0 raw\n")
    for i in range(0, len(instructionsArr)):
        f.write(instructionsArr[i] + " ")
        if i % 8 == 7:
            f.write("\n")
    f.write("\n")
f.close()

if operandData:
    #write to operand output file
    outfile = sys.argv[1]
    outfile = re.sub(r'[.]{1}\w+$', ".oram", outfile)
    with open(outfile, 'w') as f:
        f.write("v2.0 raw\n")
        formatedOperandData = ""
        for i in range(0, len(operandData), 8):
            formatedOperandData += operandData[i:i+8] + " "
        f.write(formatedOperandData.strip())
    f.close()
sys.exit(0)