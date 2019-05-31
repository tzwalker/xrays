%% hex bin plot
close all
clc
scans = {'scan422' 'scan266' 'scan385'};                         %change to scans you've run
sample_names = {'NBL3-2', 'NBL3-3', 'TS58A'};

desired_y_channels = {'XBIV_scale', 'Cd_L', 'Te_L', 'Cu', 'Cd_ratio'};                      %for reference within structure, used in surface function
ext = {'arr', 'arr_mol', 'arr_mol', 'arr_mol', 'arr_mol'};

for i = 1:length(scans)
    scan_XBIC = xrf.(scans{i}).XBIC_scale.arr;
    
    for j = 1:length(desired_y_channels)
        figure(j)
        %subplot(1, 3, j);
        
        channel = xrf.(scans{i}).(desired_y_channels{j}).(ext{j});
        hexscatter(scan_XBIC, channel);
        
        axis square
        pltname = sprintf('%s', sample_names{i});
        title(pltname)%, 'fontsize', 20);

        xlabel('XBIC (A)')%,'fontsize', 15);
        leg_names = {'XBIV', 'Cd (mol/cm2)', 'Te (mol/cm2)', 'Cu (mol/cm2)', 'Cd_{ratio} (at.%)'};
        yname = leg_names{j};
        ylabel(yname)%,'fontsize', 15);
        filename = sprintf("%s, %s hexbin.jpg", sample_names{i}, desired_y_channels{j});
        plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190509 redo corr plots_simplified no XCE_no low Cu\', filename); %Specificy path in quotes
        saveas(gcf,  plotpath)
    end
    close all
end
%%
close all
scans = {'scan422' 'scan266' 'scan385'};                         %change to scans you've run
sample_names = {'NBL3-2', 'NBL3-3', 'TS58A'};

desired_y_channels =    {'XBIC_scale', 'XBBIV_scale', 'Cd_L', 'Te_L', 'Cu', 'Cd_ratio'};                      %for reference within structure, used in surface function
ext =                   {'arr', 'arr',  'arr_corr', 'arr_corr', 'arr_corr','arr_mol'};

for i = 1:length(scans)
    figure(i)
    
    XBIC = xrf.(scans{i}).XBIC_scale.arr;
    XBIV = xrf.(scans{i}).XBIV_scale.arr;
    Cd = xrf.(scans{i}).Cd_L.arr_mol;
    Te = xrf.(scans{i}).Te_L.arr_mol;
    Cu = xrf.(scans{i}).Cu.arr_mol;
    Cd_ratio = xrf.(scans{i}).Cd_ratio.arr_mol;
    
    
    data =  [XBIC, XBIV, Cd, Te, Cu, Cd_ratio];%, Cd_ratio, Cd, Cu, Cu_over_Cd, Cu_over_Te, Cd_over_Te];
    corrplot(data, 'varnames', {'XBIC'; 'XBIV'; 'Cd';  'Te' ;'Cu'; 'Cd_ratio'})
    title(sprintf('%s', sample_names{i}))
  
%     filename = sprintf("%s, corrplot.png", sample_names{i});
%     plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190509 redo corr plots_simplified no XCE_no low Cu\', filename); %Specificy path in quotes
%     saveas(gcf,  plotpath)
%     close all
end
