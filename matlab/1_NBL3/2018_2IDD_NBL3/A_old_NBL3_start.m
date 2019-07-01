clear
clc
close all

%File Directory
path  = 'C:\Users\Trumann\Desktop\2017_12_2018_07_NBL3_bacth_refit\output\';
scanlist = {'550','475', '439', '551', '472', '440'};                   %sector 26 scans must be a 3 digit number
samplename = {'NBL3_2' 'NBL3_3' 'TS58A','NBL3_2' 'NBL3_3' 'TS58A'};      %Corresponding names of samples for each scan
beamenergy = {8.99 8.99 8.99 8.99 8.99 8.99 8.99 8.99};                     %incident energy for each scan
beamtheta = {90 90 90 90 90 90 90 90};                              %beam measurement geometry
detectortheta = {47 47 47 47 47 47 47 47};                          %sample measurement geometry

absorber_thickness = {8.515E-4, 7.744E-4, 5.845E-4, 8.515E-4, 7.744E-4, 5.845E-4};          %(cm) average thickness derived from SIMS
Cu_constant_thickness = {2.5E-7 10E-7, 2.5E-7, 2.5E-7 10E-7, 2.5E-7};

beamconversion = {2E5 1E5 1E5 2E5 1E5 1E5};     %(cts/V) beam scalar conversion

XBIC = {1,1,1, 0,0,0}; %activate or deactivate depending on whether the scan was XBIC or XBIV
stanford = {50000, 200, 200};                  %(nA/V) stanford setting (convert to nA/V) for each scan
lock_in = {100, 20, 20};                        %(V/V) lock in amplification for each scan (V/V)
flux = {3.37E9 3.37E9 1.57E9};               %(ph/s)  see PIN diode Excel calc
E_abs = {4368 3571 4581};                      %(eV) from Beer-Lambert of whole absorber

lock_in_V = {1, 1, 1, 1E4, 1E5, 1E5};


%%%%%%%%% START FOR LOOP THROUGH ALL SCANS HERE  %%%%%%%%
for N = 1:length(scanlist)
scan = scanlist{1, N};
scanheader = ['scan' scanlist{1, N}];

%FILE PATH
file  = [path 'combined_ASCII_2idd_0' scan '.h5.csv'];

[WORK, STAT] = importXRF_arrays(file);
sample = samplename{1, N};

%%% Absorb Correction and Application
[iio_cd, iio_te, iio_cu] = CdTe_Cu_Edge_Abosrb_orignal(beamenergy{N}, beamtheta{N}, detectortheta{N}, absorber_thickness{N}, Cu_constant_thickness{N});              
WORK.L_ele_IIO = [iio_cd iio_te];
WORK.K_ele_IIO = [iio_cu];

%Enter elements to map (number of elements here should equal the number of elements corrected for in Absorb)
ele_L_lines = {'Cd_L', 'Te_L'};                                     %L-line elements run through L-line for loop
ele_K_lines = {'Cu'};                                               %K-line elements run through L-line for loop

%Enter element MW (in same position)
ele_MW = [122.411 127.6 63.546]; %Cl:35.453
L_corr = 0.6;                                                                           %L_line quantification correction
for i = 1:length(WORK.L_ele_IIO)
    WORK.(ele_L_lines{i}).arr_corr = WORK.(ele_L_lines{i}).raw/ (WORK.L_ele_IIO(i)) * L_corr; %data in ug/cm2 corrected for attenuation
    WORK.(ele_L_lines{i}).arr_mol = WORK.(ele_L_lines{i}).arr_corr/ ele_MW(i) * 1E-6;
    STAT.(ele_L_lines{i}).arr_corr =  STAT.(ele_L_lines{i}).raw/ (WORK.L_ele_IIO(i)) * L_corr; %enter corrected values into STAT structure as well
    STAT.(ele_L_lines{i}).arr_mol = WORK.(ele_L_lines{i}).arr_corr/ ele_MW(i) * 1E-6;
end

for i = 1:length(WORK.K_ele_IIO)
    WORK.(ele_K_lines{i}).arr_corr = WORK.(ele_K_lines{i}).raw/ (WORK.K_ele_IIO(i)); %data in ug/cm2 corrected for attenuation
    WORK.(ele_K_lines{i}).arr_mol = WORK.(ele_K_lines{i}).arr_corr/ ele_MW(i) * 1E-6;
    STAT.(ele_K_lines{i}).arr_corr = STAT.(ele_K_lines{i}).raw/ (WORK.K_ele_IIO(i)); %data in mol/cm2 corrected for attenuation
    STAT.(ele_K_lines{i}).arr_mol = STAT.(ele_K_lines{i}).arr_corr/ ele_MW(i) * 1E-6;
