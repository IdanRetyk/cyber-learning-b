echo running $1...
echo ========================

gcc -o $1 $1.c
./$1.out

echo ========================
