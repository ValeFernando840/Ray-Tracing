!     
! File:   Sub_Hamltn.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:51
!
!******************************************************************************
      SUBROUTINE HAMLTN                                                 HAML001
!********* CALCULA LAS ECUACIONES DE HAMILTON PARA RAY TRACING          HAML002
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                   HAML003
!      COMMON /RIN/ MODRIN(3),COLL,FIELD,SPACE,KAY2,KAY2I,               HAML004
!     1             H,HI,PHPT,PHPTI,PHPR,PHPRI,PHPTH,PHPTHI,PHPPH,PHPPHI,HAML005
!     2             PHPOM,PHPOMI,PHPKR,PHPKRI,PHPKTH,PHPKTI,PHPKPH,PHPKPIHAML006
!     3            ,KPHPK,KPHPKI,POLAR,POLARI,LPOLAR,LPOLRI,SGN          HAML007
      COMMON /RIN/ MODRIN(3),COLL,FIELD,SPACE,KAY2,KAY2I,               HAML004
     1               HI,PHPT,PHPTI,PHPR,PHPRI,PHPTH,PHPTHI,PHPPH,PHPPHI,HAML005
     2             PHPOM,PHPOMI,PHPKR,PHPKRI,PHPKTH,PHPKTI,PHPKPH,PHPKPIHAML006
     3            ,KPHPK,KPHPKI,POLAR,POLARI,LPOLAR,LPOLRI              HAML007
     
      COMMON R(20),T,STP,DRDT(20),N2                                    HAML008
      COMMON /WW/ ID,W0,W(400)                                          
      EQUIVALENCE (TH,R(2)),(PH,R(3)),(KR,R(4)),(KTH,R(5)),(KPH,R(6)),  HAML009
     1 (DTHDT,DRDT(2)),(DPHDT,DRDT(3)),(DKRDT,DRDT(4)),(DKTHDT,DRDT(5)),HAML010
     2 (DKPHDT,DRDT(6)),(F,W(6))                                        HAML011
      REAL KR,KTH,KPH,KPHPK,KPHPKI,LPOLAR,LPOLRI,LOGTEN,K,KAY2,KAY2I    HAML012
!*****************************************************************************      
      OM=PIT2*1.E6*F                                                    HAML013
      STH=SIN(TH)                                                       HAML014
      CTH=SIN(PID2-TH)                                                  HAML015
      RSTH=R(1)*STH                                                     HAML016
      RCTH=R(1)*CTH                                                     HAML017
      CALL RINDEX                                                       HAML018
      DR1DT=-PHPKR/(PHPOM*C)                                            HAML019
      DRDT(1)=DR1DT                                                     HAML019a
      DTHDT=-PHPKTH/(PHPOM*R(1)*C)                                      HAML020
      DPHDT=-PHPKPH/(PHPOM*RSTH*C)                                      HAML021
      DKRDT=PHPR/(PHPOM*C)+KTH*DTHDT+KPH*STH*DPHDT                      HAML022
      DKTHDT=(PHPTH/(PHPOM*C)-KTH*DR1DT+KPH*RCTH*DPHDT)/R(1)            HAML023
      DKPHDT=(PHPPH/(PHPOM*C)-KPH*STH*DR1DT-KPH*RCTH*DTHDT)/RSTH        HAML024
      NR=6                                                              HAML025
!********* CALCULATION PHASE PATH                                                   HAML026
      IF (W(57).EQ.0.) GO TO 10                                         HAML027
      NR=NR+1                                                              HAML028
      DRDT(NR)=-     KPHPK/PHPOM/OM                                     HAML029
!********* CALCULATION ABSORPTION                                                   HAML030
   10 IF (W(58).EQ.0.) GO TO 15                                         HAML031
      NR=NR+1                                                           HAML032
      DRDT(NR)= 10./LOGTEN*KPHPK*KAY2I/(KR*KR+KTH*KTH+KPH*KPH)/PHPOM/C  HAML033
!********* CALCULATION DOPPLER SHIFT                                                HAML034
   15 IF (W(59).EQ.0.) GO TO 20                                         HAML035
      NR=NR+1                                                           HAML036
      DRDT(NR)=-PHPT/PHPOM/C/PIT2                                       HAML037
!********* CALCULATIONGEOMETRI CAL PATH LENGTH  *********                HAML038
   20 IF (W(60).EQ.0.) GO TO 25                                         HAML039
      NR=NR+1                                                           HAML040
      DRDT(NR)=-SQRT(PHPKR**2+PHPKTH**2+PHPKPH**2)/PHPOM   /C           HAML041
!********* OTHER CALCULATIONS                                           HAML042
   25 CONTINUE                                                          HAML043
      RETURN                                                            HAML044
         END                                                            HAML045-
!******************************************************************************
