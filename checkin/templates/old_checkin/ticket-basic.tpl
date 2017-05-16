{% extends "old_checkin/main.tpl" %}
{% block body %}
<h2>{{ ticket.code }}</h2>
<dl class="simple">
    <dt>Full Name</dt>
    <dd>{{ ticket }}</dd>
    
    <dt>Ticket Type</dt>
    <dd>{{ ticket.get_category_display }}{% if ticket.premium %}(Queue Jump){% endif %}</dd>

    <dt>Primary Ticket</dt>
{% if ticket.primary %}
    <dd>Yes</dd>
{% else %}
    <dd>No</dd>
{% endif %}
</dl>
{% endblock %}