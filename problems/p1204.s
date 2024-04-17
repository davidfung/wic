                            @ p1204.s
          .global main      @ printf assumed global
          .text             @ start of read-only segment
main:     push {lr}         @ save lr by pushing onto stack

          ldr r10, =n       @ get address of n
          ldr r10, [r10]    @ get value of n
          mov r11, #1
loopstart:
          ldr r0, =.fmt
          bl printf 
          subs r10, r10, r11 @ sub r11 from r10, set cond code
          bne loopstart

          pop {pc}          @ pop saved lr into pc
          .data             @ start of read/write segment
.fmt:     .asciz "David Fung\n" @ null-terminated ASCII string
n:        .word 10
