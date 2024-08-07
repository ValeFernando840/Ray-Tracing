!     
! File:   Sub_Reach.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:43
!

!******************************************************************************
      SUBROUTINE  REACH                                                  REAC001
!          CALCULATES THE STRAIGHT LINE RAY PATH BETWEEN THE EARTH      REAC002
!          AND THE IONOSPHERE OR BETWEEN IONOSPHERIC LAYERS             REAC003
      COMMON /RK/ N,STEP,MODE,E1MAX,E1MIN,E2MAX,E2MIN,FACT,RSTART       REAC004
      COMMON /TRAC/ GROUND,PERIGE,THERE,MINDIS,NEWRAY,SMT               REAC005
      COMMON /COORD/ S,X0(6),GG(6),R0(4),VERT                           REAC006
      COMMON /RIN/ MODRIN(3),COLL,FIELD,SPACE,ZZN,N2I,PNP(10),POLAR,    REAC007
     1             LPOLAR                                               REAC008
      COMMON /XX/ MODX(2),X,PXPR,PXPTH,PXPPH,PXPT,HMAX                  REAC009
      COMMON R(20),T,STP,DRDT(20),N2                                    REAC010
      COMMON /WW/ ID,W0,W(400)                                          
      EQUIVALENCE (EARTHR,W(2)),(XMTRH,W(3)),(RCVRH,W(20))              REAC011     
!*******************************************************************************
      EQUIVALENCE (STEP1,W(44)),(TH,R(2))                                       GPROF000
!      EQUIVALENCE (DTHDT,DRDT(2)),(DPHDT,DRDT(3))                               GPROF000
!*******************************************************************************     
      LOGICAL CROSS,CROSSG,CROSSR,SPACE,GROUND,PERIGE,THERE,MINDIS,     REAC012
     1        NEWRAY,RSPACE                                             REAC013
      REAL N2,N2I                                                       REAC 14
      COMPLEX PNP,POLAR,LPOLAR                                          REAC 15
      DATA  NSTEP/500/                                                  REAC 16
!*******************************************************************************
!     ALEX: Per ogni iterazione di raytracing,                          
!           è stato necessario introdurre                               
!          una variabile logica di controllo                           
!           che forzasse, una ed una sola volta, la stampa              
!           su file dell'input '+++ RAY IN THE IONOSPHERE +++'          
!           e da schermo della coordinata speciale '111.1 0 1'.         
!*******************************************************************************
      LOGICAL IN                                                        
      IF (NEWRAY) IN=.FALSE.                                            
!*******************************************************************************
      CALL HAMLTN                                                       REAC 17
      H=R(1)-EARTHR                                                     REAC 18
      IF (.NOT.NEWRAY.AND..NOT.RSPACE)  WRITE(6,*)'(8HEXIT ION,0.)'     REAC 19
      NEWRAY=.FALSE.                                                    REAC 20
      V=SQRT(R(4)**2+R(5)**2+R(6)**2)                                   REAC 21
!********* NORMALIZE THE WAVE NORMAL DIRECTION TO ONE                   REAC 22
      R(4)=R(4)/V                                                       REAC 23
      R(5)=R(5)/V                                                       REAC 24
      R(6)=R(6)/V                                                       REAC 25
!********* NEGATIVE OF DISTANCE ALONG RAY TO CLOSEST APPROACH TO CENTER REAC 26
!********* OF EARTH                                                     REAC 27
      UP=R(1)*R(4)                                                      REAC 28
      RADG=EARTHR**2-R(1)**2*(R(5)**2+R(6)**2)                          REAC 29
      DISTG=SQRT (AMAX1(0.,RADG))                                       REAC 30
!********* DISTANCE ALONG RAY TO FIRST INTERSECTION WITH OR CLOSEST     REAC 31
!********* APPROACH TO THE EARTH                                        REAC 32
      SG=-UP-DISTG                                                      REAC 33
