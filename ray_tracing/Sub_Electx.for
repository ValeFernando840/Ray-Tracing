!     
! File:   Sub_Electx.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 10:41
!

!*******************************************************************************         
      SUBROUTINE ELECTX                                                 ELECTX01
!        CALCULATES ELECTRON DENSITY AND GRADIENT FROM ACQUIRED         ELECTX02
!        PROFILES PERFORMING A POLINOMIAL INTERPOLATION                 ELECTX03
! ******************************************************************************
     
      DIMENSION FN2C(600,10,25)                                         
      DIMENSION COE(4),XA(4),YA(4)                                      
      DIMENSION ALPHA(600),BETA(600),GAMMA(600)                         
!      DIMENSION ALPHA(600),BETA(600),GAMMA(600),DELTA(600)              
     
      SAVE ALPHA,BETA,GAMMA                                             
!      SAVE ALPHA,BETA,GAMMA,DELTA                                       
     
      COMMON /ALEX2/ NOC,HPC(600),FNC(600,10,25)                        GPROF000
      COMMON /ZZZZ/ ZZLAT,ZZLON,JLAT,JLON                               LATLON00
      SAVE LATOLD,LONOLD                                                LATLON00
     
! ******************************************************************************
!      EQUIVALENCE (XMTRH,W(3)),(RCVRH,W(20))                           ELECTX04
! ******************************************************************************
     
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                   ELECTX05
      COMMON /XX/ MODX(2),X,PXPR,PXPTH,PXPPH,PXPT,HMAX                  ELECTX06
      COMMON R(20),T,STP,DRDT(20),N2                                    ELECTX07
      COMMON /WW/ ID,W0,W(400)                                          ELECTX08
      EQUIVALENCE (EARTHR,W(2)),(F,W(6)),(PVOLTA,W(100)),(PERT,W(150))  ELECTX09
!      REAL K                                                            ELECTX10
! ******************************************************************************
     
      F2=F*F                                                            ELECTX11
      MODX(1)=4HGRID                                                    ELECTX12
      IF(PVOLTA.EQ.0.) GO TO 32                                         ELECTX13
      PVOLTA=0.                                                         ELECTX14
      LATOLD=-1.                                                        ELECTX15
      LONOLD=-1.                                                        ELECTX16
! ******************************************************************************
!     ALEX: Lettura file 'GRIDPROFILES.txt',                            
!           scrittura file 'GRIDPROFILES_TEST.txt',                     
!           inizializzazione matrice per "plasma frequency profiles" FNC(K,J,I) 
! ******************************************************************************
      CALL GRIDPROFILES                                                 GPROF000
! ******************************************************************************
   32 ZZLAT=DEGS*(PID2-R(2))                                            ELECTX17
      ZZLON=DEGS*R(3)                                                   ELECTX18
      CALL LATLON                                                       ELECTX19
      IF(JLAT.EQ.LATOLD.AND.JLON.EQ.LONOLD) GO TO 33                    ELECTX20
      IF (JLAT.NE.LATOLD) LATOLD=JLAT                                   ELECTX21
      IF (JLON.NE.LONOLD) LONOLD=JLON                                   ELECTX22
! ******  FIND A PARAMETER TO EXTRAPOLATE THE ELECTRONIC DENSITY   *****ELECTX23
! ******  (BOTTOM PROFILE) NORMALIZE ITS VALUES TO OBTAIN X*F2     *****ELECTX24
! ******   FIND THE HEIGHT OF THE MAXIMUM                ***************ELECTX25
!     IF(FN2C(1,JLAT,JLON).NE.0.)                                      GPROF000
!     1A=ALOG(FN2C(2,JLAT,JLON)/FN2C(1,JLAT,JLON))/(HPC(2)-HPC(1))      GPROF000
      NMAX=1                                                            ELECTX26
      DO NH=1,NOC                                                       
