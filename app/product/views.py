from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from django.http import HttpResponse
import json

@api_view(['POST'])
def setSiteProductOrder(request):
	try:
		indx = [int(i) for i in request.DATA.get('order').split(',')]

		proList = dict([(pro.pk, pro) for pro in Product.objects.filter(pk__in=indx)])

		for idx, proId in enumerate(indx):
			pro = proList.get(proId)
			pro.order = idx
			pro.save()
		response = HttpResponse(json.dumps({'message': 'order update success'}), content_type="application/json")
		response.status_code = 202
		return response
	except :
		response = HttpResponse(json.dumps({'message': 'order update failure'}), content_type="application/json")
		response.status_code = 406
		return response

'''
	input json data: {'productId' : proId, 'photoId' : photoId}
'''
@api_view(['POST'])
def setDefaultProductPhoto(request):
	try:
		data = json.dumps(request.DATA)
		product = Product.objects.get(pk=data['productId'])
		photo = Photo.objects.get(pk=data['photoId'])
		product.thumbPhoto = photo.thumbPhoto
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
	except :
		return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)





