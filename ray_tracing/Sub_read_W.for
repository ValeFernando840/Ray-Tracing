!     
! File:   Sub_read_W.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:39
!
!******************************************************************************      
!     SE LEE EL ARCHIVO DE ENTRADA CON L OS PARAMETROS BASICOS DEL RADIO LINK 
!******************************************************************************      
      SUBROUTINE READW                                                  READ001
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                   READ002
      COMMON /WW/ ID,W0,W(400)                                          READ003
      EQUIVALENCE (EARTHR,W(2))                                         READ004
      OPEN(5,FILE='DATA_IN.txt',STATUS='unknown')                       READ005
      DO NW=1,400                                                       READ006
      READ (5,*,END=10001) W(NW)                                        READ007
10001 IF (NW.EQ.400.AND.NW.GT.400) GO TO 10                             READ008
      ENDDO                                                             READ009
   10 RETURN                                                            READ010
      CLOSE(5)
         END                                                            READ011-