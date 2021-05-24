riscv32-unknown-linux-gnu-gcc output.S -o output -L/root -lsysy -static
rm -f test.tmp.out
if [ ! -f "test.in" ]; then
    qemu-riscv32-static output > test.tmp.out
else
    qemu-riscv32-static output < test.in > test.tmp.out
fi
x=$?
echo "" >> test.tmp.out
echo $x >> test.tmp.out
rm -f test.in