!     FN2C(NH,JLAT,JLON)=K*FN2C(NH,JLAT,JLON)                          GPROF000
      FN2C(NH,JLAT,JLON)=FNC(NH,JLAT,JLON)**2                           GPROF000
     
      IF (FNC(NH,JLAT,JLON).GT.FNC(NMAX,JLAT,JLON)) NMAX=NH             GPROF000
      IF (NH.EQ.NOC) GO TO 4                                            
      ENDDO                                                             
!*******************************************************************************
!     POLINOMIAL INTERPOLATION IN THE INTERVAL OF VALUES FN2C           
!*******************************************************************************
    4 DO 10 I=1,NOC-3                                                   
      DO 22 MP=1,4                                                      
      XA(MP)=HPC(I+MP-1)                                                GPROF000
!      YA(MP)=FN2C(I+MP-1)                                              GPROF000
! ******************************************************************************
      YA(MP)=FN2C(I+MP-1,JLAT,JLON)                                     GPROF000
! ******************************************************************************
   22 CONTINUE                                                          
      CALL POLCOE (XA,YA,3,COE)                                         
!      CALL POLCOE (XA,YA,4,COE)                                         
      ALPHA(I)=COE(1)                                                   
      BETA(I)=COE(2)                                                    
      GAMMA(I)=COE(3)                                                   
!      DELTA(I)=COE(4)                                                   
!      WRITE(6,1707)I,ALPHA(I),BETA(I),GAMMA(I),DELTA(I)                 
! 1707 FORMAT (1X,I4,4(2X,E20.10))                                       
   10 CONTINUE                                                          
! ******************************************************************************
      HMAX=HPC(NMAX)                                                    ELECTX27
   33 H=R(1)-EARTHR                                                     ELECTX28
      PXPR=0.                                                           ELECTX29
      IF (H.GE.HPC(NOC)) GO TO 12                                         ELECTX30
      X=0.                                                              ELECTX31
!      IF(FN2C(1,JLAT,JLON).EQ.0.) GO TO 50                             GPROF000
!      X=FN2C(1,JLAT,JLON)*EXP(A*(H-HPC(1)))/F2                         GPROF000
!      PXPR=A*X                                                         ELECTX32
      GO TO 50                                                          ELECTX33
   12 IF (H.GE.HPC(NOC)) GO TO 18                                       ELECTX34
      NH=2                                                              ELECTX35
      NSTEP=1                                                           ELECTX36
      IF (H.LT.HPC(NH-1)) NSTEP=-1                                      ELECTX37
   15 IF (HPC(NH-1).LE.H.AND.H.LT.HPC(NH)) GO TO 16                     ELECTX38
      NH=NH+NSTEP                                                       ELECTX39
      GO TO 15                                                          ELECTX40
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
   18 X=FN2C(NOC,JLAT,JLON)/F2                                          GPROF000
   50 IF (PERT.NE.0.) CALL ELECT1                                       ELECTX42
!*******************************************************************************
!
!ALEX: Se ha establecido un ERROR debido a una condición demasiado restrictiva
!      por lo cual la impresión en pantalla de las coordenadas para el radio 
!      de la onda R (1), R (2), R (3)cuando ocurrido el transmisor estaba en
!      la parte superior del receptor, es decir, H.GE.RCVRH.
!*******************************************************************************
!      IF (X.EQ.0..AND.H.GE.RCVRH) PRINT 1234, R(1),R(2),R(3)           ELECTX43
      IF (X.EQ.0.) PRINT 1234, R(1),R(2),R(3)                           AZZ
!*******************************************************************************
     
 1234 FORMAT (3(2X,F20.10))                                             ELECTX44
      WRITE(6,1704) R(1),R(2),R(3),R(4),R(5),R(6)                       ELECTX45
 1704 FORMAT (6(X,'R=',X,F15.10))                                             ELECTX46
      RETURN                                                            ELECTX47
      END                                                               -
!*******************************************************************************

