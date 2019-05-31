function [upper, lower] = get_colorbar_scale(channel_that_was_mapped, num_of_std_deviations)
    
    %mean and std_dev of channel array are found, and the bounds for caxis are returned
    
    %for absorber with low XRF, XCE pix-by-pix will divide by 0 --> "inf" occurs
    %for last two columns of flyscan 0/0 occurs --> "nan" occurs
    
   
    %not a very solid way to do this, how about any values more than x5 the
    %std_dev will be set ot the average?
    %channel_that_was_mapped(isnan(channel_that_was_mapped)) = 0;  
    %channel_that_was_mapped(isinf(channel_that_was_mapped)) = nan;
    channel_max = max(channel_that_was_mapped);
    
%     if channel_max == 1
%         observation_to_exclude = channel_max;
%         count_obs_to_exclude = sum(channel_that_was_mapped == observation_to_exclude);
%         contribution_of_obs_to_exclude = count_obs_to_exclude * observation_to_exclude;
%         count_obs_remaining = size(channel_that_was_mapped,1) - count_obs_to_exclude;
%         
%         channel_sum = nansum(channel_that_was_mapped)
%         average_of_channel = (channel_sum - contribution_of_obs_to_exclude) / count_obs_remaining;
%     else
%         average_of_channel = nanmean( channel_that_was_mapped );
%     end

    average_of_channel = nanmean( channel_that_was_mapped );
    standard_deviation_of_channel = nanstd( channel_that_was_mapped );
    
    lower = average_of_channel - num_of_std_deviations * standard_deviation_of_channel;
    upper = average_of_channel + num_of_std_deviations * standard_deviation_of_channel;
    
    if lower < 0
        lower = 0;
    end

end
