import numpy as np
import pygame,sys
from pygame.locals import *
import random
import os


R=30
alto = 500
ancho = 1000
profundo=700
cerca=-700
h=0


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
drdist=2
cerca1Cam=cerca0Cam*drdist
Lejos0Cam=10000
Xeje=0
Yeje=0
Zeje=-cerca1Cam
angx=0.
angy=0.
angz=0.

piso=int(alto-R/2+Yeje)
techo=int(0+R/2+Yeje)
pared0=int(0+R/2-Xeje)
pared1=int(ancho-R/2-Xeje)
paredZCerca=int(profundo-R/2-Zeje)
paredZLejos=int(cerca+R/2-Zeje)


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



FuerzaControl=10
tita=0.	
phi=0.				
XVER=-1
YVER=-1			
Cuadrante=4
PAREDES=False
CHOQUES=True


CantBolas=1
X=0
Y=0
Z=0
rADIO0=[15]
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
ESCRITURA=False
VISOR=False
#_____________________
movang=2*np.pi/100
movtras=1
movtrasz=1
FuerzaControlvieja=FuerzaControl
rgcab=0
#____________________

pygame.init()
ventana = pygame.display.set_mode((ancho, alto))
screen = pygame.display.set_caption("Spaceinvader")

img=[pygame.image.load("spaceinvader.png")]
rect=[img[0].get_rect()]

#MODO PREsinTACION
#imgPELON=pygame.image.load("pelonazo.png")
#rectPELON=imgPELON.get_rect()

LabelSys1=pygame.font.SysFont("Calibri", 20)
LabelSys2=pygame.font.SysFont("Calibri", 30)
fnt=20
fnt2=50


def norm(a):
	pipi=a
	return((((pipi)**2)**(0.5)))

def MROTx(a):
	return(np.array([[1, 0,0],[0,np.cos(a),np.sin(a)],[0, -np.sin(a),np.cos(a)]]))

def MROTy(a):
	return(np.array([[np.cos(a),0, -np.sin(a)],[0,1, 0],[np.sin(a),0,np.cos(a)]]))

def MROTz(a):
	return(np.array([[np.cos(a),np.sin(a),0],[ -np.sin(a),np.cos(a),0],[ 0,0,1]]))

def MDRZ():
	return(np.array([[1,0,0],[0,1,0],[ 0,0,1/drz]]))

def MEb(angZ0, angY0, angX0, v):
	ver1=np.dot(MROTz(angZ0),v)
	ver2=np.dot(MROTy(angY0),ver1)
	ver3=np.dot(MROTx(angX0),ver2)
	ver4=np.dot(MDRZ(),ver3)
	return(ver4)

def MbE(angZ0, angY0, angX0, v):
	ver1=np.dot(MROTx(-angX0),v) 
	ver2=np.dot(MROTy(-angY0),ver1)
	ver3=np.dot(MROTz(-angZ0),ver2)
	ver4=np.dot(MDRZ(),ver3)
	return(ver4)

def ProyLinea(fin=list,ini=list, color=list):
	FL1=np.array([fin[0],fin[1],fin[2]])
	RXYZ=np.array([ini[0],ini[1],ini[2]])
	Vp=FL1-RXYZ
	XEJE=np.array([Xeje, Yeje, Zeje])
	offset=np.array([ancho/2, alto/2, 0])
	V=RXYZ-XEJE
	Vp0=MEb(angz, angy, angx, V)
	Vp=MEb(angz, angy, angx, Vp)
	Vp=Vp+Vp0
	if Vp0[2]>=cerca0Cam:
		pr0X1 = int((cerca0Cam/(Vp0[2]))*Vp0[0]+offset[0])
		pr0Y1 = int((cerca0Cam/(Vp0[2]))*Vp0[1]+offset[1])


	if Vp[2]>=cerca0Cam and Vp[2]<Lejos0Cam:
		pr1X1 = int((cerca0Cam/(Vp[2]))*Vp[0]+offset[0])
		pr1Y1 = int((cerca0Cam/(Vp[2]))*Vp[1]+offset[1])

		try:
			pygame.draw.line(ventana, (color[0],color[1],color[2]), (pr0X1, pr0Y1), (pr1X1,pr1Y1), 3)
		except:
			pass
	elif Vp[2]<cerca0Cam:
		a1=(-Vp0[2]/(Vp[2]-Vp0[2]))
		try:
			pr1X1 = int((Vp[0]-Vp[0])*a1+Vp[0]+offset[0])
			pr1Y1 = int((Vp[1]-Vp[1])*a1+Vp[1]+offset[1])
		except:
			pr1X1 = int(Vp[0]+offset[0])
			pr1Y1 = int(Vp[1]+offset[1])


