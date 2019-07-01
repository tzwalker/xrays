%% hexscatter code, easy :)
% be sure both XBIC and XBIV arrays are in the workspace
% right now the code is congigured for XBIC and Cu; it does not use the
% XBIV scans

% i have an additional structure object '.stats' that you will not have
% replace the 'xrf.(XBIC_scans{i}).stats.Cu.arr_corr;' with something
% resembling the structure navigation syntax of the old code, i.e:
% 'xrf.(XBIC_scans{i}).Cu.arr_corr;'

close all
clc

samplename = {'NBL3-2', 'NBL3-3', 'TS58A'};

XBIV_scans = {'scan551', 'scan472', 'scan440'};       
XBIC_scans = {'scan550', 'scan475', 'scan439'};


% to plot everythin on the same x and y scale:
% initialize arrays in which to store the max values found in each scan
max_x_array = size(XBIV_scans, 2);
max_y_array = size(XBIV_scans, 2);
for i = 1:length(samplename)
    x = xrf.(XBIC_scans{i}).stats.Cu.arr_corr;
    y = xrf.(XBIC_scans{i}).stats.XBIC_scale.arr;
    
    max_x = max(x); % find max
    max_x_array(i) = max_x; % add max to array
    max_y = max(y);
    max_y_array(i) = max_y;
    
end

title_size = 20; %font size for title
lab_size = 18; %font size for labels and axis ticks
for i = 1:length(XBIV_scans)
    figure(i)
    x = xrf.(XBIC_scans{i}).stats.Cu.arr_corr;
    y = xrf.(XBIC_scans{i}).stats.XBIC_scale.arr;
    
    hexscatter(x,y)
    
    xlim([0 max(max_x_array)]) % use maximum of all scans as scale limit
    ylim([0 max(max_y_array)])
    box on
    
    pltname = sprintf('%s', samplename{i});
    title(pltname, 'fontsize', title_size);
   
    ax = gca;
    ax.FontSize = lab_size;
    xlabel('Cu (\mu/cm^{2})', 'fontsize', lab_size); % REMEMBER change x/y axis titles accordingly
    ylabel('XBIC (A)', 'fontsize', lab_size);
    
    %comment this last part out if you do not want to save the figures ot a
    %destination folder
    filename = sprintf("%s, hex Cu_XBIC.jpg", samplename{i});
    plotpath = fullfile('C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190613_new plots for old scans\', filename); %Specificy path in quotes
    saveas(gcf,  plotpath)
end

close all