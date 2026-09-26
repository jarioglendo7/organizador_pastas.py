

import argparse
import shutil
from pathlib import Path

# Mapeamento de categorias -> extensões
CATEGORIAS = {
    "PDFs": [".pdf"],
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff", ".heic"],
    "Documentos": [
        ".doc", ".docx", ".odt", ".txt", ".rtf",
        ".xls", ".xlsx", ".ods", ".csv",
        ".ppt", ".pptx", ".odp",
    ],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Instaladores": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".appimage"],
}

PASTA_OUTROS = "Outros"


def obter_pasta_downloads() -> Path:
    """Retorna o caminho padrão da pasta Downloads do usuário."""
    return Path.home() / "Downloads"


def categorizar_arquivo(caminho: Path) -> str:
    """Retorna o nome da categoria (subpasta) para um dado arquivo."""
    extensao = caminho.suffix.lower()
    for categoria, extensoes in CATEGORIAS.items():
        if extensao in extensoes:
            return categoria
    return PASTA_OUTROS


def organizar(pasta_downloads: Path, simular: bool = False) -> None:
    if not pasta_downloads.exists():
        print(f"❌ A pasta '{pasta_downloads}' não existe.")
        return

    arquivos = [f for f in pasta_downloads.iterdir() if f.is_file()]

    if not arquivos:
        print("Nenhum arquivo encontrado na pasta de Downloads.")
        return

    total_movidos = 0
    resumo = {}

    for arquivo in arquivos:
        # Ignora arquivos ocultos/de sistema (ex: .DS_Store, desktop.ini)
        if arquivo.name.startswith("."):
            continue

        categoria = categorizar_arquivo(arquivo)
        pasta_destino = pasta_downloads / categoria

        if simular:
            print(f"[SIMULAÇÃO] {arquivo.name} -> {categoria}/")
        else:
            pasta_destino.mkdir(exist_ok=True)
            destino_final = pasta_destino / arquivo.name

            # Evita sobrescrever arquivos com o mesmo nome
            contador = 1
            while destino_final.exists():
                novo_nome = f"{arquivo.stem}_{contador}{arquivo.suffix}"
                destino_final = pasta_destino / novo_nome
                contador += 1

            shutil.move(str(arquivo), str(destino_final))
            print(f"✔ {arquivo.name} -> {categoria}/{destino_final.name}")

        resumo[categoria] = resumo.get(categoria, 0) + 1
        total_movidos += 1

    print("\n--- Resumo ---")
    for categoria, qtd in resumo.items():
        print(f"{categoria}: {qtd} arquivo(s)")
    print(f"Total: {total_movidos} arquivo(s) {'identificados' if simular else 'movidos'}.")


def main():
    parser = argparse.ArgumentParser(description="Organiza a pasta de Downloads por tipo de arquivo.")
    parser.add_argument(
        "--pasta",
        type=str,
        default=None,
        help="Caminho customizado da pasta a organizar (padrão: pasta Downloads do usuário).",
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Mostra o que seria feito, sem mover nenhum arquivo.",
    )
    args = parser.parse_args()

    pasta = Path(args.pasta).expanduser() if args.pasta else obter_pasta_downloads()

    print(f"📂 Organizando: {pasta}\n")
    organizar(pasta, simular=args.simular)


if __name__ == "__main__":
    main()