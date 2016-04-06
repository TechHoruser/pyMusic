from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import tkinter
import sys
import time
import urllib
import urllib.request
import re
import ssl
import webbrowser

#fix invalid certificate error
ssl._create_default_https_context = ssl._create_unverified_context

m=[];

def prueba(*args):
    messagebox.showwarning("Alerta","Botón Inutil")

def crearfichero(cadena, nombre, formato):
    f = open (nombre+"."+formato, "w", encoding='utf-8')
    f.write(cadena)
    f.close()
    print ("CREADO")
        
def quitarsaltosdelinea(cadena):
    reemplazar_por = ""
    buscar = "\n"
    cadena = cadena.replace(buscar, reemplazar_por)

    return(cadena)

def contador(segundos):
    if (segundos>0):
        #print(str(segundos) + "s")
        time.sleep(1)
        contador(segundos-1)
    else:
        #print("¡Se acabo!")
        sys.stdout.flush()

def dlProgress(count, blockSize, totalSize):
    widgets = ['Test: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=totalSize).start()
    for count in range(totalSize):
        #print count
        pbar.update(int(count*blockSize*100/totalSize))
    pbar.finish()

def descarga2(url,nombre):
    descargado = False
    while not descargado:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        try:
            html = data.decode('UTF-8')
        except UnicodeDecodeError:
            #Información del contenido de la respuesta
            #print(response.info())
            contador(10)
            urllib.request.urlretrieve(url, nombre+".mp3")
            descargado = True
    
def descargar(video):
    url = "http://youtubemp3.io/converter"
    data = urllib.parse.urlencode({'url': "http://www.youtube.com/watch?v="+video[0]})
    
    results = (urllib.request.urlopen(url, data.encode("utf-8"))).read().decode('UTF-8')

    results = quitarsaltosdelinea(results)
    
    expresion = '.*href="(.*?)" id="download-btn"'
    m = re.search(expresion,results)

    #Nombre de la Canción
    #print(video[1])
    #Enlace de Youtube
    #print(video[0])
    #Enlace de descarga
    #print(m.group(1))
    
    descarga2(m.group(1),video[1])

def reproducir(lista):
    try:
        descargar(m[lista.curselection()[0]])
    except IndexError:
        messagebox.showwarning("Alerta","Selecciona una canción")

def enlace_titulo(html):
    expresion = 'yt-lockup-video.*?yt-lockup-content.*?/watch\?v=(.*?)" class="yt-uix-sessionlink.*?dir="ltr">(.*?)</a>'

    global m
    m = re.findall(expresion,html)
    if not m:
        print('No ha encontrado nada')

    return(m)

def buscar(busqueda, lista):
    lista.delete(0,END)
    buscar = " " 
    reemplazar_por = "+"
    busqueda = busqueda.replace(buscar, reemplazar_por)

    url = "https://www.youtube.com/results?search_query="+busqueda
    response = urllib.request.urlopen(url)
    response.code
    html = response.read().decode("utf8")
    
    html = quitarsaltosdelinea(html)
    #crearfichero(html, "nombre", "html")
    l = enlace_titulo(html)

    for elemento in l:
        lista.insert(END, elemento[1])


root = Tk()
root.title("Música")

mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Búsqueda: ").grid(column=1, row=1, sticky=E)

busqueda = StringVar()
feet_entry = ttk.Entry(mainframe, width=50, textvariable=busqueda)
feet_entry.grid(column=2, row=1, sticky=(W, E))

l = Listbox(mainframe)
l.grid(column=2, row=2, rowspan=2, sticky=(E,W))

ttk.Button(mainframe, text="Buscar", command=lambda: buscar(busqueda.get(),l)).grid(column=3, row=1, sticky=W)

ttk.Button(mainframe, text="Reproducir", command=prueba).grid(column=3, row=2, sticky=(S,W))

ttk.Button(mainframe, text="Guardar", command=lambda: reproducir(l)).grid(column=3, row=3, sticky=(N,W))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
