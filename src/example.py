
"""example.py: Use a maze and solve it with classic wall-following
   algorithm.

   The RL versions should be faster
"""

__author__ = "Pablo Alvarado"
__copyright__ = "Copyright 2020, Pablo Alvarado"
__license__ = "BSD 3-Clause License (Revised)"

import time
import math
import random
import dispatcher
import env
import numpy
import simloop

numpy.set_printoptions(threshold=numpy.inf)

class ExampleStepper:
    """Simple stepper performing a random walk"""

    def __init__(self, dispatch):
        self.dispatch = dispatch
        self.reset()
        self.init()
        self.lastRenderingTime = time.perf_counter()
        
    def reset(self):
        """Account for posible serialization of new envirnoments"""
        print("ExampleStepper.reset() called")

        # Do this to get a valid reference to the environment in use
        self.env = self.dispatch.env()

        # You can for instance get the number of cells in the maze with:
        self.xCells = self.env.maze.nx
        self.yCells = self.env.maze.ny

        # Or also get the size of a cell
        self.cellSizeX = self.env.maze.cellSizeX
        self.cellSizeY = self.env.maze.cellSizeY

        # Here an arbitrary step size for the "advance" action
        step = self.env.maze.cellSizeX/3


        # Sample 50/50 a rotation or a translation
        self.actions = [self.env.agent.right,
                        self.env.agent.left,
                        self.env.agent.advance]


        #Inicializar los contadores a 0 y las probabilidades a 1/S
        Initialized_Cont=numpy.zeros((self.env.maze.nx*self.env.maze.ny*4, self.env.maze.nx*self.env.maze.ny*4))
        Initialized_Prob=numpy.zeros((self.env.maze.nx*self.env.maze.ny*4, self.env.maze.nx*self.env.maze.ny*4))

        #Initialized_Prob*=0.01
        Unk_Prob=(1)/(self.env.maze.nx*self.env.maze.ny*4)
        
        self.env.contR=Initialized_Cont.copy()
        
        
        self.env.contL=Initialized_Cont.copy()
        

        self.env.contA=Initialized_Cont.copy()


##        0 1 2 3  =0
##        4 5 6 7  =1 
##        8 9 10 11 =2  todos estos comparten x y y

##        8%4 = 0  número de columnaa

        self.env.probR=Initialized_Prob.copy()
        self.env.probL=Initialized_Prob.copy()
        self.env.probA=Initialized_Prob.copy()


##Cada estado tiene 4 estados adyacentes, dos girar, el mismo, y donde cae luego de avanzar 
        i=0
        while i< self.env.maze.nx*self.env.maze.ny*4:
            puntero=math.floor(i/4)*4
            
##            punterox=math.floor(i/4)-math.floor(i/(4*self.env.maze.nx))*self.env.maze.nx
##            punteroy=math.floor(i/(4*self.env.maze.nx))
            
            inp=0.001
            self.env.probR[i][i]=inp ##Misma Posición x y
            self.env.probL[i][i]=inp ##Misma Posición x y
            self.env.probA[i][i]=inp ##Misma Posición x y

            
            self.env.probR[i][puntero+(i+1)%4]=inp  ## Giro hacia la derecha
            self.env.probL[i][puntero+(i-1)%4]=inp  ## Giro hacia la izquierda

        
            if i%4==0:
                if (i%(4*self.env.maze.nx))<(4*self.env.maze.nx-4):
                    self.env.probA[i][i+4]=inp 
                else:
                    self.env.probA[i][i]=1
                    
            elif i%4==1:
                if (i/(4*self.env.maze.nx))<(self.env.maze.ny-1):
                    self.env.probA[i][i+4*self.env.maze.nx]=inp
                else:
                    self.env.probA[i][i]=1

            elif i%4==2:
                if i%(4*self.env.maze.nx)>2:
                    self.env.probA[i][i-4]=inp
                else:
                    self.env.probA[i][i]=1
                
            elif i/(4*self.env.maze.nx)>=1:
                self.env.probA[i][i-4*self.env.maze.nx]=inp

            else:
                self.env.probA[i][i]=1
            
