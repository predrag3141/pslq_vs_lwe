# PSLQ vs. Learning With Errors
This repository contains experiments using [PSLQ](https://www.davidhbailey.com/dhbpapers/pslq.pdf) to break a particular Learning With Errors (LWE) encryption scheme in a toy-sized example. In short, the LWE scheme challenges an attacker to solve a linear equation over a finite field with many constraints. PSLQ is suited to solve the same problem, but with just one constraint. So the code in this repository transforms the original multi-constraint equation into a single-constraint equation and uses PSLQ to solve it in some toy examples.

# How it Works
PSLQ is an algorithm that can find a small but not-all-zero integer-only solution z<sub>1</sub>,z<sub>2</sub>,...,z<sub>n</sub> of the equation

<p>a<sub>1</sub>z<sub>1</sub>+a<sub>2</sub>z<sub>2</sub>+...+a<sub>n</sub>z<sub>n</sub>=0 (1)</p>

where the a<sub>i</sub> are real numbers.

The [Learning With Errors](https://en.wikipedia.org/wiki/Learning_with_errors) problem, whose hardness is the security guarantee for a variety of cryptographic primitives, is similar to equation (1) in one way: It, too, is a linear equation with a small, hard-to-find, not-all-zero, discrete solution. LWE is the security guarantee for at least two public key encryption schemes. One of these schemes is covered in [this video](https://www.youtube.com/watch?v=K_fNK04yG4o&list=PLgKuh-lKre10rqiTYqJi6P4UlBRMQtPn0&index=7). The description of this scheme starts at 28:30 into the video.

In this scheme, all computations are in a finite field, GF(_q_).

_A_ is a public _n_ x _m_ matrix with _m_ >> _n log(n)_.

One of the parties, whom we will call ALice, chooses short _m_-long vector _x_, a private key. Alice's public key is _u_ = _Ax_. _u_ is an _n_-long column vector.

Another party, Bob, wishes to encrypt a message to Alice. Bob sends the ciphertext preamble, _b_<sup>t</sup>  = _sA_ + _e_<sup>t</sup> -- an _n_-long-vector -- using his own _n_-long secret vector, _s_. (The "_t_"s mean transpose).
