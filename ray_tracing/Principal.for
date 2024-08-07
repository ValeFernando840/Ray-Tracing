!     
! File:   Principal.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:36
!

      PROGRAM NITIAL                                                    NITI001
!          SETS THE INITIAL CONDITIONS FOR EACH RAY AND CALLS TRACE     NITI002
      DIMENSION MFLD(2)                                                 NITI003
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                   NITI004
      COMMON /FLG/ NTYP,PENET,IHOP,HPUNCH                               NITI005
      COMMON /RIN/ MODRIN(3),COLL,FIELD7,SPACE,ZZN,N2I,PNP(10),POLAR,    NITI006
     1             LPOLAR,SGN,SKIP                                           NITI007
      COMMON /RK/ N,STEP,MODE,E1MAX,E1MIN,E2MAX,E2MIN,FACT,RSTART       NITI008
      COMMON /XX/ MODX(2),X,PXPR,PXPTH,PXPPH,PXPT,HMAX                  NITI009
      COMMON /YY/ MODY,Y(16) /ZZ/ MODZ,Z(4)                             NITI010
      COMMON R(20),T,STP,DRDT(20),N2                                    NITI011
      COMMON /WW/ ID,W0,W(400)                                          
      EQUIVALENCE (RAY,W(1)),(EARTHR,W(2)),(XMTRH,W(3)),(TLAT,W(4)),    NITI012
     1 (TLON,W(5)),(F,W(6)),(FBEG,W(7)),(FEND,W(8)),(FSTEP,W(9)),       NITI013
     2 (AZ1,W(10)),(AZBEG,W(11)),(AZEND,W(12)),(AZSTEP,W(13)),          NITI014
     3 (BETA,W(14)),(ELBEG,W(15)),(ELEND,W(16)),(ELSTEP,W(17)),         NITI015
     4 (ONLY,W(21)),(HOP,W(22)),(MAXSTP,W(23)),(PLAT,W(24)),(PLON,W(25))NITI016
     5,(MDE,W(26)),(INTYP,W(41)),(MAXERR,W(42)),(ERATIO,W(43)),         NITI017
     6 (STEP1,W(44)),(STPMAX,W(45)),(STPMIN,W(46)),(FACTR,W(47))        NITI018
!                                                                       NITI019
      LOGICAL SPACE,PENET                                               NITI020
      REAL N2,N2I,LOGTEN,K,MAXSTP,INTYP,MAXERR,MU                       NITI021
      COMPLEX PNP,POLAR,LPOLAR                                          NITI022
      CHARACTER (len=19) aux,aux1
!******************************************************************************
      OPEN(16,FILE='raytracing.txt',STATUS='unknown')
      
      OPEN(6,FILE='DATA_OUT.txt',STATUS='unknown')                      
      
      !OPEN(56,FILE='CONFI_IRI.txt',STATUS='unknown')    
      
      ID=4H X00                                                         NITI023
      NDATE=4H21OT                                                      NITI024
  !    WRITE(6,999) ID,NDATE                                             NITI025
  !999 FORMAT (A4,1X,A4,/)                                               NITI026
      KOLL=4H  NO                                                       NITI027
      aux1='RAY TRACING 3D'
      aux='ZENON SAAVEDRA 2016'
      WRITE(6,999)aux,aux1
  999 FORMAT(X,A19,/,X,A19,/)
      !WRITE(6,'(X,G10.5,/)')SKIP
      !WRITE(6,'(X,g9.5,/)')COLL
      IF (COLL.NE.0.) KOLL=4HWITH                                       NITI028
!********* CONSTANTS                                                    NITI029
      PI=3.1415926536                                                   NITI030
      PIT2=2.*PI                                                        NITI031
      PID2=PI/2.                                                        NITI032
      DEGS=180./PI                                                      NITI033
      RAD=PI/180.                                                       NITI034
      C=2.997925E5                                                      NITI035
      K=2.81785E-15*C**2/PI                                             NITI036
      LOGTEN=ALOG(10.)                                                  NITI037
!********* INITIALIZE SOME VARIABLES IN THE W ARRAY                     NITI038
      DO 5 NW=1,400                                                     NITI039
    5 W(NW)=0.                                                          NITI040
      PLON=0.                                                           NITI041
      PLAT=PID2                                                         NITI042
      EARTHR=6371.                                                      NITI043
      INTYP=3.                                                          NITI044
      MAXERR=1.E-4                                                      NITI045
      ERATIO=50.                                                        NITI046
      STEP1=1.                                                          NITI047
      STPMAX=100.                                                       NITI048
      STPMIN=1.E-8                                                      NITI049
      FACTR=0.5                                                         NITI050
      MAXSTP=1000.                                                      NITI051
      HOP=1.                                                            NITI052
