!     
! File:   Sub_Frec_plasma.for
! Author: Zenon
!
! Created on 5 de octubre de 2016, 10:30
!

      SUBROUTINE frec_plasma!(ALT,FRECN,ZZLAT,ZZLON)   
      !REAL, INTENT(OUT)::FRECN(600)                                                                                                                        
      !REAL, INTENT(IN):: ZZLAT,ZZLON     
      !INTEGER, INTENT(OUT)::ALT(600)
      
      
      INTEGER           piktab,E!,ALT(600)
      DIMENSION         outf(20,1000),oar(100,1000),jfi(6)
      LOGICAL		    jf(50),rzino,igino
      
      !INTEGER           E!,ALT(600)
      !DIMENSION         jfi(6)
      !LOGICAL		    rzino,igino
      
      
      CHARACTER*2       timev(2)
      CHARACTER*3       uni(86)
      CHARACTER*4       IMZ(8),MAP,xtex,coorv(2)
      CHARACTER*5       ITEXT(8)
      CHARACTER*6       pna(86)
      real jne,R1(20),T1,STP1,DRDT1(20),N21
      DATA  IMZ  /' km ','GEOD','GEOD','yyyy',' mm ',' dd ','YEAR',
     &      'L.T.'/, ITEXT/'  H  ',' LATI',
     &      ' LONG',' YEAR','MONTH',' DAY ','DAYOF',' HOUR'/

      data pna/'NmF2','hmF2','NmF1','hmF1','NmE','hmE','NmD','hmD',
     &  'h05','B0','NVmin','hVtop','Tpeak','hTpek','T300','T400','T600',
     &  'T1400','T3000','T120','Ti450','hTeTi','sza','sundec','dip',
     &  'diplat','modip','Lati','Srise','Sset','season','Longi',
     &  'Rz12','cov','B1','M3000','TEC','TECtop','IG12','F1prb','F107d',
     &  'C1','daynr','vdrft','foF2r','F10781','foEr','sprd_F','MLAT', 
     &  'MLON','Ap_t','Ap_d','invdip','MLTinv','CGMlat','CGMlon',
     &  'CGMmlt','CGM_AB','CGMm0','CGMm1','CGMm2','CGMm3','CGMm4',
     &  'CGMm5','CGMm6','CGMm7','CGMm8','CGMm9','CGMm10','CGMm11',
     &  'CGMm12','CGMm13','CGMm14','CGMm15','CGMm16','CGMm17','CGMm18',
     &  'CGMm19','CGMm20','CGMm21','CGMm22','CGMm23','kp_t','dec','L',
     &  'DIMO'/
      data uni/'m-3','km','m-3','km','m-3','km','m-3','km','km','km',
     &   'm-3','km','K','km',7*'K','km',6*'deg',2*'h',' ','deg',4*' ',
     &   'm-2','%',5*' ','m/s',4*' ',2*'deg',2*' ','deg','h',2*'deg',
     &   'h',25*'deg',' ','deg',' ','Gau'/,
     &   timev/'LT','UT'/,coorv/'geog','geom'/

      data jfi/8,9,13,14,15,16/
      COMMON/const2/icalls,nmono,iyearo,idaynro,rzino,igino,ut0
      COMMON /ZENON/ NOC,ALT(300),FRECN(300)   
      COMMON /ZENON1/ ZZLAT,ZZLON,ZZALT     
      !SAVE /ZENON/
      COMMON /CONST/ PI,PIT2,PID2,DEGS,RAD,K,C,LOGTEN                !   ELECTX05
      COMMON /XX/ MODX(2),X,PXPR,PXPTH,PXPPH,PXPT,HMAX               !   ELECTX06
      COMMON R(20),T,STP,DRDT(20),N2                                 !   ELECTX07
      COMMON /WW/ ID,W0,W(400)                                       !   ELECTX08
      !SAVE /XX/,/WW/,/CONST/,/ZENON/,/ZENON1/,/const2/
      !COMMON /IRII/ jm,iy,imd,iut,hour,hx,htec_max,ivar,vbeg,vend,vstp,piktab
      !COMMON logical /IRI2/ jf(50)
      !COMMON DIMENSION /IRI3/ outf(20,1000),oar(100,1000)
      do i=1,20 
         R1(i)=R(i)
         DRDT1(i)=DRDT(i)
      enddo

      
      T1=T
      STP1=STP
      N21=N2
      
      icalls=0
      nmono=-1
      iyearo=-1
      idaynro=-1
      rzino=.true.
      igino=.true.
      ut0=-1

      call read_ig_rz
      call readapf107
        
      nummax=1000
        
      do 6249 i=1,100
6249    oar(i,1)=-1.0


!*******************************************************************
! Ingreso de parametros por medio de un .txt

      do i=1,50 
         jf(i)=.true.
      enddo

      !if(FRECN(10).EQ.0.) then               
      open(56,FILE='CONFI_IRI.txt',STATUS='unknown')    
      jm=0
                      
        READ(56,*) iy,imd,iut,hour
        READ(56,*) hx
        READ(56,*) piktab
        READ(56,*) htec_max
        READ(56,*) ivar
        READ(56,*) vbeg,vend,vstp 
        READ(56,*) jchoice   
      
        
        
      DO 8 E=1,50                                                     
      READ(56,*) jf(E)     
