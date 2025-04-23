from typing import Optional
from mcp.server.fastmcp import FastMCP
from web import BuscadorWeb
from functools import lru_cache

# Initialize FastMCP server
mcp = FastMCP("mojeek")

# Cache para armazenar resultados de buscas recentes
@lru_cache(maxsize=100)
def cached_search(termo: str, max_paginas: int = 1) -> str:
    buscador = BuscadorWeb()
    buscador.buscar_mojeek(termo, max_paginas=max_paginas)
    return buscador.mostrar_resultados(10)

@mcp.tool()
async def get_search(termo: str) -> str:
    """Realiza busca no Mojeek e retorna os resultados.
    O Mojeek é um motor de busca que fornece resultados imparciais, rápidos e relevantes,
    combinado com uma política de privacidade sem rastreamento.

    Args:
        termo: Palavra ou palavras para pesquisar.

    Returns:
        str: Resultados da busca formatados.

    Raises:
        ValueError: Se o termo de busca estiver vazio ou for inválido.
        Exception: Se ocorrer um erro durante a busca.
    """
    # Validação do termo de busca
    if not termo or termo.isspace():
        raise ValueError("O termo de busca não pode estar vazio")

    try:
        # Tenta recuperar resultados do cache primeiro
        resultado = cached_search(termo)
        return resultado
    except Exception as e:
        # Log do erro e re-raise para tratamento adequado
        print(f"Erro durante a busca: {str(e)}")
        raise


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
