"""Servidor Modbus TCP assíncrono (127.0.0.1:5020)."""
import asyncio
import logging

from pymodbus.server import StartAsyncTcpServer
from pymodbus.simulator import DataType, SimData, SimDevice

logging.basicConfig(level=logging.INFO)


async def run_server() -> None:
    # Blocos separados: cada área do Modbus tem sua própria memória.
    # Ordem da tupla: (coils, discrete inputs, holding registers, input registers)
    # Coils/discrete usam endereço de bit (coil 1 é o bit 1, não o registrador 1).
    coils = [SimData(0, count=100, values=False, datatype=DataType.BITS)]
    discrete_inputs = [SimData(0, count=100, values=False, datatype=DataType.BITS)]
    holding = [SimData(0, count=100, values=list(range(100)), datatype=DataType.REGISTERS)]
    inputs = [SimData(0, count=100, values=list(range(100)), datatype=DataType.REGISTERS)]
    device = SimDevice(1, simdata=(coils, discrete_inputs, holding, inputs))
    print("Servidor Modbus em 127.0.0.1:5020 (Ctrl+C para parar)")
    await StartAsyncTcpServer(context=device, address=("127.0.0.1", 5020))


def main() -> None:
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Servidor encerrado")


if __name__ == "__main__":
    main()