8     continue 
   
         
! option to enter measured values for NmF2,hmF2, NmF1, hmF1, NmE,hmE 
         
      numstp=int((vend-vbeg)/vstp)+1  
        
! option to enter F107D and/or PF107 
      if(.not.jf(25)) then
                    !print *,'User input for F107D:'
           read(56,*) f107d
                   !print *, f107d
           do i=1,100
                oar(41,i)=f107d
           enddo
      endif

      if(.not.jf(32)) then
                        !print *,'User input for PF107:'
           read(56,*) pf107d
                        !print*,pf107d
           do i=1,100
                oar(46,i)=pf107d
           enddo
      endif

      
! option to enter Rz12 and/or IG12
      if(.not.jf(17)) then
                        !print *,'User input for Rz12'
          read(56,*) oar(33,1)
                        !print *,oar(33,1)
          do i=2,100
                oar(33,i)=oar(33,1)
          enddo
      endif

      if(.not.jf(27)) then
                        !print *,'User input for IG12'
           read(56,*) oar(39,1)
                        !print *, oar(39,1)
           do i=2,100
               oar(39,i)=oar(39,1)
           enddo
      endif
      
      close(56)
      !endif 
      !REWIND(56)
! End of user input        
!*******************************************************************

      num1=(vend-vbeg)/vstp+1
      numstp=iabs(num1)
      if(numstp.GT.nummax) numstp=nummax
 
      hxx=hx
      jmag=jm
      mmdd=imd     
 !********************************************************
 ! Calling IRI subroutine with the new latitud and longitud
 ! Esta funcion devuelve el perfil de densidad electronico para
 ! las coordenadas (ZZLAT,ZZLON) y ademas su corresponente Altitud.       
      phour=hour
      
      
      xlat=ZZLAT
      xlon=ZZLON
        call iri_web(jmag,jf,xlat,xlon,iy,mmdd,iut,hour,
     &          hxx,htec_max,ivar,vbeg,vend,vstp,outf,oar)

     
     
! preparation of results page
!********************************************************
  
! table head .......................................................
!
      agnr=7          !output unit number
      xtex=imz(ivar)
             
      IF(PIKTAB.EQ.0) THEN
          if(jf(22)) then
 !      		WRITE(7,8193) ITEXT(IVAR),xtex
          else
 !       		WRITE(7,9193) ITEXT(IVAR),xtex        	
          endif
      ENDIF

		
      xcor=vbeg
      do 1234 li=1,numstp
                         
!************************************************************
! output: standard Si se Elije PIKTAP=0
!
            if(ivar.eq.1) then
                    oar(1,li)=oar(1,1)
                    oar(37,li)=oar(37,1)
                    oar(38,li)=oar(38,1)
                    endif
            jne=int(outf(1,li)/1.e6+.5)
            xner=outf(1,li)/oar(1,li)
            jtn=int(outf(2,li)+.5)
            jti=int(outf(3,li)+.5)
            jte=int(outf(4,li)+.5)
            scid=1.0E-8
            if(jf(22)) scid=10.
            jio=INT(OUTF(5,li)*scid+.5)
            jih=INT(OUTF(6,li)*scid+.5)
            jihe=INT(OUTF(7,li)*scid+.5)
            jio2=INT(OUTF(8,li)*scid+.5)
            jino=INT(OUTF(9,li)*scid+.5)
            jicl=INT(OUTF(10,li)*scid+.5)
            jin=INT(OUTF(11,li)*scid+.5)
            if(outf(1,li).lt.0) jne=-1
            if(outf(1,li).lt.0) xner=-1.
            if(outf(2,li).lt.0) jtn=-1
            if(outf(3,li).lt.0) jti=-1
            if(outf(4,li).lt.0) jte=-1
            if(outf(5,li).lt.0) jio=-1
            if(outf(6,li).lt.0) jih=-1
            if(outf(7,li).lt.0) jihe=-1
            if(outf(8,li).lt.0) jio2=-1
            if(outf(9,li).lt.0) jino=-1
            if(outf(10,li).lt.0) jicl=-1
            if(outf(11,li).lt.0) jin=-1
            tec=oar(37,li)
            if(tec.gt.0.0) then
                tec=tec/1.e16
                itopp=int(oar(38,li)+.5)
            else
                tec=-1.0
                itopp=-1
            endif
            ALT(li)=XCOR
            
            ! Conversion del perfil de densidad electronica para las coordenadas
            ! (ZZLAT,ZZLON)a Frecuencia critica del Plasma.
            ! ne ---> Fne
            FRECN(li)=(9*sqrt(abs(jne)*1e6))/1e6

1234    xcor=xcor+vstp
        
        do i=1,20 
           R(i)=R1(i)
           DRDT(i)=DRDT1(i)
        enddo
      
        T=T1
        STP=STP1
        N2=N21


        return
        end                                                             