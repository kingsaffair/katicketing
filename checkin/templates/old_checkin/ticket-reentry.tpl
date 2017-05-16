{% extends "old_checkin/main.tpl" %}
{% block body %}
	<h2>{{ hash }}</h2>
	<p>The re-entry ticket <em>{{ hash }}</em> needs to be activated.</p>
	<p>Please fill in the name of the guest which needs re-entry.</p>
	<form method="post" action="{url mode=$hash}" class="simple">
		<input type="hidden" name="ahash" value="{{ hash }}" />
		<label for="name">Full name</label>
		<input type="text" name="name" class="field" />
		<input type="submit" name="submit" value="Activate" class="button" />
	</form>
{% endblock %}