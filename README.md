# the grammar of the language

It's a subset of foxbase language.

## Assign variable

```
A = 1
```
## print variable
```
? A
```
## expression
It supports add, sub, mult, div

## loop
```
for i=1 to 100
    ? i
endfor
```
# Install

python >= 3.7

```
pip install rply
pip install llvmlite
```

# compile it 

It generates llvm ir file, then you can use clang to compile it.
```
python3 main.py --build examples/hello.prg
```
Then it generates hello.prg.ll in `examples` folder

```shell
clang -o hello hello.prg.ll
./hello
hello the world
```
# run it immediately

```
python3 main.py --run examples/hello.prg
python3 main.py --run examples/fib.prg
```

