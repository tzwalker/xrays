%% eletrical
close all
clc
scans = {'scan195', 'scan196', 'scan197'};                         %these are reference the XRF maps int he home 'xrf' structure
sample_names = {'TS118_1A', 'TS118_1A', 'TS118_1A'};

desired_channels = {'XBIC_scale'};                     %for reference within structure, used in surface function
plotname = {'XBIC'};                        %for plot titles, labels, etc 
ext = {'arr'};

file_name = {'XBIC'};

%%%[scale_min, scale_max] = get_scale_range_for_all_scans(all_scans, channel);

for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
        %subplot(1, 2, j);
        channel = xrf.(scans{i}).(desired_channels{j}).(ext{j});
        
        [x, y, channel_map] = map_array(xrf.(scans{i}).yPosition.raw, channel, xrf.(scans{i}).yPixelNo.raw, xrf.(scans{i}).xPixelNo.raw);
        surface(x, y, channel_map, 'LineStyle', 'none')
        colormap jet
        
        pltname = sprintf('%s', plotname{j});
        title(pltname, 'fontsize', 15);
        
        %ax.TickLabelInterpreter = 'latex';
        ax = gca;
        ax.FontSize = 12;
        xlabel('X position (\mum)', 'fontsize', 12);
        ylabel('Y position (\mum)', 'fontsize', 12);
        
        z = colorbar;
        %z.FontSize = 18;
        %z.TickLabelInterpreter = 'latex';
        leg_names = {"A", "\mug/cm^{2}"};
        leg_label = leg_names{j};
        ylabel(z, leg_label, 'fontsize', 12);
        
        [upper_cbar_bound, lower_cbar_bound] = get_colorbar_scale(channel, 2); %NOTE: number is the number of standard deviations to include
        caxis([lower_cbar_bound upper_cbar_bound])
        
%         filename = sprintf("%s, XBIC and Cu.jpg", sample_names{i});
%         plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190602 NREL update\', filename); %Specificy path in quotes
%         saveas(gcf,  plotpath)

    end
%     close all
end


%% histogram
close all
clc

% outer loop
scans = {'scan195', 'scan196'};                         %these are reference the XRF maps int he home 'xrf' structure
sample_names = {'TS118_1A', 'TS118_1A', 'TS118_1A'};
plotname = {'Filtered XBIC', 'Unfiltered XBIC'};                        %in this case, the plot name corresponds to length of scan list
% inner loop
desired_channels = {'XBIC_scale'};                     %for reference within structure, used in surface function
 
ext = {'arr'};

file_name = {'XBIC'};

for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
    channel = xrf.(scans{i}).(desired_channels{j}).(ext{j});
    hist(channel, 20)
    
    pltname = sprintf('%s', plotname{i});
    title(pltname, 'fontsize', 18);
    ax = gca;
    ax.FontSize = 15;
    xlabel('XBIC (A)', 'fontsize', 15);
    ylabel('# of Pixels', 'fontsize', 15);
    filename = sprintf("Plan View Pt1, hist %s.png", plotname{i});
    plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\TS118_1A_decay\', filename); %Specificy path in quotes
    saveas(gcf,  plotpath)
    end
    close all
end