def ProyPoli(fin=list,color=list):
	prX=[]
	prY=[]
	prXY=[]
	for i in range(len(fin)-1):
		FL1=np.array([fin[i][0],-fin[i][1],fin[i][2]])
		FL2=np.array([fin[i+1][0],-fin[i+1][1],fin[i+1][2]])
		XEJE=np.array([Xeje, Yeje, Zeje])
		offset=np.array([ancho/2, alto/2, 0])
		V=FL1-XEJE
		V2=FL2-XEJE
		Vp0=MEb(angz, angy, angx, V)
		Vp02=MEb(angz, angy, angx, V2)
		if Vp0[2]>=cerca0Cam:
			prX=(int((cerca0Cam/(Vp0[2]))*Vp0[0]+offset[0]))
			prY=(int((cerca0Cam/(Vp0[2]))*Vp0[1]+offset[1]))
			prXY.append((prX, prY))
		#else:
		#	param=(cerca0Cam-Vp0[2])/(Vp02[2]-Vp0[2]+0.1)
		#	prX=int(param*Vp0[0]+offset[0])
		#	prY=int(param*Vp0[1]+offset[1])
		#	prXY.append((prX, prY))


	try:
		pygame.draw.polygon(ventana, (color[0],color[1],color[2]),prXY , 0)
	except:
		pass



def ANGPAREDES(vx, x0, vy, y0, vz, z0):
	if PAREDES==True:

		x=int(x0)+int(vx)
		y=int(y0)+int(vy)
		choquepared0=False
		choquepared1=False
		choquetecho=False
		choquepiso=False

		if vx<=0:
			if x<=pared0<x0:
				choquepared0=True
			if x<=pared1<x0:
				choquepared1=True

		else:
			if x>=pared0>x0:
				choquepared0=True
			if x>=pared1>x0:
				choquepared1=True


		if vy<=0:
			if y<=piso<y0:
				choquepiso=True
			if y<=techo<y0:
				choquetecho=True

		else:
			if y>=piso>y0:
				choquepiso=True
			if y>=techo>y0:
				choquetecho=True

		if choquepared0==True:
			x0=int(pared0)
			alpha=0
			vy=(vy*(2*((np.cos(alpha))**2)-1)-vx*np.sin(2*alpha))*taupiso
			vx=(vx*(2*((np.sin(alpha))**2)-1)-vy*np.sin(2*alpha))*taupiso
			choquepared0=False



		if choquepared1==True:
			x0=int(pared1)
			alpha=-np.pi
			vy=(vy*(2*((np.cos(alpha))**2)-1)-vx*np.sin(2*alpha))*taupiso
			vx=(vx*(2*((np.sin(alpha))**2)-1)-vy*np.sin(2*alpha))*taupiso
			choquepared1=False


		if choquetecho==True:
			y0=int(techo)
			alpha=-np.pi/2
			vy=(vy*(2*((np.cos(alpha))**2)-1)-vx*np.sin(2*alpha))*taupiso
			vx=(vx*(2*((np.sin(alpha))**2)-1)-vy*np.sin(2*alpha))*taupiso
			choquetecho=False

		if choquepiso==True:
			y0=int(piso)
			alpha=np.pi/2
			vy=(vy*(2*((np.cos(alpha))**2)-1)-vx*np.sin(2*alpha))*taupiso
			vx=(vx*(2*((np.sin(alpha))**2)-1)-vy*np.sin(2*alpha))*taupiso
			choquepiso=False


		return([x0, y0, z0, vx, vy, vz])


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
					print("aca0, yachoco activado, no se chocara denuevo")
					Choq=True
					r=rADIO0[i]+rADIO0[n]
			except:
				print("aca0, yachoco descativado, se chocará")
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
file = open("prueba1.txt", "w")
file.write("Hello people this is the start of the first try in the story of the writes in python in the course of learning"+os.linesep)
file.write(""+os.linesep+os.linesep+os.linesep)


