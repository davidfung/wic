                                @ p1101.s
          .text                 @ start of read-only segment
          .global _start
_start:
          ldr r0, x             @ load r0 from x
          ldr r1, y             @ load r1 from y
          add r0, r0, r1
          ldr r1, z             @ load r1 from z
          add r0, r0, r1
          mov r7, #1            @ mov 1 into r7
          svc 0                 @ supervisor call to terminate program

x:        .word 1               @ the variable x
y:        .word 2               @ the variable y
z:        .word 3               @ the variable z
