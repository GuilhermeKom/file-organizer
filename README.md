# 📁 File Organizer

Script em Python que organiza automaticamente os arquivos de uma pasta (como Downloads) em subpastas por tipo: Imagens, Documentos, Planilhas, Vídeos, Áudios, Compactados, Programas, Código e Outros.

## ✨ Funcionalidades

- Organização automática por extensão de arquivo
- Modo **dry-run** (simulação): mostra o que seria feito sem mover nada
- Evita sobrescrever arquivos duplicados (adiciona sufixo automático)
- Log detalhado no terminal e, opcionalmente, salvo em arquivo
- Resumo estatístico ao final da execução

## 🚀 Como usar

### Pré-requisitos
- Python 3.10 ou superior instalado

### Executando

Simular antes de organizar de verdade (recomendado na primeira vez):
```bash
python organizer.py --path ~/Downloads --dry-run
```

Organizar de fato:
```bash
python organizer.py --path ~/Downloads
```

Salvar um log da execução:
```bash
python organizer.py --path ~/Downloads --log organizacao.log
```

Modo detalhado (debug):
```bash
python organizer.py --path ~/Downloads --verbose
```

## 📂 Categorias

| Categoria       | Exemplos de extensão            |
|-----------------|----------------------------------|
| Imagens         | .jpg, .png, .svg, .webp          |
| Documentos      | .pdf, .docx, .txt, .md           |
| Planilhas       | .xlsx, .csv, .ods                |
| Apresentacoes   | .pptx, .odp                      |
| Videos          | .mp4, .mkv, .mov                 |
| Audios          | .mp3, .wav, .flac                |
| Compactados     | .zip, .rar, .7z                  |
| Programas       | .exe, .msi, .apk                 |
| Codigo          | .py, .js, .html, .json           |
| Outros          | qualquer extensão não mapeada    |

## 🛠️ Possíveis melhorias futuras

- Arquivo de configuração externo (`.yaml`/`.json`) para personalizar categorias
- Agendamento automático (rodar todo dia às 22h, por exemplo)
- Interface gráfica simples
- Opção de desfazer a última organização

## 📄 Licença

Este projeto está sob a licença MIT — sinta-se livre para usar, modificar e distribuir.