!********* READ W ARRAY AND WRITE NON-ZERO VALUES                       NITI053
      
      CALL READW                                                        NITI054
      !WRITE(6,'(X,G10.5,/)')SKIP
      !WRITE(6,'(X,L2,/)')(SKIP.EQ.0.)
      IF (SKIP.EQ.0.) SKIP=MAXSTP                                       NITI056
   12 RAY=SIGN(1.,RAY)                                                  NITI057
      
      NTYP=2.+FIELD*RAY                                                 NITI058
!      WRITE(6,'(X,G5.4,/)')NTYP
      GO TO (13,14,15), NTYP                                            NITI059
   13 MFLD(1)=4HEXTR                                                    NITI060
      MFLD(2)=4HORDI                                                    NITI061
      GO TO 16                                                          NITI062
   14 MFLD(1)=4HNO F                                                    NITI063
      MFLD(2)=4H----                                                    NITI064
      GO TO 16                                                          NITI065
   15 MFLD(1)=4HORDI                                                    NITI066
      MFLD(2)=4H----                                                    NITI067
   16 MODSAV=MODX(2)                                                    NITI068
      IF (PERT.EQ.0.) MODX(2)=4H  NO                                    NITI069
!    
      WRITE(6,1050)                                                     NITI077
 1050 FORMAT (85H INITIAL VALUES FOR THE W ARRAY -- ALL ANGLES IN RADIANNITI078
     1S, ONLY NONZERO VALUES PRINTED/)                                  NITI079
      DO 17 NW=1,400                                                    NITI080
      IF (W(NW).NE.0.) WRITE(6,1700) NW,W(NW)                           NITI081
 1700 FORMAT (I4,E20.10,/)                                              NITI082
   17 CONTINUE                                                          NITI083
!******************************************************************************
!********* INITIALIZE PARAMETERS FOR INTEGRATION SUBROUTINE RKAM        NITI087
      N=6                                                               NITI088
      DO 20 NR=7,20                                                     NITI089
      IF (W(50+NR).NE.0.) N=N+1                                         NITI090
! write(6,'(x,G5.6,/)')N
   20 CONTINUE                                                          NITI091
      MODE=INTYP                                                        NITI092
      STEP=STEP1                                                        NITI093
      E1MAX=MAXERR                                                      NITI094
      E1MIN=MAXERR/ERATIO                                               NITI095
      E2MAX=STPMAX                                                      NITI096
      E2MIN=STPMIN                                                      NITI097
      FACT=FACTR                                                        NITI098
!******************************************************************************
!********* DETERMINE TRANSMITTER LOCATION IN COMPUTATIONAL COORDINATE   NITI099
!********* SYSTEM (GEOMAGNETIC COORDINATES IF DIPOLE FIELD IS USED)     NITI100
      R0=EARTHR+XMTRH                                                   NITI101
      SP=SIN (PLAT)                                                     NITI102
      CP=SIN (PID2-PLAT)                                                NITI103
      SDPH=SIN (TLON-PLON)                                              NITI104
      CDPH=SIN (PID2-(TLON-PLON))                                       NITI105
      SL=SIN (TLAT)                                                     NITI106
      CL=SIN (PID2-TLAT)                                                NITI107
!*****Diferencia entre el eje geografico y magnetico     
      ALPHA=ATAN2(-SDPH*CP,-CDPH*CP*SL+SP*CL)                           NITI108
!*****Coordenada de Longitud del radar     
      TH0=ACOS (CDPH*CP*CL+SP*SL)                                       NITI109
!*****Coordenada de Co-latitud del radar     
      PH0=ATAN2(SDPH*CL,CDPH*SP*CL-CP*SL)                               NITI110
!***************************************************************
!********* LOOP ON FREQUENCY, AZIMUTH ANGLE, AND ELEVATION ANGLE        NITI111
      NFREQ=1                                                           NITI112
      IF (FSTEP.NE.0.) NFREQ=(FEND-FBEG)/FSTEP+1.5                      NITI113
      NAZ=1                                                             NITI114
      IF (AZSTEP.NE.0.) NAZ=(AZEND-AZBEG)/AZSTEP+1.5                    NITI115
      NBETA=1                                                           NITI116
      IF (ELSTEP.NE.0.) NBETA=(ELEND-ELBEG)/ELSTEP+1.5                  NITI117
      
      DO 50 NF=1,NFREQ                                                  NITI118
      F=FBEG+(NF-1)*FSTEP                                               NITI119
      DO 45 J=1,NAZ                                                     NITI120
      AZ1=AZBEG+(J-1)*AZSTEP                                            NITI121
      AZA=AZ1*DEGS                                                      NITI122
      GAMMA=PI-AZ1+ALPHA                                                NITI123
      SGAMMA=SIN (GAMMA)                                                NITI124
      CGAMMA=SIN (PID2-GAMMA)                                           NITI125
      DO 40 I=1,NBETA                                                   NITI126
      BETA=ELBEG+(I-1)*ELSTEP                                           NITI127
      EL=BETA*DEGS                                                      NITI128
      CBETA=SIN (PID2-BETA)                                             NITI129
      R(1)=R0                                                           NITI130
      R(2)=TH0                                                          NITI131
      R(3)=PH0                                                          NITI132
      R(4)=SIN (BETA)                                                   NITI133
      R(5)=CBETA*CGAMMA                                                 NITI134
      R(6)=CBETA*SGAMMA                                                 NITI135
      T=0.                                                              NITI136
      RSTART=1.                                                         NITI137
