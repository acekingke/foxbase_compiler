# -*- coding:utf-8 -*-
__author__ = 'kyc'
import datetime
from fox_ast import *
from err import *
from codegen import CodeGen
alloc_map = dict()
from llvmlite import ir
codegen = CodeGen()
global_var = None
global_var_str = None
def wrap_fun(func):
    def _warp(cmd):
        print ("Now execute %s" % (cmd))
        func(cmd)
    return _warp

def exec_cmd_block(cmd_bolck):
    cmd_list = cmd_bolck.cmd_list
    rt = None
    for i in cmd_list:     
        rt = exec_cmd(i)
        if rt in ("EXIT", "LOOP"):
            break    
def exec_cmd(cmd):
    rt = None
    if not cmd:
        return None
    cmd_type_name = cmd.__class__.__name__
    cmd_type_name = cmd_type_name.replace("Box","exec")+"(cmd)"
    rt = eval(cmd_type_name)
    return rt
def exec_variable(cmd):
    var = alloc_map[cmd.name] 
    return codegen.builder.load(var, cmd.name)
def exec_loop_cmd(cmd):
    return "LOOP"
def exec_exit_cmd(cmd):
    return "EXIT"
def exec_expr(expr):
    if expr.type == "STRING":
        value = ir.Constant(ir.ArrayType(ir.IntType(8), len(expr.val)+1),
                            bytearray((expr.val+'\0').encode("utf8")))
        return value
    elif expr.type == "NUMBER":
        if expr.subtype == "INT":
            return ir.Constant(ir.IntType(32), expr.val)
        elif expr.subtype == "FLOAT":
            return ir.Constant(ir.FloatType, expr.val)
def exec_assign_cmd(assgin):  
    value = exec_cmd(assgin.expr)
    var = alloc_map.get(assgin.var.name)
    if var == None:
        var = codegen.builder.alloca(value.type, None, assgin.var.name)
        alloc_map[assgin.var.name] = var
    return codegen.builder.store(value, var)
def exec_print_cmd(print_cmd):
    value = exec_cmd(print_cmd.expr) 
    global    global_var
    global  global_var_str
    if print_cmd.expr.type == "STRING":
        voidptr_ty = ir.IntType(8).as_pointer()
        if global_var == None:
            global_var = ir.GlobalVariable(codegen.module, value.type, name="gstr")
            global_var.linkage = 'internal'
            global_var.global_constant = True
            global_var.initializer = value
        value_ptr = codegen.builder.bitcast(global_var, voidptr_ty)
        codegen.builder.call(codegen.printf, [value_ptr])
    elif print_cmd.expr.type == "NUMBER":
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%d \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        if global_var_str == None:      
            global_var_str = ir.GlobalVariable(codegen.module, c_fmt.type, name="gfmt_str")
            global_var_str.linkage = 'internal'
            global_var_str.global_constant = True
            global_var_str.initializer = c_fmt
        value_ptr = codegen.builder.bitcast(global_var_str, voidptr_ty)
        codegen.builder.call(codegen.printf, [value_ptr, value])
def exec_op(cmd):
    op = cmd.op
    left = cmd.left
    right = cmd.right
    val_left = exec_cmd(left)
    val_right = exec_cmd(right)
    #Plus
    if op == "PLUS":
        # DATE + NUMBER
        if left.type =="DATE" and right.type == "NUMBER":
           raise ParserError("EXEC error:exec type not match")
        # NUMBER + NUMBER
        elif left.type == "NUMBER" and right.type == "NUMBER":
           return codegen.builder.add(val_left, val_right)
        # STRING + STRING
        elif left.type == "STRING" and right.type == "STRING":
           pass
        else:
            raise ParserError("EXEC error:exec type not match")
    #  Minus
    elif op =="MINUS":
        # DATE-DATE DATE-NUMBER
        if left.type == "DATE" and right.type == "DATE":
           raise ParserError("EXEC error:exec type not match")
        elif left.type == "DATE" and right.type == "NUMBER":
           raise ParserError("EXEC error:exec type not match")
        elif left.type == "NUMBER" and right.type == "NUMBER":
           return codegen.builder.sub(val_left, val_right)
        else:
            raise ParserError("EXEC error:exec type not match")
    #  MUL DIV MOD
    elif op == "MUL":
        if left.type == "DATE" and right.type == "DATE":
           raise ParserError("EXEC error:exec type not match")
        elif left.type == "DATE" and right.type == "NUMBER":
           raise ParserError("EXEC error:exec type not match")
        elif left.type == "NUMBER" and right.type == "NUMBER":
           return codegen.builder.mul(val_left, val_right)
        else:
            raise ParserError("EXEC error:exec type not match")
    elif op == "DIV":
        if left.type == "NUMBER" and right.type == "NUMBER":
            return codegen.builder.sdiv(val_left, val_right)
        else:
            raise ParserError("EXEC error:exec type not match")
    elif op == "MOD":
        raise ParserError("EXEC not suport")
    #  POWER
    elif op == "POWER":
        raise ParserError("EXEC not suport")
    #  uminus
    elif op == "UMINUS":
        raise ParserError("EXEC not suport")
# relation op
# GT
def cmp_gt_date(left, right):
    raise ParserError("EXEC not suport")

