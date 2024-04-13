                             @ p1201.s
          .global main       @ scanf and printf assumed global 
          .text
main:
          push {lr}          @ save lr by pushing onto stack
          
          ldr r0, =.z0       @ get address of string
          ldr r1, =x         @ get address of x
          bl  scanf          @ call scanf

          ldr r0, =.z0       @ get address of string
          ldr r1, =y         @ get address of y
          bl  scanf          @ call scanf

          ldr r0, =.z0       @ get address of string
          ldr r1, =z         @ get address of z
          bl  scanf          @ call scanf

          ldr r1, =x
          ldr r1, [r1]
          ldr r2, =y
          ldr r2, [r2]
          add r1, r1, r2
          ldr r2, =z
          ldr r2, [r2]
          add r1, r1, r2

          ldr r0, =.z1       @ get address of string
          bl  printf         @ call printf
 
          pop {pc}           @ pop saved lr into pc
          .data              @ start of read/write segment
.z0:      .asciz "%d"        @ null-terminated ASCII string
.z1:      .asciz "%d\n"      @ null-terminated ASCII string
x:        .word 0
y:        .word 0
z:        .word 0
