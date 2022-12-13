from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import serial
from datetime import datetime, date
global file
global a
global b
global ser

a=date.today()
print (a)
while True:
    import math
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    global temperature

    b=date.today()

    if a==b :
        
        print ("continue")

        global temperature
        global fig
        fig = plt.figure(figsize=(5.2,3.2))
  
        running = None  # Global flag

        root = Tk()
        root.title("Solar Spectrum Simulator")
        #root.geometry("500x500")
        root.configure(bg='light yellow')
#        w = 800 # width for the Tk root
#        h = 650 # height for the Tk root
#
        # get screen width and height
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight()

        def welcome():
                print("Welcome")
                
####################################

        def start():
            """Enable scanning by setting the global flag to True."""
            global running
            running = True
            root.after(1000, scanning)

        def stop():
            """Stop scanning by setting the global flag to False."""
            global running
            running = False

        def equations():

            import math 
            import numpy as np 
            import matplotlib.pyplot as plt
            import csv
            import pandas as pd

            day1 = int(day.get());

            tilt1 = float(tilt.get())

            zenith1 = float(zenith.get())

            delta1 = float(delta.get());

            hour1 = int(hour.get())

            longitude1 = float(longitude.get());

            latitude1 = float(latitude.get())

            humidity1 = float(humidity.get())

            temperature1 = float(temperature.get())

            #relative airmass
            
            temp=(2*(math.pi)*(day1-1))/365;
            

            M=(math.cos(30.8)+(0.15)*(93.885-30.8)**(-1.253))**(-1);
            print('M=',M);

            ho=22000; ##height of maximum ozone concentration

            #ozone mass
            Mo = (1+(ho/6370)/((math.cos(zenith1)*math.cos(zenith1))+(2*ho/6370)))**0.5;

            #ozone amount
            O3=0.344

            P=1013; #measure surface pressure
            P0=1013;

            ##earth-sun distance factor
            D=1.00011+0.034221*math.cos(temp)+0.00128*math.sin(temp)+0.000719*math.cos(2*temp)+0.000077*math.sin(2*temp);
            print('D=',D);

            ALG= math.log(1-0.65)
            AFS=ALG*(1.459+ALG*(0.1595+ALG*0.4129))
            BFS=ALG*(0.0783+ALG*(-0.3824-ALG*0.5874))
            Fs=1*0.5*math.exp((AFS+BFS*math.cos(zenith1))*math.cos(zenith1))
            print('Fs=',Fs);

            Td=temperature1-((100-humidity1)/5);
            W=math.exp(0.981+(0.0341*Td));

            au_file = csv.DictReader(open("coefficients.csv"))
            file= open('transmittance' + '.csv', 'w')
            file.write("wavelength"+","+"Tu"+","+"To"+","+"Tr"+","+"Ta"+","+"Tw"+","+"I"+","+"omega\n")
            for col in au_file:

                  #gaseous absorption coefficient
                  au= float(col["au"])

                  #ozone absorption coefficient
                  ao=float(col["ao"])

                  #water vapor absorption coefficient
                  aw=float(col["aw"])
                  
                  #extraterrestrial spectrum
                  Ho=float(col["Ho"])
                  
                  w=int(col["wavelength"])
             
                  ##uniformly mixed gas absorption     
                  Tu=math.exp((-1.41*au*M)/(1+118.93*au*M)**0.45);

                  ##ozone absorption
                  To=math.exp(-ao*O3*Mo);

                  ##Rayleigh scattering
                  Tr=(math.exp(-M/((w**4)*(115.6406-(1.335/w**2)))));
                  
                  ##aerosol scattering
                  Ta=(math.exp(0.155*w**(-1.140)*M));

                  ##water absorption
                  Tw=math.exp((-0.2385*aw*1.42*M)/(1+20.07*aw*1.42*M)**0.43);

                  ##extraterrestrial irradiance*earth-sun distance
                  I= Ho*D;
                  
                  ##wavelength variation factor
                  omega=0.945*(math.exp(-0.095*(math.log(w/0.4))**2))

                  file= open('transmittance' + '.csv','a')
                  file.write(str(w)+","+str(Tu)+","+str(To)+","+str(Tr)+","+str(Ta)+","+str(Tw)+","+str(I)+","+str(omega)+"\n" ) 
                  file.flush()
                  file.close()
            file.close()
            final_file = csv.DictReader(open("transmittance.csv"))
            file= open('irradiances' + '.csv', 'w')
            file.write("wavelength"+","+"I"+","+"Id"+","+"Ir"+","+"Ia"+","+"Ig"+","+"Is\n")
            for col in final_file:
                  Tu=float(col["Tu"])
                  To=float(col["To"])
                  Tw=float(col["Tw"])
                  Ta=float(col["Ta"])
                  Tr=float(col["Tr"])
                  I=float(col["I"])
                  w=int(col["wavelength"])
                  o=float(col["omega"])

                  ##direct irradiance
                  Id=Tu*To*Ta*Tr*Tw*I;

                  ##rayleigh scattering component
                  Ir=I*math.cos(zenith1)*Tu*To*Ta*Tw*(1-Tr)*0.5

                  ##aerosol scattering component
                  Ia=I*math.cos(zenith1)*Tu*To*Tr*Tw*(1-Ta)*o*Fs

                  ##component that accounts for multiple reflections betwwen ground and air
                  Ig=(Tu*To*Ta*Tr*Tw*I*math.cos(zenith1))+(I*math.cos(zenith1)*Tu*To*Ta*Tw*(1-Tr)*0.5)+(I*math.cos(zenith1)*Tu*To*Tr*Tw*(1-Ta)*o*Fs)

                  ##total scattered irradiance
                  Is=((I*math.cos(zenith1)*Tu*To*Ta*Tw*(1-Tr)*0.5)+(I*math.cos(zenith1)*Tu*To*Tr*Tw*(1-Ta)*o*Fs)+((Tu*To*Ta*Tr*Tw*I*math.cos(zenith1))+(I*math.cos(zenith1)*Tu*To*Ta*Tw*(1-Tr)*0.5)+(I*math.cos(zenith1)*Tu*To*Tr*Tw*(1-Ta)*o*Fs)))/1000

                  file=open('irradiances' + '.csv','a')
                  file.write(str(w)+","+str(I)+","+str(Id)+","+str(Ir)+","+str(Ia)+","+str(Ig)+","+str(Is)+"\n")
                  file.flush()
                  file.close()
            file.close()
                  
        def sensors():
            import csv
            from datetime import datetime
            import pandas as pd
            import matplotlib.pyplot as plt
                
            #print("FAHRENHEIT")
            ser = serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=10
                                ,parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS
                                )
            print(ser)
            file = open('hi' + '.csv', 'a')
                
            temp = ser.readline()
            temp = ser.readline()
            temp = ser.readline()
            print(temp)    
            #file= open('hi'+str(a) + '.csv', 'a')
            file= open('hi' + '.csv', 'w')
            file.write("Wavelength"+","+"Irradiance"+"\n")
            file.write(str(temp,"utf-8"))
            file.flush()
                
            temp = ser.readline()
            #file= open('hi'+str(a) + '.csv', 'a')
            file.write(str(temp,"utf-8"))
            file.flush()
            file.close()
            #temp = ser.readline()   
            ##file= open('hi'+str(a) + '.csv', 'a')
            #file.write(str(temp,"utf-8")+"\n")
            #file.flush()
            #sensors_value()
                
            #dff = pd.read_csv('hi.csv', skiprows = [1])
            #y1=dff['Irradiance']
            #x1=dff['Wavelength']

        def nsrdb():
            import csv
            from datetime import datetime
            import pandas as pd
            import matplotlib.pyplot as plt
            global t2
            day1 = int(day.get())
            hour1 = int(hour.get())
            #print("Day: %s\nHour: %s" % (e.get(), d.get())
            t1= (int(day.get()) - 1) * 24
            t2= (int(hour.get())) + t1
            print(t2)
            t3 = str(t2)
            print(t3)
            if day1 < 366 and hour1 < 25:    
                labelText7=StringVar(master=root)
                labelText7.set("                             ")
                labelText7.set("      Inputs Verified      ")
                labelDir7=Label(root, textvariable=labelText7,fg="white",bg='green',font= "Times 15 bold", height=1)
                labelDir7.grid(row =15, column=2)
                labelText7=StringVar(master=root)
                    
            else :
                labelText7=StringVar(master=root)
                labelText7.set("Error : Invalid Inputs ")
                labelDir7=Label(root, textvariable=labelText7,fg="white",bg='red',font= "Times 15 bold", height=1)
                labelDir7.grid(row =15, column=2)
                labelText7=StringVar(master=root)
            
            #ff = pd.read_csv('78.8_tmy_use.csv', skiprows = [1])
            #y1=ff[str(t2)]
            #x1=ff['Wavelength']
                
        def gettext1():
            

            import pandas as pd
            import time 
            from time import sleep
            from datetime import datetime
            from matplotlib import pyplot
            from matplotlib import pyplot as plt
            
            if var.get()==2:
                
                equations()
                df = pd.read_csv('irradiances.csv', skiprows = [1])
                y2=df['Is']
                x2=df['wavelength']
                       
            if var.get()==4:

                import csv
                      
            if var.get()==1:

                sensors()
                df = pd.read_csv('hi.csv', skiprows = [1])
                y1=df['Irradiance']
                x1=df['Wavelength']
                    
            if var.get()==3:

                sensors()
                equations()
        
            global fig
            global samples
            fig.clf()
            canvas = FigureCanvasTkAgg(fig, master=root)
            plot_widget = canvas.get_tk_widget()
            plt.xlabel('Wavelength(nm)')
            plt.ylabel('Irradiance(W/m²)')
            if var.get()==1:
               plt.plot(x1,y1,'r')
            elif var.get()==2:
               plt.plot(x2,y2,'b')
               plt.xlim((0,2500))
            elif var.get()==3:
               plt.plot(x1,y1,'r',label="NSRDB")
               plt.plot(x2,y2,'b',label="Equations")
               plt.legend()
            elif var.get()==4:
               plt.ylabel('Temperature Sensor (Fahrenheit)')   
            
            plot_widget.grid(column=0, row=7, rowspan=1,columnspan=1)
            plt.tight_layout()
            fig.canvas.draw()

        def gettext2():

            import pandas as pd 
            if var3.get()==3:

                equations()
                df = pd.read_csv('irradiances.csv', skiprows = [1])
                y2=df['Is']
                x2=df['wavelength']
                
            if var3.get()==4:

                import csv
                from datetime import datetime
                import pandas as pd
                
            if var3.get()==1:

                nsrdb()
                df = pd.read_csv('78.8_tmy_use.csv', skiprows = [1])
                y1=df[str(t2)]
                x1=df['Wavelength']
                
            if var3.get()==2:

                nsrdb()
                df = pd.read_csv('78.8_tmy_use.csv', skiprows = [1])
                y1=df[str(t2)]
                x1=df['Wavelength']
                
                equations()
                ff = pd.read_csv('irradiances.csv', skiprows = [1])
                y2=ff['Is']
                x2=ff['wavelength']
                    
            global fig
            global samples
            fig.clf()
            canvas = FigureCanvasTkAgg(fig, master=root)
            plot_widget = canvas.get_tk_widget()
            plt.xlabel('Wavelength(nm)')
            plt.ylabel('Irradiance(W/m²)')
            if var3.get()==1:
               plt.plot(x1,y1,'r')
            elif var3.get()==3:
               plt.plot(x2,y2,'b')
            elif var3.get()==2:
               plt.plot(x1,y1,'r',label="NSRDB")
               plt.plot(x2,y2,'b',label="Equations")
               plt.xlim((0,2500))
               plt.legend()
            elif var3.get()==4:
               plt.ylabel('None')   
            
            plot_widget.grid(column=2, row=7, rowspan=1,columnspan=1)
            plt.tight_layout()
            fig.canvas.draw()


