from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import *

from .models import Ticket
from .serializers import *
from .permissions import IsAuthenticateAndNotStaff


class TicketList(APIView):
	"""Вывод тикетов(тикета) в зависимости от того, какой пользователь"""

	def get(self, request, pk=None):
		if pk:
			try:
				ticket = Ticket.objects.get(pk=pk)
			except:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			serializer = TicketDetailSerializer(ticket)
			return Response(serializer.data)
		# Вывод тикетов для админа (все тикеты)
		if request.user.is_authenticated and request.user.is_staff:
			tickets = Ticket.objects.all()
			serializer = TicketListSerializers(tickets, many=True)
			return Response(serializer.data)
		# Вывод тикетов для пользователя(только его тикеты)
		elif request.user.is_authenticated:
			tickets = Ticket.objects.filter(user=request.user)
			serializer = TicketListSerializers(tickets, many=True)
			return Response(serializer.data)
		else:
			return Response({})


class AddTicket(generics.CreateAPIView):
	"""Добавление тикета, добавлять может любой пользователь, за исключением админа"""
	serializer_class = TicketCreateSerializer
	permission_classes = (IsAuthenticateAndNotStaff,)


class MessageCreateView(generics.CreateAPIView):
	"""Создание сообщений для тикетов"""
	serializer_class = MessageCreateSerializer
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		message = MessageCreateSerializer(data=request.data)
		if message.is_valid():
			message.save()
		return Response(status=201)


class ChangeStatusTicket(generics.RetrieveUpdateDestroyAPIView):
	"""Изменение статусов тикетов или удаление"""
	serializer_class = TicketChangeStatusSerializer
	permission_classes = (IsAdminUser,)
	queryset = Ticket.objects.all()
