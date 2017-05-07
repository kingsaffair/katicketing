{% extends "original/main.tpl" %}
{% block body %}
<ul class="status">
{% if not primary.waiting %}
	<li class="complete">
		<h5>1</h5>
		<span>
			Booking
			<em>{{ primary.created|date:"j/m/Y" }}</em>
		</span>
	</li>
	<li class="{% if not primary.paid %}current{% else %}complete{% endif %}">
		<h5>2</h5>
		<span>
			Payment
			{% if primary.paid %}
				<em>{{ primary.created|date:"j/m/Y" }}</em>
			{% endif %}
		</span>
	</li>
	<li class="{% if primary.collected %}complete{% elif not primary.paid %}future{% else %}current{% endif %}">
		<h5>3</h5>
		<span>
			Collection
			{% if primary.collected %}
				<em>{{ primary.collected|date:"j/m/Y" }}</em>
			{% endif %}
		</span>
	</li>
	<li class="{% if primary.checked_in %}complete{% elif not primary.collected %}future{% else %}current{% endif %}">
		<h5>4</h5>
		<span>
			Entry
			{% if primary.checked_in %}
				<em>{{ primary.checked_in|date:"j/m/Y" }}</em>
			{% endif %}
		</span>
	</li>
{% else %}
	<li class="current">
		<h5>1</h5>
		<span>
			Waiting List
			<em>{{ primary.created|date:"j/m/Y" }}</em>
		</span>
	</li>
	<li class="future">
		<h5>2</h5>
		<span>
			Payment
		</span>
	</li>
	<li class="future">
		<h5>3</h5>
		<span>
			Collection
		</span>
	<li>
	<li class="future">
		<h5>4</h5>
		<span>
			Entry
		</span>
	<li>
{% endif %}
</ul>

<h4>Ticket Details</h4>
<table class="simple" caption="List of tickets" summary="A list of your tickets">
	<thead>
		<tr>
			<th scope="col">Ticket</th>
			<th scope="col">First Name</th>
			<th scope="col">Last Name</th>
			<th scope="col">Ticket Type</th>
{% if not primary.waiting %}
			<th scope="col">Name Changes</th>
{% endif %}
		</tr>
	</thead>
	<tbody>
{% for ticket in tickets %}
		<tr>
			<th scope="row">{% if ticket.primary %}Primary{% else %}Guest {{ forloop.counter0 }}{% endif %}</th>
			<td>{{ ticket.first_name }}</td>
			<td>{{ ticket.last_name }}</td>
			<td>{{ ticket.get_category_display }}{% if ticket.premium %}(Queue Jump){% endif %}</td>
{% if not ticket.waiting %}
{% if forloop.counter0 == 0 %}
			<td>Not permitted</td>
{% else %}
			<td>{% if ticket.has_pending_namechange %}Pending{% else %}<a href="{% url 'namechange' %}">Request a change</a>{% endif %}</td>
{% endif %}
{% endif %}
		</tr>
{% endfor %}
	</tbody>
</table>

{% if primary.waiting %}

<h4>Waiting List</h4>

<p>You are currently on the waiting list. If a place becomes available, you will be offered a spot. Please do not send any payment at this time. Payment is only required if you are offered a ticket.</p>

{% elif pending_nc %}
<h4>Name Change Details</h4>

<p>In order to complete your name change, you will need to send a Bank Transfer to <strong>King&rsquo;s Affair</strong> for the amount of <strong>&pound;{{ total_nc_cost }}</strong>.</p>
<p>Please use the following Reference Code when sending your Bank Transfer: <strong>n{{ primary.id }}-{{ user.username }}</strong>.</p>
<p>Bank Transfers should be sent to:</p>
<p>Sort Code: 60-04-23<br />
Account Number: 24175439</p>
<p>PLEASE DOUBLE CHECK THE SORT CODE, ACCOUNT NUMBER AND REFERENCE CODE, AS IF ANY OF THESE ARE INCORRECT YOUR PAYMENT MAY BE LOST.</p>
<p>If you would like to cancel your name change, please click <a href="{url mode='namechange' arg='cancel'}">here</a>.</p>

{% elif not primary.paid %}

<h4>Payment Details</h4>

{% if primary.payment_method == 'CB' %}
<p>As you have chosen payment via College Bills, you do not have to do anything at this stage.</p>
{% else %}
<p>As you have chosen payment via Bank Transfer, you will need to send a Bank Transfer payable to <strong>King&rsquo;s Affair</strong> for the amount of <strong>&pound;{{ primary.price }}</strong>.</p>
<p>This needs to be done <strong>within 10 days</strong> of the day you booked your ticket.</p>
<p>Please use the following Reference Code when sending your Bank Transfer: <strong>t{{ primary.id }}-{{user.username}}</strong>.</p>
<p>Bank Transfers should be sent to:</p>
<p>Sort Code: 60-04-23<br />
Account Number: 24175439</p>
<p>PLEASE DOUBLE CHECK THE SORT CODE, ACCOUNT NUMBER AND REFERENCE CODE, AS IF ANY OF THESE ARE INCORRECT YOUR PAYMENT MAY BE LOST.</p>

<p>Once your payment has been processed you will receive notifcation by email.</p>
{% endif %}

{% elif not primary.collected %}

<h4>Collection Details</h4>

<p>Information regarding collection of King's Affair tickets will be released shortly through our Facebook page.</p>

{% elif not data.checked_in %}

<h4>Entry Details</h4>

<p>In order to enter the King's Affair you will need to bring one of the following as Valid Photo ID:</p>

<p>&ndash; A current (non-expired) University Card;</p>
<p>&ndash; A photocopy of or actual current passport or driving license with a Photograph and Date of Birth.</p>

{% endif %}

{% endblock %}
