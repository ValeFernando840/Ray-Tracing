!     
! File:   Sub_Porcar.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:49
!

!******************************************************************************
      SUBROUTINE POLCAR                                                 POLC001
!                                                                      POLC002
      COMMON /COORD/ S,X0(6),GG(6),R0(4),VERT                           POLC003
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                   POLC004
      COMMON R(20),T,STP,DRDT(20),N2                                    POLC005
!          CONVERTS SPHERICAL COORDINATES TO CARTESIAN                  POLC006
      IF (R(5).EQ.0..AND.R(6).EQ.0.) GO TO 1                            POLC007
      VERT=0.                                                           POLC008
      SINA=SIN(R(2))                                                    POLC009
      COSA=SIN(PID2-R(2))                                               POLC010
      SINP=SIN(R(3))                                                    POLC011
      COSP=SIN(PID2-R(3))                                               POLC012
      X0(1)=R(1)*SINA*COSP                                              POLC013
      X0(2)=R(1)*SINA*SINP                                              POLC014
      X0(3)=R(1)*COSA                                                   POLC015
      GG(4)=R(4)*SINA*COSP+R(5)*COSA*COSP-R(6)*SINP                     POLC016
      GG(5)=R(4)*SINA*SINP+R(5)*COSA*SINP+R(6)*COSP                     POLC017
      GG(6)=R(4)*COSA-R(5)*SINA                                         POLC018
      RETURN                                                            POLC019
!          VERTICAL INCIDENCE                                           POLC020
    1 VERT=1.                                                           POLC021
      R0(1)=R(1)                                                        POLC022
      R0(2)=R(2)                                                        POLC023
      R0(3)=R(3)                                                        POLC024
      R0(4)=SIGN (1.,R(4))                                              POLC025
      RETURN                                                            POLC026
         END                                                            POLC026-
!******************************************************************************         
