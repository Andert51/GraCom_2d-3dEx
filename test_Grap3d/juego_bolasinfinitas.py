import numpy as np
import pygame,sys
from pygame.locals import *
import random
import os


def norm(a=list):
	b=0.
	for i in range(len(a)):
		b=b+a[i]**2
	b=np.sqrt(b)
	return(b)


R=30
alto = 500
ancho = 1000
profundo=700
cerca=-700
h=0
Xfrut=0
Yfrut=0
Zfrut=0


X0=[(ancho/2)]
Y0=[alto-R]
Z0=[0]
Ri=[R]
h0z=0
vx=[0]
vy=[0]
vz=[0]
ax=0
ay=0
az=0
DELAY=16
x=[X0[0]]
y=[Y0[0]]
z=[Z0[0]]
taupiso=0.95
tau=0.998
tau0=tau


cerca0Cam=0.1
Lejos0Cam=5000
Xeje=1900
Yeje=800
Zeje=700
angx=0.
angy=0.
angz=0.
distvisionT=0.000001
distvisionT2=cerca0Cam





paredy1=0
paredy2=-1000
paredx1=1000
paredx2=-1000
paredz1=1000
paredz2=-1000

usoKEYUP=False
usoKEYDOWN=False
usoKEYRIGHT=False
usoKEYLEFT=False
usoKEY2=False
usoKEY4=False
usoKEY6=False
usoKEY8=False
usoMOVTRASFron=False
usoMOVTRASBack=False
usoMOVTRASLeft=False
usoMOVTRASRight=False
usoMOVTRASUp=False
usoMOVTRASDown=False
usoKEYDRCOM1=False
usoKEYDRCOM2=False
Slow=False
DRAGMOUSE=True #con esto activado jugamos fullscreen y somos una bola :D 


ck1=0
ck2=0
ck3=0
ck4=0
intervalo=5
modvx=0.
modvy=0.
dvx=0.
minvYpiso=0.01



drP=[1]
dr=1
dt=100
drz=5000
zoom=1
Setcontroldrag=1000
Setcontroldrag2=50
FrozEstPiso=0.2



FuerzaControl=10
tita=0.	
phi=0.				
XVER=-1
YVER=-1			
Cuadrante=4
PAREDES=True
CHOQUES=True


CantBolas=1
X=0
Y=0
Z=0
M=[1000]
kill=[False]
m=[1]
G=3000
Fx=0.
Fy=0.
Fz=0.
r=0.


poligonX=[0]
poligonY=[0]
poligonX0=[0]
poligonY0=[0]


FIJO=[False]
PxFijo=[0]
PyFijo=[0]
PzFijo=[0]
select=1

CLAVADO=False
CLAVADO2=False
CamFija=False
BarraON=False
freez=False
Propia=0
ESCRITURA=True
VISOR=False
Enfijo=False
AnalisRay=False



Trozo=ancho/(2*zoom)
trozo2=alto/(2*zoom)
rADIO0=[norm([cerca0Cam,Trozo,trozo2])]




#_____________________
movang=2*FuerzaControl/10*np.pi/(100*zoom)
movtras=1
movtrasz=1
FuerzaControlvieja=FuerzaControl
#____________________

pygame.init()
ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_caption("Spaceinvader")
ancho, alto=pygame.display.get_window_size()
MOUSED1=[ancho/2,alto/2]
img=[pygame.image.load("spaceinvader.png")]
#imgPared=pygame.image.load("pared.png")
rect=[img[0].get_rect()]
#rectPared=imgPared.get_rect()
#frompng=pygame.image.tostring()

#MODO PREsinTACION
#imgPELON=pygame.image.load("pelonazo.png")
#rectPELON=imgPELON.get_rect()

LabelSys1=pygame.font.SysFont("Calibri", 20)
LabelSys2=pygame.font.SysFont("Calibri", 30)
fnt=20
fnt2=50
freez2=False



def MROTx(a):
	return(np.array([[1, 0,0],[0,np.cos(a),np.sin(a)],[0, -np.sin(a),np.cos(a)]]))

def MROTy(a):
	return(np.array([[np.cos(a),0, -np.sin(a)],[0,1, 0],[np.sin(a),0,np.cos(a)]]))

def MROTz(a):
	return(np.array([[np.cos(a),np.sin(a),0],[ -np.sin(a),np.cos(a),0],[ 0,0,1]]))

def MDRZ():
	return(np.array([[1,0,0],[0,1,0],[ 0,0,1/drz]]))

def MEb(angX0, angY0, angZ0, v):
	ver1=np.dot(MROTz(angZ0),v)
	ver2=np.dot(MROTy(angY0),ver1)
	ver3=np.dot(MROTx(angX0),ver2)
	ver4=np.dot(MDRZ(),ver3)
	return(ver4)

def MbE(angX0, angY0, angZ0, v):
	ver1=np.dot(MROTx(-angX0),v) 
	ver2=np.dot(MROTy(-angY0),ver1)
	ver3=np.dot(MROTz(-angZ0),ver2)
	ver4=np.dot(MDRZ(),ver3)
	return(ver4)

def PRYV(v=list):
	XEJE=np.array([Xeje,Yeje,Zeje])
	offset=np.array([ancho/2, alto/2, 0])
	FL1=np.array([v[0],v[1],v[2]])
	Vp0=MEb(angx, angy, angz, FL1-XEJE)
	prX=(int((cerca0Cam/(Vp0[2]))*Vp0[0]*zoom+offset[0]))
	prY=(int((cerca0Cam/(Vp0[2]))*Vp0[1]*zoom+offset[1]))
	return((prX, prY))

def PRYV2(v=list, v2=list):
	XEJE=np.array([Xeje,Yeje,Zeje])
	offset=np.array([ancho/2, alto/2, 0])
	FL1=np.array([v[0],v[1],v[2]])
	Vp0=MEb(angx, angy, angz, FL1-XEJE)
	prX=(int((cerca0Cam/(Vp0[2]))*Vp0[0]*zoom+offset[0]))
	prY=(int((cerca0Cam/(Vp0[2]))*Vp0[1]*zoom+offset[1]))
	return((prX, prY))

def ProyLinea(fin=list,ini=list, color=list, AnaRayT=bool):
	AnalisRay=AnaRayT
	FL1=np.array([fin[0],fin[1],fin[2]])
	RXYZ=np.array([ini[0],ini[1],ini[2]])
	XEJE=np.array([Xeje, Yeje, Zeje])
	offset=np.array([ancho/2, alto/2, 0])
	V=RXYZ-XEJE
	Vp=FL1-RXYZ
	Vp0=MEb(angx, angy, angz, V)
	Vp=MEb(angx, angy, angz, Vp)
	dibu=False
	Vp=Vp+Vp0
	if Vp0[2]>=distvisionT:
		pr0X1 = int((cerca0Cam/(Vp0[2]))*Vp0[0]+offset[0])
		pr0Y1 = int((cerca0Cam/(Vp0[2]))*Vp0[1]+offset[1])
	else:
		if AnalisRay==True:
			if Vp[2]>=distvisionT:
				pr1X1 = int((cerca0Cam/(Vp[2]))*Vp[0]*zoom+offset[0])
				pr1Y1 = int((cerca0Cam/(Vp[2]))*Vp[1]*zoom+offset[1])
				pr0X1 = int(((Vp[0]-Vp0[0])*(distvisionT-Vp0[2]/(Vp[2]-Vp0[2]))+Vp0[0])*zoom+offset[0])
				pr0Y1 = int(((Vp[1]-Vp0[1])*(distvisionT-Vp0[2]/(Vp[2]-Vp0[2]))+Vp0[1])*zoom+offset[1])
				dibu=True

				try:
					pygame.draw.line(ventana, (color[0],color[1],color[2]), (pr0X1, pr0Y1), (pr1X1,pr1Y1), 3)
				except:
					pass
	if dibu==True:
		pass
	else:
		if Vp[2]>=distvisionT:
			pr1X1 = int((cerca0Cam/(Vp[2]))*Vp[0]*zoom+offset[0])
			pr1Y1 = int((cerca0Cam/(Vp[2]))*Vp[1]*zoom+offset[1])
			try:
				pygame.draw.line(ventana, (color[0],color[1],color[2]), (pr0X1, pr0Y1), (pr1X1,pr1Y1), 3)
			except:
				pass