#..............HEADING AND LOGO.................#

            
        labelText71=StringVar(master=root)
        labelText71.set("Solar Spectrum Simulator") 
        labelDir71=Label(root, textvariable=labelText71,font= "Times 30 bold", height=1,bg='light yellow')
        labelDir71.grid(sticky=tk.W,row=0,column=2)

        labelText72=StringVar(master=root)
        labelText72.set("       ") 
        labelDir72=Label(root, textvariable=labelText72,font= "Times 30 bold", height=1,bg='light yellow')
        labelDir72.grid(sticky=tk.E,row=0,column=4)
        
        im = Image.open("dbitlogo.png")
        imag = im.resize((60,60), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imag, master=root)
        label11 = Label(root, image=img,bg='light yellow')
        label11.grid(row =0, column=0,sticky=tk.N+tk.W,padx=1,pady=1)

        im2 = Image.open("ncprelogo.png")
        imag2 = im2.resize((60,60), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(imag2,master=root)
        label13 = Label(root, image=img2,bg='light yellow')
        label13.grid(row =0, column=4,sticky=tk.N+tk.E,padx=1,pady=1)

#         im1 = Image.open("spec.png")
#         imag1 = im1.resize((200,210), Image.ANTIALIAS)
#         img1 = ImageTk.PhotoImage(imag1,master=root)
#         label12 = Label(root, image=img1,bg='light yellow')
#         label12.grid(row =10, column=4,sticky=tk.W,padx=1,pady=1)

#         labelText73=StringVar()
#         labelText73.set("Project By: Shruti Mehata and Leo Linus") 
#         labelDir73=Label(root, textvariable=labelText73,font= "Times 14 bold", height=1,bg='light yellow')
#         labelDir73.grid(sticky=tk.W,row=14,column=0)
        
#..............BOUNDARY.................#
        import tkinter.ttk

        tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=1, row=1, rowspan=16, sticky=tk.E+tk.N+tk.S)
        tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=3, row=1, rowspan=16, sticky=tk.E+tk.N+tk.S)
        tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=1, columnspan=10, sticky='ew')
        tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=3, columnspan=10, sticky='ew')
        tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=9, columnspan=4, sticky='ew')
        tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=10, columnspan=4, sticky='ew')
