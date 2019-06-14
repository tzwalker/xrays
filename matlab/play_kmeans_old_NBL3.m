close all
clc

medCu = xrf.scan550.stats.Cu.arr_corr;

clustered_channel = kmeans(medCu, 4);

rawYpos = xrf.scan550.stats.yPosition.raw;
rawXNo = xrf.scan550.stats.yPixelNo.raw;
rawYNo = xrf.scan550.stats.xPixelNo.raw;
[x, y, map] = map_array(rawYpos, medCu, rawXNo, rawYNo);
[x1, y1, c_map] = map_array(rawYpos, clustered_channel, rawXNo, rawYNo);

figure(1)
surface(x,y, map, 'LineStyle', 'none')
axis square

xlabel('X position (\mum)', 'fontsize', 12);
ylabel('Y position (\mum)', 'fontsize', 12);


z = colorbar;
%z.FontSize = 12;
%z.TickLabelInterpreter = 'latex';
leg_label = 'A';
ylabel(z, leg_label, 'fontsize', 12);

figure(2)
surface(x,y, c_map, 'LineStyle', 'none')
axis square

xlabel('X position (\mum)', 'fontsize', 12);
ylabel('Y position (\mum)', 'fontsize', 12);


z = colorbar;
%z.FontSize = 12;
%z.TickLabelInterpreter = 'latex';
leg_label = 'group #';
ylabel(z, leg_label, 'fontsize', 12);