%clear
close all
beamenergy = 10.4; %keV
beamtheta = 90;
detectortheta = 43;
x_ITO = 0;
x_SiN = 0;
x_ZnO = 0;%0.2E-4; % layer thickness in cm ... ~200nm
x_CdS = 0;%0.05E-4; %layer thickness in cm ... ~50nm
thickness = 0.1:0.2:5;
%thickness = 2;
rough = 0.1;

t = thickness.*1E-4; %um to cm
t_up = t.*(1+rough);
t_down = t.*(1-rough);
dt = 0.000001; %50nm thick layers

%thickness = [t_down',t',t_up'];
thickness = t';

IIO = zeros(length(t),3);
for l = 1:length(thickness(1,:))
    
    thick = thickness(:,l);
    
    for k = 1:length(thick)
        depth = 0:dt:thick(k);
        %define different graing profiles with same average composition
        grad_flat = ones(length(depth),1)*0.3;
%         grad_up = 0:1/(length(depth)-1):1;
%         grad_down = 1-grad_up;
%         mid = round(length(depth)/2);
%         V = 0:1/(mid-1):1;
%         gradV(1:mid) = 1-V; gradV(mid:length(depth)) = V;
%         gradN = 1-gradV;
        
        grad = grad_flat;
        
        M = thick(k)/dt;
        M = round(M); %rounds to nearest integer for total number of layers
        
        p_CIGS = -0.15.*grad + 5.75;
        mu_CIGS_in =  90.183.*grad + 679.77; % true within CIGS layer
        mu_CIGS_cu = -58.285.*grad + 128.67; % true within CIGS layer
        mu_CIGS_ga = -33.868.*grad + 130.77; % true within CIGS layer
        mu_CIGS_se =  17.324.*grad + 78.468;
        
        
        %set layer densities
        p_ITO = 7.14;    %g/cm3
        p_ZnO = 5.6;    %g/cm3
        p_CdS = 4.826;   %g/cm3
        p_SiN = 3.44;    %g/cm3
        
        %Set SiN info
        mu_SiN_CuK = 4.19E1; %cm2/g
        mu_SiN_InL = 4.97E2; %cm2/g
        mu_SiN_GaK = 2.71E1; %cm2/g
        mu_SiN_SeK = 1.57E1; %cm2/g
        
        %Set ITO info
        mu_ITO_CuK = 2.09E2; %cm2/g
        mu_ITO_InL = 4.278E2; %cm2/g
        mu_ITO_GaK = 1.442E2; %cm2/g
        mu_ITO_SeK = 8.599E1; %cm2/g
        
        %Set ZnO info
        mu_ZnO_CuK = 4.868E1; %cm2/g
        mu_ZnO_InL = 5.562E2; %cm2/g
        mu_ZnO_GaK = 3.315E1; %cm2/g
        mu_ZnO_SeK = 1.412E2; %cm2/g
        
        %Set CdS info
        mu_CdS_CuK = 1.933E2; %cm2/g
        mu_CdS_InL = 5.713E2; %cm2/g
        mu_CdS_GaK = 1.329E2; %cm2/g
        mu_CdS_SeK = 7.891E1; %cm2/g
        
        
        if beamenergy == 9.0
            % NEED TO ENTER 9KEV BEAM ATTENUATION IN CIGS LAYER
            mu_ITO_Beam = 1.55E2; %cm2/g
            mu_ZnO_Beam = 3.576E1; %cm2/g
            mu_CdS_Beam = 1.431E2; %cm2/g
            mu_SiN_Beam = 2.98E1; %cm2/g
        elseif beamenergy == 10.4
            mu_ITO_Beam = 1.06E2; %cm2/g
            mu_ZnO_Beam = 1.71E2; %cm2/g
            mu_CdS_Beam = 9.70E1; %cm2/g
            mu_SiN_Beam = 1.95E1; %cm2/g
            mu_CIGS_beam =   20.619.*grad + 95.876; % true within CIGS layer
        elseif beamenergy == 10.8
            mu_ITO_Beam = 8.96E1; %cm2/g
            mu_ZnO_Beam = 1.56E2; %cm2/g
            mu_CdS_Beam = 8.75E1; %cm2/g
            mu_SiN_Beam = 1.75E1; %cm2/g
            mu_CIGS_beam =   18.9.*grad + 86.857; % true within CIGS layer
        elseif beamenergy == 12.8
            mu_ITO_Beam = 6.033E1; %cm2/g
            mu_ZnO_Beam = 1.002E2; %cm2/g
            mu_CdS_Beam = 5.519E1; %cm2/g
            mu_SiN_Beam = 1.07E1;  %cm2/g
            mu_CIGS_beam =   22.257.*grad + 116.9; %calculates beam attenuation at a given gallium ratio in the CIGS layer
        else
            msgbox(['The beam energy for the run on ' rundate 'and for sample ', ...
                sample ' has not be entered yet. Please input the run information.']);
        end
        
        b1 = exp(-mu_ITO_Beam*p_ITO*x_ITO/sin(beamtheta*pi/180));
        b2 = exp(-mu_ZnO_Beam*p_ZnO*x_ZnO/sin(beamtheta*pi/180));
        b3 = exp(-mu_CdS_Beam*p_CdS*x_CdS/sin(beamtheta*pi/180));
        b4 = exp(-mu_SiN_Beam*p_SiN*x_SiN/sin(beamtheta*pi/180));
        b5 = b1*b2*b3*b4;
        
        
        % %plots grading and Beam I/Io vs depth
        % figure
        % plotyy(depth./(sin(beamtheta*pi/180)),b4,depth./(sin(beamtheta*pi/180)),sam_grad)
        
%         %Copper
%         i_io_cu = zeros(M,1);
%         %mu_CIGS_cu = calc_mu_Cu(sam_grad);
%         c1 = exp(-mu_ITO_CuK*p_ITO*x_ITO/sin(detectortheta*pi/180)); %ITO attn
%         c2 = exp(-mu_ZnO_CuK*p_ZnO*x_ZnO/sin(detectortheta*pi/180)); %ZnO attn
%         c3 = exp(-mu_CdS_CuK*p_CdS*x_CdS/sin(detectortheta*pi/180)); %CdS attn
%         c4 = exp(-mu_SiN_CuK*p_SiN*x_SiN/sin(detectortheta*pi/180)); %SiN attn
%         
%         %Total CuK fluorescence attenuation including incident beam attn
%         c5 = c1*c2*c3*c4*b5;
%         
%         for N = 1:M
%             for i = 1:N
%                 beam_in = -p_CIGS(1:i).*mu_CIGS_beam(1:i)*dt;
%                 beam_out = -p_CIGS(1:i).*mu_CIGS_cu(1:i)*dt;
%                 i_io_cu(N) = c5*exp(sum(beam_in+beam_out));
%             end
%         end
%         fCu = sum(i_io_cu)/M;
        
        
%         %Gallium
%         i_io_ga = zeros(M,1);
%         %mu_CIGS_ga = calc_mu_Ga(sam_grad);
%         g1 = exp(-mu_ITO_GaK*p_ITO*x_ITO/sin(detectortheta*pi/180)); %ITO attn
%         g2 = exp(-mu_ZnO_GaK*p_ZnO*x_ZnO/sin(detectortheta*pi/180)); %ZnO attn
%         g3 = exp(-mu_CdS_GaK*p_CdS*x_CdS/sin(detectortheta*pi/180)); %CdS attn
%         g4 = exp(-mu_SiN_GaK*p_SiN*x_SiN/sin(detectortheta*pi/180)); %SiN attn
%         %Total GaK fluorescence attenuation including incident beam attn
%         g5 = g1*g2*g3*g4*b5;
%         for N = 1:M
%             for i = 1:N
%                 beam_in = -p_CIGS(1:i).*mu_CIGS_beam(1:i)*dt;
%                 beam_out = -p_CIGS(1:i).*mu_CIGS_ga(1:i)*dt;
%                 i_io_ga(N) = g5*exp(sum(beam_in+beam_out));
%             end
%         end
%         fGa = sum(i_io_ga)/M;
        
        % figure
        % plotyy(depth./(sin(detectortheta*pi/180)),g4,depth./(sin(detectortheta*pi/180)),sam_grad)
%         
%         %Indium
%         i_io_in = zeros(M,1);
%         %mu_CIGS_in = calc_mu_In(sam_grad);
%         i1 = exp(-mu_ITO_InL*p_ITO*x_ITO/sin(detectortheta*pi/180)); %ITO attn
%         i2 = exp(-mu_ZnO_InL*p_ZnO*x_ZnO/sin(detectortheta*pi/180)); %ZnO attn
%         i3 = exp(-mu_CdS_InL*p_CdS*x_CdS/sin(detectortheta*pi/180)); %CdS attn
%         i4 = exp(-mu_SiN_InL*p_SiN*x_SiN/sin(detectortheta*pi/180)); %SiN attn
%         %Total GaK fluorescence attenuation including incident beam attn
%         i5 = i1*i2*i3*i4*b5;
%         
%         for N = 1:M
%             for i = 1:N
%                 beam_in = -p_CIGS(1:i).*mu_CIGS_beam(1:i)*dt;
%                 beam_out = -p_CIGS(1:i).*mu_CIGS_in(1:i)*dt;
%                 i_io_in(N) = i5*exp(sum(beam_in+beam_out));
%             end
%         end
%         fIn = sum(i_io_in)/M;
        
        %
        % % figure
        % % plotyy(depth./(sin(detectortheta*pi/180)),i4,depth./(sin(detectortheta*pi/180)),sam_grad)
        %
        %Selenium
        i_io_se = zeros(M,1);
        %mu_CIGS_se = calc_mu_Se(sam_grad);
        s1 = exp(-mu_ITO_SeK*p_ITO*x_ITO/sin(detectortheta*pi/180)); %ITO attn
        s2 = exp(-mu_ZnO_SeK*p_ZnO*x_ZnO/sin(detectortheta*pi/180)); %ZnO attn
        s3 = exp(-mu_CdS_SeK*p_CdS*x_CdS/sin(detectortheta*pi/180)); %CdS attn
        s4 = exp(-mu_SiN_SeK*p_SiN*x_SiN/sin(detectortheta*pi/180)); %SiN attn
        %Total GaK fluorescence attenuation including incident beam attn
        s5 = s1*s2*s3*s4*b5;
        
        for N = 1:M
            for i = 1:N
                beam_in = -p_CIGS(1:i).*mu_CIGS_beam(1:i)*dt;
                beam_out = -p_CIGS(1:i).*mu_CIGS_se(1:i)*dt;
                i_io_se(N) = s5*exp(sum(beam_in+beam_out));
            end
        end
        fSe = sum(i_io_se)/M;
        
        
        %IIO_Cu(k,l) = fCu;
        %IIO_Ga(k,l) = fGa;
        %IIO_In(k,l) = fIn;
        %IIO_Se(k,l) = fSe;
    end
    
end
% figure; plot(thickness*1E4,IIO_flat*100,'-o');
% legend('Cu-K\alpha', 'In-L\alpha1', 'Ga-K\alpha', 'Se-K\alpha');
% ylabel('I/I_o (%)');
% xlabel('Thicknes (\mum)');
% title('I/I_o for Varied CIGS thickness');
% text(0,0.5,'  No Grading at GGI = 0.5');
%
% i = 1;
% CU_grad = [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];
% i = 2;
% IN_grad= [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];
% i=3;
% GA_grad = [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];
% i=4;
% SE_grad = [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];
%
% figure; plot(thickness*1E4,SE_grad*100,'-o');
% legend('Flat', 'Up', 'Down', 'V', 'N');
% ylabel('I/I_o (%)');
% xlabel('Thicknes (\mum)');
% title('I/I_o for Selenium Varied CIGS Grading');
%
% 
% xlafigure; plot(thickness*1E4,CU_grad*100,'-o');
% legend('Flat', 'Up', 'Down', 'V', 'N');
% ylabel('I/I_o (%)');bel('Thicknes (\mum)');
% title('I/I_o for Copper Varied CIGS Grading');
%
% figure; plot(thickness*1E4,IN_grad*100,'-o');
% legend('Flat', 'Up', 'Down', 'V', 'N');
% ylabel('I/I_o (%)');
% xlabel('Thicknes (\mum)');
% title('I/I_o for Indium Varied CIGS Grading');
%
% figure; plot(thickness*1E4,GA_grad*100,'-o');
% legend('Flat', 'Up', 'Down', 'V', 'N');
% ylabel('I/I_o (%)');
% xlabel('Thicknes (\mum)');
% title('I/I_o for Gallium Varied CIGS Grading');
figure; plot(