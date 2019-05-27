function [valid_division_array] = check_and_replace_Cd(Cd_channel)

avg_Cd = nanmean(Cd_channel);
std_Cd = nanstd(Cd_channel);

max_data_spread = 3*std_Cd; %%THIS IS NOT A VALID RANGE; returns a negative number, 
%in which case all positive, near-zero numbers still satsify !!!

%non_zero_Cd_min = min(WORK.Cd_ratio.arr_mol(WORK.Cd_ratio.arr_mol > 0));

for i = 1:length(Cd_channel)
    if Cd_channel(i) < avg_Cd - max_data_spread %!!!
        Cd_channel(i) = 0;
        
    elseif Cd_channel(i) > avg_Cd + max_data_spread
        Cd_channel(i) = avg_Cd;
        
    end
max(Cd_channel)
min(Cd_channel(Cd_channel > 0))
nanmean(Cd_channel)

valid_division_array = Cd_channel;

end