!********* CROSSG IS TRUE IF THE RAY WILL INTERSECT OR TOUCH THE EARTH  REAC 34
      CROSSG=UP.LT.0..AND.RADG.GE.0.                                    REAC 35
      RADR=(EARTHR+RCVRH)**2-R(1)**2*(R(5)**2+R(6)**2)                  REAC 36
      DISTR=SQRT (AMAX1(0.,RADR))                                       REAC 37
!********* DISTANCE ALONG RAY TO THE FIRST INTERSECTION WITH OR CLOSEST REAC 38
!********* APPROACH TO THE RECEIVER HEIGHT                              REAC 39
      SR=DISTR-UP                                                       REAC 40
      IF (UP.LT.0..AND.DISTR.LT.-UP.AND.R(1).NE.EARTHR+RCVRH) SR=-DISTR REAC 41
     1 -UP                                                              REAC 42
!********* CROSSR IS TRUE IF THE RAY WILL INTERSECT WITH OR MAKE A      REAC 43
!********* CLOSEST APPROACH TO THE RECEIVER HEIGHT                      REAC 44
      CROSSR=R(4).LT.0..OR.R(1).LT.(EARTHR+RCVRH)                       REAC 45
      CROSS=CROSSG.OR.CROSSR                                            REAC 46
!********* MAXIMUM DISTANCE IN WHICH TO LOOK FOR THE IONOSPHERE         REAC 47
      S1=AMIN1(SR,SG)                                                   REAC 48
      IF(.NOT.CROSSG) S1=SR                                             REAC 49
      IF (UP.GE.0.) GO TO 15                                            REAC 50
      CROSS=.TRUE.                                                      REAC 51
!********* IF RAY IS GOING DOWN, S1 IS AT MOST THE DISTANCE TO A PERIGEEREAC 52
      S1=AMIN1(S1,-UP)                                                  REAC 53
!********* CONVERT THE POSITION AND DIRECTION OF THE RAY TO CARTESIAN   REAC 54
!********* COORDINATES                                                  REAC 55
   15 CALL POLCAR                                                       REAC 56
!      SSTEP=100.                                                        REAC 57
!*******************************************************************************
!     ALEX: Originariamente, SSTEP=100.0 .                              
!           In realtà, applicando la trigonometria,                     
!           si può dimostrare, in prima approssimazione,                
!           che l'elemento di ascissa curvilinea è ...                  
!*******************************************************************************
      SSTEP=STEP1/COS(TH)                                               GPROF000
!*******************************************************************************
!     FORMULA ESATTA PER L'ELEMENTO DI ASCISSA CURVILINEA IN COORDINATE POLARI: 
!*******************************************************************************
!      SSTEP=STEP1*SQRT(1+(R(1)*(DTHDT/DRDT(1)))**2+                             GPROF000
!     1(R(1)*SIN(TH)*(DPHDT/DRDT(1)))**2)                                        GPROF000
!*******************************************************************************
      S=SSTEP                                                           REAC 58
      DO 20 I=1,NSTEP                                                   REAC 59
      IF ((S-SSTEP).GT.S1.AND.CROSS) GO TO 25                           REAC 60
!********* CONVERT POSITION AND DIRECTION TO SPHERICAL POLAR COORDINATESREAC 61
!********* AT A DISTANCE S ALONG THE RAY                                REAC 62
      CALL CARPOL                                                       REAC 63
      CALL ELECTX                                                       REAC 64
!********* FREE SPACE                                                   REAC 65
      IF (X.EQ.0) GO TO 20                                              REAC 66
      CALL RINDEX                                                       REAC 67
!********* NORMALIZE THE WAVE NORMAL DIRECTION TO ONE                   REAC 22
      R(4)=R(4)/V                                                       REAC 22a
      R(5)=R(5)/V                                                       REAC 22b
      R(6)=R(6)/V                                                       REAC 22c
