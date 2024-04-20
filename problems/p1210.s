                             @ p1210.s
          .global main       @ scanf and printf assumed global 
          .text              @ start of read-only segment
main:
          push {lr}          @ save lr by pushing onto stack
          
          mov r7, #3         @ syscall 3
          mov r0, #0         @ stdin
          ldr r1, =.z1       @ input buffer
          mov r2, #5         @ chars to read, including trailing \n
          svc 0

          ldr r10, =x
          ldr r10, [r10]
          mov r11, #1
loopstart:
          mov r7, #4         @ syscall 4 
          mov r0, #1         @ output device = stdout
          ldr r1, =.z1       @ address of string
          mov r2, #5         @ characters to display
          svc 0
          subs r10, r10, r11
          bne loopstart
 
          pop {pc}           @ pop saved lr into pc
          .data              @ start of read/write segment
.z0:      .asciz "%5s"       @ null-terminated ASCII string
.z1:      .asciz "12345"     @ null-terminated ASCII string
x:        .word 10
