"""#BRUNO HENRIQUE PEREIRA#
    13/05/2021"""

########################    Bibliotecas para manipulações matematicas    #########################
import numpy as np
import math
import sympy
from sympy import *

##########################    Biblioteca para interface gráfica    ###############################
#import tkinter
from tkinter import ttk, Label, LabelFrame, Entry, Frame, Tk, Listbox, Button, Menu, messagebox
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfilename
#from tkinter.ttk import Combobox

###########################    Biblioteca para criação de DXF    #################################
import ezdxf
from ezdxf import bbox

###########################    Biblioteca para criação de PDF    #################################
#from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

######################    Biblioteca para conversão de coordenadas    ############################
from pyproj import Proj



######################################   LEITURA DE ARQUIVOS   ####################################
def Ang(a):
    graus = int(a/10000)
    minutos = int((a/10000 - graus) * 100)/60
    texto_num = str(a)
    texto_seg = int(texto_num[-2:])
    segundos = texto_seg/3600
    decimal = graus+minutos+segundos
    return decimal

def leituraTopcon102N():
    file = askopenfile(mode="r", filetypes = [("TXT", "*.txt")])
    if file is not None:
        global dadosbrutos, estacao, m, precisao_linear, ppm, precisao_angular, precisao_compensador

    ###########################   CONSTANTES DA ESTAÇÃO   #########################################
        precisao_linear=2
        ppm= 2
        precisao_angular=2
        precisao_compensador=1

        dadosbrutos=[]
        estacao = []
        for linha in file:
            dadosbrutos.append(linha)
        file.close()
        m = np.empty((len(dadosbrutos), 10), dtype=list)
                
        def est(a, dados):
            aux1 = []
            aux1.append(dados[a].split("_"))
            return aux1[0][1][1:], float(aux1[0][3][1:])
        def leitura_irr(b, dados):       
            aux = []
            aux.append(dados[b].split("_"))
            m[b][0] = aux[0][1][1:] 
            m[b][4] = float(aux[0][2][3:11])/1000
            m[b][5] = Ang(int(aux[0][2][12:19]))
            m[b][6] = Ang(int(aux[0][2][20:27]))
            m[b][7] = float(aux[0][2][29:37])/1000
            m[b][8] = aux[0][3][1:]
            m[b][9] = float(aux[0][4][1:6])
        for i in range (0, len(dadosbrutos)):
            if dadosbrutos[i][1:2] == "'":
                m[i][1], m[i][2] = est(i, dadosbrutos)
                estacao.append(m[i][1])
                m[i][3] = "ESTACAO"
            else:
                leitura_irr(i, dadosbrutos)
                m[i][1] = m[i-1][1]
                m[i][2] = float(m[i-1][2])
                m[i][3] = "IRRADIACAO"
        messagebox.showinfo(title="CONCLUÍDO", message="Arquivo lido com sucesso!")
    else:
        messagebox.showwarning(title="ERRO", message="Arquivo não encontrado!")
        
def leituraGeodetic():
    print("")
def planilhaManual():
    print("")
    
######################################   CONFIGURAR PARAMETROS   ##################################  
def inserirEstacao(a):
    lista_sequencia_correta.append(a)
    listbox_sequencia_correta.insert(END, a)
    listbox_sequencia_correta.update()
    
def removerEstacao(b):
    for i in lista_sequencia_correta:
        if i == b:
            lista_sequencia_correta.remove(i)
    for i in lista_sequencia_correta:
        listbox_sequencia_correta.insert(END, i)
    listbox_sequencia_correta.update()
    
def parametrosPOLConfigurados(a,b,c,d,e):
    global tipo_poligonal, tipo_ajustamento, tipo_reducao, reducao_ativada, ajustamento_ativado
    tipo_poligonal=a.get()
    tipo_ajustamento = b.get()
    tipo_reducao = c.get()
    reducao_ativada= d.get()
    ajustamento_ativado=e.get()

    messagebox.showinfo(title="Configuração", message="CONCLUÍDA!")

def configurarParametrosPol():
    ConfigurarPol = Toplevel()
    ConfigurarPol.title("Configurar Parametros")
    ConfigurarPol.geometry("1000x600")
    ConfigurarPol.configure(background="#dde")
    frame_confugurarPol = Frame(ConfigurarPol, borderwidth=1, relief="solid")
    frame_confugurarPol.place(x=0, y=0, width=1500, height=1200)
    

    lb_frame_tipo_pol= LabelFrame(frame_confugurarPol, text="Poligonal",borderwidth=1, relief="solid")
    lb_frame_tipo_pol.place(x=20, y=20, width=300, height=125)
    lb_tipo_pol= Label(lb_frame_tipo_pol, text="Tipo = ")
    lb_tipo_pol.place(x=5, y=13)
    lista_tipo_pol=["Fechada e apoiada em pontos distintos", "Fechada e apoiada em um só ponto", "Aberta"]
    cb_tipo_pol = ttk.Combobox(lb_frame_tipo_pol, values=lista_tipo_pol)
    cb_tipo_pol.place(x=60, y=13, width=220, height=20)

    #########################    AJUSTAMENTO   ###############################
    lb_frame_ajustamento= LabelFrame(frame_confugurarPol, text="Processamento",borderwidth=1, relief="solid")
    lb_frame_ajustamento.place(x=20, y=275, width=300, height=100)
    lb_ajust=Label(lb_frame_ajustamento, text="Método = ")
    lb_ajust.place(x=5, y=40)
    lista_ajust=["NBR-13.133 (Método Simplificado)", "Método Paramétrico"]
    cb_ajust = ttk.Combobox(lb_frame_ajustamento, values=lista_ajust)
    cb_ajust.place(x=70, y=40, width=200, height=20)
    ajustamento=IntVar()
    chk_button_ajust=ttk.Checkbutton(lb_frame_ajustamento, text='Ativar', variable=ajustamento, onvalue=1, offvalue=0)
    chk_button_ajust.place(x=5, y=10)    

    ##########################   REDUÇÕES   ##################################
    lb_frame_reducao= LabelFrame(frame_confugurarPol, text="Reduções",borderwidth=1, relief="solid")
    lb_frame_reducao.place(x=20, y=165, width=300, height=100)
    lb_reduc=Label(lb_frame_reducao, text="Plano = ")
    lb_reduc.place(x=5, y=40)
    lista_reduc=["Plano UTM", "Plano Topográfico Local"]
    cb_reduc = ttk.Combobox(lb_frame_reducao, values=lista_reduc)
    cb_reduc.place(x=70, y=40, width=200, height=20)
    reducao=IntVar()
    chk_button_reduc=ttk.Checkbutton(lb_frame_reducao, text='Ativar', variable=reducao, onvalue=1, offvalue=0)
    chk_button_reduc.place(x=5, y=10)
    
    ##########################   SEQUENCIA DE CAMINHAMENTO   #################
    lb_frame_sequencia= LabelFrame(frame_confugurarPol, text="Sequência de caminhamento",borderwidth=1, relief="solid")
    lb_frame_sequencia.place(x=340, y=20, width=400, height=300)
    listbox_sequencia = Listbox(lb_frame_sequencia)
    for i in estacao:
        listbox_sequencia.insert(END, i)
    listbox_sequencia.place(x=30, y=30)
    global listbox_sequencia_correta, lista_sequencia_correta
    lista_sequencia_correta = []
    listbox_sequencia_correta = Listbox(lb_frame_sequencia)
    listbox_sequencia_correta.place(x=220, y=30)
    btn_inserir = Button(lb_frame_sequencia, text=">", command=lambda: inserirEstacao(str(listbox_sequencia.get(ACTIVE))))
    btn_inserir.place(x=165, y=40, width=40, height=30)
    #não funciona o botao de remover
    btn_remover = Button(lb_frame_sequencia, text="<", command=lambda: removerEstacao(str(listbox_sequencia_correta.get(ACTIVE))))
    btn_remover.place(x=165, y=80, width=40, height=30)

    
    btn_configurado = Button(frame_confugurarPol, text="Parametros configurados", command=lambda: parametrosPOLConfigurados(cb_tipo_pol, cb_ajust, cb_reduc, reducao, ajustamento))
    btn_configurado.place(x=800, y=50, width=170, height=30)
    
    ConfigurarPol.mainloop()
    
def parametrosIRRConfigurados(a,b):
    global tipo_propag, propag_ativada
    tipo_propag = a.get()
    propag_ativada = b.get()
    messagebox.showinfo(title="Configuração", message="CONCLUÍDA!")
    
def configurarParametrosIrr():
    configurarIrr = Toplevel()
    configurarIrr.title("Configurar Parametros")
    configurarIrr.geometry("650x400")
    configurarIrr.configure(background="#dde")    
    configurarIrr_frame = Frame(configurarIrr, borderwidth=1, relief="solid")
    configurarIrr_frame.place(x=0,y=0,width=2000, height=2000)
    
    global cb_propagar
    lb_frame_propagar = LabelFrame(configurarIrr_frame, text="Propagação de Variancias", borderwidth=1, relief="solid")
    lb_frame_propagar.place(x=20, y=20, width=300, height=300)
    Label(lb_frame_propagar, text="Método = ").place(x=20, y=40)
    lista_propagar = ["NBR-13.133(Método Simplificado)", "Teoria dos erros (Método Completo)"]
    cb_propagar = ttk.Combobox(lb_frame_propagar, values=lista_propagar)
    cb_propagar.place(x=80, y=40, width=200, height=20)
    propag_irr=IntVar()
    chk_button_propag_irr=ttk.Checkbutton(lb_frame_propagar, text='Ativar', variable=propag_irr, onvalue=1, offvalue=0)
    chk_button_propag_irr.place(x=5, y=10)
    
    btn_irr_config = Button(configurarIrr_frame, text="Parametros Configurados", command=lambda: parametrosIRRConfigurados(cb_propagar,propag_irr))
    btn_irr_config.place(x=235, y=340, width=170, height=30)
    
    configurarIrr.mainloop()
    
################   RECEBE VALORES DE VARIAVEIS E CONFIGURA AS ESTAÇÕES   ##############    
def getConfig(a,b,c):
    global x_base_i, y_base_i, z_base_i, id_referencia_i, x_referencia_i, y_referencia_i, z_referencia_i, x_base_f, y_base_f, z_base_f, id_referencia_f, x_referencia_f, y_referencia_f, z_referencia_f
    global var_x_0, var_y_0, var_z_0, var_x_re, var_y_re, var_z_re, var_x_f, var_y_f, var_z_f, var_x_vante, var_y_vante, var_z_vante
    global fuso, hemisferio, elipsoide
    fuso=int(a.get())
    hemisferio=b.get()
    elipsoide=c.get()
    x_base_i = float(x_i.get())
    y_base_i = float(y_i.get())
    z_base_i = float(z_i.get())
    id_referencia_i = id_i_ref.get()
    x_referencia_i = float(x_i_ref.get())
    y_referencia_i = float(y_i_ref.get())
    z_referencia_i = float(z_i_ref.get())
    var_x_0=float(desv_x_i.get())
    var_y_0=float(desv_y_i.get())
    var_z_0=float(desv_z_i.get())
    var_x_re=float(desv_x_refi.get())
    var_y_re=float(desv_y_refi.get())
    var_z_re=float(desv_z_refi.get())
    if tipo_poligonal == "Fechada e apoiada em pontos distintos" or tipo_poligonal == "Fechada e apoiada em um só ponto":
        x_base_f = float(x_f.get())
        y_base_f = float(y_f.get())
        z_base_f = float(z_f.get())
        id_referencia_f = id_f_ref.get()
        x_referencia_f = float(x_f_ref.get())
        y_referencia_f = float(y_f_ref.get())
        z_referencia_f = float(z_f_ref.get())
        var_x_f=float(desv_x_f.get())
        var_y_f=float(desv_y_f.get())
        var_z_f=float(desv_z_f.get())
        var_x_vante=float(desv_x_reff.get())
        var_y_vante=float(desv_y_reff.get())
        var_z_vante=float(desv_z_reff.get())
        for j in range(0, len(m)):
            if lista_sequencia_correta[-1] == m[j][1] and id_referencia_f == m[j][0]:
                m[j][3] = "VANTE"
    for j in range(0, len(m)):
        if lista_sequencia_correta[0] == m[j][1] and id_referencia_i == m[j][0]:
            m[j][3] = "RE"
    for i in range(0, len(lista_sequencia_correta)-1):
        for l in range(0, len(m)):
            if lista_sequencia_correta[i] == m[l][1] and lista_sequencia_correta[i+1] == m[l][0]:
                m[l][3] = "VANTE"
    for s in range (1, len(lista_sequencia_correta)):
        for d in range(0, len(m)):
            if lista_sequencia_correta[s] == m[d][1] and lista_sequencia_correta[s-1] == m[d][0]:
                m[d][3] = "RE"
    
    messagebox.showinfo(title="CONCLUÍDO", message="Dados coletados com sucesso!")
  
