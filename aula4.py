3

import re
from collections import Counter
from pathlib import Path


STOPWORDS = {
    "a", "ao", "as", "com", "da", "das", "de", "do", "dos", "e", "em",
    "é", "na", "nas", "no", "nos", "o", "os", "para", "por", "que",
    "se", "um", "uma", "uns", "umas", "como", "mais", "mas", "ou",
}


def ler_arquivo(caminho):
    return Path(caminho).read_text(encoding="utf-8")


def separar_palavras(texto):
    return re.findall(r"\b[\wÀ-ÿ]+\b", texto.lower())


def separar_frases(texto):
    frases = re.split(r"(?<=[.!?])\s+|\n+", texto.strip())
    return [frase.strip() for frase in frases if len(frase.strip()) > 0]


def resumir(texto, quantidade=3):
    frases = separar_frases(texto)
    if not frases:
        return ""

    palavras = separar_palavras(texto)
    frequencias = Counter(
        palavra for palavra in palavras if palavra not in STOPWORDS
    )

    frases_ordenadas = sorted(
        enumerate(frases),
        key=lambda item: sum(
            frequencias[palavra]
            for palavra in separar_palavras(item[1])
            if palavra not in STOPWORDS
        ),
        reverse=True,
    )

    indices_selecionados = sorted(
        indice for indice, _ in frases_ordenadas[:quantidade]
    )
    return " ".join(frases[indice] for indice in indices_selecionados)


def main():
    caminho = input("Digite o caminho do arquivo: ").strip().strip('"')

    if not caminho:
        print("Caminho não informado.")
        return

    try:
        texto = ler_arquivo(caminho)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return
    except UnicodeDecodeError:
        print("O arquivo precisa estar codificado em UTF-8.")
        return

    palavras = separar_palavras(texto)
    frases = separar_frases(texto)
    linhas = texto.splitlines()

    frequencias = Counter(
        palavra for palavra in palavras if palavra not in STOPWORDS
    )

    print("\n--- Estatísticas ---")
    print(f"Caracteres: {len(texto)}")
    print(f"Linhas: {len(linhas)}")
    print(f"Palavras: {len(palavras)}")
    print(f"Frases: {len(frases)}")

    if frequencias:
        mais_comuns = ", ".join(
            f"{palavra} ({quantidade})"
            for palavra, quantidade in frequencias.most_common(5)
        )
        print(f"Palavras mais comuns: {mais_comuns}")

    print("\n--- Resumo ---")
    print(resumir(texto, quantidade=3))


if __name__ == "__main__":
    main()
