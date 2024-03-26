

from lex import lexer
from parse_fox import parser
import vistor
import argparse
source2 = '''
A =0  
for i=1 to 100  
A= A+i 
endfor
? A

'''
source = '''
A = 0
if A >0 
  ? 1
endif
? "hell"
'''
if __name__=='__main__':
    # add args if use 'build', generate 'll' file
    
    parserArg = argparse.ArgumentParser()
    parserArg.add_argument("--build", metavar="filename", help="Generate 'll' postfix file")
    parserArg.add_argument("--run", metavar="filename", help="Run the file")
    args = parserArg.parse_args()

    if args.build:
      with open(args.build, 'r') as file:
        source2 = file.read()
      ast_ = parser.parse(lexer.lex(source2))
      #print(ast_)
      vistor.exec_cmd_block(ast_)
      vistor.codegen.create_ir()
      #print(vistor.codegen.module)
      vistor.codegen.save_ir(args.build + ".ll")
      # call llvm-as to generate 'bc' file

    if args.run:
      with open(args.run, 'r') as file:
        source2 = file.read()
      ast_ = parser.parse(lexer.lex(source2))
      #print(ast_)
      vistor.exec_cmd_block(ast_)
      vistor.codegen.create_ir()
      print(vistor.codegen.module)
      vistor.codegen.run_ir()
    
