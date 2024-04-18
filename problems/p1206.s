                             @ p1206.s
          .global main       @ scanf and printf assumed global 
          .text              @ start of read-only segment
main:
          push {lr}          @ save lr by pushing onto stack
          
          ldr r0, =.z0       @ get address of string
          ldr r1, =x         @ get address of x
          bl  scanf          @ call scanf

          ldr r10, =x
          ldr r10, [r10]
          mov r11, #1
          mov r1, #0
loopstart:
          add r1, r10
          subs r10, r10, r11
          bne loopstart
 
          ldr r0, =.z1       @ get address of string
          bl  printf         @ call printf

          pop {pc}           @ pop saved lr into pc
          .data              @ start of read/write segment
.z0:      .asciz "%d"        @ null-terminated ASCII string
.z1:      .asciz "sum=%d\n"  @ null-terminated ASCII string
x:        .word 0
