N=7
A=1
B=1
TMP=0
for i=3 to N 
    TMP=B
    B=A+B
    A=TMP
endfor
? B