def cmp_gt_number(left, right):
    lhs = exec_cmd(left)
    rhs = exec_cmd(right)
    return codegen.builder.icmp_signed('>', lhs, rhs, "icmpgt") 
def cmp_gt_string(left, right):
    raise ParserError("EXEC not suport")
def cmp_gt_logic(left, right):
    raise ParserError("EXEC not suport")
# LT
def cmp_lt_date(left, right):
    raise ParserError("EXEC not suport")

def cmp_lt_number(left, right):
    lhs = exec_cmd(left)
    rhs = exec_cmd(right)
    return codegen.builder.icmp_signed('<', lhs, rhs, "icmplt") 
def cmp_lt_string(left, right):
    raise ParserError("EXEC not suport")
def cmp_lt_logic(left, right):
    raise ParserError("EXEC not suport")


# LE
def cmp_le_date(left, right):
   raise ParserError("EXEC not suport")
def cmp_le_number(left, right):
    lhs = exec_cmd(left)
    rhs = exec_cmd(right)
    return codegen.builder.icmp_signed('<=', lhs, rhs, "icmple") 
def cmp_le_string(left, right):
    raise ParserError("EXEC not suport")
def cmp_le_logic(left, right):
    raise ParserError("EXEC not suport")

# GE
def cmp_ge_date(left, right):
    raise ParserError("EXEC not suport")

def cmp_ge_number(left, right):
    lhs = exec_cmd(left)
    rhs = exec_cmd(right)
    return codegen.builder.icmp_signed('>=', lhs, rhs, "icmpge") 
def cmp_ge_string(left, right):
    raise ParserError("EXEC not suport")
def cmp_ge_logic(left, right):
    raise ParserError("EXEC not suport")

# EQ
def cmp_eq_date(left, right):
   raise ParserError("EXEC not suport")
def cmp_eq_number(left, right):
    lhs = exec_cmd(left)
    rhs = exec_cmd(right)
    return codegen.builder.icmp_signed('==', lhs, rhs, "icmpeq") 
def cmp_eq_string(left, right):
    raise ParserError("EXEC not suport")
def cmp_eq_logic(left, right):
    raise ParserError("EXEC not suport")
# NE
def cmp_ne_date(left, right):
    raise ParserError("EXEC not suport")
def cmp_ne_number(left, right):
    lhs = exec_cmd(left)
    rhs = exec_cmd(right)
    return codegen.builder.icmp_signed('!=', lhs, rhs, "icmpeq") 
def cmp_ne_string(left, right):
    raise ParserError("EXEC not suport")
def cmp_ne_logic(left, right):
    raise ParserError("EXEC not suport")


def exec_relop(cmd):
    op = cmd.op
    type = cmd.left.type
    left = cmd.left
    right = cmd.right
    if type == "LOGIC":
        raise ParserError("EXEC not suport")
    if op == "CONTAIN":
        raise ParserError("EXEC not suport")
    else :
      
       eval_cmd = "cmp_"+op.lower()+"_"+type.lower()+"(left, right)"
       return eval(eval_cmd)

def exec_logic_expr(cmd):
    pass
def  exec_if_cmd(cmd):
    pred = exec_cmd(cmd.expr)
    if cmd.cmd_else :
        with codegen.builder.if_else(pred)  as (then, otherwise):
           with then:
                exec_cmd(cmd.cmd_if)           
           with otherwise:
                exec_cmd(cmd.cmd_else)
    else:        
        with codegen.builder.if_then(pred) :
            exec_cmd(cmd.cmd_if)     

def exec_do_case(cmd):
    pass
#  for while function
#  need support loop and exit
def exec_for_cmd(cmd):
   exec_cmd(cmd.initval)
   #load variable for init
   init = exec_variable(cmd.initval.var)  
   #preheader_bb = codegen.builder.block
   loop_block_start = codegen.builder.append_basic_block(name="loop_block_start")
   loop_block = codegen.builder.append_basic_block(name="loop_block")
   after_loop = codegen.builder.append_basic_block(name = "after_loop")   
   codegen.builder.branch(loop_block_start)  
   codegen.builder.position_at_end(loop_block_start)
   var_init = alloc_map.get(cmd.initval.var.name)
   init1 = codegen.builder.load(var_init, cmd.initval.var.name)  
   endval = exec_cmd(cmd.finalval) 
   cond = codegen.builder.icmp_signed('<=', init1, endval) 
   codegen.builder.cbranch(cond, loop_block, after_loop)
   codegen.builder.position_at_end(loop_block)  
   exec_cmd(cmd.cmd)    
   init2 = codegen.builder.load(var_init, cmd.initval.var.name)  
   init3 = codegen.builder.add(init2, ir.Constant(ir.IntType(32), 1)) 
   codegen.builder.store(init3, var_init)  
   codegen.builder.branch(loop_block_start)
   codegen.builder.position_at_start(after_loop)
   

#  need support loop and exit
def exec_while_cmd(cmd):
    raise ParserError("while does not suport now")

def exec_func_cmd(cmd):
    raise ParserError("func does not suport now")
def  exec_do_cmd(cmd):
    raise ParserError("do does not suport now")
def exec_accept_cmd(cmd):
   raise ParserError("accept does not suport now")

