!     
! File:   Sub_Polcoe.for
! Author: Zenon
! Created on 5 de octubre de 2016, 9:54
!*******************************************************************************
      SUBROUTINE POLCOE(X,Y,N,COF)                                      POLCOE01
      ! Calcula los coeficientes alpha, beta y gamma necesarios para 
      ! determinar el coefciciente de reflexion n
      ! n^2=1-X^2 con X=alpha+beta*h+gamma*h^2
          
      PARAMETER(NMAX=15)                                                POLCOE02
      DIMENSION X(4),Y(4),COF(4),S(NMAX)                                POLCOE03
      DO 11 I=1,N                                                       POLCOE04
      S(I)=0                                                            POLCOE05
      COF(I)=0                                                          POLCOE06
   11 CONTINUE                                                          POLCOE07
      S(N)= -X(1)                                                       POLCOE08
      DO 13 I=2,N                                                       POLCOE09
      DO 12 J=N+1-I,N-1                                                 POLCOE10
      S(J)=S(J)-X(I)*S(J+1)                                             POLCOE11
   12 CONTINUE                                                          POLCOE12
      S(N)=S(N)-X(I)                                                    POLCOE13
   13 CONTINUE                                                          POLCOE14
      DO 16 J=1,N                                                       POLCOE15
      PHI=N                                                             POLCOE16
      DO 14 K=N-1,1,-1                                                  POLCOE17
      PHI=K*S(K+1)+X(J)*PHI                                             POLCOE18
   14 CONTINUE                                                          POLCOE19
      FF=Y(J)/PHI                                                       POLCOE20
      B=1.                                                              POLCOE21
      DO 15 K=N,1,-1                                                    POLCOE22
      COF(K)=COF(K)+B*FF                                                POLCOE23
      B=S(K)+X(J)*B                                                     POLCOE24
   15 CONTINUE                                                          POLCOE25
   16 CONTINUE                                                          POLCOE26
      RETURN                                                            POLCOE27
      END                                                               -
!******************************************************************************