#############################   CRIA ABAS DA PLANILHA DE CAMPO   ######################
def criarAba(nb, j):
    texto=lista_sequencia_correta[j]
    nome = Frame(nb)
    nb.add(nome, text=texto)
    frame_cima = Frame(nome, borderwidth=1, relief="solid")
    frame_cima.place(x=0, y=0, width=2000, height=200)
    frame_baixo = Frame(nome, borderwidth=1, relief="solid")
    frame_baixo.place(x=0, y=200, width=2000, height=4000)
    tv = ttk.Treeview(frame_baixo, columns=("id", "distincli", "angz", "angh", "disth", "descri", "alturap"), show="headings", height=400)
    tv.column("id", minwidth=0, width=50)
    tv.column("distincli", minwidth=0, width=100)
    tv.column("angz", minwidth=0, width=200)
    tv.column("angh", minwidth=0, width=200)
    tv.column("disth", minwidth=0, width=100)
    tv.column("descri", minwidth=0, width=150)
    tv.column ("alturap", minwidth=0, width=150)
    tv.heading("id", text="ID")
    tv.heading("distincli", text="DIST I (m)")
    tv.heading("angz", text="ANG Z (°)")
    tv.heading("angh", text="ANG H (°)")
    tv.heading("disth", text="DIST H (m)")
    tv.heading("descri", text="DESCRIÇÃO")
    tv.heading("alturap", text="ALTURA PRISMA (m)")
    tv.place(x=0, y=0)
    for i in range(0, len(m)):
        if m[i][3] != "ESTACAO":
            if m[i][1] == texto:
                tv.insert("", "end", values=(m[i][0],m[i][4],m[i][5],m[i][6],m[i][7],m[i][8],m[i][9]))
    lb_frame_est = LabelFrame(frame_cima, text="Estação", borderwidth=1, relief="solid")
    lb_frame_est.place(x=10, y=10, width=301, height=180)
    string_1="ESTAÇÃO: "+ texto
    lb_est = Label(lb_frame_est, text=string_1)
    lb_est.pack()
    for i in range(0,len(m)):
        if m[i][1] == texto and m[i][3] == "ESTACAO":
            t="ALTURA = "+str(m[i][2])
            lb_hest = Label(lb_frame_est, text=t)
            lb_hest.pack()
    
    if j == 0:
        lb_frame_ref = LabelFrame(frame_cima, text="Referencia", borderwidth=1, relief="solid")
        lb_frame_ref.place(x=341, y=10, width=301, height=180)
        sub_frame = LabelFrame(lb_frame_est, text="Coordenadas e seus desvios", borderwidth=1, relief="sunken")
        sub_frame.place(x=3, y=40, width=294, height=120)
        Label(sub_frame, text="X =").place(x=15, y=15)
        Label(sub_frame, text="Y =").place(x=15, y=45)
        Label(sub_frame, text="Z =").place(x=15, y=75)
        global x_i, y_i, z_i, id_i_ref, x_i_ref, y_i_ref, z_i_ref, desv_x_i, desv_y_i, desv_z_i, desv_x_refi, desv_y_refi, desv_z_refi
        x_i = Entry(sub_frame)
        y_i = Entry(sub_frame)
        z_i = Entry(sub_frame)
        x_i.place(x=40, y=15, width=100, height=20)
        y_i.place(x=40, y=45, width=100, height=20)
        z_i.place(x=40, y=75, width=100, height=20)
        Label(sub_frame, text="metros").place(x=150, y=15)
        Label(sub_frame, text="metros").place(x=150, y=45)
        Label(sub_frame, text="metros").place(x=150, y=75)
        desv_x_i=Entry(sub_frame)
        desv_y_i=Entry(sub_frame)
        desv_z_i=Entry(sub_frame)
        desv_x_i.place(x=200, y=15, width=50, height=20)
        desv_y_i.place(x=200, y=45, width=50, height=20)
        desv_z_i.place(x=200, y=75, width=50, height=20)
        Label(sub_frame, text="mm").place(x=255, y=15)
        Label(sub_frame, text="mm").place(x=255, y=45)
        Label(sub_frame, text="mm").place(x=255, y=75)        
        Label(lb_frame_ref, text="ID =").place(x=15, y=15)
        Label(lb_frame_ref, text="X =").place(x=15, y=45)
        Label(lb_frame_ref, text="Y =").place(x=15, y=75)
        Label(lb_frame_ref, text="Z =").place(x=15, y=105)
        id_i_ref = Entry(lb_frame_ref)
        x_i_ref = Entry(lb_frame_ref)
        y_i_ref = Entry(lb_frame_ref)
        z_i_ref = Entry(lb_frame_ref)
        id_i_ref.place(x=40, y=15, width=100, height=20)
        x_i_ref.place(x=40, y=45, width=100, height=20)
        y_i_ref.place(x=40, y=75, width=100, height=20)
        z_i_ref.place(x=40, y=105, width=100, height=20)
        Label(lb_frame_ref, text="metros").place(x=150, y=45)
        Label(lb_frame_ref, text="metros").place(x=150, y=75)
        Label(lb_frame_ref, text="metros").place(x=150, y=105)
        desv_x_refi=Entry(lb_frame_ref)
        desv_y_refi=Entry(lb_frame_ref)
        desv_z_refi=Entry(lb_frame_ref)
        desv_x_refi.place(x=200, y=45, width=50, height=20)
        desv_y_refi.place(x=200, y=75, width=50, height=20)
        desv_z_refi.place(x=200, y=105, width=50, height=20)
        Label(lb_frame_ref, text="mm").place(x=255, y=45)
        Label(lb_frame_ref, text="mm").place(x=255, y=75)
        Label(lb_frame_ref, text="mm").place(x=255, y=105)
        
    elif tipo_poligonal == "Fechada e apoiada em pontos distintos" and j == len(lista_sequencia_correta)-1:
        lb_frame_ref = LabelFrame(frame_cima, text="Referencias", borderwidth=1, relief="solid")
        lb_frame_ref.place(x=341, y=10, width=301, height=180)
        sub_frame = LabelFrame(lb_frame_est, text="Coordenadas e seus desvios", borderwidth=1, relief="sunken")
        sub_frame.place(x=3, y=40, width=294, height=120)
        Label(sub_frame, text="X =").place(x=15, y=15)
        Label(sub_frame, text="Y =").place(x=15, y=45)
        Label(sub_frame, text="Z =").place(x=15, y=75)
        global x_f, y_f, z_f, id_f_ref, x_f_ref, y_f_ref, z_f_ref, desv_x_f, desv_y_f, desv_z_f, desv_x_reff, desv_y_reff, desv_z_reff
        x_f = Entry(sub_frame)
        y_f = Entry(sub_frame)
        z_f = Entry(sub_frame)
        x_f.place(x=40, y=15, width=100, height=20)
        y_f.place(x=40, y=45, width=100, height=20)
        z_f.place(x=40, y=75, width=100, height=20)
        Label(sub_frame, text="metros").place(x=150, y=15)
        Label(sub_frame, text="metros").place(x=150, y=45)
        Label(sub_frame, text="metros").place(x=150, y=75)
        desv_x_f=Entry(sub_frame)
        desv_y_f=Entry(sub_frame)
        desv_z_f=Entry(sub_frame)
        desv_x_f.place(x=200, y=15, width=50, height=20)
        desv_y_f.place(x=200, y=45, width=50, height=20)
        desv_z_f.place(x=200, y=75, width=50, height=20)
        Label(sub_frame, text="mm").place(x=255, y=15)
        Label(sub_frame, text="mm").place(x=255, y=45)
        Label(sub_frame, text="mm").place(x=255, y=75)        
        Label(lb_frame_ref, text="ID =").place(x=15, y=15)
        Label(lb_frame_ref, text="X =").place(x=15, y=45)
        Label(lb_frame_ref, text="Y =").place(x=15, y=75)
        Label(lb_frame_ref, text="Z =").place(x=15, y=105)
        id_f_ref = Entry(lb_frame_ref)
        x_f_ref = Entry(lb_frame_ref)
        y_f_ref = Entry(lb_frame_ref)
        z_f_ref = Entry(lb_frame_ref)
        id_f_ref.place(x=40, y=15, width=100, height=20)
        x_f_ref.place(x=40, y=45, width=100, height=20)
        y_f_ref.place(x=40, y=75, width=100, height=20)
        z_f_ref.place(x=40, y=105, width=100, height=20)
        Label(lb_frame_ref, text="metros").place(x=150, y=45)
        Label(lb_frame_ref, text="metros").place(x=150, y=75)
        Label(lb_frame_ref, text="metros").place(x=150, y=105)
        desv_x_reff=Entry(lb_frame_ref)
        desv_y_reff=Entry(lb_frame_ref)
        desv_z_reff=Entry(lb_frame_ref)
        desv_x_reff.place(x=200, y=45, width=50, height=20)
        desv_y_reff.place(x=200, y=75, width=50, height=20)
        desv_z_reff.place(x=200, y=105, width=50, height=20)
        Label(lb_frame_ref, text="mm").place(x=255, y=45)
        Label(lb_frame_ref, text="mm").place(x=255, y=75)
        Label(lb_frame_ref, text="mm").place(x=255, y=105)
    
    ##################################   FUSO   ##############################
    lb_fuso=Label(frame_baixo, text="Fuso = ")
    lb_fuso.place(x=1000, y=30)
    fuso_entrada=Entry(frame_baixo)
    fuso_entrada.place(x=1100, y=30, width=50, height=20)
    
    ################################   HEMISFERIO   ##########################
    lb_hemisferio=Label(frame_baixo, text="Hemisfério = ")
    lb_hemisferio.place(x=1000, y=60)
    lista_hemisferio=["Norte", "Sul"]
    cb_hemisferio=ttk.Combobox(frame_baixo, values=lista_hemisferio)
    cb_hemisferio.place(x=1100, y=60, width=100, height=20)
    
    
    ################################   ELIPSOIDE   ###########################
    lb_tipo_elipsoide=Label(frame_baixo, text="Elipsóide = ")
    lb_tipo_elipsoide.place(x=1000, y=90)
    lista_elipsoide=["Hayford (Córrego Alegre)","GRS 67 (SAD 69)", "GRS 1980 (SIRGAS 2000)", "WGS 1984 (GPS)" ]
    cb_tipo_elipsoide=ttk.Combobox(frame_baixo, values=lista_elipsoide)
    cb_tipo_elipsoide.place(x=1100, y=90, width=220, height=20)
        
    btn_ok = Button(frame_cima, text="OK", command=lambda :getConfig(fuso_entrada, cb_hemisferio, cb_tipo_elipsoide))
    btn_ok.place(x=700, y=50, width=40, height=25)

############################   CRIA A JANELA DA PLANILHA DE CAMPO   ###################    
def confPlanilha():   
    configurarPlanilha = Tk()
    configurarPlanilha.title("Planilha de Campo")
    configurarPlanilha.geometry("2000x1200")
    configurarPlanilha.configure(background="#dde" )
    nb = ttk.Notebook(configurarPlanilha)
    nb.place(x=0, y=0, width=2000, height=1200)
    for i in range(0, len(lista_sequencia_correta)):
        criarAba(nb, i)
    configurarPlanilha.mainloop()
    
#############################   ANGULO ENTRE 0 E 360 EM RADIANOS   ####################
def Graus_Rad(grausdec):
    while grausdec<0:
        grausdec+=360
    while grausdec>360:
        grausdec-=360
    return (grausdec/180)*math.pi

##################################   CALCULO AZIMUTE   #################################
def Azimute(x1, y1, x2, y2):
    del_x = x2 - x1
    del_y = y2 - y1
    if del_x == 0:
        if del_y > 0:
            azimute_ = 0
        elif del_y < 0:
            azimute_ = 180
    elif del_y == 0:
        if del_x > 0:
            azimute_ = 90
        elif del_x < 0:
            azimute_ = 270
    elif del_x > 0 and del_y > 0:
        azimute_ = math.degrees(math.atan(del_x/del_y))
    elif del_x > 0 and del_y < 0:
        azimute_ = math.degrees(math.atan(del_x/del_y))+180
    elif del_x < 0 and del_y < 0:
        azimute_ = math.degrees(math.atan(del_x/del_y))+180
    elif del_x < 0 and del_y > 0:
        azimute_ = math.degrees(math.atan(del_x/del_y))+360
    return azimute_

def ang_0_360(grausdec):
    while grausdec>=360:
        grausdec-=360
    while grausdec<0:
        grausdec+=360
    return grausdec

