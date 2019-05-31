function [Cu_grading] = get_sample_Cu_grading(upstream_bound, downstream_bound, Cu_profile)

dt = 1.0E-7;    %cm

range_to_apply_Cu_profile_over = [upstream_bound:dt:downstream_bound];  %cm
range_to_apply_Cu_profile_over =  1E4 * range_to_apply_Cu_profile_over; %um, input to Cu_profile polynomial must be in um

Cu_grading = Cu_profile(range_to_apply_Cu_profile_over);                %atoms/cm3
Cu_grading = Cu_grading * (1/(6.02E23)) * (63.546/1);                   %g/cm3
end