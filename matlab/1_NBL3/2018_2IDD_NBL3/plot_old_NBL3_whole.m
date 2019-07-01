%% plot
close all
clc
%outer loop
scans = {'scan551', 'scan475', 'scan440'};                                      %change to scans you've run
samplename = {'NBL3-2', 'NBL3-3', 'TS58A'};

%inner loop
desired_channels = {'Cd_L'};%, 'Cd_L', 'Cu'};                      %for reference within structure, used in surface function
plotname = {'Cd'};%, 'Cd', 'Cu'};                                   %for plot titles, labels, etc 
ext = {'arr_corr'};%, 'arr_corr', 'arr_corr'};

label_size = 18;
tick_size = 15;

for i = 1:length(scans)
    
    for j = 1:length(desired_channels)
        figure(j)
        %subplot(1, 3, j, opt{1,1,1});
        channel = xrf.(scans{i}).whole.(desired_channels{j}).(ext{j});
        
        rawYpos = xrf.(scans{i}).whole.yPosition.raw;
        rawXNo = xrf.(scans{i}).whole.yPixelNo.raw;
        rawYNo = xrf.(scans{i}).whole.xPixelNo.raw;
        [x, y, channel_map] = map_array(rawYpos, channel, rawXNo, rawYNo);
        
        surface(x, y, channel_map, 'LineStyle', 'none')
        colormap jet
        axis square
        
        pltname = sprintf('%s', plotname{j});
        title(pltname, 'fontsize', 21);
        
        ax = gca;
        ax.FontSize = tick_size;
        xlabel('X position (\mum)', 'fontsize', label_size);
        ylabel('Y position (\mum)', 'fontsize', label_size);
        
        z = colorbar;
        z.FontSize = tick_size;
        leg_names = {"A", "\mug/cm^{2}", "\mug/cm^{2}"};
        leg_label = leg_names{j};
        ylabel(z, leg_label);%, 'fontsize', 18);
        
        [upper_cbar_bound, lower_cbar_bound] = get_colorbar_scale(channel, 2); %NOTE: number is the number of standard deviations to include
        caxis([lower_cbar_bound upper_cbar_bound])
        filename = sprintf("%s, %s Cd NBL3-3.jpg", samplename{i}, plotname{j});
        plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190613_new plots for old scans\', filename); %Specificy path in quotes
        saveas(gcf,  plotpath)
    end
    close all
    
end
