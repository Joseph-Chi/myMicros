from fastapi import FastAPI, Response
import matplotlib.pyplot as plt
import math
from io import BytesIO

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/taiwan_stock_price")
def taiwan_stock_price():
    print("get data from mysql")
    return {"data": 123}

@app.get("/CollatzChart")
def CollatzChart (
    chartType: str='',
    fN: str='',

    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response,
    ):
    def f(x):
        if x==1 : return 0
        mod = math.remainder(x,2)
        result = f(x/2)+1 if mod == 0 else f(3*x+1)+1
        return result

    def g(x):
        if x==1 : return 0
        return g(x-1)+f(x)

    try:
        fn=int(fN)
    except:
        fn=100


    fn= fn if fn > 0 else 100    
    fig,ax = plt.subplots(dpi=200)
    x=range(1,fn,1)
    y=[f(i) for i in x]

    plt.plot(x,y,'r.')
    plt.show()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # media_type here sets the media type of the actual response sent to the client.
    return Response(content= image_png, media_type="image/png")



