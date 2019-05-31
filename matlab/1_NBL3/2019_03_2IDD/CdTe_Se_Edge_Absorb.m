function [fMo, fZn, fCd_CdTe, fTe_CdTe, fSn, fCu] = CdTe_Se_Edge_Absorb(beam_energy, beamtheta, detectortheta, absorber_thickness, Cu_profile, Cu_thickness)

rad_beam = sin(beamtheta*pi/180);       %convert to radians
rad_det = sin(detectortheta*pi/180);    %convert to radians

%capture cross-sections

%Set Mo info
mu_Mo_MoL = 683.7817;               %from xraylib
mu_Mo_ZnK = 127.2039;               %from xraylib
mu_Mo_CuK = 154.9601;
mu_Mo_CdL = 1872.8;
mu_Mo_TeL = 1212.0;
mu_Mo_SnL = 1417.8148;              %from xraylib

%Set ZnTe info
mu_ZnTe_ZnK = 162.0073;             %from xraylib
mu_ZnTe_CuK = 196.3259;
mu_ZnTe_CdL = 680.0102;
mu_ZnTe_TeL = 437.554;
mu_ZnTe_SnL = 512.3745;             %from xraylib

%Set Cu info
mu_Cu_CdL = 695.4808;
mu_Cu_TeL =  440.4480;
mu_Cu_CuK = 51.8756;

%Set CdTe info
mu_CdTe_CuK  = 2.454E2;         %cm2/g
mu_CdTe_CdL  = 566.2543;        %cm2/g
mu_CdTe_TeL  = 8.372E2;         %cm2/g
mu_CdTe_SnL = 434.3490;         %from xraylib

%Set CdS info
mu_CdS_CuK = 1.933E2;           %cm2/g
mu_CdS_CdL = 657.7857;          %cm2/g
mu_CdS_SK = 1138.4054;          %from xraylib
mu_CdS_SnL = 507.4152;          %from xraylib

%Set SnO2 info 
mu_SnO2_SnL = 372.3897675032209;

%beamenergy == 12.7 keV
%values shown are taken from the python library xraylib
mu_Mo_Beam =    44.747540405670364;                 %cm2/g
mu_ZnTe_Beam =  95.21922225854857;                 %cm2/g
mu_Cu_Beam =    116.56270444159746;                 %cm2/g
mu_CdTe_Beam=   72.64365282865865;                 %cm2/g
mu_CdS_Beam =   56.377215016334254;                 %cm2/g
mu_SnO2_Beam =  57.96491059933077;                 %cm2/g

%set layer densities
%calc_p_CIGS = @(x) -0.15.*x + 5.75; %Formula to Calculate CIGS density Cu(In(1-x),Ga(x))Se2
p_Mo = 10.22;       %g/cm3
p_ZnTe = 6.34;      %g/cm3
p_Cu = 8.96;        %g/cm3
p_CdTe = 5.85;      %g/cm3
p_CdS = 4.82;       %g/cm3
p_SnO2 = 6.85;      %g/cm3 (all looked up)

%set layer thickness
x_Mo = 4.81E-5;                              %cm
x_ZnTe = 3.095E-5;                           %cm   
x_Cu = Cu_thickness;                         %cm          
x_CdTe = absorber_thickness;                 %cm
x_CdS = 8E-6;                                %cm
x_SnO2 = 6E-5;                               %cm; bottom 500nm layer has F, top 100nm layer no F
%generate sublayers
lay_thick = [x_Mo, x_ZnTe, x_Cu, absorber_thickness, x_CdS, x_SnO2];                              %layer thickness (cm)
dt = 0.25E-7;                                  %cm, 1.0nm sublayers/steps
draft_layer_steps = lay_thick/dt;           %matrix containing number of sublayers for each layer
layer_steps = round(draft_layer_steps);     %integer sublayers (to build iio_array that will be summed over)

Mo_sublayers = layer_steps(1);              %redefine matrix of sublayers for ease of use
ZnTe_sublayers = layer_steps(2);            %redefine matrix of sublayers for ease of use
Cu_sublayers = layer_steps(3);            
CdTe_sublayers = layer_steps(4);            %used for both Cd_CdTe and Te_CdTe
CdS_sublayers = layer_steps(5); 
SnO2_sublayers = layer_steps(6);

