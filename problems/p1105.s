                                @ p1103.s
          .text
          .global _start
_start:
          ldr r0, =a
          ldr r1, =b
          ldr r2, =c
          ldr r3, =d
          ldr r4, =e
          ldr r0, [r0]
          ldr r1, [r1]
          ldr r2, [r2]
          ldr r3, [r3]
          ldr r4, [r4]
          add r0, r0, r1
          add r0, r0, r2
          add r0, r0, r3
          add r0, r0, r4
          mov r7, #1            @ mov 1 into r7
          svc 0                 @ terminate program

          .data
a:        .word 22
b:        .word 5
c:        .word 2
d:        .word 7
e:        .word 1
