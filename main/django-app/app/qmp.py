import asyncio
from qemu.qmp import QMPClient


async def main():
    qmp = QMPClient('forensicVM')
    socket_path = "/forensicVM/mnt/vm/9b309b16-ad74-5d86-9879-273873a795c1/run/qmp.sock"
    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('query-status')
        print(f"VM status: {res['status']}")
        status = {res['status']}
    except Exception as e:
        print(e)
#   Destroy vm
    res = await qmp.execute('quit')
#    res = await qmp.execute('system_powerdown')

# Tested: Memory dump: OK
#    res = await qmp.execute('dump-guest-memory', { "paging": False, "protocol": "file:/forensicVM/main/django-app/app/memoria.dmp", "detach": True})

# Tested: Screendump: OK
#    res = await qmp.execute('screendump', {"filename": "/forensicVM/main/django-app/app/photo.png" })

# Tested: system_reset: OK
#    res = await qmp.execute('system_reset')
    print(res)
#    if status == {'suspended'}:
#        res = await qmp.execute('quit')
#        print(res)
#    await qmp.disconnect()

asyncio.run(main())