#        tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=11, columnspan=4, sticky='ew')
#        tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=12, columnspan=4, sticky='ew')
        tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=1, row=14, columnspan=2, sticky='ews')
#        tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=0, row=10, rowspan=3, sticky=tk.W+tk.N+tk.S)

#.............LIVE PLOTTING....................#            
        labelText2=StringVar(master=root)
        labelText2.set("Plot 1 :")
        labelDir1=Label(root, textvariable=labelText2,fg="blue",bg='light yellow',font= "Times 12 bold", height=1)
        labelDir1.grid(row =2, column=0 ,sticky=tk.N+tk.W)
         
        labelText2=StringVar(master=root)
        labelText2.set("Plot 2 :")
        labelDir1=Label(root, textvariable=labelText2,fg="blue",bg='light yellow',font= "Times 12 bold", height=1)
        labelDir1.grid(row =2, column=2 ,sticky=tk.N+tk.W)

#        labelText3=StringVar(master=root)
#        labelText3.set("SELECT THE TYPE OF PLOT")
#        labelDir2=Label(root, textvariable=labelText3, height=1,bg='light yellow')
#        labelDir2.grid(row =4, column=0 ,sticky=tk.N+tk.W)

        var = IntVar(master=root)
        R1 = Radiobutton(root, text="Sensors Value                                        ",variable=var, value=1,height=1)
        R1.grid(row=5, column=0,sticky=tk.N+tk.W)

        R2 = Radiobutton(root, text="Reference Plot                                       ", variable=var, value=2,height=1)
        R2.grid(row=5, column=0,sticky=tk.N+tk.E)
        