!     SGN=1.  (NEED FOR RAY TRACING IN COMPLEX SPACE.)                  NITI138
!********* ALLOW IONOSPHERIC MODEL SUBROUTINES TO READ AND WRITE DATA   NITI139
!      !     Salida de Datos (ALTITUD, LATITUD, LONGITUD)      
!      WRITE(16,3458)R(1),R(2),R(3)
! 3458 FORMAT(3(2X,F20.10))     

      CALL RINDEX                                                       NITI140  

      WRITE(6,3560)MODX(1),MODX(2)
 3560 FORMAT(/,X,'PERFIL =',A4,/,X,'PERTURBACIONES =',A4)     
      WRITE(6,3561)MFLD(1),KOLL
 3561 FORMAT(X,'---:',A4,/,X,'COLICIONES =',A4)     
      WRITE(6,3562)MODRIN(3),MODRIN(1),MODRIN(2)
 3562 FORMAT(X,'REFLEX.INDEX =',A4,X,A4,A4)           
      WRITE(6,2400)F,AZA                                               NITI144
 2400 FORMAT(X,'FRECUENCIA =',F10.5,'MHz'
     1,/,X,'AZIMUTH ANGLE OF TRANSMISSION =',F10.5,'º')
      WRITE(6,2500) EL                                                  NITI148
 2500 FORMAT(X,'ELEVATION ANGLE OF TRANSMISSION =',F10.5,'º',/)         NITI149
 
      IF (N2.GT.0.) GO TO 30                                            NITI150
      CALL ELECTX                                                       NITI151
      FN=SIGN (SQRT (ABS (X))*F,X)                                      NITI152     
!*******************************************************************************
!    PRINT 2900,FN                                                     SET
! 2900 FORMAT (6H 333.3,18X,F20.10,9X,3H 3 )                             SET
      WRITE(6,2901) FN                                                  NITI153
 2901 FORMAT (33H TRANSMITTER IN EVANESCENT REGION,':',/                NITI154
     1,24H TRANSMISSION IMPOSSIBLE,',',/                                NITI155
     2,20H PLASMA FREQUENCY = ,E20.10,4H MHz,'.')                       NITI155
!*******************************************************************************    
!*******************************************************************************
      CALL ZEROZ                                                         AZZ
!*******************************************************************************         
      GO TO 45                                                          NITI156
   30 MU=SQRT (N2/(R(4)**2+R(5)**2+R(6)**2))                            NITI157
      DO 34 NN=4,6                                                      NITI158
   34 R(NN)=R(NN)*MU                                                    NITI159
      DO 35 NN=7,N                                                      NITI160
   35 R(NN)=0.                                                          NITI161
      CALL TRACE                                                        NITI162
!*****CALCULO DE RETARDO DE GRUPO****                                 NITI163
      C_km_ms=C/1000.0                                                  NITI164
      GRPDELAY=T/C_km_ms                                                NITI165
      WRITE (16,3502) GRPDELAY,T,T                                      NITI166A
 3502 FORMAT (2X,F20.10,2X,F20.10,2X,F20.10)                            NITI167A
 !     WRITE (16,3504) T                                                  NITI166B
 !3504 FORMAT (15H GROUP PATH  IS,5X,F20.10,4H  km)                      NITI167B
      IF (PENET.AND.ONLY.NE.0..AND.IHOP.EQ.1) GO TO 45                  NITI168
!*******************************************************************************
      CALL ZEROZ                                                                 AZZ
!*******************************************************************************  
   40 CONTINUE                                                          NITI169
   45 CONTINUE                                                          NITI171
      IF(PENET.AND.ONLY.NE.0..AND.IHOP.EQ.1.AND.NAZ.EQ.1.AND.NBETA.EQ.1)NITI172
     1 GO TO 55                                                         NITI173
   50 CONTINUE                                                          NITI174
   55 WRITE(6,*)'THE END'                                               NITI175
      !CLOSE(56)
      END                                                               NITI176-
!     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
!     +++                          NITI END                          +++
!     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

