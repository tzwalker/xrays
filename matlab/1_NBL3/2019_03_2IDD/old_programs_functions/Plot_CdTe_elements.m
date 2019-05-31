%% elemental
close all
clc
scans = {'scan343' 'scan422' 'scan264' 'scan385'};                         %these are XRF maps of approximately same areas in electrical
sample_names = {'NBL3-1', 'NBL3-2', 'NBL3-3', 'TS58A'};

desired_channels = {'Cd','Te','Cu', 'Cu',};% 'Cu', 'Zn', 'Mo_L', 'Sn_L', 'Cl', 'Fe', 'S'};                      %for reference within structure, used in surface function
plotname = {'raw Cd', 'raw Te', 'raw Cu', 'corr Cu', 'Mo', 'Sn', 'Cl', 'Fe', 'S'};                                   %for plot titles, labels, etc 
ext = {'raw', 'raw', 'raw', 'arr_corr'};%, 'arr_corr', 'arr_corr', 'raw', 'raw', 'raw'};


for i = 1:length(scans)
    for j = 1:length(desired_channels)
        figure(i)
        subplot(2, 2, j);
        channel = xrf.(scans{i}).(desired_channels{j}).(ext{j});
        
        [x, y, channel_map] = map_array(xrf.(scans{i}).yPosition.raw, channel, xrf.(scans{i}).yPixelNo.raw, xrf.(scans{i}).xPixelNo.raw);
        surface(x, y, channel_map, 'LineStyle', 'none')
        colormap jet
        axis square
        
        pltname = sprintf('%s, %s', sample_names{i}, plotname{j});
        title(pltname)%, 'fontsize', 20);
        ax = gca;
        %ax.FontSize = 18;
        
        xlabel('X position (\mum)')%,'fontsize', 15);
        ylabel('Y position (\mum)')%,'fontsize', 15);
        
        z = colorbar;
        leg_names = {'at. %','at. %','$\displaystyle\frac{ug}{cm^{2}}$', '$\displaystyle\frac{ug}{cm^{2}}$','$\displaystyle\frac{ug}{cm^{2}}$','$\displaystyle\frac{ug}{cm^{2}}$', '$\displaystyle\frac{ug}{cm^{2}}$','$\displaystyle\frac{ug}{cm^{2}}$','$\displaystyle\frac{ug}{cm^{2}}$'};
        yname = leg_names{j};
        ylabel(z, yname, 'interpreter', 'latex')%, 'fontsize', 20);
        
        %scale colorbar to include 95% of values; i.e. values within 2 standard deviations of the mean
        [upper_cbar_bound, lower_cbar_bound] = get_colorbar_scale(channel, 2); %NOTE: number is the number of standard deviations to include
        caxis([lower_cbar_bound upper_cbar_bound])
    end
        filename = sprintf("%s, elements.jpg", sample_names{i});
        plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190403 NBL3_AXOnoInfo\', filename); %Specificy path in quotes
        saveas(gcf,  plotpath)
    close all
end