#        R3 = Radiobutton(root, text="NSRDB & Equations                                ", variable=var, value=3,height=1)
#        R3.grid(row=6, column=0,sticky=tk.N+tk.W)

#        R4 = Radiobutton(root, text="None                                                   ", variable=var, value=4,height=1)
#        R4.grid(row=6, column=0,sticky=tk.N+tk.E)

        fig.clf()
        plt.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=root)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=7, column=0,sticky=S+W)
        fig.canvas.draw()


#...................SOLAR PANEL APPLICATION PART............#

#....................SAVED DATA PLOTTING..................#

#        labelText1=StringVar(master=root)
#        labelText1.set("")
#        labelDir=Label(root, textvariable=labelText1,fg="blue",bg='light yellow',font= "Times 12 bold", height=1)
#        labelDir.grid(row =2, column=2 ,sticky=tk.N+tk.W)

#        labelText7=StringVar(master=root)
#        labelText7.set("(NOTE: PAUSE LIVE PLOT TO GET SAVED DATA PLOT)")
#        labelDir7=Label(root, textvariable=labelText7,fg="black",bg='light yellow',font= "Times 10 bold", height=1)
#        labelDir7.grid(row =2, column=2,sticky=tk.N+tk.E)
        
#        labelText4=StringVar(master=root)
#        labelText4.set("SELECT THE TYPE OF PLOT:")
#        labelDir3=Label(root, textvariable=labelText4, height=1,bg='light yellow')
#        labelDir3.grid(row =4, column=2 ,sticky=tk.N+tk.W)

        var3 = IntVar(master=root)
        R6 = Radiobutton(root, text="NSRDB Data                                        ",variable=var3, value=1,height=1)
        R6.grid(row=5, column=2,sticky=tk.N+tk.W)

        R7 = Radiobutton(root, text="Overlay Plot                                            ", variable=var3, value=2,height=1)
        R7.grid(row=5, column=2,sticky=tk.N+tk.E)
              
