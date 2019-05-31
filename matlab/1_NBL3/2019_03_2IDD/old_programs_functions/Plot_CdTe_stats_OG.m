%% hex bin plot
close all
clc
scans = {'scan343' 'scan422' 'scan264' 'scan385'};                         %change to scans you've run
sample_names = {'NBL3-1', 'NBL3-2', 'NBL3-3', 'TS58A'};

desired_y_channels = {'XBIC_scale', 'XCE'};                      %for reference within structure, used in surface function
ext = {'arr', 'arr_corr2'};

for i = 1:length(scans)
    scan_Cd = xrf.(scans{i}).Cu_over_CdTe.arr_mol;
    
    for j = 1:length(desired_y_channels)
        figure(j)
        %subplot(2, 1, j);
        
        channel = xrf.(scans{i}).(desired_y_channels{j}).(ext{j});
        hexscatter(scan_Cd, channel);
        axis square
        box on
        pltname = sprintf('%s', sample_names{i});
        title(pltname, 'fontsize', 20);
        ax = gca;
        ax.FontSize = 16;

        xlabel('Cu over CdTe (at. %)','fontsize', 18);
        leg_names = {'XBIC (A)', 'XCE (%)'};
        yname = leg_names{j};
        ylabel(yname,'fontsize', 18);
        filename = sprintf("%s, hex_Cu on CdTe v %s.png", sample_names{i}, desired_y_channels{j});
        plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190501 Q6 reporting newest plots_m\', filename); %Specificy path in quotes
        saveas(gcf,  plotpath)
    end
    close all
end
%%
close all
scans = {'scan343' 'scan422' 'scan264' 'scan385'};                         %change to scans you've run
sample_names = {'NBL3-1', 'NBL3-2', 'NBL3-3', 'TS58A'};

desired_y_channels = {'XBIC_scale',  'XCE', 'Cd_ratio', 'Cd_L','Cu', 'CuToCd_ratio', 'CuToTe_ratio', 'CdToTe_ratio'};                      %for reference within structure, used in surface function
ext = {'arr', 'arr_corr2', 'arr_corr','arr_corr','arr_corr','arr_corr','arr_corr','arr_corr'};

for i = 1:length(scans)
    figure(i)
    XBIC = xrf.(scans{i}).XBIC_scale.arr;
    XCE = xrf.(scans{i}).XCE.arr_corr2;
    Cd_ratio = xrf.(scans{i}).Cd_ratio.arr_mol;
    Cd = xrf.(scans{i}).Cd_L.arr_mol;
    Cu = xrf.(scans{i}).Cu.arr_mol;
    Cu_over_Cd = xrf.(scans{i}).CuToCd_ratio.arr_mol;
    Cu_over_Cd(isinf(Cu_over_Cd)) = 0;
    Cu_over_Te = xrf.(scans{i}).CuToTe_ratio.arr_mol;
    Cd_over_Te = xrf.(scans{i}).CdToTe_ratio.arr_mol;
    
    data =  [XBIC, XCE, Cd_ratio, Cd, Cu];%, Cd_ratio, Cd, Cu, Cu_over_Cd, Cu_over_Te, Cd_over_Te];
    corrplot(data, 'varnames', {'XBIC';     'XCE'; 'Cd Ratio';  'Cd' ;'Cu'})
    title(sprintf('%s', sample_names{i}))
  
    filename = sprintf("%s, corrplot.jpg", sample_names{i});
    plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190403 NBL3_AXOnoInfo\', filename); %Specificy path in quotes
    saveas(gcf,  plotpath)
    close all
end