def ProyPoli(fin=list,color=list):
	fin2=fin
	delante=[]
	delante2=[]
	inicio=[]
	final=[]
	movidos={}
	fuera=0
	dibuja=True
	XEJE=np.array([Xeje, Yeje, Zeje])
	offset=np.array([ancho/2, alto/2, 0])

	#buscamos los puntos por delante de la pantalla
	# y creamos un array que indica que puntos estan delante y cuales detras
	for i in range(len(fin2)):
		
		FL1=np.array([fin2[i][0],fin2[i][1],fin2[i][2]])
		Vp0=MEb(angx, angy, angz, FL1-XEJE)
		if Vp0[2]>=distvisionT2:

			delante.append(1)
			next
		else:
			delante.append(0)
			fuera=fuera+1

		
	#mejoramos el array creado "delante" segun la clasificación: "detras" (0), "inicio/final" (1), "delante" (2).
	# los puntos que marcan el inicio o final de lo que vemos los usaremos para ver un poco mas allá.
	# y los haremos "extenderse" hasta el punto no visible mas cercano para encontrar una correcta proyección en la pantalla.
	# (con extenderse nos referimos a crear un punto "virtual" en la zona visible del mapa cuya proyección coincida con la que
	# debería ser del objeto), para esto trazamos una rexta entre el punto donde esta el objeto y el espectador, y dibujamos como 
	# si el punto estuviera en el corte de esta recta con la pantalla.

	#antes de refinar la clasificación vemos q no halla dado justo "todo detras" o "todo delante", en tal caso no hay nada que 
	# clasificar.

	if fuera==0: #caso todo delante
		prX=[]
		prY=[]
		prXY=[]
		for i in range(len(fin2)):
			FL1=np.array([fin2[i][0],fin2[i][1],fin2[i][2]])
			prXY.append(PRYV(FL1))
		prXY.append(prXY[0])
		pygame.draw.polygon(ventana, (color[0]*np.cos(angx+angy + angz)**2,color[1]*np.cos(angx+angy + angz)**2,color[2]*np.cos(angx+angy + angz)**2),prXY , 0)
	elif fuera==len(fin2):  #caso todo detras
		pass

	else:
		halloprim=False
		guarh=0
		Saltofin=False
		for i in range(len(fin2)):
			if delante[i]==1:
				
				sig=i+1
				ant=i-1
				act=i
				if sig>len(fin2)-1:
					sig=sig-len(fin2)
				if ant<0:
					ant=ant+len(fin2)


				if delante[sig]>0:
					if delante[ant]>0:
						delante[i]=2
					else:
						inicio.append(i)
						halloprim=True

				else:
					if delante[ant]==0:
						inicio.append(i)
						final.append(i)
						halloprim=True
					else:
						if halloprim==False:
							guarh=i
							Saltofin=True
						else:
							final.append(i)
				print("creando:", inicio,"-" , final)

		if Saltofin==True:
			final.append(guarh)

		print("creando fin:", inicio,"-" , final)

	for i in inicio:
		sig=i+1
		ant=i-1
		act=i
		if sig>len(fin2)-1:
			sig=sig-len(fin2)
		if ant<0:
			ant=ant+len(fin2)

		prX=[]
		prY=[]
		prXY=[]
		if i in final:


			FL1=np.array([fin2[i][0],fin2[i][1],fin2[i][2]])
			FL2=np.array([fin2[ant][0],fin2[ant][1],fin2[ant][2]])
			Vp0=MEb(angx, angy, angz, FL1-XEJE)
			Vp02=MEb(angx, angy, angz, FL2-XEJE)
			dVb=Vp02-Vp0
			
			t0=(distvisionT2-Vp0[2])/dVb[2]
			Vp0=Vp0+t0*(dVb)
			pro1=(cerca0Cam/(Vp0[2]))*Vp0[0]*zoom
			pro2=(cerca0Cam/(Vp0[2]))*Vp0[1]*zoom
			if pro1>ancho*2/3*3/4:
				pro1=ancho*2/3*3/4
			if pro1<-ancho*2/3*3/4:
				pro1=-ancho*2/3*3/4

			if pro2>alto*2/3*3/4:
				pro2=alto*2/3*3/4
			if pro2<-alto*2/3*3/4:
				pro2=-alto*2/3*3/4


			prX=(int(pro1+offset[0]))
			prY=(int(pro2+offset[1]))

			prXY.append((prX, prY))


			FL1=np.array([fin2[i][0],fin2[i][1],fin2[i][2]])
			Vp0=MEb(angx, angy, angz, FL1-XEJE)
			prX=(int((cerca0Cam/(Vp0[2]))*Vp0[0]*zoom+offset[0]))
			prY=(int((cerca0Cam/(Vp0[2]))*Vp0[1]*zoom+offset[1]))
			prXY.append((prX, prY))


			FL1=np.array([fin2[i][0],fin2[i][1],fin2[i][2]])
			FL2=np.array([fin2[sig][0],fin2[sig][1],fin2[sig][2]])
			Vp0=MEb(angx, angy, angz, FL1-XEJE)
			Vp02=MEb(angx, angy, angz, FL2-XEJE)
			dVb=Vp02-Vp0
			
			t0=(distvisionT2-Vp0[2])/dVb[2]
			Vp0=Vp0+t0*(dVb)
			pro1=(cerca0Cam/(Vp0[2]))*Vp0[0]*zoom
			pro2=(cerca0Cam/(Vp0[2]))*Vp0[1]*zoom
			if pro1>ancho*2/3*3/4:
				pro1=ancho*2/3*3/4
			if pro1<-ancho*2/3*3/4:
				pro1=-ancho*2/3*3/4

			if pro2>alto*2/3*3/4:
				pro2=alto*2/3*3/4
			if pro2<-alto*2/3*3/4:
				pro2=-alto*2/3*3/4

			prX=(int(pro1+offset[0]))
			prY=(int(pro2+offset[1]))
			prXY.append((prX, prY))	


		else:

			ultppoly=final[inicio.index(i)]
			if final[inicio.index(i)]-i<0:
				ultppoly=len(fin2)+final[inicio.index(i)]


			for n in range(i, ultppoly+1):
				sig=n+1
				ant=n-1
				act=n
				if sig>len(fin2)-1:
					sig=sig-len(fin2)
				if sig<0:
					sig=sig+len(fin2)
				if act>len(fin2)-1:
					act=act-len(fin2)
				if act<0:
					act=act+len(fin2)
				if ant>len(fin2)-1:
					ant=ant-len(fin2)
				if ant<0:
					ant=ant+len(fin2)
				

				if n==i:

					FL1=np.array([fin2[act][0],fin2[act][1],fin2[act][2]])
					FL2=np.array([fin2[ant][0],fin2[ant][1],fin2[ant][2]])

					V2=FL2-XEJE
					V1=FL1-XEJE
					Vp0=MEb(angx, angy, angz, V1)
					Vp02=MEb(angx, angy, angz, V2)
					dVb=Vp02-Vp0
					
					t0=(distvisionT2-Vp0[2])/dVb[2]

					Vp0=Vp0+t0*(dVb)
					pro1=(cerca0Cam/(Vp0[2]))*Vp0[0]*zoom
					pro2=(cerca0Cam/(Vp0[2]))*Vp0[1]*zoom
					if pro1>ancho*2/3*3/4:
						pro1=ancho*2/3*3/4
					if pro1<-ancho*2/3*3/4:
						pro1=-ancho*2/3*3/4

					if pro2>alto*2/3*3/4:
						pro2=alto*2/3*3/4
					if pro2<-alto*2/3*3/4:
						pro2=-alto*2/3*3/4

					prX=(int(pro1+offset[0]))
					prY=(int(pro2+offset[1]))
					prXY.append((prX, prY))
					print("dibu: tipo Inicio-1:",prX, prY)

					Vp0=MEb(angx, angy, angz, FL1-XEJE)
					pro1=(cerca0Cam/(Vp0[2]))*Vp0[0]*zoom
					pro2=(cerca0Cam/(Vp0[2]))*Vp0[1]*zoom

					prX=(int(pro1+offset[0]))
					prY=(int(pro2+offset[1]))
					prXY.append((prX, prY))
					print("dibu: tipo Inicio:",prX, prY)


				elif n==ultppoly:
					

					FL1=np.array([fin2[act][0],fin2[act][1],fin2[act][2]])
					Vp0=MEb(angx, angy, angz, FL1-XEJE)
					pro1=(cerca0Cam/(Vp0[2]))*Vp0[0]*zoom
					pro2=(cerca0Cam/(Vp0[2]))*Vp0[1]*zoom

					prX=(int(pro1+offset[0]))
					prY=(int(pro2+offset[1]))
					prXY.append((prX, prY))
					print("dibu: tipo fin:",prX, prY)

					FL1=np.array([fin2[act][0],fin2[act][1],fin2[act][2]])
					FL2=np.array([fin2[sig][0],fin2[sig][1],fin2[sig][2]])
					Vp0=MEb(angx, angy, angz, FL1-XEJE)
					Vp02=MEb(angx, angy, angz, FL2-XEJE)
					dVb=Vp02-Vp0
					
					t0=(distvisionT2-Vp0[2])/dVb[2]

					Vp0=Vp0+t0*(dVb)
					pro1=(cerca0Cam/(Vp0[2]))*Vp0[0]*zoom
					pro2=(cerca0Cam/(Vp0[2]))*Vp0[1]*zoom
					if pro1>ancho*2/3*3/4:
						pro1=ancho*2/3*3/4
					if pro1<-ancho*2/3*3/4:
						pro1=-ancho*2/3*3/4

					if pro2>alto*2/3*3/4:
						pro2=alto*2/3*3/4
					if pro2<-alto*2/3*3/4:
						pro2=-alto*2/3*3/4

					prX=(int(pro1+offset[0]))
					prY=(int(pro2+offset[1]))
					prXY.append((prX, prY))
					print("dibu: tipo fin+1:",prX, prY)

				else:

					FL1=np.array([fin2[act][0],fin2[act][1],fin2[act][2]])
					Vp0=MEb(angx, angy, angz, FL1-XEJE)
					prX=(int((cerca0Cam/(Vp0[2]))*Vp0[0]*zoom+offset[0]))
					prY=(int((cerca0Cam/(Vp0[2]))*Vp0[1]*zoom+offset[1]))
					prXY.append((prX, prY))					
					print("dibu: tipo2:",prX, prY)


		prXY.append(prXY[0])
		try:
			pygame.draw.polygon(ventana, (color[0],color[1],color[2]),prXY , 0)
		except:
			pass




