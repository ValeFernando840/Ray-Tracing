!     
! File:   Sub_Carpol.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:50
!

!******************************************************************************         
!                                                                       POLC027
!          STEPS THE RAY A DISTANCE S, AND THEN                         POLC028
!          CONVERTS CARTESIAN COORDINATES TO SPHERICAL COORDINATES      POLC029
!****************************************************************************
      SUBROUTINE CARPOL                                                 POLC030
      COMMON /COORD/ S,X0(6),GG(6),R0(4),VERT                           POLC003bis
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                   POLC004bis
      COMMON R(20),T,STP,DRDT(20),N2                                    POLC005bis
      IF (VERT.NE.0.) GO TO 2                                           POLC031
      GG(1)=X0(1)+S*GG(4)                                               POLC032
      GG(2)=X0(2)+S*GG(5)                                               POLC033
      GG(3)=X0(3)+S*GG(6)                                               POLC034
      TEMP=SQRT(GG(1)**2+GG(2)**2)                                      POLC035
      R(1)=SQRT(GG(1)**2+GG(2)**2+GG(3)**2)                             POLC036
      R(2)=ATAN2(TEMP,GG(3))                                            POLC037
      R(3)=ATAN2(GG(2),GG(1))                                           POLC038
      R(4)=(GG(1)*GG(4)+GG(2)*GG(5)+GG(3)*GG(6))/R(1)                   POLC039
      R(5)=(GG(3)*(GG(1)*GG(4)+GG(2)*GG(5))-(GG(1)**2+GG(2)**2)*GG(6))/ POLC040
     1(R(1)*TEMP)                                                       POLC041
      R(6)=(GG(1)*GG(5)-GG(2)*GG(4))/TEMP                               POLC042
      RETURN                                                            POLC043
!          VERTICAL INCIDENCE                                           POLC044
    2 R(1)=R0(1)+R0(4)*S                                                POLC045
      R(2)=R0(2)                                                        POLC046
      R(3)=R0(3)                                                        POLC047
      R(4)=R0(4)                                                        POLC048
      R(5)=0.                                                           POLC049
      R(6)=0.                                                           POLC050
      RETURN                                                            POLC051
         END                                                            POLC 52-
!******************************************************************************
