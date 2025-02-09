# _250209_sql_parser

It's some kind of LR Parser.
There are three steps.
1. Build a parser by grammars (ex: `query → SELECT select-list FROM from-list`)
- [parser.py](parser.py) is auto-generated parser from the parser builder.   
2. Lexer, Convert plain text to token list.
- I used `regex` for code-writing efficiency. I am not sure whether it is right or not. At least, it's working!
- Save [Lexer output](1.lex) from [Some SQL file](1.sql)
3. Parser, Convert token list to tree.
- Save [Parser output](1.tree) as html-like format. 


### Previous Problem
- Parser couldn't decide which one to reduce.  
  ex:   
  ```
  S → expr $    
  expr → cmp_expr  
  expr → assign_expr;  
  cmp_expr → n = n
  assign_expr → n = n
  ```  
  if `input: 1 = 1`, `n` should be part of `cmp_epxr`    
  if `input: 1 = 1;`, `n` should be part of `assign_epxr`  
  But givens are like this when the parser have to decided.    
  ```
  input: ; $
  [State]  
  cmp_expr → n = n●
  assign_expr → n = n●
  ```
  The parser could not know right one.
  So, I added **lookahead**.
  ```
  input: ; $
  [State]  
  cmp_expr → n = n● , $
  assign_expr → n = n● , ;
  ```
  Now, the parser could know which one to reduce by lookahead.
- I traveled for hours to find how to make lookahead of each non-terminal.  
  At the beginning, Everything is OK. But I found some edge cases.
  It was like this.
  ```
  S -> expr $
  expr -> compare_expr | bool_expr 
  bool_expr -> compare_expr
  bool_expr -> TRUE | FALSE
  compare_expr -> bool_expr AND bool_expr  
  ```
  **Problem 1. What is FIRST(bool_expr) and FIRST(compare_expr).**  
  ```
  FIRST(bool_expr) = { TRUE, FALSE } ∪ FIRST(compare_expr)
  FIRST(compare_expr) = FIRST(bool_expr)
  ```
  I solved it by excluding FIRST sets by the condition.  
  (When B is first non-terminal of A. and B starts only  with A.)      
  
  **Problem 2. What is FOLLOW(bool_expr) and FOLLOW(compare_expr).**
  ```
  FOLLOW(bool_expr) = { $ } ∪ FOLLOW(compare_expr) 
  FOLLOW(compare_expr) = FOLLOW(bool_expr)
  ```
  I solve it by acting like `bool_expr` and `compare_expr` is one rule.   
  But there are a rule to be acting like one. The child non-terminal could be the parent non-terminal without another terminal or non-terminals.  
  And there are no other rules that use the child non-terminal.
# See also
  [Wikipedia - Canonical LR parser](https://en.wikipedia.org/wiki/Canonical_LR_parser)
