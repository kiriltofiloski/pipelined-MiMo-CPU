# New Changes



### Changed circuit layout and appearance to be more similar to OR class sketch

<figure><img src=".gitbook/assets/image (15).png" alt=""><figcaption><p>OR class sketch</p></figcaption></figure>

All of the stages are and their parts are now displayed on the main circuit and I have added "transition blocks" (like IF->ID, ID->EX), that store the data goign in and leaving a stage.



### Added Link Register

I added the Link register as a special register, outside of the Register Bank.&#x20;

It does not make sense to use one of the normal registers because the Write Back stage for normal registers happens at the end, and since branch with link is a branch instruction, it needs to happen immediately after decoding like the other branch/jump instructions.



<figure><img src=".gitbook/assets/temp.png" alt=""><figcaption><p>Link register</p></figcaption></figure>

I added 2 new microinstructions, **loadlink** and **strlink**.

When the first signal is active it saves the current IF stage address in the link register, the second stores the current Link register value inside the **sreg** port of the IF stage, as pictured below.



<figure><img src=".gitbook/assets/temp (1).png" alt=""><figcaption><p>Link register connection to IF stage</p></figcaption></figure>

I added **rts** as the 29th instruction to the assembler. This instruction is used to return from subroutine.