def ANGPAREDES(vx, x0, vy, y0, vz, z0):
	if PAREDES==True:
		x=(x0)+(vx)
		y=(y0)+(vy)
		z=(z0)+(vz)
		choquepiso=False


		if y0<paredy1 and y>=paredy1:
			y0=-FrozEstPiso
			vy=-norm([vy])
		elif y0>paredy1 or y>paredy1:
			y0=-FrozEstPiso
			vy=-norm([vy])

		if y0<paredy2 and y>=paredy2:
			y0=paredy2+FrozEstPiso
			vy=norm([vy])
		elif y0<paredy2 or y<paredy2:
			y0=paredy2+FrozEstPiso
			vy=norm([vy])


		if x0<paredx1 and x>=paredx1:
			x0=paredx1-FrozEstPiso
			vx=-norm([vx])
		elif x0>paredx1 or x>paredx1:
			x0=paredx1-FrozEstPiso
			vx=-norm([vx])

		if x0>paredx2 and x<=paredx2:
			x0=paredx2+FrozEstPiso
			vx=norm([vx])
		elif x0<paredx2 or x<paredx2:
			x0=paredx2+FrozEstPiso
			vx=norm([vx])


		if z0<paredz1 and z>=paredz1:
			z0=paredz1-FrozEstPiso
			vz=-norm([vz])
		elif z0>paredz1 or z>paredz1:
			z0=paredz1-FrozEstPiso
			vz=-norm([vz])

		if z0>paredz2 and z<=paredz2:
			z0=paredz2+FrozEstPiso
			vz=norm([vz])
		elif z0<paredz2 or z<paredz2:
			z0=paredz2+FrozEstPiso
			vz=norm([vz])
		#if vy<=0:
		#	if y<=piso<=y0:
		#		choquepiso=True
		#else:
		#	if y>=piso>=y0:
		#		choquepiso=True
		#if choquepiso==True:
		#	y0=int(piso)
		#	alpha=np.pi/2
		#	if norm([vy])<=FrozEstPiso:
		#		vy=0
		#		vx=(vx*(2*((np.sin(alpha))**2)-1)-vy*np.sin(2*alpha))*taupiso
		#	else:
		#		vy=(vy*(2*((np.cos(alpha))**2)-1)-vx*np.sin(2*alpha))*taupiso
		#		vx=(vx*(2*((np.sin(alpha))**2)-1)-vy*np.sin(2*alpha))*taupiso
		#	choquepiso=False
		return([x0, y0, z0, vx, vy, vz])


def Angulos(X, Y, Z):

	Rxy=(X**2+Y**2)**(1/2)
	r=((X)**2+(Y)**2+(Z)**2)**(1/2)
	if X==0:					
		if Y>=0:
			tita=np.pi/2	
		else:
			tita=-(np.pi/2)	
	else:
		if X>0:	
			tita=np.arctan(Y/X)
		if X<0:
			tita=(np.arctan(Y/X))+np.pi

	if Z==0:
		phi=np.pi/2
	else:
		if Z>0:	
			phi=(np.arctan(Rxy/Z))
		if Z<0:
			phi=np.pi-(np.arctan(Rxy/(-Z)))
	return([tita, phi])


def LecturaBolas(i, n, ):
	FxN=0.
	FyN=0.
	FzN=0.
	tita=0.
	phi=0.
	r=0.
	X=0
	Y=0
	Z=0
	if FIJO[n]==True:
		x[n]=PxFijo[n]
		y[n]=PyFijo[n]
		z[n]=PzFijo[n]
	X=(x[i]-x[n])
	Y=(-y[i]+y[n])
	Z=(z[i]-z[n])
	Rxy=(X**2+Y**2)**(1/2)
	r=((X)**2+(Y)**2+(Z)**2)**(1/2)
	LecturAng = Angulos(X,Y,Z)
	tita, phi = LecturAng[0], LecturAng[1]


	if r<rADIO0[i]+rADIO0[n]:
		if X>=0:
			x[i]=x[i]+(rADIO0[i]+rADIO0[n]-r)*np.cos(tita)*np.sin(phi)/((3)**(1/2))
			x[n]=x[n]-(rADIO0[i]+rADIO0[n]-r)*np.cos(tita)*np.sin(phi)/((3)**(1/2))
		else:
			x[i]=x[i]-(rADIO0[i]+rADIO0[n]-r)*np.cos(tita)*np.sin(phi)/((3)**(1/2))
			x[n]=x[n]+(rADIO0[i]+rADIO0[n]-r)*np.cos(tita)*np.sin(phi)/((3)**(1/2))
		if Y>=0:
			y[i]=y[i]+(rADIO0[i]+rADIO0[n]-r)*np.sin(tita)*np.sin(phi)/((3)**(1/2))
			y[n]=y[n]-(rADIO0[i]+rADIO0[n]-r)*np.sin(tita)*np.sin(phi)/((3)**(1/2))
		else:
			y[i]=y[i]-(rADIO0[i]+rADIO0[n]-r)*np.sin(tita)*np.sin(phi)/((3)**(1/2))
			y[n]=y[n]+(rADIO0[i]+rADIO0[n]-r)*np.sin(tita)*np.sin(phi)/((3)**(1/2))
		if Z>=0:
			z[i]=z[i]+(rADIO0[i]+rADIO0[n]-r)*np.cos(phi)/((3)**(1/2))
			z[n]=z[n]-(rADIO0[i]+rADIO0[n]-r)*np.cos(phi)/((3)**(1/2))
		else:
			z[i]=z[i]-(rADIO0[i]+rADIO0[n]-r)*np.cos(phi)/((3)**(1/2))
			z[n]=z[n]+(rADIO0[i]+rADIO0[n]-r)*np.cos(phi)/((3)**(1/2))
		r=rADIO0[i]+rADIO0[n]


	if CHOQUES==True:
		Choq=False
		if r<=rADIO0[i]+rADIO0[n]:

			try:
				if YaChoco[i][0]==True:
					
					Choq=True
					r=rADIO0[i]+rADIO0[n]
			except:
				
				r=rADIO0[i]+rADIO0[n]
				pass

			if Choq==False:

				C=M[n]/M[i]
				vxRes=vx[i]
				vyRes=(-vy[i])
				vzRes=vz[i]

				vxi=vxRes*(1-2*C/(1+C))
				vyi=vyRes*(1-2*C/(1+C))
				vzi=vzRes*(1-2*C/(1+C))
				YaChoco[i]=[True, vxi, -vyi, vzi, 1]


				vxn=2*(vxRes)/(1+C)
				vyn=2*(vyRes)/(1+C)
				vzn=2*(vzRes)/(1+C)
				YaChoco[n]=[True, vxn, -vyn, vzn, 1]


				C2=M[i]/M[n]
				vxRes=vx[n]
				vyRes=(-vy[n])
				vzRes=vz[n]
				vxi=vxRes*(1-2*C2/(1+C2))
				vyi=vyRes*(1-2*C2/(1+C2))
				vzi=vzRes*(1-2*C2/(1+C2))
				YaChoco[n]=[True, YaChoco[n][1]+vxi, YaChoco[n][2]-vyi, YaChoco[n][3]+vzi, 1]

				vxn=2*(vxRes)/(1+C2)
				vyn=2*(vyRes)/(1+C2)
				vzn=2*(vzRes)/(1+C2)
				YaChoco[i]=[True, YaChoco[i][1]+vxn, YaChoco[i][2]-vyn, YaChoco[i][3]+vzn, 1]

	FyN=G*M[n]*r*np.sin(tita)*np.sin(phi)/((r)**3)
	FxN=-G*M[n]*r*np.cos(tita)*np.sin(phi)/((r)**3)
	FzN=-G*M[n]*r*np.cos(phi)/((r)**3)

	return([FxN, FyN, FzN])



