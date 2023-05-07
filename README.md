# CPU Overview

I have created the first version of the pipelined CPU based on the original MiMo CPU model.

Developed in Logisim Evolution.

General features and changes:

* 5 stage pipeline ( Instruction fetch - **IF**, Instruction Decode - **ID**, Execute - **EX**, Memory Access - **MA**, Write Back - **WB** )
* Harvard Architecture ( Separate Instruction and Operand RAM )
* 32-bit Instruction Set
* 16-bit addresses ( _Logisim RAM modules have limited address sizes so I left it at 16-bits for now )._
* Instruction set has been modified to be more similar to ARM ISA ( _More details on **Instructions** page )._
* Added Overflow flag **V**
* No pipeline hazard optimization methods added yet. **Nop** commands need to be added manually to instruction scripts to avoid hazards.
