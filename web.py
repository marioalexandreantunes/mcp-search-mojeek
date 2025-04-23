import requests
import pandas as pd
import time
import random
import re

from urllib.parse import quote_plus
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

class BuscadorWeb:
    
    def __init__(self):
        # User-Agent para simular um navegador
        self.user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        ]
        self.resultados = []
    
    def _get_headers(self):
        """Gera headers aleatórios para cada requisição"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
    }
    
    def limpar_resultados(self):
        """Limpa os resultados anteriores"""
        self.resultados = []

#region "BUSCADORES"  
    # Verificado
    def buscar_bing(self, termo_busca, max_paginas=1):
        """Busca resultados no Bing"""
        print(f"Buscando '{termo_busca}' no Bing...")
        termo_codificado = quote_plus(termo_busca)
        
        for pagina in tqdm(range(1, max_paginas + 1)):
            url = f"https://www.bing.com/search?q={termo_codificado}&first={(pagina-1)*10}"
            
            try:
                headers = self._get_headers()
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraindo resultados
                    for resultado in tqdm(soup.select('li.b_algo')):
                        titulo_elem = resultado.select_one('h2')
                        link_elem = resultado.select_one('h2 a')
                        descricao_elem = resultado.select_one('.b_caption p')
                        
                        if titulo_elem and link_elem and 'href' in link_elem.attrs:
                            titulo = titulo_elem.text
                            link = link_elem['href']
                            descricao = descricao_elem.text if descricao_elem else ""
                            
                            self.resultados.append({
                                'fonte': 'Bing',
                                'titulo': titulo,
                                'descricao': descricao,
                                'link': link,
                                'tipo': self._determinar_tipo_conteudo(titulo, descricao, link)
                            })
                    
                    # Pausa para evitar bloqueio
                    time.sleep(random.uniform(2, 5))
                    
            except Exception as e:
                print(f"Erro ao buscar no Bing: {e}")

        print(f"Busca concluída com {len(self.resultados)} resultados.")
        
    # Verificado
    def buscar_duckduckgo(self, termo_busca, max_paginas=1):
        """Busca resultados no DuckDuckGo"""
        print(f"Buscando '{termo_busca}' no DuckDuckGo...")
        termo_codificado = quote_plus(termo_busca)
        
        url = f"https://html.duckduckgo.com/html/?q={termo_codificado}"
        
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extraindo resultados
                for resultado in tqdm(soup.select('.result')):
                    titulo_elem = resultado.select_one('.result__title')
                    link_elem = resultado.select_one('.result__url')
                    descricao_elem = resultado.select_one('.result__snippet')
                    
                    if titulo_elem and link_elem:
                        titulo = titulo_elem.text.strip()
                        raw_link = link_elem.text.strip()
                        descricao = descricao_elem.text.strip() if descricao_elem else ""
                        
                        # Construindo o link completo
                        if not raw_link.startswith(('http://', 'https://')):
                            link = f"https://{raw_link}"
                        else:
                            link = raw_link
                        
                        self.resultados.append({
                            'fonte': 'DuckDuckGo',
                            'titulo': titulo,
                            'descricao': descricao,
                            'link': link,
                            'tipo': self._determinar_tipo_conteudo(titulo, descricao, link)
                        })
                
                # Pausa para evitar bloqueio
                time.sleep(random.uniform(2, 5))
                
        except Exception as e:
            print(f"Erro ao buscar no DuckDuckGo: {e}")
            
        print(f"Busca concluída com {len(self.resultados)} resultados.")
    
    # Verificado
    def buscar_searx(self, termo_busca, max_paginas=1):
        """Busca resultados no SearX (meta-buscador de código aberto)"""
        print(f"Buscando '{termo_busca}' no SearX...")
        termo_codificado = quote_plus(termo_busca)
        
        for pagina in range(1, max_paginas + 1):
            url = f"https://searx.be/search?q={termo_codificado}"
            
            try:
                headers = self._get_headers()
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraindo resultados
                    # <article class="result
                    
                    for resultado in tqdm(soup.select('article.result')):
                        
                        link_header_elem = resultado.select_one('a.url_header')
                        title_elem = resultado.select_one('h3 a')
                        description_elem = resultado.select_one('p.content')
                        
                        if title_elem and link_header_elem :
                            link_header_text = link_header_elem['href']
                            title = title_elem.text.strip()
                            description = description_elem.text.strip() if description_elem else ""
                            
                            self.resultados.append({
                                'fonte': 'SearX',
                                'titulo': title,
                                'descricao': description,
                                'link': link_header_text,
                                'tipo': self._determinar_tipo_conteudo(title, description, link_header_text)
                            })
                    
                    # Pausa para evitar bloqueio
                    time.sleep(random.uniform(1, 3))
                    
            except Exception as e:
                print(f"Erro ao buscar no SearX: {e}")

    # Verificado
    def buscar_mojeek(self, termo_busca, max_paginas=1):
        """Busca resultados no Mojeek (motor de busca privado)"""
        print(f"Buscando '{termo_busca}' no Mojeek...")
        termo_codificado = quote_plus(termo_busca)
        
        for pagina in range(0, max_paginas):
            pag = 0 if pagina == 0 else (pagina * 10) + 1
            url = f"https://www.mojeek.com/search?q={termo_codificado}&s={pag}"
            
            try:
                headers = self._get_headers()
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraindo resultados
                    for resultado in tqdm(soup.select('li')):
                        link_header_elem = resultado.select_one('a.ob')
                        title_elem = resultado.select_one('h2 a.title')
                        description_elem = resultado.select_one('p.s')
                        
                        if title_elem and link_header_elem:
                            link_header_text = link_header_elem['href']
                            title = title_elem.text.strip()
                            description = description_elem.text.strip() if description_elem else ""
                                                                                    
                            self.resultados.append({
                                'fonte': 'Mojeek',
                                'titulo': title,
                                'descricao': description,
                                'link': link_header_text,
                                'tipo': self._determinar_tipo_conteudo(title, description, link_header_text)
                            })
                    
                    # Pausa para evitar bloqueio
                    time.sleep(random.uniform(1, 3))
                    
            except Exception as e:
                print(f"Erro ao buscar no Mojeek: {e}")


    def buscar_qwant(self, termo_busca, max_paginas=1):
        """Busca resultados no Qwant (motor de busca europeu)"""
        print(f"Buscando '{termo_busca}' no Qwant...")
        termo_codificado = quote_plus(termo_busca)
        
        for pagina in range(1, max_paginas + 1):
            url = f"https://www.qwant.com/?t=web&q={termo_codificado}&freshness=week&p={pagina}"
            
            try:
                headers = self._get_headers()
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print(soup)
                    # Extraindo resultados
                    for resultado in tqdm(soup.select('div[data-testid="webResult"]')):
                        
                        # link do site
                        link_header_elem = resultado.select_one('a.external')
                        # titulo
                        title_elem = resultado.select_one('div._-0tQC span')
                        # descrição
                        description_elem = resultado.select_one('div._2KSc7 ')
                        
                        if title_elem and link_header_elem :
                            link = link_header_elem['href']
                            title = title_elem.text.strip()
                            description = description_elem.text.strip() if description_elem else ""
                            
                            self.resultados.append({
                                'fonte': 'Qwant',
                                'titulo': title,
                                'descricao': description,
                                'link': link,
                                'tipo': self._determinar_tipo_conteudo(title, description, link)
                            })
                    
                    # Pausa para evitar bloqueio
                    time.sleep(random.uniform(1, 3))
                    
            except Exception as e:
                print(f"Erro ao buscar no Qwant: {e}")

    # Verificado
    def buscar_yandex(self, termo_busca, max_paginas=1):
        """Busca resultados no Yandex"""
        print(f"Buscando '{termo_busca}' no Yandex...")
        termo_codificado = quote_plus(termo_busca)
        
        for pagina in range(0, max_paginas):
            url = f"https://yandex.com/search/?text={termo_codificado}&p={pagina}&lang=en"
            
            try:
                headers = self._get_headers()
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraindo resultados
                    for resultado in tqdm(soup.select('.serp-item')):
                        titulo_elem = resultado.select_one('h2 .OrganicTitleContentSpan')
                        link_elem = resultado.select_one('.OrganicTitle-Link')
                        descricao_elem = resultado.select_one('.OrganicTextContentSpan')
                        path_elem = resultado.select_one('.path__item')

                        if titulo_elem and link_elem :
                            titulo = titulo_elem.text.strip()

                             # Reconstrua a URL corretamente do Yandex
                            link = link_elem['href']
                                        
                            descricao = descricao_elem.text.strip() if descricao_elem else ""
                            
                            self.resultados.append({
                                'fonte': 'Yandex',
                                'titulo': titulo,
                                'descricao': descricao,
                                'link': link,
                                'tipo': self._determinar_tipo_conteudo(titulo, descricao, link)
                            })
                    
                    # Pausa para evitar bloqueio
                    time.sleep(random.uniform(2, 4))
                    
            except Exception as e:
                print(f"Erro ao buscar no Yandex: {e}")


    def buscar_startpage(self, termo_busca, max_paginas=1):
        """Busca resultados no Startpage (focado em privacidade)"""
        print(f"Buscando '{termo_busca}' no Startpage...")
        termo_codificado = quote_plus(termo_busca)
        
        for pagina in range(1, max_paginas + 1):
            url = f"https://www.startpage.com/sp/search?q={termo_codificado}&page={pagina}"
            
            try:
                headers = self._get_headers()
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraindo resultados
                    for resultado in tqdm(soup.select('.result')):
                        title_elem = resultado.select_one('.wgl-title')
                        link_elem = resultado.select_one('.wgl-display-url')
                        description_elem = resultado.select_one('.description')
                        
                        if title_elem and link_elem :
                            titulo = title_elem.text.strip()
                            link = link_elem['href']
                            descricao = description_elem.text.strip() if description_elem else ""
                            
                            self.resultados.append({
                                'fonte': 'Startpage',
                                'titulo': titulo,
                                'descricao': descricao,
                                'link': link,
                                'tipo': self._determinar_tipo_conteudo(titulo, descricao, link)
                            })
                    
                    # Pausa para evitar bloqueio
                    time.sleep(random.uniform(2, 4))
                    
            except Exception as e:
                print(f"Erro ao buscar no Startpage: {e}")

#endregion

#region "EXTRAS"
    def extrair_conteudo_pagina(self, url):
        """Extrai o conteúdo principal de uma página web"""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Removendo elementos não desejados
                for elem in soup(['script', 'style', 'nav', 'footer', 'header']):
                    elem.decompose()
                
                # Buscando o conteúdo principal
                # Primeiro tenta encontrar um elemento <article> ou <main>
                content = soup.select_one('article, main, .content, .article, #content')
                
                if not content:
                    # Se não encontrar, pega o body inteiro
                    content = soup.body
                
                if content:
                    text = content.get_text(separator=' ', strip=True)
                    # Limpando espaços extras e quebras de linha
                    text = re.sub(r'\s+', ' ', text).strip()
                    return text[:5000]  # Limitando a 5000 caracteres
                
            return "Não foi possível extrair o conteúdo."
        except Exception as e:
            return f"Erro ao extrair conteúdo: {e}"
    
    def _determinar_tipo_conteudo(self, titulo, descricao, link):
        """Determina o tipo de conteúdo com base em heurísticas simples"""
        link = link.lower()
        texto_completo = (titulo + " " + descricao).lower()
        
        # Verificando tipo por URL
        if any(x in link for x in ['/noticia', '/news', 'noticias', '/article', '/artigo']):
            return 'Notícia'
        elif any(x in link for x in ['youtube.com', 'vimeo.com', 'dailymotion', '/video']):
            return 'Vídeo'
        elif any(x in link for x in ['wikipedia.org', 'britannica.com', 'enciclopedia']):
            return 'Enciclopédia'
        elif any(x in link for x in ['github.com', 'stackoverflow.com', 'docs.']):
            return 'Documentação/Código'
        elif any(x in link for x in ['amazon', 'shop', 'store', 'produto', 'product']):
            return 'Comércio'
        elif any(x in link for x in ['blog', '/post']):
            return 'Blog'
        elif any(x in link for x in ['pdf', 'doc', 'docx', 'xls', 'xlsx']):
            return 'Documento'
        
        # Verificando por conteúdo
        if re.search(r'\b(notícia|news|última hora|breaking|jornal)\b', texto_completo):
            return 'Notícia'
        elif re.search(r'\b(artigo|article|publicação|paper|research)\b', texto_completo):
            return 'Artigo'
        elif re.search(r'\b(como fazer|how to|tutorial|aprenda|learn)\b', texto_completo):
            return 'Tutorial'
        elif re.search(r'\b(fórum|forum|pergunta|question|resposta|answer)\b', texto_completo):
            return 'Fórum/Q&A'
        
        # Padrão
        return 'Página Web'
    
    def filtrar_por_tipo(self, tipo):
        """Filtra os resultados por tipo de conteúdo"""
        return [r for r in self.resultados if r['tipo'].lower() == tipo.lower()]
    
    def filtrar_por_termo(self, termo):
        """Filtra os resultados que contêm um termo específico"""
        termo = termo.lower()
        return [r for r in self.resultados if 
                termo in r['titulo'].lower() or 
                termo in r['descricao'].lower()]
    
    def salvar_resultados(self, formato='csv'):
        """Salva os resultados em CSV ou Excel"""
        if not self.resultados:
            print("Nenhum resultado encontrado para salvar.")
            return
        
        df = pd.DataFrame(self.resultados)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato.lower() == 'csv':
            filename = f"busca_web_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        elif formato.lower() == 'excel':
            filename = f"busca_web_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
        else:
            print(f"Formato '{formato}' não suportado.")
            return
        
        print(f"Resultados salvos em {filename}")
        return filename
    
    def mostrar_resultados(self, n=20) -> str:
        """Retorna os primeiros n resultados como uma string formatada"""
        if not self.resultados:
            return "Nenhum resultado encontrado."
        
        resultados_formatados = []
        for i, res in enumerate(self.resultados[:n], 1):
            descricao = f"{res['descricao'][:100]}..." if len(res['descricao']) > 100 else res['descricao']
            resultado = f"{i}. {res['titulo']} [{res['fonte']} | {res['tipo']}]\n   {descricao}\n   Link: {res['link']}"
            resultados_formatados.append(resultado)
        
        cabecalho = f"Resultados encontrados: {len(self.resultados)}.\nExibindo {min(n, len(self.resultados))} de {len(self.resultados)} resultados:\n"
        return cabecalho + "\n\n".join(resultados_formatados)

#endregion