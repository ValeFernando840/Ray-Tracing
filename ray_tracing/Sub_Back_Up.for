!     
! File:   Sub_Back_Up.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:44
!
!*******************************************************************************
      SUBROUTINE BACK UP(HS)                                            BACK001
      COMMON /RK/ N,STEP,MODE,E1MAX,E1MIN,E2MAX,E2MIN,FACT,RSTART       BACK002
      COMMON /TRAC/ GROUND,PERIGE,THERE,MINDIS,NEWRAY,SMT               BACK003
      COMMON R(20),T,STP,DRDT(20),N2                                    BACK004
      COMMON /WW/ ID,W0,W(400)                                          
      EQUIVALENCE (EARTHR,W(2)),(INTYP,W(41)),(STEP1,W(44))             BACK005
      REAL INTYP                                                        BACK006
      LOGICAL GROUND,PERIGE,THERE,MINDIS,NEWRAY,HOME                    BACK007
!********* DIAGNOSTIC PRINTOUT                                          BACK008
!        CALL PRINTR (8HBACK UP0,0.)                                    BACK009
!********* GOING AWAY FROM THE HEIGHT HS                                BACK010
      HOME=DRDT(1)*(R(1)-EARTHR-HS).GE.0.                               BACK011
      IF (HS.GT.0..AND..NOT.HOME.OR.HS.EQ.0..AND.DRDT(1).GT.0.) GO TO 30BACK012
!********* FIND NEAREST INTERSECTION OF RAY WITH THE HEIGHT HS          BACK013
      DO 10 I=1,10                                                      BACK014
      STEP=-(R(1)-EARTHR-HS)/DRDT(1)                                    BACK015
     
!*******************************************************************************
!*******************************************************************************
!      STEP=SIGN(AMIN1(ABS(STP),ABS(STEP)),STEP)                         BACK016
!*******************************************************************************
     
      IF (ABS(R(1)-EARTHR-HS).LT..5E-4.AND.ABS(STEP).LT.1.) GO TO 60    BACK017
!********* DIAGNOSTIC PRINTOUT                                          BACK018
      WRITE(6,*)'(8HBACK UP1,0.)'                                       BACK019
      MODE=1                                                            BACK020
      RSTART=1.                                                         BACK021
      CALL RKAM                                                         BACK022
   10 RSTART=1.                                                         BACK023
!********* IF A CLOSEST APPROACH COULD NOT BE FOUND IN 10 STEPS, IT     BACK044
!********* PROBABLY MEANS THAT THE RAY INTERSECTS THE HEIGHT HS         BACK045
   30 CONTINUE                                                          BACK046
!********* DIAGNOSTIC PRINTOUT                                          BACK047
      WRITE(6,*)'(8HBACK UP2,0.)'                                       BACK048
      MODE=1                                                            BACK049
!********* ESTIMATE DISTANCE TO NEAREST INTERSECTION OF RAY WITH HEIGHT BACK050
!********* HS BEHIND THE PRESENT RAY POINT                              BACK051
     
!*******************************************************************************
!     ERRATA CORRIGE DA DISPENSE DI JONES STEVENSON                     
!*******************************************************************************
!      STEP=(-R(4)-SQRT(R(4)**2-2.*(R(1)-EARTHR-HS)*DRDT(4)))/DRDT(4)    BACK052
      H=R(1)-EARTHR                                                     BACK052BIS
      STEP=(-R(4)-SQRT(R(4)**2-2.*(H-HS)*R(4)/DRDT(1)*DRDT(4)))/DRDT(4) BACK052TRIS
!*******************************************************************************
     
      RSTART=1.                                                         BACK053
      CALL RKAM                                                         BACK054
      RSTART=1.                                                         BACK055
!********* FIND NEAREST INTERSECTION OF RAY WITH HEIGHT HS              BACK056
      DO 40 I=1,10                                                      BACK057
      STEP=-(R(1)-EARTHR-HS)/DRDT(1)                                    BACK058
     
            
!*******************************************************************************
!      STEP=SIGN(AMIN1(ABS(STP),ABS(STEP)),STEP)                         BACK059
!*******************************************************************************
     
!*******************************************************************************
!     ERRATA CORRIGE DA DISPENSE DI JONES STEVENSON                     
!*******************************************************************************
!      IF(ABS(R(1)-EARTHR-HS).LT..5E-4.AND.ABS(STEP).LT.1.) GO TO 60     BACK060
      IF(ABS(R(1)-EARTHR-HS).LT..5E-4.AND.ABS(STEP).LT.1.) GO TO 50     BACK060BIS
!*******************************************************************************
     
!********* DIAGNOSTIC PRINTOUT                                          BACK061
      WRITE(6,*)'(8HBACK UP3,0.)'                                       BACK062
      MODE=1                                                            BACK063
      RSTART=1.                                                         BACK064
      CALL RKAM                                                         BACK065
   40 RSTART=1.                                                         BACK066
   50 THERE=.TRUE.                                                      BACK067
!********* RESET STANDARD MODE AND INTEGRATION TYPE                     BACK068
   60 MODE=INTYP                                                        BACK069
      STEP=STEP1                                                        BACK070
      RETURN                                                            BACK071
         END                                                            BACK072-
!******************************************************************************
