{% load static %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
	<title>{{ event_name }}{% if page_name %} &mdash; {{ page_name}}{% endif %}</title>
	<link rel="stylesheet" href="{% static 'legacy/css/default.css' %}" />

	{% block head %}{% endblock %}
</head>
<body>
<div id="mainContainer">
<h1>{{ event_name }}</h1>
<h2>{{ site_name }}</h2>
<div id="contentContainer">

{% if page_name %}<h3>{{ page_name }}</h3>{% endif %}
{% block body %}{% endblock %}
<div class="footer-links">
{% if user %}
	<span class="small_header">Logged in as {{ user.username }}{% if user.committee_flag == 2 %} &mdash; <a href="{% url 'ticket-admin' %}">Admin</a>{% endif %} &mdash; <a href="{% url 'user-logout' %}">Log out</a>.</span>
{% endif %}
	<ul>
		<li><a href="{% url "tickets" %}">Home</a></li>
		<li><a href="{% url "faq" %}">FAQ</a></li>
		<li><a href="{% url "terms-and-conditions"}">Terms and Conditions</a></li>
	</ul>
</div>
</div>
<span class="copyright">Copyright &copy; {{ event_name }}. All rights reserved.</span>
</div>
</body>
</html>
