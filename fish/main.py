from app import Fish


app = Fish()

@app.get("/")
def index(req):
    return "Hello"



