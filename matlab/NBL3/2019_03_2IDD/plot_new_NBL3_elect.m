%% eletrical
close all
clc
scans = {'scan422', 'scan266', 'scan385'};                         %these are reference the XRF maps int he home 'xrf' structure
sample_names = {'NBL3-2', 'NBL3-3', 'TS58A'};

desired_channels = {'XBIC_scale_solo', 'XBIV_scale', 'XBIC_scale'};                     %for reference within structure, used in surface function
plotname = {'XBIC', 'XBIV', 'XBIC/XRF'};                        %for plot titles, labels, etc 
ext = {'arr', 'arr', 'arr'};

file_name = {'XBIC'};

%%%[scale_min, scale_max] = get_scale_range_for_all_scans(all_scans, channel);

for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
        
        subplot(1, 3, j);
        channel = xrf.(scans{i}).(desired_channels{j}).(ext{j});
        
        [x, y, channel_map] = map_array(xrf.(scans{i}).yPosition.raw, channel, xrf.(scans{i}).yPixelNo.raw, xrf.(scans{i}).xPixelNo.raw);
        surface(x, y, channel_map, 'LineStyle', 'none')
        colormap jet
        axis square
        
        pltname = sprintf('%s, %s', sample_names{i}, plotname{j});
        title(pltname, 'interpreter', 'latex')%, 'fontsize', 20);
        ax = gca;
        %ax.FontSize = 18;
        %ax.TickLabelInterpreter = 'latex';
        
        xlabel('X position (\mum)')%, 'interpreter', 'latex')%,'fontsize', 15);
        ylabel('Y position (\mum)')%, 'interpreter', 'latex')%,'fontsize', 15);
        
        z = colorbar;
        %z.FontSize = 18;
        z.TickLabelInterpreter = 'latex';
        leg_names = {"A", "V", 'A'};
        leg_label = leg_names{j};
        ylabel(z, leg_label);%, 'interpreter', 'latex')%, 'fontsize', 15);
        
        [upper_cbar_bound, lower_cbar_bound] = get_colorbar_scale(channel, 2); %NOTE: number is the number of standard deviations to include
        caxis([lower_cbar_bound upper_cbar_bound])

    end
%         filename = sprintf("%s, electrical_filtered.jpg", sample_names{i});
%         plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190403 NBL3_AXOnoInfo\', filename); %Specificy path in quotes
%         saveas(gcf,  plotpath)
%     close all
end