##            if punterox!=0:
##                Initialized_Prob[i][puntero-4:puntero]=1 ##Izquierda
##            if punterox!=self.env.maze.nx-1:
##                Initialized_Prob[i][puntero+4:puntero+8]=1 ##derecha
##            if punteroy!=0:
##                Initialized_Prob[i][puntero-4*self.env.maze.nx:puntero-4*self.env.maze.nx+4]=1 ##arriba
##            if punteroy!=self.env.maze.ny-1:
##                Initialized_Prob[i][puntero+4*self.env.maze.nx:puntero+4*self.env.maze.nx+4]=1 ##abajo

            i+=1


        

        #Inicializar V(s)=0
        self.env.values=numpy.zeros((self.env.maze.nx*self.env.maze.ny*4,1))
        self.env.politics=numpy.random.randint(3, size=self.env.maze.nx*self.env.maze.ny*4)
        
        Es_Fin=self.env.maze.endX*4+self.env.maze.endY*4*self.env.maze.nx

        self.env.rewards=numpy.full((self.env.maze.nx*self.env.maze.ny*4,1),-0.5)


        self.env.rewards[Es_Fin:Es_Fin+4]=1
        #self.env.rewards[2*4:2*4+4]=-0.1
        self.env.rewards[self.env.maze.startX:self.env.maze.startX+4]=-1
        # i=0
        # kp=1
        # while i<=self.env.maze.nx:
        #     kp+=0.01
        #     if Es_Fin+i*4< 4*self.env.maze.nx*self.env.maze.ny:
        #         self.env.rewards[Es_Fin+i*4:Es_Fin + 4 +i*4] += kp*0.01
        #     elif Es_Fin-i*4>=0:
        #         self.env.rewards[Es_Fin - i * 4:Es_Fin + 4 - i * 4] += kp*0.01
        #     elif Es_Fin + i * 4*self.env.maze.nx<4*self.env.maze.nx*self.env.maze.ny:
        #         self.env.rewards[Es_Fin + i * 4*self.env.maze.nx:Es_Fin + 4 + i * 4*self.env.maze.nx] += kp * 0.01
        #     elif Es_Fin - i * 4*self.env.maze.nx>0:
        #         self.env.rewards[Es_Fin - i * 4*self.env.maze.nx:Es_Fin + 4 - i * 4*self.env.maze.nx] += kp * 0.01
        #     i+=1


        self.exploring=0
        self.marc=0

        
    def init(self):
        """Reset and setup the stepper"""

        print("ExampleStepper.init() called")

        # Tell the environment to place the agent at the beginning
        self.env.reset()

        # Ensure the agent's position is properly displayed
        self.dispatch.render()
        self.lastRenderingTime = time.perf_counter()

    cardinalPoints = ['E', 'S', 'W', 'N']

    def step(self, iteration):
        """Perform one simulation step"""

        global D, stepi,γ
        
        γ=0.9

        posac = [self.env.agent.state.posX, self.env.agent.state.posY]
        apx = math.floor(posac[0]/self.env.maze.cellSizeX)
        apy = math.floor(posac[1]/self.env.maze.cellSizeY)


               # """hacia donde veo D=0 Este D=1 Sur D=2 Oeste D=3 Norte"""

        E=0;
        S=1;
        O=2;
        N=3;

        
        
        AngD=self.env.agent.state.angle;
        
        
        if 45 > AngD or AngD >= 315:
            D = 0
        elif 135 > AngD >= 45:
            D = 1
        elif 225 > AngD >= 135:
            D = 2
        elif 315 > AngD >= 225:
            D = 3

        # Only at most 15fps:
        # - Print information about current position 
        # - Draw the agent's position and (if activated) the sensors
        if (time.perf_counter() - self.lastRenderingTime) > 1/15:
            print("ExampleStepper.step(", iteration, ")")
            #print("  Agent continous state: ", self.env.agent)
            #print("  Agent discrete state: ({},{})@{}".\
                  #format(posac[0],
                         #posac[1],
                         #self.cardinalPoints[D]))
            self.dispatch.render()
            self.lastRenderingTime = time.perf_counter()
        



##Una vez conozco se conoce el estado actual se conoce la acción a tomar según la política

##Según el mapeo de 3 dimensiones a 1 el estado es:   

        xi=D+apx*4+apy*4*self.env.maze.nx

