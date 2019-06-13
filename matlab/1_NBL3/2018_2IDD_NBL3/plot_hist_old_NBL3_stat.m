%% plot
close all
clc
%outer loop
scans = {'scan550', 'scan491', 'scan439'};                                      %change to scans you've run
samplename = {'NBL3-2', 'NBL3-3', 'TS58A'};

%inner loop
desired_channels = {'Cu', 'Cd_L'};                      %for reference within structure, used in surface function
plotname = {'Cu', 'Cd'};                                   %for plot titles, labels, etc 
ext = {'arr_corr', 'arr_corr'};

for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
        
        subplot(1, 2, j);
        channel = xrf.(scans{i}).stats.(desired_channels{j}).(ext{j});
        hist(channel, 10)
        
        pltnme = sprintf('%s, %s', samplename{i}, plotname{j}); 
        title(pltnme);
        xlabel('\mug/cm^{2}');
        ylabel('Count');
        
        
        
    end
    filename = sprintf("%s, hist for kmeans cluster check Cu_Cd.jpg", samplename{i});
    plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190613_old scan Cu_Cd hist_noZeros\', filename); %Specificy path in quotes
    saveas(gcf,  plotpath)
    close all
end