%set CdTe layer increments and gradings
lay_mu_beam = [mu_Mo_Beam, mu_ZnTe_Beam, mu_Cu_Beam, mu_CdTe_Beam, mu_CdS_Beam, mu_SnO2_Beam];       %layer capture cross sections (cm2/g)
lay_dens = [p_Mo, p_ZnTe, p_Cu, p_CdTe, p_CdS, p_SnO2];                                             %layer density (g/cm3)

rho_cd = 8.7;
rho_te = 6.24;
%T = exp(-mu_CdTe_Beam * p_CdTe * x_CdTe)
%Cd_SIMS = x_CdTe * rho_cd * 1E6
%Te_SIMS = x_CdTe * rho_te * 1E6

%incident transmission
Bo = exp(-lay_mu_beam.*lay_dens.*lay_thick/rad_beam); %generate transmission of each layer
Bo_ZnTe = Bo(1);                                %for transmission of beam reaching ZnTe
Bo_CdTe = Bo(1)* Bo(2);                         %for transmission of beam reaching CdTe
Bo_CdS = Bo(1)* Bo(2) * Bo(4);                  %for transmission of beam reaching CdS
Bo_SnO2 = Bo(1)* Bo(2) * Bo(4) * Bo(5);         %for transmission of beam reaching SnO2

Bo_Cu = Bo(1)* Bo(2);                        %for transmission of beam reaching Cu in CdTe

%Attenuation of Mo_L within Mo layer itself (topmost layer has no external layers attenuating signal)
iio_mo = zeros(Mo_sublayers, 1);     %initialize array to contain sublayer attenuation values

cap_cross_section_of_one_sublayer_in = -p_Mo * mu_Mo_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_MoL = -p_Mo * mu_Mo_MoL * dt / rad_det;

for number_of_sublayers = 1:Mo_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_MoL * number_of_sublayers; 
    iio_mo(number_of_sublayers) = 1 * exp(beam_in + beam_out);
end
fMo = mean(iio_mo);

%%%%%%%%
%Zn_ZnTe
%transmission of Zn_K by layers upstream of ZnTe layer
zn_1 = exp(-mu_Mo_ZnK * p_Mo * x_Mo/rad_det);        %transmission of Mo layer
Zn_external_transmission = Bo_ZnTe * zn_1;

%Attenuation of Zn_L within ZnTe layer itself
iio_zn = zeros(ZnTe_sublayers, 1);     %initialize array to contain sublayer attenuation values

cap_cross_section_of_one_sublayer_in = -p_ZnTe * mu_ZnTe_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_ZnK = -p_ZnTe * mu_ZnTe_ZnK * dt / rad_det;

for number_of_sublayers = 1:ZnTe_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_ZnK * number_of_sublayers; 
    iio_zn(number_of_sublayers) = Zn_external_transmission * exp(beam_in + beam_out);
end
fZn = mean(iio_zn);

%%%%%%%%
%Cd_CdTe
%transmission of Cd_L by layers upstream of CdTe
cd1_1 = exp(-mu_Mo_CdL * p_Mo * x_Mo/rad_det);        %transmission of Mo layer
cd1_2 = exp(-mu_ZnTe_CdL * p_ZnTe * x_ZnTe/rad_det);  %transmission of ZnTe layer
%cd1_3 = exp(-mu_Cu_CdL * p_Cu* x_Cu/rad_det);         %outward atten of Cu on Cd_L 

Cd_external_transmission = Bo_CdTe * cd1_1 * cd1_2;% * cd1_3;

%Attenuation of Cd_L within CdTe layer itself
iio_cd_cdte = zeros(CdTe_sublayers, 1);     %initialize array to contain sublayer attenuation values

cap_cross_section_of_one_sublayer_in = -p_CdTe * mu_CdTe_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_CdL = -p_CdTe * mu_CdTe_CdL * dt / rad_det;

for number_of_sublayers = 1:CdTe_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_CdL * number_of_sublayers; 
    iio_cd_cdte(number_of_sublayers) = Cd_external_transmission * exp(beam_in + beam_out);
end
fCd_CdTe = mean(iio_cd_cdte);