##Mi acción según la política
        # acciones=[0,1,2,2]
        # ac=random.choice(acciones)
        ac=self.env.politics[xi]



##############Discretización de los pasos################

        
        Dists=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        Dirxy=[[0,0],[0,0],[0,0],[0,0]]


        Ang=math.radians(AngD)

##Distancia hacia el Este
        
        Mx,My=(apx + 1.5) * self.env.maze.cellSizeX - posac[0] ,  (apy + 0.5) * self.env.maze.cellSizeY - posac[1]
        Mag = math.sqrt(pow(Mx, 2) + pow(My, 2))
        Dists[0]=Mx,My,Mag

##Componentes xy direccionales        
        Ax,Ay=math.cos(Ang) , math.sin(Ang)
        Dirxy[0]=Ax,Ay

##Distancia hacia el Sur

        Mx,My= (apx + 0.5) * self.env.maze.cellSizeX - posac[0],  (apy + 1.5) * self.env.maze.cellSizeY - posac[1]
        Mag = math.sqrt(pow(Mx, 2) + pow(My, 2))
        
        Dists[1]=Mx,My,Mag

##Componentes xy direccionales         
        Ax,Ay=math.cos(Ang)*(-1*(Ang>90)+1*(Ang<=90)) , math.sin(Ang)
        Dirxy[1]=Ax,Ay

#Distancia hacia el Oeste

        Mx,My= (apx - 0.5) * self.env.maze.cellSizeX - posac[0] ,  (apy + 0.5) * self.env.maze.cellSizeY - posac[1]
        Mag = math.sqrt(pow(Mx, 2) + pow(My, 2))
        
        Dists[2]=Mx,My,Mag

##Componentes xy direccionales 
        Ax,Ay=-math.cos(Ang) , math.sin(Ang)
        Dirxy[2]=-Ax,Ay

#Distancia hacia el Norte
        
        Mx,My= (apx + 0.5) * self.env.maze.cellSizeX - posac[0]  ,  (apy - 0.5) * self.env.maze.cellSizeY - posac[1]
        Mag = math.sqrt(pow(Mx, 2) + pow(My, 2))
        
        Dists[3]=Mx,My,Mag

##Componentes xy direccionales 
        Ax,Ay=math.cos(Ang)*(-1*(Ang>270)+1*(Ang<=270)) , math.sin(Ang)
        Dirxy[3]=Ax,Ay



        if D == 0:
            Mag=Dists[0][2]
        elif D == 1:
            Mag=Dists[1][2]
        elif D == 2:
            Mag=Dists[2][2]
        elif D == 3:
            Mag=Dists[3][2]
            

        if ac == 0:
            
            if D == 0: 
                F_Ang=math.acos((Dists[S][0]*Dirxy[0][0]+Dists[S][1]*Dirxy[0][1])/Dists[S][2])    

            elif D == 1: 
                F_Ang=math.acos((Dists[O][0]*Dirxy[1][0]+Dists[O][1]*Dirxy[1][1])/Dists[O][2])

            elif D == 2: 
                F_Ang=math.acos((Dists[N][0]*Dirxy[2][0]+Dists[N][1]*Dirxy[2][1])/Dists[N][2])

            elif D == 3: 
                F_Ang=math.acos((Dists[E][0]*Dirxy[3][0]+Dists[E][1]*Dirxy[3][1])/Dists[E][2])       

            stepi=F_Ang*(180/math.pi)

        elif ac ==1:

            if D == 2: 
                F_Ang=math.acos((Dists[S][0]*Dirxy[2][0]+Dists[S][1]*Dirxy[2][1])/Dists[S][2])    

            elif D == 3: 
                F_Ang=math.acos((Dists[O][0]*Dirxy[3][0]+Dists[O][1]*Dirxy[3][1])/Dists[O][2])

            elif D == 0: 
                F_Ang=math.acos((Dists[N][0]*Dirxy[0][0]+Dists[N][1]*Dirxy[0][1])/Dists[N][2])

            elif D == 1: 
                F_Ang=math.acos((Dists[E][0]*Dirxy[1][0]+Dists[E][1]*Dirxy[1][1])/Dists[E][2])       

            stepi=F_Ang*180/math.pi
            
        elif ac == 2:
            

            if D == 0:
                F_Ang=math.acos((Dists[E][0]*Dirxy[E][0]+Dists[E][1]*Dirxy[E][1])/Dists[E][2])

            elif D == 1:
                F_Ang=math.acos((Dists[S][0]*Dirxy[S][0]+Dists[S][1]*Dirxy[S][1])/Dists[S][2])

            elif D == 2:
                F_Ang=math.acos((Dists[O][0]*Dirxy[O][0]+Dists[O][1]*Dirxy[O][1])/Dists[O][2])

            elif D == 3:
                F_Ang=math.acos((Dists[N][0]*Dirxy[N][0]+Dists[N][1]*Dirxy[N][1])/Dists[N][2]) 

            stepi=F_Ang*180/math.pi
            
            steps=Mag;



        if ac==2:

            if (D*90)>AngD:
                self.env.tryAction(self.env.agent, self.actions[0], stepi)
            else:
                self.env.tryAction(self.env.agent, self.actions[1], stepi)
                
            self.env.tryAction(self.env.agent, self.actions[ac], steps)
        else:
            self.env.tryAction(self.env.agent, self.actions[ac], stepi)

        #print("               Agent after last step: ", self.env.agent)

        #self.dispatch.render()

        Ang=self.env.agent.state.angle;
        
        if 45 > Ang or Ang >= 315:
            nD = 0
        elif 135 > Ang >= 45:
            nD = 1
        elif 225 > Ang >= 135:
            nD = 2
        elif 315 > Ang >= 225:
            nD = 3
            

