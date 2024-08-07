!     
! File:   Sub_Graze.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:48
!

!******************************************************************************
          SUBROUTINE GRAZE(HS)                                          GRAZ001
      COMMON /RK/ N,STEP,MODE,E1MAX,E1MIN,E2MAX,E2MIN,FACT,RSTART       GRAZ002
      COMMON /TRAC/ GROUND,PERIGE,THERE,MINDIS,NEWRAY,SMT               GRAZ003
      COMMON R(20),T,STP,DRDT(20),N2                                    GRAZ004
      COMMON /WW/ ID,W0,W(400)                                          
      EQUIVALENCE (EARTHR,W(2)),(INTYP,W(41)),(STEP1,W(44))             GRAZ005
      REAL INTYP                                                        GRAZ006
      LOGICAL GROUND,PERIGE,THERE,MINDIS,NEWRAY                         GRAZ007
!    
      THERE=.FALSE.                                                     GRAZ027
!********* DIAGNOSTIC PRINTOUT                                          GRAZ028
      WRITE(6,*)'(8HGRAZE 0 ,0.)'                                       GRAZ029
      IF (SMT.GT.ABS(R(1)-EARTHR-HS)) GO TO 30                          GRAZ030
      DO 20 I=1,10                                                      GRAZ031
      STEP=-R(4)/DRDT(4)                                                GRAZ032
     
!*******************************************************************************
!     NB: La variabile STP è definita ma non inizializzata,             
!         quindi si omette la seguente istruzione                       
!         che potrebbe dar luogo a valori aleatori.                     
!*******************************************************************************
!      STEP=SIGN(AMIN1(ABS(STP),ABS(STEP)),STEP)                         GRAZ033
!*******************************************************************************
     
      IF (ABS(R(4)).LE.1.E-6.AND.ABS(STEP).LT.1.) GO TO 60              GRAZ034
!********* DIAGNOSTIC PRINTOUT                                          GRAZ035
      WRITE(6,*)'(8HGRAZE 1 ,0.)'                                       GRAZ036
      MODE=1                                                            GRAZ037
      RSTART=1.                                                         GRAZ038
      CALL RKAM                                                         GRAZ039
      RSTART=1.                                                         GRAZ040
      IF (DRDT(4)*(R(1)-EARTHR-HS).LT.0.) GO TO 30                      GRAZ041
      IF(R(5).EQ.0..AND.R(6).EQ.0.) GO TO 60                            GRAZ042
   20 CONTINUE                                                          GRAZ043
!********* IF A CLOSEST APPROACH COULD NOT BE FOUND IN 10 STEPS, IT     GRAZ044
!********* PROBABLY MEANS THAT THE RAY INTERSECTS THE HEIGHT HS         GRAZ045
   30 CONTINUE                                                          GRAZ046
!********* DIAGNOSTIC PRINTOUT                                          GRAZ047
      WRITE(6,*)' (8HBACK UP2,0.)'                                      GRAZ048
      MODE=1                                                            GRAZ049
!********* ESTIMATE DISTANCE TO NEAREST INTERSECTION OF RAY WITH HEIGHT GRAZ050
!********* HS BEHIND THE PRESENT RAY POINT                              GRAZ051
     
!*******************************************************************************
!     ERRATA CORRIGE DA DISPENSE DI JONES STEVENSON                     
!*******************************************************************************
!      STEP=(-R(4)-SQRT(R(4)**2-2.*(R(1)-EARTHR-HS)*DRDT(4)))/DRDT(4)    GRAZ052
      H=R(1)-EARTHR                                                     GRAZ052BIS
      STEP=(-R(4)-SQRT(R(4)**2-2.*(H-HS)*R(4)/DRDT(1)*DRDT(4)))/DRDT(4) GRAZ052TRIS
!*******************************************************************************
     
      RSTART=1.                                                         GRAZ053
      CALL RKAM                                                         GRAZ054
      RSTART=1.                                                         GRAZ055
!********* FIND NEAREST INTERSECTION OF RAY WITH HEIGHT HS              GRAZ056
      DO 40 I=1,10                                                      GRAZ057
      STEP=-(R(1)-EARTHR-HS)/DRDT(1)                                    GRAZ058
     
!*******************************************************************************
!     NB: La variabile STP è definita ma non inizializzata,             
!         quindi si omette la seguente istruzione                       
!         che potrebbe dar luogo a valori aleatori.                     
!*******************************************************************************
!      STEP=SIGN(AMIN1(ABS(STP),ABS(STEP)),STEP)                         GRAZ059
!*******************************************************************************
     
!*******************************************************************************
!     ERRATA CORRIGE DA DISPENSE DI JONES STEVENSON                     
!*******************************************************************************
!      IF(ABS(R(1)-EARTHR-HS).LT..5E-4.AND.ABS(STEP).LT.1.) GO TO 60     GRAZ060
      IF(ABS(R(1)-EARTHR-HS).LT..5E-4.AND.ABS(STEP).LT.1.) GO TO 50     GRAZ060BIS
!*******************************************************************************
     
!********* DIAGNOSTIC PRINTOUT                                          GRAZ061
      WRITE(6,*)'(8HBACK UP3,0.)'                                       GRAZ062
      MODE=1                                                            GRAZ063
      RSTART=1.                                                         GRAZ064
      CALL RKAM                                                         GRAZ065
   40 RSTART=1.                                                         GRAZ066
   50 THERE=.TRUE.                                                      GRAZ067
!********* RESET STANDARD MODE AND INTEGRATION TYPE                     GRAZ068
   60 MODE=INTYP                                                        GRAZ069
      STEP=STEP1                                                        GRAZ070
      RETURN                                                            GRAZ071
         END                                                            GRAZ072-
!******************************************************************************
