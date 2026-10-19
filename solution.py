import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

load_dotenv(".env")

s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)
print(res.text)

codigo_linha = 558

res = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}"
)
paradas = res.json()

pos = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo_linha}"
)
onibus = pos.json()["vs"]

m = Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=13)

for i in paradas:
    Marker(
        location=[i["py"], i["px"]],
        popup=i["np"],
        icon=Icon(color="blue"),
    ).add_to(m)

for i in onibus:
    Marker(
        location=[i["py"], i["px"]],
        popup=f"Ônibus {i['p']}",
        icon=Icon(color="red", icon="bus", prefix="fa"),
    ).add_to(m)

m.save("mapa.html")