#        R8 = Radiobutton(root, text="NSRDB & Equations                                ", variable=var3, value=3,height=1)
#        R8.grid(row=6, column=2,sticky=tk.N+tk.W)

#        R9 = Radiobutton(root, text="None                                                   ", variable=var3, value=4,height=1)
#        R9.grid(row=6, column=2,sticky=tk.N+tk.E)

        fig.clf()
        plt.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=root)
        plot_widget = canvas.get_tk_widget()
        #plot_widget.grid(row=7, column=2,sticky=S+E)
        plot_widget.grid(column=2, row=7, rowspan=1,columnspan=1)
        fig.canvas.draw()

#......................ENTRY WIDGET....................#

        labelText7=StringVar(master=root)
        labelText7.set("ENTER : ")
        labelDir7=Label(root, textvariable=labelText7,fg="black",bg='light yellow',font= "Times 10 bold", height=1)
        labelDir7.grid(row =10, column=2,sticky=tk.N+tk.W)

        var12 = tk.IntVar(master=root)
        
        R16 = Radiobutton(root, text="Longitude               -                       ",variable=var12, value=1,height=1).grid(row=11, column=0,sticky=tk.N+tk.W)        
        longitude = tk.Entry(root,width=30)
        longitude.grid(row=12, column=0, sticky=tk.N+tk.W)

        R17 = Radiobutton(root, text="Latitude                                              ",variable=var12, value=2,height=1).grid(row=11, column=0,sticky=tk.N+tk.E)
        latitude = tk.Entry(root,width=30)
        latitude.grid(row=12, column=0,sticky=tk.N+tk.E)

        R18 = Radiobutton(root, text="Tilt Angle                                      ",variable=var12, value=3,height=1).grid(row=13, column=0,sticky=tk.N+tk.W)        
        tilt = tk.Entry(root,width=30)
        tilt.grid(row=14, column=0, sticky=tk.N+tk.W)

        R19 = Radiobutton(root, text="Zenith Angle                                      ",variable=var12, value=4,height=1).grid(row=13, column=0,sticky=tk.N+tk.E)
        zenith = tk.Entry(root,width=30)
        zenith.grid(row=14, column=0,sticky=tk.N+tk.E)

        R20 = Radiobutton(root, text="Humidity                                            ",variable=var12, value=5,height=1).grid(row=15, column=0,sticky=tk.N+tk.W)        
        humidity = tk.Entry(root,width=30)
        humidity.grid(row=16, column=0, sticky=tk.N+tk.W)

        R21 = Radiobutton(root, text="Temperature                                      ",variable=var12, value=6,height=1).grid(row=15, column=0,sticky=tk.N+tk.E)
        temperature = tk.Entry(root,width=30)
        temperature.grid(row=16, column=0,sticky=tk.N+tk.E)
        
        R22 = Radiobutton(root, text="Day                                                ",variable=var12, value=7,height=1).grid(row=11, column=2,sticky=tk.N+tk.W)
        day = tk.Entry(root,width=30)
        day.grid(row=12, column=2, sticky=tk.W+tk.N)

        R23 = Radiobutton(root, text="Hour                                                     ",variable=var12, value=8,height=1).grid(row=11, column=2,sticky=tk.N+tk.E)
        hour = tk.Entry(root,width=30)
        hour.grid(row=12, column=2,sticky=tk.N+tk.E)

        R24 = Radiobutton(root, text="Difference between local time and universal standard time in India",variable=var12, value=9,height=1).grid(row=13, column=2,sticky=tk.N+tk.W)
        delta = tk.Entry(root,width=30)
        delta.grid(row=14, column=2,sticky=tk.N+tk.W)

        labelText9=StringVar(master=root)
        labelText9.set("ENTER : ")
        labelDir9=Label(root, textvariable=labelText9,fg="black",bg='light yellow',font= "Times 10 bold", height=1)
        labelDir9.grid(row =10, column=0,sticky=tk.N+tk.W)
        labelText9=StringVar(master=root)
        
        labelText3=StringVar(master=root)
        labelText3.set("MESSAGE:")
        labelDir2=Label(root, textvariable=labelText3, height=1,bg='light yellow')
        labelDir2.grid(row =15, column=2 ,sticky=tk.N+tk.W)
   
        labelText3=StringVar(master=root)
        labelText3.set("Virtual Keypad")
        labelDir=Label(root, textvariable=labelText3,font= "Times 12 bold italic", height=2,bg='light yellow')
        labelDir.grid(row=10,column=4, sticky=tk.S+tk.W)
        
        c = Button(root,text='Plot 1',bg='light blue',command=gettext1)
        c.grid(sticky=tk.N+tk.S+tk.W+tk.E,column=0,row=6)

        cc = Button(root,text='Plot 2',bg='light blue',command=gettext2)
        cc.grid(sticky=tk.N+tk.S+tk.W+tk.E,column=2,row=6)
      #  c.size(height=50, width=50)
