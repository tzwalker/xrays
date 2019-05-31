function [output] = importXBIV_array(file)

A = importdata(file);

for i = 1:size(A.colheaders, 2)
    tf = strcmp(A.colheaders{i}, ' ds_ic');
    if tf == 1
        XBIV_array = A.data(:,i);
    end
    
end

output   = XBIV_array;
end
