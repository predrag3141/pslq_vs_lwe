# -*- coding: utf-8 -*-

from math import log, sqrt
from random import randint
from mpmath import pslq

def isComposite(n_in):
    for i in range(2, n_in):
        if n_in % i == 0:
            return True
        if i * i > n_in:
            return False
    return False

# Loop through q
def runTest(n_in, m_in, maxQ_in):
    for q in range(m_in, maxQ_in):
        #
        # Skip composite values of q.
        # Give the user a chance to end the test.
        #
        if isComposite(q):
            continue
        print(
          "\nq =", str(q)+", n =", str(n_in) + ", m =", str(m_in) + "; Quit (y/n)?"
        )
        response = input()
        if response == "y": return

        #
        # Generate a random A
        #
        A = [[randint(0, q - 1) for j in range(m_in)] for i in range(n_in)]
        print("A:", A)

        #
        # Generate a random x with |x| ~ q/4
        #
        x = [0 for i in range(m_in)]
        squaredNormTarget = (q / 4) * (q / 4)
        while sum([x[i] * x[i] for i in range(m_in)]) < squaredNormTarget:
            indexToModify = randint(0, m_in - 1)
            x[indexToModify] += 2 * randint(0,1)  - 1 # -1 or +1
        print("Private key x:",x)

        #
        # Compute u
        #
        rawU = [sum([x[j] * A[i][j] for j in range(m_in)]) for i in range(n_in)]
        u = [rawU[i] % q for i in range(n_in)]
        rawUOverQ = [(u[i] - rawU[i]) // q for i in range(n_in)]
        print("rawU:", rawU)
        print("u:", u)
        print("rawUOverQ:", rawUOverQ)

        #
        # Compute the base 3^(m/n) k^(1/n) suggested above -- except to
        # use m + n instead of m, in order to account for the additional n
        # columns not mentioned in the README.
        #
        base = int(0.5 + ((20 ** ((m_in + n_in) / n_in))))
        print("base:", base)

        #
        # Compute the input to PSLQ, denoted "v" in the README. The
        # first n entries allow PSLQ to find the multiple of q to subtract from
        # the result. The next m entries come from the m columns of A. The last
        # entry comes from u.
        #
        v = [0 for i in range(m_in + 1 + n_in)]
        powerOfBase = 1
        for i in range(n_in):
            v[i] = q * powerOfBase
            for j in range(m_in):
                v[j + n_in] += powerOfBase * A[i][j]
            v[n_in + m_in] -= powerOfBase * u[i]
            powerOfBase *= base

        #
        # Print input and expected results
        #
        print("\nInput v to PSLQ:", v)
        w = rawUOverQ + x + [1]
        print("\nExpected output w of PSLQ:", w)
        vDotX = sum(
            [v[n_in + i] * x[i] for i in range(m_in)]
        )
        print(
          "\n<v,x> - v[" + str(m) + "] = <" +
          str(v) + ",", str(x) + "> -", v[m],"=",
          vDotX - v[n_in + m_in]
        )
        vDotW = sum(
          [v[i] * w[i] for i in range(m_in + 1 + n_in)]
        )
        print("\n<v,w> = <" + str(v) + ",", str(w) + "> =", vDotW)

        #
        # Run PSLQ and see if the output happens to equal x, and whether it
        # has norm q/4 or less. If the coefficient of u (position m_in + n_in)
        # happens to be 1, multiply the solution by -1
        #
        y = pslq(v)
        if y[m_in + n_in] == -1:
            for i in range(m_in + n_in + 1):
                y[i] = - y[i]
        if sum([y[i] * v[i] for i in range(m_in + n_in + 1)]) != 0:
            print("\nPSLQ found an incorrect solution, ", y)
            return
        solutionIsCausal = True
        for i in range(n_in):
            yDotAi = sum([y[n_in + j] * A[i][j] for j in range(m_in)])
            if (yDotAi - u[i]) % q != 0:
                solutionIsCausal = False
                print(
                  "\n<y,A[", i, "]> = ", yDotAi, "!=", u[i], "= u[", i, "] mod", q
                )
        if solutionIsCausal:
            if y[n_in + m_in] != 1:
                print(
                  "\nPSLQ found a solution ", y, "with coefficient for u",
                  y[n_in + m_in], "!= 1"
                )
            else:
                diffSqNorm = sum(
                  [(y[i] - x[i]) * (y[i] - x[i]) for i in range(m_in)]
                )
                if diffSqNorm == 0:
                    print("\nPSLQ found the private key, x =", str(y) + "!!!")
                else:
                    norm = sqrt(sum([y[i] * y[i] for i in range(m_in)]))
                    if norm <= q / 4:
                        print(
                          "\nPSLQ Found a causal solution", y,
                          " with norm", norm,
                          ":", y, "!=", x, "= x"
                        )
                    else:
                        print(
                          "\nPSLQ found a solution", y,
                          "with norm", norm, "> q / 4 =", q / 4
                        )

# Set fixed parameters
n = 3
m = int(2 * n * log(n, 2))
maxQ = 10 * m

runTest(n, m, maxQ)
