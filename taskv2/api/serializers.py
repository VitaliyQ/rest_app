from .models import *
from rest_framework import serializers


class MessageListSerializer(serializers.ModelSerializer):
	"""Список сообщений"""
	user = serializers.SlugRelatedField(slug_field='username', read_only=True)

	class Meta:
		model = Message
		exclude = ('ticket',)


class TicketDetailSerializer(serializers.ModelSerializer):
	"""Детальная информация по тикету"""
	messages = MessageListSerializer(many=True)
	user = serializers.SlugRelatedField(slug_field='username', read_only=True)
	status = serializers.SlugRelatedField(slug_field='status', read_only=True)

	class Meta:
		model = Ticket
		fields = '__all__'


class TicketListSerializers(serializers.ModelSerializer):
	"""Список всех тикетов"""
	status = serializers.SlugRelatedField(slug_field='status', read_only=True)
	user = serializers.SlugRelatedField(slug_field='username', read_only=True)

	class Meta:
		model = Ticket
		fields = ('id', 'title', 'time_update', 'status', 'user')


class TicketCreateSerializer(serializers.ModelSerializer):
	"""Создание нового тикета"""
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	class Meta:
		model = Ticket
		fields = '__all__'


class TicketChangeStatusSerializer(serializers.ModelSerializer):
	"""Изменение статуса тикета"""
	class Meta:
		model = Ticket
		fields = ('status',)


class MessageCreateSerializer(serializers.ModelSerializer):
	"""Создание сообщений для тикетов"""
	ticket = serializers.ChoiceField(choices=Ticket.objects.all())

	class Meta:
		model = Message
		fields = '__all__'
