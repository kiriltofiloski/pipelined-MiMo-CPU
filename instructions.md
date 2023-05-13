# Instructions

I tried making the instruction set and CPU in general function much more like a classic ARM CPU, while also combining it with some of the features of the preivous MiMo model that made it simpler for learning purposes.

### Added optional condition bits to every instruction

In the previous version of MiMo, each conditional operation would have to be made as a separate instruction in the micro-assembler.

In this version each instruction has 4 bits reserved for a condition code (_e.g. mov**eq** r1, #5 - Equal condition)._

The condition is checked in the **ID** stage in the **check\_condition** circuit. All conditions are based on the ARM ISA conditional codes. They go as follows:

| Mnemonic | Description                       | Flags state       |
| -------- | --------------------------------- | ----------------- |
| EQ       | Equal                             | Z set             |
| NE       | Not equal                         | Z clear           |
| CS       | Carry set/unsigned higher or same | C set             |
| CC       | Carry clear/unsigned lower        | C clear           |
| MI       | Minus/Negative                    | N set             |
| PL       | Plus/positive or zero             | N clear           |
| VS       | Overflow                          | V set             |
| VC       | No overflow                       | V clear           |
| HI       | Unsigned higher                   | C set and Z clear |
| LS       | Unsigned lower or same            | C clear or Z set  |
| GE       | Signed greater than or equal      | N = V             |
| LT       | Signed less than                  | N != V            |
| GT       | Signed greater than               | Z clear and N = V |
| LE       | Signed less than or equal         | Z set and N != V  |
| AL       | Always/unconditional              | Irrelevant        |

### Added 'Set Flags' ( S ) bit

In the previous version of MiMo, all instructions would change the ALU flags, now each instruction has an extra bit reserved for the 'set flag' bit, and only changes the state of the flags if it is set.

This was another change made to bring MiMo closer to a traditional ARM processor.

Instruction example: add**s** r1, r2, r3

### Added immediate as part of instruction

In the previous version of MiMo, all immediates would be contained in a separate instruction following the original instruction.

In a pipelined CPU, this would slow things down tremendously. Since we are also increasing the instruction size to 32 bits, I decided to change it to work as a classic ARM CPU would, where the immediate value would occupy a part of the original instruction, 10 bits in our case.

The downside to this approach is of course that we are more limited in the size of our immediate values

In a classic ARM Instruction set, there are also no separate instructions for immediate operands.

&#x20;I decided to implement this in MiMo by having the **imload** signal, which was previously a control signal provided by the micro-assembler, be part of the instruction assembler instead.&#x20;

We reserve 1 bit in the instruction marked as the **imload** bit. When this is active, the CPU knows that the instruction uses the immediate provided within it. This way we do not need separate instructions for using immediate values.

### Instruction breakdown:

* Operation Code - 7 bits
* Condition Code - 4 bits
* imload - 1 bit
* Set flags - 1 bit
* Rd - 3 bits
* Rs - 3 bits
* Rt - 3 bits
* Immediate value - 10 bits

#### Some possible changes:

* reduce operation code size as we do not need so many instructions?
* Remove Rd/Rs/Rt bits in instructions that only need 1 or 2 registers?
* In both cases above give extra instruction space to the immediate value

### Instruction Syntax

Changed instruction syntax to a simplified ARM Assembly syntax.

| Symbol  | Function                  | Example                                 |
| ------- | ------------------------- | --------------------------------------- |
| /\* \*/ | Multiline comment         | <p>/*not read by</p><p> assembler*/</p> |
| @       | Single-line comment       | @also not read                          |
| #       | Indicates immediate value | mov r1, #1                              |

Combinations in the form of **\[r1, r2]** have NOT been added.

Examples of current proper syntax can be seen in the **Assembler/tests** folder.

### Instruction Set

For the instruction set I implemented most of the standard ARM instructions along with some additions from the previous MiMo model.

| Instruction Code | Arguments            | Function                                                                 |
| ---------------- | -------------------- | ------------------------------------------------------------------------ |
| mov              | Rd, Rs/Immediate     | Rd <- Rs/Immediate                                                       |
| mvn              | Rd, Rs/Immediate     | <p>Rd &#x3C;- </p><p>NOT Rs/Immediate</p>                                |
| add              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs + Rt/Immediate</p>                               |
| sub              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs - Rt/Immediate</p>                               |
| rsb              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rt/Immediate - Rs</p>                               |
| mul              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs * Rt/Immediate</p>                               |
| div              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs / Rt/Immediate</p>                               |
| rem              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs % Rt/Immediate</p>                               |
| and              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs AND Rt/Immediate</p>                             |
| orr              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs OR Rt/Immediate</p>                              |
| eor              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs XOR Rt/Immediate</p>                             |
| nand             | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs NAND Rt/Immediate</p>                            |
| nor              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs NOR Rt/Immediate</p>                             |
| bic              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs AND NOT(Rt/Immediate)</p>                        |
| cmp              | Rs, Rt/Immediate     | <p>Rs - Rt<br>Set flags</p>                                              |
| cmn              | Rs, Rt/Immediate     | <p>Rs + Rt<br>Set flags</p>                                              |
| tst              | Rs, Rt/Immediate     | <p>Rs XOR Rt<br>Set flags</p>                                            |
| teq              | Rs, Rt/Immediate     | <p>Rs AND Rt<br>Set flags</p>                                            |
| lsl              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs &#x3C;&#x3C; Rt/Immediate</p>                    |
| lsr              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs >> Rt/Immediate</p>                              |
| asr              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs >> Rt/Immediate,<br>Filled bits are sign bit</p> |
| ror              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs ROLL RIGHT Rt/Immediate</p>                      |
| rol              | Rd, Rs, Rt/Immediate | <p>Rd &#x3C;- </p><p>Rs ROLL LEFT Rt/Immediate</p>                       |
| j                | Immediate/Label      | <p>PC &#x3C;-<br>Immediate/Label</p>                                     |
| b                | Immediate/Label      | <p>PC &#x3C;- PC +<br>Immediate/Label</p>                                |
| bl               | Label?               | Jump to subroutine                                                       |
| ldr              | Rd, Immediate        | Rd <- M\[Immediate]                                                      |
| str              | Rd, Immediate        | M\[Immediate] <- Rd                                                      |
| nop              | None                 | <p>No operation<br>(Used to skip cycle and avoid pipeline hazards)</p>   |

#### Some things I'm not sure about

* **bl** is the only instruction not implemented yet. I'm not sure how is best to do subroutines in this version, would like input on that.
* Not sure if **ldr** and **str** commands should also accept register arguments? (e.g. _ldr r1, r2_ -> Rd <- M\[Value in r2])
