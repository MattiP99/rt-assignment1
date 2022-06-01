%%Main

clc
clear
close all

Conf_loops_mattia;
Conf_loops_professor;


%MATTIA and PROFESSOR
T7_m = Tm7;
T7_p = Tc7;

D7_m = Dm7;
D7_p = Dc7;

T9_m = Tm9;
T9_p = Tc9;

D9_m = Dm9;
D9_p = Dc9;






figure(1)
cdfplot(T7_m)
hold on
mT7_values = linspace(min(T7_m),max(T7_m));
uno = plot(mT7_values,normcdf(mT7_values,75,5),'r-')
hold off

figure(2)
cdfplot(T9_m)
hold on
mT9_values = linspace(min(T9_m),max(T9_m));
due = plot(mT9_values,normcdf(mT9_values,70,10),'r-')
hold off

figure(3)
cdfplot(D7_m)
hold on
mD7_values = linspace(min(D7_m),max(D7_m));
tre = plot(mD7_values,normcdf(mD7_values,1.5,0.3),'r-')
hold off

figure(4)
cdfplot(D9_m)
hold on
mD9_values = linspace(min(D9_m),max(D9_m));
quattro = plot(mD9_values,normcdf(mD9_values,1.4,0.25),'r-')
hold off

[h1,p1] = ttest2(D9_p,D9_m)
[h2,p2] = ttest2(D7_p,D7_m)
[h3,p3] = ttest2(T9_p,T9_m)
[h4,p4] = ttest2(T7_p,T7_m)

avT9m = mean(T9_m)
avT9p = mean(T9_p)
avT7m = mean(T7_m)
avT7p = mean(T7_p)

avD7m = mean(D7_m)
avD7p = mean(D7_p)
avD9m = mean(D9_m)
avD9p = mean(D9_p)

varD9m = var(D9_m)
varD9p = var(D9_p)

varT9m = var(T9_m)
varT9p = var(T9_p)
varT7m = var(T7_m)
varT7p = var(T7_p)

varD7m = var(D7_m)
varD7p = var(D7_p)

varD9m = var(D9_m)
varD9p = var(D9_p)

figure(5)
ist1 = histogram(T9_p,30)
figure(6)
ist2 = histogram(T9_m,30)
figure(7)
ist3 = histogram(D9_p,30)
figure(8)
ist4 = histogram(D9_m,30)
figure(9)
ist5 = histogram(D7_p,30)
figure(10)
ist6 = histogram(D7_m,30)

figure(11)
ist7 = histogram(T7_p,30)
figure(12)
ist8 = histogram(T7_m,30)



