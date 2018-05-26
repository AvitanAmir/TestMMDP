# bgu-aitesting-testoptimizer

Project for finding optimal sub set of test that will give the max bugs using Information gain.

Each test have component with failure probability.

General Entropy -

Ps - probability of success. calculated by multiplication of component success ( 1 - component failure).
Pf - probability of failure. 1 - Ps.
Es - entropy of success: use analyzer code to obtain component new probability given success state.
Pf - entropy of failure: use analyzer code to obtain component new probability given failure state.

Algorithm:

Given X as the max amount of tests.

on each round find the min on each test Ps * Es + Pf * Ef.

perform the test.

do for others until X tests selected.