close all
clear all
clc

% This matlab script creates the physics of the inverted pendulum system

%% System

% Test numbers for mass and physics of the system
M = 0.5;
m = 0.2;
b = 0.1;
I = 0.006;
g = 9.8;
l = 0.3;
q = (M+m)*(I+m*l^2)-(m*l)^2;
s = tf('s');

% Dimensions of Simulink model
h = 12;
w = 11;
ww = 1;
Mc = 1;
Mw = 1;

% Transfer Functions of the system

P_cart = (((I+m*l^2)/q)*s^2 - (m*g*l/q))/(s^4 + (b*(I + m*l^2))*s^3/q - ((M + m)*m*g*l)*s^2/q - b*m*g*l*s/q);

P_pend = (m*l*s/q)/(s^3 + (b*(I + m*l^2))*s^2/q - ((M + m)*m*g*l)*s/q - b*m*g*l/q);

sys_tf = [P_cart ; P_pend];

inputs = {'u'};
outputs = {'x'; 'phi'};

set(sys_tf,'InputName',inputs)
set(sys_tf,'OutputName',outputs)

sys_tf;

%% PID Controller
Kp = 10;
Ki = 1;
Kd = 1;
C = pid(Kp,Ki,Kd);
T = feedback(P_pend,C);

%% Plotting the matlab system

% t=0:0.01:10;
% impulse(T,t)
% % axis([0, 2.5, -0.2, 0.2]);
% title('Response of Pendulum Position to an Impulse Disturbance');

