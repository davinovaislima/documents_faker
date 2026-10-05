# Documents Faker

Gerador de documentos médicos fictícios para uso educacional, testes e
treinamento de modelos de IA. O script cria documentos com dados sintéticos,
logos, assinaturas, selos e QR Codes e exporta cada variação como PDF.

## Funcionalidades

- Geração de atestados, receituários e laudos médicos fictícios.
- Dados sintéticos em português do Brasil: nome, CPF, endereço e CRM.
- Inserção do logotipo HCOM no cabeçalho.
- Posicionamento dos elementos por meio do arquivo `dimensoes.csv`.
- Verificação para evitar sobreposição entre imagens.
- Variações visuais com rotação do documento.
- Geração automática de 10 arquivos PDF em `output/`.

> **Aviso:** todos os dados e documentos produzidos são fictícios. Não use os
> arquivos gerados como documentos reais nem para fins fraudulentos.

## Requisitos

- Python 3.9 ou superior.
- Pip.

As principais bibliotecas utilizadas são Pillow, Faker e Pandas. Todas as
dependências estão listadas em `requirements.txt`.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/mirellaoliveiraa/documents_faker.git
cd documents_faker
```

Crie e ative um ambiente virtual (recomendado):

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS e Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

O arquivo de dependências contém apenas as bibliotecas utilizadas pelo
gerador. Isso evita instalar pacotes de outros ambientes que podem não ter
versões compatíveis com o seu sistema operacional ou com a versão do Python.

## Execução

Com o ambiente virtual ativado, execute:

```bash
python main.py
```

Os arquivos serão salvos em `output/documento_1.pdf` até
`output/documento_10.pdf`. O script também imprime no terminal o progresso de
cada documento gerado.

## Configuração do posicionamento

O arquivo `dimensoes.csv` define o tamanho e a posição de cada imagem no
canvas de `1080 x 1920` pixels. Ele usa as colunas:

| Coluna | Descrição |
| --- | --- |
| `nome` | Nome usado pelo script para localizar o elemento |
| `arquivo` | Nome do arquivo de imagem |
| `W` | Largura em pixels |
| `H` | Altura em pixels |
| `X` | Coordenada horizontal em pixels |
| `Y` | Coordenada vertical em pixels |

Exemplo:

```csv
nome,arquivo,W,H,X,Y
unimed,unimed.png,385,61,60,51
qr,qr.png,121,121,1047,1509
sign,sign.png,399,86,56,1475
```

As coordenadas `X` e `Y` indicam o canto superior esquerdo do elemento.
Imagens que ultrapassarem os limites do canvas serão reposicionadas para
caber na página.

## Estrutura do projeto

```text
documents_faker/
├── assets/
│   ├── ass_elements/  # Assinaturas e elementos de assinatura
│   ├── logo_sign/     # Logos
│   └── qr/            # QR Codes
├── dimensoes.csv      # Tamanho e posição dos elementos
├── main.py            # Script principal
├── modules/           # Módulos auxiliares
├── output/            # PDFs e imagens gerados
├── requirements.txt   # Dependências Python
└── README.md
```

Para adicionar um elemento, coloque a imagem na pasta correspondente e
adicione uma linha para ela em `dimensoes.csv`. O campo `nome` deve
corresponder ao nome do arquivo sem a extensão.

O logotipo do HCOM incluído no projeto está em `assets/logo_sign/hcom.png` e
foi configurado no CSV para aparecer no cabeçalho. Por padrão, ele é a única
imagem inserida nos documentos; QR Codes, assinaturas, selos e outros logos
não são utilizados.

## Carimbo

O gerador aplica automaticamente um carimbo retangular, centralizado, com o
texto:

```text
Dr. Marcone Novais da Silva
Médico
CRM-BA 25.751
```

Os documentos continuam sendo
simulações para uso educacional e devem ser identificados como fictícios antes
de qualquer compartilhamento.

O carimbo é textual, sem uma imagem adicional, para manter o logo HCOM como a
única imagem da receita. Para alterar o texto, edite a constante `STAMP_TEXT`
no início de `main.py`.

## Exemplo

![Exemplo de documento gerado](output/documento_gerado.png)

## Tecnologias

- [Python](https://www.python.org/)
- [Pillow](https://python-pillow.org/)
- [Faker](https://faker.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)

## Contribuição

Issues e pull requests são bem-vindos. Ao propor uma alteração, descreva
como ela foi testada e mantenha os dados gerados estritamente fictícios.