def PrintTxt(txt, lentxt, grueso):
	cantxt=len(txt)+1
	lent=grueso
	filas=1
	xtxt=[0]
	ytxt=[0]
	for i in range(0,cantxt):
		if i==0:
			pass

		else:
			lent=lent+lentxt[i-1]*12

		try:
			xtxt[i]=lent+int(i/2)*15
		except:
			xtxt.append(lent+int(i/2)*15)

		if xtxt[i]+50>=ancho:
			filas=filas+1
			xtxt[i]=xtxt[i]-ancho
			lent=lent-ancho+10

		try:
			ytxt[i]=filas*15
		except:
			ytxt.append(filas*15)

	texto=[""]
	for i in range(0,cantxt-1):
		try:
			texto[i]=LabelSys1.render(txt[i],False, (225, 225, 225))
		except:	
			texto.append(LabelSys1.render(txt[i],False, (225, 225, 225)))

		ventana.blit(texto[i], (xtxt[i],ytxt[i]))
	return(filas)














YaChoco={}
Choq=False
h0=0
pygame.mouse.set_visible(False)
file = open("prueba1.dat", "w")
#file.write("Hello people this is the start of the first try in the story of the writes in python in the course of learning"+os.linesep)
#file.write(""+os.linesep+os.linesep+os.linesep)


