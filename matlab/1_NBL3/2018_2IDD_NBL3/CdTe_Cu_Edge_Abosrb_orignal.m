function [fCd_CdTe, fTe_CdTe, fCu] = CdTe_Cu_Edge_Abosrb_orignal(beam_energy, beamtheta, detectortheta, absorber_thickness, cu_gradient)

rad_beam = sin(beamtheta*pi/180);       %convert to radians
rad_det = sin(detectortheta*pi/180);    %convert to radians


%Stack
%Mo/ ZnTe/ Cu/ CdTe + CdCl2/ CdS + O2/ SnO2/ SnO2 + F/ CaHNaO2

%capture cross-sections
%could make a function that accesses library: findMatMu(beam_energy, material)
%Stack
%Mo/ ZnTe/ Cu/ CdTe + CdCl2/ CdS + O2/ SnO2/ SnO2 + F/ CaHNaO2

%fluorescence capture cross-sections
%Set Mo info
mu_Mo_CdL = 1872.8;
mu_Mo_TeL = 1212.0;
mu_Mo_CuK = 154.9601;


%Set ZnTe info
mu_ZnTe_CdL = 680.0102;
mu_ZnTe_TeL = 437.554;
mu_ZnTe_CuK = 196.3259;

%Set Cu info
mu_Cu_CdL = 695.4808;
mu_Cu_TeL =  440.4480;
mu_Cu_CuK = 51.8756;

%Set CdTe info
mu_CdTe_CdL  = 566.2543;                    %cm2/g
mu_CdTe_TeL  = 8.372E2;                     %cm2/g
mu_CdTe_CuK  = 2.454E2;                     %cm2/g

%Set CdS info
mu_CdS_MoL = 922.9015;                      %cm2/g
mu_CdS_ZnK = 168.2039;                      %cm2/g
mu_CdS_TeL = 1221;                          %cm2/g
mu_CdS_CuK = 1.933E2;                       %cm2/g
mu_CdS_CdL = 657.7857;                      %cm2/g


%incident energy capture cross-sections @ 8.99keV
%values used are interpolated from the NIST website, values in comment are from the python package 'xraylib'
mu_Mo_Beam =    121.5342;                 %cm2/g, xraylib: 114.239
mu_ZnTe_Beam =  152.0136;                 %cm2/g, xraylib: 145.807
mu_Cu_Beam =    277.6288;                 %cm2/g, xraylib: 277.550
mu_CdTe_Beam=   194.2055;                 %cm2/g, xraylib: 182.956
mu_CdS_Beam =   152.5925;                 %cm2/g, xraylib: 143.567
mu_SnO2_Beam =  155.2955;                 %cm2/g, xraylib: 146.286

%set layer densities
%calc_p_CIGS = @(x) -0.15.*x + 5.75; %Formula to Calculate CIGS density Cu(In(1-x),Ga(x))Se2
p_Mo = 10.22;       %g/cm3
p_ZnTe = 6.34;      %g/cm3
p_Cu = 8.96;        %g/cm3
p_CdTe = 5.85;      %g/cm3
p_CdS = 4.82;       %g/cm3
p_SnO2 = 6.85;      %g/cm3 (all looked up)

%set layer
%thickness%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
x_Mo = 5.0E-5;                              %cm
x_ZnTe = 3.75E-5;                           %cm   
x_Cu = cu_gradient;                         %cm          
x_CdTe = absorber_thickness;                %cm
x_CdS = 8E-6;                               %cm
x_SnO2 = 6E-5;                              %cm; bottom 500nm layer has F, top 100nm layer no F

%set CdTe layer increments and gradings
stack = {'Mo', 'ZnTe', 'Cu', 'CdTe', 'CdS', 'SnO2'};% 'SLG'};
lay_thick = [5.0E-5 3.75E-5 cu_gradient absorber_thickness 8E-6 6E-5];                     %layer thickness (cm)
lay_mu_beam =[121.5342 152.0136 277.6288 194.2055 152.5925 155.2955];   %layer capture cross sections (cm2/g)
lay_dens = [10.22 6.34 8.96 5.85 4.82 6.85];                            %layer density (g/cm3)

