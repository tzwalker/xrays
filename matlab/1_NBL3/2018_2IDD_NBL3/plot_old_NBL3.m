%% plot
close all
clc
%outer loop
scans = {'scan550', 'scan491', 'scan439'};                                      %change to scans you've run
samplename = {'NBL3-2', 'NBL3-3', 'TS58A'};

%inner loop
desired_channels = {'XBIC_scale', 'Cu'};                      %for reference within structure, used in surface function
plotname = {'XBIC', 'Cu'};                                   %for plot titles, labels, etc 
ext = {'arr', 'arr_corr'};

file_name = {'XBIC'};

for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
        
        subplot(1, 2, j);
        channel = xrf.(scans{i}).(desired_channels{j}).(ext{j});
        
        [x, y, channel_map] = map_array(xrf.(scans{i}).yPosition.raw, channel, xrf.(scans{i}).yPixelNo.raw, xrf.(scans{i}).xPixelNo.raw);
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
        leg_names = {"A", "Cu"};
        leg_label = leg_names{j};
        ylabel(z, leg_label, 'fontsize', 12);
        
        [upper_cbar_bound, lower_cbar_bound] = get_colorbar_scale(channel, 2); %NOTE: number is the number of standard deviations to include
        caxis([lower_cbar_bound upper_cbar_bound])
        filename = sprintf("%s, XBIC and Cu old.jpg", samplename{i});
        plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190523 copper and XBIC_old and new scans\', filename); %Specificy path in quotes
        saveas(gcf,  plotpath)
    end
    close all
end

