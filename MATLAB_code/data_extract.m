close all;clear all;clc;
%% Data loading
pathname = '../BCI-IV-b/EEG_mat/EEG3';
load(pathname);

typ = [EEG.event.type].';
pos = [EEG.event.latency].';
dur = [EEG.event.duration].';
time = [EEG.times].';
data = [EEG.data].';

clearvars -except typ pos dur time data EEG
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

C3L = lEdata(:,1:3:lno*3);
CZL = lEdata(:,2:3:lno*3);
C4L = lEdata(:,3:3:lno*3);

C3R = rEdata(:,1:3:rno*3);
CZR = rEdata(:,2:3:rno*3);
C4R = rEdata(:,3:3:rno*3);

%% Feature Extraction

meanC3L = mean(abs(C3L));
meanCZL = mean(abs(CZL));
meanC4L = mean(abs(C4L));

meanC3R = mean(abs(C3R));
meanCZR = mean(abs(CZR));
meanC4R = mean(abs(C4R));