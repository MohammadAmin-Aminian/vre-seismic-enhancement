
clc ; clear ; close all;

% inpute Data
% window =  Lenght Of Moving Window 20,30
% r = Power in Formule, 2,4,8,16
load('Section_GARCH.mat')
Data=myfilter(1:700,150:200);
[nt nx]=size(Data);
window = 80 ;
r = 3 ;

% nt=8;
%%
% Split To Negative And Positive Part
for i = 1 : 1 : nt
    for j = 1 : 1 : nx
        if Data(i,j) >= 0
            datapos(i,j) = Data(i,j);
        end 
    end
end

for i = 1 : 1 : nt
    for j = 1 : 1 : nx
        if Data(i,j) < 0 
            dataneg(i,j) = Data(i,j);
        end 
    end
end
figure();
subplot(2,1,1)
imagesc(datapos);
colorbar;
ylabel('Two way time (ms)')
xlabel('Offset (m)')

title('Posetive Data')

subplot(2,1,2)
imagesc(dataneg);
colorbar;
ylabel('Two way time (ms)')
xlabel('Offset (m)')
title('Negative Data')
%%
% Creating Virtual matrix

Dneg = NaN (nt,nt,nx);
Dpos = NaN (nt,nt,nx);

for k = 1 : 1 : nx
for j = 1 : 1 : nt - window
    for i = j : 1 : j + window
      Dneg(i,j,k) = dataneg(i,k) ;
    end
end
end


Dpos = NaN (nt,nt,nx);
for k = 1 : 1 : nx
for j = 1 : 1 : nt - window
    for i = j : 1 : j + window
      Dpos(i,j,k) = datapos(i,k) ;
    end
end
end
%%
%normalization 
DD2neg = NaN (nt,nt,nx);
for kk = 1: 1:nx
for jj = 1 : 1: nt - window
   for ii = jj : 1 : jj + window
   DD2neg(ii,jj,kk) = nanmin(Dneg(:,jj,kk)).*(((Dneg(ii,jj,kk)/ nanmin(Dneg(:,jj,kk)))).^r);
   end 
end
end



DD2pos = NaN (nt,nt,nx);
for kk = 1: 1:nx
for jj = 1 : 1: nt - window
   for ii = jj : 1 : jj + window
   DD2pos(ii,jj,kk) = nanmax(Dpos(:,jj,kk)).*(((Dpos(ii,jj,kk)/ nanmax(Dpos(:,jj,kk)))).^r);
   end 
end
end
%%
% Mean value of each matrix and converting to a single trace
DD3pos = zeros(nt,nx) ; 
DD3neg = zeros(nt,nx) ; 
for kkk = 1 : 1: nx
for ii = 1 : 1 : nt
    DD3neg(ii,kkk) = nanmean(DD2neg(ii,:,kkk));
    DD3pos(ii,kkk) = nanmean(DD2pos(ii,:,kkk));
end
end
figure()
imagesc(DD3neg + DD3pos )
colormap gray
colorbar
title('Data After VRE')
%%
figure();
subplot(2,1,1)
imagesc(Data)
colormap(seismic(2))

colorbar
title('Data')

subplot(2,1,2)
imagesc(DD3pos + DD3neg)
colormap(seismic(2))
colorbar
title('VRE')
%%
% Frequency Spectrum
dt1 = 0.002;
fs=1/dt1;
% N=l000;
f=[-nt/2:nt/2-1]*fs/1000;

D2 = fftshift(abs(fft(Data(:,:))));

for i = 1 : 1 : nt
dataaa(i,:) = max(D2(i,:));
end
figure();
subplot(2,1,1);
plot(f,dataaa,'LineWidth',1,'color','k')
xlabel('Frequency (Hz)')
ylabel('Amplitude')
% xlim([0 65])
xlim([0 220])
title('Data')
%%
F = fftshift(abs(fft(DD3pos + DD3neg)));

for i = 1 : 1 : nt
fk(i,:) = max(F(i,:));
end
subplot(2,1,2);
plot(f,fk,'LineWidth',1,'color','r')
xlabel('Frequency (Hz)')
ylabel('Amplitude')
% xlim([0 65])
xlim([0 220])
title('VRE')


%%
% Normalize 0 to 1 Spectrum
figure()
% plot(f,normalize(dataaa,'range'),'LineWidth',1,'color','k')
 dataaa=dataaa/(max(max(dataaa)));
plot(f,dataaa,'LineWidth',1,'color','k')

xlabel('Frequency (Hz)')
ylabel('Amplitude')
xlim([0 250])
% ylim([0 8])

hold on

% plot(f,normalize(fk,'range') ,'LineWidth',1,'color','r')
fk=fk/(max(max(fk)));
 plot(f,fk ,'LineWidth',1,'color','r')

xlabel('Frequency (Hz)')
ylabel('Amplitude')
xlim([0 250])

legend('Data','VRE')

