import asyncio
from qemu.qmp import QMPClient


#async def main():
#    qmp = QMPClient('forensicVM')
#    socket_path = "/forensicVM/mnt/vm/8741c214-8956-573a-a6e7-c28d86684f05/run/qmp.sock"
#    try:
#        await qmp.connect(socket_path)
#        res = await qmp.execute('query-status')
#        print(f"VM status: {res['status']}")
#        status = {res['status']}
#    except Exception as e:
#        print(e)
#   Destroy vm
#    res = await qmp.execute('quit')

def run_qmp():
    qmp = QMPClient('forensicVM')
    socket_path = "/forensicVM/mnt/vm/8741c214-8956-573a-a6e7-c28d86684f05/run/qmp.sock"
    try:
        qmp.connect(socket_path)
        res = qmp.execute('query-status')
        print(f"VM status: {res['status']}")
        status = {res['status']}
    except Exception as e:
        print(e)
#   Destroy vm
    res = qmp.execute('quit')
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

run_qmp()
