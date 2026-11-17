# Comandos de linha de comando do asyncua

Ferramentas que o `asyncua` instala em `.venv\Scripts`. Servem para explorar
o servidor OPC UA sem escrever código Python.

## Preparação

Terminal 1, servidor:

```bash
uv run opcua_server
```

Terminal 2, variáveis de apoio (Git Bash):

```bash
U=opc.tcp://localhost:4840/freeopcua/server/
```

No PowerShell:

```powershell
$U = "opc.tcp://localhost:4840/freeopcua/server/"
```

Opções comuns a todas as ferramentas:

| Opção | Significado |
|---|---|
| `-u` | URL do endpoint do servidor |
| `-p` | Caminho do nó, separado por vírgula (`ns:Nome,ns:Nome`) |
| `-n` | Nó pelo NodeId (ex.: `ns=2;i=3`), alternativa ao `-p` |
| `-i` | Índice de namespace usado no `-p` |
| `-t` | Tipo do valor (no `uawrite`) |
| `-h` | Ajuda da ferramenta |

O `2:` nos caminhos é o índice do namespace
`http://examples.freeopcua.github.io`, registrado pelo servidor.
O `0:` é o namespace do padrão OPC UA.

## Comandos testados

### Navegar a árvore (`uals`)

```bash
uv run uals -u $U -p "0:Objects" -d 2
```

`-d` é a profundidade. Mostra `MyObject`, `MyVariable`, `Temperatura`
e `ServerMethod`.

### Ler um valor (`uaread`)

```bash
uv run uaread -u $U -p "0:Objects,2:MyObject,2:Temperatura"
```

Resultado esperado: o valor atual (ex.: `27.5`).

### Escrever em variável somente leitura (`uawrite`)

```bash
uv run uawrite -u $U -p "0:Objects,2:MyObject,2:Temperatura" -t float 1.0
```

Resultado esperado: `BadUserAccessDenied`, porque a `Temperatura` não tem
`set_writable()` no servidor.

### Escrever em variável gravável (`uawrite`)

```bash
uv run uawrite -u $U -p "0:Objects,2:MyObject,2:MyVariable" -t float 100.0
```

Resultado obtido: `BadTypeMismatch`. A `MyVariable` foi criada com `6.7`,
que o asyncua guarda como `Double`, e `-t float` envia outro tipo.
Provavelmente `-t double` resolve, mas **ainda não foi testado**.

## Ferramentas disponíveis, ainda não exercitadas

| Ferramenta | Para que serve |
|---|---|
| `uasubscribe` | Subscrição a um nó, equivalente ao `TempHandler` do cliente |
| `uacall` | Chama um método (ex.: `ServerMethod` com `5`, deve voltar `10`) |
| `uabrowse` | Mesmo programa que o `uals` (alias) |
| `uadiscover` | Descobre servidores e endpoints |
| `uahistoryread` | Lê histórico de um nó |
| `uaclient` | Cliente interativo |
| `uaserver` | Sobe um servidor de teste pronto |
| `uageneratestructs` | Gera código Python para tipos estruturados |

Use `uv run <ferramenta> --help` para ver os argumentos de cada uma.

## Atenção

- `python -m asyncua.tools.uals` **não funciona**. `asyncua.tools` é um
  arquivo, não um pacote. Use o comando direto: `uv run uals`.
- Se o servidor não subir (erro `10048`, porta em uso), há outro servidor
  rodando na porta 4840. Encerre-o antes de iniciar de novo.
