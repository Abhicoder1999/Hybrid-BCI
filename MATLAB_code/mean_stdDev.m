function [data] = mean_stdDev(input)
%%
%Here the Coloumbs are the Variables and the Rows as the sample inputs
%%
data = zeros(size(input,1),3);
temp = (input);
data_std = std(temp',1);
data_std = data_std';
data_mean = mean(temp,2);

temp = data_mean + data_std;
data(:,1) = (temp);
temp = data_mean;
data(:,2) = (temp);
temp = data_mean - data_std;
data(:,3) = (temp);

% disp(size(data))
end