!********* EFFECTIVELY FREE SPACE                                       REAC 68
      IF (SPACE) GO TO 20                                               REAC 69
      IF (SSTEP.LT.0.5E-4) GO TO 25                                     REAC 70
!********* RAY IN THE IONOSPHERE.  STEP BACK OUT                        REAC 71
      S=S-SSTEP                                                         REAC 72
!********* DECREASE STEP SIZE                                           REAC 73
      SSTEP=SSTEP/10.                                                   REAC 74
   20 S=S+SSTEP                                                         REAC 75
!*******************************************************************************
!      PRINT *,'222.2 0 3'                                                       AZZ
!*******************************************************************************
      WRITE(6,2000) NSTEP                                               REAC 76
! 2000 FORMAT (9H EXCEEDED,I5,26H STEPS IN SUBROUTINE REACH)             REAC 77
 2000 FORMAT ('EXCEEDED',I5,'STEPS IN SUBROUTINE REACH')
!*******************************************************************************
      CALL ZERO                                                                 AZZ
!*******************************************************************************
      STOP                                                              REAC 78
   25 IF(CROSS) S=AMIN1(S,S1)                                           REAC 79
!********* CONVERT POSITION AND DIRECTION TO SPHERICAL POLAR COORDINATESREAC 80
!********* AT A DISTANCE S ALONG THE RAY                                REAC 81
      CALL CARPOL                                                       REAC 82
!********* AVOID THE RAY BEING SLIGHTLY UNDERGROUND                     REAC 83
      R(1)=AMAX1(R(1),EARTHR)                                           REAC 84
!********* ONE STEP INTEGRATION                                         REAC 85
      IF (N.LT.7) GO TO 31                                              REAC 86
      DO 30 NN=7,N                                                      REAC 87
   30 R(NN)=R(NN)+S*DRDT(NN)                                            REAC 88
   31 T=T+S                                                             REAC 89
      CALL RINDEX                                                       REAC 90
!********* AT A PERIGEE                                                 REAC 91
      PERIGE=S.EQ.(-UP)                                                 REAC 92
!********* CORRECT MINOR ERRORS                                         REAC 93
      IF (PERIGE) R(4)=0.                                               REAC 94
!********* KEEP CONSISTENCY AFTER CORRECTING MINOR ERRORS               REAC 95
      DRDT(1)=R(4)                                                      REAC 96
!********* ON THE GROUND                                                REAC 97
      GROUND=S.EQ.SG.AND.CROSSG                                         REAC 98
!********* AT THE RECEIVER HEIGHT                                       REAC 99
      THERE=S.EQ.SR.AND.CROSSR.AND..NOT.PERIGE                          REAC100
!********* AT A CLOSEST APPROACH TO THE RECEIVER HEIGHT                 REAC101
      MINDIS=PERIGE.AND.S.EQ.SR.AND.CROSSR                              REAC102
      RSPACE=SPACE                                                      REAC103
      V=SQRT(N2/(R(4)**2+R(5)**2+R(6)**2))                              REAC104
!********* RENORMALIZE THE WAVE NORMAL DIRECTION TO = SQRT(REAL(N**2))  REAC105
      R(4)=R(4)*V                                                       REAC106
      R(5)=R(5)*V                                                       REAC107
      R(6)=R(6)*V                                                       REAC108
      RSTART=1.                                                         REAC109
!*******************************************************************************
      WRITE(6,*) 'BEFORE: IN=', IN                                              AZZ
      IF ((.NOT.IN).AND.(.NOT.SPACE).AND.(DRDT(1).GT.0.)) THEN          REAC110
      IN=.TRUE.                                                                 AZZ
!      PRINT *,'111.1 0 1'                                                       AZZ
      WRITE(6,*) '+++ RAY IN THE IONOSPHERE +++'                                AZZ
      END IF                                                                    AZZ
      WRITE(6,*) 'AFTER: IN=', IN                                               AZZ
!*******************************************************************************
      RETURN                                                            REAC111
         END                                                            REAC112-
         
!*******************************************************************************

