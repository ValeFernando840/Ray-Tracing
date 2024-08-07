!     
! File:   Sub_Rindex.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:52
!

!******************************************************************************
      SUBROUTINE RINDEX                                                 NFNC001
!          CALCULATES THE REFRACTIVE INDEX AND ITS GRADIENT USING THE   NFNC002
!          APPLETON-HARTREE FORMULA -- NO FIELD, NO COLLISIONS          NFNC003
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RADIAN,K,C,LOGTEN                NFNC004
      COMMON /RIN/ MODRIN(3),COLL,FIELD,SPACE,KAY2,KAY2I,               NFNC005
     1               HI,PHPT,PHPTI,PHPR,PHPRI,PHPTH,PHPTHI,PHPPH,PHPPHI,NFNC006
     2             PHPOM,PHPOMI,PHPKR,PHPKRI,PHPKTH,PHPKTI,PHPKPH,PHPKPINFNC007
     3            ,KPHPK,KPHPKI,POLAR,POLARI,LPOLAR,LPOLRI              NFNC008   
      COMMON /XX/ MODX(2),X,PXPR,PXPTH,PXPPH,PXPT,HMAX                  NFNC009
      COMMON /YY/ MODY,Y(16)  /ZZ/ MODZ,Z(4)                            NFNC010
      COMMON /RK/ N,STEP,MODE,E1MAX,E1MIN,E2MAX,E2MIN,FACT,RSTART       NFNC011
!     COMMON R,TH,PH,KR,KTH,KPH,ZZZZZ(14),T,STP,DRDT(20),N2             NFNC012
      COMMON R(20),T,STP,DRDT(20),N2                                    NFNC012
     
      COMMON /WW/ ID,W0,W(400)                                          
      EQUIVALENCE (RAY,W(1)),(F,W(6))                                   NFNC013
      EQUIVALENCE (KR,R(4)),(KTH,R(5)),(KPH,R(6))                       NFNC013BIS
     
      LOGICAL SPACE                                                     NFNC014
      REAL N2,NNP,KR,KTH,KPH,K2,KPHPK,KPHPKI,KAY2,KAY2I,LPOLAR,LPOLRI   NFNC015
      DATA MODRIN(1)/4HAPPL/,MODRIN(2)/4H-HAR/,MODRIN(3)/4H FOR/,COLL/0.NFNC016
     1/
      DATA  FIELD/0./, KAY2I/0./, HI/0./, PHPTI/0./, PHPRI/0./          NFNC017
      DATA  PHPTHI/0./, PHPPHI/0./, PHPOMI/0./, PHPKRI/0./, PHPKTI/0./  NFNC018
      DATA  PHPKPI/0./, KPHPKI/0./, POLAR/0./, POLARI/1./, LPOLAR/0./   NFNC019
      DATA  LPOLRI/1./                                                  NFNC020
      DATA  X/0./, PXPR/0./, PXPTH/0./, PXPPH/0./, PXPT/0./             NFNC021
      DATA  MODY/1H /, MODZ/1H /                                        NFNC022
      DATA  NNP/1./, PNPX/-0.5/, PNPVR/0./, PNPVTH/0./, PNPVPH/0./      NFNC023
     
! ******************************************************************************
      DOUBLE PRECISION ONE                                              NFNC024
! ******************************************************************************
     
      OM=PIT2*1.E6*F                                                    NFNC025
      C2=C*C                                                            NFNC026
      K2=KR*KR+KTH*KTH+KPH*KPH                                          NFNC027
      OM2=OM*OM                                                         NFNC028
      VR =(C/OM)*KR                                                     NFNC029
      VTH=(C/OM)*KTH                                                    NFNC030
      VPH=(C/OM)*KPH                                                    NFNC031
      CALL ELECTX                                                       NFNC032
      PNPR =PNPX*PXPR                                                   NFNC033
      PNPTH=PNPX*PXPTH                                                  NFNC034
      PNPPH=PNPX*PXPPH                                                  NFNC035
! Calculo del Indice de reflexion n^2=1-X  con X=fcn^2/f^2      
      PNPT=PNPX*PXPT                                                    NFNC036
      N2=1.-X                                                           NFNC037
      WRITE(6,1707) X,N2                                                BIA
 1707 FORMAT (1X,'X=',E20.10,2X,'Ne2=',E20.10)                          BIA
 
      
     
! ******************************************************************************
!     CARLO&ALEX: Se si vogliono smussare le oscillazioni numeriche spurie      
!                 allora si devono evitare le divergenze,               
!                 sottostimando l'indice di rifrazione nel vuoto ONE,   
!                 idealmente pari ad 1.,                                
!                 di una varianza infinitesimale paragonabile           
!                 al maximum allowable single step error E1MAX.         
! ******************************************************************************
!      SPACE=N2.EQ.1.                                                   NFNC038
      ONE=1.                                                            NEW: ALEX
      ONE=ONE-E1MAX                                                         NEW: ALEX
      SPACE=N2.EQ.ONE                                                           NFNC038
! ******************************************************************************
     
      KAY2=(OM2/C2)*N2                                                  NFNC039
      IF(RSTART.EQ.0.) GO TO 1                                          NFNC040
      SCALE=SQRT(KAY2/K2)                                               NFNC041
      KR =SCALE*KR                                                      NFNC042
      KTH=SCALE*KTH                                                     NFNC043
      KPH=SCALE*KPH                                                     NFNC044
  1   CONTINUE                                                          NFNC045
!********* CALCULATES A HAMILTONIAN H                                   NFNC046
      H=.5*(C2*K2/OM2-N2)                                               NFNC047
!********* AND ITS PARTIAL DERIVATIVES WITH RESPECT TO                  NFNC048
!********* TIME, R, THETA, PHI, OMEGA, KR, KTHETA, AND KPHI.            NFNC049
      PHPT =-PNPT                                                       NFNC050
      PHPR =-PNPR                                                       NFNC051
      PHPTH=-PNPTH                                                      NFNC052
      PHPPH=-PNPPH                                                      NFNC053
      PHPOM=-NNP/OM                                                     NFNC054
      PHPKR =C2/OM2*KR                                                  NFNC055
      PHPKTH=C2/OM2*KTH                                                 NFNC056
      PHPKPH=C2/OM2*KPH                                                 NFNC057
      KPHPK=N2                                                          NFNC058
      RETURN                                                            NFNC059
         END                                                            NFNC060-
!*******************************************************************************
