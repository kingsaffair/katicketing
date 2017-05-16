{% extends "old_checkin/main.tpl" %}
{% load static %}
{% block head %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
	<script type="text/javascript" src="{% static 'legacy/checkin/js/main.js' %}"></script>
{% endblock %}
{% block body %}
	<div class="nojs">
		<p>You must have JavaScript enabled to use this website.</p>
	</div>
	<div class="js">
		<p>You are logged in as {{user.username}} &dash; <a href="{% url 'loginas-logout' %}">Logout</a>.</p>
		<form id="enter-hash" class="simple">
			<p>Manually enter a hash code:</p>
			<label for="hash">Hash</label>
			<input type="text" name="hash" id="hash" class="field" maxlength=8 />
			<input type="submit" name="submit" value="Go" class="button" />
		</form>
	</div>
{% endblock %}