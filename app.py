import pygame, random, math, os, array

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init(); pygame.font.init()
try:
    if not pygame.mixer.get_init(): pygame.mixer.init()
except: pass

INFO = pygame.display.Info()
LARGURA_TELA, ALTURA_TELA = INFO.current_w, INFO.current_h
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.FULLSCREEN)
pygame.display.set_caption("GTA Maracana - Bandeira do Brasil")

SR = 22050; SONS = {}
def _cs(s):
    try:
        b = array.array('h')
        for v in s:
            val = int(max(-1.0, min(1.0, v)) * 32767)
            b.append(val); b.append(val)
        return pygame.mixer.Sound(buffer=b.tobytes())
    except: return None
def _safe(f):
    def w(*a, **k):
        try: return f(*a, **k)
        except: return None
    return w

@_safe
def g_passo():
    n=int(SR*0.08); o=[]
    for i in range(n): o.append(random.uniform(-1,1)*math.exp(-i/(SR*0.015))*0.25)
    return _cs(o)
@_safe
def g_fala():
    n=int(SR*0.5); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.2)); f=140+80*math.sin(2*math.pi*4*t)+30*math.sin(2*math.pi*8*t)
        o.append((math.sin(2*math.pi*f*t)+0.4*math.sin(2*math.pi*f*2*t)+0.2*math.sin(2*math.pi*f*3*t))*env*0.25)
    return _cs(o)
@_safe
def g_fala_fem():
    n=int(SR*0.5); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.2)); f=220+100*math.sin(2*math.pi*5*t)+40*math.sin(2*math.pi*9*t)
        o.append((math.sin(2*math.pi*f*t)+0.4*math.sin(2*math.pi*f*2*t)+0.2*math.sin(2*math.pi*f*3*t))*env*0.22)
    return _cs(o)
@_safe
def g_crianca():
    n=int(SR*0.4); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.15)); f=320+120*math.sin(2*math.pi*6*t)+50*math.sin(2*math.pi*12*t)
        o.append((math.sin(2*math.pi*f*t)+0.5*math.sin(2*math.pi*f*2*t))*env*0.2)
    return _cs(o)
@_safe
def g_torcida():
    n=int(SR*2); o=[]; b0=b1=b2=0
    for i in range(n):
        w=random.uniform(-1,1); b0=0.99*b0+w*0.05; b1=0.96*b1+w*0.08; b2=0.90*b2+w*0.12
        v=(b0+b1+b2)*0.5; env=0.5+0.5*math.sin(2*math.pi*0.3*i/SR)
        o.append(v*env*0.35)
    return _cs(o)
@_safe
def g_fogo():
    n=int(SR*0.8); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.15))
        o.append((math.sin(2*math.pi*60*t)*env+random.uniform(-1,1)*math.exp(-i/(SR*0.05))*0.4)*0.5)
    return _cs(o)
@_safe
def g_sirene():
    n=int(SR*1); o=[]
    for i in range(n):
        t=i/SR; f=800 if int(t*4)%2==0 else 600
        o.append(math.sin(2*math.pi*f*t)*min(1.0,(n-i)/(SR*0.1))*0.25)
    return _cs(o)
@_safe
def g_carro():
    n=int(SR*0.4); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.2))
        o.append((math.sin(2*math.pi*80*t)+0.5*math.sin(2*math.pi*120*t))*env*0.15+random.uniform(-1,1)*env*0.05)
    return _cs(o)
@_safe
def g_latido():
    n=int(SR*0.15); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.05)); f=400-200*(i/n)
        o.append(math.sin(2*math.pi*f*t)*env*0.35)
    return _cs(o)
@_safe
def g_notif():
    n=int(SR*0.4); o=[]
    for i in range(n):
        t=i/SR; f=880 if t<0.15 else 1100
        env=math.exp(-((t if t<0.15 else t-0.15))/0.1)
        o.append(math.sin(2*math.pi*f*t)*env*0.3)
    return _cs(o)
@_safe
def g_tiro():
    n=int(SR*0.2); o=[]
    for i in range(n): o.append(random.uniform(-1,1)*math.exp(-i/(SR*0.02))*0.5)
    return _cs(o)
@_safe
def g_heli():
    n=int(SR*1.0); o=[]
    for i in range(n):
        t=i/SR; rotor=math.sin(2*math.pi*15*t)*0.5; cauda=math.sin(2*math.pi*60*t)*0.2
        motor=math.sin(2*math.pi*100*t)*0.15; vento=random.uniform(-1,1)*0.08
        env=0.6+0.4*abs(math.sin(2*math.pi*15*t))
        o.append((rotor*env+cauda+motor+vento)*0.4)
    return _cs(o)
@_safe
def g_bala():
    n=int(SR*0.3); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.05)); f=1500-1200*(i/n)
        o.append(math.sin(2*math.pi*f*t)*env*0.4+random.uniform(-1,1)*env*0.2)
    return _cs(o)
@_safe
def g_bike():
    n=int(SR*0.4); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.1)); f=1200+200*math.sin(2*math.pi*8*t)
        o.append(math.sin(2*math.pi*f*t)*env*0.25)
    return _cs(o)
@_safe
def g_bola():
    n=int(SR*0.15); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.03)); f=200-100*(i/n)
        o.append(math.sin(2*math.pi*f*t)*env*0.4)
    return _cs(o)
@_safe
def g_apagar():
    n=int(SR*0.3); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.05))
        o.append(random.uniform(-1,1)*env*0.3+math.sin(2*math.pi*200*t)*env*0.2)
    return _cs(o)
@_safe
def g_prisao():
    n=int(SR*1.2); o=[]
    for i in range(n):
        t=i/SR; env=math.exp(-i/(SR*0.3))
        v=math.sin(2*math.pi*80*t)*env*0.6+math.sin(2*math.pi*120*t)*env*0.4
        if i>int(SR*0.6): v+=random.uniform(-1,1)*0.3
        o.append(v*0.4)
    return _cs(o)
@_safe
def g_buzina():
    n=int(SR*0.8); o=[]
    for i in range(n):
        t=i/SR
        env = min(1, i/(SR*0.05)) * (1 if t<0.6 else max(0, 1-(t-0.6)/0.2))
        v = math.sin(2*math.pi*180*t)*0.5 + math.sin(2*math.pi*220*t)*0.3 + math.sin(2*math.pi*280*t)*0.2
        o.append(v*env*0.4)
    return _cs(o)
@_safe
def g_apito_torcida():
    n=int(SR*1.5); o=[]
    for i in range(n):
        t=i/SR
        env = 0.7 + 0.3*math.sin(2*math.pi*3*t)
        v = math.sin(2*math.pi*2500*t)*0.4 + math.sin(2*math.pi*3200*t)*0.2
        o.append(v*env*0.15)
    return _cs(o)
@_safe
def g_rojão_mao():
    n=int(SR*2.0); o=[]
    for i in range(n):
        t=i/SR
        f = 3500 + 1500*math.sin(2*math.pi*2*t)
        v = math.sin(2*math.pi*f*t)*0.15 + random.uniform(-1,1)*0.35
        env = 0.6 + 0.4*math.sin(2*math.pi*8*t)
        o.append(v*env*0.25)
    return _cs(o)
@_safe
def g_sertanejo():
    dur=8; n=int(SR*dur); o=[]; notas=[261.63,293.66,329.63,349.23,392.00,349.23,329.63,293.66]
    for i in range(n):
        t=i/SR; beat=int(t*2)%len(notas); f=notas[beat]; env=(1-(t*2%1))*0.4
        o.append((math.sin(2*math.pi*f*t)*env+0.3*math.sin(2*math.pi*f*2*t)*env)*0.25)
    return _cs(o)
@_safe
def g_funk():
    dur=8; n=int(SR*dur); o=[]
    for i in range(n):
        t=i/SR; beat=int(t*4)%4; bass=0
        if beat in (0,2): bass=math.sin(2*math.pi*60*(t*4%1))*math.exp(-(t*4%1)*5)*0.6
        hat=random.uniform(-1,1)*math.exp(-((t*8)%1)*10)*0.15
        mel=math.sin(2*math.pi*440*t)*0.1 if int(t*2)%2==0 else 0
        o.append((bass+hat+mel)*0.4)
    return _cs(o)
@_safe
def g_pagode():
    dur=8; n=int(SR*dur); o=[]; notas=[523.25,587.33,659.25,783.99,880.00,783.99,659.25,587.33]
    for i in range(n):
        t=i/SR; beat=int(t*4)%len(notas); f=notas[beat]; env=(1-(t*4%1))*0.5
        o.append((math.sin(2*math.pi*f*t)*env+0.4*math.sin(2*math.pi*f*1.5*t)*env)*0.18)
    return _cs(o)
@_safe
def g_hino():
    dur=10; n=int(SR*dur); o=[]
    melodia=[(392,0.5),(392,0.5),(440,1.0),(392,0.5),(349,0.5),(392,1.0),(440,0.5),(523,0.5),(466,1.0),
             (440,0.5),(392,0.5),(349,1.5),(392,0.5),(440,0.5),(523,1.0),(466,0.5),(440,0.5),(392,1.0),(349,0.5),(392,0.5),(440,2.0)]
    pos=0
    for f,d in melodia:
        cnt=int(SR*d)
        for i in range(cnt):
            t=i/SR; env=min(1,i/(SR*0.05))*min(1,(cnt-i)/(SR*0.05))
            v=math.sin(2*math.pi*f*t)*env*0.7+0.3*math.sin(2*math.pi*f*2*t)*env
            if pos<n: o.append(v*0.25); pos+=1
    while len(o)<n: o.append(0)
    return _cs(o)

print("Gerando sons...")
SONS['passo']=g_passo(); SONS['fala']=g_fala(); SONS['fala_fem']=g_fala_fem()
SONS['crianca']=g_crianca(); SONS['torcida']=g_torcida(); SONS['fogo']=g_fogo()
SONS['sirene']=g_sirene(); SONS['carro']=g_carro(); SONS['latido']=g_latido()
SONS['notificacao']=g_notif(); SONS['tiro']=g_tiro(); SONS['helicoptero']=g_heli()
SONS['bala']=g_bala(); SONS['bike']=g_bike(); SONS['bola']=g_bola(); SONS['apagar']=g_apagar()
SONS['prisao']=g_prisao()
SONS['buzina']=g_buzina(); SONS['apito']=g_apito_torcida()
SONS['rojão_mao']=g_rojão_mao()
SONS['sertanejo']=g_sertanejo(); SONS['funk']=g_funk(); SONS['pagode']=g_pagode(); SONS['hino']=g_hino()
print("Sons prontos!")

CANAIS = {}
try:
    pygame.mixer.set_num_channels(24)
    nomes_c = ['torcida','passos','fala','efeitos','notificacao','sirene','radio','heli','buzina','apito',
               'roj1','roj2','roj3','roj4','c1','c2','c3','c4','c5','c6','c7','c8','c9','c10']
    for i,n in enumerate(nomes_c):
        CANAIS[n]=pygame.mixer.Channel(i)
    if SONS.get('torcida'):
        CANAIS['torcida'].play(SONS['torcida'], loops=-1); CANAIS['torcida'].set_volume(0.35)
except: pass

CD = {}
def pode_tocar(n,i):
    try:
        a=pygame.time.get_ticks()/1000.0
        if a-CD.get(n,0)>i: CD[n]=a; return True
    except: pass
    return False
def tocar(n,c='efeitos',v=0.5):
    try:
        if n in SONS and SONS[n] is not None and c in CANAIS:
            CANAIS[c].set_volume(v); CANAIS[c].play(SONS[n])
    except: pass
def tocar_rojão(canal_idx, v=0.4):
    try:
        if 'rojão_mao' in SONS and SONS['rojão_mao']:
            cn = f'roj{canal_idx}'
            if cn in CANAIS:
                CANAIS[cn].set_volume(v)
                CANAIS[cn].play(SONS['rojão_mao'])
    except: pass

FU=pygame.font.SysFont('arial',28,bold=True); FT=pygame.font.SysFont('arial',24,bold=True)
FA=pygame.font.SysFont('arial',36,bold=True); FApp=pygame.font.SysFont('arial',14,bold=True)
FAM=pygame.font.SysFont('arial',16,bold=True); FAG=pygame.font.SysFont('arial',40,bold=True)
FD=pygame.font.SysFont('arial',18,bold=True); FL=pygame.font.SysFont('arial',60,bold=True)
FF=pygame.font.SysFont('arial',14); FC=pygame.font.SysFont('arial',16)
FP=pygame.font.SysFont('arial',30,bold=True); FTX=pygame.font.SysFont('arial',22,bold=True)
FB=pygame.font.SysFont('arial',70,bold=True); FG=pygame.font.SysFont('arial',90,bold=True)

BR=(255,255,255); CL=(230,230,230); CZ=(120,120,120); CE=(60,60,60); PT=(0,0,0)
VC=(34,139,34); VCC=(50,180,50); AB=(255,223,0); VB=(0,150,64); AZB=(0,39,118)
PE=(224,172,105); PEB=(255,224,189); CES=(184,134,11); MC=(139,69,19); PC=(30,30,30)
AS=(80,80,80); FAMC=(255,215,0); CPM=(210,180,140); CPI=(0,191,255)
VF=(255,0,0); CTR=(100,100,100); CM=(200,200,200); CMJ=(0,100,200)
CH=(50,50,50); LI=(255,140,0); CB=(255,255,255); CCO=(0,200,100)
VP=(0,100,40); AG=(20,60,140); VFU=(60,200,80); VRO=(255,60,20); VFG=(0,255,100)
VV=(220,30,30); VDV=(30,200,50); ACH=(100,150,220); ASol=(255,230,100)
CPP=(180,160,140); CPQ=(150,130,180); CPS=(200,170,130); CPC=(180,200,180)
CPB=(180,200,220); CSA=(140,120,100); CCN=(255,140,0)
RADIO_COR=(40,40,50); RADIO_TXT=(100,255,100); SANGUE=(200,0,0); C_BIKE=(50,50,100)
AZUL_POLICIA=(20,20,120); VERMELHO_POLICIA=(180,20,20); AMARELO_POLICIA=(240,200,0)
COR_DELEGACIA=(100,100,120); COR_GRADE=(60,60,60)
FUMACA_VERDE_ROJAO = (80, 220, 80)
FUMACA_BRANCA_ROJAO = (240, 240, 240)
FUMACA_AZUL_ROJAO = (80, 140, 255)

TM=4000; CX=TM//2; CY=TM//2; RE=350; RI=200
MX=200; MY=200; ML=800; MA=600; PX=MX+ML+100; PY=MY+100; PL=300; PA=200
REY=CY+RE+150; TY=REY+150
RH=[0,600,1200,3000,3600,REY]; RV=[0,600,1200,3000,3600]
DEL_X=3200; DEL_Y=2400; DEL_L=280; DEL_A=220

SL=pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA)
SE=pygame.Surface((LARGURA_TELA,ALTURA_TELA))
SC=pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA)
VINHETA=pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA)
for i in range(60):
    a=int(80*(1-i/60)); pygame.draw.rect(VINHETA,(0,0,0,a),(i,i,LARGURA_TELA-i*2,ALTURA_TELA-i*2),1)
TEX_GRAMA=pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA)
for _ in range(400):
    x=random.randint(0,LARGURA_TELA); y=random.randint(0,ALTURA_TELA)
    pygame.draw.circle(TEX_GRAMA,(140,180,140,60),(x,y),random.randint(1,3))

NUVENS = []
for _ in range(12):
    NUVENS.append({'x': random.randint(-500, TM+500), 'y': random.randint(-500, -100),
                   'tam': random.randint(120, 250), 'vel': random.uniform(5, 15), 'alt': random.uniform(0.3, 0.7)})