#############################   AJUSTAMENTO POLIGONAL   ################################
def ajustarPol():
    if ajustamento_ativado == 1:
        global resultados_ajust_ida, resultados_ajust_volta, resultados_ajust
        
        resultados_ajust_ida=np.empty((len(coordenadas_estacao),18), dtype=list)
        resultados_ajust_volta=np.empty((len(coordenadas_estacao),18), dtype=list)
        resultados_ajust=np.empty((len(coordenadas_estacao),18), dtype=list)
        
        ###########################   PROPAGAÇÃO IDA   #############################
        for o in range(0,len(coordenadas_estacao)):
            resultados_ajust_ida[o][0]=coordenadas_estacao[o][0]
            resultados_ajust_ida[o][1]=coordenadas_estacao[o][1]
            resultados_ajust_ida[o][2]=coordenadas_estacao[o][2]
            if o == 0:
                resultados_ajust_ida[o][14]=var_x_0
                resultados_ajust_ida[o][15]=var_y_0
                resultados_ajust_ida[o][17]=math.sqrt(var_x_0**2+var_y_0**2)
            elif coordenadas_estacao[o][0] == lista_sequencia_correta[-1]:
                resultados_ajust_ida[o][14]=var_x_f
                resultados_ajust_ida[o][15]=var_y_f
                
        
        #####################   MÉTODO PROPOSTO PELA NBR 13.133   ###########################    
        if tipo_ajustamento == "NBR-13.133 (Método Simplificado)":
            
            n=1
            for i in range (0, len(m)):
                if m[i][3] == "ESTACAO" and m[i][1] != lista_sequencia_correta[-1]:
                    for j in range (0, len(m)):
                        if m[j][3] == "RE" and m[j][1] == m[i][1]:
                            for k in range (0, len(m)):
                                if m[k][3] == "VANTE" and m[k][1] == m[i][1]:
                                    ###############    ERRO DE CENTRAGEM DA ESTAÇÃO   #########################################
                                    Ei=1*m[i][2] #mm
                                    
                                    ###############    ERRO DE CENTRAGEM DO REFLETOR   ########################################
                                    Er=2.3*m[k][9] #mm
                                    
                                    ###############   PRECISÃO NOMINAL LINEAR DAS DISTANCIAS   ################################
                                    PNlin=precisao_linear+ppm*m[k][7]/1000 #mm
                                    
                                    ###############   DESVIO PADRÃO DA DISTANCIA INCLINADA MÉDIA   ############################
                                    DESV_DI=math.sqrt(Ei**2+Er**2+PNlin**2) #mm
                                    
                                    ###############   DESVIO PADRÃO DO ANGULO ZENITAL MÉDIO   #################################
                                    DESV_z=math.sqrt(2*precisao_angular**2+precisao_compensador**2) #"
                                    
                                    ###############   DESVIO PADRÃO DA DISTANCIA HORIZONTAL   #################################
                                    DESV_DH=math.sqrt((math.sin(math.radians(m[k][5])))**2*DESV_DI**2+(m[k][4]*math.cos(math.radians(m[k][5])))**2*(DESV_z*math.pi/648000)**2) #mm
                                    
                                    ##   EFEITO DO ERRO DE NIVELAMENTO DO INSTRUMENTO SOBRE O ANGULO HORIZONTAL IRRADIADO   ###
                                    DESV_n=math.sqrt(precisao_compensador**2*((1/math.tan(math.radians(m[j][5])))**2+(1/math.tan(math.radians(m[k][5])))**2)) #"
                                    
                                    #########   DISTANCIA HORIZONTAL ENTRE O VÉRTICE DE RÉ E O PONTO VISADO   ###################
                                    DHpv_re = math.sqrt(m[j][7]**2+m[k][7]**2-2*m[j][7]*m[k][7]*math.cos(Graus_Rad(m[k][6]-m[j][6]))) #m
                                    
                                    ###########   EFEITOS DOS ERROS DE CENTRAGEM SOBRE O ANGULO HORIZONTAL IRRADIADO   ##########
                                    DESV_c=math.sqrt(((Er/1000)/(m[j][7]*m[k][7]))**2*(m[j][7]**2+m[k][7]**2)+((Ei/1000)/(m[j][7]*m[k][7]))**2*(DHpv_re/2))*648000/math.pi #"
                                    
                                    ##################   DESVIO PADRÃO DO ANGULO HORIZONTAL IRRADIADO MÉDIO   ###################
                                    DESV_i=math.sqrt(4*precisao_angular**2+DESV_n**2/2+DESV_c**2) #"
                                    
                                    ############################   DESVIO PADRÃO DO AZIMUTE DA RÉ   #############################
                                    if m[i][1] == resultados_ajust_ida[0][0]:
                                        DESV_az_re=math.sqrt(((y_referencia_i-coordenadas_estacao[0][2])/m[j][7]**2)**2*((var_x_re/1000)**2+(var_x_0/1000)**2)+((x_referencia_i-coordenadas_estacao[0][1])/m[j][7]**2)**2*((var_y_re/1000)**2+(var_y_0/1000)**2))*648000/math.pi #"
                                    else:
                                        for p in range(0,len(resultados_ajust_ida)):
                                            if m[i][1]==resultados_ajust_ida[p][0]:
                                                DESV_az_re=math.sqrt(((resultados_ajust_ida[p-1][2]-resultados_ajust_ida[p][2])/m[j][7]**2)**2*((resultados_ajust_ida[p-1][14]/1000)**2+(resultados_ajust_ida[p][14]/1000)**2)+((resultados_ajust_ida[p-1][1]-resultados_ajust_ida[p][1])/m[j][7]**2)**2*((resultados_ajust_ida[p-1][15]/1000)**2+(resultados_ajust_ida[p][15]/1000)**2))*648000/math.pi
                                    
                                    ###########################   DESVIO PADRÃO DO AZIMUTE AO PONTO VISADO   ####################
                                    DESV_az=math.sqrt(DESV_az_re**2+DESV_i**2) #"
                                    
                                    ##############   DESVIO PADRÃO DAS COORDENADAS X E Y E SUA COVARIANCIA   ####################
                                    for l in range(0, len(azimute_estacao)):
                                        if lista_sequencia_correta[l]==m[i][1]:
                                            for x in range(0, len(resultados_ajust_ida)):
                                                if resultados_ajust_ida[x][0]==m[i][1]:
                                                    DESV_x=math.sqrt(resultados_ajust_ida[x][14]**2+(math.sin(azimute_estacao[l]))**2*DESV_DH**2+(m[k][7]*1000*math.cos(azimute_estacao[l]))**2*(DESV_az*math.pi/648000)**2) #mm
                                                    DESV_y=math.sqrt(resultados_ajust_ida[x][15]**2+(math.cos(azimute_estacao[l]))**2*DESV_DH**2+(m[k][7]*1000*math.sin(azimute_estacao[l]))**2*(DESV_az*math.pi/648000)**2) #mm
                                                    co_var_x_y=math.sin(azimute_estacao[l])*math.cos(azimute_estacao[l])*DESV_DH**2-(m[k][7]*1000)**2*math.sin(azimute_estacao[l])*math.cos(azimute_estacao[l])*(DESV_az*math.pi/648000)**2
                                    
                                    ####################################   DESVIO PADRÃO 2D   ###################################
                                    DESV_2d=math.sqrt(DESV_x**2+DESV_y**2)
                                    
                                    resultados_ajust_ida[n][3]=Ei
                                    resultados_ajust_ida[n][4]=Er
                                    resultados_ajust_ida[n][5]=PNlin
                                    resultados_ajust_ida[n][6]=DESV_DI
                                    resultados_ajust_ida[n][7]=DESV_z
                                    resultados_ajust_ida[n][8]=DESV_DH
                                    resultados_ajust_ida[n][9]=DESV_n
                                    resultados_ajust_ida[n][10]=DESV_c
                                    resultados_ajust_ida[n][11]=DESV_i
                                    resultados_ajust_ida[n][12]=DESV_az_re
                                    resultados_ajust_ida[n][13]=DESV_az
                                    resultados_ajust_ida[n][14]=DESV_x
                                    resultados_ajust_ida[n][15]=DESV_y
                                    resultados_ajust_ida[n][16]=co_var_x_y
                                    resultados_ajust_ida[n][17]=DESV_2d
                    n+=1
                    
            ##########################   PROPAGAÇÃO VOLTA   ############################
            g=0
            for o in range(-1,-len(coordenadas_estacao)-1,-1):
                resultados_ajust_volta[g][0]=coordenadas_estacao[o][0]
                resultados_ajust_volta[g][1]=coordenadas_estacao[o][1]
                resultados_ajust_volta[g][2]=coordenadas_estacao[o][2]
                if o == -1:
                    resultados_ajust_volta[g][14]=var_x_f
                    resultados_ajust_volta[g][15]=var_y_f
                    resultados_ajust_volta[g][17]=math.sqrt(var_x_f**2+var_y_f**2)
                elif o == -len(coordenadas_estacao):
                    resultados_ajust_volta[g][14]=var_x_0
                    resultados_ajust_volta[g][15]=var_y_0
                    resultados_ajust_volta[g][17]=math.sqrt(var_x_0**2+var_y_0**2)
                g+=1
            
            lista_sequencia_correta_reversed=list(reversed(lista_sequencia_correta))
            n=1
            for l in range(0,len(lista_sequencia_correta_reversed)-1):
                for i in range (0, len(m)):
                    if m[i][3] == "ESTACAO" and m[i][1]==lista_sequencia_correta_reversed[l]:
                        for j in range (0, len(m)):
                            if m[j][3] == "RE" and m[j][1] == m[i][1]:
                                for k in range (0, len(m)):
                                    if m[k][3] == "VANTE" and m[k][1] == m[i][1]:
                                        Ei_V=1*m[i][2] #mm
                                        Er_V=2.3*m[k][9] #mm
                                        PNlin_V=precisao_linear+ppm*m[k][7]/1000 #mm
                                        DESV_DI_V=math.sqrt(Ei_V**2+Er_V**2+PNlin_V**2) #mm
                                        DESV_z_V=math.sqrt(2*precisao_angular**2+precisao_compensador**2) #"
                                        DESV_DH_V=math.sqrt((math.sin(math.radians(m[k][5])))**2*DESV_DI_V**2+(m[k][4]*math.cos(math.radians(m[k][5])))**2*(DESV_z_V*math.pi/648000)**2) #mm
                                        DESV_n_V=math.sqrt(precisao_compensador**2*((1/math.tan(math.radians(m[j][5])))**2+(1/math.tan(math.radians(m[k][5])))**2)) #"
                                        DHpv_re_V = math.sqrt(m[j][7]**2+m[k][7]**2-2*m[j][7]*m[k][7]*math.cos(Graus_Rad(m[k][6]-m[j][6]))) #m
                                        DESV_c_V=math.sqrt(((Er_V/1000)/(m[j][7]*m[k][7]))**2*(m[j][7]**2+m[k][7]**2)+((Ei_V/1000)/(m[j][7]*m[k][7]))**2*(DHpv_re_V/2))*648000/math.pi #"
                                        DESV_i_V=math.sqrt(4*precisao_angular**2+DESV_n_V**2/2+DESV_c_V**2) #"
                                        if m[i][1] == resultados_ajust_volta[0][0]:
                                            DESV_az_re_V=math.sqrt(((y_referencia_f-coordenadas_estacao[0][2])/m[j][7]**2)**2*((var_x_vante/1000)**2+(var_x_f/1000)**2)+((x_referencia_f-coordenadas_estacao[0][1])/m[j][7]**2)**2*((var_y_vante/1000)**2+(var_y_f/1000)**2))*648000/math.pi #"
                                        else:
                                            for p in range(0,len(resultados_ajust_volta)):
                                                if m[i][1]==resultados_ajust_volta[p][0]:
                                                    DESV_az_re_V=math.sqrt(((resultados_ajust_volta[p-1][2]-resultados_ajust_volta[p][2])/m[j][7]**2)**2*((resultados_ajust_volta[p-1][14]/1000)**2+(resultados_ajust_volta[p][14]/1000)**2)+((resultados_ajust_volta[p-1][1]-resultados_ajust_volta[p][1])/m[j][7]**2)**2*((resultados_ajust_volta[p-1][15]/1000)**2+(resultados_ajust_volta[p][15]/1000)**2))*648000/math.pi
                                        DESV_az_V=math.sqrt(DESV_az_re_V**2+DESV_i_V**2) #"
                                        for l in range(0, len(azimute_estacao)):
                                            if lista_sequencia_correta[l]==m[i][1]:
                                                for x in range(0, len(resultados_ajust_volta)):
                                                    if resultados_ajust_volta[x][0]==m[i][1]:
                                                        DESV_x_V=math.sqrt(resultados_ajust_volta[x][14]**2+(math.sin(azimute_estacao[l]))**2*DESV_DH_V**2+(m[k][7]*1000*math.cos(azimute_estacao[l]))**2*(DESV_az_V*math.pi/648000)**2) #mm
                                                        DESV_y_V=math.sqrt(resultados_ajust_volta[x][15]**2+(math.cos(azimute_estacao[l]))**2*DESV_DH_V**2+(m[k][7]*1000*math.sin(azimute_estacao[l]))**2*(DESV_az_V*math.pi/648000)**2) #mm
                                                        co_var_x_y_V=math.sin(azimute_estacao[l])*math.cos(azimute_estacao[l])*DESV_DH_V**2-(m[k][7]*1000)**2*math.sin(azimute_estacao[l])*math.cos(azimute_estacao[l])*(DESV_az_V*math.pi/648000)**2
                                        DESV_2d_V=math.sqrt(DESV_x_V**2+DESV_y_V**2)
                                        
                                        resultados_ajust_volta[n][3]=Ei_V
                                        resultados_ajust_volta[n][4]=Er_V
                                        resultados_ajust_volta[n][5]=PNlin_V
                                        resultados_ajust_volta[n][6]=DESV_DI_V
                                        resultados_ajust_volta[n][7]=DESV_z_V
                                        resultados_ajust_volta[n][8]=DESV_DH_V
                                        resultados_ajust_volta[n][9]=DESV_n_V
                                        resultados_ajust_volta[n][10]=DESV_c_V
                                        resultados_ajust_volta[n][11]=DESV_i_V
                                        resultados_ajust_volta[n][12]=DESV_az_re_V
                                        resultados_ajust_volta[n][13]=DESV_az_V
                                        resultados_ajust_volta[n][14]=DESV_x_V
                                        resultados_ajust_volta[n][15]=DESV_y_V
                                        resultados_ajust_volta[n][16]=co_var_x_y_V
                                        resultados_ajust_volta[n][17]=DESV_2d_V
                                        n+=1
                        
            #############   COMPARAÇÃO ENTRE OS RESULTADOS DA IDA E DA VOLTA   #####################
            resultados_ajust_volta_reversed=list(reversed(resultados_ajust_volta))
            for i in range(0, len(resultados_ajust_ida)):
                if resultados_ajust_ida[i][17] <= resultados_ajust_volta_reversed[i][17]:
                    for j in range(0,18):
                        resultados_ajust[i][j]=resultados_ajust_ida[i][j]
                else:
                    for k in range(0,18):
                        resultados_ajust[i][k]=resultados_ajust_volta_reversed[i][k]
            
            ###################    Cria uma matriz para impressao    ###############################
            global matriz_impressao
            matriz_impressao = np.empty((len(coordenadas_estacao), 5), dtype=list)
            
            matriz_impressao[0][0] = lista_sequencia_correta[0]
            matriz_impressao[0][3] = var_x_0/100
            matriz_impressao[0][4] = var_y_0/100
            
            matriz_impressao[-1][0] = lista_sequencia_correta[-1]
            matriz_impressao[-1][3] = var_x_f/100
            matriz_impressao[-1][4] = var_y_f/100
            
            for i in range(0, len(coordenadas_estacao)):
                matriz_impressao[i][0] = lista_sequencia_correta[i]
                matriz_impressao[i][1] = coordenadas_estacao[i][1]
                matriz_impressao[i][2] = coordenadas_estacao[i][2]
                if i > 0 and i < len(coordenadas_estacao):
                    matriz_impressao[i][3] = resultados_ajust[i][14]
                    matriz_impressao[i][4] = resultados_ajust[i][15]
                    k+=1
            
        ###############################   MÉTODO PARAMÉTRICO   ##############################
        elif tipo_ajustamento == "Método Paramétrico":
            global A2, A22, variancias, Clb, P, X0, X0_pratico, Y0_pratico, lb, eq, L0, A, L, DELTAX, X01, X01_pratico, Y01_pratico, L01, A1, L1
            ###############   POLIGONAL FECHADA E APOIADA EM PONTOS DISTINTOS   #########
            if tipo_poligonal == "Fechada e apoiada em pontos distintos":
                
                ##########################   MATRIZ LB   ################################
                lb=np.empty((len(lista_sequencia_correta)*2-1,1), dtype=float)
                
                """Essa parte do código cria a matriz das observaçoes com os dados
                    que NÃO passaram por redução para o plano de projeções"""
                
                if reducao_ativada==0:
                    for i in range(0, len(dist)):
                        lb[i][0]=dist[i]
                    for i in range(0, len(azimute_estacao)):
                        lb[i+len(dist)][0]=math.radians(ang_h[i])
                
                elif reducao_ativada==1:
                    """Essa parte do código cria a matriz das observaçoes com os dados
                        que PASSARAM por redução para o plano de projeções"""
                        
                    for i in range(0, len(matriz_reducao)-1):
                        lb[i][0] = matriz_reducao[i][11]
                    for i in range(0, len(ang_h)):
                        lb[i+len(dist)][0]=math.radians(ang_h[i])
                    
                ##########################   MATRIZ Clb   ###############################
                variancias=[]
                #for i in range(0, 2*len(lista_sequencia_correta)-1):
                #    variancias.append(1)
                for i in dist:
                    variancias.append(((precisao_linear+ppm*i/1000)/1000)**2)
                for l in range(0, len(lista_sequencia_correta)):
                    for i in range (0, len(m)):
                        if m[i][3] == "ESTACAO" and m[i][1] == lista_sequencia_correta[l]:
                            for j in range (0, len(m)):
                                if m[j][3] == "RE" and m[j][1] == m[i][1]:
                                    for k in range (0, len(m)):
                                        if m[k][3] == "VANTE" and m[k][1] == m[i][1]:
                                            Ei=1*m[i][2] #mm
                                            Er=2.3*m[k][9] #mm
                                            desv_n=math.sqrt(precisao_compensador**2*((1/math.tan(math.radians(m[j][5])))**2+(1/math.tan(math.radians(m[k][5])))**2)) #"
                                            DHpv_re = math.sqrt(m[j][7]**2+m[k][7]**2-2*m[j][7]*m[k][7]*math.cos(Graus_Rad(m[k][6]-m[j][6]))) #m
                                            desv_c=math.sqrt(((Er/1000)/(m[j][7]*m[k][7]))**2*(m[j][7]**2+m[k][7]**2)+((Ei/1000)/(m[j][7]*m[k][7]))**2*(DHpv_re/2))*648000/math.pi #"
                                            desv_i=math.sqrt(4*precisao_angular**2+desv_n**2/2+desv_c**2) #"
                                            variancias.append(math.radians((desv_i/3600)**2))
                Clb=np.diagflat(variancias)
                
                ####################################   MATRIZ PESO   ############################
                var_priori=1
                P=var_priori*np.linalg.inv(Clb)
                
                ####################################   X0   #####################################
                X0=np.empty((len(lista_sequencia_correta)*2-4,1), dtype=float)
                j=0
                for i in range(1, len(coordenadas_estacao)-1):
                    X0[j][0]=coordenadas_estacao[i][1]
                    j+=1
                    X0[j][0]=coordenadas_estacao[i][2]
                    j+=1
                
                ################################    X0 pratico    ################################
                "Matrizes criadas especialmente para a substituição no modelo funcional"
                
                X0_pratico=[]
                X0_pratico.append(x_referencia_i)
                X0_pratico.append(x_base_i)
                
                Y0_pratico=[]
                Y0_pratico.append(y_referencia_i)
                Y0_pratico.append(y_base_i)
                
                for i in range(1, len(coordenadas_estacao)-1):
                    X0_pratico.append(coordenadas_estacao[i][1])
                    Y0_pratico.append(coordenadas_estacao[i][2])

                X0_pratico.append(x_base_f)
                X0_pratico.append(x_referencia_f)
                Y0_pratico.append(y_base_f)
                Y0_pratico.append(y_referencia_f)
                
                ##############################   MODELO FUNCIONAL   ####################################
                x_id,y_id,x_ref_id,y_ref_id,x_fd,y_fd,x_ref_fd,y_ref_fd = sympy.symbols("x_id y_id x_ref_id y_ref_id x_fd y_fd x_ref_fd y_ref_fd")
                
                #####################   AJUSTAMENTO PARA POLIGONAL COM 4 ESTAÇÕES   ####################
                if len(lista_sequencia_correta)==4:
                    ###################   Parametros para poligonal com 4 estaçoes   #####################
                    x1d,y1d,x2d,y2d = sympy.symbols("x1d y1d x2d y2d")
                    par=[x1d, y1d, x2d, y2d]
                    parametros_x=[x_ref_id, x_id, x1d, x2d, x_fd, x_ref_fd]
                    parametros_y=[y_ref_id, y_id, y1d, y2d, y_fd, y_ref_fd]
                    
                #####################   AJUSTAMENTO PARA POLIGONAL COM 5 ESTAÇÕES   ####################
                if len(lista_sequencia_correta)==5:
                    ###################   Parametros para poligonal com 5 estaçoes   #####################
                    x1d,y1d,x2d,y2d,x3d,y3d = sympy.symbols("x1d y1d x2d y2d x3d y3d")
                    par=[x1d, y1d, x2d, y2d, x3d, y3d]
                    parametros_x=[x_ref_id, x_id, x1d, x2d, x3d, x_fd, x_ref_fd]
                    parametros_y=[y_ref_id, y_id, y1d, y2d, y3d, y_fd, y_ref_fd]
                    
                eq=[]
                i2=0
                for i in range(0,2*len(lista_sequencia_correta)-1):
                    if i <= len(lista_sequencia_correta)-2:
                        eq.append(sympy.sqrt((parametros_x[i+2]-parametros_x[i+1])**2+(parametros_y[i+2]-parametros_y[i+1])**2))
                    else:
                        eq.append(sympy.atan((parametros_x[i2+2]-parametros_x[i2+1])/(parametros_y[i2+2]-parametros_y[i2+1])) - sympy.atan((parametros_x[i2]-parametros_x[i2+1])/(parametros_y[i2]-parametros_y[i2+1])))
                        i2+=1
                
                ###################################   L0=F(X0)   ######################################
                distancia_i = sympy.sqrt((x_fd-x1d)**2+(y_fd-y1d)**2)
 
                L0=np.empty((2*len(lista_sequencia_correta)-1,1), dtype=list)
                j=0
                for i in range (0, len(L0)):    
                    if i <= len(lista_sequencia_correta)-2:
                        L0[i][0] = float(distancia_i.subs({x_fd: X0_pratico[i+1], x1d: X0_pratico[i+2], y_fd: Y0_pratico[i+1], y1d: Y0_pratico[i+2]}).n())
                    else:
                        azimute_1 = Azimute(X0_pratico[j+1], Y0_pratico[j+1], X0_pratico[j], Y0_pratico[j])
                        azimute_2 = Azimute( X0_pratico[j+1], Y0_pratico[j+1], X0_pratico[j+2], Y0_pratico[j+2])
                        ang_az2_az1 = azimute_2 - azimute_1
                        if ang_az2_az1 < 0:
                            ang_az2_az1 += 360
                        L0[i][0] = float(math.radians(ang_az2_az1))
                        j+=1

                ###################################   MATRIZ DESIGN   ##########################################
                A1=[]
                br=0
                for i in range(0,len(eq)):
                    for j in range(0,len(par)):
                        if i <= len(lista_sequencia_correta)-2:
                            A1.append(sympy.diff(eq[i],par[j]).subs({parametros_x[i+1]: X0_pratico[i+1], parametros_x[i+2]: X0_pratico[i+2], parametros_y[i+1]: Y0_pratico[i+1], parametros_y[i+2]: Y0_pratico[i+2]}).n())
                        else:
                            A1.append(sympy.diff(eq[i],par[j]).subs({parametros_x[br+2]: X0_pratico[br+2], parametros_x[br+1]: X0_pratico[br+1], parametros_x[br]: X0_pratico[br], parametros_y[br+2]: Y0_pratico[br+2], parametros_y[br+1]: Y0_pratico[br+1], parametros_y[br]: Y0_pratico[br]}).n())
                            if j == len(par)-1:
                                br+=1
                            
                A=np.empty((2*len(lista_sequencia_correta)-1, 2*len(lista_sequencia_correta)-4), dtype=float)
                i2=0
                for i in range(0, 2*len(lista_sequencia_correta)-1):
                    for j in range(0, 2*len(lista_sequencia_correta)-4):
                        A[i][j]=float(A1[i2])
                        i2+=1
                
                #####################################   L=Lb-L0   #########################################
                L = np.empty((len(lb),1), dtype=list)
                for i in range(0, len(lb)):
                    L[i][0]=lb[i][0]-L0[i][0]
                
                ###########################   CORREÇÕES APROXIMADAS   #####################################
                global determinante_AtPA
                determinante_AtPA=np.linalg.det(np.transpose(A)@P@A)
                if determinante_AtPA != 0:
                    global DELTAX, XA, iteracoes, XA1
                    DELTAX=np.linalg.inv(np.transpose(A)@P@A)@np.transpose(A)@P@L

                    #######################   Confere se convergiu   ######################################
                    def confere_convergencia(DELTA):
                        criterio_c = math.exp(-10)
                        contador=0
                        for i in DELTA:
                            if abs(i) > criterio_c: 
                                contador+=1
                        if contador != 0: return False
                        else: return True
                    
                    ##########################   COORDENADAS AJUSTADAS   ###############################
                    XA = X0+DELTAX

                    #################################    ITERAÇÕES    ########################################
                    convergencia = confere_convergencia(DELTAX)
                    iteracoes=0
                    while convergencia == False:
                        iteracoes+=1
                        ############################   X01 PRÁTICO   ###########################
                        X01_pratico = []
                        Y01_pratico = []
                        X01_pratico.append(x_referencia_i)
                        X01_pratico.append(x_base_i)
                        Y01_pratico.append(y_referencia_i)
                        Y01_pratico.append(y_base_i)
                        k=0
                        for i in range(0,len(XA)):
                            if i%2==0:
                                X01_pratico.append(float(XA[i]))
                            else:
                                Y01_pratico.append(float(XA[i]))
                        X01_pratico.append(x_base_f)
                        X01_pratico.append(x_referencia_f)
                        Y01_pratico.append(y_base_f)
                        Y01_pratico.append(y_referencia_f)

                        ####################################   L01 = F(XA)   ##############################
                        L01=np.empty((len(L0),1), dtype=list)
                        j=0
                        for i in range (0, len(L0)):    
                            if i <= len(lista_sequencia_correta)-2:
                                L01[i][0] = float(distancia_i.subs({x_fd: X01_pratico[i+1], x1d: X01_pratico[i+2], y_fd: Y01_pratico[i+1], y1d: Y01_pratico[i+2]}).n())
                            else:
                                azimute_1 = Azimute(X01_pratico[j+1], Y01_pratico[j+1], X01_pratico[j], Y01_pratico[j])
                                azimute_2 = Azimute( X01_pratico[j+1], Y01_pratico[j+1], X01_pratico[j+2], Y01_pratico[j+2])
                                ang_az2_az1 = azimute_2 - azimute_1
                                if ang_az2_az1 < 0:
                                    ang_az2_az1 += 360
                                L01[i][0] = float(math.radians(ang_az2_az1))
                                j+=1 
                        
                        ###########################   MATRIZ DESING   ###########################
                        A2=[]
                        br=0
                        for i in range(0,len(eq)):
                            for j in range(0,len(par)):
                                if i <= len(lista_sequencia_correta)-2:
                                    A2.append(sympy.diff(eq[i],par[j]).subs({parametros_x[i+1]: X01_pratico[i+1], parametros_x[i+2]: X01_pratico[i+2], parametros_y[i+1]: Y01_pratico[i+1], parametros_y[i+2]: Y01_pratico[i+2]}).n())
                                else:
                                    A2.append(sympy.diff(eq[i],par[j]).subs({parametros_x[br+2]: X01_pratico[br+2], parametros_x[br+1]: X01_pratico[br+1], parametros_x[br]: X01_pratico[br], parametros_y[br+2]: Y01_pratico[br+2], parametros_y[br+1]: Y01_pratico[br+1], parametros_y[br]: Y01_pratico[br]}).n())
                                    if j == len(par)-1:
                                        br+=1
    
                        A22=np.empty((2*len(lista_sequencia_correta)-1, 2*len(lista_sequencia_correta)-4), dtype=float)
                        i2=0
                        for i in range(0, 2*len(lista_sequencia_correta)-1):
                            for j in range(0, 2*len(lista_sequencia_correta)-4):
                                A22[i][j]=float(A2[i2])
                                i2+=1                             
                        
                        #####################################   L1=Lb-L01   #########################################
                        L1=lb-L01
                        
                        ###########################   CORREÇÕES APROXIMADAS   #####################################
                        global DELTAX1, XA1
                        DELTAX1 = np.linalg.inv(np.transpose(A22)@P@A22)@np.transpose(A22)@P@L1
                        XA = XA + DELTAX1
                        convergencia = confere_convergencia(DELTAX1)
                    
                    if iteracoes != 0:
                        A = A22
                        DELTAX = DELTAX1
                        L = L1
                    
                    global V, SIGMA_QUADRADO, Cxy, CLB, Cv
                    ########################   RESÍDUOS DAS OBSERVAÇÕES   ###############################
                    V = (A@DELTAX) - L
                    
                    ###################   VARIANCIA DE REFERENCIA A POSTERIORI   ########################
                    GL = 3
                    SIGMA_QUADRADO = (np.transpose(V)@P@V)/GL
                
                    #########################   MCV A POSTERIORI DOS PARAMETROS   #######################
                    Cxy = SIGMA_QUADRADO * np.linalg.inv(np.transpose(A)@P@A)
                    diagonal_principal = []
                    for i in range(0,len(Cxy)):
                        for j in range(0, len(Cxy)):
                            if i == j:
                                diagonal_principal.append(Cxy[i][j])
                    
                    ########################   MCV A POSTERIORI DAS OBSERVAÇOES   #######################
                    CLB = SIGMA_QUADRADO * Clb
                    
                    ########################   MCV A POSTERIORI DOS RESIDUOS   ##########################
                    Cv = CLB - A @ Cxy @ np.transpose(A)
                    
                    ################################   ELIPSE DOS ERROS   ###############################
                    #elementos_elipses = np.empty((len(coordenadas_estacao)-2,6), dtype=list)
                    #for i in range
                    
                    
                    #M = math.sqrt()
                    
                    global coordenadas_ajustadas
                    coordenadas_ajustadas = np.empty((len(lista_sequencia_correta),2), dtype=float)
                    coordenadas_a = []
                    coordenadas_a.append(x_base_i)
                    coordenadas_a.append(y_base_i)
                    for i in XA:
                        coordenadas_a.append(i)
                    coordenadas_a.append(x_base_f)
                    coordenadas_a.append(y_base_f)
                    k1=0
                    for i in range(0, len(coordenadas_a),2):
                        coordenadas_ajustadas[k1][0] = coordenadas_a[i]
                        coordenadas_ajustadas[k1][1] = coordenadas_a[i+1]
                        k1+=1
                    
                    ###########################    Cria a matriz para impressao    ###################
                    matriz_impressao = np.empty((len(coordenadas_ajustadas), 5), dtype=list)
                    
                    global comprimento_pol_a
                    comprimento_pol_a=0
                    for i in range(0, len(lb)):
                        if i <= len(lista_sequencia_correta)-1:
                            comprimento_pol_a+=lb[i]
                    
                    matriz_impressao[0][0] = lista_sequencia_correta[0]
                    matriz_impressao[0][3] = var_x_0/1000
                    matriz_impressao[0][4] = var_y_0/1000
                    
                    matriz_impressao[-1][0] = lista_sequencia_correta[-1]
                    matriz_impressao[-1][3] = var_x_f/1000
                    matriz_impressao[-1][4] = var_y_f/1000
                    
                    kn=0
                    for i in range(0, len(coordenadas_ajustadas)):
                        matriz_impressao[i][0] = lista_sequencia_correta[i]
                        matriz_impressao[i][1] = coordenadas_ajustadas[i][0]
                        matriz_impressao[i][2] = coordenadas_ajustadas[i][1]
                        if i > 0 and i < len(coordenadas_ajustadas)-1:
                            matriz_impressao[i][3] = math.sqrt(diagonal_principal[kn])
                            matriz_impressao[i][4] = math.sqrt(diagonal_principal[kn+1])
                            kn+=2
                    
                    messagebox.showinfo(title="AJUSTAMENTO", message="Concluído!")
  
                else:
                    messagebox.showerror(title="ERRO", message="Ajustamento não realizado! Determinante da matriz At*P*A igual a zero")
                
            
            elif tipo_poligonal == "Fechada e apoiada em um só ponto":
                i=1
        
    else:
        messagebox.showerror(title="ERRO", message="Ajustamento não ativado")