%%%%%%%%
%Te_CdTe
%transmission of Te_L by layers upstream of CdTe
te1_1 = exp(-mu_Mo_TeL *    p_Mo *      x_Mo/rad_det);          %transmission of Mo layer 
te1_2 = exp(-mu_ZnTe_TeL *  p_ZnTe *    x_ZnTe/rad_det);        %transmission of ZnTe layer
%te1_3 = exp(-mu_Cu_TeL *    p_Cu*       x_Cu/rad_det);          %outward atten of Cu on Te_L 

Te_CdTe_external_atten = Bo_CdTe * te1_1 * te1_2;% * te1_3;

%Attenuation of Te_L within CdTe layer itself
iio_te_cdte = zeros(CdTe_sublayers, 1);                         %initialize array to contain sublayer attenuation values

cap_cross_section_of_one_sublayer_in = -p_CdTe * mu_CdTe_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_TeL = -p_CdTe * mu_CdTe_TeL * dt / rad_det;

for number_of_sublayers = 1:CdTe_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_TeL * number_of_sublayers; 
    iio_te_cdte(number_of_sublayers) = Te_CdTe_external_atten * exp(beam_in + beam_out);
end
fTe_CdTe = mean(iio_te_cdte);


%%%%%%%%
%Sn
%transmission of Sn_L by layers upstream of SnO2
sn_1 = exp(-mu_Mo_SnL *    p_Mo *      x_Mo/rad_det);           %transmission of Mo layer 
sn_2 = exp(-mu_ZnTe_SnL *  p_ZnTe *    x_ZnTe/rad_det);         %transmission of ZnTe layer
sn_3 = exp(-mu_CdTe_SnL *  p_CdTe *    x_CdTe/rad_det);         %transmission of CdTe layer
sn_4 = exp(-mu_CdS_SnL *  p_CdS *    x_CdS/rad_det);            %transmission of CdS layer
Sn_external_atten = Bo_SnO2 * sn_1 * sn_2 * sn_3 * sn_4;

%Attenuation of Te_L within CdTe layer itself
iio_sn = zeros(SnO2_sublayers, 1);                         %initialize array to contain sublayer attenuation values

cap_cross_section_of_one_sublayer_in = -p_SnO2 * mu_SnO2_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_SnL = -p_SnO2 * mu_SnO2_SnL * dt / rad_det;

for number_of_sublayers = 1:SnO2_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_SnL * number_of_sublayers; 
    iio_sn(number_of_sublayers) = Sn_external_atten * exp(beam_in + beam_out);
end
fSn = mean(iio_sn);

% %%%%%%%
%Cu
%these are the interface depths determined from derivative max/mins of the SIMS channel shown
CdTe_start = [0.630E-4, 0.847E-4, 0.872E-4, 0.811E-4];      %cm, "start" of Cd channel as Te is upstream of CdTe in ZnTe
CdTe_end = [6.475E-4, 9.362E-4, 8.616E-4, 6.130E-4];        %cm, "end" of Te channel as Cd is downstream of CdTe in CdS

p_Cu_CdTe_array = get_sample_Cu_grading(CdTe_start, CdTe_end, Cu_profile); %g/cm^3
%mu_Cu_CdTe_array = 

%transmission of CuK by layers upstream of CdTe; WELL APPROXIMATES IIO FOR
%ANY LAYERS <= 10nm
cu1 = exp(-mu_Mo_CuK  * p_Mo * x_Mo /rad_det); 
cu2 = exp(-mu_ZnTe_CuK * p_ZnTe * x_ZnTe /rad_det);
Cu_external_atten = Bo_Cu * cu1 * cu2;              %this will be the effective iio if considering a bulk Cu layer

%transmission of Cu_K within Cu layer... 1 nm step with 10 nm layer thick
%layer... not necessary
i_io_cu = zeros(Cu_sublayers,1); %change this to CdTe_sublayers when doing the profile method

cap_cross_section_of_one_sublayer_in = -p_Cu * mu_Cu_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_CuK = -p_Cu * mu_Cu_CuK * dt / rad_det;

for number_of_sublayers = 1:Cu_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_CuK * number_of_sublayers; 
    i_io_cu(number_of_sublayers) = Cu_external_atten * exp(beam_in + beam_out);
end
fCu = mean(i_io_cu);

end

