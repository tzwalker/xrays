clear
clc

f = 'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\output\combined_ASCII_2idd_0385.h5.csv';

A = importdata(f);

data = A.data;

logic_array = data > 0;
mark_zeros = ~logic_array;
count_zeros_in_row = sum(mark_zeros, 2);

cut_off_array = diff(count_zeros_in_row);
cut_off_index = find(cut_off_array > 20);

stat_data = data([1:cut_off_index], :);


%help from online, this guy is awesome: https://www.mathworks.com/matlabcentral/answers/383918-delete-a-row-if-it-contains-a-specific-number-of-zeros
% % Sample Array
% OriginalVector = [1 2 3 0; 1 0 0 0 ; 3 4 0 0]
% %Create Logical Array
% CreateLogicalArray = OriginalVector > 0
% ArrayWithZeroPositionsMarked = ~CreateLogicalArray
% CountNoOfZerosInOriginalArray = sum(ArrayWithZeroPositionsMarked, 2)
% 
% % If you want rows with more than 3 
% FindRowsWithZerosLargerThan = CountNoOfZerosInOriginalArray > 2;
% FindRowsWithZerosLargerThan
% DesiredVectorWithElimiatedRows = OriginalVector(~FindRowsWithZerosLargerThan, :) 

