function [Cu_grading] = get_sample_Cu_grading(stack_thickness, Cu_profile)

dt = 0.25E-7;

stack_sublayers = [0:dt:stack_thickness]; %cm, array containing the depth values to be used as input to Cu_profile
stack_sublayers =  1E4 * stack_sublayers; %um, convert to micron; required unit for input to the gaussian obtained from SIMS data

Cu_grading = Cu_profile(stack_sublayers);               %atoms/cm3
Cu_grading = Cu_grading * (1/(6.02E23)) * (63.546/1);   %g/cm3
end