clear all
clc

% num = [1];
% den = [1 3 1];
g = 9.8;
l = 12;
k1 = -1;
k2 = -0.5;
K = [k1;k2];
A = [0 1;g/l 0];
B = [0;1];
C=[1 0];
D = [0];

sys = ss(A,B,C,D);
[num, den] = ss2tf(A,B,C,D);
eigA = eig(A);
poleSys = pole(sys);


G = tf(num,den)
% H = [1];
H = k2;
M = feedback(G,H)
step(M)
hold on

%%
% Kp = 30;
% Ki = 10;
% Kd = 0;
% 
% C = pid(Kp,Ki,Kd)
% Mc = feedback(C*G,H)
% step(Mc)
% grid on