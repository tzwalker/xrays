clear
clc
close all

%File Directory
path  = 'C:\Users\Trumann\Desktop\2018_11_26IDC_XBIC_decay\';

beamenergy = {10.4 10.4 10.4};                          %incident energy for each scan
beamtheta = {75 75 75};                                 %beam measurement geometry
detectortheta = {15 15 15};                             %sample measurement geometry
beamconversion = {100000 100000 100000};                %beam scalar conversion (cts/V)
flux = {3.42E8 2.52E6 2.52E6};                          %(ph/s)  see PIN diode Excel calc

absorber_thickness = {5.0E-4, 5.0E-4, 5.0E-4};  %cm

samplename = {'TS118_1A'};         %Corresponding names of samples for each scan
scans = {'195', '196', '197'};                            

XRF_stanford = {20, 20, 20};                  %stanford setting (convert to nA/V) for each scan
XRF_lock_in = {1000, 5, 1000};                    %lock in amplification for each scan (V/V)

%%%%%%%%% START FOR LOOP THROUGH ALL SCANS HERE  %%%%%%%%
for N = 1:length(scans)
scanheader = ['scan' scans{1, N}];                      %NOTE: this is the line that gereneates the header name within the home 'xrf' structure, using the fluorescence scans because they have more usable data

%%% Import XRF scan
scan = scans{1, N};
xrffile  = [path 'combined_ASCII_26idbSOFT_0' scan '.h5.csv'];
WORK = importXRF_arrays(xrffile); %20190605 referencing custom function in 2019_032IDD that makes STAT data as well

%%% Import XBIV scan
% XBIVscan = XBIV_scans{1, N};
% xbiv_file  = [path 'combined_ASCII_2idd_0' XBIVscan '.h5.csv'];
% WORK.XBIV.raw = import_electrical_array(xbiv_file);
% XBIV_scale_factor = XBIV_lock_in{N} * beamconversion{N};
% WORK.XBIV_scale.arr = WORK.XBIV.raw / XBIV_scale_factor;


%%% Import XBIC scan
% XBICscan = XBIC_scans{1, N};
% xbic_file  = [path 'combined_ASCII_2idd_0' XBICscan '.h5.csv'];
% WORK.XBIC.raw = import_electrical_array(xbic_file);
% XBIC_scale_factor1 = (XBIC_stanford{N} * 1E-9)  /  (beamconversion{N} * XBIC_lock_in{N});
% WORK.XBIC_scale_solo.arr = WORK.XBIC.raw * XBIC_scale_factor1;

