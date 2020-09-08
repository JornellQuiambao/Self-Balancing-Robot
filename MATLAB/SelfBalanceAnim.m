function Get = SelfBalanceAnim(S)

S1 = S(:,1);
S2 = S(:,2);
l = 12;
L = [1:0.1:l];
sS = size(S);


i=1;
for t = 1:1:sS(1)
    o = S(i,1)*pi/180;
    x = L*cos(o);
    y = L*sin(o);
    plot(x,y,'.')
    xlim(l*[-1,1])
    ylim(l*[0,1.1])
    anim(i)=getframe;
    i=i+1;
end