jugando = True
# Empieza el Juego...
while jugando:

	PTotal=0

	cerca1Cam=cerca0Cam*drdist
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


	rango=slice(0,7)
	rango2=slice(0,4)

	txt=["Tiempo:",str(h),"Z:",str(z[0]),"X:", str(x[0]),"Y:", str(y[0]),"Radio:",str(r)[rango],"Tita:",str(tita)[rango],"G:", str(G),"CantBolas:",str(CantBolas),"FzaControl:",str(FuerzaControl),"ay:",str(ay),"tau:",str(tau),"M0:",str(M[0]),"dr:",str(dr),"select:",str(select), "paredes:", str(PAREDES),"PTotal:", str(PTotal)[rango2], "Xeje", str(Xeje)[rango2], "Yeje", str(Yeje)[rango2], "Zeje", str(Zeje)[rango2], "AngX", str(angx)[rango2], "AngY", str(angy)[rango2], "AngZ", str(angz)[rango2], "Drz:", str(drz)]
	lentxt=[6, 6,2, 6,  2, 6, 2, 6, 5, 11, 4, 11, 2, 6, 8, 4, 9, 6, 2, 4, 3, 6, 3, 6, 2, 4, 5, 3, 6, 4,6,6, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5]
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
		Vp=MEb(angz, angy, angx, V)
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
		rect[0].left = int(x[0]-(R)/2)
		rect[0].top = int(y[0]-(R)/2)
		ventana.blit(img[0],rect[0])
		pygame.draw.line(ventana,(255,255,255),(poligonX0[0], poligonY0[0]),(poligonX[0],poligonY[0]),4)
		textoVy=LabelSys2.render("Presiona Barra Espaciadora para comenzar.",False, (225, 225, 225))
		ventana.blit(textoVy,(int(ancho*1/4),int(alto-50)))
	else:
		for i in foundA:
			V=np.array([x[i]-Xeje,y[i]-Yeje, (z[i]-Zeje)])
			Vp=MEb(angz, angy, angx, V)
			rect[i].left = int((cerca0Cam/(Vp[2]))*Vp[0]+ancho/2+rADIO0[i]) #dando offset del eje coord. al centro de la pantalla en h=0
			rect[i].top = int((cerca0Cam/(Vp[2]))*Vp[1]+alto/2+rADIO0[i])

			img[i]=pygame.image.load("spaceinvader.png")
			img[i]=pygame.transform.scale(img[i], (int(cerca1Cam*2*rADIO0[i]/Vp[2]), int(cerca1Cam*2*rADIO0[i]/Vp[2]))) 
			ventana.blit(img[i],rect[i])

	#aca solo indico los vertices de unos Rectangulos para que haya algo. (cubo entre 0,0,0 y 100,100,10)
	Rectangulos={}
	Rectangulos[0]=[(0,0,0),(0,100,0),(100,100,0),(100,0,0),(0,0,0)]
	Rectangulos[1]=[(0,0,0),(0,0,100),(0,100,100),(0,100,0),(0,0,0)]
	Rectangulos[2]=[(0,0,0),(0,0,100),(100,0,100),(100,0,0),(0,0,0)]
	Rectangulos[3]=[(100,0,0),(100,100,0),(100,100,100),(100,0,100),(100,0,0)]
	Rectangulos[4]=[(0,100,0),(100,100,0),(100,100,100),(0,100,100),(0,100,0)]
	Rectangulos[5]=[(0,0,100),(100,0,100),(100,100,100),(0,100,100),(0,0,100)]
	Rectangulos[6]=[(0,0,100),(100,100,0),]
	espiral=[]
	for i in range(10):
		espiral.append((100*np.sin(2*np.pi*i/10),300+i*10,100*np.cos(2*np.pi*i/10)))
	Rectangulos[7]=espiral

	cantRect=len(Rectangulos) 


	FL=[]
	RXY=[]
	for i in range(cantRect):
		for n in range(len(Rectangulos[i])-1):
		# eje de coordenadas en 0,0,-200
			FL=[Rectangulos[i][n+1][0],Rectangulos[i][n+1][1],Rectangulos[i][n+1][2]]
			RXY=[Rectangulos[i][n][0],Rectangulos[i][n][1],Rectangulos[i][n][2]]
			COLr=[155*i/len(Rectangulos[i])+100, 255*n/len(Rectangulos[i]), 0]
			ResProyLinea=ProyLinea(FL,RXY,COLr)


	fin={}
	fin[0]=[[300,300,50], [300+50,300,50],[300+50,300+50,50],[300+50,300+50,50+50],[300,300+50,50+50],[300,300,50+50],[300,300,50]]
	fin[1]=[[-100,0,0],[100,0,0],[100,0,5000],[-100,0,5000],[-100,0,0]]
	fin[2]=[[-500,0,0],[-500,1000,0],[-500,1000,5000],[-500,0,5000],[-500,0,0]]
	fin[3]=[[500,0,0],[500,1000,0],[500,1000,5000],[500,0,5000],[500,0,0]]
	fin[4]=[[-500,0,5000],[-500,1000,5000],[500,1000,5000],[500,0,5000],[-500,0,5000]]

	for i in range(5):
		poli=fin[i]
		ProyPoli(poli, (255,255,0))


	#UNA VEZ SETEADA NUESTRA PANTALLA LA MOSTRAMOS, BRINDAMOS LA DATA A LA CONSOLA, Y DEMORAMOS LA SIGUIENTE INTERACION.
	pygame.display.flip()
	pygame.time.wait(DELAY)

	if ESCRITURA==True:
		file.write(str(PTotal) + " -             "+ str(CantBolas) + os.linesep)
		#Luego de dibujar borramos la pantalla en los sectores elegidos
 
	poly = [(0,0), (ancho,0), (ancho, int((filas+1)*30)), (0, int((filas+1)*30)),(0,0) ]
	pygame.draw.polygon(ventana, (0, 0, 0), poly, 0)


	poly2 = [(0,int((filas+1)*30)), (0,alto) , (ancho, alto), (ancho,int((filas+1)*30)),(0,int((filas+1)*30))]

	if freez==False:

		pygame.draw.polygon(ventana, (0, 0, 0), poly2, 0)

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
		movz=MbE(angz, angy, angx, movz)
		x[0]=x[0]+movz[0]
		y[0]=y[0]+movz[1]
		z[0]=z[0]+movz[2]*drz


	if usoKEYRIGHT==True:
		movz=np.array([movtras*FuerzaControl,0, 0])
		movz=MbE(angz, angy, angx, movz)
		x[0]=x[0]+movz[0]
		y[0]=y[0]+movz[1]
		z[0]=z[0]+movz[2]*drz


	if usoKEYLEFT==True:
		movz=np.array([movtras*FuerzaControl,0, 0])
		movz=MbE(angz, angy, angx, movz)
		x[0]=x[0]-movz[0]
		y[0]=y[0]-movz[1]
		z[0]=z[0]-movz[2]*drz


	if usoKEYDOWN==True:
		movz=np.array([0,-movtras*FuerzaControl, 0])
		movz=MbE(angz, angy, angx, movz)
		x[0]=x[0]-movz[0]
		y[0]=y[0]-movz[1]
		z[0]=z[0]-movz[2]*drz


	if usoMOVTRASFron==True:
		movz=np.array([0,0, movtras*FuerzaControl])
		movz=MbE(angz, angy, angx, movz)
		Xeje=Xeje-movz[0]
		Yeje=Yeje-movz[1]
		Zeje=Zeje-movz[2]*drz

	if usoMOVTRASBack==True:
		movz=np.array([0,0, movtras*FuerzaControl])
		movz=MbE(angz, angy, angx, movz)
		Xeje=Xeje+movz[0]
		Yeje=Yeje+movz[1]
		Zeje=Zeje+movz[2]*drz

	if usoMOVTRASLeft==True:
		movz=np.array([movtras*FuerzaControl,0,0])
		movz=MbE(angz, angy, angx, movz)
		Xeje=Xeje-movz[0]
		Yeje=Yeje-movz[1]
		Zeje=Zeje-movz[2]*drz

	if usoMOVTRASRight==True:
		movz=np.array([movtras*FuerzaControl,0,0])
		movz=MbE(angz, angy, angx, movz)
		Xeje=Xeje+movz[0]
		Yeje=Yeje+movz[1]
		Zeje=Zeje+movz[2]*drz

	if usoMOVTRASUp==True:
		movz=np.array([0,movtras*FuerzaControl,0])
		movz=MbE(angz, angy, angx, movz)
		Xeje=Xeje-movz[0]
		Yeje=Yeje-movz[1]
		Zeje=Zeje-movz[2]*drz

	if usoMOVTRASDown==True:
		movz=np.array([0,movtras*FuerzaControl,0])
		movz=MbE(angz, angy, angx, movz)
		Xeje=Xeje+movz[0]
		Yeje=Yeje+movz[1]
		Zeje=Zeje+movz[2]*drz


	if usoKEYDRCOM1==True:
		drz=drz-1

	if	usoKEYDRCOM2==True:
		drz=drz+1

	for event in pygame.event.get():
		print(event)
		if event.type == pygame.KEYUP:

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
    
			elif event.key == pygame.K_x:
				jugando = False
				pygame.quit()
				sys.exit()

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

				
			elif event.key==104: #H
				#print("H")
				if Slow==True:
					pass
				else:
					FuerzaControl=FuerzaControl-1
					FuerzaControlvieja=FuerzaControl


			elif event.key==110: #N
				#print("N")
				tau=tau-0.001	

				
			elif event.key==109: #M
				#print("M")
				tau=tau+0.001


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

			elif event.key==96: # |
				if PAREDES==True:
					PAREDES=False

				else:
					PAREDES=True
				#PAREDES=CParedes(PAREDES)



			elif event.key==32:  #Barra espaciadora

				if CantBolas==1:
					tau=1
					x[0]=0
					y[0]=0
					z[0]=0
					Xeje=0
					Yeje=0
					Zeje=0


				if CantBolas<=2:
					pipi1=0
					pipi2=0
					pipi3=(250)*dr
					stvx=0
					stvy=0
					stvz=1
				elif CantBolas<=4:
					pipi1=0
					pipi2=250*dr
					pipi3=0
					stvx=0
					stvy=1
					stvz=0
				else:
					pipi1=(250)*dr
					pipi2=0
					pipi3=0
					stvx=1
					stvy=0

				CantBolas=CantBolas+1
				x.append(pipi2)
				y.append(pipi3)
				z.append(pipi1)
				if pipi1==0:
					vx.append(0)
				else:
					vx.append(-(stvx*dt*G*M[0]/(((pipi1)**2)**(0.5)))**(1/2))
				if pipi2==0:
					vy.append(0)
				else:
					vy.append(-(stvy*dt*G*M[0]/(((pipi2)**2)**(0.5)))**(1/2))

				if pipi3==0:
					vz.append(0)
				else:
					vz.append(-(stvz*dt*G*M[0]/(((pipi3)**2)**(0.5)))**(1/2))
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

			elif event.key==303:  #Shift D
				if freez==True:
					freez=False
				else:
					freez=True


			elif event.key==1073742049:  #Shift I
				Slow=True

			elif event.key==270:  #+ TEC NUM
				if M[0]>=3000:
					M[0]=M[0]+1000
				elif M[0]>=300:
					M[0]=M[0]+100
				elif M[0]>=10:
					M[0]=M[0]+10
				else:
					M[0]=M[0]+1

			elif event.key==269:  #- TEC NUM
				if M[0]>3000:
					M[0]=M[0]-1000
				elif M[0]>300:
					M[0]=M[0]-100
				elif M[0]>10:
					M[0]=M[0]-10
				else:
					M[0]=M[0]-1




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