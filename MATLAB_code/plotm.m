function [] = plotm(m1,m2,Fs,k)
nfft = 2^nextpow2(length(m1(:,1)));

figure(k)
Pxx = abs(fft(m1,nfft)).^2/length(m1(:,1))/Fs;
Hpsd = dspdata.psd(Pxx(1:length(Pxx(:,1))/2,:),'Fs',Fs);
subplot(211)
plot(Hpsd)

Pxx = abs(fft(m2,nfft)).^2/length(m1(:,1))/Fs;
Hpsd = dspdata.psd(Pxx(1:length(Pxx(:,1))/2,:),'Fs',Fs);
subplot(212)
plot(Hpsd)
end

