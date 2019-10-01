%% Raw Data
clc; close all;clear all;
[s,h] = sload('./data/B0101T.gdf');
Fs = h.SampleRate;
t = 0:1/Fs:length(s);

typ = h.EVENT.TYP;
pos = h.EVENT.POS;
dur = h.EVENT.DUR;
% art = h.ArtifactSelection;

%% Visualize


ind_typ = 770;

for i = 1:length(typ)
    if typ(i) == ind_typ
        disp(i)
        temp = s(pos(i):(pos(i) + dur(i)),:);
        figure(2)
        subplot(611)
        plot(temp(:,1))
        subplot(612)
        plot(temp(:,2))
        subplot(613)
        plot(temp(:,3))
        subplot(614)
        plot(temp(:,4))
        subplot(615)
        plot(temp(:,5))
        subplot(616)
        plot(temp(:,6))
        r = input('press any key to continue');
        break;
    end    
end

%% Data Extraction

ind_type1 = 769; % class1
ind_type2 = 770; % class2

j = 1;
k = 1;
for i = 1:length(typ)
    disp(i);
    disp(typ(i));
    if typ(i) == ind_type1
        C1_data(:,:,j) = s(pos(i):(pos(i) + dur(i)),:);
        j = j+1;
    end

    if typ(i) == ind_type2
        C2_data(:,:,k) = s(pos(i):(pos(i) + dur(i)),:);
        k = k+1;
    end
end


%% Feature Analysis

event = 2;
d1 = C1_data(:,1:3,event);
d2 = C2_data(:,1:3,event);


m1 = d1(:,[1 3]);
m2 = d2(:,[1 3]);

% figure(1)
% subplot(211)
% plot(m1)
% subplot(212)
% plot(m2)


%% Testing

plotm(m1,m2,Fs,1);

m1 = m1 - d1(:,2); % Cz as referrence
m2 = m2 - d2(:,2);

plotm(m1,m2,Fs,2);



%% Develop

% M1 = fft(m1);
% M2 = fft(m2);
% 
% L = length(M1(:,1));
% f = linspace(-Fs/2,Fs/2,L);
% f = circshift(f,ceil(L/2));
% 
% figure(2)
% subplot(211)
% plot(abs(M1))
% subplot(212)
% plot(abs(M2))

