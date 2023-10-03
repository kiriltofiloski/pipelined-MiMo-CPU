import sys
import re

#Control signals
ctrlSignals = {
    'instrUnload' : 0,      #IF
    'pcsel' : 0,
    'loadlink' : 0,
    'strlink' : 0,

    'op2sel' : 0,     #EX
    'aluop' : 0,
    'negOp2' : 0,
    'rvrsOps' : 0,

    'datasel' : 0,     #MA
    'datawrite' : 0,
    'addrsel' : 0,

    'regsrc' : 0,      #WB
    'dwrite' : 0,
    'swrite' : 0,
    'twrite' : 0,
}

#Valid control signal values
ctrlSigPairs = {
    'instrUnload=0' : ['instrUnload', 0],
    'instrUnload=1' : ['instrUnload', 1],

    'pcsel=pc' : ['pcsel', 0],
    'pcsel=immed' : ['pcsel', 1],
    'pcsel=pcimmed' : ['pcsel', 2],

    'loadlink=0' : ['loadlink', 0],
    'loadlink=1' : ['loadlink', 1],

    'strlink=0' : ['strlink', 0],
    'strlink=1' : ['strlink', 1],

    #'op2sel=treg' : ['op2sel', 0],
    #'op2sel=immed' : ['op2sel', 1],
    'op2sel=op2' : ['op2sel', 0],
    'op2sel=const0' : ['op2sel', 2],
    'op2sel=const1' : ['op2sel', 3],

    'negOp2=0' : ['negOp2', 0],
    'negOp2=1' : ['negOp2', 1],

    'rvrsOps=0' : ['rvrsOps', 0],
    'rvrsOps=1' : ['rvrsOps', 1],

    'aluop=add' : ['aluop', 0],
    'aluop=sub' : ['aluop', 1],
    'aluop=mul' : ['aluop', 2],
    'aluop=div' : ['aluop', 3],
    'aluop=rem' : ['aluop', 4],
    'aluop=and' : ['aluop', 5],
    'aluop=or' : ['aluop', 6],
    'aluop=xor' : ['aluop', 7],
    'aluop=nand' : ['aluop', 8],
    'aluop=nor' : ['aluop', 9],
    'aluop=not' : ['aluop', 10],
    'aluop=lsl' : ['aluop', 11],
    'aluop=lsr' : ['aluop', 12],
    'aluop=asr' : ['aluop', 13],
    'aluop=rol' : ['aluop', 14],
    'aluop=ror' : ['aluop', 15],

    'datasel=sreg' : ['datasel', 0],
    'datasel=treg' : ['datasel', 1],
    'datasel=aluout' : ['datasel', 2],

    'datawrite=0' : ['datawrite', 0],
    'datawrite=1' : ['datawrite', 1],

    'addrsel=immed' : ['addrsel', 0],
    'addrsel=aluout' : ['addrsel', 1],
    'addrsel=sreg' : ['addrsel', 2],

    #'regsrc=sreg' : ['regsrc', 0],
    #'regsrc=immed' : ['regsrc', 1],
    'regsrc=op2' : ['regsrc', 0],
    'regsrc=operand' : ['regsrc', 2],
    'regsrc=aluout' : ['regsrc', 3],

    'dwrite=0' : ['dwrite', 0],
    'dwrite=1' : ['dwrite', 1],

    'swrite=0' : ['swrite', 0],
    'swrite=1' : ['swrite', 1],

    'twrite=0' : ['twrite', 0],
    'twrite=1' : ['twrite', 1],
}

currentOpcode = None
usedOpcodes = []
instructionsArr = []
#fill with zeros at beginning so they are addressed properly according to the opcode
for i in range(256):
    instructionsArr.append(0)

