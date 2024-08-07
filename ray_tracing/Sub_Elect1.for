!     
! File:   Sub_Elect1.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 9:54
!
!*****************************************************************************
      SUBROUTINE ELECT1                                                 ELEC001
!          USE WHEN AN ELECTRON DENSITY PERTURBATION IS NOT WANTED      ELEC002
      COMMON /XX/ MODX(2),X(6)                                          ELEC003
      COMMON /WW/ ID,W0,W(400)                                          ELEC004
      EQUIVALENCE (PERT,W(150))                                         ELEC005
      MODX(2)=4HNONE                                                    ELEC006
      PERT=0.                                                           ELEC007
      RETURN                                                            ELEC008
      END                                                               ELEC009-
!*******************************************************************************

