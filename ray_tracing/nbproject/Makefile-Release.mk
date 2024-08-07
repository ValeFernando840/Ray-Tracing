#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Environment
MKDIR=mkdir
CP=cp
GREP=grep
NM=nm
CCADMIN=CCadmin
RANLIB=ranlib
CC=gcc
CCC=g++
CXX=g++
FC=gfortran
AS=as

# Macros
CND_PLATFORM=Cygwin_1-Windows
CND_DLIB_EXT=dll
CND_CONF=Release
CND_DISTDIR=dist
CND_BUILDDIR=build

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/Principal.o \
	${OBJECTDIR}/Sub_Back_Up.o \
	${OBJECTDIR}/Sub_Carpol.o \
	${OBJECTDIR}/Sub_ELectx2.o \
	${OBJECTDIR}/Sub_Elect1.o \
	${OBJECTDIR}/Sub_Frec_plasma.o \
	${OBJECTDIR}/Sub_Graze.o \
	${OBJECTDIR}/Sub_Grid.o \
	${OBJECTDIR}/Sub_Hamltn.o \
	${OBJECTDIR}/Sub_Latlon.o \
	${OBJECTDIR}/Sub_Polcoe.o \
	${OBJECTDIR}/Sub_Porcar.o \
	${OBJECTDIR}/Sub_Reach.o \
	${OBJECTDIR}/Sub_Rindex.o \
	${OBJECTDIR}/Sub_Rkam.o \
	${OBJECTDIR}/Sub_Trace.o \
	${OBJECTDIR}/Sub_Zero.o \
	${OBJECTDIR}/Sub_cira.o \
	${OBJECTDIR}/Sub_igrf.o \
	${OBJECTDIR}/Sub_iridreg.o \
	${OBJECTDIR}/Sub_iriflip.o \
	${OBJECTDIR}/Sub_irifun.o \
	${OBJECTDIR}/Sub_irisub.o \
	${OBJECTDIR}/Sub_iritec.o \
	${OBJECTDIR}/Sub_read_W.o


# C Compiler Flags
CFLAGS=

# CC Compiler Flags
CCFLAGS=
CXXFLAGS=

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/ray_tracing.exe

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/ray_tracing.exe: ${OBJECTFILES}
	${MKDIR} -p ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.f} -o ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/ray_tracing ${OBJECTFILES} ${LDLIBSOPTIONS}

${OBJECTDIR}/Principal.o: Principal.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Principal.o Principal.for

${OBJECTDIR}/Sub_Back_Up.o: Sub_Back_Up.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Back_Up.o Sub_Back_Up.for

${OBJECTDIR}/Sub_Carpol.o: Sub_Carpol.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Carpol.o Sub_Carpol.for

${OBJECTDIR}/Sub_ELectx2.o: Sub_ELectx2.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_ELectx2.o Sub_ELectx2.for

${OBJECTDIR}/Sub_Elect1.o: Sub_Elect1.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Elect1.o Sub_Elect1.for

${OBJECTDIR}/Sub_Frec_plasma.o: Sub_Frec_plasma.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Frec_plasma.o Sub_Frec_plasma.for

${OBJECTDIR}/Sub_Graze.o: Sub_Graze.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Graze.o Sub_Graze.for

${OBJECTDIR}/Sub_Grid.o: Sub_Grid.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Grid.o Sub_Grid.for

${OBJECTDIR}/Sub_Hamltn.o: Sub_Hamltn.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Hamltn.o Sub_Hamltn.for

${OBJECTDIR}/Sub_Latlon.o: Sub_Latlon.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Latlon.o Sub_Latlon.for

${OBJECTDIR}/Sub_Polcoe.o: Sub_Polcoe.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Polcoe.o Sub_Polcoe.for

${OBJECTDIR}/Sub_Porcar.o: Sub_Porcar.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Porcar.o Sub_Porcar.for

${OBJECTDIR}/Sub_Reach.o: Sub_Reach.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Reach.o Sub_Reach.for

${OBJECTDIR}/Sub_Rindex.o: Sub_Rindex.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Rindex.o Sub_Rindex.for

${OBJECTDIR}/Sub_Rkam.o: Sub_Rkam.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Rkam.o Sub_Rkam.for

${OBJECTDIR}/Sub_Trace.o: Sub_Trace.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Trace.o Sub_Trace.for

${OBJECTDIR}/Sub_Zero.o: Sub_Zero.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_Zero.o Sub_Zero.for

${OBJECTDIR}/Sub_cira.o: Sub_cira.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_cira.o Sub_cira.for

${OBJECTDIR}/Sub_igrf.o: Sub_igrf.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_igrf.o Sub_igrf.for

${OBJECTDIR}/Sub_iridreg.o: Sub_iridreg.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_iridreg.o Sub_iridreg.for

${OBJECTDIR}/Sub_iriflip.o: Sub_iriflip.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_iriflip.o Sub_iriflip.for

${OBJECTDIR}/Sub_irifun.o: Sub_irifun.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_irifun.o Sub_irifun.for

${OBJECTDIR}/Sub_irisub.o: Sub_irisub.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_irisub.o Sub_irisub.for

${OBJECTDIR}/Sub_iritec.o: Sub_iritec.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_iritec.o Sub_iritec.for

${OBJECTDIR}/Sub_read_W.o: Sub_read_W.for
	${MKDIR} -p ${OBJECTDIR}
	$(COMPILE.f) -O2 -o ${OBJECTDIR}/Sub_read_W.o Sub_read_W.for

# Subprojects
.build-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}
	${RM} *.mod

# Subprojects
.clean-subprojects:

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