################################   PROCESSAR POLIGONAL   ###############################
def Somatorio(a, b):
    soma = 0
    for j in range(0, a):
        soma += b[j]
    return soma

def processarPoligonal():
    global azimute_estacao, ang_h, dist, azimute_inicial, azimute_final, coordenadas_estacao
    ang_h = []
    dist = []
    azimute_estacao = []
    delx = []
    dely = []
    coordenadas_estacao = np.empty((len(estacao),3), dtype=list)
    
    ##########################    Calculo dos azimutes    #######################################
    azimute_inicial=Azimute(x_base_i, y_base_i, x_referencia_i, y_referencia_i)
    if tipo_poligonal == "Fechada e apoiada em pontos distintos":
        azimute_final=Azimute(x_base_f, y_base_f, x_referencia_f, y_referencia_f)
    
    ###############    Calculo do angulo horario entre cada re e vante    #######################
    for i in range (0, len(m)):
        if m[i][3] == "RE":
            for j in range(i, len(m)):
                if m[i][1] == m[j][1] and m[j][3] == "VANTE":
                    ang = ang_0_360(m[j][6]-m[i][6]) 
                    ang_h.append(ang)
                    
    ################    Calculo das distancias entre cada est e sua vante    ####################
    for i in range(0, len(m)): 
        if m[i][3] == "VANTE" and m[i][0] != id_referencia_f:
            for j in range(i, len(m)):
                if m[j][3] == "RE" and m[j][0] != id_referencia_i and m[j][0]== m[i][1]:
                    if m[i][7] != None and m[j][7] == None:
                        d = m[i][7]
                    elif m[i][7] == None and m[j][7] != None:
                        d = m[j][7]
                    elif m[i][7] != None and m[j][7] != None:
                        d = (m[i][7] + m[j][7])/2
                    else:
                        messagebox.showerror(title="Erro", message="Nao foi possivel encontrar a distancia entre os pontos!")
                        break
                    dist.append(d)
                    
    #####################    Calculo dos azimutes de cada alinhamento    ###########################
    for i in range (0, len(ang_h)):
        az = ang_0_360(azimute_inicial + Somatorio(i+1, ang_h) - (i*180))
        azimute_estacao.append(math.radians(az))
        
    if ajustamento_ativado == 0 and reducao_ativada == 0:
        global ea_processamento, tolerancia_a
        ##########################    Erro angular    ##############################################
        ea_processamento = (math.degrees(azimute_estacao[-1]) - azimute_final)*3600
        
        #############################    Tolerancia angular    ####################################
        tolerancia_a = (3*10*math.sqrt(len(lista_sequencia_correta)))+10
        
        ##############################    Correção angular    ######################################
        correcao_ea_processamento = (ea_processamento/3600)/len(azimute_estacao)
        for i in range(0, len(azimute_estacao)):
            azimute_estacao[i] = azimute_estacao[i] + (math.radians(-correcao_ea_processamento*(i+1)))
        
    ########################    Calculo das componentes vetoriais    ###############################
    for i in range (0, len(dist)):
        delx.append(dist[i] * math.sin(azimute_estacao[i]))
        dely.append(dist[i] * math.cos(azimute_estacao[i]))
    
    ########################    Adiciona as coordenadas do primeiro ponto    #######################
    coordenadas_estacao[0][0]=lista_sequencia_correta[0]
    coordenadas_estacao[0][1]=x_base_i
    coordenadas_estacao[0][2]=y_base_i
    
    #####################    Calculo das coordenadas de cada ponto da poligonal    ################
    for i in range (1, len(lista_sequencia_correta)):
        coordenadas_estacao[i][0]=lista_sequencia_correta[i]
        coordenadas_estacao[i][1]=x_base_i + Somatorio(i, delx)
        coordenadas_estacao[i][2]=y_base_i + Somatorio(i, dely)
        
    #######################    Calculo do erro de fechamento linear    #############################
    if ajustamento_ativado==0 and reducao_ativada==0:
        global elx_processamento, ely_processamento, el_processamento, comprimento_pol_processamento, erro_f_long, erro_f_trans, erro_linear
        elx_processamento = coordenadas_estacao[-1][1] - x_base_f
        ely_processamento = coordenadas_estacao[-1][2] - y_base_f
        el_processamento = math.sqrt(elx_processamento**2+ely_processamento**2)
        comprimento_pol_processamento = sum(dist)
        erro_linear = "1/{}".format(int(round(comprimento_pol_processamento/el_processamento,0)))
        
        
        ###########################    Erro de fechamento Longitudinal    ###########################
        dist_total = math.sqrt((x_base_f-x_base_i)**2+(y_base_f-y_base_i)**2)
        erro_f_long = (elx_processamento*(x_base_f-x_base_i)+ely_processamento*(y_base_f-y_base_i))/dist_total
        
        ###########################    Erro de fechamento Transversal    ############################
        erro_f_trans = (ely_processamento*(x_base_f-x_base_i)+elx_processamento*(y_base_f-y_base_i))/dist_total
        
        #####################################    Correções    #######################################
        correcao_elx_processamento = -elx_processamento/comprimento_pol_processamento
        correcao_ely_processamento = -ely_processamento/comprimento_pol_processamento
    
        def soma_L_processamento(matriz,i):
            soma_dist = 0
            for j in range(0,i):
                soma_dist = soma_dist + matriz[j]
            return soma_dist
            
        for i in range(0, len(coordenadas_estacao)-1):
            coordenadas_estacao[i+1][1]=coordenadas_estacao[i+1][1] + correcao_elx_processamento*soma_L_processamento(dist,i+1)
            coordenadas_estacao[i+1][2]=coordenadas_estacao[i+1][2] + correcao_ely_processamento*soma_L_processamento(dist,i+1)
        
    messagebox.showinfo(title="Processamento", message="CONCLUÍDO!")

