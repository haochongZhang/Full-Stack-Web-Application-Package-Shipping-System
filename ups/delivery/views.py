from django.shortcuts import render, redirect
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

@login_required
def overviewShipment(request):
    if request.user.is_authenticated():
        # get all related shipment of the user
        shipments = request.user.shipment_set.all()
        return render(request, "delivery/overviewShipment.html", {"shipments":shipments})
    else:
        return redirect("Login")

@login_required
def detailShipment(request, pk):
    if request.method == "POST":
        if request.POST["xAddr"] and request.POST["yAddr"]:
            shipment = Shipment.objects.get(shipment_id=pk)
            shipment.dest_addr_x = request.POST["xAddr"]
            shipment.dest_addr_y = request.POST["yAddr"]
            #shipment.save()
            return redirect("delivery/overviewShipment")
    else:
        if Shipment.objects.filter(shipment_id=pk).exists() and request.user.is_authenticated():
            shipment = Shipment.objects.get(shipment_id=pk)
            item_set = shipment.item_set.all()
            return render(request, "delivery/detailShipment.html", {"shipment":shipment, "item_set":item_set})
        else:
            return redirect("accounts/Login")
