# pymodbus

Estudos de Python com `asyncio`, usando os protocolos Modbus TCP
([pymodbus](https://github.com/pymodbus-dev/pymodbus)) e OPC UA
([asyncua](https://github.com/FreeOpcUa/opcua-asyncio)).

## Requisitos

- Python 3.15 ou mais novo
- [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

## Exemplos

Cada exemplo tem um servidor e um cliente. Rode o servidor em um terminal e o
cliente em outro.

### Modbus TCP

```bash
uv run server_async          # servidor em 127.0.0.1:5020 (Ctrl+C para parar)
uv run simple_async_client   # lê e escreve registradores e coils
```

### OPC UA

```bash
uv run opcua_server          # servidor em opc.tcp://0.0.0.0:4840/freeopcua/server/
uv run opcua_client          # lê, escreve, chama método e assina mudanças (Ctrl+C para sair)
```

Para explorar o servidor OPC UA sem escrever código, veja
[opcua-comandos.md](opcua-comandos.md): comandos de linha de comando do
asyncua (`uals`, `uaread`, `uawrite` e outros), com os resultados dos testes.

## Estrutura

```
src/examples/
├── server_async.py            # servidor Modbus TCP
├── simple_async_client.py     # cliente Modbus TCP
├── opcua_server_minimal.py    # servidor OPC UA
└── opcua_client_minimal.py    # cliente OPC UA
```
