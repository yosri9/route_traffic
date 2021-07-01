import json
import xml
from xml import etree

from django.shortcuts import render
from math import radians, cos, sin, asin, sqrt

from django.http import HttpResponse
from folium.plugins import FloatImage
from pyroutelib3 import Router, router
import folium
from requests import Response
from rest_framework.decorators import api_view

from polls.models import Data, AverageData, AverageDataPerSegment

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

renderer_classes = [JSONRenderer]


def index(request):
    latest_question_list = Data.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


# def averageData(request):
#     average_data_list =Data.objects.order_by('altitude' , 'longitude')
#     dataSet = set()
#     for data in average_data_list:
#         dataSet.add((data.altitude,data.longitude))
#
#     context={'average_data_list': average_data_list, 'dataSet':dataSet}
#     return render(request,'polls/averagedata.html',context)


def distance(lat1, lat2, lon1, lon2):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        return (c * r) * 1000
def drawMap(c,first_node_coord ,next_node_coord):

    folium.Marker(first_node_coord).add_to(c)
    folium.Marker(next_node_coord).add_to(c)

    c.save('maCarte.html')

def averageData(request):

        datas = Data.objects.order_by('id')
        roads = {}
        first_node = 0
        next_node = 0
        # speed for specific road from the first_node to the next_node
        speed = []
        router = Router("car")
        c = folium.Map(location=[46.078025, 6.409053], zoom_start=10)
        pointIteration=0
        try:
            for data in datas:
                pointIteration+=1

                # the nearest node(way intersection) for this point coordination(altitude , longitude)
                try:

                    data_node = router.findNode(data.altitude, data.longitude)
                except Exception:
                    pass

                # vehicule begin his way
                if first_node == 0:
                    first_node = data_node
                # we are in the same road
                if data_node == first_node:
                    if data.speed != "NULL":
                        speed.append(int(data.speed))
                # we are in the end of the road
                if data_node != first_node:
                    next_node = data_node

                    first_node_coord = router.nodeLatLon(first_node)
                    next_node_coord = router.nodeLatLon(next_node)

                    distanceBetweenEndNodeAndPoint = distance(data.altitude,next_node_coord[0] , data.longitude,next_node_coord[1])


                    length = distance(first_node_coord[0], next_node_coord[0], first_node_coord[1], next_node_coord[1])

                    if data.speed != "NULL":
                        speed.append(int(data.speed))

                        # it is impossible to drive 1km to find a node
                        if length < 1000:

                            # if the driver reach a point that has distance < 10 meter to end_node of the road that's mean
                            # the vehicule approximately finish the road and enter in the next road
                            if float(distanceBetweenEndNodeAndPoint) < 10  and float(data.speed) > 2.5 :
                                road = first_node_coord,next_node_coord
                                # Now we can calculate the average speed of the road
                                averageSpeed = sum(speed) / len(speed)

                                # add averageData to database
                                averageData = AverageData()
                                averageData.first_node_altitude = first_node_coord[0]
                                averageData.first_node_longitude = first_node_coord[1]
                                averageData.end_node_altitude = next_node_coord[0]
                                averageData.end_node_longitude = next_node_coord[1]
                                averageData.distance_between_end_node_and_point = distanceBetweenEndNodeAndPoint
                                averageData.road_length = length
                                averageData.averageSpeed = averageSpeed
                                averageData.save_base()

                                # -------------------------------------
                                roads[str(road)] = {"speed" : averageSpeed , "length": length , "count" : pointIteration ,"distanceBetweenEndNodeAndPoint" : distanceBetweenEndNodeAndPoint}
                                drawMap(c, first_node_coord, next_node_coord)
                                pointIteration = 0

                                # Now we go to the next road of the vehicule and we know that the end_node of the last road is the first_node of the new road
                                speed.clear()
                                first_node = next_node





                        else:


                            speed.clear()
                            first_node = next_node
        except NameError:
            print(NameError)
        finally:
            print(NameError)



        averageDataPerSegment()
        context = {'speed': speed , "roads":roads}

        dump = json.dumps(context)
        return HttpResponse(dump, content_type='application/json')

def averageDataPerSegment():
    cart = folium.Map(location=[34.72289696, 10.71833154], zoom_start=10)

    speedRoadMap = {}
    datas = AverageData.objects.order_by("id")
    print(datas)

    for data in datas:

      node = [data.first_node_altitude, data.first_node_longitude,
                      data.end_node_altitude, data.end_node_longitude]
      node = json.dumps(node)
      speedRoadMap[node] = 0
    for data in datas:
        node = [data.first_node_altitude, data.first_node_longitude,
                data.end_node_altitude, data.end_node_longitude]

        speedRoadMap[json.dumps(node)] = float(data.averageSpeed) + speedRoadMap[str(node)]
    print(speedRoadMap)
    for segment in speedRoadMap:
        nodes = json.loads(segment)
        print(nodes)
        averageDataPerSegment = AverageDataPerSegment()
        averageDataPerSegment.first_node_altitude = nodes[0]
        averageDataPerSegment.first_node_longitude = nodes[1]
        averageDataPerSegment.end_node_altitude = nodes[2]
        averageDataPerSegment.end_node_longitude = nodes[3]

        count =AverageData.objects.all().filter(first_node_altitude=nodes[0],first_node_longitude=nodes[1],end_node_altitude=nodes[2]
                          ,end_node_longitude=nodes[3]).count()

        print(count)
        if count != 0 :
            averageSpeed = speedRoadMap[segment] / count
            averageDataPerSegment.averageSpeed =  averageSpeed
            averageDataPerSegment.counted_value = count

            if averageSpeed <= 15 :
                color = "Red"
            if averageSpeed > 15 and averageSpeed <= 30:
                color = "orange"
            if averageSpeed > 30 and averageSpeed <= 50:
                color = "yellow"
            if averageSpeed > 50 and averageSpeed <= 90:
                color = "B6C867"
            if averageSpeed > 90:
                color = "green"
            drawPaths(cart=cart, first_node_altitude=nodes[0],first_node_longitude=nodes[1],end_node_altitude=nodes[2]
                          ,end_node_longitude=nodes[3], color=color)

            averageDataPerSegment.save()

    url = (
        "speedColor.jpg"
    )

    FloatImage(url, bottom=80, left=80).add_to(cart)

    cart.save('maCarte.html')

def drawPaths(cart ,first_node_altitude, first_node_longitude, end_node_altitude, end_node_longitude , color ):
    router = Router("car" )
    start = router.findNode(first_node_altitude, first_node_longitude)
    end = router.findNode(end_node_altitude, end_node_longitude)
    status, route = router.doRoute(start, end)
    if status == 'success':
        routeLatLons = list(map(router.nodeLatLon, route))



    folium.vector_layers.PolyLine(routeLatLons, popup=None, tooltip=None, color = color).add_to(cart)































