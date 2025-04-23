# O que é o protocolo de contexto de modelo (MCP)?

O protocolo de contexto de modelo (MCP) é um padrão aberto desenvolvido pela Anthropic para permitir a integração fácil e padronizada entre modelos de IA e ferramentas externas. Ele atua como um conector universal, permitindo que grandes modelos de linguagem (LLMs) interajam dinamicamente com APIs, bases de dados e aplicações comerciais.

---

## Arquitetura do MCP

### Hosts
A aplicação voltada para o utilizador (por exemplo, Claude Desktop, IDEs como Cursor/VsCode/Trae, ou agentes personalizados) que inicia as conexões.
Os Hosts integram Clientes MCP para comunicar com servidores.

### Cliente
Gere uma conexão 1:1 com um Servidor MCP, tratando pedidos, respostas e descoberta de capacidades.
Traduz instruções geradas por LLM em mensagens compatíveis com MCP.

### Servidor
Expõe ferramentas (por exemplo, chamadas de API, consultas de base de dados), recursos (dados somente leitura) e prompts (modelos predefinidos) através do protocolo MCP.
Executa localmente ou remotamente, conectando-se a sistemas como GitHub, Slack, PostgreSQL ou ficheiros locais.

---

## O que é necessário para fazer um Servidor MCP?

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

- Verificar a versão é necessario +3.11 
    ```bash
    python --version
    ```
- Gerenciador de Pacotes , UV 
    - UV (e sua extensão UVX) é um gerenciador de pacotes Python extremamente rápido, até 10x mais rápido que pip e Poetry, o que é crítico para servidores MCP que dependem de ambientes Python atualizados e livres de conflitos.
    - UVX é usado como um "executor universal" para servidores MCP, simplificando comandos.
    - macOS ou Linux 
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    - Windows
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    - Upgrade 
    ```bash
    uv self update
    ```

### Projecto Python

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
    - Will create a virtual environment and install the dependencies
    - Will run the main.py file


