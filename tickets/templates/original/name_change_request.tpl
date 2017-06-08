{% extends "original/main.tpl" %}
{% load static %}
{% block head %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
	<script type="text/javascript" src="{% static 'legacy/js/namechange.js' %}"></script>
{% endblock %}
{% block body %}
<p>Please select and fill in the tickets you wish you change.</p>
<form action="{% url 'namechange' %}" method="post" class="tickets" id="tickets">
	{% csrf_token %}
	<input type="hidden" name="g_count" id="g_count" value="{{ guests|length }}" />

{% for guest in guests %}
	<fieldset id="g{{ forloop.counter0 }}_ticket" class="ticket {% cycle 'odd' 'even' %}">
		<legend><strong>Guest {{ forloop.counter }}</strong> Ticket</legend>
		<div>
			<input type="hidden" name="g{{ forloop.counter0 }}_tid" id="g{{ forloop.counter0 }}_tid" value="{{ guest.id }}" />
			<p>
				<label for="g{{ forloop.counter0 }}_change">Mark for change<span>Check if you want this ticket to change</span></label>
				<input type="checkbox" name="g{{ forloop.counter0 }}_change" id="g{{ forloop.counter0 }}_change" value="true" class="option-field" />
			</p>
			<p{% if error.first_name %}class="field-error"{% endif %}>
				<label for="g{{ forloop.counter0 }}_fname">First Name<span>Their first name&mdash;not just initials</span></label>
				<input type="text" name="g{{ forloop.counter0 }}_fname" id="g{{ forloop.counter0 }}_fname" maxlength="32" value="{{ guest.first_name }}" class="field" />
				<span class="error-message">First name cannot be blank!</span>
			</p>
			<p{% if error.last_name %}class="field-error"{% endif %}>
				<label for="g{{ forloop.counter0 }}_lname">Last Name<span>Their surname</span></label>
				<input type="text" name="g{{ forloop.counter0 }}_lname" id="g{{ forloop.counter0 }}_lname" maxlength="32" value="{{ guest.last_name }}" class="field" />
				<span class="error-message">Last name cannot be blank!</span>
			</p>
		</div>
	</fieldset>
{% endfor %}

{# {% if not user.is_staff %} #}
	<p class="nofield"><strong>Name change requests must be paid by Bank Transfer.</strong></p>
{# {% else %}
	<p class="nofield"><strong>Name changes are free, since you're a committee member.</strong></p>
{% endif %} #}
	<p class="nofield"><input type="submit" name="submit" id="submit" value="Submit" class="button" /></p>
</form>
{% endblock %}
