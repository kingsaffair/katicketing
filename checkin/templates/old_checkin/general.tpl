{% extends "old_checkin/main.tpl" %}
{% block body %}
{% for error_line in description %}
<p>{{ error_line }}</p>
{% endfor %}
{% endblock %}
