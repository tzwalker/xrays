clear
clc
close all

%File Directory
path  = 'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\output\';
scanlist = {'343', '416', '264', '385'};                   %sector 26 scans must be a 3 digit number
samplename = {'NBL3-1', 'NBL3-2', 'NBL3-3', 'TS58A'};      %Corresponding names of samples for each scan
beamenergy = {12.7 12.7 12.7 12.7 12.7 12.7 12.7 12.7};                     %incident energy for each scan
beamtheta = {75 75 75 75 75 75 75 75};                              %beam measurement geometry
detectortheta = {15 15 15 15 15 15 15 15};                          %sample measurement geometry

absorber_thickness = {5.845E-4, 5.845E-4, 8.515E-4, 8.515E-4, 7.744E-4, 7.744E-4, 5.319E-4, 5.319E-4};  %cm, to be entered into CdTe_Absorb()
Cu_thickness = {0.5E-7, 0.5E-7, 2.5E-7, 2.5E-7, 10E-7, 10E-7, 2.5E-7, 2.5E-7};      %cm, estimate for preliminary works

%IN PROGRESS: following polynomials fitted form third-party SIMS data using OriginPro
NBL31_Cu_grad = @(x) 18.360 -4.409*x +25.488*x.^2 -35.406*x.^3 +22.28*x.^4 -7.637*x.^5 +1.533*x.^6 -0.179*x.^7 +0.0114*x.^8 -(3.010E-4)*x.^9;      %atoms/cm^3, x in um
NBL32_Cu_grad = @(x) 17.870 -2.674*x +16.920*x.^2 -18.764*x.^3 +9.213*x.^4 -2.474*x.^5 +0.389*x.^6 -0.359*x.^7 +0.0018*x.^8 -(3.772E-5)*x.^9;     %atoms/cm^3, x in um
NBL33_Cu_grad = @(x) 19.251 -5.325*x +22.107*x.^2 -23.715*x.^3 +11.765*x.^4 -3.231*x.^5 +0.522*x.^6 -0.0497*x.^7 +0.00258*x.^8 -(5.619E-5)*x.^9;     %atoms/cm^3, x in um
TS58A_Cu_grad = @(x) 19.929 -9.325*x +37.204*x.^2 -45.885*x.^3 +27.219*x.^4 -9.067*x.^5 +1.784*x.^6 -0.206*x.^7 + 0.0128*x.^8 -(3.324E-4)*x.^9;    %atoms/cm^3, x in um

Cu_gradient = {NBL31_Cu_grad,NBL31_Cu_grad, NBL32_Cu_grad,NBL32_Cu_grad, NBL33_Cu_grad,NBL33_Cu_grad, TS58A_Cu_grad,TS58A_Cu_grad};

stanford = {5000,5000, 5000,5000, 5000,5000, 50, 5000};                  %stanford setting (convert to nA/V) for each scan
beamconversion = {200000 200000 200000 200000 200000 200000 200000 200000};     %beam scalar conversion (cts/V)
lock_in = {500,500, 500,500, 500,500, 10000,10000};                        %lock in amplification for each scan (V/V)

flux = {6.00E8 6.00E8 6.00E8 6.00E8 6.00E8 6.00E8 6.00E8 6.00E8};               %(ph/s)  see PIN diode Excel calc

%%%%%%%%% START FOR LOOP THROUGH ALL SCANS HERE  %%%%%%%%
for N = 1:length(scanlist)
scan = scanlist{1, N};
scanheader = ['scan' scanlist{1, N}];
WORK.samplename = samplename{1, N};

%FILE PATH
file  = [path 'combined_ASCII_2idd_0' scan '.h5.csv'];

WORK = importXRF_arrays(file);
sample = samplename{1, N};

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

%%% Ratio Data: CdTe
WORK.Cd_ratio.arr_mol = WORK.Cd_L.arr_mol ./ (WORK.Cd_L.arr_mol + WORK.Te_L.arr_mol);
WORK.Te_ratio.arr_mol = WORK.Te_L.arr_mol ./ (WORK.Cd_L.arr_mol + WORK.Te_L.arr_mol);

WORK.CuToCd_ratio.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Cd_L.arr_mol);
WORK.CuToTe_ratio.arr_mol = WORK.Cu.arr_mol ./ (WORK.Cu.arr_mol + WORK.Te_L.arr_mol);
WORK.CdToTe_ratio.arr_mol = WORK.Cd_L.arr_mol ./ (WORK.Te_L.arr_mol);

%%% XCE Calculation
%convert from counts to amps
XBIC_scale_factor = ((stanford{N} * 1E-9)  /  (beamconversion{N} * lock_in{N}));   %generate scan electrical scale factor
WORK.XBIC_scale.arr = WORK.ds_ic.raw * XBIC_scale_factor;                   %amperes

%convert from amps to e-h pairs collected
eh_per_coulomb = (1/(1.6E-19));
WORK.XBIC_collected.arr = WORK.XBIC_scale.arr .* eh_per_coulomb;            %e-h

%XBIC_thick: thickness correction raw
WORK.XBIC_thick.arr_corr = WORK.XBIC_scale.arr ./ (WORK.Cd_L.arr_corr + WORK.Te_L.arr_corr);    %A/(ug/cm2)    

%CdTe absorber parameters
E_g = 1.45;                         %eV
alpha = 3;                          %ratio E_ion/E_g

%thickness correction pixel by pixel:   E_abs_XRF
mu_Cd_Beam = 65.2851;                                       %cm2/g (from xraylib)
mu_Te_Beam = 79.1261;                                       %cm2/g (from xraylib)
WORK.Cd_L.arr_corr_gcm2 = WORK.Cd_L.arr_corr .* 1E-6;       %g/cm2
WORK.Te_L.arr_corr_gcm2 = WORK.Te_L.arr_corr .* 1E-6;       %g/cm2
WORK.E_abs_XRF.arr_corr = (beamenergy{N} * 1000) * (1 - exp(- (WORK.Cd_L.arr_corr_gcm2 .* mu_Cd_Beam + WORK.Te_L.arr_corr_gcm2 .* mu_Te_Beam)));

%pix-by-pix flux correction factor
WORK.C_arr = WORK.E_abs_XRF.arr_corr ./ (alpha * E_g); 

%calculate XCE arrays (corr1 = using bulk correction; corr2 = using pix-by-pix)
WORK.XCE.arr_corr2 = WORK.XBIC_collected.arr ./ (WORK.C_arr * flux{N}) * 100;              %as percent     
WORK.XCE_rel.arr_corr2 = WORK.XCE.arr_corr2 ./ max(WORK.XCE.arr_corr2)*100;                %relative percentages of pix-by-pix

%Put the data back into the structure
xrf.(scanheader) = WORK;

end


