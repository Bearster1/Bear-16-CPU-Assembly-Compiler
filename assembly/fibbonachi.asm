LDR r0 i0 ; Load zeroth term (Reffered as A)
LDR r1 i1 ; Load first term (Reffered as B)
LDR r2 i24 ; Load term you are finding (Reffered as Counter)

; Initiate loop
LDR r3 pc ; Load loop location

; Calculate terms
LDR racc r0 ; Set the acc to A
ADD r1 ; Add B to the Acc
LDR r0 r1 ; Set A to B
LDR r1 racc ; Set B to the Acc

; Decrement counter
LDR racc r2 ; Set the acc to the counter
SUB i1 ; Subtract 1 from the acc
LDR r2 racc ; Set the counter to the acc

; Loop
JGT r2 r3

; Finished