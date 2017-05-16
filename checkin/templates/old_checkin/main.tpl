{% load static %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
	<title>{{ event_name }}{% if page_name != '' %} &mdash; {% endif %}{{ page_name }}</title>
	<link rel="stylesheet" href="{% static 'legacy/checkin/css/default.css' %}" />
	{% block head %}{% endblock %}
</head>
<body>
<div id="mainContainer">
<h1>{{ event_name }}</h1>
<h2>{{ mode }}</h2>
{% if user.is_staff  %}
	<a href="{url mode=""}" class="toplink">Main Menu</a>
{% endif %}
<div id="contentContainer">
{% block body %}{% endblock %}
</div>
<span class="copyright">Copyright &copy; {{ event_name }}. All rights reserved.</span>
</div>
</body>
</html>