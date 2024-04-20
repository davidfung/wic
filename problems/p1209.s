                             @ p1209.s
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
loopstart:
          mov r7, #4         @ syscall 4 
          mov r0, #1         @ output device = stdout
          ldr r1, =.z1       @ address of string
          mov r2, #6         @ characters to display
          svc 0
          subs r10, r10, r11
          bne loopstart
 
          pop {pc}           @ pop saved lr into pc
          .data              @ start of read/write segment
.z0:      .asciz "%d"        @ null-terminated ASCII string
.z1:      .asciz "David\n"   @ null-terminated ASCII string
x:        .word 0
