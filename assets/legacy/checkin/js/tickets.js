/*
 * Ticket selector written by Andrew Lee 2011.
 */


$(document).ready(function() {
	var primary = false;
	var ns = $('div.ticket.selected').length;
	
	if ($('div.ticket.primary').first().hasClass('complete') || $('div.ticket.primary').first().hasClass('selected') || ignore) {
		primary = true;
	} else {
		$('div.ticket.selected').each(function(i,x) {
			$(x).addClass('warning');
			$(x).removeClass('selected');
		});	
		if (ns > 0 && !primary) {
			$('span#warning').html('WARNING: The primary ticket is not selected');
		} else {
				$('span#warning').html('');
		}
	}
	
	$('div.ticket').click(function() {
		if ($(this).hasClass('complete')) {
			if (mode == 0)
				$(this).next('span.error').html('This ticket has already been collected.');
			else
				$(this).next('span.error').html('This ticket has already been checked in.');
		} else {
			v = $(this).children('input').val();
			if (!ignore && $(this).hasClass('primary')) {
				if (v == '0') {
					primary = true;
					$('div.ticket.warning').each(function(i,x) {
						$(x).removeClass('warning');
						$(x).addClass('selected');
					});
					$('span#warning').html('');
				} else {
					primary = false;
					$('div.ticket.selected').each(function(i,x) {
						$(x).addClass('warning');
						$(x).removeClass('selected');
					});
				}
			}
			if (v == '0') {
				$(this).children('input').val('1');
				if (primary || ignore)
					$(this).addClass('selected');
				else
					$(this).addClass('warning');
				ns++;
			} else {
				$(this).children('input').val('0');
				$(this).removeClass('selected');
				if (primary || ignore)
					$(this).removeClass('selected');
				else
					$(this).removeClass('warning');
				ns--;
			}
			if (!ignore && ns > 0 && !primary) {
				$('span#warning').html('WARNING: The primary ticket is not selected');
			} else {
					$('span#warning').html('');
			}
		}
	});	
	
	$(document).keypress(function(e) {
		v = e.which;
		if (v >= 49 && v <= 57) {
			v -= 49;
			$('div.ticket:eq(' + v + ')').trigger('click');
		}
		if (v == 83 || v == 115) {
			$('form.tickets').trigger('submit');
		}
	});
	
	$('form.tickets').submit(function() {
		if ($(this).hasClass('notpaid')) {
			if (confirm("WARNING: This person has not yet paid.\n\nWould you like to mark him as paid and submit the tickets?") == false) {
				return false;
			}
		}
		
		if (!ignore && ns > 0 && !primary) {
			return confirm("WARNING: The primary ticket is not selected.\n\nWould you still like to submit the tickets?");
		} else {
			return true;
		}
	});
	
});