################################   PROCESSAR IRRADIAÇÕES   ############################# 
def Calc_irr(i, irr): 
    delta_x = irr[i][4] * math.sin(irr[i][3])
    delta_y = irr[i][4] * math.cos(irr[i][3])
    return delta_x, delta_y

def processarIrradiacoes():
    
    
    """Encontra o numero de irradiacoes e cria uma matriz no tamanho certo
       para armazenar todas irradiações"""
       
    global irrad, dados_irr
    irrad = 0
    for i in range(0, len(m)):
        if m[i][3] == "IRRADIACAO":
            irrad += 1
    irr = np.empty((irrad,5), dtype=list)
    
    ###    Calculo dos angulos horarios das irradiações e suas distancias    ##
    nu=0
    for i in range(0, len(m)):
        if m[i][3] == "RE":
            for k in range(i, len(m)):
                if m[k][3] == "IRRADIACAO" and m[k][1] == m[i][1]:
                    irr[nu][0] = m[k][0]
                    irr[nu][1] = m[k][1]
                    irr[nu][2] = m[k][8]
                    irr[nu][3] = math.radians(m[k][6] - m[i][6])
                    irr[nu][4] = m[k][7]
                    nu+=1
                else: continue
        else: continue
    
    ####    Matriz para armazenar as componentes vetoriais e seus dados    ####
    dados_irr = np.empty((irrad, 26), dtype=list)
    
    #######################    Calculo dos azimutes    ########################
    az_re = np.empty((len(estacao),2), dtype=list)
    for i in range (0, len(estacao)):
        az_re[i][0] = estacao[i]
        az_re[i][1] = azimute_estacao[i]-math.radians(ang_h[i])
    for i in range(0, len(az_re)):
        for j in range(0, len(irr)):
            if az_re[i][1] == irr[j][1]:
                irr[j][3] = irr[j][3] + az_re[i][1]
    for i in range (0, len(irr)): 
        x, y = Calc_irr(i, irr)
        dados_irr[i][0] = irr[i][0]
        dados_irr[i][1] = irr[i][1]
        dados_irr[i][2] = irr[i][2]
        dados_irr[i][3] = x
        dados_irr[i][4] = y
        dados_irr[i][24] = irr[i][4]
        dados_irr[i][25] = irr[i][3]
        
    for j in range (0, len(estacao)):
        for i in range (0, len(dados_irr)):
            if estacao[j] == dados_irr[i][1]:
                if ajustamento_ativado==0 and reducao_ativada==0 or ajustamento_ativado==1 and reducao_ativada==0 and tipo_ajustamento == "NBR-13.133 (Método Simplificado)":
                    dados_irr[i][5] = coordenadas_estacao[j][1] + dados_irr[i][3]
                    dados_irr[i][6] = coordenadas_estacao[j][2] + dados_irr[i][4]
                    dados_irr[i][22] = coordenadas_estacao[j][1]
                    dados_irr[i][23] = coordenadas_estacao[j][2]
                    
                elif ajustamento_ativado==0 and reducao_ativada==1 or ajustamento_ativado==1 and reducao_ativada==1:
                    dados_irr[i][5] = matriz_reducao[i][4] + dados_irr[i][3]
                    dados_irr[i][6] = matriz_reducao[i][5] + dados_irr[i][4]
                    dados_irr[i][22] = matriz_reducao[i][4]
                    dados_irr[i][23] = matriz_reducao[i][5]
                    
                elif ajustamento_ativado==1 and reducao_ativada==0:
                    if tipo_ajustamento == "Método Paramétrico":
                        dados_irr[i][5] = coordenadas_ajustadas[j][0] + dados_irr[i][3]
                        dados_irr[i][6] = coordenadas_ajustadas[j][1] + dados_irr[i][4]
                        dados_irr[i][22] = coordenadas_ajustadas[j][0]
                        dados_irr[i][23] = coordenadas_ajustadas[j][1]
                        
    messagebox.showinfo(title="Processamento", message="CONCLUÍDO!")

