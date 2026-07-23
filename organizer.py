#!/usr/bin/env python3
"""
File Organizer
---------------
Organiza automaticamente os arquivos de uma pasta em subpastas por tipo
(Imagens, Documentos, Planilhas, Vídeos, Áudios, Compactados, Programas, Outros).

Uso:
    python organizer.py --path /caminho/da/pasta
    python organizer.py --path /caminho/da/pasta --dry-run
    python organizer.py --path /caminho/da/pasta --log organizacao.log

Autor: Você :)
Licença: MIT
"""

import argparse
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Mapeamento de extensões para categorias
CATEGORIAS = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Planilhas": [".xls", ".xlsx", ".csv", ".ods"],
    "Apresentacoes": [".ppt", ".pptx", ".odp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audios": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programas": [".exe", ".msi", ".dmg", ".apk", ".sh", ".bat"],
    "Codigo": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".json", ".xml"],
}

PASTA_OUTROS = "Outros"


def configurar_logger(caminho_log: str | None, verbose: bool) -> logging.Logger:
    """Configura o logger para exibir no console e, opcionalmente, salvar em arquivo."""
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)

    if caminho_log:
        file_handler = logging.FileHandler(caminho_log, encoding="utf-8")
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)

    return logger


def obter_categoria(extensao: str) -> str:
    """Retorna o nome da categoria correspondente a uma extensão de arquivo."""
    extensao = extensao.lower()
    for categoria, extensoes in CATEGORIAS.items():
        if extensao in extensoes:
            return categoria
    return PASTA_OUTROS


def gerar_nome_unico(destino: Path) -> Path:
    """
    Evita sobrescrever arquivos com o mesmo nome, adicionando um sufixo numérico.
    Ex: foto.jpg -> foto (1).jpg -> foto (2).jpg
    """
    if not destino.exists():
        return destino

    contador = 1
    nome_base = destino.stem
    extensao = destino.suffix
    pasta = destino.parent

    novo_destino = pasta / f"{nome_base} ({contador}){extensao}"
    while novo_destino.exists():
        contador += 1
        novo_destino = pasta / f"{nome_base} ({contador}){extensao}"

    return novo_destino


def organizar_pasta(caminho: Path, dry_run: bool, logger: logging.Logger) -> dict:
    """
    Organiza os arquivos da pasta informada em subpastas por categoria.
    Retorna um dicionário com estatísticas da execução.
    """
    if not caminho.exists():
        logger.error(f"O caminho informado não existe: {caminho}")
        sys.exit(1)

    if not caminho.is_dir():
        logger.error(f"O caminho informado não é uma pasta: {caminho}")
        sys.exit(1)

    estatisticas = {"movidos": 0, "ignorados": 0, "categorias": {}}

    arquivos = [f for f in caminho.iterdir() if f.is_file()]

    if not arquivos:
        logger.info("Nenhum arquivo encontrado nessa pasta. Nada a fazer.")
        return estatisticas

    logger.info(f"{len(arquivos)} arquivo(s) encontrado(s) em: {caminho}")
    if dry_run:
        logger.info("Modo DRY-RUN ativado: nenhum arquivo será movido de verdade.\n")

    for arquivo in arquivos:
        # Ignora o próprio script e arquivos ocultos/sistema
        if arquivo.name.startswith(".") or arquivo.name == Path(__file__).name:
            estatisticas["ignorados"] += 1
            continue

        categoria = obter_categoria(arquivo.suffix)
        pasta_destino = caminho / categoria
        destino_final = pasta_destino / arquivo.name

        if dry_run:
            logger.info(f"[SIMULAÇÃO] '{arquivo.name}' → {categoria}/")
        else:
            pasta_destino.mkdir(exist_ok=True)
            destino_final = gerar_nome_unico(destino_final)
            try:
                shutil.move(str(arquivo), str(destino_final))
                logger.info(f"Movido: '{arquivo.name}' → {categoria}/{destino_final.name}")
            except Exception as erro:
                logger.error(f"Falha ao mover '{arquivo.name}': {erro}")
                estatisticas["ignorados"] += 1
                continue

        estatisticas["movidos"] += 1
        estatisticas["categorias"][categoria] = estatisticas["categorias"].get(categoria, 0) + 1

    return estatisticas


def exibir_resumo(stats: dict, dry_run: bool, logger: logging.Logger) -> None:
    """Exibe um resumo final da organização."""
    logger.info("\n" + "=" * 40)
    logger.info("RESUMO DA ORGANIZAÇÃO" + (" (SIMULAÇÃO)" if dry_run else ""))
    logger.info("=" * 40)
    logger.info(f"Total de arquivos processados: {stats['movidos']}")
    logger.info(f"Total de arquivos ignorados: {stats['ignorados']}")

    if stats["categorias"]:
        logger.info("\nPor categoria:")
        for categoria, quantidade in sorted(stats["categorias"].items()):
            logger.info(f"  • {categoria}: {quantidade} arquivo(s)")

    logger.info("=" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Organiza automaticamente os arquivos de uma pasta em subpastas por tipo.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Caminho da pasta que será organizada (ex: ~/Downloads)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa em modo simulação: mostra o que seria feito, sem mover nenhum arquivo",
    )
    parser.add_argument(
        "--log",
        type=str,
        default=None,
        help="Caminho de um arquivo para salvar o log da execução (opcional)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Exibe mensagens detalhadas (nível DEBUG)",
    )

    args = parser.parse_args()
    logger = configurar_logger(args.log, args.verbose)

    caminho = Path(args.path).expanduser().resolve()

    logger.info(f"Iniciando organização em: {caminho}")
    logger.info(f"Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    stats = organizar_pasta(caminho, args.dry_run, logger)
    exibir_resumo(stats, args.dry_run, logger)


if __name__ == "__main__":
    main()
