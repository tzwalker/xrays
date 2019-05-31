close all

%generate cell array containing scan number structures (the fields in 'xrf' structure)
%this array will be used to help iterate through the xrf structure
fields = fieldnames(xrf); 

for i = 1:numel(fields)
    figure(i)
    %subplot(1,2,1)
    amp = xrf.(fields{i}).XBIC_scale.arr; %extract electrical array of the scan

% [x,y,amp_cluster_map] = map_array(WORK.yPosition.raw, amp_cluster, WORK.yPixelNo.raw, WORK.xPixelNo.raw);
% surface(x, y, amp_cluster_map, 'LineStyle', 'none')
% axis equal; newdata = amp(~isnan(amp));
    
    
    %enter array where zeros are changed to nan before calling hist()
    hist()
    
end