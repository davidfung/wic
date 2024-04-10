                                @ p1106.s
          .text                 @ start of read-only segment
          .global _start
y:        .word 43            @ the variable x
          .space 4084
_start:
          ldr r0, y             @ load r0 from x
          mov r7, #1            @ mov 1 into r7
          svc 0                 @ supervisor call to terminate program

@         .space 36000
          .space 4092
@         .space 39999
x:        .word 42            @ the variable x
