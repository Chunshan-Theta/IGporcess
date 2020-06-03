import psutil

ram = dict(psutil.virtual_memory()._asdict())
hdd = psutil.disk_usage('/')

def get_server_usage_status():
    show_list = list()
    show_list.append(("hdd Total", hdd.total))
    show_list.append(("hdd Used", hdd.used))
    show_list.append(("hdd Free", hdd.free))
    show_list.append(("hdd Used(%)", f"{int(round(hdd.free/hdd.total, 2)*100)}"))
    show_list.append(("ram Total", ram['total']))
    show_list.append(("ram Used", ram['total']-ram['available']))
    show_list.append(("ram Free", ram['available']))
    show_list.append(("ram Used(%)", ram['percent']))
    show_list.append(("cpu Used(%)", float(psutil.cpu_percent(interval=1, percpu=False))))

    for (text, value) in show_list:

        print(f"{text}: {value}")


get_server_usage_status()