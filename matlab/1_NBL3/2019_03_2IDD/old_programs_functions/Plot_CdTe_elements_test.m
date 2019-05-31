%% elemental
close all
clc
scans = {'scan343' 'scan422' 'scan264' 'scan385'};                         %these are XRF maps of approximately same areas in electrical
sample_names = {'NBL3-1', 'NBL3-2', 'NBL3-3', 'TS58A'};

desired_channels =  {'Cd_L'};%,'Zn', 'Cu', 'Cd_L', 'Te_L', 'Sn_L'};                      %for reference within structure, used in surface function
plotname =          {'Cd_L'};%,'Zn', 'Cu', 'Cd_L', 'Te_L', 'Sn_L'};                                   %for plot titles, labels, etc 
ext =               {'arr_corr'};%, 'arr_corr', 'arr_corr', 'arr_corr', 'arr_corr', 'arr_corr', 'arr_corr', 'arr_corr', 'arr_corr'};


for i = 1:length(scans)
    figure(i)
    for j = 1:length(desired_channels)
        
        %subplot = @(m,n,p) subtightplot(m, n, p, [1 1]);
        %subplot(3,3,j)
        channel = xrf.(scans{i}).(desired_channels{j}).(ext{j});
        
        [x, y, channel_map] = map_array(xrf.(scans{i}).yPosition.raw, channel, xrf.(scans{i}).yPixelNo.raw, xrf.(scans{i}).xPixelNo.raw);
        surface(x, y, channel_map, 'LineStyle', 'none')
        colormap jet
        axis square
        
        pltname = sprintf('%s', plotname{j});
        title(pltname, 'fontsize', 20);
        ax = gca;
        ax.FontSize = 16;
        
        xlabel('X position (\mum)','fontsize', 18);
        ylabel('Y position (\mum)','fontsize', 18);
        
        z = colorbar;
        leg_names = {'ug/cm^{2}','ug/cm^{2}','ug/cm^{2}','ug/cm^{2}','ug/cm^{2}', 'ug/cm^{2}', 'ug/cm^{2}', 'ug/cm^{2}', 'ug/cm^{2}'};
        yname = leg_names{j};
        ylabel(z, yname, 'fontsize', 18);
        
        %scale colorbar to include 95% of values; i.e. values within 2 standard deviations of the mean
        [upper_cbar_bound, lower_cbar_bound] = get_colorbar_scale(channel, 2); %NOTE: number is the number of standard deviations to include
        caxis([lower_cbar_bound upper_cbar_bound]);
%         filename = sprintf("%s, %s.png", sample_names{i}, plotname{j});
%         plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190501 Q6 reporting newest plots_m\layer_corrected\', filename); %Specificy path in quotes
%         saveas(gcf,  plotpath)
%         close all
    end

    
end

