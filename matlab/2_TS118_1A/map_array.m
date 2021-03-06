function [rel_X, rel_Y, mapped_channel] = map_array(y_position_mm, data_to_map, y, x)

%convert all NaN to zeros(i.e. for those pixels where 0/0 occurs; 
%flyscans always have zeros for last two columns)
%will make separate function that scales the colorbar "get_cbar_scale()"
%data_to_map(isnan(data_to_map)) = 0;
%data_to_map(isinf(data_to_map)) = 0;    

%shape data according to index of x and y pixels
mapped_channel = reshape(data_to_map, [max(y)+1, max(x)+1]);


%calculate step distance (in um) based off motor position
del_y = abs(y_position_mm(2,1) - y_position_mm(1,1)) * 1000;       %difference of y motor position (mm) to um

%contruct x and y micron arrays
pre_rel_Y = y * del_y;                                             %make array of converted y coordinates (ypixel * step)
pre_rel_X = x * del_y;                                             %make array of converted y coordinates (ypixel * step)

%shape x and y micron arrays to provide indices unto which mapped_channel will be mapped
rel_Y = reshape(pre_rel_Y, [max(y)+1, max(x)+1]);                  %shape array containing correct units 
rel_X = reshape(pre_rel_X, [max(y)+1, max(x)+1]);                  %shape array containing correct units 

end
