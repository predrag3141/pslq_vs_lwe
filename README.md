# PSLQ vs. Learning With Errors
This repository contains experiments using PSLQ to break Learning With Errors (LWE).PSLQ 

# How it Works
[PSLQ](https://www.davidhbailey.com/dhbpapers/pslq.pdf) is an algorithm that can find a small but non-zero integer-only solution x<sub>1</sub>,x<sub>2</sub>,...,x<sub>n</sub> of the equation

<p>a<sub>1</sub>x<sub>1</sub>+a<sub>2</sub>x<sub>2</sub>+...+a<sub>n</sub>x<sub>n</sub>=0 (1)</p>

where the a<sub>i</sub> are real numbers. The Learning With Errors problem, whose hardness is the security guarantee for a variety of cryptographic primitives, is similar to equation (1) in one way: It, too, is a linear equation with a small solution. 
