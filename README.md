# PSLQ vs. Learning With Errors

This repository contains an experiment using [PSLQ](https://www.davidhbailey.com/dhbpapers/pslq.pdf) to break a particular [Learning With Errors](https://en.wikipedia.org/wiki/Learning_with_errors) (LWE) encryption scheme in a toy-sized example.

The LWE problem challenges an attacker to find a short solution to a linear equation with many constraints over a finite field. PSLQ is suited to solve the same problem, but with just one constraint. So the code in this repository transforms the original multi-constraint equation into a single-constraint equation and uses PSLQ to solve it in some toy examples.

# How it Works

PSLQ is an algorithm that can find a small but not-all-zero integer-only solution z<sub>1</sub>,z<sub>2</sub>,...,z<sub>n</sub> of the equation

a<sub>1</sub>z<sub>1</sub>+a<sub>2</sub>z<sub>2</sub>+...+a<sub>n</sub>z<sub>n</sub>=0 (equation 1)

where the a<sub>i</sub> are real numbers.

The LWE problem, whose hardness is the security guarantee for a variety of cryptographic primitives, is similar to equation (1) in one way: It, too, is a linear equation with a small, hard-to-find, not-all-zero, discrete solution.

## An LWE Public Key Scheme

LWE is the security guarantee for at least two public key encryption schemes. One of these schemes is covered in [this video](https://www.youtube.com/watch?v=K_fNK04yG4o&list=PLgKuh-lKre10rqiTYqJi6P4UlBRMQtPn0&index=7). The description of this scheme starts at 28:30 into the video.

### Public and Private Key

In this scheme, all computations are in a finite field, GF(_q_), where _q_ is a moderately large prime number. To give an idea of the size of _q_, the toy-sized code in this repository iterates through values of _q_ starting with 11.

_A_ is a public _n_ x _m_ matrix with _m_ >> _n log(n)_. The toy-sized _n_ and _m_ in the code here are 3 and 9, respectively. 

One of the parties, whom we will call Alice, chooses short _m_-long vector _x_, a private key. Alice's public key is

_u_ = _Ax_ mod _q_ (equation 2)

Here,
- _x_ is short enough to keep estimate 5 (below) within _q_/4, which turns out to be close enough.
- _u_ is an _n_-long column vector.

### Encrypting

Another party, Bob, wishes to encrypt a one-bit message, denoted _bit_ below, to Alice. First, Bob sends the ciphertext preamble,

_b_<sup>t</sup> = _sA_ + _e_<sup>t</sup> (equation 3)

Here,
- The "_t_"s mean transpose
- _e_ is a temporary short vector private to Bob.
- _e_, like _x_, is short enough to keep estimate 5 (below) within _q_/4. That doesn't mean that _e_ and _x_ have similar sizes, but they work together to keep estimate 5 that close.
- Bob uses his own _n_-long secret vector, _s_

Next, using Alice's public key, _u_, Bob sends the payload -- a rational number:

_b'_ = _s_<sup>t</sup> _u_ + _e'_ + (_q_ /2) _bit_

Here,
- _e'_, like _e_ and _x_, is short enough to keep the estimate 5 (below) within _q_/4.

### Decrypting

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

Since _x_, _e_ and _e'_ were chosen to keep estimate 5 within _q_/4, Alice distinguishes _bit_ = 0 from _bit_ = 1 by concluding that
- _bit_ = 0 if -_q_/4 < _b'_ - _b_<sup>t</sup> _x_ - _b_<sup>t</sup> _x_ < _q_/4
- _bit_ = 1 otherwise

## Breaking this Scheme with PSLQ

"Breaking LWE" sounds dramatic, but this is a toy-sized example. Lots already goes wrong as we'll see; yet all of it is repairable at the scale of a toy example. As we'll also see, there was one success out of many failures, but the ratio should improve with tweaks to PSLQ. The interesting part would be trying to scale the size of the example, and of course more can go wrong when that happens. But PSLQ *is* a polynomial time algorithm in precision and dimension (_m_ in this case). So there is reason to investigate, beginning with this baby step.

### Any Short Solution Works

What keeps estimate 5 close enough to distinguish _bit_ = 0 from _bit_ = 1 is not the specific value of Alice's private key, _x_. It is _how short_ _x_ is. To break this public key encryption scheme, it is enough to find a vector, _y_, such that
- |_y_| <= |_x_| (in Euclidean norm)
- _Ay_ = _u_ mod _q_

The fact that _x_ is short and that _Ax_ = _u_ mod _q_ are what make estimate 4 work. Any _y_ with those properties would work too. PSLQ can be adapted to find _y_ as follows.

### Constructing Input to PSLQ

Notation:
- _A_ has row vectors _a_<sub>1</sub>,_a_<sub>2</sub>,...,_a_<sub>n</sub>
- _u_ has corresponding entries, _u_<sub>1</sub>,_u_<sub>2</sub>,...,_u_<sub>n</sub>
- Select a suitably-sized integer, denoted _base_ in what follows
- _y_ will denote the short solution mentioned in the previous section.
- _v_ will denote the input to give PSLQ, to get PSLQ to return a short solution of _Ay_ = _u_ mod _q_

_Ay_ = _u_ mod q

&nbsp;&nbsp;&nbsp;&nbsp;=>_a_<sub>1</sub> + _base_ _a_<sub>2</sub> + _base_<sup>2</sup> _a_<sub>3</sub> + ... + _base_<sup>n-1</sup> _a_<sub>n</sub>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= _u_<sub>1</sub> + _base_ _u_<sub>2</sub> + _base_<sup>2</sup> _u_<sub>3</sub> + ... + _base_<sup>n-1</sup> _u_<sub>n</sub>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- _q_ - _base_ _q_ - _base_<sup>2</sup> _q_ - ... - _base_<sup>n-1</sup> _q_

&nbsp;&nbsp;&nbsp;&nbsp;=> _q_ + _base_ _q_ + _base_<sup>2</sup> _q_ + ... + _base_<sup>n-1</sup> _q_

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _a_<sub>1</sub> + _base_ _a_<sub>2</sub> + _base_<sup>2</sup> _a_<sub>3</sub> + ... + _base_<sup>n-1</sup> _a_<sub>n</sub>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ (-_u_<sub>1</sub>) + _base_ (-_u_<sub>2</sub>) + _base_<sup>2</sup> (-_u_<sub>3</sub>) + ... + _base_<sup>n-1</sup> (-_u_<sub>n</sub>) = 0 (equation 6)

Based on equation 6, PSLQ is given input

_v_ = (_q_, _base_ _q_, _base_<sup>2</sup> _q_, ..., _base_<sup>n-1</sup> _q_,  _a_<sub>1</sub>, _base_ _a_<sub>2</sub>, _base_<sup>2</sup> _a_<sub>3</sub>, ..., _base_<sup>n-1</sup> _a_<sub>n</sub>, -_u_<sub>1</sub>, _base_ (-_u_<sub>2</sub>), _base_<sup>2</sup> (-_u_<sub>3</sub>), ..., _base_<sup>n-1</sup> (-_u_<sub>n</sub>)

### Calling PSLQ

PSLQ *will* find a short solution _y_ of <_v_, _y_> = 0. If all goes well, _y_ will be a solution of _Ay_ = _u_ mod _q_.

What can go wrong is
- _y_ being a short non-causal solution; i.e., it does not satisfy each equation <_a_<sub>_i_</sub>, _y_> = _u_<sub>_i_</sub>, _i_=1,...,_n_. To mitigate this risk, _base_ must be chosen large enough that _y_ being is likely to be causal. In the code, for reasons outside the scope of this README, _base_ = 20<sup>(_m_ + _n_)/_n_</sup>.
- _y_ not even being short! Though PSLQ is designed to produce short solutions, its intended use case is for non-integer inputs. In this scenario, any integer solution is (falsely) considered a win, and PSLQ terminates. There is a potential remedy to this problem, which -- for the most part -- is also outside the scope of this README. Suffice it to say that PSLQ optimizes the size of diagonal elements in its intenal matrix, H. But PSLQ also tracks an integer matrix, B, whose columns get close to the solution plane. Rather than optimize the diagonal elements of H, the algorithm could be modified to optimize the size of the projection of B's columns onto that plane. This would steadily sharpen the bound on the smallest solution of <_v_,_y_> = 0. Only when this bound can no longer be sharpened, would PSLQ be allowed to terminate. But the implementation of PSLQ that the code in this repository uses doesn't incorporate such a modification.
- _y_<sub>_m_ + _n_ + 1</sub> != 1. If the last coefficient of _y_ is 0, _y_ is a solution of _Ay_ = 0 -- no use in this situation. If the last coefficient of _y_ is other than 0 or 1, the solution needs to be multiplied by _y_<sub>_n_ + _m_ + 1</sub><sup>-1</sup> mod q. Only if _y_<sub>_n_ + _m_ + 1</sub> is a unit (1 or -1) does _y_/_y_<sub>_n_ + _m_ + 1</sub> remain a short solution of _Ay_ = _u_.

You may have noticed a strange reordering of terms in the previous section, "Constructing Input to PSLQ". The _q_-related coefficients -- _base_<sup>i</sup> _q_ for _i_=1,2,...,_n_ -- were moved from the end to the beginning of _v_. This is because, in the ordering with the _base_<sup>i</sup> _q_ at the end, the particular implementation of PSLQ used caused the second bullet above, about _y_ not always being short, to come true. PSLQ returned a vector _y_ that is all-zero, except for two coefficients 1 and -_base_. These two coefficients corresponded to some _base_<sup>i</sup> and _base_<sup>i+1</sup> in _v_. In this unuseable result, |_y_| = sqrt(1 + _base_<sup>2</sup>) ~ _base_ -- a disappointingly long output for PSLQ, and one with coefficient 0 for the coordinate that packages up the elements of _u_.

# Running the Experiment

The code in this repository is a single file, PSLQ_vs_LWE.py. It defines small _n_ and _m_, and generates _v_ as described above. To run this, install [Python](https://www.python.org/downloads) and [mpmath](https://mpmath.org/doc/current/setup.html) if you haven't already.

Below is the output of a successful run. It was one output amongst those of many unsuccessful runs. The unsuccesful runs went awry for the reasons in the bullet list under "What can go wrong" in the section, "Deriving a Private Key With PSLQ".

Output of a successful run:
```
q = 11, n = 3, m = 9; Quit (y/n)?

n
A: [[3, 10, 4, 8, 10, 9, 8, 5, 10], [9, 10, 9, 8, 5, 1, 7, 1, 3], [1, 4, 4, 10, 4, 4, 7, 5, 4]]
Private key x: [1, -1, 0, 1, 0, -1, -2, 0, -1]
rawU: [-34, -11, -15]
u: [10, 0, 7]
rawUOverQ: [4, 1, 2]
base: 160000

Input v to PSLQ: [11, 1760000, 281600000000, 25601440003, 102401600010, 102401440004, 256001280008, 102400800010, 102400160009, 179201120008, 128000160005, 102400480010, -179200000010]

Expected output w of PSLQ: [4, 1, 2, 1, -1, 0, 1, 0, -1, -2, 0, -1, 1]

<v,x> - v[9] = <[11, 1760000, 281600000000, 25601440003, 102401600010, 102401440004, 256001280008, 102400800010, 102400160009, 179201120008, 128000160005, 102400480010, -179200000010], [1, -1, 0, 1, 0, -1, -2, 0, -1]> - 179201120008 = -204801760024

<v,w> = <[11, 1760000, 281600000000, 25601440003, 102401600010, 102401440004, 256001280008, 102400800010, 102400160009, 179201120008, 128000160005, 102400480010, -179200000010], [4, 1, 2, 1, -1, 0, 1, 0, -1, -2, 0, -1, 1]> = 0

PSLQ Found a causal solution [0, -1, 0, 0, 0, 0, 0, 0, -2, 1, 0, 2, 1]  with norm 2.23606797749979 : [0, -1, 0, 0, 0, 0, 0, 0, -2, 1, 0, 2, 1] != [1, -1, 0, 1, 0, -1, -2, 0, -1] = x
```

Here is the meaning of the solution, _v_, above. The first three coefficients (0, -1, 0) of _v_ make the rest of the solution work mod _q_. The next _m_ + 1 = 10 coefficients annihilate (_a_<sub>i,1</sub>, _a_<sub>i,2</sub>, ..., _a_<sub>i,9</sub>, -_u_<sub>i</sub>) mod _q_ for _i_=1,2,3.

# Conclusion

The experiment in this repository shows that attacking LWE with PSLQ may hold some promise. The next step is to implement PSLQ with adaptations to perform better with integer inputs. This implementation should be capable of arbitrary precision, in order to attack LWE with more realistic _m_, _n_ and _q_.

Lastly, it's worth mentioning that there is a way to defend against this attack, and perhaps other lattice reduction attacks. Notice that PSLQ will tend to find small coefficients of the _q_-related coefficients, _base_<sup>_i_</sup> _q_. A randomly chosen private key, _x_, makes these coefficients small (~sqrt(nq)). But a carefully chosen _x_ could make the causal coefficients of _base_<sup>_i_</sup> large. To defend on lattice attacks like this one, it will help if
- _x_ be the *only* solution of _Ax_ = _u_ mod _q_ small enough for Alice to calculate _bit_ and
- _x_ be chosen so that some of the <_a_<sub>i</sub>, _x_> are a large multiple of _q_ that a lattice reduction algorithm will reject.

The first constraint above may be difficult to pull off, and the two constraints are not a complete answer to lattice attacks. The attacker can still launch a statistical attack on biased plaintext, even without calculating _bit_ correctly every time, by finding a small enough _y_ -- albeit not as small as the private key, _x_ -- such that _Ay_ = _u_ mod _q_. With all that said, the easier constraint -- choosing _x_ so that some of the <_a_<sub>i</sub>, _x_> - _u_<sub>i</sub> are large multiples of _q_ -- is probably a good practice.
