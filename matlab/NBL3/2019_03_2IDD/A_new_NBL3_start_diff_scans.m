clear
clc
close all

%File Directory
path  = 'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\output\';

beamenergy = {12.7 12.7 12.7};                          %incident energy for each scan
beamtheta = {75 75 75};                                 %beam measurement geometry
detectortheta = {15 15 15};                             %sample measurement geometry
beamconversion = {200000 200000 200000};                %beam scalar conversion (cts/V)
flux = {6.00E8 6.00E8 6.00E8};                          %(ph/s)  see PIN diode Excel calc

absorber_thickness = {8.515E-4, 7.744E-4, 5.319E-4};  %cm, to be entered into CdTe_Absorb()
Cu_thickness = {2.5E-7, 10E-7, 2.5E-7};      %cm, estimate for preliminary works

%IN PROGRESS: following polynomials fitted form third-party SIMS data using OriginPro
NBL31_Cu_grad = @(x) 18.360 -4.409*x +25.488*x.^2 -35.406*x.^3 +22.28*x.^4 -7.637*x.^5 +1.533*x.^6 -0.179*x.^7 +0.0114*x.^8 -(3.010E-4)*x.^9;      %atoms/cm^3, x in um
NBL32_Cu_grad = @(x) 17.870 -2.674*x +16.920*x.^2 -18.764*x.^3 +9.213*x.^4 -2.474*x.^5 +0.389*x.^6 -0.359*x.^7 +0.0018*x.^8 -(3.772E-5)*x.^9;     %atoms/cm^3, x in um
NBL33_Cu_grad = @(x) 19.251 -5.325*x +22.107*x.^2 -23.715*x.^3 +11.765*x.^4 -3.231*x.^5 +0.522*x.^6 -0.0497*x.^7 +0.00258*x.^8 -(5.619E-5)*x.^9;     %atoms/cm^3, x in um
TS58A_Cu_grad = @(x) 19.929 -9.325*x +37.204*x.^2 -45.885*x.^3 +27.219*x.^4 -9.067*x.^5 +1.784*x.^6 -0.206*x.^7 + 0.0128*x.^8 -(3.324E-4)*x.^9;    %atoms/cm^3, x in um

Cu_gradient = {NBL32_Cu_grad, NBL33_Cu_grad, TS58A_Cu_grad};

samplename = {'NBL3_2', 'NBL3_3', 'TS58A'};         %Corresponding names of samples for each scan
XRF_scans = {'422', '266', '385'};                            
XRF_scanType = {'flyscan', 'flyscan', 'flyscan'};
%NOTE: scan numbers in 'XRF_scans' are the heading for the home structure of all (XRF,XBIC, XBIV) scans      
%electrical scans generally have a short dwell time, and therefore less XRF
%signal; therefore the XRF scan numbers will be used to generate the
%headers within the home 'xrf' structure, and the separate XBIV and XRF
%arrays will be thrown into there. 
%Note that one needs to be wary of the
%different scan settings used for an exclusively electrical or XRF scan,
%and any sort of physical drift between scans will ruin pixel-pixel
%correlation. However, XBIC and XRF are almost always collected together.
%The reason for separating the scans was the notable decay in XBIC signal as the measurement was performed.
XBIV_scans = {'419', '263', '382'};
XBIC_scans = {'416', '260', '378'};


XRF_stanford = {5000, 5000, 5000};                  %stanford setting (convert to nA/V) for each scan
XRF_lock_in = {500, 500, 10000};                    %lock in amplification for each scan (V/V)

XBIC_stanford = {5000, 5000, 50};
XBIC_lock_in = {500, 500, 10000};

XBIV_lock_in = {10000, 1000, 1000};


%%%%%%%%% START FOR LOOP THROUGH ALL SCANS HERE  %%%%%%%%
for N = 1:length(XRF_scans)
scanheader = ['scan' XRF_scans{1, N}];                      %NOTE: this is the line that gereneates the header name within the home 'xrf' structure, using the fluorescence scans because they have more usable data


%%% Import XRF scan
XRFscan = XRF_scans{1, N};
xrffile  = [path 'combined_ASCII_2idd_0' XRFscan '.h5.csv'];
WORK = importXRF_arrays(xrffile);

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



%%% Absorb Correction and Application
[iio_mo, iio_zn, iio_cd, iio_te, iio_sn, iio_cu] = CdTe_Se_Edge_Absorb(beamenergy{N}, beamtheta{N}, detectortheta{N}, absorber_thickness{N}, Cu_gradient{N}, Cu_thickness{N});              
WORK.L_ele_IIO = [iio_mo, iio_cd, iio_te, iio_sn];
WORK.K_ele_IIO = [iio_zn, iio_cu];

%Enter elements to map (number of elements here should equal the number of elements corrected for in Absorb)
ele_L_lines = {'Mo_L', 'Cd_L', 'Te_L', 'Sn_L'};               %L-line elements run through L-line for loop
ele_K_lines = {'Zn', 'Cu'};                                   %K-line elements run through K-line for loop

%Enter element MW (in same position)
ele_L_MW = [95.94, 122.411, 127.6, 118.71];         %g/mol
ele_K_MW = [65.38, 63.546];                         %g/mol

L_corr = 0.6;                                       %L_line quantification correction
for i = 1:length(WORK.L_ele_IIO)
    WORK.(ele_L_lines{i}).arr_corr = WORK.(ele_L_lines{i}).raw / (WORK.L_ele_IIO(i)) * L_corr; %data in ug/cm2 corrected for attenuation
    WORK.(ele_L_lines{i}).arr_mol = WORK.(ele_L_lines{i}).arr_corr / ele_L_MW(i) * 1E-6;         %data in mol/cm2 corrected for attenuation
end

for i = 1:length(WORK.K_ele_IIO)
    WORK.(ele_K_lines{i}).arr_corr = WORK.(ele_K_lines{i}).raw/ (WORK.K_ele_IIO(i)); %data in ug/cm2 corrected for attenuation
    WORK.(ele_K_lines{i}).arr_mol = WORK.(ele_K_lines{i}).arr_corr/ ele_L_MW(i) * 1E-6;         %data in mol/cm2 corrected for attenuation
end

%Cd_qnt_mean = nzmean(WORK.Cd_L.arr_corr);
%Te_qnt_mean = nzmean(WORK.Te_L.arr_corr);

%%% Ratio Data: CdTe
WORK.Cd_ratio.arr_mol = WORK.Cd_L.arr_mol ./ (WORK.Cd_L.arr_mol + WORK.Te_L.arr_mol);
WORK.Te_ratio.arr_mol = WORK.Te_L.arr_mol ./ (WORK.Cd_L.arr_mol + WORK.Te_L.arr_mol);

WORK.CuToCd_ratio.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Cd_L.arr_mol);
WORK.CuToTe_ratio.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Te_L.arr_mol);
WORK.Cu_over_CdTe.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Te_L.arr_mol);
WORK.CdToTe_ratio.arr_mol = WORK.Cd_L.arr_mol ./ (WORK.Te_L.arr_mol);


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