ESTRELAS = []
for _ in range(150):
    ESTRELAS.append({'x': random.randint(0, LARGURA_TELA), 'y': random.randint(0, ALTURA_TELA//2),
                     'tam': random.randint(1, 3), 'brilho': random.uniform(0.5, 1.0), 'twinkle': random.uniform(0, 6.28)})

PP=2; PG=1; TJ=90
RADIOS=[{'nome':'Sertanejo FM 101.5','som':'sertanejo','cor':(200,120,50)},
        {'nome':'Funk Radio 105.0','som':'funk','cor':(255,50,150)},
        {'nome':'Pagode FM 98.0','som':'pagode','cor':(50,200,100)},
        {'nome':'Hino dos Times 90.0','som':'hino','cor':(200,200,50)}]

FALAS_PED=["Vamo Palmeiras!","Gremio e imortal!","Que jogao, hein!","Vai chover hoje, viu!","Chamei um Uber agora!",
    "Olha o celular ai, mano!","Bora pro Maracana!","Olha o preco da pipoca!","Que calor, meu Deus!","Cade meu amigo?","To perdido aqui!","Viu o jogo ontem?"]
FALAS_JOG=["Vamo Palmeiras!","Bora pro jogo!","Vou chamar um Uber!","Que jogao, mano!","Aqui e Brasil!","Bora, bora!","E ai, beleza?","Fala, mano!"]
FALAS_MOR=["Que jogo bom!","Vou ver da sacada!","Chegou a pizza!","Vou dormir!","To com sono!","Bora assistir!","Ai que tedio!","Vou ver TV!"]
FALAS_POL=["Maos ao alto!","Afasta, afasta!","Vai pra tras!","Sai fora!","Calma ai!","Chega, chega!","Para com isso!","Vai pra casa!","Separa essa briga!"]
FALAS_CHAT=["Vamo Palmeiras!","Gremio! Gremio!","Olha a radio!","Bora pro jogo!","Chamei um Uber!","Sertanejo e top!","Funk na veia!","Viva o Brasil!","Olha o rojão!"]
FALAS_MOLE=["Bora joga bola!","Deixa a gente entra!","Por favor, seu guarda!","Vamo chuta!","Vamo fazer gol!","Que massa, mano!","So um pouquinho!"]
FALAS_SEG_LIBERA=["Pode entra, crianca!","Liberado!","Vai la, mas cuidado!","Ta liberado, vai!","Aproveita, molecada!"]
FALAS_SEG_NEGA=["Nao pode nao!","Aqui nao, moleque!","Volta amanha!","Fechado!","Vai pra casa, crianca!"]
FALAS_HORA_IR=["Ja ta tarde, vamo embora!","Apaga a luz, guarda!","Ate amanha, pessoal!","Tchau, Maracana!","Amanha tem aula!","Valeu pela bola, guarda!"]
FALAS_SEG_APAGA=["Ja deu, crianca! Vao pra casa!","Ta na hora de dormir!","Apaga a luz, Ze!","Vamos, ja sao 23:40!","Vao com Deus!"]
FALAS_POLICIA_RJ=["Policia do Rio! Maos ao alto!","Voce esta preso!","Deita no chao!","Bora pra delegacia!",
    "Aqui e a PM do Rio!","Chega de confusao!","Voce vai preso, moleque!","Nao corre!","Algemas nele!"]
FALAS_PRESO=["Eu nao fiz nada!","Me solta!","Foi mal, seu guarda!","Nao vou mais!","Foi brincadeira!",
    "Me da uma chance!","Nao quero ir preso!","Ai, ai!","Que vergonha...","Minha mae vai me mata!"]
FALAS_TORCIDA_ONIBUS=["Vamo Palmeiras!","Aqui e a Mancha!","Aqui e a Geral!","Bora pro Maracana!",
    "E o Verdão!","Gremio! Gremio!","Vamo cantar!","Torcida unida!",
    "Vai começar o jogo!","Rumo ao hexa!","Gremio imortal!","Vamo ganhar!",
    "Bora, bora, bora!","Alo torcida!","Canta comigo!","E o time!","Vamo Brasil!"]
FALAS_ROJAO=["Olha o rojão!","Segura o rojão!","Rojão na area!","Vamo, vamo!",
    "Fumaça verde!","Que fumaça!","Rojão aceso!","Bora com tudo!"]
FALAS_MORADORA=["Vamo Brasil!","Olha minha bandeira!","Aqui e Brasil!","Bora, bora!",
    "Viva o Brasil!","Palmeiras! Palmeiras!","Vamo ganhar!","Que jogo bom!",
    "Estou torcendo!","Bandeira do Brasil!"]

class CameraShake:
    def __init__(self):
        self.intensidade = 0; self.duracao = 0
    def ativar(self, inten, dur):
        self.intensidade = inten; self.duracao = dur
    def atualizar(self, dt):
        if self.duracao > 0:
            self.duracao -= dt; self.intensidade *= 0.92
        else: self.intensidade = 0
    def get_offset(self):
        if self.intensidade > 0.5:
            return (random.uniform(-self.intensidade, self.intensidade),
                    random.uniform(-self.intensidade, self.intensidade))
        return (0, 0)

CAM_SHAKE = CameraShake()

class FumacaRoxa:
    def __init__(self, x, y, cor):
        self.x = x; self.y = y
        self.cor = cor
        self.vx = random.uniform(-15, 15)
        self.vy = random.uniform(-70, -40)
        self.tam = random.randint(8, 16)
        self.tv = 0
        self.vm = random.uniform(2.0, 3.5)
    def atualizar(self, dt):
        self.tv += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.tam += 25 * dt
        self.vy += 8 * dt
        self.vx *= 0.97
        return self.tv < self.vm
    def desenhar(self, camx, camy):
        a = max(0, int(220 * (1 - self.tv / self.vm)))
        s = pygame.Surface((int(self.tam*2), int(self.tam*2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, a), (int(self.tam), int(self.tam)), int(self.tam))
        pygame.draw.circle(s, (min(255, self.cor[0]+60), min(255, self.cor[1]+60), min(255, self.cor[2]+60), a//2), 
            (int(self.tam), int(self.tam)), int(self.tam * 0.5))
        TELA.blit(s, (self.x - camx - self.tam, self.y - camy - self.tam))

class RojaoMao:
    def __init__(self, fanatico, time):
        self.fanatico = fanatico
        self.time = time
        self.tempo_vida = random.uniform(4.0, 8.0)
        self.tempo_atual = 0
        self.fase = 0
        if time == 'palmeiras':
            self.cores = [FUMACA_VERDE_ROJAO, FUMACA_BRANCA_ROJAO]
        else:
            self.cores = [FUMACA_AZUL_ROJAO]
        self.cor_idx = 0
        self.tempo_troca_cor = 0
        self.tempo_proximo_som = 0
        self.canal_idx = random.randint(1, 4)
    def atualizar(self, dt, fumacas_ref):
        self.tempo_atual += dt
        self.fase += dt * 30
        if self.time == 'palmeiras':
            self.tempo_troca_cor += dt
            if self.tempo_troca_cor > 0.8:
                self.tempo_troca_cor = 0
                self.cor_idx = 1 - self.cor_idx
        if random.random() < 0.7:
            cor = self.cores[self.cor_idx]
            fx = self.fanatico.x + random.randint(-3, 3)
            fy = self.fanatico.y - 15 + random.randint(-2, 2)
            fumacas_ref.append(FumacaRoxa(fx, fy, cor))
        self.tempo_proximo_som += dt
        if self.tempo_proximo_som > 1.5:
            self.tempo_proximo_som = 0
            tocar_rojão(self.canal_idx, 0.3)
        return self.tempo_atual < self.tempo_vida
    def desenhar_na_mao(self, camx, camy):
        fx = self.fanatico.x - camx
        fy = self.fanatico.y - camy
        pygame.draw.rect(TELA, (60, 60, 60), (fx+3, fy-18, 3, 15))
        pygame.draw.rect(TELA, (150, 100, 50), (fx+3, fy-5, 3, 6))
        if self.time == 'palmeiras':
            cor_chama = FUMACA_VERDE_ROJAO if self.cor_idx == 0 else FUMACA_BRANCA_ROJAO
        else:
            cor_chama = FUMACA_AZUL_ROJAO
        brilho = int(abs(math.sin(self.fase)) * 100)
        cor_brilho = (min(255, cor_chama[0]+brilho), min(255, cor_chama[1]+brilho), min(255, cor_chama[2]+brilho))
        pygame.draw.circle(TELA, cor_brilho, (int(fx+4), int(fy-19)), 6)
        pygame.draw.circle(TELA, (255,255,255), (int(fx+4), int(fy-19)), 3)
        for _ in range(2):
            sx = fx + 4 + random.randint(-4, 4)
            sy = fy - 19 + random.randint(-4, 4)
            pygame.draw.circle(TELA, (255, 240, 150), (int(sx), int(sy)), 1)

# ============ TV ANIMADA DENTRO DO APARTAMENTO ============
class TV:
    """TV dentro do apartamento com tela animada"""
    def __init__(self, x, y):
        self.x = x; self.y = y
        self.ligada = random.random() < 0.7
        self.canal = random.choice(['futebol', 'novela', 'noticia', 'desenho', 'static'])
        self.fase = 0
        self.cor_canal = random.choice([(50,150,50), (100,50,150), (150,50,50), (50,50,150)])
    def atualizar(self, dt, horas=12):
        self.fase += dt
        # À noite, mais TVs ligadas
        if 19 <= horas or horas < 6:
            if not self.ligada and random.random() < 0.001:
                self.ligada = True
        else:
            if self.ligada and random.random() < 0.0005:
                self.ligada = False
        # Muda de canal de vez em quando
        if random.random() < 0.002:
            self.canal = random.choice(['futebol', 'novela', 'noticia', 'desenho', 'static'])
            self.cor_canal = random.choice([(50,150,50), (100,50,150), (150,50,50), (50,50,150)])
    def desenhar(self, camx, camy):
        x = self.x - camx; y = self.y - camy
        # Móvel da TV (base)
        pygame.draw.rect(TELA, (60, 40, 20), (x-1, y+4, 14, 6))
        # TV (moldura)
        pygame.draw.rect(TELA, PT, (x-2, y-4, 16, 10))
        # Tela
        if self.ligada:
            # Cintilação da tela
            brilho = int(abs(math.sin(self.fase*5)) * 50)
            if self.canal == 'static':
                # Estática (chuviscos)
                for i in range(8):
                    px = x + random.randint(0, 12)
                    py = y - 3 + random.randint(0, 7)
                    cor = random.choice([(200,200,200), (150,150,150), (100,100,100)])
                    pygame.draw.rect(TELA, cor, (px, py, 1, 1))
            else:
                cor = self.cor_canal
                cor_clara = (min(255, cor[0]+brilho), min(255, cor[1]+brilho), min(255, cor[2]+brilho))
                pygame.draw.rect(TELA, cor_clara, (x, y-3, 12, 8))
                # Detalhe da programação
                if self.canal == 'futebol':
                    # Campo de futebol em miniatura
                    pygame.draw.rect(TELA, (30,100,30), (x+1, y-2, 10, 6))
                    pygame.draw.line(TELA, BR, (x+6, y-2), (x+6, y+4), 1)
                    pygame.draw.circle(TELA, BR, (int(x+6), int(y+1)), 1)
                elif self.canal == 'novela':
                    # 2 bonequinhos
                    pygame.draw.circle(TELA, PE, (int(x+3), int(y-1)), 1)
                    pygame.draw.circle(TELA, PE, (int(x+9), int(y-1)), 1)
                elif self.canal == 'noticia':
                    # Texto piscando
                    if int(self.fase) % 2 == 0:
                        pygame.draw.rect(TELA, (240, 240, 100), (x+2, y+2, 8, 2))
                elif self.canal == 'desenho':
                    # Cores vibrantes
                    pygame.draw.circle(TELA, (255,255,0), (int(x+4), int(y)), 1)
                    pygame.draw.circle(TELA, (255,0,255), (int(x+8), int(y+2)), 1)
        else:
            pygame.draw.rect(TELA, (30, 30, 30), (x, y-3, 12, 8))

# ============ MORADORA NA SACADA COM BANDEIRA DO BRASIL ============
class MoradoraBandeira:
    """Moradora em cima da sacada balançando bandeira do Brasil"""
    def __init__(self, sacada_x, sacada_y):
        self.x = sacada_x
        self.y = sacada_y
        self.cor_camisa = random.choice([(255,220,220), (255,255,255), (240,200,255)])
        self.cor_calca = random.choice([(100,100,150), (150,100,100)])
        self.cor_pele = random.choice([PE, PEB, (200,150,100)])
        self.fase = 0
        self.tempo_fala = random.uniform(3, 10)
        self.fala = None
        self.ativo = True
        self.esta_na_sacada = True
        self.tempo_na_sacada = 0
        self.duracao_na_sacada = random.uniform(15, 30)
        self.respirando = random.uniform(0, 6.28)
    def atualizar(self, dt):
        self.fase += dt * 3  # Balanço da bandeira
        self.respirando += dt * 2
        self.tempo_na_sacada += dt
        self.tempo_fala -= dt
        if self.tempo_fala <= 0:
            self.tempo_fala = random.uniform(4, 10)
            if random.random() < 0.5 and self.fala is None:
                self.fala = Fala(self.x, self.y-10, random.choice(FALAS_MORADORA),
                    cor=(255,255,150), dur=2.5, tipo_fala='fem')
        if self.fala:
            self.fala.x = self.x; self.fala.y = self.y - 10
            if not self.fala.atualizar(dt): self.fala = None
    def desenhar(self, camx, camy):
        if not self.ativo: return
        x = self.x - camx
        y = self.y - camy
        # Sombra
        pygame.draw.ellipse(TELA, (0,0,0,90), (x-8, y+8, 16, 6))
        bob = math.sin(self.respirando) * 0.4
        # Pernas
        pygame.draw.rect(TELA, self.cor_calca, (x-5, y+2+bob, 4, 8))
        pygame.draw.rect(TELA, self.cor_calca, (x+1, y+2+bob, 4, 8))
        # Corpo (camisa)
        pygame.draw.rect(TELA, self.cor_camisa, (x-6, y-8+bob, 12, 12))
        # Highlight
        pygame.draw.rect(TELA, tuple(min(255,c+40) for c in self.cor_camisa), (x-6, y-8+bob, 12, 3))
        # Cabeça (com cabelo)
        pygame.draw.circle(TELA, self.cor_pele, (int(x), int(y-12+bob)), 6)
        # Cabelo (topo da cabeça)
        pygame.draw.circle(TELA, (60, 30, 20), (int(x), int(y-14+bob)), 6)
        pygame.draw.circle(TELA, self.cor_pele, (int(x), int(y-10+bob)), 5)
        # Braço esquerdo (levantado segurando bandeira)
        pygame.draw.rect(TELA, self.cor_pele, (x+6, y-18+bob, 4, 12))
        # BRAÇO DIREITO - levanta a bandeira
        braco_x = x + 10
        braco_y = y - 20 + bob
        
        # ===== BANDEIRA DO BRASIL =====
        # Mastro (bastão)
        pygame.draw.line(TELA, (100, 70, 40), (braco_x, braco_y), (braco_x+2, braco_y-25), 2)
        
        # Bandeira retangular com ondulação
        band_x = braco_x + 2
        band_y = braco_y - 25
        band_l = 20
        band_a = 14
        
        # Onda em cada linha vertical da bandeira
        for i in range(band_l):
            # Ondulação - baseada na posição X + tempo
            wave = math.sin(self.fase * 3 + i * 0.4) * 3
            # Pontos da coluna vertical da bandeira
            cor_base = (0, 155, 58)  # Verde Brasil
            # A bandeira tem verde, amarelo e azul
            # Desenha cada coluna com a cor da posição
            for j in range(band_a):
                # Cor baseado na posição (verde > losango amarelo > círculo azul)
                px = band_x + i
                py = band_y + j + wave
                # Formato losango amarelo no meio
                cx_r = band_l // 2  # centro horizontal
                cy_r = band_a // 2  # centro vertical
                # Distância ao centro em relação ao losango
                dx = abs(i - cx_r)
                dy = abs(j - cy_r)
                # Losango: dx/7 + dy/4 <= 1
                if dx * 0.14 + dy * 0.25 <= 1.0:
                    # Círculo azul no centro
                    if dx * 0.25 + dy * 0.4 <= 0.7:
                        cor = (0, 39, 118)  # Azul Brasil
                    else:
                        cor = (255, 223, 0)  # Amarelo Brasil
                else:
                    cor = cor_base  # Verde Brasil
                # Desenha um ponto da bandeira
                pygame.draw.rect(TELA, cor, (px, py, 1, 1))
        
        # Contorno da bandeira (sombra/traço)
        # (não desenha contorno para manter o visual limpo)
        
        # Mão segurando o mastro
        pygame.draw.circle(TELA, self.cor_pele, (int(braco_x), int(braco_y)), 3)
        
        # Fala
        if self.fala: self.fala.desenhar(camx, camy)

class Predio:
    def __init__(self,x,y,larg=180,alt=180):
        self.x,self.y=x,y; self.largura,self.altura=larg,alt
        self.sacadas=[pygame.Rect(x,y-15,larg,15),pygame.Rect(x,y+alt,larg,15),
                      pygame.Rect(x-15,y,15,alt),pygame.Rect(x+larg,y,15,alt)]
        self.porta=pygame.Rect(x+larg//2-20,y+alt-10,40,15)
        m=5; eh=alt//2; ew=larg//2
        self.quartos=[pygame.Rect(x+m,y+m,ew-m*1.5,eh-m*1.5),pygame.Rect(x+ew+m//2,y+m,ew-m*1.5,eh-m*1.5),
                      pygame.Rect(x+m,y+eh+m//2,ew-m*1.5,eh-m*1.5),pygame.Rect(x+ew+m//2,y+eh+m//2,ew-m*1.5,eh-m*1.5)]
        self.cores=[CPQ,CPS,CPC,CPB]; self.moradores=[]
        self.cor_fac=(random.randint(150,200),random.randint(140,180),random.randint(120,160))
        self.altura_3d = random.randint(30, 70)
        # TV em cada quarto
        self.tvs = []
        for q in self.quartos:
            tv_x = q.x + q.w // 2 + random.randint(-5, 5)
            tv_y = q.y + q.h - 15
            self.tvs.append(TV(tv_x, tv_y))
        # Moradora na sacada (topo - 50% de chance)
        self.moradora_bandeira = None
        if random.random() < 0.5:
            # Pega uma sacada aleatória
            sac = random.choice(self.sacadas)
            mx = sac.x + sac.w // 2
            my = sac.y + sac.h // 2
            self.moradora_bandeira = MoradoraBandeira(mx, my)
    def atualizar(self, dt, horas=12):
        # Atualiza TVs
        for tv in self.tvs: tv.atualizar(dt, horas)
        # Atualiza moradora da bandeira
        if self.moradora_bandeira is not None:
            self.moradora_bandeira.atualizar(dt)
    def desenhar(self,camx,camy,horas=12):
        angulo_sol = (horas - 6) / 12 * math.pi
        offset_sombra_x = math.cos(angulo_sol) * self.altura_3d
        offset_sombra_y = self.altura_3d * 0.4
        sombra_surf = pygame.Surface((self.largura+40, self.altura+40), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, (0,0,0,80), (20, 20, self.largura, self.altura))
        TELA.blit(sombra_surf, (self.x-camx+offset_sombra_x, self.y-camy+offset_sombra_y))
        cor_topo = (min(255, self.cor_fac[0]+40), min(255, self.cor_fac[1]+40), min(255, self.cor_fac[2]+40))
        cor_lateral = (max(0, self.cor_fac[0]-30), max(0, self.cor_fac[1]-30), max(0, self.cor_fac[2]-30))
        pygame.draw.rect(TELA, cor_topo, (self.x-camx-6, self.y-camy-6, self.largura+12, self.altura+12), border_radius=3)
        pygame.draw.rect(TELA, self.cor_fac, (self.x-camx, self.y-camy, self.largura, self.altura))
        pygame.draw.rect(TELA, cor_lateral, (self.x-camx+self.largura-8, self.y-camy, 8, self.altura))
        pygame.draw.rect(TELA,PT,(self.x-camx,self.y-camy,self.largura,self.altura),3)
        # Desenha quartos
        for i,q in enumerate(self.quartos):
            cor_q = self.cores[i]
            if 19 <= horas or horas < 5: cor_q = tuple(min(255, c+60) for c in cor_q)
            pygame.draw.rect(TELA,cor_q,(q.x-camx,q.y-camy,q.w,q.h))
            pygame.draw.rect(TELA,PT,(q.x-camx,q.y-camy,q.w,q.h),2)
            # Desenha TV do quarto
            if i < len(self.tvs): self.tvs[i].desenhar(camx, camy)
        # Sacadas
        for s in self.sacadas:
            pygame.draw.rect(TELA,CSA,(s.x-camx,s.y-camy,s.w,s.h))
            pygame.draw.rect(TELA,PT,(s.x-camx,s.y-camy,s.w,s.h),2)
            # Grades (visual)
            if s.w > s.h:
                for gx in range(s.x+8, s.x+s.w-4, 15):
                    pygame.draw.line(TELA, PT, (gx-camx, s.y-camy), (gx-camx, s.y+s.h-camy), 1)
            else:
                for gy in range(s.y+8, s.y+s.h-4, 15):
                    pygame.draw.line(TELA, PT, (s.x-camx, gy-camy), (s.x+s.w-camx, gy-camy), 1)
        # Porta
        pygame.draw.rect(TELA,(100,60,30),(self.porta.x-camx,self.porta.y-camy,self.porta.w,self.porta.h))
        # MORADORA COM BANDEIRA (por cima das sacadas)
        if self.moradora_bandeira is not None:
            self.moradora_bandeira.desenhar(camx, camy)

class Fala:
    def __init__(self,x,y,txt,cor=CB,dur=3.0,som=True,tipo_fala='masc'):
        self.x,self.y=x,y; self.txt=txt; self.cor=cor; self.tv=dur; self.ta=0; self.offset_y = 0
        if som and pode_tocar('fala',0.35):
            s='fala_fem' if tipo_fala=='fem' else ('crianca' if tipo_fala=='crianca' else 'fala')
            tocar(s,'fala',0.25)
    def atualizar(self,dt):
        self.ta+=dt; self.offset_y = math.sin(self.ta * 4) * 3
        return self.ta<self.tv
    def desenhar(self,camx,camy):
        if self.ta>=self.tv: return
        a=min(255,int(255*(1-self.ta/self.tv)+100))
        ts=FF.render(self.txt,True,PT)
        lb=ts.get_width()+16; ab=ts.get_height()+16
        bx=self.x-camx-lb//2; by=self.y-camy-60-ab+self.offset_y
        b=pygame.Surface((lb,ab),pygame.SRCALPHA)
        pygame.draw.rect(b,(*self.cor,a),(0,0,lb,ab),border_radius=8)
        pygame.draw.rect(b,(0,0,0,a),(0,0,lb,ab),2,border_radius=8)
        ts.set_alpha(a); b.blit(ts,(8,8)); TELA.blit(b,(bx,by))

class Morador:
    def __init__(self,p):
        self.predio=p; q=random.choice(p.quartos)
        self.x=q.x+q.w//2; self.y=q.y+q.h//2
        self.cor=random.choice([(100,50,150),(50,100,150),(150,100,50),(100,150,100)])
        self.calca=(50,50,80); self.vel=1.0; self.est='dentro'; self.dest=None
        self.te=0; self.de=random.uniform(3,8); self.cel=False; self.fala=None
        self.vida=100.0; self.th=0; self.tp=0; self.fase=0; self.tempo_fala=random.uniform(5,15)
        self.respirando = random.uniform(0, 6.28)
    def atualizar(self,dt):
        self.te+=dt; self.tempo_fala-=dt; self.respirando += dt*2
        if self.th>0: self.th-=dt
        if self.tempo_fala<=0:
            self.tempo_fala=random.uniform(8,20)
            if random.random()<0.4 and self.fala is None:
                self.fala=Fala(self.x,self.y,random.choice(FALAS_MOR),cor=(220,240,255),dur=2.5,som=True,
                    tipo_fala='fem' if random.random()<0.5 else 'masc')
        if self.te>self.de:
            self.te=0; self.de=random.uniform(3,8); self.cel=False
            if self.est=='dentro':
                r=random.random()
                if r<0.4:
                    self.est='indo_sacada'; s=random.choice(self.predio.sacadas); self.dest=(s.x+s.w//2,s.y+s.h//2)
                elif r<0.7: self.cel=True; self.de=random.uniform(3,5)
            elif self.est=='na_sacada':
                self.est='voltando'; q=random.choice(self.predio.quartos); self.dest=(q.x+q.w//2,q.y+q.h//2)
            elif self.est=='indo_sacada': self.est='na_sacada'; self.de=random.uniform(3,8)
            elif self.est=='voltando': self.est='dentro'; self.de=random.uniform(3,10)
        if self.dest and self.est in ('indo_sacada','voltando'):
            dx=self.dest[0]-self.x; dy=self.dest[1]-self.y; d=math.hypot(dx,dy)
            if d>3:
                self.x+=(dx/d)*self.vel; self.y+=(dy/d)*self.vel
                self.tp+=dt; self.fase+=dt*8
                if self.tp>0.4:
                    self.tp=0
                    if pode_tocar('passo',0.3): tocar('passo','passos',0.15)
            else: self.dest=None
        if self.fala:
            self.fala.x=self.x; self.fala.y=self.y
            if not self.fala.atualizar(dt): self.fala=None
    def desenhar(self,camx,camy):
        pygame.draw.ellipse(TELA,(0,0,0,90),(self.x-camx-9,self.y-camy+9,18,7))
        bob = math.sin(self.respirando) * 0.5
        off=math.sin(self.fase)*3 if self.dest else 0
        pygame.draw.rect(TELA,self.calca,(self.x-camx-4+off,self.y-camy+4,3,7))
        pygame.draw.rect(TELA,self.calca,(self.x-camx+1-off,self.y-camy+4,3,7))
        pygame.draw.rect(TELA,self.cor,(self.x-camx-5,self.y-camy-5+bob,10,10))
        pygame.draw.rect(TELA,tuple(min(255,c+40) for c in self.cor),(self.x-camx-5,self.y-camy-5+bob,10,3))
        cc=PE if self.th<=0 else (255,100,100)
        pygame.draw.circle(TELA,cc,(int(self.x-camx),int(self.y-camy-7+bob)),5)
        pygame.draw.circle(TELA,(min(255,cc[0]+30),min(255,cc[1]+30),min(255,cc[2]+30)),(int(self.x-camx-2),int(self.y-camy-9+bob)),2)
        if self.cel: pygame.draw.rect(TELA,CCN,(self.x-camx+5,self.y-camy-3+bob,6,9),border_radius=1)
        if self.vida<100:
            bx=self.x-camx-12; by=self.y-camy-18
            pygame.draw.rect(TELA,(100,0,0),(bx,by,24,4))
            pygame.draw.rect(TELA,(0,255,0),(bx,by,int(24*(self.vida/100)),4))
        if self.fala: self.fala.desenhar(camx,camy)

class Clima:
    def __init__(self):
        self.tipos=['sol','chuva','frio']; self.atual=random.choice(self.tipos)
        self.prox=random.choice(self.tipos); self.tmud=600; self.cont=0
        self.gotas=[]; self.flocos=[]; self.tg=0; self.temp=random.randint(15,35)
    def atualizar(self,dt,h):
        self.cont+=dt
        if self.cont>self.tmud:
            self.cont=0; self.atual=self.prox; self.prox=random.choice(self.tipos)
            if self.atual=='sol': self.temp=random.randint(28,38)
            elif self.atual=='chuva': self.temp=random.randint(18,25)
            else: self.temp=random.randint(5,15)
        if self.atual=='chuva':
            self.tg+=dt
            if self.tg>0.02:
                self.tg=0
                for _ in range(3): self.gotas.append([random.randint(0,LARGURA_TELA),-10,random.uniform(12,20)])
        elif self.atual=='frio':
            self.tg+=dt
            if self.tg>0.15:
                self.tg=0
                self.flocos.append([random.randint(0,LARGURA_TELA),-10,random.uniform(1,3),random.uniform(-1,1)])
        for g in self.gotas[:]:
            g[1]+=g[2]
            if g[1]>ALTURA_TELA: self.gotas.remove(g)
        for f in self.flocos[:]:
            f[1]+=f[2]; f[0]+=f[3]
            if f[1]>ALTURA_TELA: self.flocos.remove(f)
    def desenhar(self):
        SC.fill((0,0,0,0))
        if self.atual=='chuva':
            SC.fill((30,50,90,80)); TELA.blit(SC,(0,0))
            for g in self.gotas: pygame.draw.line(TELA,ACH,(g[0],g[1]),(g[0]-2,g[1]+12),2)
        elif self.atual=='frio':
            SC.fill((100,150,220,70)); TELA.blit(SC,(0,0))
            for f in self.flocos: pygame.draw.circle(TELA,BR,(int(f[0]),int(f[1])),int(f[2])+1)
        elif self.atual=='sol':
            SC.fill((255,220,100,25)); TELA.blit(SC,(0,0))
    def nome(self,t=None): return {'sol':'Ensolarado','chuva':'Chuvoso','frio':'Frio'}[t or self.atual]

def desenhar_ceu(camx, camy, horas):
    if 5 <= horas < 7: top = (255, 150, 100); bot = (255, 200, 150)
    elif 7 <= horas < 17: top = (100, 180, 255); bot = (200, 230, 255)
    elif 17 <= horas < 19: top = (255, 100, 50); bot = (255, 180, 100)
    elif 19 <= horas < 21: top = (30, 20, 80); bot = (100, 50, 100)
    else: top = (5, 5, 20); bot = (20, 20, 50)
    if camy < 300:
        for i in range(0, ALTURA_TELA, 4):
            t = i / ALTURA_TELA
            r = int(top[0]*(1-t) + bot[0]*t); g = int(top[1]*(1-t) + bot[1]*t); b = int(top[2]*(1-t) + bot[2]*t)
            pygame.draw.rect(TELA, (r,g,b), (0, i, LARGURA_TELA, 4))
        if horas >= 19 or horas < 6:
            for e in ESTRELAS:
                twinkle = math.sin(pygame.time.get_ticks()/300 + e['twinkle']) * 0.3 + 0.7
                br = int(255 * e['brilho'] * twinkle)
                pygame.draw.circle(TELA, (br, br, br), (int(e['x']), int(e['y'])), e['tam'])
        if 6 <= horas < 18:
            prog = (horas - 6) / 12
            sol_x = LARGURA_TELA * prog; sol_y = 100 + math.sin(prog * math.pi) * -50
            for i in range(5, 0, -1): pygame.draw.circle(TELA, (255, 255, 200), (int(sol_x), int(sol_y)), 40 + i*5)
            pygame.draw.circle(TELA, (255, 240, 100), (int(sol_x), int(sol_y)), 40)
        else:
            prog = ((horas + 6) % 24 - 6) / 12
            lua_x = LARGURA_TELA * (1 - prog); lua_y = 100 + math.sin(prog * math.pi) * -50
            pygame.draw.circle(TELA, (200, 200, 220), (int(lua_x), int(lua_y)), 30)
            pygame.draw.circle(TELA, (230, 230, 250), (int(lua_x-8), int(lua_y-8)), 20)
        for n in NUVENS:
            nx = (n['x'] - camx * n['alt']) % (TM + 1000) - 500
            ny = (n['y'] - camy * n['alt']) % (ALTURA_TELA + 400) - 200
            if -300 < nx < LARGURA_TELA + 300 and -300 < ny < ALTURA_TELA + 300:
                sombra = pygame.Surface((n['tam']*2, n['tam']//2), pygame.SRCALPHA)
                for i in range(4):
                    pygame.draw.circle(sombra, (255,255,255,180), (n['tam']//2 + i*20 - 40, n['tam']//4), n['tam']//5)
                TELA.blit(sombra, (int(nx), int(ny)))

def loading():
    TELA.fill(PT)
    try:
        img=pygame.image.load("maracana.jpg"); img=pygame.transform.scale(img,(LARGURA_TELA,ALTURA_TELA)); TELA.blit(img,(0,0))
        ov=pygame.Surface((LARGURA_TELA,ALTURA_TELA)); ov.set_alpha(160); ov.fill((0,0,0)); TELA.blit(ov,(0,0))
    except: TELA.fill((10,20,40))
    for i in range(6, 0, -1):
        t_shadow=FL.render("FINAL COPA DO BRASIL",True,(100+i*20, 80+i*20, 0))
        TELA.blit(t_shadow,(LARGURA_TELA//2-t_shadow.get_width()//2+i-3, 60+i-3))
    t=FL.render("FINAL COPA DO BRASIL",True,AB); TELA.blit(t,(LARGURA_TELA//2-t.get_width()//2,60))
    s=FT.render("PALMEIRAS x GREMIO - Bandeira do Brasil",True,BR); TELA.blit(s,(LARGURA_TELA//2-s.get_width()//2,135))
    aviso=FAM.render("+50 Predios | TVs animadas | Moradora com Bandeira!",True,(100,255,255))
    TELA.blit(aviso,(LARGURA_TELA//2-aviso.get_width()//2,180))
    bw=600; bx=LARGURA_TELA//2-bw//2; by=ALTURA_TELA-130
    pygame.draw.rect(TELA,CE,(bx,by,bw,30),border_radius=15)
    for p in range(0,101,2):
        for e in pygame.event.get():
            if e.type==pygame.QUIT: return False
        pygame.draw.rect(TELA,VB,(bx,by,int(bw*p/100),30),border_radius=15)
        pygame.draw.rect(TELA,(100,255,100),(bx,by,int(bw*p/100),10),border_radius=15)
        pygame.draw.rect(TELA,PT,(bx,by,bw,30),3,border_radius=15)
        txt=FT.render(f"{p}%",True,BR); TELA.blit(txt,(LARGURA_TELA//2-txt.get_width()//2,by+35))
        d=FD.render("V: 1a Pessoa | Y: Carro | R: Radio | SHIFT: Celular | ESPACO: Socar",True,CL)
        TELA.blit(d,(LARGURA_TELA//2-d.get_width()//2,ALTURA_TELA-70))
        pygame.display.flip(); pygame.time.delay(15)
    return True

class Particula:
    def __init__(self,x,y,tipo='fumaca',cor=None,com_som=False):
        self.x,self.y=x,y; self.tipo=tipo; self.tv=0
        if tipo=='fumaca':
            self.cor=cor or VFU; self.vx=random.uniform(-30,30); self.vy=random.uniform(-60,-20)
            self.tam=random.randint(15,30); self.vm=random.uniform(2.5,4.5)
        elif tipo in ('rojão','rojao'):
            self.cor=cor or VRO; self.vx=random.uniform(-50,50); self.vy=random.uniform(-300,-200)
            self.tam=5; self.vm=random.uniform(1.5,2.5); self.expl=False
            if com_som and pode_tocar('fogo',0.5): tocar('fogo','efeitos',0.35)
        elif tipo=='sangue':
            self.cor=cor or SANGUE; self.vx=random.uniform(-80,80); self.vy=random.uniform(-80,0)
            self.tam=random.randint(2,4); self.vm=random.uniform(0.5,1.5)
        elif tipo=='faisca':
            self.cor=cor or (255,200,50); self.vx=random.uniform(-150,150); self.vy=random.uniform(-150,150)
            self.tam=random.randint(2,4); self.vm=random.uniform(0.3,0.6)
        elif tipo=='poeira':
            self.cor=cor or (200,180,150); self.vx=random.uniform(-30,30); self.vy=random.uniform(-30,-10)
            self.tam=random.randint(4,8); self.vm=random.uniform(0.5,1.0)
        elif tipo=='folha':
            self.cor=cor or random.choice([(100,200,80),(150,220,100),(200,200,80)])
            self.vx=random.uniform(-40,40); self.vy=random.uniform(-20,20)
            self.tam=random.randint(3,5); self.vm=random.uniform(3.0,5.0)
        elif tipo=='confete':
            self.cor=cor or random.choice([(255,100,100),(100,255,100),(100,100,255),(255,255,100),(255,100,255),(100,255,255)])
            self.vx=random.uniform(-100,100); self.vy=random.uniform(-200,-50)
            self.tam=random.randint(2,4); self.vm=random.uniform(2.0,4.0)
        else:
            self.cor=cor or VFG; a=random.uniform(0,2*math.pi); v=random.uniform(80,350)
            self.vx=math.cos(a)*v; self.vy=math.sin(a)*v; self.tam=random.randint(3,6); self.vm=random.uniform(1.5,3)
    def atualizar(self,dt):
        self.tv+=dt; self.x+=self.vx*dt; self.y+=self.vy*dt
        if self.tipo=='fumaca': self.tam+=20*dt; self.vy+=10*dt; self.vx*=0.98
        elif self.tipo in ('rojão','rojao'):
            self.vy+=400*dt
            if not self.expl and self.vy>0:
                self.expl=True; self.cor=random.choice([(255,100,100),(255,200,100),(255,255,100)]); self.tam=40
        elif self.tipo in ('sangue','faisca'): self.vy+=300*dt
        elif self.tipo=='poeira': self.vy+=5*dt; self.vx*=0.95; self.tam+=5*dt
        elif self.tipo=='folha': 
            self.vy+=10*dt; self.vx += random.uniform(-20,20)*dt; self.vx *= 0.98
        elif self.tipo=='confete':
            self.vy += 100*dt; self.vx += math.sin(self.tv*5) * 30 * dt
        else: self.vy+=50*dt; self.vx*=0.97
        return self.tv<self.vm
    def desenhar(self,camx,camy):
        a=max(0,int(255*(1-self.tv/self.vm)))
        if self.tipo=='fumaca': a=int(a*0.7)
        s=pygame.Surface((int(self.tam*2),int(self.tam*2)),pygame.SRCALPHA)
        pygame.draw.circle(s,(*self.cor,a),(int(self.tam),int(self.tam)),int(self.tam))
        TELA.blit(s,(self.x-camx-self.tam,self.y-camy-self.tam))

class Fanatico:
    def __init__(self,x,y,t):
        self.x,self.y=x+random.randint(-80,80),y+random.randint(-80,80)
        self.cor=VP if t=='palmeiras' else AG
        self.vx=random.uniform(-1,1); self.vy=random.uniform(-1,1); self.tp=0; self.fase=0; self.fala=None
        self.salto = 0
        self.tempo_fala = random.uniform(2, 8)
        self.rojão = None
        if random.random() < 0.6:
            self.rojão = RojaoMao(self, t)
    def atualizar(self,dt):
        if random.random()<0.02: self.vx=random.uniform(-1.5,1.5); self.vy=random.uniform(-1.5,1.5)
        self.x+=self.vx*2; self.y+=self.vy*2; self.fase+=dt*10; self.tp+=dt
        self.salto = abs(math.sin(self.fase*0.8)) * 4 if random.random() < 0.3 else 0
        if self.tp>0.4:
            self.tp=0
            if pode_tocar('passo',0.1): tocar('passo','passos',0.1)
        self.tempo_fala -= dt
        if self.tempo_fala <= 0:
            self.tempo_fala = random.uniform(5, 15)
            if random.random() < 0.3 and self.fala is None:
                if self.rojão is not None and random.random() < 0.5:
                    self.fala = Fala(self.x, self.y, random.choice(FALAS_ROJAO), cor=(255,200,100), dur=2.5,
                        tipo_fala='fem' if random.random()<0.5 else 'masc')
                else:
                    self.fala = Fala(self.x, self.y, random.choice(FALAS_PED), cor=(255,240,200), dur=2.5, 
                        tipo_fala='fem' if random.random()<0.5 else 'masc')
        if self.fala:
            self.fala.x=self.x; self.fala.y=self.y
            if not self.fala.atualizar(dt): self.fala=None
    def atualizar_rojão(self, dt, fumacas_ref):
        if self.rojão is not None:
            if not self.rojão.atualizar(dt, fumacas_ref):
                self.rojão = None
    def desenhar(self,camx,camy):
        pygame.draw.ellipse(TELA,(0,0,0,90),(self.x-camx-7,self.y-camy+8,14,5))
        off=math.sin(self.fase)*2
        y_off = -self.salto
        pygame.draw.rect(TELA,(30,30,30),(self.x-camx-3+off,self.y-camy+4+y_off,3,6))
        pygame.draw.rect(TELA,(30,30,30),(self.x-camx-off,self.y-camy+4+y_off,3,6))
        pygame.draw.rect(TELA,self.cor,(self.x-camx-7,self.y-camy-6+y_off,14,12))
        pygame.draw.rect(TELA,tuple(min(255,c+40) for c in self.cor),(self.x-camx-7,self.y-camy-6+y_off,14,3))
        pygame.draw.circle(TELA,PE,(int(self.x-camx),int(self.y-camy-12+y_off)),6)
        if self.rojão is not None:
            self.rojão.desenhar_na_mao(camx,camy)
        if self.fala: self.fala.desenhar(camx,camy)

class Torcida:
    def __init__(self,x,y,t):
        self.x,self.y=x,y; self.t=t; self.cor=VP if t=='palmeiras' else AG
        self.fas=[Fanatico(x,y,t) for _ in range(25)]
        self.tf=0; self.tr=0; self.tfala=0
    def atualizar(self,dt,part,fumacas_ref=None):
        for f in self.fas: 
            f.atualizar(dt)
            if fumacas_ref is not None:
                f.atualizar_rojão(dt, fumacas_ref)
        if self.t=='palmeiras':
            self.tf+=dt
            if self.tf>0.15:
                self.tf=0; part.append(Particula(self.x+random.randint(-100,100),self.y+random.randint(-60,60),'fumaca',VFU))
            self.tr+=dt
            if self.tr>1.5:
                self.tr=0; part.append(Particula(self.x+random.randint(-100,100),self.y+random.randint(-60,60),'rojão',VRO,com_som=True))
        self.tfala+=dt
        if self.tfala>random.uniform(3,7):
            self.tfala=0
            for f in self.fas:
                if f.fala is None:
                    f.fala=Fala(f.x,f.y,random.choice(FALAS_PED),cor=(255,240,200),dur=2.5,tipo_fala='fem' if random.random()<0.5 else 'masc')
                    break
    def desenhar(self,camx,camy):
        for f in self.fas: f.desenhar(camx,camy)

class Briga:
    def __init__(self,x,y):
        self.x,self.y=x,y; self.tv=0; self.dur=random.uniform(8,15); self.sep=False
    def atualizar(self,dt):
        self.tv+=dt; return self.tv<self.dur and not self.sep
    def desenhar(self,camx,camy):
        pulse = int(abs(math.sin(pygame.time.get_ticks()/200))*30)+70
        pygame.draw.circle(TELA,(255,pulse-50,pulse-50),(int(self.x-camx),int(self.y-camy)),100,3)
        pygame.draw.circle(TELA,(255,0,0),(int(self.x-camx),int(self.y-camy)),100,1)

class Chat:
    def __init__(self):
        self.msgs=[]; self.tu=0; self.iv=3.0
        self.nomes=["PalmeirenseBR","GremistaRS","Verdao","GremioCamp","UberMot","CariocaGamer","PM_RJ","Torcedor10"]
        self.ufp=0; self.ifp=3.0
    def atualizar(self,dt,j,ped):
        self.tu+=dt
        if self.tu>self.iv:
            self.tu=0; self.iv=random.uniform(3,6)
            msg_pool = FALAS_CHAT + ["Rojão verde!","Fumaça branca!","Rojão azul!","Olha a bandeira!","Viva o Brasil!"]
            self.msgs.append((random.choice(self.nomes),random.choice(msg_pool),random.choice([(100,200,255),(200,255,100),(255,200,100)]),pygame.time.get_ticks()))
            if pode_tocar('notificacao',5): tocar('notificacao','notificacao',0.4)
        if len(self.msgs)>8: self.msgs.pop(0)
        ag=pygame.time.get_ticks(); self.msgs=[m for m in self.msgs if ag-m[3]<15000]
        self.ufp+=dt
        if self.ufp>self.ifp:
            self.ufp=0; self.ifp=random.uniform(2,4)
            for p in ped:
                if math.hypot(p.x-j.x,p.y-j.y)<250 and random.random()<0.4 and p.fala is None:
                    p.fala=Fala(p.x,p.y,random.choice(FALAS_PED),dur=2.5,tipo_fala='fem' if random.random()<0.5 else 'masc'); break
    def desenhar(self):
        if not self.msgs: return
        al=22; lc=340; xb=LARGURA_TELA-lc-20; yb=ALTURA_TELA-100-len(self.msgs)*al
        f=pygame.Surface((lc,len(self.msgs)*al+20),pygame.SRCALPHA)
        pygame.draw.rect(f,(0,0,0,140),(0,0,lc,len(self.msgs)*al+20),border_radius=10)
        TELA.blit(f,(xb-5,yb-10))
        t=FC.render("Chat Online (BR)",True,CCO); TELA.blit(t,(xb,yb-30))
        for i,(n,x,c,_) in enumerate(self.msgs):
            y=yb+i*al
            tn=FC.render(f"{n}:",True,c); tm=FC.render(x,True,BR)
            TELA.blit(tn,(xb,y)); TELA.blit(tm,(xb+tn.get_width()+5,y))

class Sem:
    def __init__(self,x,y,h=True):
        self.x,self.y=x,y; self.h=h; self.e=0; self.t=0
    def atualizar(self,dt):
        self.t+=dt
        if self.e==0 and self.t>5: self.e=1; self.t=0
        elif self.e==1 and self.t>2: self.e=2; self.t=0
        elif self.e==2 and self.t>5: self.e=0; self.t=0
    def desenhar(self,camx,camy):
        c=(0,255,0) if self.e==0 else((255,255,0) if self.e==1 else(255,0,0))
        pygame.draw.rect(TELA,PT,(self.x-camx-6,self.y-camy-25,12,35),border_radius=3)
        pygame.draw.circle(TELA,tuple(min(255,v+30) for v in c),(int(self.x-camx),int(self.y-camy-12)),7)
        pygame.draw.circle(TELA,c,(int(self.x-camx),int(self.y-camy-12)),6)

class SemM:
    def __init__(self,x,y):
        self.x,self.y=x,y; self.e=0
    def atualizar(self,m): self.e=2 if abs(m.x-self.x)<350 else 0
    def desenhar(self,camx,camy):
        c=(0,255,0) if self.e==0 else(255,0,0)
        pygame.draw.rect(TELA,PT,(self.x-camx-6,self.y-camy-25,12,35),border_radius=3)
        pygame.draw.circle(TELA,tuple(min(255,v+30) for v in c),(int(self.x-camx),int(self.y-camy-12)),7)
        pygame.draw.circle(TELA,c,(int(self.x-camx),int(self.y-camy-12)),6)

class Celular:
    def __init__(self):
        self.min=True; self.x=20; self.y=80; self.larg=350; self.alt=700
        self.cor=LI; self.app='home'; self.cf=1; self.tuf=0; self.mf=False
    def desenhar(self,t,rel=None,cl=None):
        if self.min:
            pygame.draw.rect(t,self.cor,(10,80,40,60),border_radius=10)
            pygame.draw.rect(t,PT,(12,82,36,56),border_radius=8)
            for i in range(3): pygame.draw.rect(t,self.cor,(20,95+i*12,20,3))
            return
        pygame.draw.rect(t,(0,0,0,80),(self.x+8,self.y+8,self.larg,self.alt),border_radius=30)
        pygame.draw.rect(t,self.cor,(self.x,self.y,self.larg,self.alt),border_radius=30)
        pygame.draw.rect(t,PT,(self.x,self.y,self.larg,self.alt),5,border_radius=30)
        pygame.draw.rect(t,(255,200,150),(self.x+3,self.y+30,4,self.alt-60),border_radius=2)
        pygame.draw.rect(t,PT,(self.x+120,self.y,100,25),border_radius=10)
        tr=pygame.Rect(self.x+10,self.y+30,self.larg-20,self.alt-40)
        pygame.draw.rect(t,(20,20,20),tr,border_radius=20)
        if self.app=='home': self.draw_home(t,tr)
        elif self.app=='camera': self.draw_cam(t,tr)
        elif self.app=='mapa': self.draw_mapa(t,tr)
        elif self.app=='galeria': self.draw_gal(t,tr)
        elif self.app=='config': self.draw_cfg(t,tr)
        elif self.app=='tempo': self.draw_temp(t,tr,cl)
        elif self.app=='relogio': self.draw_rel(t,tr,rel)
        pygame.draw.circle(t,BR,(self.x+self.larg//2,self.y+self.alt-20),15)
        pygame.draw.circle(t,CZ,(self.x+self.larg//2,self.y+self.alt-20),15,2)
    def draw_home(self,t,r):
        apps=[("WhatsApp",(37,211,102),(r.x+20,r.y+20)),("YouTube",(255,0,0),(r.x+130,r.y+20)),
              ("Telefone",(0,150,0),(r.x+240,r.y+20)),("Contatos",(0,100,200),(r.x+20,r.y+140)),
              ("Camera",(60,60,60),(r.x+130,r.y+140)),("Fotos",(255,255,255),(r.x+240,r.y+140)),
              ("Mapa",(34,139,34),(r.x+20,r.y+260)),("Galeria",(200,150,200),(r.x+130,r.y+260)),
              ("Musica",(255,100,200),(r.x+240,r.y+260)),("Tempo",(100,180,255),(r.x+20,r.y+380)),
              ("Relogio",(50,50,50),(r.x+130,r.y+380)),("Uber",(0,0,0),(r.x+240,r.y+380))]
        for nome,c,p in apps:
            pygame.draw.rect(t,(0,0,0,60),(p[0]+3,p[1]+3,90,90),border_radius=18)
            pygame.draw.rect(t,c,(p[0],p[1],90,90),border_radius=18)
            hl = tuple(min(255,v+50) for v in c)
            pygame.draw.rect(t,hl,(p[0]+5,p[1]+5,80,15),border_radius=10)
            if nome=="WhatsApp":
                pygame.draw.circle(t,BR,(p[0]+45,p[1]+45),22); pygame.draw.circle(t,(37,211,102),(p[0]+45,p[1]+45),17)
            elif nome=="YouTube": pygame.draw.polygon(t,BR,[(p[0]+35,p[1]+30),(p[0]+60,p[1]+45),(p[0]+35,p[1]+60)])
            elif nome=="Telefone": pygame.draw.circle(t,BR,(p[0]+45,p[1]+45),22); pygame.draw.rect(t,(0,150,0),(p[0]+35,p[1]+35,20,20))
            elif nome=="Contatos": pygame.draw.circle(t,BR,(p[0]+45,p[1]+35),18); pygame.draw.rect(t,BR,(p[0]+25,p[1]+58,40,20))
            elif nome=="Camera": pygame.draw.rect(t,PT,(p[0]+22,p[1]+35,46,32),border_radius=6); pygame.draw.circle(t,(150,150,200),(p[0]+45,p[1]+51),10)
            elif nome=="Fotos":
                for i,c2 in enumerate([(255,0,0),(0,255,0),(0,0,255)]): pygame.draw.circle(t,c2,(p[0]+45,p[1]+45),20-i*6)
            elif nome=="Mapa": pygame.draw.circle(t,BR,(p[0]+45,p[1]+45),22); pygame.draw.circle(t,(0,100,0),(p[0]+45,p[1]+45),18)
            elif nome=="Galeria":
                pygame.draw.rect(t,(255,100,100),(p[0]+15,p[1]+15,25,25)); pygame.draw.rect(t,(100,200,100),(p[0]+50,p[1]+15,25,25))
            elif nome=="Musica": pygame.draw.circle(t,BR,(p[0]+45,p[1]+45),22); pygame.draw.circle(t,(255,100,200),(p[0]+45,p[1]+45),5)
            elif nome=="Tempo":
                pygame.draw.circle(t,ASol,(p[0]+45,p[1]+45),18)
                for i in range(8):
                    a=math.radians(i*45)
                    pygame.draw.line(t,ASol,(p[0]+45+math.cos(a)*20,p[1]+45+math.sin(a)*20),(p[0]+45+math.cos(a)*28,p[1]+45+math.sin(a)*28),3)
            elif nome=="Relogio": pygame.draw.circle(t,BR,(p[0]+45,p[1]+45),30); pygame.draw.circle(t,PT,(p[0]+45,p[1]+45),30,3)
            elif nome=="Uber": pygame.draw.rect(t,BR,(p[0]+20,p[1]+40,50,12))
            txt=FApp.render(nome,True,BR if c!=(255,255,255) else PT)
            t.blit(txt,(p[0]+45-txt.get_width()//2,p[1]+95))
    def draw_cam(self,t,r):
        pygame.draw.rect(t,PT,r,border_radius=20)
        v=pygame.Rect(r.x+15,r.y+50,r.width-30,r.height-180); pygame.draw.rect(t,(30,30,30),v)
        try:
            reg=pygame.Rect(LARGURA_TELA//2-100,ALTURA_TELA//2-80,200,160)
            cap=t.subsurface(reg); cap=pygame.transform.scale(cap,(v.width,v.height)); t.blit(cap,(v.x,v.y))
        except: pass
        pygame.draw.rect(t,BR,v,2); pygame.draw.circle(t,BR,(r.centerx,r.bottom-80),35)
        txt=FApp.render("C = Tirar Foto",True,BR); t.blit(txt,(r.centerx-txt.get_width()//2,r.y+15))
    def draw_mapa(self,t,r):
        pygame.draw.rect(t,(180,210,180),r,border_radius=20)
        for i in range(10):
            x=r.x+i*(r.width//10); pygame.draw.line(t,(200,200,200),(x,r.y),(x,r.bottom),2)
        pygame.draw.circle(t,BR,(r.centerx,r.centery),50); pygame.draw.circle(t,AB,(r.centerx,r.centery),35); pygame.draw.circle(t,VC,(r.centerx,r.centery),20)
    def draw_gal(self,t,r):
        pygame.draw.rect(t,(40,40,40),r,border_radius=20)
        for i in range(9):
            col=i%3; lin=i//3; x=r.x+20+col*97; y=r.y+70+lin*97
            pygame.draw.rect(t,(80,80,80),(x,y,85,85),border_radius=8)
            a=f"foto_{i+1}.png"
            if os.path.exists(a):
                try: im=pygame.image.load(a); im=pygame.transform.scale(im,(81,81)); t.blit(im,(x+2,y+2))
                except: pass
    def draw_cfg(self,t,r):
        pygame.draw.rect(t,(40,40,40),r,border_radius=20)
        for i,it in enumerate(["Som: ON","WiFi: OK","Bateria: 100%","Idioma: PT-BR","Controles: ON","Camera: HD"]):
            txt=FApp.render(it,True,BR); t.blit(txt,(r.x+25,r.y+80+i*40))
    def draw_temp(self,t,r,cl):
        if not cl: return
        cores={'sol':(60,130,200),'chuva':(40,50,80),'frio':(90,130,180)}
        pygame.draw.rect(t,cores[cl.atual],r,border_radius=20)
        tp=FT.render("Previsao",True,BR); t.blit(tp,(r.x+15,r.y+15))
        if cl.atual=='sol': pygame.draw.circle(t,ASol,(r.centerx,r.y+150),40)
        elif cl.atual=='chuva':
            pygame.draw.circle(t,CL,(r.centerx-25,r.y+140),22); pygame.draw.circle(t,CL,(r.centerx+25,r.y+140),22)
        else:
            for i in range(6):
                a=math.radians(i*60); pygame.draw.line(t,BR,(r.centerx,r.y+150),(r.centerx+math.cos(a)*45,r.y+150+math.sin(a)*45),3)
        tt=FAG.render(f"{cl.temp}C",True,BR); t.blit(tt,(r.centerx-tt.get_width()//2,r.y+230))
        dd=FAM.render(cl.nome(),True,BR); t.blit(dd,(r.centerx-dd.get_width()//2,r.y+285))
    def draw_rel(self,t,r,rel):
        if not rel: return
        pygame.draw.rect(t,(25,25,40),r,border_radius=20)
        cx,cy=r.centerx,r.y+200; ra=110
        pygame.draw.circle(t,(0,0,0,80),(cx+5,cy+5),ra)
        pygame.draw.circle(t,BR,(cx,cy),ra); pygame.draw.circle(t,PT,(cx,cy),ra,5)
        h=rel.get_horas()%12; m=rel.get_minutos()
        ah=math.radians((h*30+m*0.5)-90); pygame.draw.line(t,PT,(cx,cy),(cx+math.cos(ah)*55,cy+math.sin(ah)*55),6)
        am=math.radians(m*6-90); pygame.draw.line(t,PT,(cx,cy),(cx+math.cos(am)*80,cy+math.sin(am)*80),4)
        ht=FAG.render(f"{rel.get_horas():02d}:{rel.get_minutos():02d}",True,BR); t.blit(ht,(r.centerx-ht.get_width()//2,r.y+340))
    def clique(self,pos):
        if self.min: return
        if self.app=='home':
            apps=[("whatsapp",(self.x+30,self.y+50)),("youtube",(self.x+140,self.y+50)),("telefone",(self.x+250,self.y+50)),
                  ("contatos",(self.x+30,self.y+170)),("camera",(self.x+140,self.y+170)),("fotos",(self.x+250,self.y+170)),
                  ("mapa",(self.x+30,self.y+290)),("galeria",(self.x+140,self.y+290)),("musica",(self.x+250,self.y+290)),
                  ("tempo",(self.x+30,self.y+410)),("relogio",(self.x+140,self.y+410)),("uber",(self.x+250,self.y+410))]
            for n,(ax,ay) in apps:
                if ax<pos[0]<ax+90 and ay<pos[1]<ay+90:
                    self.app=n
                    if pode_tocar('notificacao',0.3): tocar('notificacao','notificacao',0.3)
                    return
        if math.hypot(pos[0]-(self.x+self.larg//2),pos[1]-(self.y+self.alt-20))<20: self.app='home'
    def tirar_foto(self,t):
        if self.app=='camera':
            try:
                pygame.image.save(t,f"foto_{self.cf}.png"); self.cf+=1; self.mf=True; self.tuf=pygame.time.get_ticks()
                tocar('notificacao','notificacao',0.4)
            except: pass

class Relogio:
    def __init__(self):
        self.min=18*60; self.vel=1.0; self.dia=1
    def atualizar(self,dt):
        self.min+=self.vel*dt
        if self.min>=1440: self.min-=1440; self.dia+=1
    def get_horas(self): return int(self.min//60)
    def get_minutos(self): return int(self.min%60)
    def fmt(self): return f"Dia {self.dia} - {self.get_horas():02d}:{self.get_minutos():02d}"

class Molecada:
    def __init__(self):
        ang=random.uniform(0,2*math.pi); d=random.randint(800,2000)
        self.x=CX+math.cos(ang)*d; self.y=CY+math.sin(ang)*d
        self.vel=random.uniform(2.5,4.0)
        self.cor_camisa=random.choice([(255,100,100),(100,100,255),(255,255,100),(100,255,100),(255,100,255),(100,255,255)])
        self.cor_bike=random.choice([C_BIKE,(150,50,50),(50,150,50),(50,50,150),(200,100,50)])
        self.fase=0; self.fala=None; self.est='indo'; self.destino=None
        self.tempo_espera=0; self.tp=0; self.vida=100.0
    def atualizar(self,dt,segs):
        if self.fala:
            self.fala.x=self.x; self.fala.y=self.y
            if not self.fala.atualizar(dt): self.fala=None
        if self.est=='indo':
            if self.destino is None:
                ang=random.uniform(0, 2*math.pi)
                self.destino=(CX+math.cos(ang)*(RE+20), CY+math.sin(ang)*(RE+20))
            dx=self.destino[0]-self.x; dy=self.destino[1]-self.y; d=math.hypot(dx,dy)
            if d>30:
                self.x+=(dx/d)*self.vel; self.y+=(dy/d)*self.vel
                self.fase+=dt*8; self.tp+=dt
                if self.tp>0.3:
                    self.tp=0
                    if pode_tocar('bike',0.8): tocar('bike','efeitos',0.15)
            else:
                self.est='esperando'; self.tempo_espera=0
                if random.random()<0.5:
                    self.fala=Fala(self.x,self.y,random.choice(FALAS_MOLE),cor=(255,255,180),dur=2.5,tipo_fala='crianca')
        elif self.est=='esperando':
            self.tempo_espera+=dt
            seg_perto=None
            for s in segs:
                if math.hypot(s.x-self.x,s.y-self.y)<150: seg_perto=s; break
            if seg_perto is not None:
                if random.random()<0.7:
                    self.est='autorizado'; self.tempo_espera=0
                    if random.random()<0.5:
                        self.fala=Fala(self.x,self.y,random.choice(FALAS_SEG_LIBERA),cor=(200,255,200),dur=2.0)
                    tocar('notificacao','notificacao',0.4)
                else:
                    self.est='negado'; self.tempo_espera=0
                    if random.random()<0.5:
                        self.fala=Fala(self.x,self.y,random.choice(FALAS_SEG_NEGA),cor=(255,150,150),dur=2.0)
            if self.tempo_espera>15: self.est='embora'; self.destino=None
        elif self.est=='autorizado':
            if self.destino is None:
                self.destino=(CX+random.randint(-100,100), CY+random.randint(-60,60))
            dx=self.destino[0]-self.x; dy=self.destino[1]-self.y; d=math.hypot(dx,dy)
            if d>15:
                self.x+=(dx/d)*self.vel; self.y+=(dy/d)*self.vel
                self.fase+=dt*8; self.tp+=dt
                if self.tp>0.3:
                    self.tp=0
                    if pode_tocar('bike',0.8): tocar('bike','efeitos',0.12)
            else:
                self.est='jogando'
                if random.random()<0.6:
                    self.fala=Fala(self.x,self.y,"Cheguei! Bora joga bola!",cor=(255,255,180),dur=2.5,tipo_fala='crianca')
        elif self.est=='negado':
            if self.destino is None:
                ang=random.uniform(0,2*math.pi); d=random.randint(1500,2500)
                self.destino=(CX+math.cos(ang)*d, CY+math.sin(ang)*d)
            dx=self.destino[0]-self.x; dy=self.destino[1]-self.y; d=math.hypot(dx,dy)
            if d>30:
                self.x+=(dx/d)*self.vel; self.y+=(dy/d)*self.vel; self.fase+=dt*8
            else: self.est='embora'
        elif self.est=='jogando':
            self.x+=random.uniform(-1.5,1.5); self.y+=random.uniform(-1.5,1.5)
            if abs(self.x-CX)>130: self.x=CX+random.uniform(-130,130)
            if abs(self.y-CY)>90: self.y=CY+random.uniform(-90,90)
            self.fase+=dt*8
            if random.random()<0.005 and self.fala is None:
                self.fala=Fala(self.x,self.y,random.choice(["Gol!","Passa!","Chuta!","Aqui!","Bora!"]),cor=(255,255,180),dur=1.5,tipo_fala='crianca')
        elif self.est=='hora_ir':
            if self.destino is None:
                ang=random.uniform(0, 2*math.pi)
                self.destino=(CX+math.cos(ang)*(RE+40), CY+math.sin(ang)*(RE+40))
            dx=self.destino[0]-self.x; dy=self.destino[1]-self.y; d=math.hypot(dx,dy)
            if d>30:
                self.x+=(dx/d)*self.vel; self.y+=(dy/d)*self.vel
                self.fase+=dt*8; self.tp+=dt
                if self.tp>0.3:
                    self.tp=0
                    if pode_tocar('bike',0.8): tocar('bike','efeitos',0.15)
            else:
                self.est='indo_casa'
                ang=random.uniform(0,2*math.pi); d=random.randint(2000,3000)
                self.destino=(CX+math.cos(ang)*d, CY+math.sin(ang)*d)
        elif self.est=='indo_casa':
            if self.destino is None:
                ang=random.uniform(0,2*math.pi); d=random.randint(2000,3000)
                self.destino=(CX+math.cos(ang)*d, CY+math.sin(ang)*d)
            dx=self.destino[0]-self.x; dy=self.destino[1]-self.y; d=math.hypot(dx,dy)
            if d>30:
                self.x+=(dx/d)*self.vel; self.y+=(dy/d)*self.vel
                self.fase+=dt*8; self.tp+=dt
                if self.tp>0.3:
                    self.tp=0
                    if pode_tocar('bike',0.8): tocar('bike','efeitos',0.15)
            else: self.est='embora'
    def desenhar(self,camx,camy):
        if self.est=='embora': return
        pygame.draw.ellipse(TELA,(0,0,0,90),(self.x-camx-12,self.y-camy+7,24,7))
        mostrar_bike = self.est in ('indo','esperando','autorizado','negado','hora_ir','indo_casa')
        if mostrar_bike:
            pygame.draw.circle(TELA,(30,30,30),(int(self.x-camx-8),int(self.y-camy+4)),6,2)
            pygame.draw.circle(TELA,(30,30,30),(int(self.x-camx+8),int(self.y-camy+4)),6,2)
            pygame.draw.line(TELA,self.cor_bike,(self.x-camx-8,self.y-camy+4),(self.x-camx,self.y-camy-2),2)
            pygame.draw.line(TELA,self.cor_bike,(self.x-camx+8,self.y-camy+4),(self.x-camx,self.y-camy-2),2)
            pygame.draw.line(TELA,self.cor_bike,(self.x-camx-8,self.y-camy+4),(self.x-camx+8,self.y-camy+4),2)
            pygame.draw.rect(TELA,self.cor_camisa,(self.x-camx-5,self.y-camy-8,10,10))
            pygame.draw.rect(TELA,tuple(min(255,c+40) for c in self.cor_camisa),(self.x-camx-5,self.y-camy-8,10,3))
            pygame.draw.circle(TELA,PE,(int(self.x-camx),int(self.y-camy-11)),5)
            off=math.sin(self.fase)*3
            pygame.draw.rect(TELA,(50,50,80),(self.x-camx-3+off,self.y-camy-1,3,5))
            pygame.draw.rect(TELA,(50,50,80),(self.x-camx+1-off,self.y-camy-1,3,5))
        else:
            pygame.draw.ellipse(TELA,(0,0,0,90),(self.x-camx-6,self.y-camy+9,12,5))
            off=math.sin(self.fase)*3
            pygame.draw.rect(TELA,(50,50,80),(self.x-camx-3+off,self.y-camy+4,3,6))
            pygame.draw.rect(TELA,(50,50,80),(self.x-camx+1-off,self.y-camy+4,3,6))
            pygame.draw.rect(TELA,self.cor_camisa,(self.x-camx-5,self.y-camy-5,10,10))
            pygame.draw.rect(TELA,tuple(min(255,c+40) for c in self.cor_camisa),(self.x-camx-5,self.y-camy-5,10,3))
            pygame.draw.circle(TELA,PE,(int(self.x-camx),int(self.y-camy-9)),5)
        if self.fala: self.fala.desenhar(camx,camy)

class Bola:
    def __init__(self):
        self.x=CX; self.y=CY; self.tem_dono=None; self.fase = 0
    def atualizar(self,dt,molecada):
        self.fase += dt * 10
        if self.tem_dono is not None and self.tem_dono.est=='jogando' and self.tem_dono in molecada:
            self.x=self.tem_dono.x; self.y=self.tem_dono.y; return
        self.tem_dono=None; dist_min=999
        for m in molecada:
            if m.est=='jogando':
                d=math.hypot(m.x-self.x,m.y-self.y)
                if d<dist_min: dist_min=d; self.tem_dono=m
        if self.tem_dono:
            dx=self.tem_dono.x-self.x; dy=self.tem_dono.y-self.y; d=math.hypot(dx,dy)
            if d>5:
                self.x+=(dx/d)*150*dt; self.y+=(dy/d)*150*dt
                if random.random()<0.03 and pode_tocar('bola',0.2): tocar('bola','efeitos',0.2)
    def desenhar(self,camx,camy):
        pygame.draw.ellipse(TELA,(0,0,0,120),(self.x-camx-6,self.y-camy+4,12,4))
        pygame.draw.circle(TELA,BR,(int(self.x-camx),int(self.y-camy)),6)
        pygame.draw.circle(TELA,PT,(int(self.x-camx),int(self.y-camy)),6,1)
        pygame.draw.circle(TELA,(200,200,200),(int(self.x-camx-2),int(self.y-camy-2)),3)

class ViaturaPolicia:
    def __init__(self, x, y):
        self.x=x; self.y=y; self.vel=6.5
        self.chegou=False; self.tempo_no_local=0
        self.levando_jogador=False; self.fase=0; self.fala=None; self.pisca=0
    def atualizar(self,dt,jogador,preso):
        self.fase+=dt*8; self.pisca+=dt*6
        if self.levando_jogador:
            dx=DEL_X+DEL_L//2 - self.x; dy=DEL_Y+DEL_A//2 - self.y
            d=math.hypot(dx,dy)
            if d>15:
                self.x+=(dx/d)*self.vel*1.3; self.y+=(dy/d)*self.vel*1.3
            else:
                jogador.x=DEL_X+DEL_L//2; jogador.y=DEL_Y+DEL_A+50
                preso['transportando']=False
            return
        if self.chegou:
            self.tempo_no_local+=dt; return
        dx=jogador.x-self.x; dy=jogador.y-self.y; d=math.hypot(dx,dy)
        if d>10:
            self.x+=(dx/d)*self.vel; self.y+=(dy/d)*self.vel
        if d<70 and not preso['preso']:
            self.chegou=True; preso['preso']=True
            preso['tempo']=pygame.time.get_ticks()
            preso['fase']='algemando'
            self.fala=Fala(self.x,self.y,random.choice(FALAS_POLICIA_RJ),cor=(200,200,255),dur=3.0)
            tocar('sirene','sirene',0.5)
    def desenhar(self,camx,camy):
        pygame.draw.rect(TELA,(0,0,0,100),(self.x-camx+6,self.y-camy+6,70,50),border_radius=6)
        pygame.draw.rect(TELA,AZUL_POLICIA,(self.x-camx,self.y-camy,70,50),border_radius=6)
        pygame.draw.rect(TELA,(60,60,200),(self.x-camx,self.y-camy,70,10),border_radius=6)
        pygame.draw.rect(TELA,BR,(self.x-camx+20,self.y-camy,15,50))
        pygame.draw.rect(TELA,BR,(self.x-camx+40,self.y-camy,5,50))
        pygame.draw.rect(TELA,(100,150,200),(self.x-camx+10,self.y-camy+10,50,30),border_radius=3)
        cor_giro = VERMELHO_POLICIA if int(self.pisca)%2==0 else (100,50,50)
        pygame.draw.circle(TELA,tuple(min(255,v+80) for v in cor_giro),(int(self.x-camx+20),int(self.y-camy-8)),9)
        pygame.draw.circle(TELA,cor_giro,(int(self.x-camx+20),int(self.y-camy-8)),6)
        cor_giro2 = (50,50,150) if int(self.pisca)%2==0 else AMARELO_POLICIA
        pygame.draw.circle(TELA,tuple(min(255,v+80) for v in cor_giro2),(int(self.x-camx+50),int(self.y-camy-8)),9)
        pygame.draw.circle(TELA,cor_giro2,(int(self.x-camx+50),int(self.y-camy-8)),6)
        txt=FApp.render("PM",True,BR)
        TELA.blit(txt,(self.x-camx+30-txt.get_width()//2,self.y-camy+20))
        if self.fala: self.fala.desenhar(camx,camy)

class OnibusTorcida:
    def __init__(self, time):
        self.time = time
        self.cor_principal = VP if time == 'palmeiras' else AG
        self.cor_secundaria = BR if time == 'palmeiras' else (100,180,255)
        self.x = CX - 2000
        self.y = CY + REY - CY + random.randint(100, 300)
        self.vel = 3.0
        self.chegou = False; self.porta_aberta = False
        self.tempo_parado = 0; self.fans_soltos = 0
        self.total_fans = 20
        self.tempo_som_buzina = 0; self.tempo_apito = 0
        if time == 'palmeiras':
            self.destino_x = CX - 600; self.destino_y = CY + RE + 250
        else:
            self.destino_x = CX + 600; self.destino_y = CY + RE + 250
    def atualizar(self, dt, torcidas_ref, particulas_globais, fumacas_ref):
        if not self.chegou:
            self.tempo_som_buzina += dt
            if self.tempo_som_buzina > 2.0:
                self.tempo_som_buzina = 0
                if pode_tocar('buzina', 1.5): tocar('buzina', 'buzina', 0.4)
        if self.chegou and self.porta_aberta and self.fans_soltos < self.total_fans:
            self.tempo_apito += dt
            if self.tempo_apito > 0.5:
                self.tempo_apito = 0
                if pode_tocar('apito', 0.6): tocar('apito', 'apito', 0.3)
            self.tempo_parado += dt
            if self.tempo_parado > 0.3:
                self.tempo_parado = 0
                self.fans_soltos += 1
                for t in torcidas_ref:
                    if t.t == self.time:
                        novo_fan = Fanatico(self.x, self.y, self.time)
                        novo_fan.x = self.x + random.randint(-50, 50)
                        novo_fan.y = self.y + random.randint(-50, 50)
                        t.fas.append(novo_fan)
                        break
                for _ in range(3):
                    particulas_globais.append(Particula(self.x + random.randint(-40,40), self.y - 20, 'fumaca', VFU if self.time=='palmeiras' else (100,150,220)))
        if not self.chegou:
            dx = self.destino_x - self.x; dy = self.destino_y - self.y
            d = math.hypot(dx, dy)
            if d > 20:
                self.x += (dx/d) * self.vel; self.y += (dy/d) * self.vel
                if random.random() < 0.2:
                    particulas_globais.append(Particula(self.x - 40, self.y + 15, 'poeira'))
            else:
                self.chegou = True; self.porta_aberta = True; self.tempo_parado = 0
                tocar('buzina', 'buzina', 0.6)
    def desenhar(self, camx, camy):
        pygame.draw.rect(TELA, (0,0,0,100), (self.x-camx+8, self.y-camy+8, 180, 60), border_radius=8)
        pygame.draw.rect(TELA, self.cor_principal, (self.x-camx-90, self.y-camy-30, 180, 60), border_radius=8)
        pygame.draw.rect(TELA, tuple(min(255,c+40) for c in self.cor_principal), (self.x-camx-90, self.y-camy-30, 180, 12), border_radius=8)
        pygame.draw.rect(TELA, self.cor_secundaria, (self.x-camx-90, self.y-camy-5, 180, 15))
        for i in range(5):
            pygame.draw.rect(TELA, (100,180,220), (self.x-camx-75+i*32, self.y-camy-22, 25, 18), border_radius=3)
            pygame.draw.rect(TELA, (180,220,255), (self.x-camx-72+i*32, self.y-camy-20, 10, 5))
        pygame.draw.circle(TELA, PT, (int(self.x-camx+70), int(self.y-camy+30)), 12)
        pygame.draw.circle(TELA, (80,80,80), (int(self.x-camx+70), int(self.y-camy+30)), 8)
        pygame.draw.circle(TELA, CZ, (int(self.x-camx+70), int(self.y-camy+30)), 3)
        pygame.draw.circle(TELA, PT, (int(self.x-camx-70), int(self.y-camy+30)), 12)
        pygame.draw.circle(TELA, (80,80,80), (int(self.x-camx-70), int(self.y-camy+30)), 8)
        pygame.draw.circle(TELA, CZ, (int(self.x-camx-70), int(self.y-camy+30)), 3)
        if self.porta_aberta:
            pygame.draw.rect(TELA, (30,30,30), (self.x-camx+40, self.y-camy-15, 30, 40))
            pygame.draw.rect(TELA, PT, (self.x-camx+40, self.y-camy-15, 30, 40), 2)
        pygame.draw.circle(TELA, (255,255,200), (int(self.x-camx+85), int(self.y-camy+15)), 4)
        if self.time == 'palmeiras':
            pygame.draw.circle(TELA, VP, (int(self.x-camx-30), int(self.y-camy)), 18)
            pygame.draw.circle(TELA, BR, (int(self.x-camx-30), int(self.y-camy)), 18, 2)
            pygame.draw.circle(TELA, AB, (int(self.x-camx-30), int(self.y-camy)), 8)
        else:
            pygame.draw.circle(TELA, AG, (int(self.x-camx-30), int(self.y-camy)), 18)
            pygame.draw.circle(TELA, BR, (int(self.x-camx-30), int(self.y-camy)), 18, 2)
            pygame.draw.circle(TELA, (100,180,255), (int(self.x-camx-30), int(self.y-camy)), 8)
        nome = "PALMEIRAS" if self.time == 'palmeiras' else "GREMIO"
        txt = FApp.render(nome, True, BR if self.time=='palmeiras' else (100,180,255))
        TELA.blit(txt, (self.x-camx - txt.get_width()//2 - 30, self.y-camy + 18))
        for i in range(6):
            fx = self.x-camx - 80 + i*32
            fy = self.y-camy - 38 + math.sin(pygame.time.get_ticks()/200 + i) * 3
            cor_band = random.choice([self.cor_principal, self.cor_secundaria, AB])
            pygame.draw.polygon(TELA, cor_band, [(fx, fy), (fx+12, fy), (fx+6, fy+10)])
        if self.chegou and self.fans_soltos < self.total_fans:
            info = FAM.render(f"TORCIDA {nome}: {self.fans_soltos}/{self.total_fans}", True, self.cor_principal)
            bg = pygame.Surface((info.get_width()+10, info.get_height()+6), pygame.SRCALPHA)
            bg.fill((0,0,0,180))
            TELA.blit(bg, (self.x-camx - info.get_width()//2 - 5, self.y-camy - 70))
            TELA.blit(info, (self.x-camx - info.get_width()//2, self.y-camy - 67))

def draw_delegacia(camx,camy):
    pygame.draw.rect(TELA,(150,150,160),(DEL_X-camx-20,DEL_Y-camy-20,DEL_L+40,DEL_A+40))
    pygame.draw.rect(TELA,(0,0,0,100),(DEL_X-camx+10,DEL_Y-camy+10,DEL_L,DEL_A))
    pygame.draw.rect(TELA,COR_DELEGACIA,(DEL_X-camx,DEL_Y-camy,DEL_L,DEL_A))
    pygame.draw.rect(TELA,(140,140,160),(DEL_X-camx-5,DEL_Y-camy-5,DEL_L+10,DEL_A+10))
    pygame.draw.rect(TELA,COR_DELEGACIA,(DEL_X-camx,DEL_Y-camy,DEL_L,DEL_A))
    pygame.draw.rect(TELA,PT,(DEL_X-camx,DEL_Y-camy,DEL_L,DEL_A),5)
    pygame.draw.rect(TELA,(40,40,60),(DEL_X+DEL_L//2-30-camx,DEL_Y+DEL_A-15-camy,60,30))
    for i in range(3):
        for j in range(2):
            jx=DEL_X+30+i*80; jy=DEL_Y+30+j*60
            cor_jan = (200,220,255) if (i+j)%2==0 else (100,120,150)
            pygame.draw.rect(TELA,cor_jan,(jx-camx,jy-camy,50,40))
            pygame.draw.rect(TELA,PT,(jx-camx,jy-camy,50,40),2)
            for k in range(5):
                pygame.draw.line(TELA,PT,(jx+k*10-camx,jy-camy),(jx+k*10-camx,jy+40-camy),1)
    placa=pygame.Rect(DEL_X+DEL_L//2-80-camx,DEL_Y+DEL_A-60-camy,160,25)
    pygame.draw.rect(TELA,AZUL_POLICIA,placa); pygame.draw.rect(TELA,BR,placa,2)
    txt=FAM.render("DELEGACIA - 12 DP RJ",True,BR)
    TELA.blit(txt,(placa.x+placa.w//2-txt.get_width()//2,placa.y+3))
    pulse = int(abs(math.sin(pygame.time.get_ticks()/200))*100)+155
    pygame.draw.circle(TELA,(pulse,30,30),(DEL_X+DEL_L//2-camx,DEL_Y-10-camy),10)
    pygame.draw.circle(TELA,BR,(DEL_X+DEL_L//2-camx,DEL_Y-10-camy),8,2)

def draw_cela(camx,camy,tempo_restante):
    ov=pygame.Surface((LARGURA_TELA,ALTURA_TELA)); ov.set_alpha(200); ov.fill((0,0,0)); TELA.blit(ov,(0,0))
    bx=LARGURA_TELA//2-200; by=ALTURA_TELA//2-100; bw=400; bh=200
    pygame.draw.rect(TELA,(60,60,70),(bx-10,by-10,bw+20,bh+20))
    pygame.draw.rect(TELA,(30,30,40),(bx,by,bw,bh))
    for i in range(11):
        gx=bx+i*(bw//10); pygame.draw.line(TELA,(80,80,90),(gx,by),(gx,by+bh),8)
        pygame.draw.line(TELA,(120,120,140),(gx,by),(gx,by+bh),1)
    pygame.draw.line(TELA,(80,80,90),(bx,by),(bx+bw,by),10)
    pygame.draw.line(TELA,(80,80,90),(bx,by+bh),(bx+bw,by+bh),10)
    m1=FG.render("VOCE FOI PRESO!",True,(255,80,80))
    TELA.blit(m1,(LARGURA_TELA//2-m1.get_width()//2,by-120))
    m2=FT.render("Delegacia de Policia do Rio de Janeiro",True,BR)
    TELA.blit(m2,(LARGURA_TELA//2-m2.get_width()//2,by-60))
    m3=FA.render(f"Libertacao em: {int(tempo_restante)}s",True,AMARELO_POLICIA)
    TELA.blit(m3,(LARGURA_TELA//2-m3.get_width()//2,by+bh+30))
    total=30.0; prog=1.0 - (tempo_restante/total)
    pbar=pygame.Rect(LARGURA_TELA//2-250,by+bh+120,500,20)
    pygame.draw.rect(TELA,(60,60,60),pbar,border_radius=10)
    pygame.draw.rect(TELA,VDV,(pbar.x,pbar.y,int(pbar.w*prog),pbar.h),border_radius=10)
    pygame.draw.rect(TELA,BR,pbar,2,border_radius=10)

def draw_chao(camx,camy):
    TELA.fill((245,245,240)); TELA.blit(TEX_GRAMA,(0,0))
    lr=120
    for y in RH:
        if abs(y-CY)<500: continue
        pygame.draw.rect(TELA,AS,(0-camx,y-camy,TM,lr))
        pygame.draw.rect(TELA,(100,100,100),(0-camx,y-camy,TM,lr//3))
        for x in range(0,TM,100):
            pygame.draw.rect(TELA,FAMC,(x-camx,y+lr//2-2-camy,50,4))
    for x in RV:
        if abs(x-CX)<500: continue
        pygame.draw.rect(TELA,AS,(x-camx,0-camy,lr,TM))
        pygame.draw.rect(TELA,(100,100,100),(x-camx,0-camy,lr//3,TM))
        for y in range(0,TM,100):
            pygame.draw.rect(TELA,FAMC,(x+lr//2-2-camx,y-camy,4,50))
    pygame.draw.rect(TELA,AS,(CX-1000-camx,REY-camy,2000,120))
    for x in range(CX-1000,CX+1000,100):
        pygame.draw.rect(TELA,FAMC,(x-camx,REY+58-camy,50,4))
    pygame.draw.rect(TELA,CE,(CX-1200-camx,TY-camy,2400,50))
    pygame.draw.line(TELA,CTR,(CX-1200-camx,TY-camy),(CX+1200-camx,TY-camy),4)
    pygame.draw.line(TELA,(150,150,150),(CX-1200-camx,TY-camy-2),(CX+1200-camx,TY-camy-2),2)
    pygame.draw.line(TELA,CTR,(CX-1200-camx,TY+46-camy),(CX+1200-camx,TY+46-camy),4)

def draw_mansao(camx,camy):
    pygame.draw.rect(TELA,(100,150,100),(MX-50-camx,MY-50-camy,ML+500,MA+200))
    pygame.draw.rect(TELA,CPI,(PX-camx,PY-camy,PL,PA))
    for i in range(6):
        onda_y = PY + i * (PA//6) + math.sin(pygame.time.get_ticks()/300 + i) * 3
        pygame.draw.line(TELA,(150,220,255),(PX+5-camx,onda_y-camy),(PX+PL-5-camx,onda_y-camy),2)
    pygame.draw.rect(TELA,BR,(PX-camx,PY-camy,PL,PA),5)
    pygame.draw.rect(TELA,(0,0,0,80),(MX-camx+10,MY-camy+10,ML,MA))
    pygame.draw.rect(TELA,CPM,(MX-camx,MY-camy,ML,MA))
    pygame.draw.rect(TELA,PT,(MX-camx,MY-camy,ML,MA),10)
    pygame.draw.rect(TELA,(230,200,160),(MX-camx,MY-camy,ML,10))

def draw_estadio(camx,camy,fim=False,luzes_apagadas=False):
    if luzes_apagadas:
        cor_telhado=(140,140,150); cor_arq_amar=(100,90,20)
        cor_arq_clara=(100,100,110); cor_arq_azul=(10,20,60)
        cor_pista=(50,50,55); cor_grama1=(15,60,15); cor_grama2=(25,80,25); cor_linha=(120,120,120)
    else:
        cor_telhado=BR; cor_arq_amar=AB; cor_arq_clara=CL
        cor_arq_azul=AZB; cor_pista=CZ; cor_grama1=VC; cor_grama2=VCC; cor_linha=BR
    pygame.draw.ellipse(TELA,(0,0,0,90),(CX-RE-camx+15,CY-RE-camy+15,RE*2,RE*2))
    pygame.draw.ellipse(TELA,cor_telhado,(CX-RE-camx,CY-RE-camy,RE*2,RE*2))
    pygame.draw.ellipse(TELA,CE,(CX-(RE-30)-camx,CY-(RE-30)-camy,(RE-30)*2,(RE-30)*2))
    pygame.draw.ellipse(TELA,cor_arq_amar,(CX-(RE-70)-camx,CY-(RE-70)-camy,(RE-70)*2,(RE-70)*2))
    if not fim and not luzes_apagadas:
        for i in range(20):
            a=math.radians(i*18)
            tx=CX+math.cos(a)*(RE-90); ty=CY+math.sin(a)*(RE-90)
            bob = math.sin(pygame.time.get_ticks()/200 + i) * 2
            pygame.draw.circle(TELA,VP,(int(tx-camx),int(ty-camy+bob)),12)
            pygame.draw.circle(TELA,(50,200,50),(int(tx-camx-3),int(ty-camy-3+bob)),3)
    pygame.draw.ellipse(TELA,cor_arq_clara,(CX-(RE-110)-camx,CY-(RE-110)-camy,(RE-110)*2,(RE-110)*2))
    pygame.draw.ellipse(TELA,cor_arq_azul,(CX-(RE-110)-camx,CY-(RE-110)-camy,(RE-110)*2,(RE-110)*2),3)
    pygame.draw.ellipse(TELA,cor_pista,(CX-RI-camx,CY-RI-camy,RI*2,RI*2))
    cpx,cpy=CX-150,CY-100
    for i in range(6):
        cor=cor_grama1 if i%2==0 else cor_grama2
        pygame.draw.rect(TELA,cor,(cpx+i*50-camx,cpy-camy,50,200))
        if not luzes_apagadas:
            pygame.draw.rect(TELA,tuple(min(255,c+20) for c in cor),(cpx+i*50-camx,cpy-camy,50,20))
    pygame.draw.rect(TELA,cor_linha,(cpx-camx,cpy-camy,300,200),2)
    pygame.draw.line(TELA,cor_linha,(CX-camx,cpy-camy),(CX-camx,cpy+200-camy),2)
    pygame.draw.circle(TELA,cor_linha,(CX-camx,CY-camy),30,2)
    if not fim:
        for i in range(5):
            jx=CX-100+i*40; jy=CY-60+(i%2)*120
            pygame.draw.ellipse(TELA,(0,0,0,80),(jx-camx-10,jy-camy+5,20,6))
            pygame.draw.circle(TELA,VP,(int(jx-camx),int(jy-camy)),8)
        for i in range(5):
            jx=CX+100-i*40; jy=CY-60+(i%2)*120
            pygame.draw.ellipse(TELA,(0,0,0,80),(jx-camx-10,jy-camy+5,20,6))
            pygame.draw.circle(TELA,AG,(int(jx-camx),int(jy-camy)),8)
        pygame.draw.circle(TELA,BR,(int(CX-camx),int(CY-camy)),4)
    tw,th=140,90; xt=CX+RE-180; yt=CY-th//2
    cor_telao=PT if not luzes_apagadas else (20,20,20)
    cor_tela=(0,30,0) if not luzes_apagadas else (5,10,5)
    pygame.draw.rect(TELA,cor_telao,(xt-camx,yt-camy,tw,th))
    pygame.draw.rect(TELA,cor_tela,(xt+5-camx,yt+5-camy,tw-10,th-10))
    for i in range(0, th-10, 3):
        pygame.draw.line(TELA,(0,60,0,80),(xt+5-camx,yt+5+i-camy),(xt+tw-5-camx,yt+5+i-camy),1)
    tp=FTX.render("PAL",True,VP); tg=FTX.render("GRE",True,(150,200,255))
    tpl=FP.render(f"{PP} x {PG}",True,BR)
    TELA.blit(tp,(xt+10-camx,yt+10-camy)); TELA.blit(tg,(xt+tw-50-camx,yt+10-camy))
    TELA.blit(tpl,(xt+tw//2-tpl.get_width()//2-camx,yt+th//2-10-camy))
    if luzes_apagadas: tt=FTX.render("LUZES APAGADAS",True,(255,100,100))
    elif fim: tt=FTX.render("FIM",True,AB)
    else: tt=FTX.render(f"{TJ}'",True,AB)
    TELA.blit(tt,(xt+tw//2-tt.get_width()//2-camx,yt+th-25-camy))
    ex,ey=CX,CY+RE+60
    pygame.draw.ellipse(TELA,(0,0,0,100),(ex-camx-30,ey-camy+40,60,15))
    pygame.draw.rect(TELA,CE,(ex-30-camx,ey-camy,60,40))
    pygame.draw.rect(TELA,CZ,(ex-20-camx,ey-10-camy,40,50))
    pygame.draw.rect(TELA,CES,(ex-10-camx,ey-40-camy,20,30))
    pygame.draw.circle(TELA,CES,(int(ex-camx),int(ey-50-camy)),8)

def draw_noite(camx,camy,h,cl,luzes_apagadas=False):
    SE.fill((0,0,40))
    if 6<=h<18: a=0
    elif 18<=h<20: a=(h-18)*60
    elif 20<=h or h<5: a=180
    elif 5<=h<6: a=180-(h-5)*180
    else: a=0
    if cl and cl.atual=='chuva': a=max(a,100)
    if cl and cl.atual=='frio': a=max(a,80)
    if luzes_apagadas: a=max(a,210)
    SE.set_alpha(int(min(255,a))); TELA.blit(SE,(0,0))
    if not luzes_apagadas:
        SL.fill((0,0,0,0))
        for ang in range(0,360,15):
            ra=math.radians(ang)
            lx=CX+math.cos(ra)*(RE-15); ly=CY+math.sin(ra)*(RE-15)
            it=180 if a>100 else 60
            for r in range(60, 20, -10):
                alpha_r = int(it * (r/60) * 0.3)
                pygame.draw.circle(SL,(255,255,200,alpha_r),(int(lx-camx),int(ly-camy)),r)
        TELA.blit(SL,(0,0))

class Humano:
    def __init__(self,x,y,cc,cc2,cp,tipo='civil'):
        self.x,self.y=x,y; self.cor_camisa=cc; self.cor_calca=cc2; self.cor_pele=cp
        self.tipo=tipo; self.vel=5
        self.dir=random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.tem_ing=random.choice([True,False]); self.ent_est=False; self.fala=None
        self.est_pol='patrulha'; self.t_at=0; self.vida=100.0; self.th=0
        self.cel=False; self.tp=0; self.fase=0
        self.atirando_no_jogador=False; self.tempo_ultimo_tiro=0
        self.intervalo_tiro=0.8; self.distancia_max_ataque=600
        self.respirando = random.uniform(0, 6.28)
    def desenhar(self,camx,camy):
        pygame.draw.ellipse(TELA,(0,0,0,90),(self.x-camx-9,self.y-camy+14,18,7))
        self.respirando += 0.05
        bob = math.sin(self.respirando) * 0.5
        off=math.sin(self.fase)*3 if self.tp>0 else 0
        pygame.draw.rect(TELA,self.cor_calca,(self.x-camx-6+off,self.y-camy+5+bob,5,11))
        pygame.draw.rect(TELA,self.cor_calca,(self.x-camx+1-off,self.y-camy+5+bob,5,11))
        pygame.draw.rect(TELA,self.cor_camisa,(self.x-camx-10,self.y-camy-8+bob,20,18))
        pygame.draw.rect(TELA,tuple(min(255,c+40) for c in self.cor_camisa),(self.x-camx-10,self.y-camy-8+bob,20,4))
        pygame.draw.rect(TELA,self.cor_pele,(self.x-camx-15,self.y-camy-6+bob,5,12))
        if self.tipo=='jogador' and hasattr(self,'soc') and self.soc:
            pygame.draw.circle(TELA,self.cor_pele,(int(self.x-camx+22),int(self.y-camy-5+bob)),7)
        else:
            pygame.draw.rect(TELA,self.cor_pele,(self.x-camx+10,self.y-camy-6+bob,5,12))
        cc=self.cor_pele if self.th<=0 else (255,100,100)
        pygame.draw.circle(TELA,cc,(int(self.x-camx),int(self.y-camy-14+bob)),8)
        pygame.draw.circle(TELA,tuple(min(255,c+40) for c in cc),(int(self.x-camx-2),int(self.y-camy-16+bob)),3)
        if self.tipo in ('police','seguranca'):
            pygame.draw.rect(TELA,PT,(self.x-camx-8,self.y-camy-20+bob,16,4))
        if self.tem_ing and self.tipo=='civil':
            pygame.draw.circle(TELA,AB,(int(self.x-camx),int(self.y-camy-25+bob)),3)
        if self.tipo in ('police','seguranca') and (self.est_pol=='atirando' or self.atirando_no_jogador):
            pygame.draw.rect(TELA,(30,30,30),(self.x-camx+10,self.y-camy-8+bob,12,4))
            if random.random()<0.5:
                pygame.draw.circle(TELA,(255,200,50),(int(self.x-camx+22),int(self.y-camy-6+bob)),5)
        if self.vida<100:
            bx=self.x-camx-15; by=self.y-camy-30
            pygame.draw.rect(TELA,(100,0,0),(bx,by,30,5))
            pygame.draw.rect(TELA,(0,255,0),(bx,by,int(30*(self.vida/100)),5))
        if self.fala: self.fala.desenhar(camx,camy)

class Jogador(Humano):
    def __init__(self,x,y):
        super().__init__(x,y,AB,AZB,PEB,'jogador')
        self.tem_ing=True; self.fala=None; self.soc=False; self.ts=0; self.vida=100.0
        self.no_carro=False; self.carro_atual=None; self.estacao_atual=0; self.tempo_apanhar=0
        self.preso=False
        self.primeira_pessoa=False
    def mover(self,tk,dt):
        if self.no_carro or self.preso: return
        mov=False
        if tk[pygame.K_a] or tk[pygame.K_LEFT]: self.x-=self.vel; mov=True
        if tk[pygame.K_d] or tk[pygame.K_RIGHT]: self.x+=self.vel; mov=True
        if tk[pygame.K_w] or tk[pygame.K_UP]: self.y-=self.vel; mov=True
        if tk[pygame.K_s] or tk[pygame.K_DOWN]: self.y+=self.vel; mov=True
        self.x=max(0,min(TM,self.x)); self.y=max(0,min(TM,self.y))
        if mov:
            self.tp+=dt; self.fase+=dt*10
            if self.tp>0.35:
                self.tp=0
                if pode_tocar('passo',0.25): tocar('passo','passos',0.2)
        else: self.fase=0
    def falar(self,txt): self.fala=Fala(self.x,self.y,txt,cor=(255,220,100),dur=3.5,som=True)
    def socar(self,hs,particulas=None,callback_policia=None):
        if self.preso: return
        self.soc=True; self.ts=0.2
        tocar('tiro','efeitos',0.3)
        CAM_SHAKE.ativar(6, 0.3)
        for h in hs:
            if h is self: continue
            if math.hypot(h.x-self.x,h.y-self.y)<60:
                h.vida-=random.uniform(10,25); h.th=0.3
                if h.tipo in ('police','seguranca'):
                    h.atirando_no_jogador=True; h.tempo_ultimo_tiro=0
                    h.fala=Fala(h.x,h.y,random.choice(FALAS_POL),cor=(255,100,100),dur=1.8)
                    if callback_policia is not None: callback_policia(h.x,h.y)
                else:
                    h.fala=Fala(h.x,h.y,"Ai! Voce me bateu!",cor=(255,100,100),dur=1.5)
                if particulas is not None:
                    for _ in range(6): particulas.append(Particula(h.x,h.y,'sangue'))

class Pedestre(Humano):
    def __init__(self):
        a=random.uniform(0,2*math.pi); d=random.randint(500,1500)
        x=CX+math.cos(a)*d; y=CY+math.sin(a)*d
        c=VP if random.random()<0.5 else AG
        super().__init__(x,y,c,(30,30,30),PE,'civil')
        self.vel=random.uniform(1.5,3.0); self.tc=0
    def atualizar(self,segs,dt,j):
        if self.th>0: self.th-=dt
        self.tc+=dt
        if self.tc>random.uniform(5,15): self.tc=0; self.cel=not self.cel
        if random.random()<0.02: self.dir=random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        if self.vida<30:
            dx=self.x-j.x; dy=self.y-j.y; d=math.hypot(dx,dy)
            if d>0: self.x+=(dx/d)*3; self.y+=(dy/d)*3
        else:
            dc=math.hypot(self.x-CX,self.y-CY)
            if dc<500 and not self.ent_est:
                if random.random()<0.03: self.ent_est=True
            if self.ent_est:
                dx,dy=CX-self.x,CY-self.y; d=math.hypot(dx,dy)
                if d>0: self.dir=(dx/d,dy/d)
                for s in segs:
                    if math.hypot(self.x-s.x,self.y-s.y)<70 and not self.tem_ing:
                        self.dir=(-self.dir[0],-self.dir[1]); self.ent_est=False
                        self.fala=Fala(self.x,self.y,"Nao tenho ingresso!",cor=(255,150,150),dur=2.0); break
                if d<RI and self.tem_ing:
                    self.x=CX+random.choice([-1,1])*random.randint(1000,2000)
                    self.y=CY+random.choice([-1,1])*random.randint(1000,2000)
                    self.ent_est=False; self.tem_ing=random.choice([True,False])
            else:
                self.x+=self.dir[0]*self.vel; self.y+=self.dir[1]*self.vel
                self.x=max(0,min(TM,self.x)); self.y=max(0,min(TM,self.y))
                self.tp+=dt; self.fase+=dt*8
                if self.tp>0.4:
                    self.tp=0
                    if pode_tocar('passo',0.1): tocar('passo','passos',0.12)
        if self.fala:
            self.fala.x=self.x; self.fala.y=self.y
            if not self.fala.atualizar(dt): self.fala=None

class Carro:
    def __init__(self):
        self.cor=random.choice([(255,0,0),(0,0,255),(0,255,0),(255,255,0),(255,255,255),(0,0,0),(200,100,200),(100,200,255)])
        self.vel=random.uniform(3,6); self.dh=random.choice([True,False])
        if self.dh:
            self.x=random.randint(0,TM); self.y=random.choice(RH)+40
            self.vx=random.choice([-1,1])*self.vel; self.vy=0
        else:
            self.x=random.choice(RV)+40; self.y=random.randint(0,TM)
            self.vx=0; self.vy=random.choice([-1,1])*self.vel
        self.ts=0; self.ocupado=False
        self.estacao=random.randint(0,len(RADIOS)-1); self.radio_ligada=False
    def atualizar(self,sems,sm2,dt):
        if self.ocupado: return
        self.ts+=dt
        if self.ts>random.uniform(4,10):
            self.ts=0
            if pode_tocar('carro',0.8): tocar('carro','efeitos',0.15)
        for s in sems:
            if s.e!=0:
                if self.dh and s.h and abs(self.y-s.y)<60:
                    if (self.vx>0 and 0<s.x-self.x<180) or (self.vx<0 and 0<self.x-s.x<180): return
                if not self.dh and not s.h and abs(self.x-s.x)<60:
                    if (self.vy>0 and 0<s.y-self.y<180) or (self.vy<0 and 0<self.y-s.y<180): return
        for sm in sm2:
            if sm.e!=0 and math.hypot(self.x-sm.x,self.y-sm.y)<200: return
        self.x+=self.vx; self.y+=self.vy
        if self.dh:
            if self.x>TM: self.x=0
            elif self.x<0: self.x=TM
        else:
            if self.y>TM: self.y=0
            elif self.y<0: self.y=TM
    def desenhar(self,camx,camy):
        if self.dh:
            pygame.draw.rect(TELA,(0,0,0,100),(self.x-camx+6,self.y-camy+6,60,40),border_radius=5)
            pygame.draw.rect(TELA,self.cor,(self.x-camx,self.y-camy,60,40),border_radius=5)
            pygame.draw.rect(TELA,tuple(min(255,c+50) for c in self.cor),(self.x-camx,self.y-camy,60,10),border_radius=5)
            pygame.draw.rect(TELA,PT,(self.x+10-camx,self.y+5-camy,40,30),border_radius=3)
            pygame.draw.rect(TELA,(150,200,255),(self.x+12-camx,self.y+8-camy,20,8),border_radius=2)
            pygame.draw.circle(TELA,(255,255,200),(self.x+58-camx,self.y+8-camy),3)
            pygame.draw.circle(TELA,(255,255,200),(self.x+58-camx,self.y+32-camy),3)
            pygame.draw.circle(TELA,PT,(int(self.x+10-camx),int(self.y+42-camy)),5)
            pygame.draw.circle(TELA,PT,(int(self.x+50-camx),int(self.y+42-camy)),5)
        else:
            pygame.draw.rect(TELA,(0,0,0,100),(self.x-camx+6,self.y-camy+6,40,60),border_radius=5)
            pygame.draw.rect(TELA,self.cor,(self.x-camx,self.y-camy,40,60),border_radius=5)
            pygame.draw.rect(TELA,tuple(min(255,c+50) for c in self.cor),(self.x-camx,self.y-camy,10,60),border_radius=5)
            pygame.draw.rect(TELA,PT,(self.x+5-camx,self.y+10-camy,30,40),border_radius=3)
            pygame.draw.rect(TELA,(150,200,255),(self.x+8-camx,self.y+12-camy,8,20),border_radius=2)
            pygame.draw.circle(TELA,(255,255,200),(self.x+8-camx,self.y+58-camy),3)
            pygame.draw.circle(TELA,(255,255,200),(self.x+32-camx,self.y+58-camy),3)
            pygame.draw.circle(TELA,PT,(int(self.x-2-camx),int(self.y+10-camy)),5)
            pygame.draw.circle(TELA,PT,(int(self.x-2-camx),int(self.y+50-camy)),5)

class Cachorro:
    def __init__(self):
        d=random.randint(300,1500); a=random.uniform(0,2*math.pi)
        self.x,self.y=CX+math.cos(a)*d,CY+math.sin(a)*d
        self.vel=random.uniform(2,4); self.dir=random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.cor=random.choice([MC,PC,BR]); self.tl=0; self.fase=0
    def atualizar(self,dt):
        if random.random()<0.03: self.dir=random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.x+=self.dir[0]*self.vel; self.y+=self.dir[1]*self.vel
        self.x=max(0,min(TM,self.x)); self.y=max(0,min(TM,self.y))
        self.fase+=dt*12; self.tl+=dt
        if self.tl>random.uniform(3,8):
            self.tl=0
            if pode_tocar('latido',1): tocar('latido','efeitos',0.3)
    def desenhar(self,camx,camy):
        pygame.draw.ellipse(TELA,(0,0,0,90),(self.x-camx-9,self.y-camy+5,18,5))
        pygame.draw.ellipse(TELA,self.cor,(self.x-camx-10,self.y-camy,20,10))
        pygame.draw.ellipse(TELA,tuple(min(255,c+40) for c in self.cor),(self.x-camx-10,self.y-camy,20,4))
        pygame.draw.circle(TELA,self.cor,(int(self.x-camx+10),int(self.y-camy+5)),6)
        pygame.draw.circle(TELA,self.cor,(int(self.x-camx+8),int(self.y-camy+1)),3)
        pygame.draw.circle(TELA,self.cor,(int(self.x-camx+12),int(self.y-camy+1)),3)
        off=math.sin(self.fase)*2
        pygame.draw.rect(TELA,self.cor,(self.x-camx-8+off,self.y-camy+8,3,6))
        pygame.draw.rect(TELA,self.cor,(self.x-camx+5-off,self.y-camy+8,3,6))
        rabo_off = math.sin(self.fase*2)*4
        pygame.draw.line(TELA,self.cor,(self.x-camx-10,self.y-camy+2),(self.x-camx-18,self.y-camy-5+rabo_off),3)

class Trem:
    def __init__(self):
        self.x=CX-1000; self.y=TY+25; self.vel=12; self.dir=1
    def atualizar(self):
        self.x+=self.vel*self.dir
        if self.x>CX+1200: self.dir=-1
        if self.x<CX-1200: self.dir=1
    def desenhar(self,camx,camy):
        for i in range(4):
            vx=self.x-camx-(i*130) if self.dir==1 else self.x-camx+(i*130)
            pygame.draw.rect(TELA,(0,0,0,80),(vx+4,self.y-camy-16,120,40),border_radius=5)
            pygame.draw.rect(TELA,CM,(vx,self.y-camy-20,120,40),border_radius=5)
            pygame.draw.rect(TELA,(240,240,240),(vx,self.y-camy-20,120,8),border_radius=5)
            pygame.draw.rect(TELA,CMJ,(vx+10,self.y-camy-15,100,15))

class Heli:
    def __init__(self):
        self.a=random.uniform(0,2*math.pi); self.r=random.randint(RE+100,RE+600)
        self.va=random.uniform(0.005,0.02)*random.choice([-1,1])
        self.x=CX+math.cos(self.a)*self.r; self.y=CY+math.sin(self.a)*self.r
        self.alt=random.randint(100,250); self.fase=0
    def atualizar(self,dt):
        self.a+=self.va
        self.x=CX+math.cos(self.a)*self.r; self.y=CY+math.sin(self.a)*self.r
        self.fase+=dt*15
    def desenhar(self,camx,camy):
        hx,hy=self.x-camx,self.y-camy-self.alt
        pygame.draw.ellipse(TELA,(0,0,0,80),(hx-25,self.y-camy-12,50,20))
        pygame.draw.ellipse(TELA,CH,(hx-20,hy-12,40,24))
        pygame.draw.ellipse(TELA,(80,80,80),(hx-20,hy-12,40,10))
        pygame.draw.circle(TELA,(0,200,255),(int(hx-5),int(hy)),8)
        for j in range(4):
            ang = self.fase*8 + j * math.pi/2
            rot_x = math.cos(ang)*35; rot_y = math.sin(ang)*35
            pygame.draw.line(TELA,(220,220,220),(hx-35,hy-15),(hx+35,hy-15),3)
            pygame.draw.line(TELA,(180,180,180),(hx+rot_x,hy-20),(hx-rot_x,hy-10),2)
        pygame.draw.line(TELA,CH,(hx+15,hy),(hx+55,hy),4)

class Seguranca(Humano):
    def __init__(self,ai,tipo):
        self.a=ai; self.rp=RE+30; self.va=0.005*random.choice([-1,1])
        x=CX+math.cos(self.a)*self.rp; y=CY+math.sin(self.a)*self.rp
        cc=(0,0,255) if tipo=='police' else (30,30,30)
        cl=(0,0,100) if tipo=='police' else (30,30,30)
        super().__init__(x,y,cc,cl,PE,tipo)
    def atualizar(self,dt,brigas,jogador=None,particulas=None):
        if self.th>0: self.th-=dt
        if self.atirando_no_jogador and jogador:
            dx=jogador.x-self.x; dy=jogador.y-self.y; dist=math.hypot(dx,dy)
            if dist>self.distancia_max_ataque: self.atirando_no_jogador=False
            else:
                self.tempo_ultimo_tiro+=dt
                if self.tempo_ultimo_tiro>self.intervalo_tiro:
                    self.tempo_ultimo_tiro=0
                    tocar('tiro','efeitos',0.5)
                    if pode_tocar('bala',0.3): tocar('bala','efeitos',0.3)
                    dano=random.uniform(5,15)*(1-dist/self.distancia_max_ataque*0.5)
                    jogador.vida-=dano; jogador.tempo_apanhar=0.3
                    CAM_SHAKE.ativar(8, 0.4)
                    if particulas is not None:
                        for _ in range(5): particulas.append(Particula(jogador.x,jogador.y,'sangue'))
                        for _ in range(3): particulas.append(Particula(self.x+15,self.y-3,'faisca'))
                return
        if self.tipo=='police' and brigas:
            bmp=None; dm=99999
            for b in brigas:
                d=math.hypot(b.x-self.x,b.y-self.y)
                if d<dm: dm=d; bmp=b
            if bmp and dm<800:
                self.est_pol='indo_briga'
                if pode_tocar('sirene',1.5): tocar('sirene','sirene',0.4)
                dx=bmp.x-self.x; dy=bmp.y-self.y; d=math.hypot(dx,dy)
                if d>60: self.x+=(dx/d)*4; self.y+=(dy/d)*4
                else:
                    self.est_pol='atirando'; self.t_at+=dt
                    if random.random()<0.15: tocar('tiro','efeitos',0.4)
                    if self.t_at>1: bmp.sep=True; self.est_pol='patrulha'; self.t_at=0
                return
        self.est_pol='patrulha'
        self.a+=self.va
        self.x=CX+math.cos(self.a)*self.rp; self.y=CY+math.sin(self.a)*self.rp

def draw_hands_fps(jogador, celular):
    mx_l = LARGURA_TELA//2 - 220; my_l = ALTURA_TELA - 100
    mx_r = LARGURA_TELA//2 + 220; my_r = ALTURA_TELA - 100
    if jogador.soc: mx_r -= 60
    pygame.draw.circle(TELA, (0,0,0), (mx_l+5, my_l+5), 55)
    pygame.draw.circle(TELA, (0,0,0), (mx_r+5, my_r+5), 55)
    pygame.draw.circle(TELA, PE, (mx_l, my_l), 55)
    pygame.draw.circle(TELA, (150,100,60), (mx_l, my_l), 55, 4)
    for i in range(4):
        pygame.draw.rect(TELA, PE, (mx_l-40+i*20, my_l-75, 18, 40), border_radius=8)
        pygame.draw.rect(TELA, (150,100,60), (mx_l-40+i*20, my_l-75, 18, 40), 2, border_radius=8)
    pygame.draw.circle(TELA, PE, (mx_r, my_r), 55)
    pygame.draw.circle(TELA, (150,100,60), (mx_r, my_r), 55, 4)
    for i in range(4):
        pygame.draw.rect(TELA, PE, (mx_r-40+i*20, my_r-75, 18, 40), border_radius=8)
        pygame.draw.rect(TELA, (150,100,60), (mx_r-40+i*20, my_r-75, 18, 40), 2, border_radius=8)
    if jogador.soc:
        pygame.draw.circle(TELA, (255,255,200), (mx_r-40, my_r-20), 15, 3)
        pygame.draw.circle(TELA, (255,200,100), (mx_r-40, my_r-20), 8)

def draw_crosshair():
    cx, cy = LARGURA_TELA//2, ALTURA_TELA//2
    pygame.draw.circle(TELA, (0,0,0), (cx,cy), 21, 3)
    pygame.draw.circle(TELA, (255,255,255), (cx,cy), 20, 2)
    pygame.draw.line(TELA, (255,255,255), (cx-30, cy), (cx-10, cy), 3)
    pygame.draw.line(TELA, (255,255,255), (cx+10, cy), (cx+30, cy), 3)
    pygame.draw.line(TELA, (255,255,255), (cx, cy-30), (cx, cy-10), 3)
    pygame.draw.line(TELA, (255,255,255), (cx, cy+10), (cx, cy+30), 3)
    pygame.draw.circle(TELA, (255,50,50), (cx,cy), 3)

def draw_zoom_frame():
    borda = 60
    pygame.draw.rect(TELA, (0,0,0), (0,0,LARGURA_TELA,borda))
    pygame.draw.rect(TELA, (0,0,0), (0,ALTURA_TELA-borda,LARGURA_TELA,borda))
    pygame.draw.rect(TELA, (0,0,0), (0,0,borda,ALTURA_TELA))
    pygame.draw.rect(TELA, (0,0,0), (LARGURA_TELA-borda,0,borda,ALTURA_TELA))

def salvar(j,r):
    try:
        with open("savegame.txt","w") as f: f.write(f"{j.x},{j.y},{r.min},{r.dia}")
        return True
    except: return False

def criar_predios():
    """Cria MUITOS prédios pelo mapa - expandido"""
    pred=[]
    pos=[]
    # Grade de prédios ao redor do mapa (espaço de 250 em 250)
    for x in range(300, TM - 300, 260):
        for y in range(300, TM - 300, 260):
            # Pula a área do estádio
            dx = abs(x + 90 - CX); dy = abs(y + 90 - CY)
            if math.hypot(dx, dy) < RE + 100: continue
            # Pula a área da mansão
            if x < MX + ML + 200 and y < MY + MA + 200: continue
            # Pula a área da delegacia
            if abs(x - DEL_X) < 300 and abs(y - DEL_Y) < 250: continue
            # Pula as ruas
            na_rua = False
            for ry in RH:
                if abs(y - ry) < 200: na_rua = True; break
            for rx in RV:
                if abs(x - rx) < 200: na_rua = True; break
            if na_rua: continue
            pos.append((x, y))
    # Adiciona alguns prédios extras em posições aleatórias
    for _ in range(30):
        x = random.randint(300, TM - 300)
        y = random.randint(300, TM - 300)
        dx = abs(x + 90 - CX); dy = abs(y + 90 - CY)
        if math.hypot(dx, dy) < RE + 150: continue
        if x < MX + ML + 200 and y < MY + MA + 200: continue
        if abs(x - DEL_X) < 300 and abs(y - DEL_Y) < 250: continue
        na_rua = False
        for ry in RH:
            if abs(y - ry) < 200: na_rua = True; break
        for rx in RV:
            if abs(x - rx) < 200: na_rua = True; break
        if na_rua: continue
        pos.append((x, y))
    
    print(f"Criando {len(pos)} predios...")
    for p in pos:
        pr=Predio(p[0],p[1])
        for _ in range(random.randint(2,4)): pr.moradores.append(Morador(pr))
        pred.append(pr)
    print(f"{len(pred)} predios criados!")
    return pred

def draw_radio_hud(j):
    if not j.no_carro or not j.carro_atual: return
    rp=pygame.Rect(LARGURA_TELA-350,ALTURA_TELA-140,330,110)
    pygame.draw.rect(TELA,(0,0,0,100),(rp.x+4,rp.y+4,rp.w,rp.h),border_radius=15)
    pygame.draw.rect(TELA,RADIO_COR,rp,border_radius=15)
    pygame.draw.rect(TELA,(100,100,120),rp,3,border_radius=15)
    titulo=FAM.render("RADIO",True,RADIO_TXT); TELA.blit(titulo,(rp.x+15,rp.y+10))
    est=RADIOS[j.estacao_atual]
    nome=FT.render(est['nome'],True,est['cor']); TELA.blit(nome,(rp.x+15,rp.y+35))
    if j.carro_atual.radio_ligada: status=FAM.render(">> Tocando",True,(100,255,100))
    else: status=FAM.render("|| Pausado",True,(255,200,100))
    TELA.blit(status,(rp.x+15,rp.y+70))
    teclas=FApp.render("R: Trocar | P: Play/Pause",True,(200,200,200))
    TELA.blit(teclas,(rp.x+15,rp.y+88))

def draw_bus_hud(onibus_lista, horas, minutos):
    px, py = 10, 200
    bg = pygame.Surface((280, 100 + len(onibus_lista)*35), pygame.SRCALPHA)
    bg.fill((0,0,0,180))
    TELA.blit(bg, (px, py))
    pygame.draw.rect(TELA, (100,100,120), (px, py, 280, 100 + len(onibus_lista)*35), 2, border_radius=8)
    titulo = FAM.render("ONIBUS DE TORCIDA", True, (255,255,100))
    TELA.blit(titulo, (px+10, py+8))
    info1 = FApp.render("Palmeiras: chega 19:10", True, VP)
    info2 = FApp.render("Gremio: chega 19:30", True, (100,180,255))
    TELA.blit(info1, (px+10, py+30))
    TELA.blit(info2, (px+10, py+48))
    y_off = py+70
    horario_atual = horas * 60 + minutos
    if not any(o.time == 'palmeiras' for o in onibus_lista) and horario_atual < 19*60+10:
        restante = (19*60+10) - horario_atual
        st = FApp.render(f"PAL: faltam {restante//60}h{restante%60:02d}m", True, CZ)
        TELA.blit(st, (px+10, y_off)); y_off += 20
    if not any(o.time == 'gremio' for o in onibus_lista) and horario_atual < 19*60+30:
        restante = (19*60+30) - horario_atual
        st = FApp.render(f"GRE: faltam {restante//60}h{restante%60:02d}m", True, CZ)
        TELA.blit(st, (px+10, y_off)); y_off += 20
    for o in onibus_lista:
        nome = "PAL" if o.time == 'palmeiras' else "GRE"
        cor = VP if o.time == 'palmeiras' else (100,180,255)
        if o.chegou and o.fans_soltos < o.total_fans:
            st = FApp.render(f"{nome}: soltando {o.fans_soltos}/{o.total_fans}", True, cor)
        elif o.chegou:
            st = FApp.render(f"{nome}: chegou!", True, cor)
        else:
            st = FApp.render(f"{nome}: chegando...", True, cor)
        TELA.blit(st, (px+10, y_off)); y_off += 20

def main():
    if not loading():
        pygame.quit(); return
    rp=pygame.time.Clock(); rj=Relogio(); cl=Clima()
    j=Jogador(CX,CY+500); cel=Celular(); chat=Chat()
    ped,segs,carros,helis,cach=[],[],[],[],[]
    part=[]; brigas=[]; viaturas=[]; onibus=[]
    fumacas_rojão = []
    metro=Trem(); msg_sv,t_sv=False,0
    tp=Torcida(CX-600,CY+RE+250,'palmeiras'); tg=Torcida(CX+600,CY+RE+250,'gremio')
    torc=[tp,tg]; pred=criar_predios()
    sems=[]
    for rx in RV:
        if abs(rx-CX)<500: continue
        for ry in RH:
            if abs(ry-CY)<500: continue
            sems.append(Sem(rx+60,ry+60,True)); sems.append(Sem(rx+60,ry+60,False))
    sm2=[SemM(1200,TY-10),SemM(3000,TY-10)]
    for i in range(6): segs.append(Seguranca((2*math.pi/6)*i,'police'))
    ped=[Pedestre() for _ in range(80)]
    carros=[Carro() for _ in range(30)]
    helis=[Heli() for _ in range(4)]
    cach=[Cachorro() for _ in range(15)]
    molecada=[]; bola=None
    tnb=0; fim=False; tfi=0; fog=False; fdur=30; tsf=0; mfim=False; tmf=0
    luzes_apagadas=False; msg_hora_ir=False; tempo_msg_hora=0
    rodando=True; tempo_spawn_mole=0; hora_ir_disparada=False
    estado_prisao = {'preso': False, 'tempo': 0, 'fase': '', 'transportando': False, 'duracao': 30.0}
    msg_prisao=False; tempo_msg_prisao=0
    msg_liberdade=False; tempo_msg_liberdade=0
    cam_x_suave = j.x - LARGURA_TELA//2
    cam_y_suave = j.y - ALTURA_TELA//2
    tempo_amb = 0
    onibus_palmeiras_spawn = False
    onibus_gremio_spawn = False
    msg_bus_pal = False; tempo_msg_bus_pal = 0
    msg_bus_gre = False; tempo_msg_bus_gre = 0

    def chamar_policia(x, y):
        try:
            if not estado_prisao['preso']:
                for _ in range(2):
                    vx = x + random.randint(-400, 400); vy = y + random.randint(-400, 400)
                    viaturas.append(ViaturaPolicia(vx, vy))
                tocar('sirene','sirene',0.6)
        except: pass

    while rodando:
        dt=rp.tick(60)/1000
        rj.atualizar(dt); cl.atualizar(dt,rj.get_horas())
        h=rj.get_horas(); m=rj.get_minutos()
        horario_atual = h * 60 + m
        CAM_SHAKE.atualizar(dt)
        for n in NUVENS:
            n['x'] += n['vel'] * dt
            if n['x'] > TM + 500: n['x'] = -500
        tempo_amb += dt
        if tempo_amb > 0.3:
            tempo_amb = 0
            if random.random() < 0.4:
                px = j.x + random.randint(-LARGURA_TELA//2, LARGURA_TELA//2)
                py = j.y + random.randint(-ALTURA_TELA//2, ALTURA_TELA//2)
                part.append(Particula(px, py, 'poeira' if random.random()<0.7 else 'folha'))
        
        if not onibus_palmeiras_spawn and horario_atual >= 19*60+10:
            onibus_palmeiras_spawn = True
            onibus.append(OnibusTorcida('palmeiras'))
            msg_bus_pal = True; tempo_msg_bus_pal = pygame.time.get_ticks()
            for _ in range(60):
                part.append(Particula(CX + random.randint(-300, 300), CY + random.randint(-100, 300), 'confete'))
        if not onibus_gremio_spawn and horario_atual >= 19*60+30:
            onibus_gremio_spawn = True
            onibus.append(OnibusTorcida('gremio'))
            msg_bus_gre = True; tempo_msg_bus_gre = pygame.time.get_ticks()
            for _ in range(60):
                part.append(Particula(CX + random.randint(-300, 300), CY + random.randint(-100, 300), 'confete'))
        
        for e in pygame.event.get():
            if e.type==pygame.QUIT: rodando=False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_F11: pygame.display.toggle_fullscreen()
                if e.key==pygame.K_ESCAPE: rodando=False
                if e.key==pygame.K_v:
                    j.primeira_pessoa = not j.primeira_pessoa
                    if j.primeira_pessoa:
                        j.fala=Fala(j.x,j.y,"Modo primeira pessoa!",cor=(100,255,255),dur=2.0)
                    else:
                        j.fala=Fala(j.x,j.y,"Modo terceira pessoa.",cor=(255,220,100),dur=2.0)
                if e.key==pygame.K_LSHIFT or e.key==pygame.K_RSHIFT:
                    if not estado_prisao['preso']:
                        cel.min=not cel.min
                        if pode_tocar('notificacao',0.3): tocar('notificacao','notificacao',0.3)
                if e.key==pygame.K_c and not cel.min and cel.app=='camera' and not estado_prisao['preso']: cel.tirar_foto(TELA)
                if e.key==pygame.K_SPACE and not j.no_carro and not estado_prisao['preso']:
                    todos=[j]+ped+[s for s in segs]
                    for p in pred:
                        if math.hypot(p.x-j.x,p.y-j.y)<300: todos.extend(p.moradores)
                    j.socar(todos, part, chamar_policia)
                if e.key==pygame.K_e and not estado_prisao['preso']:
                    if MX<j.x<MX+ML and MY<j.y<MY+MA:
                        if salvar(j,rj):
                            msg_sv=True; t_sv=pygame.time.get_ticks()
                            tocar('notificacao','notificacao',0.5)
                if e.key==pygame.K_f and not estado_prisao['preso']: j.falar(random.choice(FALAS_JOG))
                if e.key==pygame.K_y and not estado_prisao['preso']:
                    if not j.no_carro:
                        cm=None; dm=100
                        for c in carros:
                            if c.ocupado: continue
                            d=math.hypot(c.x-j.x,c.y-j.y)
                            if d<dm: dm=d; cm=c
                        if cm:
                            cm.ocupado=True; j.carro_atual=cm; j.no_carro=True
                            j.estacao_atual=cm.estacao; cm.radio_ligada=True
                            tocar('notificacao','notificacao',0.5)
                            try:
                                sn=RADIOS[j.estacao_atual]['som']
                                if 'radio' in CANAIS and SONS.get(sn):
                                    CANAIS['radio'].play(SONS[sn],loops=-1); CANAIS['radio'].set_volume(0.4)
                            except: pass
                    else:
                        c=j.carro_atual; c.ocupado=False; c.radio_ligada=False
                        try:
                            if 'radio' in CANAIS: CANAIS['radio'].stop()
                        except: pass
                        j.no_carro=False; j.carro_atual=None
                        tocar('notificacao','notificacao',0.4)
                if e.key==pygame.K_r and j.no_carro and j.carro_atual and not estado_prisao['preso']:
                    j.estacao_atual=(j.estacao_atual+1)%len(RADIOS); j.carro_atual.estacao=j.estacao_atual
                    try:
                        if 'radio' in CANAIS: CANAIS['radio'].stop()
                        sn=RADIOS[j.estacao_atual]['som']
                        if j.carro_atual.radio_ligada and 'radio' in CANAIS and SONS.get(sn):
                            CANAIS['radio'].play(SONS[sn],loops=-1); CANAIS['radio'].set_volume(0.4)
                    except: pass
                    tocar('notificacao','notificacao',0.3)
                if e.key==pygame.K_p and j.no_carro and j.carro_atual and not estado_prisao['preso']:
                    j.carro_atual.radio_ligada=not j.carro_atual.radio_ligada
                    try:
                        sn=RADIOS[j.estacao_atual]['som']
                        if j.carro_atual.radio_ligada and 'radio' in CANAIS and SONS.get(sn):
                            CANAIS['radio'].play(SONS[sn],loops=-1); CANAIS['radio'].set_volume(0.4)
                        elif 'radio' in CANAIS: CANAIS['radio'].stop()
                    except: pass
            if e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==1 and not estado_prisao['preso']: cel.clique(e.pos)
        
        for o in onibus:
            o.atualizar(dt, torc, part, fumacas_rojão)
        
        if estado_prisao['preso']:
            tempo_passado = (pygame.time.get_ticks() - estado_prisao['tempo']) / 1000.0
            if estado_prisao['fase']=='algemando' and tempo_passado > 2.0:
                estado_prisao['fase']='transportando'; estado_prisao['tempo']=pygame.time.get_ticks()
                if viaturas:
                    viaturas[0].levando_jogador=True
                    estado_prisao['transportando']=True
                    j.fala=Fala(j.x,j.y,random.choice(FALAS_PRESO),cor=(255,150,150),dur=2.5)
            elif estado_prisao['fase']=='transportando':
                if not estado_prisao['transportando']:
                    estado_prisao['fase']='cumprindo_pena'
                    estado_prisao['tempo']=pygame.time.get_ticks()
                    j.x = DEL_X+DEL_L//2; j.y = DEL_Y+DEL_A+50
                    j.preso=True
                    if not msg_prisao: msg_prisao=True; tempo_msg_prisao=pygame.time.get_ticks()
                    try: tocar('prisao','efeitos',0.6)
                    except: pass
            elif estado_prisao['fase']=='cumprindo_pena':
                tempo_pena = (pygame.time.get_ticks() - estado_prisao['tempo']) / 1000.0
                if tempo_pena > estado_prisao['duracao']:
                    estado_prisao['preso']=False; estado_prisao['fase']=''; j.preso=False
                    j.x = DEL_X + DEL_L//2 + random.randint(-100,100)
                    j.y = DEL_Y + DEL_A + 120
                    msg_liberdade=True; tempo_msg_liberdade=pygame.time.get_ticks()
                    viaturas.clear()
                    for s in segs: s.atirando_no_jogador=False
                    j.fala=Fala(j.x,j.y,"To livre! Valeu!",cor=(200,255,200),dur=3.0)
                    tocar('notificacao','notificacao',0.6)
        if not estado_prisao['preso']:
            for v in viaturas: v.atualizar(dt, j, estado_prisao)
            viaturas=[v for v in viaturas if not (v.chegou and not v.levando_jogador and v.tempo_no_local>10) and not estado_prisao['preso']]
        for s in sems: s.atualizar(dt)
        for s in sm2: s.atualizar(metro)
        if h>=22 and not fim:
            fim=True; fog=True
            tfi=pygame.time.get_ticks()/1000
            mfim=True; tmf=pygame.time.get_ticks()
            torc.clear(); ped.clear(); brigas.clear()
            for _ in range(200):
                part.append(Particula(CX+random.randint(-500,500), CY+random.randint(-500,500), 'fogo', random.choice([VFG, VRO, (255,255,100), (100,200,255)])))
        if fog:
            td=(pygame.time.get_ticks()/1000)-tfi
            if td>fdur: fog=False
            else:
                tsf+=dt
                if tsf>0.3:
                    tsf=0
                    fx=CX+random.randint(-400,400); fy=CY+random.randint(-400,400)
                    for _ in range(25): part.append(Particula(fx,fy-200,'fogo',VFG))
                    if pode_tocar('fogo',0.3): tocar('fogo','efeitos',0.5)
        if fim and not fog:
            tempo_spawn_mole+=dt
            if tempo_spawn_mole>3 and len(molecada)<15:
                tempo_spawn_mole=0; molecada.append(Molecada())
                if bola is None: bola=Bola()
        if h>=23 and m>=40 and not hora_ir_disparada:
            hora_ir_disparada=True; luzes_apagadas=True
            msg_hora_ir=True; tempo_msg_hora=pygame.time.get_ticks()
            tocar('apagar','efeitos',0.6)
            for mo in molecada:
                if mo.est in ('jogando','esperando','indo','autorizado'):
                    mo.est='hora_ir'; mo.destino=None
                    mo.fala=Fala(mo.x,mo.y,random.choice(FALAS_HORA_IR),cor=(255,255,180),dur=3.0,tipo_fala='crianca')
            if segs:
                segs[0].fala=Fala(segs[0].x,segs[0].y,random.choice(FALAS_SEG_APAGA),cor=(200,255,200),dur=3.0)
        if luzes_apagadas and h<6:
            for mo in molecada:
                if mo.est in ('jogando','esperando','autorizado','indo'):
                    mo.est='hora_ir'; mo.destino=None
            if bola is not None:
                qtd=sum(1 for mo in molecada if mo.est=='jogando')
                if qtd==0: bola=None
        if not fim:
            if 18<=h<22 and len(ped)<150: ped.extend([Pedestre() for _ in range(2)])
            tnb+=dt
            if tnb>20 and len(brigas)<3:
                tnb=0
                if random.random()<0.5: bx,by=tp.x+random.randint(-150,150),tp.y+random.randint(-150,150)
                else: bx,by=tg.x+random.randint(-150,150),tg.y+random.randint(-150,150)
                brigas.append(Briga(bx,by)); tocar('sirene','sirene',0.4)
            brigas=[b for b in brigas if b.atualizar(dt)]
        for s in segs: s.atualizar(dt,brigas,j,part)
        for p in ped: p.atualizar(segs,dt,j)
        for c in carros: c.atualizar(sems,sm2,dt)
        for hh in helis: hh.atualizar(dt)
        for c in cach: c.atualizar(dt)
        metro.atualizar()
        chat.atualizar(dt,j,ped)
        # Atualiza prédios (TVs e moradoras com bandeira)
        for p in pred: p.atualizar(dt, h)
        for p in pred:
            for m2 in p.moradores: m2.atualizar(dt)
        if not fim:
            for t in torc: 
                t.atualizar(dt, part, fumacas_rojão)
        fumacas_rojão = [f for f in fumacas_rojão if f.atualizar(dt)]
        for mo in molecada: mo.atualizar(dt,segs)
        molecada=[mo for mo in molecada if mo.est!='embora']
        if bola is not None and len(molecada)>0: bola.atualizar(dt,molecada)
        part=[p for p in part if p.atualizar(dt)]
        try:
            if helis and 'heli' in CANAIS and SONS.get('helicoptero') and not estado_prisao['preso']:
                min_dist=min(math.hypot(hh.x-j.x,hh.y-j.y) for hh in helis)
                vol=max(0,min(0.5,0.5*(1-min_dist/1500)))
                if vol>0.05:
                    if not CANAIS['heli'].get_busy(): CANAIS['heli'].play(SONS['helicoptero'],loops=-1)
                    CANAIS['heli'].set_volume(vol)
                else: CANAIS['heli'].stop()
            elif estado_prisao['preso']:
                try: CANAIS['heli'].stop()
                except: pass
        except: pass
        tk=pygame.key.get_pressed()
        if j.no_carro and j.carro_atual and not estado_prisao['preso']:
            c=j.carro_atual; vc=8; mov=False
            if tk[pygame.K_a] or tk[pygame.K_LEFT]: c.x-=vc; mov=True
            if tk[pygame.K_d] or tk[pygame.K_RIGHT]: c.x+=vc; mov=True
            if tk[pygame.K_w] or tk[pygame.K_UP]: c.y-=vc; mov=True
            if tk[pygame.K_s] or tk[pygame.K_DOWN]: c.y+=vc; mov=True
            c.x=max(0,min(TM,c.x)); c.y=max(0,min(TM,c.y)); j.x=c.x; j.y=c.y
            if mov:
                if pode_tocar('carro',0.4): tocar('carro','efeitos',0.2)
                if random.random()<0.3: part.append(Particula(c.x, c.y, 'poeira'))
        else:
            j.mover(tk,dt)
        if j.ts>0: j.ts-=dt
        else: j.soc=False
        if j.tempo_apanhar>0: j.tempo_apanhar-=dt
        if j.fala:
            j.fala.x=j.x; j.fala.y=j.y
            if not j.fala.atualizar(dt): j.fala=None
        j.vida=max(0,min(100,j.vida))
        
        target_cam_x = j.x - LARGURA_TELA//2
        target_cam_y = j.y - ALTURA_TELA//2
        cam_x_suave += (target_cam_x - cam_x_suave) * 0.15
        cam_y_suave += (target_cam_y - cam_y_suave) * 0.15
        shake_x, shake_y = CAM_SHAKE.get_offset()
        camx = cam_x_suave + shake_x
        camy = cam_y_suave + shake_y
        
        desenhar_ceu(camx, camy, h)
        draw_chao(camx,camy); draw_mansao(camx,camy)
        draw_delegacia(camx,camy)
        # Desenha prédios (com TVs e bandeira da moradora)
        for p in pred: p.desenhar(camx,camy,h)
        for p in pred:
            if math.hypot(p.x-j.x,p.y-j.y)<800:
                for m2 in p.moradores: m2.desenhar(camx,camy)
        draw_estadio(camx,camy,fim,luzes_apagadas)
        metro.desenhar(camx,camy)
        for c in carros: c.desenhar(camx,camy)
        for o in onibus: o.desenhar(camx, camy)
        for v in viaturas: v.desenhar(camx,camy)
        if not fim:
            for t in torc: t.desenhar(camx,camy)
        for b in brigas: b.desenhar(camx,camy)
        for s in segs: s.desenhar(camx,camy)
        for p in ped: p.desenhar(camx,camy)
        for c in cach: c.desenhar(camx,camy)
        for mo in molecada: mo.desenhar(camx,camy)
        if bola is not None: bola.desenhar(camx,camy)
        if not j.primeira_pessoa and not j.no_carro and not estado_prisao['preso']:
            j.desenhar(camx,camy)
        for hh in helis: hh.desenhar(camx,camy)
        for s in sems: s.desenhar(camx,camy)
        for s in sm2: s.desenhar(camx,camy)
        for p in part: p.desenhar(camx,camy)
        for f in fumacas_rojão: f.desenhar(camx, camy)
        draw_noite(camx,camy,h,cl,luzes_apagadas)
        cl.desenhar()
        
        if j.primeira_pessoa and not estado_prisao['preso']:
            draw_zoom_frame()
            draw_crosshair()
            if not j.no_carro: draw_hands_fps(j, cel)
            aviso_v=FAM.render("MODO PRIMEIRA PESSOA (V para voltar)",True,(100,255,255))
            TELA.blit(aviso_v,(LARGURA_TELA//2-aviso_v.get_width()//2,ALTURA_TELA-150))
        
        cel.desenhar(TELA,rj,cl); chat.desenhar(); draw_radio_hud(j)
        draw_bus_hud(onibus, h, m)
        TELA.blit(VINHETA,(0,0))
        hd=pygame.Surface((LARGURA_TELA,60),pygame.SRCALPHA); hd.fill((0,0,0,180)); TELA.blit(hd,(0,0))
        t1=FT.render("PALMEIRAS",True,VP); t2=FT.render("GRE",True,(100,180,255))
        pg=FP.render(f"{PP} x {PG}",True,BR)
        if luzes_apagadas: ct=FTX.render("LUZES APAGADAS - ESTADIO FECHADO",True,(255,100,100))
        elif fim: ct=FTX.render("FIM - MOLECADA NO CAMPO!",True,AB)
        else: ct=FTX.render("FINAL COPA DO BRASIL - Bandeira do Brasil",True,AB)
        TELA.blit(t1,(60,15)); TELA.blit(t2,(LARGURA_TELA-200,15))
        TELA.blit(pg,(LARGURA_TELA//2-pg.get_width()//2,10))
        TELA.blit(ct,(LARGURA_TELA//2-ct.get_width()//2,40))
        tr=FU.render(rj.fmt(),True,BR)
        fr=pygame.Surface((tr.get_width()+20,tr.get_height()+10)); fr.set_alpha(150); fr.fill(PT)
        TELA.blit(fr,(10,70)); TELA.blit(tr,(20,75))
        clt=FT.render(f"{cl.nome()} {cl.temp}C",True,BR)
        fcl=pygame.Surface((clt.get_width()+20,clt.get_height()+10)); fcl.set_alpha(150); fcl.fill(PT)
        TELA.blit(fcl,(10,105)); TELA.blit(clt,(20,110))
        vx,vy=10,155
        pygame.draw.rect(TELA,(0,0,0),(vx-5,vy-5,260,40),border_radius=8)
        pygame.draw.rect(TELA,(80,0,0),(vx,vy,250,30),border_radius=5)
        wv=int(250*(max(0,j.vida)/100))
        cv=VDV if j.vida>50 else((255,165,0) if j.vida>25 else VV)
        pygame.draw.rect(TELA,cv,(vx,vy,wv,30),border_radius=5)
        pygame.draw.rect(TELA,PT,(vx,vy,250,30),3,border_radius=5)
        tv=FT.render(f"VIDA {int(j.vida)}%",True,BR); TELA.blit(tv,(vx+125-tv.get_width()//2,vy+2))
        modo = "FPS" if j.primeira_pessoa else "3rd"
        dica=FD.render(f"[{modo}] V: Camera | Y: Carro | R: Radio | SHIFT: Celular | ESPACO: Socar",True,BR)
        fd=pygame.Surface((dica.get_width()+10,dica.get_height()+5)); fd.set_alpha(100); fd.fill(PT)
        TELA.blit(fd,(10,ALTURA_TELA-30)); TELA.blit(dica,(15,ALTURA_TELA-28))
        if not j.no_carro and not estado_prisao['preso']:
            for c in carros:
                if not c.ocupado and math.hypot(c.x-j.x,c.y-j.y)<100:
                    av=FA.render("Y = Entrar no carro",True,AB)
                    TELA.blit(av,(LARGURA_TELA//2-av.get_width()//2,ALTURA_TELA-180)); break
        perigo=False
        for s in segs:
            if s.atirando_no_jogador: perigo=True; break
        if perigo and not estado_prisao['preso']:
            pulse=int(abs(math.sin(pygame.time.get_ticks()/200))*155+100)
            av=FA.render("!! A POLICIA ESTA ATIRANDO EM VOCE !!",True,(255,pulse,pulse))
            TELA.blit(av,(LARGURA_TELA//2-av.get_width()//2,170))
        if viaturas and not estado_prisao['preso']:
            qtd_v=len(viaturas)
            pulse2=int(abs(math.sin(pygame.time.get_ticks()/150))*100)+155
            av2=FAM.render(f"VIATURAS DA PM RJ CHEGANDO! ({qtd_v})",True,(100,pulse2,255))
            TELA.blit(av2,(LARGURA_TELA//2-av2.get_width()//2,200))
        if msg_bus_pal:
            if pygame.time.get_ticks()-tempo_msg_bus_pal < 5000:
                ov=pygame.Surface((LARGURA_TELA,140),pygame.SRCALPHA); ov.fill((0,0,0,200))
                TELA.blit(ov,(0,ALTURA_TELA//2-70))
                m1=FG.render("ONIBUS DO PALMEIRAS CHEGOU!",True,VP)
                m2=FD.render("Torcida com ROJOES VERDE e BRANCO!",True,(200,255,200))
                TELA.blit(m1,(LARGURA_TELA//2-m1.get_width()//2,ALTURA_TELA//2-55))
                TELA.blit(m2,(LARGURA_TELA//2-m2.get_width()//2,ALTURA_TELA//2+20))
            else: msg_bus_pal=False
        if msg_bus_gre:
            if pygame.time.get_ticks()-tempo_msg_bus_gre < 5000:
                ov=pygame.Surface((LARGURA_TELA,140),pygame.SRCALPHA); ov.fill((0,0,0,200))
                TELA.blit(ov,(0,ALTURA_TELA//2-70))
                m1=FG.render("ONIBUS DO GREMIO CHEGOU!",True,AG)
                m2=FD.render("Torcida com ROJOES AZUIS!",True,(200,220,255))
                TELA.blit(m1,(LARGURA_TELA//2-m1.get_width()//2,ALTURA_TELA//2-55))
                TELA.blit(m2,(LARGURA_TELA//2-m2.get_width()//2,ALTURA_TELA//2+20))
            else: msg_bus_gre=False
        if fim and len(molecada)>0:
            jogando=sum(1 for m2 in molecada if m2.est=='jogando')
            if jogando>0:
                info=FAM.render(f"Molecada jogando bola: {jogando}",True,(255,255,100))
                TELA.blit(info,(LARGURA_TELA//2-info.get_width()//2,230))
        if MX<j.x<MX+ML and MY<j.y<MY+MA and not estado_prisao['preso']:
            av=FA.render("E = Salvar",True,AB)
            TELA.blit(av,(LARGURA_TELA//2-av.get_width()//2,ALTURA_TELA-100))
        if msg_sv:
            if pygame.time.get_ticks()-t_sv<2000:
                m=FA.render("JOGO SALVO!",True,VB); TELA.blit(m,(LARGURA_TELA//2-m.get_width()//2,130))
            else: msg_sv=False
        if cel.mf:
            if pygame.time.get_ticks()-cel.tuf<1500:
                m=FU.render(f"Foto {cel.cf-1} salva!",True,AB)
                TELA.blit(m,(LARGURA_TELA//2-m.get_width()//2,ALTURA_TELA-60))
            else: cel.mf=False
        if mfim:
            if pygame.time.get_ticks()-tmf<5000:
                ov=pygame.Surface((LARGURA_TELA,200),pygame.SRCALPHA); ov.fill((0,0,0,180))
                TELA.blit(ov,(0,ALTURA_TELA//2-100))
                m1=FB.render("FIM DE JOGO!",True,AB); m2=FA.render("PALMEIRAS CAMPEAO!",True,VP)
                TELA.blit(m1,(LARGURA_TELA//2-m1.get_width()//2,ALTURA_TELA//2-100))
                TELA.blit(m2,(LARGURA_TELA//2-m2.get_width()//2,ALTURA_TELA//2-10))
            else: mfim=False
        if msg_hora_ir:
            if pygame.time.get_ticks()-tempo_msg_hora<6000:
                ov=pygame.Surface((LARGURA_TELA,180),pygame.SRCALPHA); ov.fill((0,0,0,200))
                TELA.blit(ov,(0,ALTURA_TELA//2-90))
                m1=FB.render("23:40 - HORA DE IR EMBORA!",True,(255,200,100))
                m2=FA.render("Molecada pega a bike e vai pra casa!",True,(200,255,200))
                TELA.blit(m1,(LARGURA_TELA//2-m1.get_width()//2,ALTURA_TELA//2-70))
                TELA.blit(m2,(LARGURA_TELA//2-m2.get_width()//2,ALTURA_TELA//2+10))
            else: msg_hora_ir=False
        if msg_prisao:
            if pygame.time.get_ticks()-tempo_msg_prisao<4000:
                ov=pygame.Surface((LARGURA_TELA,200),pygame.SRCALPHA); ov.fill((0,0,0,220))
                TELA.blit(ov,(0,ALTURA_TELA//2-100))
                m1=FG.render("VOCE FOI PRESO!",True,(255,80,80))
                m2=FA.render("Policia do Rio de Janeiro - 12 DP",True,BR)
                TELA.blit(m1,(LARGURA_TELA//2-m1.get_width()//2,ALTURA_TELA//2-90))
                TELA.blit(m2,(LARGURA_TELA//2-m2.get_width()//2,ALTURA_TELA//2+20))
            else: msg_prisao=False
        if msg_liberdade:
            if pygame.time.get_ticks()-tempo_msg_liberdade<3000:
                m1=FA.render("VOCE FOI LIBERADO!",True,VDV)
                TELA.blit(m1,(LARGURA_TELA//2-m1.get_width()//2,ALTURA_TELA//2-200))
            else: msg_liberdade=False
        if estado_prisao['preso'] and estado_prisao['fase']=='cumprindo_pena':
            tempo_pena = (pygame.time.get_ticks() - estado_prisao['tempo']) / 1000.0
            tempo_restante = max(0, estado_prisao['duracao'] - tempo_pena)
            draw_cela(camx, camy, tempo_restante)
        # Minimapa
        mx,my,mt=LARGURA_TELA-220,20,200
        pygame.draw.rect(TELA,PT,(mx-3,my-3,mt+6,mt+6),border_radius=6)
        pygame.draw.rect(TELA,(30,30,30),(mx,my,mt,mt))
        e=mt/TM
        pygame.draw.rect(TELA,CPM,(mx+MX*e,my+MY*e,ML*e,MA*e))
        pygame.draw.rect(TELA,COR_DELEGACIA,(mx+DEL_X*e,my+DEL_Y*e,DEL_L*e,DEL_A*e))
        pygame.draw.ellipse(TELA,BR,(mx+(CX-RE)*e,my+(CY-RE)*e,RE*2*e,RE*2*e))
        # Prédios no minimapa
        for p in pred:
            pygame.draw.rect(TELA, (90,90,100), (mx+int(p.x*e), my+int(p.y*e), max(1,int(p.largura*e)), max(1,int(p.altura*e))))
        for c in carros: pygame.draw.circle(TELA,c.cor,(mx+int(c.x*e),my+int(c.y*e)),1)
        for o in onibus:
            ox = mx + int(o.x*e); oy = my + int(o.y*e)
            cor_bus = VP if o.time == 'palmeiras' else (100,180,255)
            pygame.draw.rect(TELA, cor_bus, (ox-4, oy-2, 8, 4), border_radius=2)
        for v in viaturas: pygame.draw.circle(TELA,AZUL_POLICIA,(mx+int(v.x*e),my+int(v.y*e)),3)
        for p in ped: pygame.draw.circle(TELA,p.cor_camisa,(mx+int(p.x*e),my+int(p.y*e)),1)
        for t in torc: pygame.draw.circle(TELA,t.cor,(mx+int(t.x*e),my+int(t.y*e)),4)
        for m in molecada:
            if m.est!='embora': pygame.draw.circle(TELA,m.cor_camisa,(mx+int(m.x*e),my+int(m.y*e)),2)
        for s in segs:
            c=(0,0,255) if s.tipo=='police' else (30,30,30)
            pygame.draw.circle(TELA,c,(mx+int(s.x*e),my+int(s.y*e)),2)
        jx,jy=mx+int(j.x*e),my+int(j.y*e)
        if j.primeira_pessoa:
            pygame.draw.circle(TELA,(100,255,255),(jx,jy),4)
            pygame.draw.circle(TELA,AB,(jx,jy),4,2)
        else:
            pygame.draw.circle(TELA,AB,(jx,jy),3)
            pygame.draw.circle(TELA,VB,(jx,jy),3,1)
        pygame.display.flip()
    try:
        if 'radio' in CANAIS: CANAIS['radio'].stop()
        if 'heli' in CANAIS: CANAIS['heli'].stop()
    except: pass
    pygame.quit()

if __name__=="__main__":
    main()