import os
import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import textwrap
from faker import Faker

# ================= CONFIGURAÇÕES =================
BASE_WIDTH = 1080
BASE_HEIGHT = 1920

OUTPUT_DIR = "./output/novos"
ASSETS_DIR = "./assets"
ASS_DIR = os.path.join(ASSETS_DIR, "ass_elements")
QR_DIR = os.path.join(ASSETS_DIR, "qr")
LOGO_DIR = os.path.join(ASSETS_DIR, "logo_sign")
SELOS_DIR = os.path.join(ASSETS_DIR, "selos_rodape")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
STAMP_DIR = os.path.join(ASSETS_DIR, "stamp")
STAMP_TEXT = "Dr. Exemplo da Silva\nMédico\nCRM-XX 00000"
CLINIC_ADDRESS = "Avenida Altamirando de Araújo Ramos, 253 - Centro, Simões Filho - BA"

faker = Faker("pt_BR")

def carregar_fonte(tamanho):
    """Carrega uma fonte disponível no sistema ou usa a fonte padrão do Pillow."""
    candidatos = [
        os.path.join(FONTS_DIR, "arial.ttf"),
        "arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for caminho in candidatos:
        if os.path.exists(caminho):
            return ImageFont.truetype(caminho, size=tamanho)
    return ImageFont.load_default(size=tamanho)

def carregar_fonte_negrito(tamanho):
    candidatos = [
        os.path.join(FONTS_DIR, "arialbd.ttf"),
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf",
    ]
    for caminho in candidatos:
        if os.path.exists(caminho):
            return ImageFont.truetype(caminho, size=tamanho)
    return carregar_fonte(tamanho)

def aplicar_carimbos(base):
    """Aplica o carimbo textual e uma imagem opcional ao documento."""
    camada = Image.new("RGBA", base.size, (255, 255, 255, 0))
    carimbo = ImageDraw.Draw(camada)
    fonte = carregar_fonte(30)
    caixa = carimbo.multiline_textbbox(
        (0, 0),
        STAMP_TEXT,
        font=fonte,
        spacing=2,
        align="center",
    )
    largura = caixa[2] - caixa[0] + 44
    altura = caixa[3] - caixa[1] + 24
    x = (BASE_WIDTH - largura) // 2
    y = (BASE_HEIGHT - altura) // 2
    carimbo.rectangle(
        (x, y, x + largura, y + altura),
        outline=(110, 110, 110, 210),
        width=2,
    )
    carimbo.multiline_text(
        (BASE_WIDTH // 2, y + 12),
        STAMP_TEXT,
        font=fonte,
        fill=(35, 35, 35, 235),
        spacing=2,
        align="center",
        anchor="ma",
    )
    base.paste(camada, (0, 0), camada)

# ================= CARREGAR CSV =================
df = pd.read_csv("dimensoes.csv")

dimensoes = {}
for _, row in df.iterrows():
    nome = row['nome']
    dimensoes[nome] = {
        'arquivo': row['arquivo'],
        'W': int(row['W']),
        'H': int(row['H']),
        'X': int(row['X']),
        'Y': int(row['Y'])
    }

# ================= FUNÇÃO INSERIR IMAGEM (ANTI-SOBREPOSIÇÃO) =================
def inserir_imagem(base, pasta, item, ocupados):
    if item not in dimensoes:
        print(f"❌ {item} não encontrado no CSV.")
        return False

    info = dimensoes[item]
    img_path = os.path.join(pasta, info['arquivo'])

    if not os.path.exists(img_path):
        print(f"❌ Arquivo {img_path} não encontrado.")
        return False

    img = Image.open(img_path).convert("RGBA")

    w = info['W']
    h = info['H']
    x = info['X']
    y = info['Y']

    # Corrige para não ultrapassar bordas
    if x + w > BASE_WIDTH:
        x = BASE_WIDTH - w
    if y + h > BASE_HEIGHT:
        y = BASE_HEIGHT - h
    x = max(0, x)
    y = max(0, y)

    # Verifica se cabe
    if w <= 0 or h <= 0:
        print(f"⚠️ {item} não cabe na área.")
        return False

    novo_retangulo = (x, y, x + w, y + h)

    # Verificar sobreposição
    for rect in ocupados:
        if not (novo_retangulo[2] <= rect[0] or novo_retangulo[0] >= rect[2] or
                novo_retangulo[3] <= rect[1] or novo_retangulo[1] >= rect[3]):
            print(f"🔴 {item} sobrepõe outro elemento. Pulando...")
            return False

    ocupados.append(novo_retangulo)

    img = img.resize((w, h))
    base.paste(img, (x, y), img)
    return True


# ================= GERAR DOCUMENTOS =================
quantidade = 1

for idx in range(1, quantidade + 1):
    base_img = Image.new("RGB", (BASE_WIDTH, BASE_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(base_img)
    ocupados = []  # Lista para controlar áreas ocupadas

    # Dados sintéticos
    nome_paciente = "Alan Geovani Barboza Santos"
    cpf = "090.929.189-62"
    endereco = CLINIC_ADDRESS
    idade = "33 anos"
    crm = "25.751/BA"

    # Título
    titulo = "PRESCRIÇÃO MÉDICA"
    titulo_font = carregar_fonte_negrito(42)
    draw.text((300, 250), titulo, fill="black", font=titulo_font)

    # Cabeçalho
    cabecalho = (
        f"Nome: {nome_paciente}   CPF: {cpf}\n"
        f"Idade: {idade}\n"
        f"Endereço: {endereco}\n"
        f"CRM: {crm}\n\n"
    )
    cabecalho_font = carregar_fonte(26)
    draw.text((100, 320), cabecalho, fill="black", font=cabecalho_font)

    # Texto corpo
    texto = """PRESCRIÇÃO MÉDICA
Nome do medicamento: AMOXICILINA + CLAVULANATO DE POTÁSSIO
Concentração: 600mg/5mL
Forma farmacêutica:  Suspensão Oral
Quantidade: 2 Frascos de 50mL
Posologia: dministrar 2,6 mL (aproximadamente 2,5 a 3 mL) por via oral, de 12 em 12 horas, durante 10
dias -
."""
    font = carregar_fonte(28)

    linhas = []
    for paragrafo in texto.splitlines():
        linhas.extend(textwrap.wrap(paragrafo, width=55) or [""])

    for i, linha in enumerate(linhas):
        y = 500 + i * 35
        draw.text((100, y), linha, fill="black", font=font)

    rodape_font = carregar_fonte(20)
    rodape_linhas = textwrap.wrap(CLINIC_ADDRESS, width=70)
    rodape_y = BASE_HEIGHT - 105
    for i, linha in enumerate(rodape_linhas):
        largura = draw.textlength(linha, font=rodape_font)
        draw.text(((BASE_WIDTH - largura) / 2, rodape_y + i * 25), linha, fill="black", font=rodape_font)

    draw.rectangle((40, 40, BASE_WIDTH - 40, BASE_HEIGHT - 40), outline="black", width=3)

    # O documento usa somente o logotipo HCOM como imagem institucional.
    inserir_imagem(base_img, LOGO_DIR, "hcom", ocupados)

    aplicar_carimbos(base_img)

    # Salvar PDF
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    output_file = os.path.join(OUTPUT_DIR, f"documento_{idx}.pdf")
    base_img.save(output_file, "PDF", resolution=100.0)
    print(f"✅ Documento {idx} gerado.")

print("🚀 Todos os documentos foram gerados com sucesso!")
