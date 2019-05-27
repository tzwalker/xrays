function [mean_without_zeros] = nzmean(M)

mean_without_zeros = mean(M(M>0));

end