dt = 0.25E-7;                                  %0.25nm sublayers (in cm)
draft_layer_steps = lay_thick/dt;           %matrix containing number of sublayers for each layer
layer_steps = round(draft_layer_steps);     %integer sublayers (to build iio_array that will be summed over)

ZnTe_sublayers = layer_steps(2);            %redefine matrix of sublayers for ease of use
Cu_sublayers = layer_steps(3);            
CdTe_sublayers = layer_steps(4);            %used for both Cd_CdTe and Te_CdTe
CdS_sublayers = layer_steps(5); 


%incident absorption
stack = {'Mo', 'ZnTe', 'hiCu', 'CdTe', 'CdS', 'SnO2'};% 'SLG'};
Bo = exp(-lay_mu_beam.*lay_dens.*lay_thick/rad_beam); %fracctional intensity of beam transmitted through each layer

Bo_CdL_CdTe = Bo(1)* Bo(2) * Bo(3);         %for transmission of beam reaching CdTe
Bo_CdL_CdS = Bo(1)* Bo(2) * Bo(3) * Bo(4);  %for transmission of beam reaching CdS

Bo_TeL_ZnTe = Bo(1);                        %for transmission of beam reaching ZnTe
Bo_TeL_CdTe = Bo(1)* Bo(2) * Bo(3);         %for transmission of beam reaching CdTe

Bo_Cu_Cu = Bo(1)* Bo(2);                    %for transmission of beam reaching Cu 'layer'

%%%%%%%%
%Cd_CdTe
%Attenuation of Cd_L by all **external** layers on the way out of CdTe layer, includes beam attenuation on the way in...?
cd1_1 = exp(-mu_Mo_CdL * p_Mo * x_Mo/rad_det);        %outward atten of Mo on Cd_L 
cd1_2 = exp(-mu_ZnTe_CdL * p_ZnTe * x_ZnTe/rad_det);  %outward atten of ZnTe on Cd_L 
cd1_3 = exp(-mu_Cu_CdL * p_Cu* x_Cu/rad_det);         %outward atten of Cu on Cd_L 

Cd_CdTe_external_atten = Bo_CdL_CdTe * cd1_1 * cd1_2 * cd1_3;

%Attenuation of Cd_L within CdTe layer itself
iio_cd_cdte = zeros(CdTe_sublayers, 1);     %initialize array to contain sublayer attenuation values

cap_cross_section_of_one_sublayer_in = -p_CdTe * mu_CdTe_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_CdL = -p_CdTe * mu_CdTe_CdL * dt / rad_det;

for number_of_sublayers = 1:CdTe_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_CdL * number_of_sublayers; 
    iio_cd_cdte(number_of_sublayers) = Cd_CdTe_external_atten * exp(beam_in + beam_out);
end
fCd_CdTe = mean(iio_cd_cdte);


%%%%%%%%
% %Cd_CdS
% %Attenuation of Cd_L by all **external** layers on the way out of CdS layer, includes beam attenuation on the way in...?
% cd2_1 = exp(-mu_Mo_CdL * p_Mo * x_Mo/rad_det);        %outward atten of Mo on Cd_L 
% cd2_2 = exp(-mu_ZnTe_CdL * p_ZnTe * x_ZnTe/rad_det);  %outward atten of ZnTe on Cd_L 
% cd2_3 = exp(-mu_Cu_CdL * p_Cu* x_Cu/rad_det);         %outward atten of Cu on Cd_L
% cd2_4 = exp(-mu_CdTe_CdL * p_CdTe* x_CdTe/rad_det);   %outward atten of Cu on Cd_L 
% 
% Cd_CdS_external_atten = Bo_CdL_CdS * cd2_1 * cd2_2 * cd2_3 * cd2_4;
% 
% %Attenuation of Cd_L within CdS layer itself
% iio_cd_cds = zeros(CdS_sublayers, 1);     %initialize array to contain sublayer attenuation values
% depth_3 = 0:dt:x_CdS;                     %initialize iteration index, 10nm increments
% 
% for i = 1:length(depth_3)
%         beam_in = -p_CdS * mu_CdS_Beam * depth_3(i)/rad_beam;
%         beam_out = -p_CdS * mu_CdS_CdL * depth_3(i)/rad_det; %(check 1-sin?)
%         iio_cd_cds(i) = Cd_CdS_external_atten * exp(beam_in + beam_out);
% end
% fCd_CdS = sum(iio_cd_cds)/(x_CdS/dt);


