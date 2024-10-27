echo running $1...
echo ========================
echo 

gcc -o $1 $1.c
./$1

echo 
echo ========================
