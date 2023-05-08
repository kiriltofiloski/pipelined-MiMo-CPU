# Overview of Stages

## Instruction Fetch

<figure><img src=".gitbook/assets/image (5).png" alt=""><figcaption><p>IF Stage along with Instruction RAM</p></figcaption></figure>

#### Inputs:

* immed
* Rs
* pcsel
* instrUnload

#### Outputs:

* instruction

<figure><img src=".gitbook/assets/image (2).png" alt=""><figcaption><p>Inside of IF_Stage circuit</p></figcaption></figure>

The Instruction Fetch Stage has the task of fetching a new instruction each cycle.

The **immed** and **Rs** values are directly taken from the most recently processed ID Stage immediate and register values.

The **pcsel** signal dictates whether the PC should increment, jump to immediate address(**immed**), jump to PC + immediate or jump to register address(**Rs**).

<figure><img src=".gitbook/assets/image (10).png" alt=""><figcaption><p>Inside of PC</p></figcaption></figure>

After processing the correct address, the Instruction RAM gives us the corresponding instruction.

<figure><img src=".gitbook/assets/image (8).png" alt=""><figcaption><p>instrUnload MUX</p></figcaption></figure>

The **instrUnload** signal decides whether the instruction passes through to the ID stage. It's purpose is to stop the instruction that is right after a jump/branch command from passing through.

## Instruction Decode

<figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

#### Inputs

* instruction
* Flags (C, Z, V, N)

#### Outputs

* immed
* imload
* dregs
* tregs
* sregs
* cond\_met
* set\_flags
* opcode

<figure><img src=".gitbook/assets/image (4).png" alt=""><figcaption><p>Instruction decoding inside ID_Stage</p></figcaption></figure>

The purpose of this stage is to decode the given instruction, decide if it should be executed, and access the needed register values.

The instruction enters the instruction register, from which we receive:

* &#x20;the immediate **immed** that is only loaded if **imload** bit is also active. This immediate is then passed to the next stage.
* **dregs, sregs** and **tregs** which indicate which registers to access
* the **opcode** that will go to the Control ROM
* the **set\_flags** bit that indicates whether the instruction should influence the flags or not.
* the **condition** bits that indiciate the condition for which thsi instruction should execute

<figure><img src=".gitbook/assets/image.png" alt=""><figcaption><p>Conditional checking inside ID Stage</p></figcaption></figure>

The **condition** bits enter the **check\_condition** circuit along with the condition flags (N, Z, C, V). The output is the **condition\_met** signal which indicates whether this instruction passes the given condition.

This  **cond\_met** signal is then passed to the Control ROM along with the **opcode**.

The **set\_flags** signal from our Instruction Register passes through an AND gate with the **condition\_met** signal and is then passed to the next stage (Execute).

The Register Bank needed to be changed to allow 2 selections at the same time, as both the ID and the WB stage need access to it.

**dsel, ssel, tsel** have been changed to **dselin, sselin, tselin** for the WB stage and **dselout, sselout, tselout** for the ID stage.

<figure><img src=".gitbook/assets/image (11).png" alt=""><figcaption><p>Register Bank change</p></figcaption></figure>

the **dregs, sregs** and **tregs** signals enter the **dselout, sselout, tselout** signals of the Register Bank and from the **dreg, sreg** and **treg** outputs the values for **Rd**, **Rs** and **Rt** are transferred to the next stage.

<figure><img src=".gitbook/assets/image (6).png" alt=""><figcaption><p>ID_Stage and Register Bank connections</p></figcaption></figure>

The same **dregs, sregs** and **tregs** signals enter into their respective 3 stage shift registers before entering the **dselin, sselin** and **tselin** inputs of the Register Bank. This is done because these same values will be needed in the WB stage, 3 stages from now.

## Instruction Execute

<figure><img src=".gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

#### Inputs:

* Rd
* Rs
* Rt
* Immediate (**immed**)
* flags\_set
* op2sel
* aluop
* negOp2
* rvrsOps

#### Outputs:

* aluout
* Flags (C, Z, V, N)
* Rd1
* Rs1
* Rt1
* immed1

The purpose of the Execute stage is to transform the data using an ALU operation if needed and change the condition signals (C, Z, V, N) if instructed to.

<figure><img src=".gitbook/assets/image (12).png" alt=""><figcaption><p>Inside operation of Execute Stage</p></figcaption></figure>

The Execute stage takes the register values and immediate fetched in the ID stage as it's operands for data transformation.

**Rs** is always taken as the first operand. The **op2sel** signal dictates which values to take as the second operand: **Rt**, the immediate, constant 0 or constant 1. The **negOp2** signal dictates whether we want the second operand to pass through a NOT gate. The **rvrsOps** signal dictates whether we should swap the first and second operand in the ALU.

The **aluop** signal dictates which ALU operation we want to perform. Each of the condition signals are only changed if the **flags\_set** signal is active.

The resulting ALU result is passed through to the next stage along with the register and immediate values for this instruction.

## Memory Access

<figure><img src=".gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>
