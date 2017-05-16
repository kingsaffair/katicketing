{% extends "old_checkin/main.tpl" %}
{% load static %}
{% block head %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
	<script type="text/javascript">mode = 1; ignore = {% if separate %}1{% else %}0{% endif %};</script>
	<script type="text/javascript" src="{% static 'legacy/checkin/js/tickets.js' %}"></script>
{% endblock %}
{% block body %}
<form method="post" action="" class="tickets">
{% csrf_token %}

{% for ticket in tickets %}
<div class="ticket{% if ticket.checked_in %} complete{% elif ticket.selected %} selected{% endif %}{% if ticket.primary %} primary{% endif %}">
	<input type="hidden" name="t_{{ ticket.id }}" value="{% if ticket.selected and ticket.entered %}1{% else %}0{% endif %}" />
{% if ticket.selected %}
	<div class="initial"></div>
{% endif %}
	<ul class="icons">
{% if ticket.primary %}
	 	<li>Primary</li>
{% endif %}
	<li>{{ ticket.get_category_display }}{% if ticket.premium %}(Queue Jump){% endif %}</li>
	</ul>
{% if ticket.checked_in %}
	<div class="status">Already Entered</div>
{% endif %}
	<h3>{{ ticket }}</h3>
	<h4>{{ ticket.code }}</h4>
	<!-- <h5>{$ticket['entrance']}</h5> -->
	<!-- <h6>{if $separate}Separated Entry{/if}</h6> -->
</div>
<span class="error"></span>
{% endfor %}

<span id="warning" class="error"></span>
{% if not complete %}
	<input type="submit" name="form_submit" value="Check In" class="button" />
{% endif %}
</form>
{% endblock %}