##mapeo de las 3 dimensiones, x,y,dirección a una dimensión
            
        npx = math.floor(self.env.agent.state.posX/self.env.maze.cellSizeX)
        npy = math.floor(self.env.agent.state.posY/self.env.maze.cellSizeY)
        yi=nD+npx*4+npy*4*self.env.maze.nx
        xi=D+apx*4+apy*4*self.env.maze.nx

##        if xi==yi and posac[0]==self.env.agent.state.posX and posac[1]==self.env.agent.state.posY:
##            print("estoy atascado")
##            self.dispatch.restart()

        
##        if D==0:
##            yis=xi+4
##        elif D==1:
##            yis=xi+self.env.maze.nx*4
##        elif D==2:
##            yis=xi-4
##        else:
##            yis=xi-self.env.maze.nx*4


        
        right_flag,left_flag,forw_flag=0,0,0
        
        if ac == 0:
            self.env.contR[xi][yi] += 1
            #self.env.contL[yi][xi] += 1
            den = sum(self.env.contR[xi][:])
            #den2 = sum(self.env.contL[yi][:])
            right_flag=1
            
        elif ac == 1:
            self.env.contL[xi][yi] += 1
            #elf.env.contL[yi][xi] += 1
            den = sum(self.env.contL[xi][:])
            #den2 = sum(self.env.contL[yi][:])
            left_flag=1
            
        elif ac == 2:
            self.env.contA[xi][yi] += 1
            #self.env.contA[xi][yis]+=0.1
            #self.env.contA[yi-nD+(nD+2)%4][xi-D+(D+2)%4] +=1
            den = sum(self.env.contA[xi][:])
            #den2= sum(self.env.contA[yi-nD+(nD+2)%4][:])
            forw_flag=1

            
            
        if right_flag:
            self.env.probR[xi][:] = self.env.contR[xi][:]/den
            #self.env.probR[yi][:] = self.env.contR[yi][:]/den2
        elif left_flag:
            self.env.probL[xi][:] = self.env.contL[xi][:]/den
            #self.env.probL[yi][:] = self.env.contL[yi][:]/den2
        else:
            self.env.probA[xi][:] = self.env.contA[xi][:]/den
            #self.env.probA[yi-nD+(nD+2)%4][:] = self.env.contA[yi-nD+(nD+2)%4][:]/den2
            
        ##Setting the rewards of the positions in the maze

        
        #print("----")
        #print(self.env.probR[0])

        #print(xi)
           #yi
            # # # # # #
   #xi  # -  - -  -  -
        #
        #
        #
        #

        #print(self.env.probR.shape,self.env.values.shape)
        
        valuesR=numpy.dot(self.env.probR,self.env.values)
        
        #en las filas queda el valor esperado para el estado i haciendo
        
        valuesL=numpy.dot(self.env.probL,self.env.values)
        valuesA=numpy.dot(self.env.probA,self.env.values)



        #print(self.env.probR[xi])
        #print(self.env.probL[xi])
        #print(self.env.probA[xi])




        
        #print(valuesR[xi])
        #print(valuesL[xi])
        #print(valuesA[xi])


        #print(valuesR[yi])
        #print(valuesL[yi])
        #print(valuesA[yi])
        
        values=numpy.append(valuesR,valuesL,1)
        values=numpy.append(values,valuesA,1)

        #print(values[xi])
        
        values_max=numpy.transpose(numpy.append([[]],[values.max(axis=1)],1))





        #print(self.env.rewards)

        #print(values_max)

        #print(γ)
        

               # V      =  Rec(i)  +  γ*(Valor esperado de siguiente acción)(máx)    
        self.env.values=self.env.rewards+γ*values_max



        #print(self.env.values)
        
        self.env.values/=1.2

        #valuesR[yi]-=right_flag*(((xi-D)-(yi-nD))==0)
        #valuesL[yi]-=left_flag*(((xi-D)-(yi-nD))==0)
        #valuesA[yi]-=forw_flag*(((xi-D)-(yi-nD))==0)


        #print(self.env.politics[xi])

        i=0
        while i<self.env.maze.nx*self.env.maze.ny*4:
            Pos_Mov=numpy.where(values[i]==values.max(axis=1)[i])[0]
            if self.exploring:
                Pos_Mov=[0,1,2,2]

            self.env.politics[i]=numpy.random.choice(Pos_Mov)
            #if numpy.where(Pos_Mov==2)[0].size!=0:
                #self.env.politics[i]=2
            #else:
                #self.env.politics[i]=numpy.random.choice(Pos_Mov)
            i+=1

