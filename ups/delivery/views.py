from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Shipment, Item


# Create your views here.
def home(request):
    if request.method == "POST":
        # check the existence of shipment via tracking number
        if request.POST["s_id"]:
            shipmentid = request.POST["s_id"]
            if Shipment.objects.filter(shipment_id=shipmentid).exists():
                shipment = Shipment.objects.get(shipment_id=shipmentid)
                item_set = set(shipment.item_set.all())
                # show the required shipment status
                return render(request, "delivery/shipmentDetail.html", {"shipment":shipment, "item_set":item_set})
            else:
                return render(request, "delivery/home.html", {"error":"Unable to find the required shipment"})
        else:
            return render(request, "delivery/home.html", {"error":"Please enter valid tracking number"})

    else:
        return render(request, "delivery/home.html")

def searchShipment(request):
    if request.method == "POST":
        return render(request, "delivery/home.html")
    else:
        return render(request, "delivery/shipmentDetail.html")
