!     
! File:   Sub_Trace.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:42
!

!*******************************************************************************
      SUBROUTINE TRACE                                                  TRAC001
!     CALCULATES THE RAY PATH                                           TRAC002
      DIMENSION ROLD(20),DROLD(20)                                      TRAC003
      COMMON /RK/ N,STEP,MODE,E1MAX,E1MIN,E2MAX,E2MIN,FACT,RSTART       TRAC004
      COMMON /FLG/ NTYP,PENET,IHOP,HPUNCH                               TRAC005
      COMMON /TRAC/ GROUND,PERIGE,THERE,MINDIS,NEWRAY,SMT               TRAC006
      COMMON /RIN/ MODRIN(3),COLL,FIELD,SPACE,ZZN,PNP(10),POLAR,LPOLAR  TRAC007
      COMMON /XX/ MODX(2),X,PXPR,PXPTH,PXPPH,PXPT,HMAX                  TRAC008
      COMMON R(20),T,STP,DRDT(20),N2                                    TRAC009
      COMMON /WW/ ID,W0,W(400)                                          
      LOGICAL SPACE,HOME,WASNT,GROUND,PERIGE,THERE,MINDIS,PENET,NEWRAY, TRAC010
     1WAS                                                               TRAC011
      REAL MAXSTP                                                       TRAC012
      COMPLEX N2,PNP,POLAR,LPOLAR                                       TRAC013
      EQUIVALENCE (EARTHR,W(2)),(RCVRH,W(20)),(HOP,W(22)),(MAXSTP,W(23))TRAC014
     
!*******************************************************************************
!     ALEX: Per ogni iterazione di raytracing,                          
!           è stato necessario introdurre                               
!           una variabile logica di controllo                           
!           che forzasse, una ed una sola volta, la stampa              
!           su file dell'input '+++ RAY OUT THE IONOSPHERE +++'         
!           e da schermo della coordinata speciale '111.1 0 3'.         
!*******************************************************************************
      LOGICAL OUT                                                       
!      IF (NEWRAY) OUT=.FALSE.                                           
      OUT=.FALSE.                                                       
!*******************************************************************************
     
      NHOP=HOP                                                          TRAC016
      MAX=MAXSTP                                                        TRAC017
!                                                                       TRAC018
      RSTART=1.                                                         TRAC019
      CALL HAMLTN                                                       TRAC020
      HOME=DRDT(1)*(R(1)-EARTHR-RCVRH).GE.0.                            TRAC021
!*********                                                              TRAC022
!*********                                                              TRAC023
      IHOP=0                                                            TRAC024
     
      WRITE(6,1701)W(3),RCVRH,NHOP,MAXSTP,HOME 
 1701 FORMAT (/,X,'INICIA TRACE DESDE UNA ALTURA (TX)=',F10.5,/
     1,X,'INICIA TRACE DESDE UNA ALTURA (RX)=',F10.5,/
     2,X,'NHOP=',I4,/,X,'MAX.PASO=',F10.5,/,X,'HOME=',L4,/)      
     
      HTMAX=0.                                                          TRAC027
      NEWRAY=.TRUE.                                                     TRAC028
      THERE=R(1)-EARTHR.EQ.RCVRH                                        TRAC029
!********* LOOP ON NUMBER OF HOPS                                       TRAC030
   10 IHOP=IHOP+1                                                       TRAC031
      
      IF (IHOP.GT.NHOP) RETURN                                          TRAC032
      PENET=.FALSE.                                                     TRAC033
      APHT=RCVRH                                                        TRAC034
!********* LOOP ON MAXIMUM NUMBER OF STEPS PER HOP                      TRAC035
      DO 79 J=1,MAX                                                     TRAC036
      H=R(1)-EARTHR                                                     TRAC037
      IF (ABS(H-RCVRH).GT.ABS(APHT-RCVRH)) APHT=H                       TRAC038
      HTMAX=AMAX1(H,HTMAX)                                              TRAC039
      IF (.NOT.SPACE) GO TO 12                                          TRAC040
      CALL REACH                                                        TRAC041
      RSTART=1.                                                         TRAC042
      H=R(1)-EARTHR                                                     TRAC043
      IF (ABS(H-RCVRH).GT.ABS(APHT-RCVRH)) APHT=H                       TRAC044
      HTMAX=AMAX1(H,HTMAX)                                              TRAC045
      IF (.NOT.SPACE) GO TO 12                                          TRAC046
      IF (PERIGE) WRITE (6,*)'PERIGEE'                                  TRAC047
      IF (THERE) GO TO 51                                               TRAC048
      IF (MINDIS) GO TO 40                                              TRAC049
      IF (GROUND) GO TO 60                                              TRAC050
