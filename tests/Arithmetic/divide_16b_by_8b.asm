NAME Arithmetic
TITLE divide_16b_by_8b

assume cs:code,ds:data

data segment
    var1 dw 6827H
    var2 db 0feH
    quo db ?
    rem db ?
data ends          

code segment
    start: mov ax,data
           mov ds,ax
           
           mov ax,var1
           mov bl,var2
           
           div bl          
           
           mov quo,al
           mov rem,ah
           mov ah,4ch
           int 21h
code ends
end start