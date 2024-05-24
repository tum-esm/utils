! PROFFAST 2 - Retrieval code for the COllaborative Carbon COlumn Network (COCCON)
! Copyright (C)   2022   Frank Hase, Karlsruhe Institut of Technology (KIT)
!
! This program is free software: you can redistribute it and/or modify
! it under the terms of the GNU General Public License version 3 as published by
! the Free Software Foundation.
!
! This program is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
! GNU General Public License for more details.
!
! You should have received a copy of the GNU General Public License
! along with this program.  If not, see <https://www.gnu.org/licenses/>.

!====================================================================
!
! This program is for the preprocessing of COCCON measurements.
! It performs quality checks, DC-correction, FFT and phase correction,
! and a resampling of the spectrum to a minimally sampled grid.
!
! This code has been created by Frank Hase (frank.hase@kit.edu) and
! Darko Dubravica (darko.dubravica@kit.edu), both affiliated with KIT
! in the framework of ESA's COCCON-PROCEEDS project.
!
!====================================================================

program opus_file_validator

use glob_prepro6

implicit none

logical :: dateidadec,reftrmdec
integer :: imeas
character(len=300) :: inputdatei

character(len=lengthcharmeas),dimension(:),allocatable :: measfile
integer(8),dimension(:),allocatable :: errflag,errflag_CO 
integer,dimension(:),allocatable :: nptrfirstdir,nofblock,nifg &
  ,icbfwd,icbbwd,icbfwd2,icbbwd2
integer,dimension(:,:),allocatable :: blocktype,blocklength,blockptr

real(8),dimension(:),allocatable :: JDdate
real,dimension(:),allocatable :: UTh,durationsec,astrelev,azimuth

character(len=6),dimension(:),allocatable :: YYMMDDlocal,HHMMSSlocal,YYMMDDUT

real,dimension(:,:),allocatable :: reftrmT
real,dimension(:),allocatable :: refspec,refspec2,refphas,reftrm,sinc
real,dimension(:),allocatable :: cbfwd,cbbwd,cbfwd2,cbbwd2
real,dimension(:),allocatable :: obslatdeg,obslondeg,obsaltkm

logical :: file_is_intact

!====================================================================
!  read command argument
!  read input file
!====================================================================
call get_command_argument(1,inputdatei)
print *,'Reading input file...'
call read_input(trim(inputdatei))
print *,'Done!'
print *,'Number of raw measurements to be processed:',nmeas

if (nmeas .gt. maxmeas) then
    print *,'nmeas maxmeas: ',nmeas,maxmeas
    call warnout ('Too many files for processing!')
end if

!====================================================================
!  set ifg, spectral points and OPDmax according to input choice of mpowFFT
!====================================================================
select case (mpowFFT)
    case (17)
        OPDmax = 1.8d0 ! equivalent to Bruker Res 0.5 cm-1
        ifgradius = 56873            
    case (19)
        OPDmax = 4.5d0
        ifgradius = 142182
    case (20)
        OPDmax = 16.2d0
        ifgradius = 511857
    case (181)
        mpowFFT = 18
        OPDmax = 2.5d0 ! equivalent to Bruker Res 0.36 cm-1
        ifgradius = 78990
    case (182)
        mpowFFT = 18
        OPDmax = 3.0d0 ! equivalent to Bruker Res 0.3 cm-1
        ifgradius = 94788
    case default
        call warnout("Invalid choice of mpowFFT (allowed: 17, 181/182, 19, 20)!")
end select
maxspcrs = ifgradius + 1
maxifg = 2**mpowFFT
maxspc = maxifg / 2 

!====================================================================
!  allocation of general arrays, init sinc, read reference spectrum (for nue cal check)
!====================================================================
allocate (errflag(nmeas),errflag_CO(nmeas))
allocate (measfile(nmeas),nptrfirstdir(nmeas),nofblock(nmeas),nifg(nmeas))
allocate (icbfwd(nmeas),icbbwd(nmeas),icbfwd2(nmeas),icbbwd2(nmeas))
allocate (cbfwd(nmeas),cbbwd(nmeas),cbfwd2(nmeas),cbbwd2(nmeas))
allocate (obslatdeg(maxmeas),obslondeg(maxmeas),obsaltkm(maxmeas))
allocate (blocktype(maxblock,nmeas),blocklength(maxblock,nmeas),blockptr(maxblock,nmeas))
allocate (YYMMDDlocal(nmeas),HHMMSSlocal(nmeas),YYMMDDUT(nmeas))
allocate (JDdate(nmeas),UTh(nmeas),durationsec(nmeas),astrelev(nmeas),azimuth(nmeas))
nsinc = nzf * nconv
allocate (sinc(-nsinc:nsinc))
allocate (refspec(maxspc),refspec2(maxspc),refphas(maxspc),reftrm(maxspc))