! *****     QUI CHIAMAVA RAYPLOT                                        TRAC051
      IF (PERIGE) GO TO 79                                              TRAC052
      
      
 

      
      !************************************************************************
      !!! Actualizacion del R,theta,phi,k_R,k_theta,k_phi
   12 DO 13 L=1,N                                                       TRAC053
      ROLD(L)=R(L)                                                      TRAC054
   13 DROLD(L)=DRDT(L)                                                  TRAC055
      TOLD=T                                                            TRAC056
      WAS=THERE                                                         TRAC057
      CALL RKAM                                                         TRAC058
     
!*******************************************************************************
      WRITE(6,*) 'BEFORE: OUT=', OUT                                            AZZ
      IF((.NOT.OUT).AND.(.NOT.PENET).AND.SPACE.AND.(DRDT(1).LT.0.))THEN         AZZ
      OUT=.TRUE.                                                                AZZ
    ! PRINT *,'111.1 0 3'                                                       AZZ
      WRITE(6,*) '+++ RAY OUT THE IONOSPHERE +++'                               AZZ
      ENDIF                                                                     AZZ
      WRITE(6,*) 'AFTER: OUT=', OUT                                             AZZ
!*******************************************************************************
   

            
!     Salida de Datos (ALTITUD, LATITUD, LONGITUD)      
      WRITE(16,3561)R(1),R(2),R(3)
 3561 FORMAT(3(2X,F20.10))     
      
     
      
      WRITE (6,1703) R(1),R(2),R(3),R(4),R(5),R(6)                         	BIA
 1703 FORMAT (8H TRAC000,/,6(2X,F20.10))                                        BIA
      H=R(1)-EARTHR                                                     TRAC059
      THERE=.FALSE.                                                     TRAC060
      WASNT=.NOT.HOME                                                   TRAC061
      HOME=DRDT(1)*(H-RCVRH).GE.0.                                      TRAC062
      TMP=(DRDT(1)-DROLD(1))*(T-TOLD)                                   TRAC063
      SMT=0.                                                            TRAC064
      IF (TMP.NE.0.) SMT=0.5*(R(1)-ROLD(1)+0.5*TMP)**2/ABS(TMP)         TRAC065
      IF (((H-RCVRH)*(ROLD(1)-EARTHR-RCVRH).LT.0..AND..NOT.WAS).OR.     TRAC066
     1 (WAS.AND.DRDT(1)*DROLD(1).LT.0..AND.HOME)) GO TO 50              TRAC067
      IF (HOME.AND.WASNT) GO TO 30                                      TRAC068
      IF (H.LT.0..OR.DRDT(1).GT.0..AND.DROLD(1).LT.0..AND.SMT.GT.H)     TRAC069
     1 GO TO 20                                                         TRAC070
      IF (DROLD(1).LT.0..AND.DRDT(1).GT.0.) WRITE(6,*)'PERIGEE'         TRAC071
      IF (DROLD(1).GT.0..AND.DRDT(1).LT.0.) THEN                        TRAC072
!      PRINT *,'111.1 0 2'                                                       AZZ
      WRITE(6,*)'APOGEE'                                                        AZZ
      ENDIF                                                                     AZZ
      IF (DROLD(2)*DRDT(2).LT.0.) WRITE(6,*)'REACHED MAX LAT'           TRAC073
      IF (DROLD(3)*DRDT(3).LT.0.) WRITE(6,*)'REACHED MAX LONG'          TRAC074
      DO 14 I=4,6                                                       TRAC075
      IF (ROLD(I)*R(I).LT.0.) WRITE(6,*)'WAVE REVERSE'                  TRAC076
   14 CONTINUE                                                          TRAC077
      GO TO 75                                                          TRAC078
!********* RAY WENT UNDERGROUND                                         TRAC079
   20 CALL BACK UP(0.)                                                  TRAC080
      GO TO 60                                                          TRAC081
