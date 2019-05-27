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

thickness = [t_down',t',t_up'];
%thickness = t';

IIO = zeros(length(t),3);

for l = 1:length(thickness(1,:))
    
    thick = thickness(:,l);
    
    for k = 1:length(thick)
        depth = 0:dt:thick(k);
        %define different graing profiles with same average composition
        grad_flat = ones(length(depth),1)*0.3;
         grad_up = 0:1/(length(depth)-1):1;
         grad_down = 1-grad_up;
         mid = round(length(depth)/2);
         V = 0:1/(mid-1):1;
         gradV(1:mid) = 1-V; gradV(mid:length(depth)) = V;
         gradN = 1-gradV;
        
        grad = grad_flat;
        
        M = thick(k)/dt;
        M = round(M); %rounds to nearest integer for total number of layers
        
%%% gradient and capture cross section info deleted %%%
        
        b1 = exp(-mu_ITO_Beam*p_ITO*x_ITO/sin(beamtheta*pi/180));
        b2 = exp(-mu_ZnO_Beam*p_ZnO*x_ZnO/sin(beamtheta*pi/180));
        b3 = exp(-mu_CdS_Beam*p_CdS*x_CdS/sin(beamtheta*pi/180));
        b4 = exp(-mu_SiN_Beam*p_SiN*x_SiN/sin(beamtheta*pi/180));
        b5 = b1*b2*b3*b4;
        
        
         %plots grading and Beam I/Io vs depth
         figure
         plotyy(depth./(sin(beamtheta*pi/180)),b4,depth./(sin(beamtheta*pi/180)),sam_grad)
        
         %Copper
         i_io_cu = zeros(M,1);
         %mu_CIGS_cu = calc_mu_Cu(sam_grad);
         c1 = exp(-mu_ITO_CuK*p_ITO*x_ITO/sin(detectortheta*pi/180)); %ITO attn
         c2 = exp(-mu_ZnO_CuK*p_ZnO*x_ZnO/sin(detectortheta*pi/180)); %ZnO attn
         c3 = exp(-mu_CdS_CuK*p_CdS*x_CdS/sin(detectortheta*pi/180)); %CdS attn
         c4 = exp(-mu_SiN_CuK*p_SiN*x_SiN/sin(detectortheta*pi/180)); %SiN attn
         
        %Total CuK fluorescence attenuation including incident beam attn
        c5 = c1*c2*c3*c4*b5;         
        for N = 1:M
             for i = 1:N
                beam_in = -p_CIGS(1:i).*mu_CIGS_beam(1:i)*dt;
                 beam_out = -p_CIGS(1:i).*mu_CIGS_cu(1:i)*dt;
                 i_io_cu(N) = c5*exp(sum(beam_in+beam_out));
             end
         end
         fCu = sum(i_io_cu)/M;

%%% each element line internal absorber reabsorption loops deleted %%%        
        
        %IIO_Cu(k,l) = fCu;
        %IIO_Ga(k,l) = fGa;
        %IIO_In(k,l) = fIn;
        %IIO_Se(k,l) = fSe;
    end
    
end
 figure; plot(thickness*1E4,IIO_flat*100,'-o');
 legend('Cu-K\alpha', 'In-L\alpha1', 'Ga-K\alpha', 'Se-K\alpha');
 ylabel('I/I_o (%)');
 xlabel('Thicknes (\mum)');
 title('I/I_o for Varied CIGS thickness');
 text(0,0.5,'  No Grading at GGI = 0.5');

 i = 1;
 CU_grad = [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];
 i = 2;
 IN_grad= [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];
 i=3;
 GA_grad = [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];
 i=4;
 SE_grad = [IIO_flat(:,i),IIO_up(:,i),IIO_down(:,i),IIO_V(:,i),IIO_N(:,i)];

 figure; plot(thickness*1E4,SE_grad*100,'-o');
 legend('Flat', 'Up', 'Down', 'V', 'N');
 ylabel('I/I_o (%)');
 xlabel('Thicknes (\mum)');
 title('I/I_o for Selenium Varied CIGS Grading');

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
