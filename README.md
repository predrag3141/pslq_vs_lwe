# PSLQ vs. Learning With Errors
This repository contains experiments using [PSLQ](https://www.davidhbailey.com/dhbpapers/pslq.pdf) to break a particular [Learning With Errors](https://en.wikipedia.org/wiki/Learning_with_errors) (LWE) encryption scheme in a toy-sized example. In short, the LWE scheme challenges an attacker to find a short solution to a linear equation with many constraints over a finite field. PSLQ is suited to solve the same problem, but with just one constraint. So the code in this repository transforms the original multi-constraint equation into a single-constraint equation and uses PSLQ to solve it in some toy examples.

# How it Works
PSLQ is an algorithm that can find a small but not-all-zero integer-only solution z<sub>1</sub>,z<sub>2</sub>,...,z<sub>n</sub> of the equation

<p>a<sub>1</sub>z<sub>1</sub>+a<sub>2</sub>z<sub>2</sub>+...+a<sub>n</sub>z<sub>n</sub>=0 (1)</p>

where the a<sub>i</sub> are real numbers.

The LWE problem, whose hardness is the security guarantee for a variety of cryptographic primitives, is similar to equation (1) in one way: It, too, is a linear equation with a small, hard-to-find, not-all-zero, discrete solution. LWE is the security guarantee for at least two public key encryption schemes. One of these schemes is covered in [this video](https://www.youtube.com/watch?v=K_fNK04yG4o&list=PLgKuh-lKre10rqiTYqJi6P4UlBRMQtPn0&index=7). The description of this scheme starts at 28:30 into the video.

In this scheme, all computations are in a finite field, GF(_q_).

_A_ is a public _n_ x _m_ matrix with _m_ >> _n log(n)_.

One of the parties, whom we will call Alice, chooses short _m_-long vector _x_, a private key. Alice's public key is

_u_ = _Ax_ (2)

_u_ is an _n_-long column vector.

Another party, Bob, wishes to encrypt a one-bit message, denoted _bit_ below, to Alice. First, Bob sends the ciphertext preamble,

_b_<sup>t</sup>  = _sA_ + _e_<sup>t</sup> (3)

Here,
- The "_t_"s mean transpose
- Bob uses his own _n_-long secret vector, _s_

Next, using Alice's public key, _u_, Bob sends the payload -- a rational number:

_b'_ = _s_<sup>t</sup> _u_ + _e'_ + (_q_ /2) _bit_

