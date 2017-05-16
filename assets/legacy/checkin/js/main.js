/*
 * Written by Andrew Lee 2012.
 */

$(document).ready(function() {
	
	$('.nojs').hide();
	$('.js').show();
	
	$('#enter-hash').submit(function() {
		v = $('#enter-hash input#hash').val();
		if (v.length != 8) {
			alert('A hash must be 8 characters long!');
		} else {
			$('#enter-hash input#hash').val('');
			window.open('/t/' + v.toLowerCase() + '/', '_self');
		}
		return false;
	});
	
});