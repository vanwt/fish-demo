from fish.application.app import Fish
from fish.response import Text
from psutil import cpu_percent, cpu_count

app = Fish()


@app.get("/index")
def index(req):
    return Text("CpuPre:{0}  CpuPres:{1}  CpuCount:{2}".format(cpu_percent(interval=0, percpu=False),
        cpu_percent(interval=0, percpu=True),
        cpu_count(logical=False)
    ))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
