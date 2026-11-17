import asyncio

from asyncua import Client, ua

url = "opc.tcp://localhost:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"


async def main():
    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(f"0:Objects/{nsidx}:MyObject/{nsidx}:MyVariable")
        value = await var.read_value()
        print(f"Value of MyVariable ({var}): {value}")

        new_value = value - 50
        print(f"Setting value of MyVariable to {new_value} ...")
        await var.write_value(new_value)

        # Variável somente leitura: ler funciona, escrever é recusado pelo servidor
        temp = await client.nodes.root.get_child(f"0:Objects/{nsidx}:MyObject/{nsidx}:Temperatura")
        print(f"Temperatura atual: {await temp.read_value()}")
        try:
            await temp.write_value(99.0)
            print("Escrita na Temperatura foi aceita (inesperado!)")
        except ua.UaStatusCodeError as e:
            print(f"Escrita na Temperatura recusada pelo servidor: {e}")

        # Calling a method
        res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)
        print(f"Calling ServerMethod returned {res}")

        # Subscrição: o servidor AVISA quando a Temperatura ou MyVariable muda (sem polling)
        handler = TempHandler()
        sub = await client.create_subscription(2000, handler)  # 2000 ms
        handles = await sub.subscribe_data_change([temp, var])
        print("Aguardando mudanças de Temperatura e MyVariable (Ctrl+C para sair)...")
        try:
            while True:
                await asyncio.sleep(1)
        finally:
            # Roda no Ctrl+C também: limpa a subscrição antes de fechar a conexão
            await sub.unsubscribe(handles)
            await sub.delete()


class TempHandler:
    """Recebe as notificações da subscrição.

    O asyncua chama este método sozinho a cada mudança do(s) valor(es).
    """

    def datachange_notification(self, node, val, data):
        print(f"[notificação][{data.monitored_item.Value.SourceTimestamp}]: {node} mudou para {val}")


def cli() -> None:
    """Ponto de entrada síncrono (usado pelo script do pyproject)."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Cliente encerrado")


if __name__ == "__main__":
    cli()