#-------------------popup window------------------#

        def clickforhelp():

            toplevel = Toplevel(bg="light yellow")
            toplevel.title("User Guide")
            #label1 = Label(toplevel, text="USER GUIDE:", height=0,bg="light pink")
            #label1.grid(sticky=tk.W+tk.S)
            #label3 = Label(toplevel, text="       spacing      ",bg="light yellow",fg="light yellow")
            #label3.grid(sticky=tk.W,row=1,column=0)

            label2 = Label(toplevel, text="There are 2 canvases on which the desired graphs can be obtained.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=2)
            #label3 = Label(toplevel, text="       spacing      ",bg="light yellow",fg="light yellow")
            #label3.grid(sticky=tk.W,row=3,column=0)
            label2 = Label(toplevel, text="1. Canvas 1 gives you two options :", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=4)
            label2 = Label(toplevel, text="    (a)Sensors Value", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=5)
            label2 = Label(toplevel, text="       -->To get the plot just select the Sensors value option.  ", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=6)
            label2 = Label(toplevel, text="       -->And click on the button below ", height=0,bg="light yellow")
##            label2.grid(sticky=tk.W,column=0,row=7)
            label3 = Label(toplevel, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=8,column=0)
            label2 = Label(toplevel, text="    (b)Reference Plot    ", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=9)
            label2 = Label(toplevel, text="       -->This option gives the user a reference plot based on some user defined values.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=10)
            label3 = Label(toplevel, text="            The main purpose of having this reference plot so that the user will be able to compare other plots with this one.",bg="light yellow")
            label3.grid(sticky=tk.W,row=11,column=0)
            label2 = Label(toplevel, text="            This will eventually help them to check the accuracy of their plot.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=12)
            label2 = Label(toplevel, text="       -->To get this plot select the Reference plot option by clicking on the radiobutton.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=13)
            label2 = Label(toplevel, text="       -->Then enter the values in all of the empty boxes provided below the canvas.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=14)
            label2 = Label(toplevel, text="       -->Then click on Plot button to get the plot.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=15)
            label3 = Label(toplevel, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=16,column=0)
            label2 = Label(toplevel, text="2. Canvas 2 also gives you 2 options :", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=17)
            label2 = Label(toplevel, text="    (a)NSRDB Data", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=18)
            label2 = Label(toplevel, text="       -->This plot uses all the values which are collected by National Solar Radiation Database.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=19)
            label2 = Label(toplevel, text="       -->To get the plot just select the NSRDB Plot button.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=20)
            label2 = Label(toplevel, text="       -->Then fill in the day number and the hour of the day at which the plot is desired.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=21)
            label2 = Label(toplevel, text="       -->Then just click on the Plot button.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=22)
            #label2 = Label(toplevel, text="       -->If all information is mentioned properly then the graph will be seen",bg="light yellow")
            #label2.grid(sticky=tk.W,row=22,column=0)
            label3 = Label(toplevel, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=23,column=0)
            label2 = Label(toplevel, text="    (b) Overlay Plot ", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=24)
            label2 = Label(toplevel, text="       --> This option will plot the reference plot and the Nsrdb plot on the same canvas.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=25)
            label2 = Label(toplevel, text="       -->This will help to match the plots.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=26)
            label2 = Label(toplevel, text="       -->To get this plot select the Overlay Plot option.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=27)
            label2 = Label(toplevel, text="       -->Then enter the values in all of the empty boxes provided below the canvas.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=28)
            label2 = Label(toplevel, text="       -->Then click on Plot button to get the plot.", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=29)
            label3 = Label(toplevel, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=30,column=0)
            label2 = Label(toplevel, text="3. Virtual Keypad ", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=31)
            label2 = Label(toplevel, text="    --> In case you don't have your keyboard, you can still enter the values by using the Virtual Keypad. ", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=32)
            label2 = Label(toplevel, text="    --> You can find the virtual keypad provided on the bottom right corner of the GUI", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=33)
            label2 = Label(toplevel, text="    --> To enter the values using virtual keypad click on theempty box that you need to fill", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=34)
            label2 = Label(toplevel, text="    --> And then just click on the numbers you want to enter", height=0,bg="light yellow")
            label2.grid(sticky=tk.W,column=0,row=35)
            #label3 = Label(toplevel, text="       spacing      ",bg="light yellow",fg="light yellow")
            #label3.grid(sticky=tk.W,row=33,column=0)
            
        button1 = Button(root, text="USER GUIDE", width=20, command=clickforhelp,bg="light pink")
        button1.grid(column=4,row=2,sticky=tk.E)

        #button3 = Button(root, text="Virtual Keypad Guide", width=20, command=clickforhelp,bg="light pink")
        #button3.grid(column=4,row=2,sticky=tk.E)

        def clicktoseelivevalue():
            toplevel1 = Toplevel(bg="light yellow")
            toplevel1.title("Live Data Analysis")
            label1 = Label(toplevel1, font= "Times 14 bold italic",height=3,text="Live Data Values for all sensors:",bg="light yellow")
            label1.grid(row=0,column=1)
            label3 = Label(toplevel1, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=1,column=0)
            label2 = Label(toplevel1, text="Device Temperature:",font= "Times 12 bold",bg="light green")
            label2.grid(sticky=tk.E,row=1,column=0)
            label3 = Label(toplevel1, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=2,column=0)
            label2 = Label(toplevel1, text="Temperature sensor1:",font= "Times 12 bold",bg="light green")
            label2.grid(sticky=tk.E,row=3,column=0)
            label3 = Label(toplevel1, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=4,column=0)
            label2 = Label(toplevel1, text="Temperature sensor2:",font= "Times 12 bold",bg="light green")
            label2.grid(sticky=tk.E,row=5,column=0)
            label3 = Label(toplevel1, text="       spacing      ",bg="light yellow",fg="light yellow")
            label3.grid(sticky=tk.W,row=6,column=0)
            label2 = Label(toplevel1, text="Temperature sensor3:",font= "Times 12 bold",bg="light green")
            label2.grid(sticky=tk.E,row=7,column=0)
            lab = Label(toplevel1,bg='light yellow',font= "Times 14 bold")
            lab.grid(row=1,column=1)
            lab1 = Label(toplevel1,bg='light yellow',font= "Times 14 bold")
            lab1.grid(row=3,column=1)

#                    canvas = FigureCanvasTkAgg(fig, master=toplevel1)                  
#                    plt.grid(True)
#                    plt.xlabel('Time (s)')
#                    plt.ylabel('Temperature Sensor (Celsius)')
#                    plt.plot(t, tempa, 'r--')#, t, y, 'bs', t, x, 'g^', t, z, 'yo')
#                    fig.clf()  
#                    plot_widget.grid(row=10, columnspan=2,column=0,sticky=S+E)
#                    fig.canvas.draw()
#                    plt.tight_layout()
#                    plt.show()
                
        button2 = Button(root, text="Live Data Analysis", command=clicktoseelivevalue,bg="light pink")
        button2.grid(column=0,row=2,sticky=tk.E)
     
#...................VIRTUAL KEYPAD..................#

        def code1(value):
            global pin

            if value == '<=':
                # remove last number from `pin`
                pin = pin[:-1]
                # remove all from `entry` and put new `pin`
                if var12.get()==1:
                   longitude.delete('0', 'end')
                   longitude.insert('end', pin)
                if var12.get()==2:
                   latitude.delete('0', 'end')
                   latitude.insert('end', pin)
                if var12.get()==3:
                   tilt.delete('0', 'end')
                   tilt.insert('end', pin)
                if var12.get()==4:
                   zenith.delete('0', 'end')
                   zenith.insert('end', pin)
                if var12.get()==5:
                   humidity.delete('0', 'end')
                   humidity.insert('end', pin)
                if var12.get()==6:
                   temperature.delete('0', 'end')
                   temperature.insert('end', pin)
                if var12.get()==7:
                   day.delete('0', 'end')
                   day.insert('end', pin)
                if var12.get()==8:
                   hour.delete('0', 'end')
                   hour.insert('end', pin)
                if var12.get()==9:
                   delta.delete('0', 'end')
                   delta.insert('end', pin)   
                   
            elif value == 'CLR':
                # clear `pin`
                pin = ''
                # clear `entry`
                
                if var12.get()==1:
                   longitude.delete('0', 'end')
                if var12.get()==2:
                   latitude.delete('0', 'end')
                if var12.get()==3:
                   tilt.delete('0', 'end')
                if var12.get()==4:
                   zenith.delete('0', 'end')
                if var12.get()==5:
                   humidity.delete('0', 'end')
                if var12.get()==6:
                   temperature.delete('0', 'end')
                if var12.get()==7:
                   day.delete('0', 'end')
                if var12.get()==8:
                   hour.delete('0', 'end')
                if var12.get()==9:
                   delta.delete('0', 'end')
   
            else:
                pin += value
                
                if var12.get()==1:
                   longitude.insert('end', value)
                if var12.get()==2:
                   latitude.insert('end', value)
                if var12.get()==3:
                   tilt.insert('end', value)
                if var12.get()==4:
                   zenith.insert('end', value)
                if var12.get()==5:
                   humidity.insert('end', value)
                if var12.get()==6:
                   temperature.insert('end', value)
                if var12.get()==7:
                   day.insert('end', value)
                if var12.get()==8:
                   hour.insert('end', value)
                if var12.get()==9:
                   delta.insert('end', value)

        keys = [
            ['1', '2', '3'],    
            ['4', '5', '6'],    
            ['7', '8', '9'],    
            ['-', '0', ':'],
            ['<=', 'CLR',' ']
        ]
        pin = '' # empty string

        # create buttons using `keys`
        for y, row in enumerate(keys, 1):
            for x, key in enumerate(row):
                    b1 = tk.Button(root, text=key, command=lambda val=key:code1(val))
                    if x==0:
                        b1.grid(row=y+10,sticky=tk.W, column=4, ipadx=15)
                    if x==1:
                        b1.grid(row=y+10, column=4, ipadx=15)
                    if x==2:
                        b1.grid(row=y+10,sticky=tk.E, column=4, ipadx=15)

        root.mainloop()
        
    else:
        print ("change")

        a=b

root.mainloop()