##        if xi==yi and posac[0]==self.env.agent.state.posX and posac[1]==self.env.agent.state.posY:
##            print("estoy atascado")
##            if D==0:
##                if self.env.agent.state.angle>90:
##                    E=self.env.agent.state.angle-360
##                else:
##                    E=self.env.agent.state.angle
##            elif D==1:
##                E=self.env.agent.state.angle-90
##            elif D==2:
##                E=self.env.agent.state.angle-180
##            else:
##                E=self.env.agent.state.angle-270
##            if E<0:
##                self.env.tryAction(self.env.agent, self.actions[0],abs(E))
##            else:
##                self.env.tryAction(self.env.agent, self.actions[1], abs(E))
##            self.env.tryAction(self.env.agent, self.actions[2])
##
##            npxa = math.floor(self.env.agent.state.posX / self.env.maze.cellSizeX)
##            npya = math.floor(self.env.agent.state.posY / self.env.maze.cellSizeY)
##            yia = nD + npxa * 4 + npya * 4 * self.env.maze.nx
##            self.env.contA[xi][yia] +=1
##            den = sum(self.env.contA[xi][:])
##            self.env.probA[xi][:] = self.env.contA[xi][:] / den
##            valuesA = numpy.dot(self.env.probA, self.env.values)
##            values = numpy.append(valuesR, valuesL, 1)
##            values = numpy.append(values, valuesA, 1)
##            values_max = numpy.transpose(numpy.append([[]], [values.max(axis=1)], 1))
##            self.env.values = self.env.rewards + γ * values_max
##            self.env.values /= 1.2
##            i = 0
##            while i < self.env.maze.nx * self.env.maze.ny * 4:
##                Pos_Mov = numpy.where(values[i] == values.max(axis=1)[i])[0]
##                if self.exploring:
##                    Pos_Mov = [0, 1, 2, 2]
##                self.env.politics[i] = numpy.random.choice(Pos_Mov)
##                i += 1
        #     self.env.tryAction(self.env.agent, self.actions[random.choice([0,1])])
        #     if 45 > Ang or Ang >= 315:
        #         Da = 0
        #     elif 135 > Ang >= 45:
        #         Da = 1
        #     elif 225 > Ang >= 135:
        #         Da = 2
        #     elif 315 > Ang >= 225:
        #         Da = 3
        #
        #     ##mapeo de las 3 dimensiones, x,y,dirección a una dimensión
        #
        #     apxa = math.floor(self.env.agent.state.posX / self.env.maze.cellSizeX)
        #     apya = math.floor(self.env.agent.state.posY / self.env.maze.cellSizeY)
        #     aca=random.choice([0,1,2])
        #     self.env.tryAction(self.env.agent, self.actions[aca])
        #     if 45 > Ang or Ang >= 315:
        #         nDa = 0
        #     elif 135 > Ang >= 45:
        #         nDa = 1
        #     elif 225 > Ang >= 135:
        #         nDa = 2
        #     elif 315 > Ang >= 225:
        #         nDa = 3
        #
        #     ##mapeo de las 3 dimensiones, x,y,dirección a una dimensión
        #
        #     npxa = math.floor(self.env.agent.state.posX / self.env.maze.cellSizeX)
        #     npya = math.floor(self.env.agent.state.posY / self.env.maze.cellSizeY)
        #     yia = nDa + npxa * 4 + npya * 4 * self.env.maze.nx
        #     xia = Da + apxa * 4 + apya * 4 * self.env.maze.nx
        #     if aca==2:
        #         self.env.contA[xia][yia] += 1
        #
        #     Da=nDa
        #
        #     ##mapeo de las 3 dimensiones, x,y,dirección a una dimensión
        #
        #     apxa = npxa
        #     apya = npya
        #     aca=random.choice([0,1,2])
        #     self.env.tryAction(self.env.agent, self.actions[aca])
        #     if 45 > Ang or Ang >= 315:
        #         nDa = 0
        #     elif 135 > Ang >= 45:
        #         nDa = 1
        #     elif 225 > Ang >= 135:
        #         nDa = 2
        #     elif 315 > Ang >= 225:
        #         nDa = 3
        #
        #     ##mapeo de las 3 dimensiones, x,y,dirección a una dimensión
        #
        #     npxa = math.floor(self.env.agent.state.posX / self.env.maze.cellSizeX)
        #     npya = math.floor(self.env.agent.state.posY / self.env.maze.cellSizeY)
        #     yia = nDa + npxa * 4 + npya * 4 * self.env.maze.nx
        #     xia = Da + apxa * 4 + apya * 4 * self.env.maze.nx
        #     if aca==2 and not xia==yia:
        #         self.env.contA[xia][yia] += 1
        #
        #     Da=nDa
        #
        #     ##mapeo de las 3 dimensiones, x,y,dirección a una dimensión
        #
        #     apxa = npxa
        #     apya = npya
        #     aca=random.choice([0,1,2])
        #     self.env.tryAction(self.env.agent, self.actions[aca])
        #     if 45 > Ang or Ang >= 315:
        #         nDa = 0
        #     elif 135 > Ang >= 45:
        #         nDa = 1
        #     elif 225 > Ang >= 135:
        #         nDa = 2
        #     elif 315 > Ang >= 225:
        #         nDa = 3
        #
        #     ##mapeo de las 3 dimensiones, x,y,dirección a una dimensión
        #
        #     npxa = math.floor(self.env.agent.state.posX / self.env.maze.cellSizeX)
        #     npya = math.floor(self.env.agent.state.posY / self.env.maze.cellSizeY)
        #     yia = nDa + npxa * 4 + npya * 4 * self.env.maze.nx
        #     xia = Da + apxa * 4 + apya * 4 * self.env.maze.nx
        #     if aca==2 and not xia==yia:
        #         self.env.contA[xia][yia] += 1


        #print(self.env.politics[xi])


        # Check which is the finishing cell
        finX, finY = self.env.maze.endX, self.env.maze.endY



        # Check if the agent as reached the finish cell
        if self.env.finished():
            print("GOAL REACHED!")
            self.dispatch.pause()
            # self.dispatch.restart()  # We could restart instead!
        


# #######################
# # Main control center #
# #######################

# This object centralizes everything
theDispatcher = dispatcher.Dispatcher()

# Provide a new environment (maze + agent)
theDispatcher.setEnvironment(env.Environment(12, 8, 15))

# Provide also the simulation stepper, which needs access to the
# agent and maze in the dispatcher.
theDispatcher.setStepper(ExampleStepper(theDispatcher))

# Start the GUI and run it until quit is selected
# (Remember Ctrl+\ forces python to quit, in case it is necessary)
theDispatcher.run()
