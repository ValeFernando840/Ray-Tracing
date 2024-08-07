!     
! File:   Sub_Latlon.for
! Author: Zenon
! Created on 5 de octubre de 2016, 9:53
!*******************************************************************************
      SUBROUTINE LATLON                                                 LATLON01
!*******************************************************************************  
      COMMON /ZZZZ/ ZZLAT,ZZLON,JLAT,JLON                               LATLON02
      COMMON /ALEX1/ NLAT,NLON,LAT(10),LON(25)                          GPROF000
!*******************************************************************************
!**** Busqueda de la ubicacion del radar Tx (lat,long)
!*****dentro de la matriz de grilla de (h Km,f MHz)
!*****Devuelve los indices (i,j) de la ubicacion del Tx en la grilla
!*****Busqueda Binaria
      JL=0                                                              LATLON03
      JU=NLAT+1                                                         GPROF000
   10 IF(JU-JL.GT.1)THEN                                                LATLON04
      JM=(JU+JL)/2                                                      LATLON05
      IF(LAT(NLAT).GT.LAT(1).EQV.(ZZLAT.GT.LAT(JM)))THEN                GPROF000
         JL=JM                                                          LATLON06
      ELSE                                                              LATLON07
         JU=JM                                                          LATLON08
      ENDIF                                                             LATLON09
      GO TO 10                                                          LATLON10
      ENDIF                                                             LATLON11
      JLAT=JL                                                           LATLON12
      
      JLO=0                                                             LATLON13
      JUO=NLON+1                                                        GPROF000
   11 IF(JUO-JLO.GT.1)THEN                                              LATLON14
      JMO=(JUO+JLO)/2                                                   LATLON15
      IF(LON(NLON).GT.LON(1).EQV.(ZZLON.GT.LON(JMO)))THEN               GPROF000
        JLO=JMO                                                         LATLON16
      ELSE                                                              LATLON17
         JUO=JMO                                                        LATLON18
      ENDIF                                                             LATLON19
      GO TO 11                                                          LATLON20
      ENDIF                                                             LATLON21
      JLON=JLO                                                          LATLON22
      WRITE(6,998)JLAT,JLON                                             LATLON23
  998 FORMAT (2(1X,I4))                                                 LATLON24
      RETURN                                                            LATLON25
      END                                                               -
!*******************************************************************************
