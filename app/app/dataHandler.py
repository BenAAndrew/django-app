from .tools import *

progress = ['draft', 'submitted', 'processing', 'approved']

def progressToProgressPercent(application):
    state = application["progress"]
    if state == 'declined':
        return 5
    else:
        return (progress.index(state)+1) * 25

def getApplications(request):
    applications = decode_request(requests.get("http://127.0.0.1:8001/applications/", cookies=request.COOKIES))
    for i in range(0, len(applications)):
        applications[i]["progress_percent"] = progressToProgressPercent(applications[i])
        applications[i]["progress"] = applications[i]["progress"].capitalize()
    return applications

def getGoods():
    return jsonToDict('http://127.0.0.1:8001/goods/')

def getGoodsSelected(ids):
    allGoods = getGoods()
    for i in range(0, len(allGoods)):
        allGoods[i]["selected"] = allGoods[i]["id"] in ids
    return allGoods

def getApplication(id):
    application = jsonToDict('http://127.0.0.1:8001/applications/'+str(id)+"/")
    application["goods"] = getGoodsNames(application["goods"])
    application["goods"] = getGoodsSelected([good["id"] for good in application["goods"]])
    return application

def getGood(id):
    return jsonToDict('http://127.0.0.1:8001/goods/'+str(id)+"/")

def getGoodsNames(ids):
    goods = list()
    for id in ids:
        goods.append({ "id": int(id), "name" : getGood(int(id))["name"]})
    return goods

def getMessage(request):
    message = request.session["message"]
    request.session["message"] = None
    return message