end

%%% Ratio Data: CdTe
WORK.Cd_ratio.arr_corr = WORK.Cd_L.arr_corr ./ (WORK.Cd_L.arr_corr + WORK.Te_L.arr_corr);
WORK.Te_ratio.arr_corr = WORK.Te_L.arr_corr ./ (WORK.Cd_L.arr_corr + WORK.Te_L.arr_corr);

WORK.CdToTe_ratio.arr_corr = WORK.Cd_L.arr_corr ./ (WORK.Te_L.arr_corr);


if XBIC{N} == 1
    %%% XCE Calculation
    %convert from counts to amps
    XBIC_scale_factor = ((stanford{N} * 1E-9)  /  (beamconversion{N} * lock_in{N}));   %generate scan electrical scale factor
    WORK.XBIC_scale.arr = WORK.ds_ic.raw * XBIC_scale_factor;                   %amperes
    STAT.XBIC_scale.arr = STAT.ds_ic.raw * XBIC_scale_factor;
else
    XBIV_scale_factor = 1 / (beamconversion{N} * lock_in_V{N});
    WORK.XBIV_scale.arr = WORK.ds_ic.raw * XBIV_scale_factor;
    STAT.XBIV_scale.arr = STAT.ds_ic.raw * XBIV_scale_factor;
end



% %convert from amps to e-h pairs collected
% eh_per_coulomb = (1/(1.6E-19));
% WORK.XBIC_collected.arr = WORK.XBIC_scale.arr .* eh_per_coulomb;            %e-h
% 
% %XBIC_thick: thickness correction raw
% WORK.XBIC_thick.arr_corr = WORK.XBIC_scale.arr ./ (WORK.Cd_L.arr_corr + WORK.Te_L.arr_corr);    %A/(ug/cm2)    
% 
% 
% %CdTe absorber parameters
% E_g = 1.45;                         %eV
% alpha = 3;                          %ratio E_ion/E_g
% rho_CdTe = 5.85;                    %g/cm3
% 
% %bulk flux correction factor:             E_abs_z
% C = E_abs{N} / (E_g * alpha);
% 
% 
% %thickness correction pixel by pixel:   E_abs_XRF
% mu_Cd_Beam = 165.132;                               %cm2/g (from xraylib)
% mu_Te_Beam = 198.658;                               %cm2/g (from xraylib)
% 
% WORK.Cd_L.arr_corr_gcm2 = WORK.Cd_L.arr_corr .* 1E-6;       %g/cm2
% WORK.Te_L.arr_corr_gcm2 = WORK.Te_L.arr_corr .* 1E-6;       %g/cm2
% 
% WORK.E_abs_XRF_try.arr_corr = (beamenergy{N} * 1000) * (1 - exp(- (rho_CdTe./(WORK.Cd_L.arr_corr_gcm2 + WORK.Te_L.arr_corr_gcm2) * absorber_thickness{N})));
% WORK.E_abs_XRF.arr_corr = (beamenergy{N} * 1000) * (1 - exp(- (WORK.Cd_L.arr_corr_gcm2 .* mu_Cd_Beam + WORK.Te_L.arr_corr_gcm2 .* mu_Te_Beam)));
% 
% %pix-by-pix flux correction factor
% WORK.C_arr = WORK.E_abs_XRF.arr_corr ./ (alpha * E_g); 
% 
% 
% %calculate XCE arrays (corr1 = using bulk correction; corr2 = using pix-by-pix)
% WORK.XCE.arr_corr1 = WORK.XBIC_collected.arr ./ (C * flux{N}) * 100;
% WORK.XCE.arr_corr2 = WORK.XBIC_collected.arr ./ (WORK.C_arr * flux{N}) * 100;              %as percent     
% 
% WORK.XCE_rel.arr_corr1 = WORK.XCE.arr_corr1 ./ max(WORK.XCE.arr_corr1)*100;           %relative percentages of bulk
% WORK.XCE_rel.arr_corr2 = WORK.XCE.arr_corr2 ./ max(WORK.XCE.arr_corr2)*100;           %relative percentages of pix-by-pix
% 
% %Put the data back into the structure
 xrf.(scanheader).whole = WORK;
 xrf.(scanheader).stats = STAT;

end


