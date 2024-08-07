function Inicio()
% Ejecuta el propgrama ionort_exe en la carpeta 'source'
%
clc
close
clear

disp('Inicio de programa')
disp('==================')
disp('==================')
disp('.....')
datestr(now)
oldFolder = cd('MinGW-Windows');% Ingresa en la carpeta "source" desde la direcc.
                         % F:\Doctorado_Radar\ionort_0.7.2\MATLAB 
[status,result] = system('ray_tracing');%Ejecuta el propgram
                                                    %ionort_"chapman_nf"
                                                                 
coord=textread('raytracing.txt');
datestr(now)

% Eliminazione dei duplicati (righe con uguali coordin:ate)
coord( find( diff(coord(:,1) ) == 0 & diff(coord(:,2) ) == 0 & diff(coord(:,3) ) == 0 ), : ) = [];
x=coord(:,2);
y=coord(:,3);
z=coord(:,1);
    
%N=length(x)-1; %% Range y retardo
%xx=linspace(x(1),x(end-1),(N-1)*2+N);
%yy=linspace(y(1),y(end-1),(N-1)*2+N);
%zz=interp1(x(1:end-1),z(1:end-1),xx,'spline');
%plot3(x(1:end-1),y(1:end-1),z(1:end-1)-6371,'b','LineWidth',1)
%hold on
%plot3(xx,yy,zz-6371,'m','LineWidth',1)


rho = z(1:end-1);
phi = x(1:end-1);
theta = y(1:end-1);
radius = rho .* 1000;
lat = (pi/2 - phi)./(pi/180);
lon = (theta)./(pi/180);
altitude = ( radius - 6371* 1000 ) ./ 1000;

[x,y] = Spherical2AzimuthalEquidistantzz(lat, lon, lat(1), lon(1), 0, 0, radius(1));
hold on;  
xlabel('Ground Range [km]','fontweight','b');
ylabel('Altitud [km]','fontweight','b');
ray = sqrt( x.^2 + y.^2 ) / ( 100 * pi ); 
%cline( ray( 1 : length(ray) ),altitude( 1 : length(altitude) ));
plot(ray,altitude,'b','LineWidth',1)
xlim([0,4000]);
grid on
title('RAY TRACING 2D')
%xlabel('LATITUD [rad]')
%ylabel('LONGITUD [rad]')
%zlabel('ALTITUD [km]')
disp('Fin')
hold on
mark_trans = plot(ray(1), altitude(1),'ks','MarkerFaceColor','g');
legenda_punti = [ mark_trans ];
legenda_label = {'Transmisor'};
legend( legenda_punti, legenda_label );


cd(oldFolder); % Vuelde desde la carpera "source"
               % a F:\Doctorado_Radar\ionort_0.7.2\MATLAB
end               
               
               