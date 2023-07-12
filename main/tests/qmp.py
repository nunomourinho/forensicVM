import asyncio
from qemu.qmp import QMPClient


async def main():
    print("hello")
    qmp = QMPClient('forensicVM')
    socket_path = "/forensicVM/mnt/vm/8741c214-8956-573a-a6e7-c28d86684f05/run/qmp.sock"
    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('query-status')
        print(f"VM status: {res['status']}")
        status = {res['status']}
    except Exception as e:
        print(e)
    res = await qmp.execute('quit')

async def run_qmp():
    qmp = QMPClient('forensicVM')
    socket_path = "/forensicVM/mnt/vm/9cf39b70-1e7a-5e78-a8ee-fa0ea3b90a7f/run/qmp.sock"
    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('query-status')
        print(res)
        print(f"VM status: {res['status']}")
        status = res['status']
        # Create snapshot
        snapshot_name = "my_snapshot3"
        res = await qmp.execute("human-monitor-command", {
            "command-line": f"savevm {snapshot_name}"
        })
        #res = await qmp.execute('snapshot-create', {'name': snapshot_name})
        print(f"Snapshot '{snapshot_name}' created.")
        print(res)

        #res = await qmp.execute('quit')
    except Exception as e:
        print(e)


#async def run_qmp():
#    print("I am here")
#    qmp = QMPClient('forensicVM')
#    socket_path = "/forensicVM/mnt/vm/9cf39b70-1e7a-5e78-a8ee-fa0ea3b90a7f/run/qmp.sock2"
#    try:
#        print("Trying to connect")
#        qmp.connect(socket_path)
#        res = await qmp.execute('query-status')
#        print(res)
#        print(f"VM status: {res['status']}")
#        status = {res['status']}
#    except Exception as e:
#        print(e)
##   Destroy vm
##    res = qmp.execute('quit')
#    res = await qmp.execute('system_powerdown')
#
## Tested: Memory dump: OK
##    res = await qmp.execute('dump-guest-memory', { "paging": False, "protocol": "file:/forensicVM/main/django-app/app/memoria.dmp", "detach": True})
#
## Tested: Screendump: OK
##    res = await qmp.execute('screendump', {"filename": "/forensicVM/main/django-app/app/photo.png" })
#
## Tested: system_reset: OK
##    res = await qmp.execute('system_reset')
#    print(res)
##    if status == {'suspended'}:
##        res = await qmp.execute('quit')
##        print(res)
##    await qmp.disconnect()
#
##await run_qmp()
asyncio.run(run_qmp())
