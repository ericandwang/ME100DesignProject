%% Clear Workspace
clear all, close all

%% Define file data
filename = 'postureData.csv';

%% import csv file data
T = readtable(filename);
d = table2array(T);
d(:,1) = d(:,1) - d(1,1);

figure, scatter(d(:,1),d(:,2))
hold on
plot(d(:,1),d(:,2))
plot(d(:,1),ones(size(d(:,1))).*30)
xlabel('Time [sec]')
ylabel('Distance from screen [cm]')
title('Posture Estimation Plot')