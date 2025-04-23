# O que é o Protocolo de Contexto de Modelo (MCP)?

O Protocolo de Contexto de Modelo (MCP) é um padrão aberto desenvolvido pela Anthropic para facilitar a integração simples e padronizada entre modelos de IA e ferramentas externas. Funciona como um conector universal, permitindo que grandes modelos de linguagem (LLMs) interajam dinamicamente com APIs, bases de dados e aplicações comerciais.

---

## Arquitetura do MCP

### Hosts
A aplicação orientada para o utilizador (por exemplo, Claude Desktop, IDEs como Cursor/VsCode/Trae, ou agentes personalizados) que inicia as conexões.
Os Hosts integram Clientes MCP para comunicar com servidores.

### Cliente
Estabelece uma conexão 1:1 com um Servidor MCP, tratando pedidos, respostas e descoberta de capacidades.
Traduz instruções geradas por LLM em mensagens compatíveis com MCP.

### Servidor
Expõe ferramentas (por exemplo, chamadas de API, consultas de base de dados), recursos (dados apenas de leitura) e prompts (modelos predefinidos) através do protocolo MCP.
Executa localmente ou remotamente, conectando-se a sistemas como GitHub, Slack, PostgreSQL ou ficheiros locais.

---

## O que é necessário para criar um Servidor MCP?

- Python 
    ```
    https://github.com/modelcontextprotocol/python-sdk
    ```
- Node
    ```
    https://github.com/modelcontextprotocol/typescript-sdk
    ```
- C#
    ```
    https://github.com/modelcontextprotocol/csharp-sdk
    ```

- Java
    ```
    https://github.com/modelcontextprotocol/java-sdk
    ```
- Kotlin
    ```
    https://github.com/modelcontextprotocol/kotlin-sdk
    ```

### Python 

- Verificar a versão: necessita da versão 3.11 ou superior
    ```bash
    python --version
    ```
- Gestor de Pacotes, UV 
    - O UV (e a sua extensão UVX) é um gestor de pacotes Python extremamente rápido, até 10x mais rápido que pip e Poetry, o que é crítico para servidores MCP que dependem de ambientes Python atualizados e livres de conflitos.
    - O UVX é usado como um "executor universal" para servidores MCP, simplificando comandos.
    - macOS ou Linux 
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    - Windows
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    - Atualização 
    ```bash
    uv self update
    ```

### Projeto em Python

    ```bash
    mkdir mcp_exemple
    cd mcp_exemple
    uv init
    ```

```.
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

    ```bash
    uv run mojeek.py
  ```

### Projeto em Node.js

- Verificar a versão: necessita do Node.js 14 ou superior
    ```bash
    node --version
    ```
- projecto
    ```bash
        mkdir meu-projeto && cd meu-projeto
    ```
- Inicia o projeto com npm:
    ```bash
    npm init -y
    ```
- Instalação do SDK
    ```bash
    npm install @modelcontextprotocol/mcp-sdk
    ```
- Comandos para iniciar o servidor
    - Crie um arquivo `server.js` com o seguinte conteúdo:
    ```javascript
    const MCP = require('@modelcontextprotocol/mcp-sdk');
    const server = new MCP.Server();

    server.start().then(() => {
        console.log('Servidor MCP rodando em http://localhost:3000');
    }).catch(err => {
        console.error('Erro ao iniciar o Servidor MCP', err);
    });
    ```
    - Execute o servidor
    ```bash
    node server.js
    ```

