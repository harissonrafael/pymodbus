"""Cliente Modbus TCP assíncrono simples."""
import asyncio

from pymodbus.client import AsyncModbusTcpClient

DEVICE_ID = 1

async def run_client() -> None:
    client = AsyncModbusTcpClient("127.0.0.1", port=5020)
    await client.connect()
    if not client.connected:
        print("Não foi possível conectar. O servidor está rodando?")
        return

    try:
        wr = await client.write_register(4, 1234, device_id=DEVICE_ID)
        if wr.isError():
            print("Erro ao escrever registrador:", wr)

        rr = await client.read_holding_registers(0, count=5, device_id=DEVICE_ID)
        if rr.isError():
            print("Erro ao ler holding registers:", rr)
        else:
            print("Holding registers 0-4:", rr.registers)

        wc = await client.write_coil(0, True, device_id=DEVICE_ID)
        if wc.isError():
            print("Erro ao escrever coil 0:", wc)

        rc = await client.read_coils(0, count=3, device_id=DEVICE_ID)
        if rc.isError():
            print("Erro ao ler coils:", rc)
        else:
            print("Coils 0-2:", rc.bits[:3])
    finally:
        # Roda sempre: com sucesso, com return ou com exceção
        client.close()


def main() -> None:
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
