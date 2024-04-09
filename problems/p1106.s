                                @ p1101.s
          .text                 @ start of read-only segment
          .global _start
_start:
          ldr r0, x             @ load r0 from x
          mov r7, #1            @ mov 1 into r7
          svc 0                 @ supervisor call to terminate program

@         .space 36000
          .space 39999
@         .space 39999
x:        .word 6502            @ the variable x
