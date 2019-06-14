%% plot
close all
clc
%outer loop
scans = {'scan550', 'scan491', 'scan439'};                                      %change to scans you've run
samplename = {'NBL3-2', 'NBL3-3', 'TS58A'};

%inner loop
desired_channels = {'ds_ic', 'XBIC_scale'};                      %for reference within structure, used in surface function
plotname = {'ds_ ic', 'XBIC'};                                   %for plot titles, labels, etc 
ext = {'raw', 'arr'};

for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
        
        subplot(1, 2, j);
        channel = xrf.(scans{i}).whole.(desired_channels{j}).(ext{j});
        
        rawYpos = xrf.(scans{i}).whole.yPosition.raw;
        rawXNo = xrf.(scans{i}).whole.yPixelNo.raw;
        rawYNo = xrf.(scans{i}).whole.xPixelNo.raw;
        [x, y, channel_map] = map_array(rawYpos, channel, rawXNo, rawYNo);
        
        surface(x, y, channel_map, 'LineStyle', 'none')
        colormap jet
        axis square
        
        pltname = sprintf('%s, %s', samplename{i}, plotname{j});
        title(pltname, 'fontsize', 15);
        ax = gca;
        ax.FontSize = 12;
        %ax.TickLabelInterpreter = 'latex';
        %set(ax, 'TickLabelInterpreter', 'latex')
        
        xlabel('X position (\mum)', 'fontsize', 12);
        ylabel('Y position (\mum)', 'fontsize', 12);
        
        
        z = colorbar;
        %z.FontSize = 12;
        %z.TickLabelInterpreter = 'latex';
        leg_names = {"cts", "A"};
        leg_label = leg_names{j};
        ylabel(z, leg_label, 'fontsize', 12);
        
        [upper_cbar_bound, lower_cbar_bound] = get_colorbar_scale(channel, 2); %NOTE: number is the number of standard deviations to include
        caxis([lower_cbar_bound upper_cbar_bound])

    end
    filename = sprintf("%s, ds_ic and XBIC.jpg", samplename{i});
    plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190613_new plots for old scans\', filename); %Specificy path in quotes
    saveas(gcf,  plotpath)
    
end


close all