jugando = True
# Empieza el Juego...
while jugando:
	PTotal=0
	print("h:", h)

	piso=int(alto-R/2-Yeje)
	techo=int(0+R/2-Yeje)
	pared0=int(0+R/2-Xeje)
	pared1=int(ancho-R/2-Xeje)

	h=h+1

	if CantBolas==1:
		Fy=0
		Fx=0
		Fz=0

		vy[0]=(vy[0]*tau+Fy+ay)
		vx[0]=(vx[0]*tau+Fx+ax)
		vz[0]=(vz[0]*tau+Fz+az)

		if PAREDES==True:
			Rebote=ANGPAREDES(vx[0]/dt, x[0], vy[0]/dt, y[0], vz[0]/dt, z[0])
			x[0]=Rebote[0]
			y[0]=Rebote[1]
			z[0]=Rebote[2]
			vx[0]=Rebote[3]*dt
			vy[0]=Rebote[4]*dt
			vz[0]=Rebote[5]*dt


		y[0]=y[0]+int(vy[0]/dt)
		x[0]=x[0]+int(vx[0]/dt)
		z[0]=z[0]+int(vz[0]/dt)

		PTotal=M[0]/2*((vx[0]**2+vy[0]**2+vz[0]**2)**(1/2))

	else:
		if Enfijo==True:
			Xeje, Yeje, Zeje = x[0], y[0], z[0]

		for i in range(CantBolas):				#Ya sin 1 sola bola

			Fx=0
			Fy=0
			Fz=0
			if FIJO[i]==True:
				x[i]=PxFijo[i]	
				y[i]=PyFijo[i]
				z[i]=PzFijo[i]
			elif CantBolas>1:
				for n in range(CantBolas):
					if i==n:
						pass
					else:
						if kill[n]==True:		#Por esta condicion "kill[n]==True nadie siente a fuerza de bola"n"
							FxN=0
							FyN=0
							FzN=0
						else:
							Lectura=LecturaBolas(i, n)
							FxN=Lectura[0]
							FyN=Lectura[1]
							FzN=Lectura[2]


						Fx=Fx+FxN
						Fy=Fy+FyN
						Fz=Fz+FzN
		



			if CHOQUES==True:
				try:
					if YaChoco[i][0]==True:
						vx[i]=YaChoco[i][4]*YaChoco[i][1]
						vy[i]=YaChoco[i][4]*YaChoco[i][2]
						vz[i]=YaChoco[i][4]*YaChoco[i][3]
						YaChoco[i][0]=False
				except:
					pass
			vx[i]=(vx[i]*tau+Fx+ax)
			vy[i]=(vy[i]*tau+Fy+ay)
			vz[i]=(vz[i]*tau+Fz+az)


			if PAREDES==True:


				Rebote=ANGPAREDES(vx[i]/dt, x[i], vy[i]/dt, y[i], vz[i]/dt, z[i])
				x[i]=int(Rebote[0])
				y[i]=int(Rebote[1])
				z[i]=int(Rebote[2])
				vx[i]=int(Rebote[3]*dt)
				vy[i]=int(Rebote[4]*dt)
				vz[i]=int(Rebote[5]*dt)


			if FIJO[i]==True:
				y[i]=int(PyFijo[i])
				x[i]=int(PxFijo[i])
				z[i]=int(PzFijo[i])
			else:
				x[i]=x[i]+int(vx[i]/dt)
				y[i]=y[i]+int(vy[i]/dt)
				z[i]=z[i]+int(vz[i]/dt)


			poligonX[i]=int(Fx+x[i])
			poligonY[i]=int(Fy+y[i])
			poligonX0[i]=int(x[i])
			poligonY0[i]=int(y[i])


			PTotal=PTotal+M[i]*((((vx[i]/dt)**2)+((vy[i]/dt))**2+(vz[i]/dt)**2)**(1/2))/2



	#ACA EMPIEZA A ESCRIBIRSE LOS TEXTOS INDICADORES EN LA PANTALLA
	rango=slice(0,7)
	rango2=slice(0,4)
	txt=["Tiempo:",str(h),"Z:",str(z[0]),"X:", str(x[0]),"Y:", str(y[0]),"G:", str(G),"CantBolas:",str(CantBolas),"FzaControl:",str(FuerzaControl),"ay:",str(ay),"M0:",str(M[0]), "paredes:", str(PAREDES),"Xeje", str(Xeje)[rango], "Yeje", str(Yeje)[rango], "Zeje", str(Zeje)[rango], "AngX", str(angx)[rango2], "AngY", str(angy)[rango2], "AngZ", str(angz)[rango2], "Drz:", str(drz), "zoom:", str(zoom), "rADIO0:", str(rADIO0[0])[rango], "Trozo:", str(Trozo)]
	lentxt=[6, 6,2, 6,  2, 6, 2, 6, 2, 6     , 8, 4, 9, 6, 2, 4, 3, 6, 6, 4,4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 6, 5, 6, 5, 6, 5]
	cant1=len(txt)
	filas=PrintTxt(txt, lentxt, 30)
	if VISOR==True:
		#VISOR PRINCIPAL
		textoVy=LabelSys2.render("raiz(G*M/R): Vy",False, (225, 225, 225))
		textoVy2=LabelSys2.render(str(np.sqrt(G*M[0]/(250*dr))),False, (225, 225, 225))
		textoR=LabelSys2.render("R:",False, (225, 225, 225))
		textoR2=LabelSys2.render(str(250*dr),False, (225, 225, 225))
		#BARRA
		if BarraON==True:
			pygame.draw.line(ventana,(255,0,0), (int(Xeje),int(Yeje)),(int(Xeje+250),int(Yeje+0)),3)


		if freez==False:
			ventana.blit(textoVy,(int(ancho*3/4),int(alto*3/4-30)))
			ventana.blit(textoVy2,(int(ancho*3/4),int(alto*3/4)))
			ventana.blit(textoR,(int(ancho*3/4),int(alto*3/4+30)))
			ventana.blit(textoR2,(int(ancho*3/4+30),int(alto*3/4+30)))





	#ACA EMPIEZAN A DIBUJARSE LAS BOLAS EN ORDEN DE DISTANCIA, DE MAYOR A MENOR (SOLO LAS QUE ESTAN DELANTE NUESTRO)
	foundA=[]
	foundB=[]
	foundC=[]
	foundD=[]
	cantF=0
	#MODO PREsinTACION#
	#ventana.blit(imgPELON,(ancho/2-330, alto/2-70-120))
	#camara tiene propiedades Xeje, Yeje, Zeje, xang, yang, zang

	for k in range(0,len(x)):
		V=np.array([x[k]-Xeje, y[k]-Yeje,(z[k]-Zeje)])
		Vp=MEb(angx, angy, angz, V)
		if Vp[2]>=cerca0Cam and Vp[2]<=Lejos0Cam:
			radius=cerca0Cam/(Vp[2])
			if -ancho/2<=radius*Vp[0]<=ancho/2:
				if -alto/2<=radius*Vp[1]<=alto/2:
					ProyX=int(radius*Vp[0])
					ProyY=int(radius*Vp[1])
					cantF=cantF+1
					foundA.append(k)
					foundB.append(Vp[2])
					foundC.append(ProyX)
					foundD.append(ProyY)
	if cantF==0:
		pass
	else:
		d=list(zip(foundB,foundC, foundD, foundA))  #Z, X, Y
		d.sort(reverse=True)
		foundB, foundC, foundD, foundA=zip(*d)
	if CantBolas==1:
		rect[0].left = int(x[0]-(R)/2)*zoom
		rect[0].top = int(y[0]-(R)/2)*zoom
		ventana.blit(img[0],rect[0])
		#pygame.draw.line(ventana,(255,255,255),(poligonX0[0]*zoom, poligonY0[0]*zoom),(poligonX[0]*zoom,poligonY[0]*zoom),4)
		textoVy=LabelSys2.render("Presiona Barra Espaciadora para comenzar.",False, (225, 225, 225))
		ventana.blit(textoVy,(int(ancho*1/4),int(alto-50)))
	else:
		for i in foundA:
			V=np.array([x[i]-Xeje,y[i]-Yeje, (z[i]-Zeje)])
			Vp=MEb(angx, angy, angz, V)
			rect[i].left = int((cerca0Cam/(Vp[2]))*Vp[0]*zoom+ancho/2+rADIO0[i]) #dando offset del eje coord. al centro de la pantalla en h=0
			rect[i].top = int((cerca0Cam/(Vp[2]))*Vp[1]*zoom+alto/2+rADIO0[i])

			img[i]=pygame.image.load("spaceinvader.png")
			img[i]=pygame.transform.scale(img[i], (int(cerca0Cam*2*rADIO0[i]/Vp[2])*zoom, int(cerca0Cam*2*rADIO0[i]/Vp[2])*zoom)) 
			#img[i]=pygame.transform.laplacian(img[i])
			ventana.blit(img[i],rect[i])







	#AHORA DIBUJAREMOS Lineas y Poligonos:

	#Nota:
	# Actualmente veran que hay muchas lineas dedicadas a dibujar un cubo de lineas, unas figurillas de poligonos, 
	# pero en esencia en esta sección, debe haber un código que recorra objetos ".txt" o similares, (.obj podrían ser tambien)
	# de modo que podamos "importar" los objetos desde archivos externos entendiendo sus dinamicas.
	# almenos basicamente ya podremos hacerlo próximamente..



	#aca solo indico los vertices de unos Rectangulos para que haya algo. (cubo entre 0,0,0 y 100,100,10)

	ladoRectx=-rADIO0[0]*np.sin(h*np.pi/150)**2*np.cos(int(h/150)*np.pi)
	ladoRecty=-rADIO0[0]*np.sin(h*np.pi/150)**2
	ladoRectz=-rADIO0[0]*np.sin(h*np.pi/150)**2*np.cos(int(h/300)*np.pi)
	Rectangulos={}
	Rectangulos[0]=[(0,0,0),(0,ladoRecty,0),(ladoRectx,ladoRecty,0),(ladoRectx,0,0),(0,0,0)]
	Rectangulos[1]=[(0,0,0),(0,0,ladoRectz),(0,ladoRecty,ladoRectz),(0,ladoRecty,0),(0,0,0)]
	Rectangulos[2]=[(0,0,0),(0,0,ladoRectz),(ladoRectx,0,ladoRectz),(ladoRectx,0,0),(0,0,0)]
	Rectangulos[3]=[(ladoRectx,0,0),(ladoRectx,ladoRecty,0),(ladoRectx,ladoRecty,ladoRectz),(ladoRectx,0,ladoRectz),(ladoRectx,0,0)]
	Rectangulos[4]=[(0,ladoRecty,0),(ladoRectx,ladoRecty,0),(ladoRectx,ladoRecty,ladoRectz),(0,ladoRecty,ladoRectz),(0,ladoRecty,0)]
	Rectangulos[5]=[(0,0,ladoRectz),(ladoRectx,0,ladoRectz),(ladoRectx,ladoRecty,ladoRectz),(0,ladoRecty,ladoRectz),(0,0,ladoRectz)]
	Rectangulos[6]=[(0,0,ladoRectz),(ladoRectx,ladoRecty,0),]
	


	espiral=[]
	espiral2=[]
	espiral3=[]
	espiral4=[]
	espiral5=[]
	espiral6=[]
	espiral7=[]
	espiral8=[]
	CuadPj=rADIO0[0]
	
	Xfrut=(Xeje)
	Zfrut=(Zeje)
	Yfrut=(Yeje)
	for i in range(26):
		esp=np.array([Xfrut+(CuadPj)*np.sin(2*np.pi*i/25),0,Zfrut+(CuadPj)*np.cos(2*np.pi*i/25)])
		#XEJE=np.array([Xeje, Yeje, Zeje])
		#esp=esp+XEJE
		espiral.append(esp)
	Rectangulos[7]=espiral

	cantRect=len(Rectangulos) 
	#ACA DIBUJAMOS LAS LINEAS QUE HAYA (func. "ProyLinea")
	FL=[]
	RXY=[]
	#for i in range(cantRect):
	#	for n in range(len(Rectangulos[i])-1):
	#	# eje de coordenadas en 0,0,-200
	#		FL=[Rectangulos[i][n+1][0],Rectangulos[i][n+1][1],Rectangulos[i][n+1][2]]
	#		RXY=[Rectangulos[i][n][0],Rectangulos[i][n][1],Rectangulos[i][n][2]]
	#		COLr=[155*i/len(Rectangulos[i])+100, 255*n/len(Rectangulos[i]), 0]
	#		ResProyLinea=ProyLinea(FL,RXY,COLr, AnalisRay)


	fin={}
	largocasa=1000

	fin[0]=[[largocasa,largocasa,50], [largocasa+50,largocasa,50],[largocasa+50,largocasa+50,50],[largocasa+50,largocasa+50,50+50],[largocasa,largocasa+50,50+50],[largocasa,largocasa,50+50]]

	fin[1]=[[-10,0,0],[10,0,0],[10,0,largocasa],[-10,0,largocasa]]
	fin[2]=[[-largocasa,0,0],[-largocasa,100,0],[-largocasa,100,largocasa],[-largocasa,0,largocasa]]
	fin[3]=[[largocasa,0,0],[largocasa,100,0],[largocasa,100,largocasa],[largocasa,0,largocasa]]
	fin[4]=[[-largocasa,0,largocasa],[-largocasa,100,largocasa],[largocasa,100,largocasa],[largocasa,0,largocasa]]
	#fin[5]=[(Xeje+CuadPj, Yeje, Zeje),(Xeje+CuadPj, Yeje, Zeje+CuadPj),(Xeje-CuadPj, Yeje, Zeje+CuadPj),(Xeje-CuadPj, Yeje, Zeje-CuadPj),(Xeje+CuadPj, Yeje, Zeje-CuadPj)]



	Xfrut=0
	Zfrut=0
	Yfrut=0

	posy=paredy1
	espiral2.append([Xfrut, posy, Zfrut])
	espiral2.append([Xfrut, posy, Zfrut+CuadPj])
	espiral2.append([Xfrut-CuadPj, posy, Zfrut+CuadPj])
	espiral2.append([Xfrut-CuadPj, posy, Zfrut])
	espiral2.append([Xfrut, posy, Zfrut])
	espiral2.append([Xfrut, posy, Zfrut+CuadPj])
	espiral2.append([Xfrut+CuadPj, posy, Zfrut+CuadPj])
	espiral2.append([Xfrut+CuadPj, posy, Zfrut])
	espiral2.append([Xfrut, posy, Zfrut])
	espiral2.append([Xfrut, posy, Zfrut-CuadPj])
	espiral2.append([Xfrut-CuadPj, posy, Zfrut-CuadPj])
	espiral2.append([Xfrut-CuadPj, posy, Zfrut])
	espiral2.append([Xfrut, posy, Zfrut])
	espiral2.append([Xfrut, posy, Zfrut-CuadPj])
	espiral2.append([Xfrut+CuadPj, posy, Zfrut-CuadPj])
	espiral2.append([Xfrut+CuadPj, posy, Zfrut])
	fin[5]=espiral2
	
	
	


	posy=paredy2
	espiral3.append([Xfrut, posy, Zfrut])
	espiral3.append([Xfrut, posy, Zfrut+CuadPj])
	espiral3.append([Xfrut-CuadPj, posy, Zfrut+CuadPj])
	espiral3.append([Xfrut-CuadPj, posy, Zfrut])
	espiral3.append([Xfrut, posy, Zfrut])
	espiral3.append([Xfrut, posy, Zfrut+CuadPj])
	espiral3.append([Xfrut+CuadPj, posy, Zfrut+CuadPj])
	espiral3.append([Xfrut+CuadPj, posy, Zfrut])
	espiral3.append([Xfrut, posy, Zfrut])
	espiral3.append([Xfrut, posy, Zfrut-CuadPj])
	espiral3.append([Xfrut-CuadPj, posy, Zfrut-CuadPj])
	espiral3.append([Xfrut-CuadPj, posy, Zfrut])
	espiral3.append([Xfrut, posy, Zfrut])
	espiral3.append([Xfrut, posy, Zfrut-CuadPj])
	espiral3.append([Xfrut+CuadPj, posy, Zfrut-CuadPj])
	espiral3.append([Xfrut+CuadPj, posy, Zfrut])
	fin[6]=espiral3


	if PAREDES==True:

		posy=paredx1
		espiral4.append([posy, Yfrut, Zfrut])
		espiral4.append([posy, Yfrut, Zfrut+CuadPj])
		espiral4.append([posy, Yfrut-CuadPj, Zfrut+CuadPj])
		espiral4.append([posy, Yfrut-CuadPj, Zfrut])
		espiral4.append([posy, Yfrut, Zfrut])
		espiral4.append([posy, Yfrut, Zfrut+CuadPj])
		espiral4.append([posy, Yfrut+CuadPj, Zfrut+CuadPj])
		espiral4.append([posy, Yfrut+CuadPj, Zfrut])
		espiral4.append([posy, Yfrut, Zfrut])
		espiral4.append([posy, Yfrut, Zfrut-CuadPj])
		espiral4.append([posy, Yfrut-CuadPj, Zfrut-CuadPj])
		espiral4.append([posy, Yfrut-CuadPj, Zfrut])
		espiral4.append([posy, Yfrut, Zfrut])
		espiral4.append([posy, Yfrut, Zfrut-CuadPj])
		espiral4.append([posy, Yfrut+CuadPj, Zfrut-CuadPj])
		espiral4.append([posy, Yfrut+CuadPj, Zfrut])
		fin[7]=espiral4

		posy=paredx2
		espiral5.append([posy, Yfrut, Zfrut])
		espiral5.append([posy, Yfrut, Zfrut+CuadPj])
		espiral5.append([posy, Yfrut-CuadPj, Zfrut+CuadPj])
		espiral5.append([posy, Yfrut-CuadPj, Zfrut])
		espiral5.append([posy, Yfrut, Zfrut])
		espiral5.append([posy, Yfrut, Zfrut+CuadPj])
		espiral5.append([posy, Yfrut+CuadPj, Zfrut+CuadPj])
		espiral5.append([posy, Yfrut+CuadPj, Zfrut])
		espiral5.append([posy, Yfrut, Zfrut])
		espiral5.append([posy, Yfrut, Zfrut-CuadPj])
		espiral5.append([posy, Yfrut-CuadPj, Zfrut-CuadPj])
		espiral5.append([posy, Yfrut-CuadPj, Zfrut])
		espiral5.append([posy, Yfrut, Zfrut])
		espiral5.append([posy, Yfrut, Zfrut-CuadPj])
		espiral5.append([posy, Yfrut+CuadPj, Zfrut-CuadPj])
		espiral5.append([posy, Yfrut+CuadPj, Zfrut])
		fin[8]=espiral5

		posy=paredz1
		espiral6.append([Xfrut, Yfrut, posy])
		espiral6.append([Xfrut+CuadPj, Yfrut, posy])
		espiral6.append([Xfrut+CuadPj, Yfrut-CuadPj, posy])
		espiral6.append([Xfrut, Yfrut-CuadPj, posy])
		espiral6.append([Xfrut, Yfrut, posy])
		espiral6.append([Xfrut+CuadPj, Yfrut, posy])
		espiral6.append([Xfrut+CuadPj, Yfrut+CuadPj, posy])
		espiral6.append([Xfrut, Yfrut+CuadPj, posy])
		espiral6.append([Xfrut, Yfrut, posy])
		espiral6.append([Xfrut-CuadPj, Yfrut, posy])
		espiral6.append([Xfrut-CuadPj, Yfrut-CuadPj, posy])
		espiral6.append([Xfrut, Yfrut-CuadPj, posy])
		espiral6.append([Xfrut, Yfrut, posy])
		espiral6.append([Xfrut-CuadPj, Yfrut, posy])
		espiral6.append([Xfrut-CuadPj, Yfrut+CuadPj, posy])
		espiral6.append([Xfrut, Yfrut+CuadPj, posy])
		fin[9]=espiral6

		posy=paredz2
		espiral7.append([Xfrut, Yfrut, posy])
		espiral7.append([Xfrut+CuadPj, Yfrut, posy])
		espiral7.append([Xfrut+CuadPj, Yfrut-CuadPj, posy])
		espiral7.append([Xfrut, Yfrut-CuadPj, posy])
		espiral7.append([Xfrut, Yfrut, posy])
		espiral7.append([Xfrut+CuadPj, Yfrut, posy])
		espiral7.append([Xfrut+CuadPj, Yfrut+CuadPj, posy])
		espiral7.append([Xfrut, Yfrut+CuadPj, posy])
		espiral7.append([Xfrut, Yfrut, posy])
		espiral7.append([Xfrut-CuadPj, Yfrut, posy])
		espiral7.append([Xfrut-CuadPj, Yfrut-CuadPj, posy])
		espiral7.append([Xfrut, Yfrut-CuadPj, posy])
		espiral7.append([Xfrut, Yfrut, posy])
		espiral7.append([Xfrut-CuadPj, Yfrut, posy])
		espiral7.append([Xfrut-CuadPj, Yfrut+CuadPj, posy])
		espiral7.append([Xfrut, Yfrut+CuadPj, posy])
		fin[10]=espiral7



	#ACA DIBUJAMOS LOS POLIGONOS QUE HAYA (func. "ProyPoly")
	for i in range(len(fin)):
		poli=fin[i]
		ProyPoli(poli, (50*(1+i/len(fin))*np.cos(angx)**2,(255-50*(1+i/len(fin)))*np.sin(angy)**2,0))




	#Acá ya en instancia de Actualizar la pantalla, demorar la siguiente entrega, y borrar.
	#UNA VEZ SETEADA NUESTRA PANTALLA LA MOSTRAMOS, BRINDAMOS LA DATA A LA CONSOLA, Y DEMORAMOS LA SIGUIENTE INTERACION.
	pygame.display.flip()
	pygame.time.wait(DELAY)


	if ESCRITURA==True:
		file.write(str(h) + "	"+ str(x[0]) + "	"+str(y[0]) + "	" +str(z[0]) + os.linesep)
		#Luego de dibujar borramos la pantalla en los sectores elegidos
 

 	#ACA BORRAMOS LA PANTALLA O NO, SIN DEJAR DE BORRAR LOS INDICADORES.
	color=[15+15*np.sin(angx),15+15*np.sin(angx),50+50*np.sin(angx)]
	poly = [(0,0), (ancho,0), (ancho, int((filas+1)*30)), (0, int((filas+1)*30)),(0,0) ]
	pygame.draw.polygon(ventana, color, poly, 0)
	poly2 = [(0,int((filas+1)*30)), (0,alto) , (ancho, alto), (ancho,int((filas+1)*30)),(0,int((filas+1)*30))]
	if freez==False:
		pygame.draw.polygon(ventana, color, poly2, 0)

	#ACA EMPIEZA LA PROGRAMACION DEL MANDO:

	#1ERO LOS CHECK DE USO Y SUS CONTADORES SE BAJAN UNA VUELTA SI ES EL CASO.
	if Slow==True:
		FuerzaControl=1


	if usoKEY8==True:
		angx=angx+movang

	if usoKEY2==True:
		angx=angx-movang


	if usoKEY6==True:
		angy=angy+movang

	if usoKEY4==True:
		angy=angy-movang



	if usoKEYUP==True:
		movz=np.array([0, -movtras*FuerzaControl,0])
		movz=MbE(angx, angy, angz, movz)
		x[0]=x[0]+movz[0]
		y[0]=y[0]+movz[1]
		z[0]=z[0]+movz[2]*drz


	if usoKEYRIGHT==True:
		movz=np.array([movtras*FuerzaControl,0, 0])
		movz=MbE(angx, angy, angz, movz)
		x[0]=x[0]+movz[0]
		y[0]=y[0]+movz[1]
		z[0]=z[0]+movz[2]*drz


	if usoKEYLEFT==True:
		movz=np.array([movtras*FuerzaControl,0, 0])
		movz=MbE(angx, angy, angz, movz)
		x[0]=x[0]-movz[0]
		y[0]=y[0]-movz[1]
		z[0]=z[0]-movz[2]*drz


	if usoKEYDOWN==True:
		movz=np.array([0,-movtras*FuerzaControl, 0])
		movz=MbE(angx, angy, angz, movz)
		x[0]=x[0]-movz[0]
		y[0]=y[0]-movz[1]
		z[0]=z[0]-movz[2]*drz


	if usoMOVTRASFron==True:
		movz=np.array([0,0, movtras*FuerzaControl])
		movz=MbE(angx, angy, angz, movz)
		if Enfijo==False:
			Xeje=Xeje-movz[0]
			Yeje=Yeje-movz[1]
			Zeje=Zeje-movz[2]*drz
		else:
			vx[0]=vx[0]-movz[0]
			vy[0]=vy[0]-movz[1]
			vz[0]=vz[0]-movz[2]*drz


	if usoMOVTRASBack==True:
		movz=np.array([0,0, movtras*FuerzaControl])
		movz=MbE(angx, angy, angz, movz)
		if Enfijo==False:
			Xeje=Xeje+movz[0]
			Yeje=Yeje+movz[1]
			Zeje=Zeje+movz[2]*drz
		else:
			vx[0]=vx[0]+movz[0]
			vy[0]=vy[0]+movz[1]
			vz[0]=vz[0]+movz[2]*drz

	if usoMOVTRASLeft==True:
		movz=np.array([movtras*FuerzaControl,0,0])
		movz=MbE(angx, angy, angz, movz)
		if Enfijo==False:
			Xeje=Xeje-movz[0]
			Yeje=Yeje-movz[1]
			Zeje=Zeje-movz[2]*drz
		else:
			vx[0]=vx[0]-movz[0]
			vy[0]=vy[0]-movz[1]
			vz[0]=vz[0]-movz[2]*drz

	if usoMOVTRASRight==True:
		movz=np.array([movtras*FuerzaControl,0,0])
		movz=MbE(angx, angy, angz, movz)
		if Enfijo==False:
			Xeje=Xeje+movz[0]
			Yeje=Yeje+movz[1]
			Zeje=Zeje+movz[2]*drz
		else:
			vx[0]=vx[0]+movz[0]
			vy[0]=vy[0]+movz[1]
			vz[0]=vz[0]+movz[2]*drz

	if usoMOVTRASUp==True:
		movz=np.array([0,movtras*FuerzaControl,0])
		movz=MbE(angx, angy, angz, movz)
		if Enfijo==False:
			Xeje=Xeje-movz[0]
			Yeje=Yeje-movz[1]
			Zeje=Zeje-movz[2]*drz
		else:
			vx[0]=vx[0]-movz[0]
			vy[0]=vy[0]-movz[1]
			vz[0]=vz[0]-movz[2]*drz

	if usoMOVTRASDown==True:
		movz=np.array([0,movtras*FuerzaControl,0])
		movz=MbE(angx, angy, angz, movz)
		if Enfijo==False:
			Xeje=Xeje+movz[0]
			Yeje=Yeje+movz[1]
			Zeje=Zeje+movz[2]*drz
		else:
			vx[0]=vx[0]+movz[0]
			vy[0]=vy[0]+movz[1]
			vz[0]=vz[0]+movz[2]*drz


	if usoKEYDRCOM1==True:
		vx[0]=0
		vy[0]=0
		vz[0]=0

	if	usoKEYDRCOM2==True:
		M[0]=M[0]+100

	if DRAGMOUSE==True:
		DANG=[(MOUSED1[0]-ancho/2),(-MOUSED1[1]+alto/2)]
		angy1=np.arctan(DANG[0]/cerca0Cam)/Setcontroldrag
		angx1=np.arctan(DANG[1]/cerca0Cam)/Setcontroldrag
		if DANG[1]!=0:
			angx=angx+angx1*norm([DANG[1]])/(ancho/2)*100

			#control de angx entre [-pi/2 ; pi/2]
			if angx<np.pi/2:
				if angx>-np.pi/2:
					pass
				else:
					angx=-np.pi/2
			else:
				angx=np.pi/2

		if DANG[0]!=0:
			angy=angy+angy1*norm([DANG[0]/(alto/2)*100])


	for event in pygame.event.get():
		print(event)
		if event.type == pygame.QUIT:
		    pygame.quit()
		    exit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			pass
			#if event.button==1:
			#	DRAGMOUSE=True
			#	mxy=event.pos
			#	MOUSED0=mxy
			#	print(MOUSED0)
		elif event.type == pygame.MOUSEMOTION:
			MOUSED1=event.pos
			pygame.mouse.set_pos([ancho/2,alto/2])

		elif event.type == pygame.MOUSEBUTTONUP:
			pass
			#if event.button==1:
			#	DRAGMOUSE=False


		elif event.type == pygame.KEYUP:

			if event.key==K_UP:
				usoKEYUP=False
			elif event.key==K_RIGHT:
				usoKEYRIGHT=False

			elif event.key == K_LEFT:
				usoKEYLEFT=False

			elif event.key == K_DOWN:
				usoKEYDOWN=False


			elif event.key==1073741916: # 4  (punto)
				usoKEY4=False

			elif event.key==1073741920: # 8  (punto)
				usoKEY8=False

			elif event.key==1073741918: # 6  (punto)
				usoKEY6=False

			elif event.key==1073741914: # 2  (punto)
				usoKEY2=False



			elif event.key==115: # s
				usoMOVTRASFron=False

			elif event.key==119: # w
				usoMOVTRASBack=False


			elif event.key==97: # a
				usoMOVTRASLeft=False

			elif event.key==100: # d
				usoMOVTRASRight=False

			elif event.key==101: # E
				usoMOVTRASUp=False

			elif event.key==113:  #Q  
				usoMOVTRASDown=False



			elif event.key==49: # 1  
				usoKEYDRCOM1=False

			elif event.key==50: # 2  
				usoKEYDRCOM2=False



			elif event.key==1073742049:  #Shift I
				Slow=False
				FuerzaControl=FuerzaControlvieja


		elif event.type == pygame.KEYDOWN:

			if event.key==K_UP:
				usoKEYUP=True

			elif event.key==K_RIGHT:
				usoKEYRIGHT=True

			elif event.key == K_LEFT:
				usoKEYLEFT=True

			elif event.key == K_DOWN:
				usoKEYDOWN=True


			elif event.key==117: #U
				#print("U")
				if G>=3000:
					G=G+1000
				elif G>=300:
					G=G+100
				elif G>=10:
					G=G+10
				else:
					G=G+1


			elif event.key==121: #Y
				#print("Y")
				if G>3000:
					G=G-1000
				elif G>300:
					G=G-100
				elif G>10:
					G=G-10
				else:
					G=G-1


			elif event.key==106: #J
				#print("J")
				if Slow==True:
					pass
				else:
					FuerzaControl=FuerzaControl+1
					FuerzaControlvieja=FuerzaControl
				movang=2*FuerzaControl/10*np.pi/(100*zoom)

				
			elif event.key==104: #H
				#print("H")
				if Slow==True:
					pass
				else:
					FuerzaControl=FuerzaControl-1
					FuerzaControlvieja=FuerzaControl
				movang=2*FuerzaControl/10*np.pi/(100*zoom)


			elif event.key==110: #N
				#print("N")
				M[0]=M[0]-100	

				
			elif event.key==109: #M
				#print("M")
				M[0]=M[0]+100


			elif event.key==44: #,  (coma)
				#print("ay")
				if ay==100:
					ay=ay-10
				else:
					ay=ay-10


			elif event.key==48: # 0  (teclado letras)
				#print("0")

				if CantBolas>=3:
					CantBolas=CantBolas-1
					x.pop
					y.pop
					z.pop
					vx.pop
					vy.pop
					vz.pop
					M.pop
					m.pop
					FIJO.pop
					PxFijo.pop
					PyFijo.pop
					PzFijo.pop
					poligonX.pop
					poligonX0.pop
					poligonY.pop
					poligonY0.pop
					rADIO0.pop
					img.pop
					rect.pop

			elif event.key==46: # .  (punto)
				#print(".")
				if ay==0:
					ay=ay+10
				else:
					ay=ay+10

			elif event.key==47: # - (guion medio)  desactiva barra roja de radio
				#print("-")
				if BarraON==True:
					BarraON=False
				else:
					BarraON=True


			elif event.key==55: #7 
				#print("7")
				if select==100:
					pass
				else:
					if select==CantBolas-1:
						pass
					else:
						select=select+1
						kill[select]=True


			elif event.key==54: # 6 
				#print("6")
				if select==1:
					pass
				else:
					select=select-1


			elif event.unicode=='4':  #4 

				if Enfijo==False:
					Enfijo=True
				else:
					Enfijo=False


			elif event.key==115: # s
				usoMOVTRASFron=True

			elif event.key==119: # w
				usoMOVTRASBack=True


			elif event.key==97: # a
				usoMOVTRASLeft=True

			elif event.key==100: # d
				usoMOVTRASRight=True

			elif event.key==101: # E
				usoMOVTRASUp=True

			elif event.key==113:  #Q  
				usoMOVTRASDown=True

			elif event.unicode=='|': # |
				if PAREDES==True:
					PAREDES=False

				else:
					PAREDES=True
				#PAREDES=CParedes(PAREDES)


			elif event.unicode=='3':  #3

				if freez2==True:
					freez2=False
				else:
					freez2=True

			elif event.unicode==' ':  #Barra espaciadora

				if CantBolas==1:
					Enfijo=True
					tau=1
					FuerzaControl=30
					x[0]=0
					y[0]=0
					z[0]=0
					Xeje=0
					Yeje=0
					Zeje=0

				CantBolas=CantBolas+1
				rand=np.cos(angx*angy*angz+h*Zeje*Xeje+Yeje+PTotal)**2 
				Vect1=np.array([0, -500-200*rand, 500*rand+500+rADIO0[0]])
				XEJE=np.array([Xeje, Yeje, Zeje])
				Vect1=Vect1+XEJE
				pipi1=norm(Vect1)
				x.append(Vect1[0])
				y.append(Vect1[1])
				z.append(Vect1[2])
				vx.append(-(rand*dt*G*M[0]/(((pipi1)**2)**(0.5)))**(1/2))
				vy.append(-((1-rand)*dt*G*M[0]/(((pipi1)**2)**(0.5)))**(1/2))
				vz.append(0)
				M.append(1)
				m.append(1)
				poligonX.append(0)
				poligonX0.append(0)
				poligonY.append(0)
				poligonY0.append(0)
					


				if CLAVADO==False:
					FIJO.append(False)
					kill.append(False)
				else:
					FIJO.append(True)
					kill.append(True)
				if CantBolas<20:
					PxFijo.append(CantBolas*(ancho/20)-ancho/2)
					PyFijo.append(-alto/2)
				elif CantBolas<40:
					PxFijo.append((CantBolas-20)*(ancho/20)-ancho/2)
					PyFijo.append(+alto/2)
				elif CantBolas<60:
					PxFijo.append(-ancho/2)
					PyFijo.append((CantBolas-40)*(alto/20)-alto/2)
				elif CantBolas<80:
					PxFijo.append(ancho/2)
					PyFijo.append((CantBolas-60)*(alto/20)-alto/2)
				PzFijo.append(0)
				rADIO0.append(5)
				img.append(pygame.image.load("spaceinvader.png"))
				rect.append(img[CantBolas-1].get_rect())



			elif event.key==256:  #0 TEC NUM

				if CantBolas>=3:
					CantBolas=CantBolas-1
					x.pop
					y.pop
					z.pop
					vx.pop
					vy.pop
					vz.pop
					M.pop
					m.pop
					poligonX.pop
					poligonX0.pop
					poligonY.pop
					poligonY0.pop
					img.pop
					rect.pop
					FIJO.pop
					PxFijo.pop
					PyFijo.pop
					PzFijo.pop
					rADIO0.pop


			elif event.key==114:  #R 

				if CantBolas>=2:
					DEST=CantBolas-1
					for i in range(DEST):
						i=i+1
						x.pop
						y.pop
						z.pop
						vx.pop
						vy.pop
						vz.pop
						M.pop
						m.pop
						poligonX.pop
						poligonX0.pop
						poligonY.pop
						poligonY0.pop
						img.pop
						rect.pop
						FIJO.pop
						PxFijo.pop
						PyFijo.pop
						PzFijo.pop
						rADIO0.pop
					CantBolas=1
					x[0]=0+Xeje
					y[0]=0+Yeje
					z[0]=0
					vx[0]=0
					vy[0]=0
					vz[0]=0



			elif event.key==261:  #5 TEC NUM

				if CamFija==False:
					CamFija=True
				else:
					CamFija=False



			elif event.key==102:  #f

				if FIJO[select-1]==False:
					FIJO[select-1]=True
				else:
					FIJO[select-1]=False
					vx[select-1]=0
					vy[select-1]=0
					vz[select-1]=0


			elif event.key==118:  #v
				if CLAVADO==True:
					CLAVADO=False
				else:
					CLAVADO=True

			elif event.key==1073742053:  #Shift D
				if freez2==True:
					freez2=False
				else:
					freez2=True


			elif event.key==1073742049:  #Shift Izq
				Slow=True

			elif event.unicode=='+':  #+ TEC NUM
				if freez2==False:
					if zoom>=3000:
						zoom=zoom+1000
					elif zoom>=1000:
						zoom=zoom+100
					elif zoom>=50:
						zoom=zoom+10
					else:
						zoom=zoom+1
					rADIO0[0]=np.sqrt(cerca0Cam**2+(ancho/(2*zoom))**2)
				else:
					if Trozo>=3000:
						Trozo=Trozo+1000
					elif Trozo>=300:
						Trozo=Trozo+100
					elif Trozo>=50:
						Trozo=Trozo+10
					else:
						Trozo=Trozo+1



			elif event.unicode=='-':  #- TEC NUM
				if freez2==False:
					if zoom>3000:
						zoom=zoom-1000
					elif zoom>1000:
						zoom=zoom-100
					elif zoom>50:
						zoom=zoom-10
					else:
						zoom=zoom-1

					rADIO0[0]=np.sqrt(cerca0Cam**2+(ancho/(2*zoom))**2)
				else:
					if Trozo>3000:
						Trozo=Trozo-1000
					elif Trozo>300:
						Trozo=Trozo-100
					elif Trozo>50:
						Trozo=Trozo-10
					else:
						Trozo=Trozo-1





			elif event.key==1073741916: # 4  (punto)

				usoKEY4=True

			elif event.key==1073741920: # 8  (punto)
				usoKEY8=True

			elif event.key==1073741918: # 6  (punto)
				usoKEY6=True

			elif event.key==1073741914: # 2  (punto)
				
				usoKEY2=True


			elif event.key==49: # 1
				usoKEYDRCOM1=True

			elif event.key==50: # 2
				usoKEYDRCOM2=True
				

			elif event.key==93:  #+ notebook
				angy=angy-movang

			elif event.key==92:  #- notebook
				angy=angy+movang

#SI SE CIERRA EL BUCLE (BREAK) SE LLAMA AL CIERRE.
pygame.quit()   