call prepare_sinc(sinc)

if (checkoutdec) then 
    call tofile_spec(trim(diagoutpath)//pathstr//'sinc.dat',2*nsinc+1,sinc(-nsinc:nsinc))
end if

call read_refspec('refspec.dat',maxspc,refspec)
call read_refspec('refspec2.dat',maxspc,refspec2)

inquire (file = 'refphase.inp',exist = dateidadec)
if (dateidadec) then
    print *,'Optional phase reference file detected...'
    call read_refspec('refphase.inp',maxspc,refphas)
else
    refphas = 0.0
end if

inquire (file = 'reftrm.inp',exist = dateidadec)
if (dateidadec) then
    print *,'Optional trm reference file detected...'
    allocate (reftrmT(maxT,maxspc))
    reftrmdec = .true.
    call read_reftrmT('reftrm.inp',maxT,maxspc,reftrmT)
else
    reftrmdec = .false.
end if

!====================================================================
!  read file names
!====================================================================
print *,'Reading file names'
call read_meas_files(trim(inputdatei),nmeas,measfile,obslatdeg,obslondeg,obsaltkm)
print *,'Done!'

!====================================================================
!  read all OPUS file headers, ephemerid calculation
!====================================================================
errflag(1:nmeas) = 0
errflag_CO(1:nmeas) = 0

print *
print '(A)', '--- Start verifying file integrities ---'
print *

do imeas = 1,nmeas
    file_is_intact = .true.
    print '(A)', 'Parsing file "' // trim(measfile(imeas)) // '"'

    ! read OPUS parms
    call read_opus_hdr( &
        measfile(imeas), &
        nptrfirstdir(imeas), &
        nofblock(imeas), &
        file_is_intact &
    )
    call read_opus_dir( &
        measfile(imeas), &
        nptrfirstdir(imeas), &
        nofblock(imeas), &
        blocktype(1:maxblock,imeas), &
        blocklength(1:maxblock,imeas), &
        blockptr(1:maxblock,imeas), &
        nifg(imeas), &
        file_is_intact &
    )
    call read_opus_parms( &
        imeas, &
        measfile(imeas), &
        nofblock(imeas), &
        blocktype(1:maxblock,imeas), &
        blocklength(1:maxblock,imeas), &
        blockptr(1:maxblock,imeas), &
        file_is_intact &
    )

    ! check formal consistency of file with COCCON / preprocessor demands
    call checkOPUSparms( &
        imeas, &
        file_is_intact &
    )

    if (file_is_intact) then
        print '(A)', 'File is intact'
    else
        print '(A)', 'File is corrupted'
    end if

    print *

end do

print '(A)', '--- Done verifying file integrities ---'

!====================================================================
!  Deallocation of general arrays
!====================================================================
if (reftrmdec) deallocate (reftrmT)
deallocate (refspec,refspec2,refphas,reftrm)
deallocate (sinc)

deallocate (JDdate,UTh,durationsec,astrelev,azimuth)
deallocate (YYMMDDlocal,HHMMSSlocal,YYMMDDUT)
deallocate (obslatdeg,obslondeg,obsaltkm)
deallocate (cbfwd,cbbwd,cbfwd2,cbbwd2)
deallocate (blocktype,blocklength,blockptr)
deallocate (measfile,nptrfirstdir,nofblock,nifg)
deallocate (icbfwd,icbbwd,icbfwd2,icbbwd2)
deallocate (errflag,errflag_CO)

end program opus_file_validator









!====================================================================
!  checkOPUSparms
!====================================================================
subroutine checkOPUSparms(imeas,file_is_intact)

use glob_prepro6, only : OPDmax
use glob_OPUSparms6

implicit none

integer,intent(in) :: imeas
logical,intent(inout) :: file_is_intact

if (OPUS_parms(imeas)%RES .gt. 0.90001d0 / OPDmax) then
    print *,'OPUS RES:',OPUS_parms(imeas)%RES
    print *,'Requested RES:',0.9d0 / OPDmax
    call warnout ('RES too small!')
    file_is_intact = .false.
end if

if (modulo(OPUS_parms(imeas)%NSS,2) .gt. 0) then
    call warnout ('Uneven number of scans!') 
    file_is_intact = .false.   
end if


end subroutine checkOPUSparms


!====================================================================
!  gonext: Einlesen bis zum naechsten $ Zeichen
!====================================================================
subroutine gonext(ifile,bindec)

implicit none

integer,intent(in) :: ifile
logical,intent(in) :: bindec

character(1) :: nextchar

nextchar='x'
do while (nextchar /= '$')
    if (bindec) then
        read(ifile) nextchar
    else
        read(ifile,'(A1)') nextchar
    end if
end do

end subroutine gonext


!====================================================================
!  next_free_unit
!====================================================================
integer function next_free_unit()

implicit none

integer :: iu_free, istatus
logical :: is_open

iu_free = 9
is_open = .true.

do while (is_open .and. iu_free < 100)
    iu_free = iu_free+1
    inquire (unit=iu_free, opened=is_open, iostat=istatus)
    if (istatus .ne. 0) call warnout ('Error in inquiry!')
enddo

if (iu_free >= 100) call warnout ('No free unit < 100 found!')

next_free_unit = iu_free

end function next_free_unit



!====================================================================
!  OPUS_eval_char
!====================================================================
subroutine OPUS_eval_char(blocklength,binchar,charfilter,charwert)

use glob_prepro6,only : maxOPUSchar

implicit none

integer,intent(in) :: blocklength
character(len=blocklength),intent(in) :: binchar
character(len=3),intent(in) :: charfilter
character(len=maxOPUSchar),intent(out) :: charwert

integer(2) :: ityp,ireserved
integer :: ipos

ipos = index(binchar,charfilter//achar(0))
if (ipos .eq. 0) then
    print '(A)', 'Charfilter "', charfilter, '" is missing'
end if

read(binchar(ipos+4:ipos+5),FMT='(A2)') ityp

read(binchar(ipos+6:ipos+7),FMT='(A2)') ireserved
    
if (ityp .ne. 2 .and. ityp .ne. 3) then
    call warnout('Inconsistent parameter kind in OPUS file!')
end if

charwert = '                                                  '
read(binchar(ipos+8:ipos+8+2*ireserved-1),FMT='(A)') charwert(1:2*ireserved)

end subroutine OPUS_eval_char



!====================================================================
!  OPUS_eval_int
!====================================================================
subroutine OPUS_eval_int(blocklength,binchar,charfilter,iwert)

implicit none

integer,intent(in) :: blocklength
character(len=blocklength),intent(in) :: binchar
character(len=3),intent(in) :: charfilter
integer,intent(out) :: iwert

integer(2) :: ityp,ireserved
integer :: ipos

ipos = index(binchar,charfilter//achar(0))
if (ipos .eq. 0) then
    print '(A)', 'Charfilter "', charfilter, '" is missing'
end if

read(binchar(ipos+4:ipos+5),FMT='(A2)') ityp

read(binchar(ipos+6:ipos+7),FMT='(A2)') ireserved
    
if (ityp .ne. 0 .or. ireserved .ne. 2) then
    call warnout('Inconsistent parameter kind in OPUS file!')
end if

read(binchar(ipos+8:ipos+8+2*ireserved-1),FMT='(A4)') iwert

end subroutine OPUS_eval_int


!====================================================================
!  OPUS_eval_dble
!====================================================================
subroutine OPUS_eval_dble(blocklength,binchar,charfilter,dblewert)

implicit none

integer,intent(in) :: blocklength
character(len=blocklength),intent(in) :: binchar
character(len=3),intent(in) :: charfilter
real(8),intent(out) :: dblewert

integer(2) :: ityp,ireserved
integer :: ipos

ipos = index(binchar,charfilter//achar(0))
if (ipos .eq. 0) then
    print '(A)', 'Charfilter "', charfilter, '" is missing'
end if

read(binchar(ipos+4:ipos+5),FMT='(A2)') ityp

read(binchar(ipos+6:ipos+7),FMT='(A2)') ireserved
    
if (ityp .ne. 1 .or. ireserved .ne. 4) then
    call warnout('Inconsistent parameter kind in OPUS file!')
end if

read(binchar(ipos+8:ipos+8+2*ireserved-1),FMT='(A8)') dblewert

end subroutine OPUS_eval_dble



!====================================================================
!  prepare_sinc
!====================================================================
subroutine prepare_sinc(sinc)

use glob_prepro6, only : nconv,nzf,nsinc,pi

implicit none

real,dimension(-nsinc:nsinc),intent(out) :: sinc

integer :: i
real(8) :: x,xapo,apowert

sinc(0) = 1.0
do i = 1,nsinc
    xapo = real(i,8) / real(nzf * (nconv - 2),8)
    if (xapo .gt. 1.0) then
        xapo = pi
    else
        xapo = pi * xapo
    end if
    apowert = 0.5d0 * (1.0d0 + cos(xapo))
    x = pi * real(i,8) / real(nzf,8)
    sinc(i) = apowert * sin(x) / x
    sinc(-i) = sinc(i)
end do

end subroutine prepare_sinc



!====================================================================
!  read_input
!====================================================================
subroutine read_input(inpdatei)

use glob_prepro6

implicit none

character(len=*),intent(in) :: inpdatei

character(len = lengthcharmeas) :: zeile,dateiname
logical :: marke,decfileda,decsize
integer :: iunit,iowert,imeas,next_free_unit,nfilebytes,iscan

iunit = next_free_unit()
open (iunit,file = trim(inpdatei),status = 'old',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(inpdatei)
    call warnout('Cannot open input file!')
end if

call gonext(iunit,.false.)
read(iunit,*) checkoutdec
read(iunit,*) mpowFFT
read(iunit,*) DCmin
read(iunit,*) DCvar

call gonext(iunit,.false.)
read(iunit,*) ILSapo,ILSphas
read(iunit,*) ILSapo2,ILSphas2
read(iunit,*) semiFOV

call gonext(iunit,.false.)
read(iunit,*) obsfixdec
read(iunit,*) obslocation
read(iunit,*) toffseth_UT
if (obsfixdec) then
    read(iunit,*) obsfixlatdeg,obsfixlondeg,obsfixaltkm
else
    continue
end if

call gonext(iunit,.false.)
read(iunit,'(L)') quietrundec
read(iunit,'(A)') diagoutpath
read(iunit,'(A)') binoutpath
read(iunit,'(L)') dualchandec
read(iunit,'(L)') chanswapdec
read(iunit,'(L)') anaphasdec
read(iunit,'(I2)') bandselect

if (diagoutpath .eq. 'standard') diagoutpath = 'diagnosis'
if (chanswapdec .and. .not. dualchandec) call warnout('chanswap requires dualchandec')
if (bandselect .eq. 1 .and. .not. dualchandec) call warnout('bandselect = 1 requires dualchandec')

call gonext(iunit,.false.)
read(iunit,'(A)') infotext

call gonext(iunit,.false.)
! determine number of raw measurements to treat
marke = .false.
imeas = 0
do while (.not. marke)
    zeile = ''
    read(iunit,'(A)') zeile
    if (zeile(1:3) .eq. '***') then
        marke = .true.
    else        
        ! test OPSUS file existence and size here
        if (obsfixdec) then
            dateiname = trim(zeile)
        else
            iscan = scan(zeile,',')
            dateiname = zeile(1:iscan - 1)
        end if
        inquire(file = trim(dateiname),exist = decfileda,size = nfilebytes)
        if (.not. decfileda) then
            print *,dateiname
            call warnout('spectrum file does not exist!')
        end if
        if (nfilebytes .lt. minfilesize) then
            decsize = .false.
        else
            decsize = .true.
        end if
        if (decsize) imeas = imeas + 1
    end if
end do

close (iunit)
nmeas = imeas

end subroutine read_input



!====================================================================
! read_meas_files
!====================================================================
subroutine read_meas_files(inpdatei,nmeas,measfile,obslatdeg,obslondeg,obsaltkm)

use glob_prepro6, only : obsfixdec,obsfixlatdeg,obsfixlondeg,obsfixaltkm,lengthcharmeas,minfilesize

implicit none

character(len=*),intent(in) :: inpdatei
integer,intent(in) :: nmeas
character(len=lengthcharmeas),dimension(nmeas),intent(out) :: measfile
real,dimension(nmeas),intent(out) :: obslatdeg,obslondeg,obsaltkm

logical :: marke,decfileda,decsize
character(len=lengthcharmeas) :: zeile,dateiname
integer :: i,imeas,iunit,iowert,next_free_unit,nfilebytes,iscan
real :: latdeg,londeg,altkm

iunit = next_free_unit()

open (iunit,file = trim(inpdatei),status = 'old',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(inpdatei)
    call warnout('Cannot open input file!')
end if

do i = 1,6
    call gonext(iunit,.false.)
end do

marke = .false.
imeas = 0
do while (.not. marke)
    zeile = ''
    read(iunit,'(A)') zeile
    if (zeile(1:3) .ne. '***') then
        if (obsfixdec) then
            dateiname = trim(zeile)
            latdeg = obsfixlatdeg
            londeg = obsfixlondeg
            altkm = obsfixaltkm
        else
            iscan = scan(zeile,',')
            dateiname = zeile(1:iscan - 1)
            read(zeile(iscan+1:len(trim(zeile))),*) latdeg,londeg,altkm
        end if
    end if
    if (zeile(1:3) .eq. '***') then
        marke = .true.
    else        
        ! test file size here
        inquire(file = trim(dateiname),exist = decfileda,size = nfilebytes)
        if (.not. decfileda) then
            print *,dateiname
            call warnout('spectrum file does not exist!')
        end if
        if (nfilebytes .lt. minfilesize) then
            decsize = .false.
        else
            decsize = .true.
        end if
        if (decsize) then
            imeas = imeas + 1
            obslatdeg(imeas) = latdeg
            obslondeg(imeas) = londeg
            obsaltkm(imeas) = altkm
            measfile(imeas) = trim(dateiname)
            print *,trim(measfile(imeas))
        end if
    end if
end do

close (iunit)

end subroutine read_meas_files



!====================================================================
!  read_opus_dir
!====================================================================
subroutine read_opus_dir(measfile,nptrfirstdir,nofblock,blocktype &
  ,blocklength,blockptr,nifg,file_is_intact)

use glob_prepro6,only : maxblock,maxblength,maxifg,dualchandec,ifgradius,nphaspts

implicit none

character(len=*),intent(in) :: measfile
integer,intent(in) :: nptrfirstdir,nofblock
integer,dimension(maxblock),intent(out) :: blocktype,blocklength,blockptr
integer,intent(out) :: nifg
logical,intent(inout) :: file_is_intact

character(len=1) :: charbyte
logical :: dualifg
integer :: i,nifga,nifgb,iwert,iunit,iowert,next_free_unit

iunit = next_free_unit()

open (iunit,file = trim(measfile),form='unformatted',access ='stream',status = 'old',action = 'read',iostat = iowert)

do i = 1,nptrfirstdir
    read(iunit) charbyte
end do

do i = 1,nofblock
    read(iunit) iwert
    blocktype(i) = mod(iwert,2**16)
    read(iunit) blocklength(i)
    blocklength(i) = 4 * blocklength(i)
    read(iunit) blockptr(i)
end do

close (iunit)

nifga = 0
nifgb = 0
dualifg = .false.
do i = 1,nofblock
   if (blocktype(i) .eq. 2055) then
        nifga = blocklength(i)
    end if
    ! dual channel?
    if (blocktype(i) .eq. 34823) then
        dualifg = .true.
        nifgb = blocklength(i)
    end if
end do

if (dualifg .neqv. dualchandec) then
    call warnout ('Inconsistent dualifg!') 
    file_is_intact = .false.   
end if

if (nifga .eq. 0) then
    call warnout('Zero IFG block size!')
    file_is_intact = .false.
end if

if (dualchandec .and. nifga .ne. nifgb) then
    call warnout('Differing sizes of dual channel IFGs!')
    file_is_intact = .false.
else
    if (mod(nifga,8) .ne. 0) then
        print*, measfile
        call warnout('Unexpected IFG size!')
        file_is_intact = .false.
    end if
    nifg = nifga / 8
end if

if (nifg .gt. maxifg) then
    call warnout('Note: nifg > maxifg')
    file_is_intact = .false.
end if

if (nifg .lt. ifgradius + nphaspts + 1) then
    call warnout('IFG size too small!')
    file_is_intact = .false.
end if

end subroutine read_opus_dir



!====================================================================
!  read_opus_hdr
!====================================================================
subroutine read_opus_hdr(measfile,nptrfirstdir,nofblock,file_is_intact)

use glob_prepro6, only : maxblock

implicit none

character(len=*),intent(in) :: measfile
integer,intent(out) :: nptrfirstdir,nofblock
logical,intent(inout) :: file_is_intact

integer :: ntest,magic,iunit,iowert,next_free_unit
real(8) :: progver

iunit = next_free_unit()

open (iunit,file = trim(measfile),form='unformatted',access ='stream',status = 'old',action = 'read',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(measfile)
    call warnout('Cannot open measurement file!')
    file_is_intact = .false.
end if

read(iunit) magic
if (magic .ne. -16905718) then
    print *,'measurement file:',trim(measfile)
    call warnout('Not an OPUS file!')
    file_is_intact = .false.
end if

read(iunit) progver
!print *,progver

read(iunit) nptrfirstdir
!print *,nptrfirstdir

read(iunit) ntest ! Angabe maxblock
!print *,ntest

read(iunit) nofblock
!print *,nofblock
if (nofblock .gt. maxblock) then
    print *,'measurement file:',trim(measfile)
    call warnout('nofblock too big!')
    file_is_intact = .false.
end if

close (iunit)

end subroutine read_opus_hdr



!====================================================================
! read_opus_parms           
!====================================================================
subroutine read_opus_parms(imeas,measfile,nofblock,blocktype,blocklength,blockptr,file_is_intact)

use glob_prepro6,only : maxblock,maxblength
use glob_OPUSparms6

implicit none

character(len=*),intent(in) :: measfile
integer,intent(in) :: imeas,nofblock
integer,dimension(maxblock),intent(in) :: blocktype,blocklength,blockptr
logical,intent(inout) :: file_is_intact

integer :: i,iunit,iowert,next_free_unit
character(len=maxblength) :: binchar

! read variables from blocktype 32: HFL,LWN,GFW,GBW,TSC,SSM
do i = 1,nofblock
   if (blocktype(i) .eq. 32) exit
end do

iunit = next_free_unit()

open (iunit,file = trim(measfile),form='unformatted',access ='stream',status = 'old',action = 'read',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(measfile)
    call warnout('Cannot open measurement file!')
    file_is_intact = .false.
end if

if (blocklength(i) .gt. maxblength) then
    print *,trim(measfile)
    call warnout('Max blocklength exceeded!')
    file_is_intact = .false.
end if

read(unit = iunit,pos = blockptr(i) + 1) binchar(1:blocklength(i))
close (iunit)

call OPUS_eval_int(blocklength(i),binchar,'GFW',OPUS_parms(imeas)%GFW)
call OPUS_eval_int(blocklength(i),binchar,'GBW',OPUS_parms(imeas)%GBW)
call OPUS_eval_dble(blocklength(i),binchar,'HFL',OPUS_parms(imeas)%HFL)
call OPUS_eval_dble(blocklength(i),binchar,'LWN',OPUS_parms(imeas)%LWN)
call OPUS_eval_dble(blocklength(i),binchar,'TSC',OPUS_parms(imeas)%TSC)
call OPUS_eval_dble(blocklength(i),binchar,'DUR',OPUS_parms(imeas)%DUR)

! read variables from blocktype 48: NSS,AQM
do i = 1,nofblock
   if (blocktype(i) .eq. 48) exit
end do

iunit = next_free_unit()

open (iunit,file = trim(measfile),form='unformatted',access ='stream',status = 'old',action = 'read',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(measfile)
    call warnout('Cannot open measurement file!')
    file_is_intact = .false.
end if

if (blocklength(i) .gt. maxblength) then
    print *,trim(measfile)
    call warnout('Max blocklength exceeded!')
    file_is_intact = .false.
end if

read(unit = iunit,pos = blockptr(i) + 1) binchar(1:blocklength(i))
close (iunit)

!call OPUS_eval_char(blocklength,binchar,'VEL',OPUS_parms(imeas)%VEL)
!print*,OPUS_parms(imeas)%VEL

call OPUS_eval_int(blocklength(i),binchar,'NSS',OPUS_parms(imeas)%NSS)
call OPUS_eval_char(blocklength(i),binchar,'AQM',OPUS_parms(imeas)%AQM)
call OPUS_eval_dble(blocklength(i),binchar,'RES',OPUS_parms(imeas)%RES)

! read variables from blocktype 96: VEL,HPF,LPF
do i = 1,nofblock
   if (blocktype(i) .eq. 96) exit
end do

iunit = next_free_unit()

open (iunit,file = trim(measfile),form='unformatted',access ='stream',status = 'old',action = 'read',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(measfile)
    call warnout('Cannot open measurement file!')
    file_is_intact = .false.
end if

if (blocklength(i) .gt. maxblength) then
    print *,trim(measfile)
    call warnout('Max blocklength exceeded!')
    file_is_intact = .false.
end if

read(unit = iunit,pos = blockptr(i) + 1) binchar(1:blocklength(i))
close (iunit)

call OPUS_eval_char(blocklength(i),binchar,'VEL',OPUS_parms(imeas)%VEL)
call OPUS_eval_char(blocklength(i),binchar,'HPF',OPUS_parms(imeas)%HPF)
call OPUS_eval_char(blocklength(i),binchar,'LPF',OPUS_parms(imeas)%LPF)

! read variables from blocktype 2071: DAT,TIM

do i = 1,nofblock
   if (blocktype(i) .eq. 2071) exit
end do

iunit = next_free_unit()

open (iunit,file = trim(measfile),form='unformatted',access ='stream',status = 'old',action = 'read',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(measfile)
    call warnout('Cannot open measurement file!')
    file_is_intact = .false.
end if

if (blocklength(i) .gt. maxblength) then
    print *,trim(measfile)
    call warnout('Max blocklength exceeded!')
    file_is_intact = .false.
end if

read(unit = iunit,pos = blockptr(i) + 1) binchar(1:blocklength(i))
close (iunit)

call OPUS_eval_char(blocklength(i),binchar,'DAT',OPUS_parms(imeas)%DAT)
call OPUS_eval_char(blocklength(i),binchar,'TIM',OPUS_parms(imeas)%TIM)

end subroutine read_opus_parms



!====================================================================
!  read_refspec
!====================================================================
subroutine read_refspec(refspecfile,maxspc,refspec)

implicit none

character(len=*),intent(in) :: refspecfile
integer,intent(in) :: maxspc
real,dimension(maxspc),intent(out) :: refspec

integer :: i,icount,ixpos,iunit,iowert,next_free_unit
real :: wert
real(8) :: a0,a1,a2,a3,a4,xpos,rest,gridratio
real,dimension(:),allocatable :: wrkspec

iunit = next_free_unit()
! check availability of file, number of file entries
open (iunit,file = trim(refspecfile),status = 'old',iostat = iowert)
if (iowert .ne. 0) then
    print *,trim(refspecfile)
    call warnout('Cannot open refspec file!')
end if

icount = 0
do
    read(iunit,*,end = 102) wert
    icount = icount + 1
end do
102 continue
close (iunit)

if (icount .lt. maxspc) then
    print *,'maxspc:',maxspc
    print *,'icount:',icount
    call warnout('Incompatible # of entries in refspec!')
end if

iunit = next_free_unit()
open (iunit,file = trim(refspecfile),status = 'old',iostat = iowert)
if (icount .gt. maxspc) then
    allocate (wrkspec(icount))    
    do i = 1,icount
        read(iunit,*) wrkspec(i)
    end do
    close (iunit)
    ! interpolation on output grid
    gridratio = real(icount - 1,8) / real(maxspc - 1,8)
    refspec(1) = wrkspec(1)
    xpos = 1.0d0 + gridratio
    ixpos = nint(xpos)
    rest = xpos - real(ixpos,8)
    a0 = wrkspec(ixpos)
    a1 = 0.5d0 * (wrkspec(ixpos + 1) - wrkspec(ixpos - 1))
    a2 = 0.125d0 * (wrkspec(ixpos-1) - 2.0d0 * wrkspec(ixpos) + wrkspec(ixpos+1))
    refspec(2) = a0 + rest * (a1 + rest * a2)
    do i = 3,maxspc - 2
        xpos = 1.0d0 + gridratio * real(i - 1,8)
        ixpos = nint(xpos)
        rest = xpos - real(ixpos,8)
        a0 = wrkspec(ixpos)
        a1 = wrkspec(ixpos - 2) / 12.0d0 - 2.0d0 * wrkspec(ixpos - 1) &
          / 3.0d0 + 2.0d0 * wrkspec(ixpos + 1) / 3.0d0 - wrkspec(ixpos + 2) / 12.0d0
        a2 = - wrkspec(ixpos - 2) / 24.0d0 + 2.0d0 * wrkspec(ixpos - 1) / 3.0d0 - 5.0d0 * wrkspec(ixpos) / 4.0d0 &
          + 2.0d0 * wrkspec(ixpos + 1) / 3.0d0 - wrkspec(ixpos + 2) / 24.0d0
        a3 = - wrkspec(ixpos - 2) / 12.0d0 + wrkspec(ixpos - 1) / 6.0d0 - wrkspec(ixpos + 1) / 6.0d0 &
          + wrkspec(ixpos + 2) / 12.0d0
        a4 = wrkspec(ixpos - 2) / 24.0d0 - wrkspec(ixpos - 1) / 6.0d0 + 0.25d0 * wrkspec(ixpos) - wrkspec(ixpos + 1) &
          / 6.0d0 + wrkspec(ixpos + 2) / 24.0d0
        refspec(i) = a0 + rest * (a1 + rest * (a2 + rest * (a3 + rest * a4)))
    end do
    xpos = 1.0d0 + gridratio * real(maxspc - 2,8)
    ixpos = nint(xpos)
    rest = xpos - real(ixpos,8)
    a0 = wrkspec(ixpos)
    a1 = 0.5d0 * (wrkspec(ixpos + 1) - wrkspec(ixpos - 1))
    a2 = 0.125d0 * (wrkspec(ixpos-1) - 2.0d0 * wrkspec(ixpos) + wrkspec(ixpos+1))
    refspec(maxspc - 1) = a0 + rest * (a1 + rest * a2)
    refspec(maxspc) = wrkspec(icount)
    deallocate (wrkspec)
else
    do i = 1,icount
        read(iunit,*) refspec(i)
    end do
    close (iunit)
end if

end subroutine read_refspec



!====================================================================
!  read_reftrmT
!====================================================================
subroutine read_reftrmT(refspecfile,maxT,maxspc,reftrmT)

implicit none

character(len=*),intent(in) :: refspecfile
integer,intent(in) :: maxT,maxspc
real,dimension(maxT,maxspc),intent(out) :: reftrmT

character(len=376) :: zeile
integer :: i,j,icount,iunit,iowert,next_free_unit

iunit = next_free_unit()
! check availability of file, number of file entries
open (iunit,file = trim(refspecfile),status = 'old',iostat = iowert)

if (iowert .ne. 0) then
    print *,trim(refspecfile)
    call warnout('Cannot open refspec file!')
end if

icount = 0
do
    read(iunit,'(A376)',end = 102) zeile
    icount = icount + 1
end do
102 continue
close (iunit)

if (icount .ne. maxspc) then
    print *,'maxspc:',maxspc
    print *,'icount:',icount
    call warnout('Incompatible # of entries in reftrmT!')
end if

iunit = next_free_unit()
open (iunit,file = trim(refspecfile),status = 'old',iostat = iowert)  
do i = 1,maxspc
    read(iunit,'(A376)') zeile
    read (zeile,'(E12.5,28(1X,E12.5))') (reftrmT(j,i),j = 1,maxT)
end do
close (iunit)

end subroutine read_reftrmT



!====================================================================
!  tofile_spec
!====================================================================
subroutine tofile_spec(ausdatei,nspec,spec)

implicit none

character(len=*),intent(in) :: ausdatei
integer,intent(in) :: nspec
real,dimension(nspec),intent(in) :: spec

integer :: i,iunit,next_free_unit

iunit = next_free_unit()

open (iunit,file = ausdatei,status = 'replace')

do i = 1,nspec
    write(iunit,'(ES13.6)') spec(i)
end do

close (iunit)

end subroutine tofile_spec




!====================================================================
!� Warnung rausschreiben und Programm evtl. beenden
!====================================================================
subroutine warnout(text)

use ISO_FORTRAN_ENV, only : ERROR_UNIT

implicit none

character(len=*),intent(in) :: text

print '(A)', trim(text)

end subroutine warnout
