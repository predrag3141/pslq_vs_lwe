# PSLQ vs. Learning With Errors
This repository contains experiments using [PSLQ](https://www.davidhbailey.com/dhbpapers/pslq.pdf) to break a particular [Learning With Errors](https://en.wikipedia.org/wiki/Learning_with_errors) (LWE) encryption scheme in a toy-sized example. In short, the LWE scheme challenges an attacker to find a short solution to a linear equation with many constraints over a finite field. PSLQ is suited to solve the same problem, but with just one constraint. So the code in this repository transforms the original multi-constraint equation into a single-constraint equation and uses PSLQ to solve it in some toy examples.

# How it Works
PSLQ is an algorithm that can find a small but not-all-zero integer-only solution z<sub>1</sub>,z<sub>2</sub>,...,z<sub>n</sub> of the equation

a<sub>1</sub>z<sub>1</sub>+a<sub>2</sub>z<sub>2</sub>+...+a<sub>n</sub>z<sub>n</sub>=0 (equation 1)

where the a<sub>i</sub> are real numbers.

The LWE problem, whose hardness is the security guarantee for a variety of cryptographic primitives, is similar to equation (1) in one way: It, too, is a linear equation with a small, hard-to-find, not-all-zero, discrete solution.

## An LWE Public Key Scheme

LWE is the security guarantee for at least two public key encryption schemes. One of these schemes is covered in [this video](https://www.youtube.com/watch?v=K_fNK04yG4o&list=PLgKuh-lKre10rqiTYqJi6P4UlBRMQtPn0&index=7). The description of this scheme starts at 28:30 into the video.

In this scheme, all computations are in a finite field, GF(_q_).

_A_ is a public _n_ x _m_ matrix with _m_ >> _n log(n)_.

One of the parties, whom we will call Alice, chooses short _m_-long vector _x_, a private key. Alice's public key is

_u_ = _Ax_ mod _q_ (equation 2)

Here,
- _x_ is short enough to keep estimate 5 below within _q_/4, which turns out to be close enough.
- _u_ is an _n_-long column vector.

Another party, Bob, wishes to encrypt a one-bit message, denoted _bit_ below, to Alice. First, Bob sends the ciphertext preamble,

_b_<sup>t</sup> = _sA_ + _e_<sup>t</sup> (equation 3)

Here,
- The "_t_"s mean transpose
- _e_ is a temporary short vector private to Bob.
- _e_, like _x_, is short enough to keep estimate 5 below within _q_/4. That doesn't mean that _e_ and _x_ have similar sizes, but they work together to keep estimate 5 that close.
- Bob uses his own _n_-long secret vector, _s_

Next, using Alice's public key, _u_, Bob sends the payload -- a rational number:

_b'_ = _s_<sup>t</sup> _u_ + _e'_ + (_q_ /2) _bit_

Here,
- _e'_, like _e_ and _x_, is short enough to keep the estimate 5 below within _q_/4.

In order to calculate _bit_ from _b'_, Alice combines Bob's preamble and her private key, _x_, to compute

_b_<sup>t</sup> _x_
&nbsp;&nbsp;&nbsp;&nbsp;= _s_<sup>t</sup> _Ax_ + _e_<sup>t</sup> _x_
&nbsp;&nbsp;&nbsp;&nbsp;= _s_<sup>t</sup> _u_ + _e_<sup>t</sup> _x_
&nbsp;&nbsp;&nbsp;&nbsp;~ _s_<sup>t</sup> _u_ (estimate 4)

Alice then computes

_b'_ - _b_<sup>t</sup> _x_
&nbsp;&nbsp;&nbsp;&nbsp;= _s_<sup>t</sup> _u_ + _e'_ + _bit_ * _q_/2 - _b_<sup>t</sup> _x_
&nbsp;&nbsp;&nbsp;&nbsp;~ _s_<sup>t</sup> _u_ + _e'_ + _bit_ * _q_/2 - _s_<sup>t</sup> _u_ (using estimate 4)
&nbsp;&nbsp;&nbsp;&nbsp;= _e'_ + _bit_ * _q_/2
&nbsp;&nbsp;&nbsp;&nbsp;~ _bit_ * _q_/2 (estimate 5)

Since _x_, _e_ and _e'_ were chosen to keep estimate 5 within ing _q_/4, Alice distinguishes _bit_ = 0 from _bit_ = 1 by concluding that
- _bit_ = 0 if -_q_/4 < _b'_ - _b_<sup>t</sup> _x_ - _b_<sup>t</sup> _x_ < _q_/4
- _bit_ = 1 otherwise

## Deriving a Private Key With PSLQ

What keeps estimate 5 close enough to distinguish _bit_ = 0 from _bit_ = 1 is not the specific value of Alice's private key, _x_. It is also _how short_ _x_ is. So, to break this public key encryption scheme, it is enough to find a vector, _y_, such that
- |_y_| <= |_x_| (in Euclidean norm)
- A|_y_| = _u_ mod _q_

The fact that _x_ is short and that _Ax_ = _u_ mod _q_ are what make estimate 4 work. Any _y_ with those properties would work too. PSLQ can be adapted to find _y_ as follows.

_A_ has row vectors _a_<sub>1</sub>,_a_<sub>2</sub>,...,_a_<sub>n</sub>, and _u_ has corresponding entries, _u_<sub>1</sub>,_u_<sub>2</sub>,...,_u_<sub>n</sub>. Select a suitably-sized integer, _base_.

_Ay_ = _u_ mod q
&nbsp;&nbsp;&nbsp;&nbsp;=>_a_<sub>1</sub> + _base_ _a_<sub>2</sub> + _base_<sup>2</sup> _a_<sub>3</sub> + ... + _base_<sup>n-1</sup> _a_<sub>n</sub>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= _u_<sub>1</sub> + _base_ _u_<sub>2</sub> + _base_<sup>2</sup> _u_<sub>3</sub> + ... + _base_<sup>n-1</sup> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _u_<sub>n</sub> - _q_ - _base_ _q_ - _base_<sup>2</sup> _q_ - ... - _base_<sup>n-1</sup> _q_
&nbsp;&nbsp;&nbsp;&nbsp;=> _q_ + _base_ _q_ + _base_<sup>2</sup> _q_ + ... + _base_<sup>n-1</sup> _q_
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _a_<sub>1</sub> + _base_ _a_<sub>2</sub> + _base_<sup>2</sup> _a_<sub>3</sub> + ... + _base_<sup>n-1</sup> _a_<sub>n</sub>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- _u_<sub>1</sub> - _base_ _u_<sub>2</sub> - _base_<sup>2</sup> _u_<sub>3</sub> - ... - _base_<sup>n-1</sup> _u_<sub>n</sub>
= 0 (equation 6)
