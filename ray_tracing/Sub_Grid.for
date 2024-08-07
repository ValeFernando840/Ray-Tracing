!     
! File:   Sub_Grid.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:41
!

      SUBROUTINE GRIDPROFILES                                           GPROF000
! ******************************************************************************
      COMMON /ALEX1/ NLAT,NLON,LAT(10),LON(25)                          GPROF000
      COMMON /ALEX2/ NOC,HPC(300),FNC(300,10,25)                        GPROF000
      SAVE /ALEX1/,/ALEX2/                                              GPROF000
      CHARACTER LINE1*18,LINE2*43,LINE3*44,LINEa*24,LINEb*16            GPROF000
! ******************************************************************************
      LATINF=31.0                                                       GPROF000
      LATSUP=49.0                                                       GPROF000
      LATSTEP=2.0                                                       GPROF000
      NLAT=1+(LATSUP-LATINF)/LATSTEP                                    GPROF000
      LONINF=-9.0                                                       GPROF000
      LONSUP=39.0                                                       GPROF000
      LONSTEP=2.0                                                       GPROF000
      NLON=1+(LONSUP-LONINF)/LONSTEP                                    GPROF000
      HINF=1.0                                                          GPROF000
      HSUP=300.0                                                        GPROF000
      HSTEP=1.0                                                         GPROF000
      NOC=1+(HSUP-HINF)/HSTEP                                           GPROF000
      OPEN(9,FILE='GRIDPROFILES.txt',STATUS='unknown')                  GPROF000
      OPEN(10,FILE='GRIDPROFILES_TEST.txt',STATUS='unknown')            GPROF000
      READ(9,1) LINE1                                                   GPROF000
!      PRINT 1,LINE1                                                     GPROF000
      WRITE(10,1) LINE1                                                 GPROF000
    1 FORMAT(A18)                                                       GPROF000
      READ(9,2) LINE2                                                   GPROF000
!      PRINT 2,LINE2                                                     GPROF000
      WRITE(10,2) LINE2                                                 GPROF000
    2 FORMAT(A43)                                                       GPROF000
      READ(9,3) LINE3                                                   GPROF000
!      PRINT 3,LINE3                                                     GPROF000
      WRITE(10,3) LINE3                                                 GPROF000
    3 FORMAT(A44)                                                       GPROF000
    
      DO 10 I=1,NLON                                                    GPROF000
      LON(I)=LONINF+LONSTEP*(I-1)                                       GPROF000
      DO 9 J=1,NLAT                                                     GPROF000
      LAT(J)=LATINF+LATSTEP*(J-1)                                       GPROF000
      READ(9,4) LINEa                                                   GPROF000
!      !PRINT 4,LINEa                                                     GPROF000
      WRITE(10,4) LINEa                                                 GPROF000
    4 FORMAT(A24)                                                       GPROF000
      READ(9,5) LINEb                                                   GPROF000
!      PRINT 5,LINEb                                                     GPROF000
      WRITE(10,5) LINEb                                                 GPROF000
    5 FORMAT(A16)                                                       GPROF000
      
      DO 8 K=1,NOC                                                      GPROF000
!      HPC(K)=HINF+HSTEP*(K-1)                                          GPROF000
      READ(9,*,END=6) HPC(K),FNC(K,J,I)                                 GPROF000
!    6 PRINT 7, HPC(K),FNC(K,J,I)                                        GPROF000
    6 WRITE(10,7) HPC(K),FNC(K,J,I)                                     GPROF000
    7 FORMAT(F5.1,3X,F5.2)                                              GPROF000
    8 CONTINUE                                                          GPROF000
    9 CONTINUE                                                          GPROF000
   10 CONTINUE                                                          GPROF000
      CLOSE(9)                                                          GPROF000
      CLOSE(10)                                                         GPROF000
      RETURN                                                            GPROF000
      END                                                               -
!*******************************************************************************
