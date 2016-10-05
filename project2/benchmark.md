Running

```
make benchmarks
```
on a i7-6560U @ 3 GHz gave the following output

```
N =   50
Reached tolerance (1E-08) in 3955 iterations (1.58 iterations/element)
Solution for non-interacting case with omega=     1, n=50 took 0.006454 seconds
[  2.99566798   6.97830505  10.94697351]

N =   59
Reached tolerance (1E-08) in 5614 iterations (1.61 iterations/element)
Solution for non-interacting case with omega=     1, n=59 took 0.013573 seconds
[  2.99687147   6.98433924  10.96174064]

N =   71
Reached tolerance (1E-08) in 8132 iterations (1.61 iterations/element)
Solution for non-interacting case with omega=     1, n=71 took 0.0255 seconds
[  2.99782816   6.98913209  10.9734597 ]

N =   84
Reached tolerance (1E-08) in 11505 iterations (1.63 iterations/element)
Solution for non-interacting case with omega=     1, n=84 took 0.046156 seconds
[  2.99844203   6.99220568  10.98097027]

N =  100
Reached tolerance (1E-08) in 16238 iterations (1.62 iterations/element)
Solution for non-interacting case with omega=     1, n=100 took 0.085839 seconds
[  2.99889673   6.9944814   10.98652883]

N =  119
Reached tolerance (1E-08) in 23166 iterations (1.64 iterations/element)
Solution for non-interacting case with omega=     1, n=119 took 0.162588 seconds
[  2.99921853   6.99609153  10.99046044]

N =  141
Reached tolerance (1E-08) in 32716 iterations (1.65 iterations/element)
Solution for non-interacting case with omega=     1, n=141 took 0.305165 seconds
[  2.99944196   6.99720924  10.99318909]

N =  168
Reached tolerance (1E-08) in 46576 iterations (1.65 iterations/element)
Solution for non-interacting case with omega=     1, n=168 took 0.597272 seconds
[  2.99960605   6.99802997  10.99519241]

N =  200
Reached tolerance (1E-08) in 65899 iterations (1.65 iterations/element)
Solution for non-interacting case with omega=     1, n=200 took 1.1659 seconds
[  2.99972151   6.99860743  10.99660178]

  N      λ_1      λ_2      λ_3    iterations    it./N**2      time
---  -------  -------  -------  ------------  ----------  --------
 50  2.99567  6.97831  10.947           3955     1.582    0.006454
 59  2.99687  6.98434  10.9617          5614     1.61275  0.013573
 71  2.99783  6.98913  10.9735          8132     1.61317  0.0255
 84  2.99844  6.99221  10.981          11505     1.63053  0.046156
100  2.9989   6.99448  10.9865         16238     1.6238   0.085839
119  2.99922  6.99609  10.9905         23166     1.6359   0.162588
141  2.99944  6.99721  10.9932         32716     1.64559  0.305165
168  2.99961  6.99803  10.9952         46576     1.65023  0.597272
200  2.99972  6.99861  10.9966         65899     1.64748  1.1659
```
