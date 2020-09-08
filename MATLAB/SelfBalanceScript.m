clear all
close all
clc

%% Parameters
M = .5;
m = 0.2;
b = 0.1;
I = 0.006;
g = 9.8;
l = 0.3;

p = I*(M+m)+M*m*l^2; %denominator for the A and B matrices

%% Matricies
A = [0      1              0           0;
     0 -(I+m*l^2)*b/p  (m^2*g*l^2)/p   0;
     0      0              0           1;
     0 -(m*l*b)/p       m*g*l*(M+m)/p  0];
 
B = [0; (I+m*l^2)/p; 0; m*l/p];

%% Output
C = [1 0 0 0;
     0 0 1 0];
 
D = [0; 0];

%% System
sys = ss(A,B,C,D);

%% Build
x0 = [0; 0; 100; 0];

%% Controller 
Q = eye(4);
R = 0.1;
K = lqr(A,B,Q,R);