%%%%%%%%
%Te_CdTe
%Attenuation of Te_L by all **external** layers on the way out of CdTe layer, includes beam attenuation on the way in...?
te1_1 = exp(-mu_Mo_TeL *    p_Mo *      x_Mo/rad_det);          %outward atten of Mo on Te_L 
te1_2 = exp(-mu_ZnTe_TeL *  p_ZnTe *    x_ZnTe/rad_det);        %outward atten of ZnTe on Te_L 
te1_3 = exp(-mu_Cu_TeL *    p_Cu*       x_Cu/rad_det);          %outward atten of Cu on Te_L 

Te_CdTe_external_atten = Bo_TeL_CdTe * te1_1 * te1_2 * te1_3;

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

% %%%%%%%%
% %Te_ZnTe
% %Attenuation of Te_L by all **external** layers on the way out of ZnTe layer, includes beam attenuation on the way in...?
% te2_1 = exp(-mu_Mo_TeL * p_Mo * x_Mo/rad_det);        %outward atten of Mo on Te_L 
% 
% Te_ZnTe_external_atten = Bo_TeL_ZnTe * te2_1;
% 
% %Attenuation of Te_L within CdTe layer itself
% iio_te_znte = zeros(ZnTe_sublayers, 1);     %initialize array to contain sublayer attenuation values
% depth_2 = 0:dt:x_ZnTe;                      %initialize iteration index, 10nm increments
% 
% for i = 1:length(depth_2)
%         beam_in = -p_ZnTe * mu_ZnTe_Beam * depth_2(i)/rad_beam;
%         beam_out = -p_ZnTe * mu_ZnTe_TeL * depth_2(i)/rad_det;
%         iio_te_znte(i) = Te_ZnTe_external_atten * exp(beam_in + beam_out);
% end
% fTe_ZnTe = sum(iio_te_znte)/(x_ZnTe/dt);


%%%%%%%
%Cu_Cu
%Attenuation of Cu_K by all **external** layers on the way out of Cu layer, includes beam attenuation on the way in...?
cu1 = exp(-mu_Mo_CuK  * p_Mo * x_Mo /rad_det); 
cu2 = exp(-mu_ZnTe_CuK * p_ZnTe * x_ZnTe /rad_det);
Cu_Cu_external_atten = Bo_Cu_Cu * cu1 * cu2;

%attenuation of Cu_K within Cu layer... 10 nm step with 10 nm layer thick layer...
i_io_cu = zeros(Cu_sublayers,1);

cap_cross_section_of_one_sublayer_in = -p_Cu * mu_Cu_Beam * dt / rad_beam;
cap_cross_section_of_one_sublayer_out_CuK = -p_Cu * mu_Cu_CuK * dt / rad_det;

for number_of_sublayers = 1:Cu_sublayers
    beam_in = cap_cross_section_of_one_sublayer_in * number_of_sublayers;
    beam_out = cap_cross_section_of_one_sublayer_out_CuK * number_of_sublayers; 
    i_io_cu(number_of_sublayers) = Cu_Cu_external_atten * exp(beam_in + beam_out);
end
fCu = mean(i_io_cu);
end

