# PSLQ vs. Learning With Errors
This repository contains experiments using PSLQ to break Learning With Errors (LWE).PSLQ 

# How it Works
[PSLQ](https://www.davidhbailey.com/dhbpapers/pslq.pdf) is an algorithm that can find a small but not-all-zero integer-only solution z<sub>1</sub>,z<sub>2</sub>,...,z<sub>n</sub> of the equation

<p>a<sub>1</sub>z<sub>1</sub>+a<sub>2</sub>z<sub>2</sub>+...+a<sub>n</sub>z<sub>n</sub>=0 (1)</p>

where the a<sub>i</sub> are real numbers.

The Learning With Errors problem, whose hardness is the security guarantee for a variety of cryptographic primitives, is similar to equation (1) in one way: It, too, is a linear equation with a small, hard-to-find, not-all-zero solution. LWE is the security guarantee for at least two public key encryption schemes. One of these schemes is covered in [this video](https://www.youtube.com/watch?v=K_fNK04yG4o&list=PLgKuh-lKre10rqiTYqJi6P4UlBRMQtPn0&index=7). The description of this scheme starts at 28:30 into the video.

In this scheme, the secret is a short solution, x, of the matrix equation

<p>Ax=u<p>
  
Here, A is an n x m matrix and x is a secret one party chooses, and 

