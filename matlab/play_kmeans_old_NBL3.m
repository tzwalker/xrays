close all
clc

scans = {'scan475', 'scan551', 'scan472', 'scan440'};                                      %change to scans you've run
samplename = {'NBL3-3', 'NBL3-2', 'NBL3-3', 'TS58A'};

%inner loop
desired_channels = {'XBIC_scale', 'Cu'};%, 'Cd_L', 'Cu'};                      %for reference within structure, used in surface function
plotname = {'XBIC', 'Cu'};%, 'Cd', 'Cu'};                                   %for plot titles, labels, etc 
ext = {'arr', 'arr_corr'};%, 'arr_corr', 'arr_corr'};

label_size = 18;
tick_size = 15;
for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
        subplot(1,2,j)
        channel = xrf.(scans{i}).stats.(desired_channels{j}).(ext{j});
        clustered_channel = kmeans(channel, 3);
        
        rawYpos = xrf.(scans{i}).stats.yPosition.raw;
        rawXNo = xrf.(scans{i}).stats.yPixelNo.raw;
        rawYNo = xrf.(scans{i}).stats.xPixelNo.raw;
        [x1, y1, c_map] = map_array(rawYpos, clustered_channel, rawXNo, rawYNo);
        surface(x1, y1, c_map, 'LineStyle', 'none')
        
        xlim([0 max()])
        
        axis square
        xlabel('X position (\mum)', 'fontsize', tick_size);
        ylabel('Y position (\mum)', 'fontsize', tick_size);
        
        z = colorbar;
        %z.FontSize = 12;
        leg_label = 'group #';
        ylabel(z, leg_label, 'fontsize', tick_size);
    end
end