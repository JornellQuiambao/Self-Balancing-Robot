close all
clear all
clc

%% Parameters
M = 5;
m = 0.5;
g = 9.8;
l = 12;

%% Matrix

A = [0,1;g/l,0];
B = [0;1];

%% Output
C = [1,0];
D = 0;

%% System
sys = ss(A,B,C,D);

%% Build

% x0 = [0;5*pi/180];
x0 = [115;0];


%% Controller
% des_poles = [-0.9;-0.9];
% K = acker(A,B,des_poles);

Q = 50*eye(2);
R = 0.1;
K = lqr(A,B,Q,R);

% K = [20,20];
% F = feedback(K*sys,1);