################################   PROPAGAR VARIANCIAS IRR   ###############################
def propagarVariancias():
    if propag_ativada == 1:
        if tipo_propag == "NBR-13.133(Método Simplificado)":
            n=0
            for i in range (0, len(m)):
                if m[i][3] == "ESTACAO":
                    for j in range (0, len(m)):
                        if m[j][3] == "RE" and m[j][1] == m[i][1]:
                            for k in range (0, len(m)):
                                if m[k][3] == "IRRADIACAO" and m[k][1] == m[i][1]:
                                    Ei=1*m[k][2] #mm
                                    Er=2.3*m[k][9] #mm
                                    PNlin=precisao_linear+ppm*m[k][7]*1000 #mm
                                    var_DI=math.sqrt(Ei**2+Er**2+PNlin**2) #mm
                                    var_z=math.sqrt(2*precisao_angular**2+precisao_compensador**2) #"
                                    var_DH=math.sqrt((math.sin(math.radians(m[k][5])))**2*var_DI**2+(m[k][4]*math.cos(math.radians(m[k][5])))**2*(var_z*math.pi/648000)**2) #mm
                                    var_n=math.sqrt(precisao_compensador**2*((1/math.tan(math.radians(m[j][5])))**2+(1/math.tan(math.radians(m[k][5])))**2)) #"
                                    DHpv_re = math.sqrt(m[j][7]**2+m[k][7]**2-2*m[j][7]*m[k][7]*math.cos(Graus_Rad(m[k][6]-m[j][6]))) #m
                                    var_c=math.sqrt(((Er/1000)/(m[j][7]*m[k][7]))**2*(m[j][7]**2+m[k][7]**2)+((Ei/1000)/(m[j][7]*m[k][7]))**2*(DHpv_re/2))*648000/math.pi #"
                                    var_i=math.sqrt(4*precisao_angular**2+var_n**2/2+var_c**2) #"
                                    if m[i][1] == resultados_ajust[0][0]:
                                        var_az_re=math.sqrt(((y_referencia_i-ypol[0])/m[j][7]**2)**2*((var_x_re/1000)**2+(var_x_0/1000)**2)+((x_referencia_i-xpol[0])/m[j][7]**2)**2*((var_y_re/1000)**2+(var_y_0/1000)**2))*648000/math.pi #"
                                    else:
                                        for p in range(0,len(resultados_ajust)):
                                            if m[i][1]==resultados_ajust[p][0]:
                                                var_az_re=math.sqrt(((resultados_ajust[p-1][2]-resultados_ajust[p][2])/m[j][7]**2)**2*((resultados_ajust[p-1][14]/1000)**2+(resultados_ajust[p][14]/1000)**2)+((resultados_ajust[p-1][1]-resultados_ajust[p][1])/m[j][7]**2)**2*((resultados_ajust[p-1][15]/1000)**2+(resultados_ajust[p][15]/1000)**2))*648000/math.pi
                                    var_az=math.sqrt(var_az_re**2+var_i**2) #"
                                    for l in range(0, len(lista_sequencia_correta)):
                                        if lista_sequencia_correta[l]==m[i][1]:
                                            for t in range(0, len(resultados_ajust)):
                                                if resultados_ajust[t][0] == m[i][1]:
                                                    var_x=math.sqrt(resultados_ajust[t][14]**2+(math.sin(azmt_est[l]))**2*var_DH**2+(m[k][7]*1000*math.cos(azmt_est[l]))**2*(var_az*math.pi/648000)**2) #mm
                                                    var_y=math.sqrt(resultados_ajust[t][15]**2+(math.cos(azmt_est[l]))**2*var_DH**2+(m[k][7]*1000*math.sin(azmt_est[l]))**2*(var_az*math.pi/648000)**2) #mm
                                                    co_var_x_y=math.sin(azmt_est[l])*math.cos(azmt_est[l])*var_DH**2-(m[k][7]*1000)**2*math.sin(azmt_est[l])*math.cos(azmt_est[l])*(var_az*math.pi/648000)**2
                                    var_2d=math.sqrt(var_x**2+var_y**2)
                                    
                                    dados_irr[n][7]=Ei
                                    dados_irr[n][8]=Er
                                    dados_irr[n][9]=PNlin
                                    dados_irr[n][10]=var_DI
                                    dados_irr[n][11]=var_z
                                    dados_irr[n][12]=var_DH
                                    dados_irr[n][13]=var_n
                                    dados_irr[n][14]=var_c
                                    dados_irr[n][15]=var_i
                                    dados_irr[n][16]=var_az_re
                                    dados_irr[n][17]=var_az
                                    dados_irr[n][18]=var_x
                                    dados_irr[n][19]=var_y
                                    dados_irr[n][20]=co_var_x_y
                                    dados_irr[n][21]=var_2d
                                    n+=1                
        
        elif tipo_propag == "Teoria dos erros (Método Completo)":
            global var_irr
            var_irr = np.empty((irrad, 3), dtype=list)
            
            for i in range (0, len(dados_irr)):
                var_irr[i][0] = dados_irr[i][0]
                var_irr[i][1] = math.sqrt(precisao_linear**2+(ppm*dados_irr[i][24]/1000)**2)/1000
            
            h=0
            for i in range (0, len(m)):
                if m[i][3] == "ESTACAO":
                    for j in range (0, len(m)):
                        if m[j][3] == "RE" and m[j][1] == m[i][1]:
                            for k in range (0, len(m)):
                                if m[k][3] == "IRRADIACAO" and m[k][1] == m[i][1]:
                                    Ei=1*m[k][2] #mm
                                    Er=2.3*m[k][9] #mm
                                    PNlin=precisao_linear+ppm*m[k][7]*1000 #mm
                                    var_DI=math.sqrt(Ei**2+Er**2+PNlin**2) #mm
                                    var_z=math.sqrt(2*precisao_angular**2+precisao_compensador**2) #"
                                    var_n=math.sqrt(precisao_compensador**2*((1/math.tan(math.radians(m[j][5])))**2+(1/math.tan(math.radians(m[k][5])))**2)) #"
                                    DHpv_re = math.sqrt(m[j][7]**2+m[k][7]**2-2*m[j][7]*m[k][7]*math.cos(Graus_Rad(m[k][6]-m[j][6]))) #m
                                    var_c=math.sqrt(((Er/1000)/(m[j][7]*m[k][7]))**2*(m[j][7]**2+m[k][7]**2)+((Ei/1000)/(m[j][7]*m[k][7]))**2*(DHpv_re/2))*648000/math.pi #"
                                    var_i=math.sqrt(4*precisao_angular**2+var_n**2/2+var_c**2) #"
                                    if m[i][1] == resultados_ajust_ida[0][0]:
                                        var_az_re=math.sqrt(((y_referencia_i-y_base_i)/m[j][7]**2)**2*((var_x_re/1000)**2+(var_x_0/1000)**2)+((x_referencia_i-x_base_i)/m[j][7]**2)**2*((var_y_re/1000)**2+(var_y_0/1000)**2))*648000/math.pi #"
                                    else:
                                        for p in range(0,len(resultados_ajust_ida)):
                                            if m[i][1]==resultados_ajust_ida[p][0]:
                                                var_az_re=math.sqrt(((resultados_ajust_ida[p-1][2]-resultados_ajust_ida[p][2])/m[j][7]**2)**2*((resultados_ajust_ida[p-1][14]/1000)**2+(resultados_ajust_ida[p][14]/1000)**2)+((resultados_ajust_ida[p-1][1]-resultados_ajust_ida[p][1])/m[j][7]**2)**2*((resultados_ajust_ida[p-1][15]/1000)**2+(resultados_ajust_ida[p][15]/1000)**2))*648000/math.pi

                                    var_irr[h][2]=math.sqrt(var_az_re**2+var_i**2)
                                    h+=1
            
            ##############################    Matriz dos resultados    #########################################
            global var_irradiacoes
            var_irradiacoes = np.empty((irrad, 3), dtype=float)
            
            ##########################    Definindo matrizes para a propagação    ###############################
            xa, ya, d, az = sympy.symbols("xa ya d az")
            x = xa+d*sympy.sin(az)
            y = ya+d*sympy.cos(az)
            parametros_deriv = [xa, ya, d, az]
            
            for i in range (0, irrad):
                ################################    Matriz Jacobiana    ############################################
                jacobiana = np.empty((2,4), dtype=float)
                for ik in range(0, 2):
                    for j in range(0,4):
                        if ik == 0:
                            jacobiana[ik][j] = float(sympy.diff(x, parametros_deriv[j]).subs({parametros_deriv[0]: dados_irr[i][22], parametros_deriv[1]: dados_irr[i][23], parametros_deriv[2]: dados_irr[i][24], parametros_deriv[3]: dados_irr[i][25]}).n())
                        else:
                            jacobiana[ik][j] = float(sympy.diff(y, parametros_deriv[j]).subs({parametros_deriv[0]: dados_irr[i][22], parametros_deriv[1]: dados_irr[i][23], parametros_deriv[2]: dados_irr[i][24], parametros_deriv[3]: dados_irr[i][25]}).n())
                
                #####################################    MVC    ##################################################
                lista_cl = []
                
                if ajustamento_ativado == 1 and tipo_ajustamento == "Método Paramétrico":
                    for k in range(0, len(matriz_impressao)):
                        if dados_irr[i][1] == matriz_impressao[k][0]:
                            lista_cl.append(matriz_impressao[k][3])
                            lista_cl.append(matriz_impressao[k][4])
                   
                elif ajustamento_ativado == 1 and tipo_ajustamento == "NBR-13.133 (Método Simplificado)":
                    for k in range(0, len(matriz_impressao)):
                        if dados_irr[i][1] == matriz_impressao[k][0]:
                            lista_cl.append(matriz_impressao[k][3])
                            lista_cl.append(matriz_impressao[k][4])
                    
                lista_cl.append(var_irr[i][1]**2)
                lista_cl.append(math.radians(var_irr[i][2]/3600)**2)           

                cl = np.diagflat(lista_cl)

                var_xy = jacobiana@cl@np.transpose(jacobiana)
                
                var_irradiacoes[i][1] = var_xy[0][0]
                var_irradiacoes[i][2] = var_xy[1][1]

        messagebox.showinfo(title="Propagação", message="CONCLUÍDA!")
        
    elif propag_ativada == 0:
        messagebox.showerror(title="Propagação", message="PROPAGAÇÃO NÃO ATIVADA!")
        
###############################   REDUÇÕES PARA O PLANO DE PROJEÇÃO   ##################
def reducaoPol():
    if reducao_ativada == 1:
        
        ####################   REDUZ PARA O PLANO TOPOGRÁFICO LOCAL   ##################
        if tipo_reducao == "Plano Topográfico Local":
            numero=1
            
        ########################   REDUZ PARA O PLANO UTM   ############################
        elif tipo_reducao == "Plano UTM":
            """ Essa parte do código realiza a redução das observações para o 
            plano de projeção UNIVERSAL TRANSVERSO DE MERCATOR"""
            
            ######################    Parametros dos elipsoides    #########################
            if elipsoide == "Hayford (Córrego Alegre)":
                a_=6378388
                b=6356911.94612794
                e2=(a_**2-b**2)/a_**2
                e_linha_2=(a_**2-b**2)/b**2
                
            elif elipsoide == "GRS 67 (SAD 69)":
                a_=6378160
                b=6356774.719
                e2=(a_**2-b**2)/a_**2
                e_linha_2=(a_**2-b**2)/b**2
                
            elif elipsoide == "GRS 1980 (SIRGAS 2000)":
                a_=6378137
                b=6356752.314140347
                e2=(a_**2-b**2)/a_**2
                e_linha_2=(a_**2-b**2)/b**2
                
            elif elipsoide == "WGS 1984 (GPS)":
                a_=6378137
                b=6356752.31424518
                e2=(a_**2-b**2)/a_**2
                e_linha_2=(a_**2-b**2)/b**2            
    
            k0_=0.9996
            
            ###################    Cálculo das distancias e angulos horizontais horarios   #####################
            global matriz_reducao
            matriz_reducao=np.empty((len(lista_sequencia_correta),20), dtype=list)
            a=0
            matriz_reducao[a][4]=x_base_i
            matriz_reducao[a][5]=y_base_i
            for i in range (0, len(m)):
                if m[i][3]=="ESTACAO":
                    for j in range(0, len(m)):
                        if m[j][3]=="RE" and m[j][1]==m[i][1]:
                            for k in range(0, len(m)):
                                if m[k][3]=="VANTE" and m[k][1]==m[i][1]:
                                    matriz_reducao[a][0]=m[i][1]
                                    matriz_reducao[a][1]=ang_0_360(m[k][6]-m[j][6])
                                    matriz_reducao[a][2]=m[k][7]
                                    a+=1
                
###############################   DEFINE A TRANSFORMAÇÃO DE COORDENADAS   ##############################
########################################    GRS 80   ###################################################
            if fuso == 1 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=1 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 2 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=2 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 3 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=3 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 4 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=4 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 5 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=5 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 6 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=6 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 7 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=7 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 8 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=8 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 9 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=9 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 10 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=10 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 11 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=11 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 12 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=12 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 13 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=13 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 14 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=14 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 15 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=15 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 16 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=16 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 17 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=17 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 18 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=18 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 19 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=19 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 20 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=20 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 21 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=21 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 22 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=22 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 23 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=23 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 24 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=24 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 25 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=25 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 26 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=26 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 27 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=27 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 28 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=28 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 29 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=29 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 30 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=30 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 31 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=31 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 32 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=32 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 33 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=33 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 34 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=34 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 35 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=35 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 36 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=36 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 37 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=37 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 38 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=38 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 39 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=39 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 40 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=40 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 41 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=41 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 42 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=42 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 43 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=43 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 44 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=44 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 45 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=45 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 46 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=46 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 47 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=47 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 48 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=48 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 49 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=49 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 50 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=50 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 51 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=51 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 52 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=52 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 53 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=53 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 54 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=54 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 55 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=55 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 56 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=56 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 57 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=57 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 58 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=58 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 59 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=59 +ellps=GRS80 +south', preserve_units=False)
                
            elif fuso == 60 and elipsoide == "GRS 1980 (SIRGAS 2000)" and hemisferio == "Sul":                
                p=Proj('+proj=utm zone=60 +ellps=GRS80 +south', preserve_units=False)
                