% %%% Absorb Correction and Application
% [iio_mo, iio_zn, iio_cd, iio_te, iio_sn, iio_cu] = CdTe_Ga_Edge_Absorb(beamenergy{N}, beamtheta{N}, detectortheta{N}, absorber_thickness{N});              
% WORK.L_ele_IIO = [iio_mo, iio_cd, iio_te, iio_sn];
% WORK.K_ele_IIO = [iio_zn, iio_cu];
% 
% %Enter elements to map (number of elements here should equal the number of elements corrected for in Absorb)
% ele_L_lines = {'Cd_L', 'Te_L', 'Sn_L'};               %L-line elements run through L-line for loop
% ele_K_lines = {'Zn', 'Cu'};                                   %K-line elements run through K-line for loop
% 
% %Enter element MW (in same position)
% ele_L_MW = [95.94, 122.411, 127.6, 118.71];         %g/mol
% ele_K_MW = [65.38, 63.546];                         %g/mol
% 
% L_corr = 0.6;                                       %L_line quantification correction
% for i = 1:length(WORK.L_ele_IIO)
%     WORK.(ele_L_lines{i}).arr_corr = WORK.(ele_L_lines{i}).raw / (WORK.L_ele_IIO(i)) * L_corr; %data in ug/cm2 corrected for attenuation
%     WORK.(ele_L_lines{i}).arr_mol = WORK.(ele_L_lines{i}).arr_corr / ele_L_MW(i) * 1E-6;         %data in mol/cm2 corrected for attenuation
% end
% 
% for i = 1:length(WORK.K_ele_IIO)
%     WORK.(ele_K_lines{i}).arr_corr = WORK.(ele_K_lines{i}).raw/ (WORK.K_ele_IIO(i)); %data in ug/cm2 corrected for attenuation
%     WORK.(ele_K_lines{i}).arr_mol = WORK.(ele_K_lines{i}).arr_corr/ ele_L_MW(i) * 1E-6;         %data in mol/cm2 corrected for attenuation
% end
% 
% %Cd_qnt_mean = nzmean(WORK.Cd_L.arr_corr);
% %Te_qnt_mean = nzmean(WORK.Te_L.arr_corr);
% 
% %%% Ratio Data: CdTe
% WORK.Cd_ratio.arr_mol = WORK.Cd_L.arr_mol ./ (WORK.Cd_L.arr_mol + WORK.Te_L.arr_mol);
% WORK.Te_ratio.arr_mol = WORK.Te_L.arr_mol ./ (WORK.Cd_L.arr_mol + WORK.Te_L.arr_mol);
% 
% WORK.CuToCd_ratio.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Cd_L.arr_mol);
% WORK.CuToTe_ratio.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Te_L.arr_mol);
% WORK.Cu_over_CdTe.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Te_L.arr_mol);
% WORK.CdToTe_ratio.arr_mol = WORK.Cd_L.arr_mol ./ (WORK.Te_L.arr_mol);


%%% XCE Calculation
%convert from counts to amps
XBIC_scale_factor2 = ((XRF_stanford{N} * 1E-9)  /  (beamconversion{N} * XRF_lock_in{N}));   %generate scan electrical scale factor
WORK.XBIC_scale.arr = WORK.ds_ic.raw * XBIC_scale_factor2;                           %amperes

% %convert from amps to e-h pairs collected
% eh_per_coulomb = (1/(1.6E-19));
% WORK.XBIC_collected.arr = WORK.XBIC_scale.arr .* eh_per_coulomb;            %e-h
% 
% %XBIC_thick: thickness correction raw
% WORK.XBIC_thick.arr_corr = WORK.XBIC_scale.arr ./ (WORK.Cd_L.arr_corr + WORK.Te_L.arr_corr);    %A/(ug/cm2)    
% 
% %CdTe absorber parameters
% E_g = 1.45;                         %eV
% alpha = 3;                          %ratio E_ion/E_g
% 
% %thickness correction pixel by pixel:   E_abs_XRF
% mu_Cd_Beam = 65.2851;                                       %cm2/g (from xraylib)
% mu_Te_Beam = 79.1261;                                       %cm2/g (from xraylib)
% WORK.Cd_L.arr_corr_gcm2 = WORK.Cd_L.arr_corr .* 1E-6;       %g/cm2
% WORK.Te_L.arr_corr_gcm2 = WORK.Te_L.arr_corr .* 1E-6;       %g/cm2
% WORK.E_abs_XRF.arr_corr = (beamenergy{N} * 1000) * (1 - exp(- (WORK.Cd_L.arr_corr_gcm2 .* mu_Cd_Beam + WORK.Te_L.arr_corr_gcm2 .* mu_Te_Beam)));
% 
% %pix-by-pix flux correction factor
% WORK.C_arr = WORK.E_abs_XRF.arr_corr ./ (alpha * E_g); 
% 
% %calculate XCE arrays (corr1 = using bulk correction; corr2 = using pix-by-pix)
% WORK.XCE.arr_corr2 = WORK.XBIC_collected.arr ./ (WORK.C_arr * flux{N}) * 100;              %as percent     
% WORK.XCE_rel.arr_corr2 = WORK.XCE.arr_corr2 ./ max(WORK.XCE.arr_corr2)*100;                %relative percentages of pix-by-pix

%Put the data back into the structure
xrf.(scanheader) = WORK;

end


