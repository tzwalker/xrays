function [raw, stat] = importXRF_arrays(file)

%scan_type is a string indicating whether the exported csv of interest has
%zeros generated by flyscan mode at Argonee Nat'l lab
%these zzeros must be neglected and should not be imported for purposes
%of performing relevant statistical analyses

A = importdata(file);

data = A.data;   %isolate full csv matrix

logic_array = data > 0;                     %find cells with values greater than zero (ture = 1, false = 0)
mark_zeros = ~logic_array;                  %invert logic zeros to logic ones)
count_zeros_in_row = sum(mark_zeros, 2);    %sum logic ones across rows of csv array

%the number of detector channels selected on an export from MAPS = number of columns in the csv
%this implies sum logic ones is dependent on the number of detector channels;
%i've chosen to find the difference between adjacent values in count_zeros_in_row
%to identify the index where the zeros of a fly scan csv begin (and
%therefore where to cut off the data) semi-regardless of the number of detector
%channels selected
cut_off_array = diff(count_zeros_in_row);	%find difference between consecutive summed values
%if the difference between the number of zeros in one row is more than
%twenty, that indicates the beginning of the two dead lines of a flyscan
%(for the most part)
cut_off_index = find(cut_off_array > 20); 

stat_data = data([1:cut_off_index], :);

for i = 1:size(A.colheaders, 2)
    A.colheaders{i} = genvarname(A.colheaders{i});
    eval(['WORK.  ' A.colheaders{i}  '.raw = data(:,i);'])
end

for i = 1:size(A.colheaders, 2)
    A.colheaders{i} = genvarname(A.colheaders{i});
    eval(['STAT.  ' A.colheaders{i}  '.raw = stat_data(:,i);'])
end


%Put the data back into the structure
raw   =  WORK;
stat = STAT;

end

