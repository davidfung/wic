                                @ p1102.s
          .text                 @ start of read-only segment
          .global _start
                                @             
f:        add r0, r0, #1        @ add 1 to r0 
          push {lr}
          bl  g
          pop {lr}
          mov pc, lr            @ return to caller

g:        add r0, r0, #2        @ add 2 to r0
          mov pc, lr            @ return to caller

_start:   mov r0, #1            & mov 1 into r0
          bl  f                 @ call f            
          mov r7, #1            @ mov 1 into r7     
          svc 0                 @ terminate program 