#######################################   WGS 84   ###########################################################
            elif fuso == 1 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=1 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 2 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=2 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 3 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=3 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 4 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=4 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 5 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=5 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 6 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=6 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 7 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=7 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 8 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=8 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 9 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=9 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 10 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=10 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 11 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=11 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 12 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=12 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 13 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=13 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 14 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=14 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 15 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=15 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 16 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=16 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 17 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=17 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 18 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=18 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 19 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=19 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 20 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=20 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 21 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=21 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 22 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=22 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 23 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=23 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 24 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=24 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 25 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=25 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 26 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=26 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 27 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=27 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 28 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=28 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 29 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=29 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 30 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=30 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 31 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=31 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 32 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=32 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 33 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=33 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 34 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=34 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 35 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=35 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 36 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=36 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 37 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=37 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 38 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=38 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 39 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=39 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 40 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=40 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 41 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=41+ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 42 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=42+ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 43 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=43 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 44 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=44 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 45 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=45 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 46 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=46 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 47 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=47 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 48 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=48 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 49 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=49 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 50 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=50 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 51 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=51 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 52 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=52 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 53 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=53 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 54 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=54 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 55 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=55 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 56 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=56 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 57 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=57 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 58 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=58 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 59 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":
                p=Proj('+proj=utm zone=59 +ellps=WGS84 +south', preserve_units=False)
                
            elif fuso == 60 and elipsoide == "WGS 1984 (GPS)" and hemisferio == "Sul":                
                p=Proj('+proj=utm zone=60 +ellps=WGS84 +south', preserve_units=False)
                
            #############################   Calculo da altitude média e do Raio Médio   ############################
            if tipo_poligonal=="Fechada e apoiada em pontos distintos":
                h_medio=(z_base_i+z_base_f+z_referencia_i+z_referencia_f)/4
                lambda_pi, fi_pi = p(x_base_i, y_base_i, inverse=True)
                lambda_pf, fi_pf = p(x_base_f , y_base_f, inverse=True)
                lambda_referencia_i, fi_referencia_i = p(x_referencia_i , y_referencia_i, inverse=True)
                fi_medio_rad=math.radians(fi_pi+(fi_pf-fi_pi)/2)
                M=a_*(1-e2)/(1-e2*(math.sin(fi_medio_rad))**2)**(3/2)
                N=a_/math.sqrt(1-e2*(math.sin(fi_medio_rad))**2)
                Rm_provisorio=math.sqrt(M*N)
            else:
                h_medio=(z_base_i+z_referencia_i)/2
            
            ####################################    TRANSPORTE DE AZIMUTES    ######################################
            def Somatorio2(a,b):
                soma = 0
                for j in range(0, a):
                    soma += b[j][1]
                return soma
            
            ####################################    Longitude do Meridiano Central    ###############################
            if fuso < 30:
                lambda_MC=-180+((fuso-1)*6+3)
            
            ################################    Convergencia Meridiana na primeira estação    #######################
            convergencia_meridiana_i = math.degrees(math.radians(lambda_pi-lambda_MC)*math.sin(math.radians(fi_pi)))

            ###############################    Redução angular na primeira estação    ################################
            E_linha_1_i = x_base_i-500000
            E_linha_2_i = x_referencia_i-500000
            XVIII_i=(10**12)/(2*N*M*k0_**2)            
            red_ang_i=6.8755*10**(-8)*( y_referencia_i - y_base_i )*(2*E_linha_2_i+E_linha_1_i)*XVIII_i
            
            #####################################    Azimute inicial corrigido    ####################################
            azimute_inicial_corrigido = azimute_inicial+convergencia_meridiana_i+red_ang_i/3600
            
            """  Essa parte do código calcula os azimutes geográficos de cada 
                alinhamento e os adiciona na matriz redução. Essa matriz será 
                utilizada quando não há a necessidade de se distribuir as 
                variações angulares"""
            
            for i in range (0, len(matriz_reducao)):
                az = azimute_inicial_corrigido + Somatorio2(i+1, matriz_reducao) - (i*180)
                while az < 0:
                    az += 360
                while az > 360:
                    az -= 360
                matriz_reducao[i][3]=az
            
            ########################################    Erro angular    ############################################
            if ajustamento_ativado==0:
                
                """Se o ajustamento estiver desativado se faz a distribuição 
                    de erro de fechamento angular para as coordenadas. Nesse 'if' 
                    os azimutes geodesicos são recalculados de forma a se distribuir
                    o erro de fechamento angular igualmente entre todos os 
                    angulos observados."""
                    
                ##################################    Convergencia Meridiana na ultima estação    ########################
                convergencia_meridiana_f = math.degrees(math.radians(lambda_pf-lambda_MC)*math.sin(math.radians(fi_pf)))
                
                ###############################    Redução angular na última estação    #################################
                E_linha_1_f = x_base_f-500000
                E_linha_2_f = x_referencia_f-500000
                XVIII_f=(10**12)/(2*N*M*k0_**2)            
                red_ang_f=6.8755*10**(-8)*( y_referencia_f - y_base_f )*(2*E_linha_2_f+E_linha_1_f)*XVIII_f
                
                #####################################    Azimute final corrigido    ####################################
                azimute_final_geodesico_calculado = azimute_final+convergencia_meridiana_f+red_ang_f/3600
                
                ####################################     Erro Angular    ###############################################
                global tolerancia_a_r, ea_reducao
                ea_reducao = (azimute_final_geodesico_calculado-matriz_reducao[-1][3])*3600
                
                #############################    Tolerancia angular    ####################################
                tolerancia_a_r = (3*10*math.sqrt(len(lista_sequencia_correta)))+10
                
                ##################################    Correção dos azimutes    #########################################
                correcao_ea_reducao = (ea_reducao/3600)/len(matriz_reducao)
                for i in range(0, len(matriz_reducao)):
                    matriz_reducao[i][3] = matriz_reducao[i][3] + (-correcao_ea_reducao*(i+1))
                    
            #############################    Calculos das coordenadas UTM    #########################
            for i in range(0,len(matriz_reducao)-1):
                
                #####################    Coeficiente de redução linear m1    #########################
                m1= Rm_provisorio/(h_medio+Rm_provisorio)
                matriz_reducao[i][6]=m1
                
                ##############################     Distancia Provisória     ##########################
                de_1_2=matriz_reducao[i][2]*m1
                matriz_reducao[i][7]=de_1_2
                                    
                #################### Convergencia meridiana a partir das coord UTM ###################
                lambda_p, fi_p = p(matriz_reducao[i][4],matriz_reducao[i][5], inverse=True)
                fi_p_rad=math.radians(fi_p)
                ELINHA=abs(500000-matriz_reducao[i][4])
                q=10**(-6)*ELINHA
                XV=(math.tan(fi_p_rad)*10**6)/(N*math.sin(math.radians(1/3600))*k0_)
                XVI=math.tan(fi_p_rad)*10**18*(1+(math.tan(fi_p_rad))**2-e2*(math.cos(fi_p_rad))**2-2*e2**2*(math.cos(fi_p_rad))**4)/(3*N**3*math.sin(math.radians(1/3600))*k0_**3)
                F=math.tan(fi_p_rad)*10**30*(2+5*(math.tan(fi_p_rad))**2+3*(math.tan(fi_p_rad))**4)/(15*N**5*math.sin(math.radians(1/3600))*k0_**5)
                conv_meri_plana=XV*q-XVI*q**3+F*q**5
                matriz_reducao[i][8]=conv_meri_plana               
                
                ###########################    AZIMUTE PROVISÓRIO   #################################
                az_prov=matriz_reducao[i][3]-conv_meri_plana/3600
                matriz_reducao[i][9]=az_prov
                
                ###########################   COORDENADAS PROVISÓRIAS   #############################
                E_prov=matriz_reducao[i][4]+de_1_2*math.sin(math.radians(az_prov))
                N_prov=matriz_reducao[i][5]+de_1_2*math.cos(math.radians(az_prov))
    
                ###########################   ENCONTRANDO O PONTO MÉDIO   ###########################
                lambda_prov, fi_prov=p(E_prov, N_prov, inverse=True)               
                lambda_medio=lambda_p+(lambda_prov-lambda_p)/2
                lambda_medio_rad=math.radians(lambda_medio)
                fi_medio=fi_p+(fi_prov-fi_p)/2
                fi_medio_rad=math.radians(fi_medio)
                
                Mm=a_*(1-e2)/(1-e2*(math.sin(fi_medio_rad))**2)**(3/2)
                Nm=a_/math.sqrt(1-e2*(math.sin(fi_medio_rad))**2)
                matriz_reducao[i][19]=Mm
                
                ###########################   Coeficiente k   #######################################
                if fuso < 30:
                    lambda_MC_rad=math.radians(-180+((fuso-1)*6+3))
                coe_k=k0_/math.sqrt(1-(math.cos(fi_medio_rad)*math.sin(lambda_medio_rad-lambda_MC_rad))**2)
                matriz_reducao[i][10]=coe_k
                
                ############################   DISTANCIA UTM   ######################################
                dutm=matriz_reducao[i][7]*coe_k
                matriz_reducao[i][11]=dutm
                
                ############################ REDUCAO ANGULAR   ######################################
                E_linha_1=matriz_reducao[i][4]-500000
                E_linha_2=E_prov-500000
                XVIII=(10**12)/(2*Nm*Mm*k0_**2)            
                red_ang_1_2=6.8755*10**(-8)*(N_prov-matriz_reducao[i][5])*(2*E_linha_2+E_linha_1)*XVIII
                matriz_reducao[i][12]=red_ang_1_2
                
                ############################   AZIMUTE PLANO   #######################################
                azutm=matriz_reducao[i][3]-conv_meri_plana/3600-red_ang_1_2/3600
                matriz_reducao[i][13]=azutm
    
                #########################    COORDENADAS DEFINITIVAS    ##############################
                Eutm=matriz_reducao[i][4]+dutm*math.sin(math.radians(azutm))
                Nutm=matriz_reducao[i][5]+dutm*math.cos(math.radians(azutm))
                matriz_reducao[i+1][4]=Eutm
                matriz_reducao[i+1][5]=Nutm
            
            ###########################    Distribuição de erro Linear    ############################
            if ajustamento_ativado==0:
            
                """ Se o ajustamento estiver desativado, ao final do processo de
                    redução das observações para o plano UTM faz-se a distribuição
                    do erro linear. """
                    
                global elx_reducao, ely_reducao, el_reducao, erro_linear_r, erro_f_long_r, erro_f_trans_r, comprimento_pol
                
                elx_reducao = matriz_reducao[-1][4] - x_base_f
                ely_reducao = matriz_reducao[-1][5] - y_base_f
                el_reducao = math.sqrt(elx_reducao**2+ely_reducao**2)
                
                ##########################    Comprimento da poligonal reduzida    ######################
                comprimento_pol=0
                for i in range(0, len(matriz_reducao)-1):
                    comprimento_pol+=matriz_reducao[i][11]

                ###########################    Erro linear    ###########################################
                erro_linear_r = "1/{}".format(int(round(comprimento_pol/el_reducao,0)))
                
                ###########################    Erro de fechamento Longitudinal    ###########################
                dist_total = math.sqrt((x_base_f-x_base_i)**2+(y_base_f-y_base_i)**2)
                erro_f_long_r = (elx_reducao*(x_base_f-x_base_i)+ely_reducao*(y_base_f-y_base_i))/dist_total
                
                ###########################    Erro de fechamento Transversal    ############################
                erro_f_trans_r = (ely_reducao*(x_base_f-x_base_i)+elx_reducao*(y_base_f-y_base_i))/dist_total

                """ Essa parte do código aplica o método de Bowditch para a 
                    distribuição do erro linear de forma proporcional a distancia
                    de cada alinhamento."""
                
                correcao_elx_reducao = -elx_reducao/comprimento_pol
                correcao_ely_reducao = -ely_reducao/comprimento_pol
            
                def soma_L(matriz,i):
                    soma_dist = 0
                    for j in range(0,i):
                        soma_dist = soma_dist + matriz[j][11]
                    return soma_dist
                    
                for i in range(0, len(matriz_reducao)-1):
                    matriz_reducao[i+1][4] = matriz_reducao[i+1][4] + correcao_elx_reducao*soma_L(matriz_reducao,i+1)
                    matriz_reducao[i+1][5] = matriz_reducao[i+1][5] + correcao_ely_reducao*soma_L(matriz_reducao,i+1)
            
            messagebox.showinfo(title="REDUÇÕES", message="CONCUÍDAS!")
    else:
        messagebox.showerror(title="ERRO", message="Redução não ativada!")

def reduzirIrr():
    
    
    
    messagebox.showinfo(title="REDUÇÕES", message="CONCUÍDAS!")

