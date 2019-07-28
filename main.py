

from lex import lexer
from parse_fox import parser
import vistor
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
    ast_=  parser.parse(lexer.lex(source))
    print(ast_)
    vistor.exec_cmd_block(ast_)
    vistor.codegen.create_ir()
    print(vistor.codegen.module)
    vistor.codegen.save_ir("hello.ll")
    
