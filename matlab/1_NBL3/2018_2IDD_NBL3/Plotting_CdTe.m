%% plotting in mol/cm2
close all
scans = {'scan439' 'scan475' 'scan519' 'scan550'};                      %change to scans you've run
plot_input = {'Cd_ratio', 'Te_ratio', 'Cu'};                 %for reference within structure, used in surface function
plotname = {'Cd/(Cd+Te)', 'Te/(Cd+Te)', 'Cu'};                                   %for plot titles, labels, etc 
ext = {'map_corr', 'map_corr', 'map_corr', 'map_corr'};


for j = 1:length(scans)
    for i = 1:length(plot_input)
        figure(i)
        %subplot(2, 2, i);
        surface(xrf.(scans{j}).rel_X,   xrf.(scans{j}).rel_Y,   xrf.(scans{j}).(plot_input{i}).(ext{i}), 'LineStyle', 'none');
        
        colormap jet;
        pltname = sprintf('%s, %s', samplename{j}, plotname{i});
        title(pltname, 'fontsize', 20);
        ax = gca;
        ax.FontSize = 18;
        xlabel('X position (\mum)','fontsize', 20);
        ylabel('Y position (\mum)','fontsize', 20);
        %set(gca,'fontsize',10,'fontweight','demi');
        colorbar("FontSize", 18);
        z = colorbar;
        ynames = {'at. %', 'at. %', 'ug/cm2'};
        yname = ynames{i};
        ylabel(z, yname, 'fontsize', 20);
        axis square;
%         filename = sprintf("%s, %s.fig", plot_input{i}, samplename{j});
%         plotpath = fullfile('C:\Users\Trumann\Desktop\XRF_codes_m\CdTe_figures', filename); %Specificy path in quotes
%         saveas(gcf,  plotpath)
    end
    %close all
end

