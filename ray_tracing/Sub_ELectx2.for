!     
! File:   Sub_ELectx2.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 10:52
       SUBROUTINE ELECTX                                                 ELECTX01
!        CALCULATES ELECTRON DENSITY AND GRADIENT FROM ACQUIRED         ELECTX02
!        PROFILES PERFORMING A POLINOMIAL INTERPOLATION                 ELECTX03
! ******************************************************************************
     
      REAL FRECN2(300)!,FRECN(600)                                        
      DIMENSION COE(4),XA(4),YA(4)                                      
      DIMENSION ALPHA(300),BETA(300),GAMMA(300)                                     
      !REAL ZZLAT,ZZLON   
      SAVE ALPHA,BETA,GAMMA                                                                                   
      !INTEGER NOC!,ALT(600)       
     
      COMMON /ZENON/ NOC,ALT(300),FRECN(300)   
      COMMON /ZENON1/ ZZLAT,ZZLON,ZZALT
      !COMMON /IRII/ jm,iy,imd,iut,hour,hx,htec_max,ivar,vbeg,vend,vstp,outf(20,1000),oar(100,1000),piktab
      !COMMON logical /IRI2/ jf(50)
      !COMMON DIMENSION /IRI3/ outf(20,1000),oar(100,1000)

      !SAVE /ZENON/
      SAVE LATOLD,LONOLD                                                LATLON00
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                   ELECTX05
      COMMON /XX/ MODX(2),X,PXPR,PXPTH,PXPPH,PXPT,HMAX                  ELECTX06
      COMMON R(20),T,STP,DRDT(20),N2                                    ELECTX07
      COMMON /WW/ ID,W0,W(400)                                          ELECTX08

      EQUIVALENCE (EARTHR,W(2)),(F,W(6)),(PVOLTA,W(100)),(PERT,W(150))  ELECTX09
!     REAL K                                                             ELECTX10
! ******************************************************************************
     
      F2=F*F                                                            ELECTX11
      MODX(1)=4HGRID                                                    ELECTX12
      IF(PVOLTA.EQ.0.) GO TO 32                                         ELECTX13
      PVOLTA=0.                                                         ELECTX14
      LATOLD=-1.                                                        ELECTX15
      LONOLD=-1.                                                        ELECTX16
!      NOC=600.                                                          ELECTX17

! ******************************************************************************
   32 ZZLAT=DEGS*(PID2-R(2)) !Nueva Latitud                                           ELECTX18
      ZZLON=DEGS*R(3)        !Nueva Longitud                                           ELECTX19
      ZZALT=R(1)
      
      
      IF (ZZLAT.EQ.LATOLD.AND.ZZLON.EQ.LONOLD) GO TO 33
      IF (ZZLAT.NE.LATOLD) LATOLD=ZZLAT
      IF (ZZLON.NE.LONOLD) LONOLD=ZZLON      
    
      
! ******  FIND A PARAMETER TO EXTRAPOLATE THE ELECTRONIC DENSITY   *****ELECTX23
! ******  (BOTTOM PROFILE) NORMALIZE ITS VALUES TO OBTAIN X*F2     *****ELECTX24
! ******   FIND THE HEIGHT OF THE MAXIMUM                ***************ELECTX25
!     IF(FN2C(1,JLAT,JLON).NE.0.)                                       GPROF000
!     1A=ALOG(FN2C(2,JLAT,JLON)/FN2C(1,JLAT,JLON))/(HPC(2)-HPC(1))      GPROF000           
            
!************************************************************+**********
! Se calcula el prefil de Frecuncia Critica vs Altitud
! Correspondiente a las coordenadas (ZZLAT,ZZLON))
! Frecuencia critica: FRECN(600)
! Altitud: ALT(600)
      CALL frec_plasma!(ALT,FRECN,ZZLAT,ZZLON)      
      NOC=300
      NMAX=1 
      DO NH=1,NOC
         FRECN2(NH)=FRECN(NH)**2
         IF (FRECN(NH).GT.FRECN(NMAX)) NMAX=NH
         IF (NH.EQ.NOC) GO TO 4 
      ENDDO       
            
                  
!*******************************************************************************
!     POLINOMIAL INTERPOLATION IN THE INTERVAL OF VALUES FN2C           
!*******************************************************************************
    4 DO 10 I=1,NOC-3
      DO 22 MP=1,4
      XA(MP)=ALT(I+MP-1)
      YA(MP)=FRECN2(I+MP-1)
   22 CONTINUE
      CALL POLCOE(XA,YA,3,COE)
      ALPHA(I)=COE(1)
      BETA(I)=COE(2)
      GAMMA(I)=COE(3)
   10 CONTINUE   
   
! ******************************************************************************
   
      HMAX=ALT(NMAX)
   33 H=R(1)-EARTHR   
      PXPR=0.
      IF (H.GE.ALT(1)) GO TO 12
      X=0.
      GO TO 50
   12 IF (H.GE.ALT(NOC)) GO TO 18
   
      NH=2
      NSTEP=1
      IF (H.LT.ALT(NH-1)) NSTEP=-1
   15 IF (ALT(NH-1).LE.H.AND.H.LT.ALT(NH)) GO TO 16 
      NH=NH+NSTEP
      GO TO 15
    
! ******************************************************************************
!     LINEAR INTERPOLATION IN THE INTERVAL FN2C(K-1,J,I) AND FN2C(K,J,I)
! ******************************************************************************
!   16 X=(ALPHA(NH-1)+BETA(NH-1)*H)/F2                                   
!      PXPR=(BETA(NH-1))/F2                                              
! ******************************************************************************
!     POLINOMIAL INTERPOLATION IN THE INTERVAL FN2C(K-1,J,I) AND FN2C(K,J,I)    
! ******************************************************************************
   16 X=(ALPHA(NH-1)+BETA(NH-1)*H+GAMMA(NH-1)*H**2)/F2             
      PXPR=(BETA(NH-1)+H*(2.*GAMMA(NH-1)))/F2        
     
!   16 X=(ALPHA(NH-1)+BETA(NH-1)*H+GAMMA(NH-1)*H**2+DELTA(NH-1)*H**3)/F2 
!      PXPR=(BETA(NH-1)+H*(2.*GAMMA(NH-1))+H**2*(3.*DELTA(NH-1)))/F2     
! ******************************************************************************  
      GO TO 50                                                          ELECTX41
   !18 X=FN2C(NOC,JLAT,JLON)/F2                                          GPROF000
   ! n^2=1-X   
   18 X=FRECN2(NOC)/F2
   50 IF (PERT.NE.0.) CALL ELECT1                                       ELECTX42
!*******************************************************************************
!
!ALEX: Se ha establecido un ERROR debido a una condición demasiado restrictiva
!      por lo cual la impresión en pantalla de las coordenadas para el radio 
!      de la onda R (1), R (2), R (3)cuando ocurrido el transmisor estaba en
!      la parte superior del receptor, es decir, H.GE.RCVRH.
!*******************************************************************************
!      IF (X.EQ.0..AND.H.GE.RCVRH) PRINT 1234, R(1),R(2),R(3)           ELECTX43
      IF (X.EQ.0.) WRITE(16,1234) R(1),R(2),R(3)                           AZZ
!*******************************************************************************
     
 1234 FORMAT (3(2X,F20.10))                                             ELECTX44
      WRITE(6,1704) R(1),R(2),R(3),R(4),R(5),R(6)                       ELECTX45
 1704 FORMAT (6(X,'R=',X,F15.10))                                       ELECTX46
      RETURN                                                            ELECTX47
      END                                                               -