def generateInstr():
    global ctrlSignals
    global currentOpcode

    #Convert to binary strings
    instrUnloadBin = '{0:01b}'.format(ctrlSignals['instrUnload'])
    pcselBin = '{0:02b}'.format(ctrlSignals['pcsel'])
    loadlinkBin = '{0:01b}'.format(ctrlSignals['loadlink'])
    strlinkBin = '{0:01b}'.format(ctrlSignals['strlink'])
    op2selBin = '{0:02b}'.format(ctrlSignals['op2sel'])
    aluopBin = '{0:04b}'.format(ctrlSignals['aluop'])
    negOp2Bin = '{0:01b}'.format(ctrlSignals['negOp2'])
    rvrsOpsBin = '{0:01b}'.format(ctrlSignals['rvrsOps'])
    dataselBin = '{0:02b}'.format(ctrlSignals['datasel'])
    datawritebin = '{0:01b}'.format(ctrlSignals['datawrite'])
    addrselBin = '{0:02b}'.format(ctrlSignals['addrsel'])
    regsrcBin = '{0:02b}'.format(ctrlSignals['regsrc'])
    dwriteBin = '{0:01b}'.format(ctrlSignals['dwrite'])
    swriteBin = '{0:01b}'.format(ctrlSignals['swrite'])
    twriteBin = '{0:01b}'.format(ctrlSignals['twrite'])
    filler = '{0:09b}'.format(0)

    #Form binary instruction
    instrBin = filler + twriteBin + swriteBin + dwriteBin + regsrcBin + addrselBin + datawritebin + dataselBin + rvrsOpsBin + negOp2Bin + aluopBin + op2selBin + strlinkBin + loadlinkBin + pcselBin + instrUnloadBin

    #Convert to hex and add to array
    instrHex = hex(int(instrBin, 2))
    instrHex = instrHex[2:]
    if currentOpcode == 'default':
        instructionsArr[0] = instrHex
    else:
        instructionsArr[int(currentOpcode) + 1] = instrHex

    #Print for testing
    print("instruction: " + instrHex)
    print("current opcode: " + currentOpcode)
    print("#################")
    print("instrUnload: " + str(ctrlSignals['instrUnload']))
    print("pcsel: " + str(ctrlSignals['pcsel']))
    print("loadlink: " + str(ctrlSignals['loadlink']))
    print("strlink: " + str(ctrlSignals['strlink']))
    print("op2sel: " + str(ctrlSignals['op2sel']))
    print("aluop: " + str(ctrlSignals['aluop']))
    print("negOp2: " + str(ctrlSignals['negOp2']))
    print("rvrsOps: " + str(ctrlSignals['rvrsOps']))
    print("datasel: " + str(ctrlSignals['datasel']))
    print("datawrite: " + str(ctrlSignals['datawrite']))
    print("addrsel: " + str(ctrlSignals['addrsel']))
    print("regsrc: " + str(ctrlSignals['regsrc']))
    print("dwrite: " + str(ctrlSignals['dwrite']))
    print("swrite: " + str(ctrlSignals['swrite']))
    print("twrite: " + str(ctrlSignals['twrite']))
    print('\n\n')

    #Clear control signals
    for key in ctrlSignals:
        ctrlSignals[key] = 0


with open(sys.argv[1]) as f:
    #First we remove multiline comments
    fClean = re.sub(r'/\*[\s\S]*?\*/', '', f.read())
    for index, line in enumerate(fClean.splitlines()):
        line = line.strip()

        if "@" in line:
            line = line.split("@", 1)[0]    #if line contains comment, delete everythig after the comment
        
        #if default address, for when conditions aren't met
        if re.match(r'^\s*default:', line):
            #Save current control signals to new instruction if not first instruction(if currentOpcode!=None)
            if currentOpcode is not None:
                generateInstr() 

            opcode = line.split(':', 1)[0]
            signals = line.split(':', 1)[1]
            currentOpcode = opcode

            #Change control signals
            signals = signals.strip()
            signalsArr = re.split(r'\s+', signals)

            for signal in signalsArr:
                if signal in ctrlSigPairs:
                    ctrlSignals[ctrlSigPairs[signal][0]] = ctrlSigPairs[signal][1]
        #if new opcode in line
        elif re.match(r'^\s*\d+:', line):
            #Save current control signals to new instruction if not first instruction(if currentOpcode!=None)
            if currentOpcode is not None:
                generateInstr() 

            opcode = line.split(':', 1)[0]
            signals = line.split(':', 1)[1]

            if int(opcode) > 31:
                print("Error! Unknown opearation code at line: '" + line + "'")
                sys.exit()
            
            #Check if opcode is duplicate
            if opcode in usedOpcodes:
                print("Error! Duplicate opearation code at line: '" + line + "'")
                sys.exit()
            else:
                usedOpcodes.append(opcode)
                currentOpcode = opcode
            
            #Change control signals
            signals = signals.strip()
            signalsArr = re.split(r'\s+', signals)

            for signal in signalsArr:
                if signal in ctrlSigPairs:
                    ctrlSignals[ctrlSigPairs[signal][0]] = ctrlSigPairs[signal][1]
            #if last line generate instruction
            if index == len(fClean.splitlines()) - 1:
                generateInstr()
        else:
            #Change control signals
            signals = line.strip()
            signalsArr = re.split(r'\s+', signals)

            for signal in signalsArr:
                if signal in ctrlSigPairs:
                    ctrlSignals[ctrlSigPairs[signal][0]] = ctrlSigPairs[signal][1]
            #if last line generate instruction
            if index == len(fClean.splitlines()) - 1:
                generateInstr()
    
    #write to output file
    outfile = sys.argv[1]
    outfile = re.sub(r'[.]{1}\w+$', ".rom", outfile)
    with open(outfile, 'w') as f:
        f.write("v2.0 raw\n")
        for i in range(0, len(instructionsArr)):
            f.write(str(instructionsArr[i]) + " ")
            if i % 8 == 7:
                f.write("\n")
        f.write("\n")
    f.close()
    sys.exit(0)