###################################   RELATORIO   #####################################
def gerarRelatorio():
    def criar_cabecalho1(canvas, doc):
        styles = getSampleStyleSheet()
        header = Paragraph("Relatório Estatístico - Poligonal", styles['Heading1'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, 175, doc.height + doc.topMargin - h)
    
    def criar_cabecalho2(canvas, doc):
        styles = getSampleStyleSheet()
        header = Paragraph("Relatório Estatístico - Poligonal reduzida", styles['Heading1'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, 175, doc.height + doc.topMargin - h)
    
    def criar_cabecalho3(canvas, doc):
        styles = getSampleStyleSheet()
        header = Paragraph("Relatório Estatístico - Poligonal ajustada", styles['Heading1'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, 175, doc.height + doc.topMargin - h)
    
    def gera(a,b,c,d,e,f,g):
        ############################    Cria o arquivo PDF    ##########################
        nome_jan = asksaveasfilename(defaultextension= ".pdf", initialdir = "/",title = "Salvar",filetypes = (("PDF","*.pdf"),("all files","*.*")))
        doc = SimpleDocTemplate(nome_jan, pagesize=A4, topMargin=100)

        ############    Coordenadas processadas, reduzidas e ajustadas    ##############
        imprimir_v_cp = int(a.get())
        imprimir_v_cr = int(b.get())
        imprimir_v_ca = int(c.get())
        
        ###############    Coordenadas da poligonal e das irradiações    ###############    
        imprimir_v_cpol = int(d.get())
        imprimir_v_cirr = int(e.get())
        
        ##############    Precisões das coordenadas e dados do ajustamento    ##########
        imprimir_v_pre = int(f.get())
        imprimir_v_aju = int(g.get())
        
        global conteudo
        conteudo = []
        ####################    Imprime coordenadas processadas    #####################
        if imprimir_v_cp == 1 and imprimir_v_cr == 0 and imprimir_v_ca == 0:
            
            texto_1 = "Erro linear em X: {} m".format(round(elx_processamento,3))
            texto_2 = "Erro linear em Y: {} m".format(round(ely_processamento,3))
            texto_3 = "Erro linear: {} m".format(round(el_processamento,3))
            texto_4 = erro_linear
            texto_5 = "Erro longitudinal: {} m".format(round(erro_f_long,3))
            texto_6 = "Erro transversal: {} m".format(round(erro_f_trans,3))
            texto_7 = 'Erro angular: {} "'.format(round(ea_processamento, 1))
            texto_8 = 'Tolerancia angular: {} "'.format(round(tolerancia_a,1))
            texto_9 = "Número de estações: {} estações".format(len(lista_sequencia_correta))
            texto_10 = "Comprimento da poligonal: {} m".format(round(comprimento_pol_processamento))
            
            linhas_de_texto=[texto_1, texto_2, texto_3, texto_4, texto_5, texto_6, texto_7, texto_8, texto_9, texto_10]
            
            # Criar uma lista de objetos Paragraph para cada linha de texto
            styles = getSampleStyleSheet()
            for linha in linhas_de_texto:
                paragrafo = Paragraph(linha, style=styles['Normal'])
                conteudo.append(paragrafo)
            
            ###################    Cria a planilha para impressão    ###################
            planilha1=[]
            cab=[]
            cab.append("ID")
            cab.append("X (m)")
            cab.append("Y (m)")
            planilha1.append(cab)
            
            for i in range(0, len(coordenadas_estacao)):
                lista_aux=[]
                for j in range(0, 3):
                    if j==0:
                        lista_aux.append(coordenadas_estacao[i][j])
                    else:
                        lista_aux.append(str(round(coordenadas_estacao[i][j],3)))
                planilha1.append(lista_aux)
            tabela = Table(planilha1)
            tabela.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            
            conteudo.append(tabela)
            
            #############################    Imprime as coordenadas das irradiações    #####################
            if imprimir_v_cirr == 1:
                planilha2=[]
                cab2=[]
                cab2.append("Irradiação")
                cab2.append("X (m)")
                cab2.append("Y (m)")
                cab2.append("Descrição")
                planilha2.append(cab2)
                for i in range(0, len(dados_irr)):
                    lista_aux2=[]
                    lista_aux2.append(dados_irr[i][0])
                    lista_aux2.append(str(round(dados_irr[i][5],3)))
                    lista_aux2.append(str(round(dados_irr[i][6],3)))
                    lista_aux2.append(dados_irr[i][2])
                    planilha2.append(lista_aux2)
                tabela2 = Table(planilha2)
                tabela2.setStyle(TableStyle([
                                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
                conteudo.append(tabela2)
            doc.build(conteudo, onFirstPage=criar_cabecalho1)
        
        ####################    Imprime coordenadas reduzidas    #######################
        if imprimir_v_cr == 1 and imprimir_v_cp==0 and imprimir_v_ca==0:
            texto_1 = "Erro linear em X: {} m".format(round(elx_reducao,3))
            texto_2 = "Erro linear em Y: {} m".format(round(ely_reducao,3))
            texto_3 = "Erro linear: {} m".format(round(el_reducao,3))
            texto_4 = erro_linear_r
            texto_5 = "Erro longitudinal: {} m".format(round(erro_f_long_r,3))
            texto_6 = "Erro transversal: {} m".format(round(erro_f_trans_r,3))
            texto_7 = 'Erro angular: {} "'.format(round(ea_reducao, 1))
            texto_8 = 'Tolerancia angular: {} "'.format(round(tolerancia_a_r,1))
            texto_9 = "Número de estações: {} estações".format(len(lista_sequencia_correta))
            texto_10 = "Comprimento da poligonal: {} m".format(round(comprimento_pol))
            linhas_de_texto=[texto_1, texto_2, texto_3, texto_4, texto_5, texto_6, texto_7, texto_8, texto_9, texto_10]
            
            # Criar uma lista de objetos Paragraph para cada linha de texto
            styles = getSampleStyleSheet()
            for linha in linhas_de_texto:
                paragrafo = Paragraph(linha, style=styles['Normal'])
                conteudo.append(paragrafo)
                
            ###################    Cria a planilha para impressão    ###################
            planilha1=[]
            cab=[]
            cab.append("ID")
            cab.append("X (m)")
            cab.append("Y (m)")
            planilha1.append(cab)
            
            for i in range(0, len(matriz_reducao)):
                lista_aux=[]
                lista_aux.append(coordenadas_estacao[i][0])
                lista_aux.append(str(round(matriz_reducao[i][4],3)))
                lista_aux.append(str(round(matriz_reducao[i][5],3)))
                planilha1.append(lista_aux)
            tabela = Table(planilha1)
            tabela.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            
            conteudo.append(tabela)
            #############################    Imprime as coordenadas das irradiações    #####################
            if imprimir_v_cirr == 1:
                planilha2=[]
                cab2=[]
                cab2.append("Irradiação")
                cab2.append("X (m)")
                cab2.append("Y (m)")
                cab2.append("Descrição")
                planilha2.append(cab2)
                for i in range(0, len(dados_irr)):
                    lista_aux2=[]
                    lista_aux2.append(dados_irr[i][0])
                    lista_aux2.append(str(round(dados_irr[i][5],3)))
                    lista_aux2.append(str(round(dados_irr[i][6],3)))
                    lista_aux2.append(dados_irr[i][2])
                    planilha2.append(lista_aux2)
                tabela2 = Table(planilha2)
                tabela2.setStyle(TableStyle([
                                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
                conteudo.append(tabela2)
            doc.build(conteudo, onFirstPage=criar_cabecalho2)
        
        ########################    Imprime coordenadas ajustadas    ################################
        if imprimir_v_ca == 1 and imprimir_v_cp == 0 and imprimir_v_cr == 0:
            texto_9 = "Número de estações: {} estações".format(len(lista_sequencia_correta))
            texto_10 = "Comprimento da poligonal: {} m".format(np.round(comprimento_pol_a))
            texto_11 = "Número de iterações: {}".format(iteracoes)
            linhas_de_texto=[texto_9, texto_10, texto_11]
            
            # Criar uma lista de objetos Paragraph para cada linha de texto
            styles = getSampleStyleSheet()
            for linha in linhas_de_texto:
                paragrafo = Paragraph(linha, style=styles['Normal'])
                conteudo.append(paragrafo)
            
            ###################    Imprime as coordenadas ajustadas sem as precisões    ##############
            if imprimir_v_pre == 0:
                #########################    Cria a planilha para impressão    #######################
                planilha1=[]
                cab=[]
                cab.append("ID")
                cab.append("X (m)")
                cab.append("Y (m)")
                planilha1.append(cab)
                
                for i in range(0, len(coordenadas_ajustadas)):
                    lista_aux=[]
                    lista_aux.append(lista_sequencia_correta[i])
                    lista_aux.append(str(round(coordenadas_ajustadas[i][0],3)))
                    lista_aux.append(str(round(coordenadas_ajustadas[i][1],3)))
                    planilha1.append(lista_aux)
                tabela = Table(planilha1)
                tabela.setStyle(TableStyle([
                                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
                
                conteudo.append(tabela)
                
                ###############################    Imprime as irradiacoes    ######################
                if imprimir_v_cirr == 1:   
                    planilha2=[]
                    cab2=[]
                    cab2.append("Irradiação")
                    cab2.append("X (m)")
                    cab2.append("Y (m)")
                    cab2.append("Descrição")
                    planilha2.append(cab2)
                    for i in range(0, len(dados_irr)):
                        lista_aux2=[]
                        lista_aux2.append(dados_irr[i][0])
                        lista_aux2.append(str(round(dados_irr[i][5],3)))
                        lista_aux2.append(str(round(dados_irr[i][6],3)))
                        lista_aux2.append(dados_irr[i][2])
                        planilha2.append(lista_aux2)
                    tabela2 = Table(planilha2)
                    tabela2.setStyle(TableStyle([
                                                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0, 0), (-1, 0), 12),
                                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
                    conteudo.append(tabela2)
                
                doc.build(conteudo, onFirstPage=criar_cabecalho3)
            
            #####################    Imprime as coordenadas com as precisões    ####################
            elif imprimir_v_pre == 1:
                ###################    Cria a planilha para impressão    ###################
                planilha1=[]
                cab=[]
                cab.append("ID")
                cab.append("X (m)")
                cab.append("Y (m)")
                cab.append("DESV X (m)")
                cab.append("DESV Y (m)")
                planilha1.append(cab)
                
                for i in range(0, len(matriz_impressao)):
                    lista_aux=[]
                    lista_aux.append(matriz_impressao[i][0])
                    lista_aux.append(str(round(matriz_impressao[i][1],3)))
                    lista_aux.append(str(round(matriz_impressao[i][2],3)))
                    lista_aux.append(str(round(matriz_impressao[i][3],3)))
                    lista_aux.append(str(round(matriz_impressao[i][4],3)))
                    planilha1.append(lista_aux)
                tabela = Table(planilha1)
                tabela.setStyle(TableStyle([
                                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
                
                conteudo.append(tabela)
                
                ##########################    Imprime as irradiaçoes    #########################
                if imprimir_v_cirr == 1:
                    planilha2=[]
                    cab2=[]
                    cab2.append("Irradiação")
                    cab2.append("X (m)")
                    cab2.append("Y (m)")
                    cab2.append("Descrição")
                    if imprimir_v_pre == 1:
                        cab2.append("Desvio X (m)")
                        cab2.append("Desvio Y (m)")
                    planilha2.append(cab2)
                    for i in range(0, len(dados_irr)):
                        lista_aux2=[]
                        lista_aux2.append(dados_irr[i][0])
                        lista_aux2.append(str(round(dados_irr[i][5],3)))
                        lista_aux2.append(str(round(dados_irr[i][6],3)))
                        lista_aux2.append(dados_irr[i][2])
                        if imprimir_v_pre == 1:
                            lista_aux2.append(str(round(math.sqrt(var_irradiacoes[i][1]),3)))
                            lista_aux2.append(str(round(math.sqrt(var_irradiacoes[i][2]),3)))
                        planilha2.append(lista_aux2)
                    tabela2 = Table(planilha2)
                    tabela2.setStyle(TableStyle([
                                                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0, 0), (-1, 0), 12),
                                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
                    conteudo.append(tabela2)
                doc.build(conteudo, onFirstPage=criar_cabecalho3)
        
        #########################    Imprime os dados do ajustamento    ################################
        if imprimir_v_aju == 1:
            ############################    Imprime a matriz das covariancias    #######################
            planilha1=[["Matriz das covariâncias"]]
            
            for i in range(0, len(Cxy)):
                lista_aux=[]
                for j in range(0, len(Cxy)):
                    lista_aux.append(Cxy[i][j])
                planilha1.append(lista_aux)
            
            tabela=Table(planilha1)
            tabela.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            conteudo.append(tabela)
            
            ############################    Residuo das observações    ##########################
            planilha2=[["Resíduo das observações"]]
            
            for i in range(0, len(V)):
                lista_aux=[]
                lista_aux.append(V[i])
                planilha2.append(lista_aux)
            
            tabela2=Table(planilha2)
            tabela2.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            conteudo.append(tabela2)
            
            ############################    MVC  a posteriori das observações    ########################
            planilha3=[["MCV a posteriori das observações"]]
            
            for i in range(0, len(CLB)):
                lista_aux=[]
                for j in range(0, len(CLB)):
                    lista_aux.append(round(CLB[i][j],10))
                planilha3.append(lista_aux)
            
            tabela3=Table(planilha3)
            tabela3.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            conteudo.append(tabela3)
            
            ###########################    MVC a posteriori dos residuos    ########################
            planilha4=[["MCV a posteriori dos resíduos"]]
            
            for i in range(0, len(Cv)):
                lista_aux=[]
                for j in range(0, len(Cv)):
                    lista_aux.append(round(Cv[i][j],10))
                planilha4.append(lista_aux)
            
            tabela4=Table(planilha3)
            tabela4.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            conteudo.append(tabela4)
            
            doc.build(conteudo, onFirstPage=criar_cabecalho3)
            
            
        messagebox.showinfo(title="RELATÓRIO", message="GERADO!")
    
    ###################    Cria a janela de configuraçao do relatorio    ########################
    gerar_relatorio = Toplevel()
    gerar_relatorio.title("Relatório")
    gerar_relatorio.geometry("800x500")
    gerar_relatorio.configure(background='#dde')
    
    frame_gerar_relatorio = Frame(gerar_relatorio, borderwidth=1, relief="solid")
    frame_gerar_relatorio.place(x=0, y=0, width=1000, height=600)

    frame1=LabelFrame(frame_gerar_relatorio, text="Coordenadas", borderwidth=1, relief="solid")
    frame1.place(x=20, y=20, width=301, height=180)
    frame2=LabelFrame(frame_gerar_relatorio, text="Tipo de Coordenadas", borderwidth=1, relief="solid")
    frame2.place(x=341, y=20, width=301, height=180)
    frame3=LabelFrame(frame_gerar_relatorio, text="Outros", borderwidth=1, relief="solid")
    frame3.place(x=20, y=220, width=301, height=180)
    
    v_coordenadas_processadas = IntVar()
    v_coordenadas_reduzidas = IntVar()
    v_coordenadas_ajustadas = IntVar()
    v_coordenadas_poligonal = IntVar()
    v_coordenadas_irradiacoes = IntVar()
    v_precisoes = IntVar()
    v_ajustamento = IntVar()
    
    chk_coordenadas_processadas=Checkbutton(frame1, text="Processadas", variable=v_coordenadas_processadas, onvalue=1, offvalue=0)
    chk_coordenadas_reduzidas=Checkbutton(frame1, text="Reduzidas", variable=v_coordenadas_reduzidas, onvalue=1, offvalue=0)
    chk_coordenadas_ajustadas=Checkbutton(frame1, text="Ajustadas", variable=v_coordenadas_ajustadas, onvalue=1, offvalue=0)
    chk_coordenadas_poligonal=Checkbutton(frame2, text="Poligonal", variable=v_coordenadas_poligonal, onvalue=1, offvalue=0)
    chk_coordenadas_irradiacoes=Checkbutton(frame2, text="Irradiações", variable=v_coordenadas_irradiacoes, onvalue=1, offvalue=0)
    chk_precisoes=Checkbutton(frame3, text="Precisões das coordenadas", variable=v_precisoes, onvalue=1, offvalue=0)
    chk_ajustamento=Checkbutton(frame3, text="Resultados do Ajustamento", variable=v_ajustamento, onvalue=1, offvalue=0)
    
    chk_coordenadas_processadas.place(x=15, y=25)
    chk_coordenadas_reduzidas.place(x=15, y=50)
    chk_coordenadas_ajustadas.place(x=15, y=75)
    chk_coordenadas_poligonal.place(x=15, y=25)
    chk_coordenadas_irradiacoes.place(x=15, y=50)
    chk_precisoes.place(x=15, y=25)
    chk_ajustamento.place(x=15, y=50)
    
    btn_gerar_relatorio=Button(frame_gerar_relatorio, text="OK", command=lambda :gera(v_coordenadas_processadas, v_coordenadas_reduzidas, v_coordenadas_ajustadas, v_coordenadas_poligonal, v_coordenadas_irradiacoes, v_precisoes, v_ajustamento))
    btn_gerar_relatorio.place(x=491, y=310, width=50, height=30)

    gerar_relatorio.mainloop()
    
######################################   DXF   ########################################
def gerarDxf():
    nome_janela= asksaveasfilename(defaultextension= ".dxf", initialdir = "/",title = "Salvar",filetypes = (("DXF","*.dxf"),("all files","*.*")))
    nomes_descri=[]
    for k in range(0, len(m)):
        if m[k][3]=="IRRADIACAO":
            if m[k][8] not in nomes_descri:
                nomes_descri.append(m[k][8])    
    
    doc = ezdxf.new('R2000', setup=True)
    msp = doc.modelspace()
    doc.header['$INSUNITS'] = 6
    doc.header['$PDMODE'] = 67
    doc.header['$PDSIZE'] = 3.0
    doc.layers.new(name="poligonal")
    for i in nomes_descri:
        doc.layers.new(name=i)
    
    for i in range(0,len(lista_sequencia_correta)):
        msp.add_point(location=(xpol[i],ypol[i]), dxfattribs={"layer": "poligonal"})
        texto=lista_sequencia_correta[i]
        msp.add_text(texto,dxfattribs={"layer": "poligonal"}).set_pos((xpol[i], ypol[i]), align="TOP_RIGHT")
    extents = bbox.extents(msp)
    
    for j in nomes_descri:
        for l in range(0, len(dados_irr)):
            if j == dados_irr[l][2]:
                msp.add_point(location=(dados_irr[l][5], dados_irr[l][6]), dxfattribs={"layer": j})
                texto1 = j
                texto2 = dados_irr[l][0]
                msp.add_text(texto1, dxfattribs={"layer": j}).set_pos((dados_irr[l][5], dados_irr[l][6]), align="TOP_RIGHT")
                msp.add_text(texto2, dxfattribs={"layer": j}).set_pos((dados_irr[l][5], dados_irr[l][6]), align="TOP_LEFT")
    aux=[]
    aux.append(nome_janela.split("/"))
    nome=aux[0][-1]
    doc.saveas(nome) 
    
    messagebox.showinfo(title="DXF", message="GERADO!")


def abrirHelp():
    print("")
def Sobre():
    print("")

##############################   Janela Principal   ###########################
Gauss = Tk()
Gauss.title("Gauss   Versão BETA")
Gauss.geometry("1500x800")
Gauss.configure(background="#899" ) #dde
Fr_1=Frame(Gauss, borderwidth=1, relief="sunken")
Fr_1.place(x=0, y=0, width=220, height=680)
btn_planilha= Button(Fr_1, text="Planilha de Campo", command=confPlanilha)
btn_planilha.place(x=10, y=10, width=200, height=30)

###############################   Menu   #####################################
menuBar = Menu(Gauss)

###############################   Menu Importar   ############################
menuColetora = Menu(menuBar, tearoff=0)
menuColetora.add_command(label="Topcon 102N", command=leituraTopcon102N)
menuColetora.add_command(label="Geodetic", command=leituraGeodetic)
menuColetora.add_command(label="Planilha manual", command=planilhaManual)
menuBar.add_cascade(label="Importar", menu= menuColetora) 

###############################   Menu Poligonal   ###########################
menuPoligonal = Menu(menuBar, tearoff=0)
menuConfigurarPol = Menu(menuPoligonal, tearoff=0)
menuConfigurarPol.add_command(label="Configurar Parametros", command=configurarParametrosPol)
menuConfigurarPol.add_command(label="Processar", command=processarPoligonal)
menuConfigurarPol.add_command(label="Reduzir", command=reducaoPol)
menuConfigurarPol.add_command(label="Ajustar", command=ajustarPol)
menuBar.add_cascade(label="Poligonal", menu= menuConfigurarPol)

###############################   Menu Irradiacao   ###########################
menuIrradia = Menu(menuBar, tearoff=0)
menuIrr = Menu(menuIrradia, tearoff=0)
menuIrr.add_command(label="Configurar Parametros", command=configurarParametrosIrr)
menuIrr.add_command(label="Processar", command=processarIrradiacoes)
menuIrr.add_command(label="Reduzir", command=reduzirIrr)
menuIrr.add_command(label="Propagar variancias", command=propagarVariancias)
menuBar.add_cascade(label="Irradiação", menu= menuIrr)

###############################   Menu Gerar   ###############################
menuGerar = Menu(menuBar, tearoff=0)
menuGerar.add_command(label="DXF", command=gerarDxf)
menuGerar.add_command(label="Relatorio", command=gerarRelatorio)
menuBar.add_cascade(label="Gerar", menu= menuGerar)

###############################   Help   #####################################
menuHelp = Menu(menuBar, tearoff=0)
menuHelp.add_command(label="Help", command=abrirHelp)
menuHelp.add_command(label="Sobre", command=Sobre)
menuBar.add_cascade(label="?", menu= menuHelp)

Gauss.config(menu=menuBar)
Gauss.mainloop()