!********* RAY MAY HAVE MADE A CLOSEST APPROACH                         TRAC082
   30 CALL GRAZE(RCVRH)                                                 TRAC083
      IF (THERE) GO TO 51                                               TRAC084
   40 DRDT(1)=0.                                                        TRAC085
      HPUNCH=R(1)-EARTHR                                                TRAC086
     
!*******************************************************************************
!      PRINT *,'222.2 0 1'                                                       AZZ
      WRITE(6,*)'CLOSEST APPROACH : MIN. DIST.'                         TRAC087
!*******************************************************************************
     
      IF (IHOP.GE.NHOP) RETURN                                          TRAC089
      IHOP=IHOP+1                                                       TRAC090
     
!*******************************************************************************
!      PRINT *,'222.2 0 1'                                                       AZZ
      WRITE(6,*)'CLOSEST APPROACH : MIN. DIST.'                         TRAC091
!*******************************************************************************
     
      GO TO 89                                                          TRAC092
!********* RAY CROSSED RECEIVER HEIGHT                                  TRAC093
   50 CALL BACK UP(RCVRH)                                               TRAC094
      THERE=.TRUE.                                                      TRAC095
   51 R(1)=EARTHR+RCVRH                                                 TRAC096
      HTMAX=AMAX1(RCVRH,HTMAX)                                          TRAC097
      HPUNCH=APHT                                                       TRAC098
      WRITE(6,*)'RAY CROSSED RECEIVER HEIGHT'                           TRAC099
                                                                        TRAC100
      IF (RCVRH.NE.0.) GO TO 89                                         TRAC101
      IF (IHOP.GE.NHOP) RETURN                                          TRAC102
      IHOP=IHOP+1                                                       TRAC103
      APHT=RCVRH                                                        TRAC104
!********* GROUND REFLECT                                               TRAC105
   60 R(1)=EARTHR                                                       TRAC106
      IF (ABS(RCVRH).GT.ABS(APHT-RCVRH)) APHT=0.                        TRAC107
      R(4)=ABS (R(4))                                                   TRAC108
      DRDT(1)=ABS (DRDT(1))                                             TRAC109
      RSTART=1.                                                         TRAC110
      HPUNCH=HTMAX                                                      TRAC111
     
!*******************************************************************************
!      PRINT *,'222.2 0 2'                                                       AZZ
      WRITE(6,*)'GROUND REFLECTION'                                     TRAC112
!*******************************************************************************
!*******************************************************************************
      CALL ZEROZ                                                                 AZZ
!*******************************************************************************
      HTMAX=0.                                                          TRAC113
      IF (RCVRH.NE.0.) GO TO 65                                         TRAC114
      THERE=.TRUE.                                                      TRAC115
      HPUNCH=APHT                                                       TRAC116
      WRITE(6,*)'AT THE RECEIVER'                                       TRAC117
      GO TO 89                                                          TRAC118
   65 H=0.                                                              TRAC119
      THERE=.FALSE.                                                     TRAC120
!*********                                                              TRAC121
   75 CONTINUE                                                          TRAC122
      IF (H.GT.HMAX.AND.H.GT.RCVRH.AND.DRDT(1).GT.0.) GO TO 90          TRAC123
      IF (MOD(J,NSKIP).EQ.0) CONTINUE                                   TRAC124
   79 CONTINUE                                                          TRAC125
!********* EXCEEDED MAXIMUM NUMBER OF STEPS                             TRAC126
      HPUNCH=H                                                          TRAC127
!*******************************************************************************
!      PRINT *,'222.2 0 3'                                                       AZZ
      WRITE(6,*)'EXCEEDED MAX NUM. STEPS'                               TRAC128
!*******************************************************************************     
      RETURN                                                            TRAC129
!*********                                                              TRAC130
   89 HOME=.TRUE.                                                       TRAC131
      GO TO 10                                                          TRAC132
!********* RAY PENETRATED                                               TRAC133
   90 PENET=.TRUE.                                                      TRAC134
      HPUNCH=H                                                          TRAC135     
!*******************************************************************************
!      PRINT *,'222.2 0 0'                                                       AZZ
      WRITE(6,*)'RAY PENETRATE'                                         TRAC136
!*******************************************************************************  
      RETURN                                                            TRAC137
         END                                                            TRAC138-
!******************************************************************************

