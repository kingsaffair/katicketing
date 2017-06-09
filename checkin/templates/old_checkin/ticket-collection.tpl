{% extends "old_checkin/main.tpl" %}
{% load static %}
{% block head %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
	<script type="text/javascript">mode = 0; ignore = 0;</script>
	<script type="text/javascript" src="{% static 'legacy/checkin/js/tickets.js' %}"></script>
{% endblock %}
{% block body %}
{% if not ticket.paid %}
<p class="error">Required payment of &pound;{{ ticket.price }}.</p>
{% endif %}
<form method="post" action="" class="tickets{% if not paid %} notpaid{% endif %}">
{% csrf_token %}

{% for ticket in tickets %}
<div class="ticket{% if ticket.collected %} complete{% elif ticket.selected %} selected{% endif %}{% if ticket.primary %} primary{% endif %}">
	<input type="hidden" name="t_{{ ticket.id }}" value="{% if ticket.selected and ticket.collected %}1{% else %}0{% endif %}" />
{% if ticket.selected %}
	<div class="initial"></div>
{% endif %}
	<ul class="icons">
{% if ticket.primary %}
	 	<li>Primary</li>
{% endif %}
	<li>{{ ticket.get_category_display }}{% if ticket.premium %}(Queue Jump){% endif %}</li>
	</ul>
{% if ticket.collected %}
	<div class="status">Already Collected</div>
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
	<input type="submit" name="form_submit" value="Mark as Collected" class="button" />
{% endif %}
</form>
{% endblock %}