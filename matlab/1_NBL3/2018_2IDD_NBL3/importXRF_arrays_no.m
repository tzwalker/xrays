function [output] = importXRF_arrays(file)

A = importdata(file);

for i = 1:size(A.colheaders, 2)
    A.colheaders{i} = genvarname(A.colheaders{i});
    %assignin('base', newData1.colheaders{i}, newData1.data(:,i));
    eval(['WORK.  ' A.colheaders{i}  '.raw = A.data(:,i);'])
end
%WORK = data.(scanheader);
WORK.headers = A.colheaders;

%Put the data back into the structure
output   = WORK;
end
