close all;clear all;clc;
%% Data loading
pathname = '../BCI-IV-b/EEG_mat/EEG2';
load(pathname);

% typ = [EEG.event.type].';
% pos = [EEG.event.latency].';
% dur = [EEG.event.duration].';
% time = [EEG.times].';
% data = [EEG.data].';
% Fs = 250;

%  clearvars -except typ pos dur time data EEG h Fs
%% Data Extraction
ltyp = 769;
lEdata = [];
lno = sum(typ == ltyp);
lidx = pos(typ == ltyp);
ldur = dur(typ == ltyp);

rtyp = 770;
rEdata = [];
rno = sum(typ == rtyp);
ridx = pos(typ == rtyp);
rdur = dur(typ == rtyp);

for m = 1:lno
    lEdata = [data(lidx(m):lidx(m)+ldur(m),1:3) lEdata];
end
for m = 1:rno
    rEdata = [data(ridx(m):ridx(m)+rdur(m),1:3) rEdata];
end


%% Essemble Features

C3_lEdata = lEdata(:,1:3:size(lEdata,2));
Cz_lEdata = lEdata(:,2:3:size(lEdata,2));
C4_lEdata = lEdata(:,3:3:size(lEdata,2));

C3_rEdata = rEdata(:,1:3:size(rEdata,2));
Cz_rEdata = rEdata(:,2:3:size(rEdata,2));
C4_rEdata = rEdata(:,3:3:size(rEdata,2));

%Time
std_C3_lEdata = mean_stdDev(C3_lEdata);
std_Cz_lEdata = mean_stdDev(Cz_lEdata);
std_C4_lEdata = mean_stdDev(C4_lEdata);

std_C3_rEdata = mean_stdDev(C3_rEdata);
std_Cz_rEdata = mean_stdDev(Cz_rEdata);
std_C4_rEdata = mean_stdDev(C4_rEdata);
% 
% figure(1)
% subplot(311)
% plot(std_C3_lEdata(:,1))
% hold on
% plot(std_C3_lEdata(:,2))
% hold on
% plot(std_C3_lEdata(:,3))
% 
% subplot(312)
% plot(std_Cz_lEdata(:,1))
% hold on
% plot(std_Cz_lEdata(:,2))
% hold on
% plot(std_Cz_lEdata(:,3))
% 
% subplot(313)
% plot(std_C4_lEdata(:,1))
% hold on
% plot(std_C4_lEdata(:,2))
% hold on
% plot(std_C4_lEdata(:,3))
% 
% figure(2)
% subplot(311)
% plot(std_C3_rEdata(:,1))
% hold on
% plot(std_C3_rEdata(:,2))
% hold on
% plot(std_C3_rEdata(:,3))
% 
% subplot(312)
% plot(std_Cz_rEdata(:,1))
% hold on
% plot(std_Cz_rEdata(:,2))
% hold on
% plot(std_Cz_rEdata(:,3))
% 
% subplot(313)
% plot(std_C4_rEdata(:,1))
% hold on
% plot(std_C4_rEdata(:,2))
% hold on
% plot(std_C4_rEdata(:,3))

%Frequency
f = linspace(-Fs/2,Fs/2,length(std_C3_lEdata));

fft_C3_lEdata = fftshift(fft(C3_lEdata));
fft_Cz_lEdata = fftshift(fft(Cz_lEdata));
fft_C4_lEdata = fftshift(fft(C4_lEdata));

fft_C3_rEdata = fftshift(fft(C3_rEdata));
fft_Cz_rEdata = fftshift(fft(Cz_rEdata));
fft_C4_rEdata = fftshift(fft(C4_rEdata));


%% PCA analysis

% [c,s,l] = pca(C3_lEdata');
% nCz_lEdata = normalize(lEdata(:,2:3:size(lEdata,2)),1);
% nC4_lEdata = normalize(lEdata(:,3:3:size(lEdata,2)),1);
% 
% nC3_rEdata = normalize(rEdata(:,1:3:size(rEdata,2)),1);
% nCz_rEdata = normalize(rEdata(:,2:3:size(rEdata,2)),1);
% nC4_rEdata = normalize(rEdata(:,3:3:size(rEdata,2)),1);

%% Energy Analysis
% check1 = sum(abs(C3_rEdata),1);
% check2 = sum(abs(C4_rEdata),1);
% figure(2)
% plot(check1)
% hold on
% plot(check2)