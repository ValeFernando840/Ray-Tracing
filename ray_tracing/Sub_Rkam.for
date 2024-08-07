!     
! File:   Sub_Rkam.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:51
!

!******************************************************************************
      SUBROUTINE RKAM                                                   RKAM001
!        NUMERICAL INTEGRATION OF DIFFERENTIAL EQUATIONS                RKAM002
      COMMON /RK/ NN,SPACE,MODE,E1MAX,E1MIN,E2MAX,E2MIN,FACT,RSTART     RKAM003
      COMMON Y(20),T,STEP,DYDT(20),N2                                   RKAM004
      DIMENSION DELY(4,20),BET(4),XV(5),FV(4,20),YU(5,20)               RKAM005
      DOUBLE PRECISION YU                                               RKAM006
      IF (RSTART.EQ.0.) GO TO 1000                                      RKAM007
      LL=1                                                              RKAM008a
      MM=1                                                              RKAM008b
      IF (MODE.EQ.1) MM=4                                               RKAM009
      ALPHA=T                                                           RKAM010
      EPM=0.0                                                           RKAM011
      BET(1)=0.5                                                        RKAM012a
      BET(2)=0.5                                                        RKAM012b
      BET(3)=1.0                                                        RKAM013
      BET(4)=0.0                                                        RKAM014
      STEP=SPACE                                                        RKAM015
      WRITE(6,*)'***************************'
      WRITE(6,'(/,X,F10.5,X,/)')STEP
      WRITE(6,'(/,X,L5,X,/)')STEP
      R=19.0/270.0                                                      RKAM016
      XV(MM)=T                                                          RKAM017
      IF (E1MIN.LE.0.) E1MIN=E1MAX/55.                                  RKAM018
      IF (FACT.LE.0.) FACT=0.5                                          RKAM019
      CALL HAMLTN                                                       RKAM020
      
      DO 320 I=1,NN                                                     RKAM021
      FV(MM,I)=DYDT(I)                                                  RKAM022
  320 YU(MM,I)=Y(I)                                                     RKAM023
      RSTART=1.                                                         RKAM024
      GO TO 1001                                                        RKAM025
 1000 IF (MODE.NE.1) GO TO 2000                                         RKAM026
!                                                                       RKAM027
!          RUNGE-KUTTA                                                  RKAM028
 1001 DO 1034 K=1,4                                                     RKAM029
      DO 1350 I=1,NN                                                    RKAM030
      DELY(K,I)=STEP*FV(MM,I)                                           RKAM031    
      Z=YU(MM,I)                                                        RKAM032
 1350 Y(I)=Z+BET(K)*DELY(K,I)                                           RKAM033
      T=BET(K)*STEP+XV(MM)                                              RKAM034
      CALL HAMLTN                                                       RKAM035
      DO 1034 I=1,NN                                                    RKAM036
 1034 FV(MM,I)=DYDT(I)                                                  RKAM037
 
      DO 1039 I=1,NN                                                    RKAM038
      DEL=(DELY(1,I)+2.0*DELY(2,I)+2.0*DELY(3,I)+DELY(4,I))/6.0         RKAM039
 1039 YU(MM+1, I)=YU(MM,I)+DEL                                          RKAM040
      
      MM=MM+1                                                           RKAM041
      XV(MM)=XV(MM-1)+STEP                                              RKAM042
      DO 1400 I=1,NN                                                    RKAM043
 1400 Y(I)=YU(MM,I)                                                     RKAM044
      T=XV(MM)                                                          RKAM045
      CALL HAMLTN                                                       RKAM046
      IF (MODE.EQ.1) GO TO 42                                           RKAM047
      DO 150 I=1,NN                                                     RKAM048
  150 FV(MM,I)=DYDT(I)                                                  RKAM049
      IF (MM.LE.3) GO TO 1001                                           RKAM050
!                                                                       RKAM051
!          ADAMS-MOULTON                                                RKAM052
 2000 DO 2048 I=1,NN                                                    RKAM053
      DEL=STEP*(55.*FV(4,I)-59.*FV(3,I)+37.*FV(2,I)-9.*FV(1,I))/24.     RKAM054
      Y(I)=YU(4,I)+DEL                                                  RKAM055
 2048 DELY(1,I)=Y(I)                                                    RKAM056
      T=XV(4)+STEP                                                      RKAM057
      CALL HAMLTN                                                       RKAM058
      XV(5)=T                                                           RKAM059
      DO 2051 I=1,NN                                                    RKAM060
      DEL=STEP*(9.*DYDT(I)+19.*FV(4,I)-5.*FV(3,I)+FV(2,I))/24.          RKAM061
      YU(5,I)=YU(4,I)+DEL                                               RKAM062
 2051 Y(I)=YU(5,I)                                                      RKAM063
      CALL HAMLTN                                                       RKAM064
      IF (MODE.LE.2) GO TO 42                                           RKAM065
!                                                                       RKAM066
!          ERROR ANALYSIS                                               RKAM067
      SSE=0.0                                                           RKAM068
      DO 3033 I=1,NN                                                    RKAM069
      EPSIL=R*ABS(Y(I)-DELY(1,I))                                       RKAM070
      IF (MODE.EQ.3.AND.Y(I).NE.0.) EPSIL=EPSIL/ABS(Y(I))               RKAM071
      IF (SSE.LT.EPSIL) SSE=EPSIL                                       RKAM072
 3033 CONTINUE                                                          RKAM073
      IF (E1MAX.GT.SSE) GO TO 3035                                      RKAM074
      IF (ABS(STEP).LE.E2MIN) GO TO 42                                  RKAM075
      LL=1                                                              RKAM076a
      MM=1                                                              RKAM076b
      STEP=STEP*FACT                                                    RKAM077
      GO TO 1001                                                        RKAM078
 3035 IF (LL.LE.1.OR.SSE.GE.E1MIN.OR.E2MAX.LE.ABS(STEP)) GO TO 42       RKAM079
      LL=2                                                              RKAM080
      MM=3                                                              RKAM081
      XV(2)=XV(3)                                                       RKAM082
      XV(3)=XV(5)                                                       RKAM083
      DO 5363 I=1,NN                                                    RKAM084
      FV(2,I)=FV(3,I)                                                   RKAM085
      FV(3,I)=DYDT(I)                                                   RKAM086
      YU(2,I)=YU(3,I)                                                   RKAM087
 5363 YU(3,I)=YU(5,I)                                                   RKAM088
      STEP=2.0*STEP                                                     RKAM089
      GO TO 1001                                                        RKAM090    
!                                                                       RKAM091
!          EXIT ROUTINE                                                 RKAM092
   42 LL=2                                                              RKAM093
      MM=4                                                              RKAM094
      DO 12 K=1,3                                                       RKAM095
      XV(K)=XV(K+1)                                                     RKAM096
      DO 12 I=1,NN                                                      RKAM097
      FV(K,I)=FV(K+1,I)                                                 RKAM098
   12 YU(K,I)=YU(K+1,I)                                                 R KAM099
      XV(4)=XV(5)                                                       RKAM100
      DO 52 I=1,NN                                                      RKAM101
      FV(4,I)=DYDT(I)                                                   RKAM102
   52 YU(4,I)=YU(5,I)                                                   RKAM103
      IF (MODE.LE.2) RETURN                                             RKAM104
      E=ABS(XV(4)-ALPHA)                                                RKAM105
      IF (E.LE.EPM) GO TO 2000                                          RKAM106
      EPM=E                                                             RKAM107
      RETURN                                                            RKAM108
         END                                                            RKAM109-
!******************************************************************************

