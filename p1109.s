          .text
          .global _start
_start:
          .space 20000
          ldr r0, =a
          ldr r0, [r0]
          mov r7, #1
          svc 0
          .data
a:        .word 17
