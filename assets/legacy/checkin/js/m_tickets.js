/*
 * Ticket selector written by Andrew Lee 2011.
 */

// Fast Button
FastButton = function(element, handler) {
  this.element = element;
  this.handler = handler;
  
  element.addEventListener('touchstart', this, false);
  element.addEventListener('click', this, false);
};

FastButton.prototype.handleEvent = function(event) {
  switch (event.type) {
    case 'touchstart': this.onTouchStart(event); break;
    case 'touchmove': this.onTouchMove(event); break;
    case 'touchend': this.onClick(event); break;
    case 'click': this.onClick(event); break;
  }
};

FastButton.prototype.onTouchStart = function(event) {
  event.stopPropagation();

  this.element.addEventListener('touchend', this, false);
  document.body.addEventListener('touchmove', this, false);

  this.startX = event.touches[0].clientX;
  this.startY = event.touches[0].clientY;
};

FastButton.prototype.onTouchMove = function(event) {
  if (Math.abs(event.touches[0].clientX - this.startX) > 10 ||
      Math.abs(event.touches[0].clientY - this.startY) > 10) {
    this.reset();
  }
};

FastButton.prototype.onClick = function(event) {
  event.stopPropagation();
  this.reset();
  this.handler(this.element);

  if (event.type == 'touchend') {
    clickbuster.preventGhostClick(this.startX, this.startY);
  }
};

FastButton.prototype.reset = function() {
  this.element.removeEventListener('touchend', this, false);
  document.body.removeEventListener('touchmove', this, false);
};

clickbuster = function() {};

clickbuster.preventGhostClick = function(x, y) {
  clickbuster.coordinates.push(x, y);
  window.setTimeout(clickbuster.pop, 2500);
};

clickbuster.pop = function() {
  clickbuster.coordinates.splice(0, 2);
};

clickbuster.onClick = function(event) {
  for (var i = 0; i < clickbuster.coordinates.length; i += 2) {
    var x = clickbuster.coordinates[i];
    var y = clickbuster.coordinates[i + 1];
    if (Math.abs(event.clientX - x) < 25 && Math.abs(event.clientY - y) < 25) {
      event.stopPropagation();
      event.preventDefault();
    }
  }
};

document.addEventListener('click', clickbuster.onClick, true);
clickbuster.coordinates = [];

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
	
	ticketHandler = function(e) {
		if ($(e).hasClass('complete')) {
			if (mode == 0)
				$(e).next('span.error').html('This ticket has already been collected.');
			else
				$(e).next('span.error').html('This ticket has already been checked in.');
		} else {
			v = $(e).children('input').val();
			if (!ignore && $(e).hasClass('primary')) {
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
				$(e).children('input').val('1');
				if (primary || ignore)
					$(e).addClass('selected');
				else
					$(e).addClass('warning');
				ns++;
			} else {
				$(e).children('input').val('0');
				$(e).removeClass('selected');
				if (primary || ignore)
					$(e).removeClass('selected');
				else
					$(e).removeClass('warning');
				ns--;
			}
			if (!ignore && ns > 0 && !primary) {
				$('span#warning').html('WARNING: The primary ticket is not selected');
			} else {
					$('span#warning').html('');
			}
		}
	};	
	
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
	
	$('div.ticket').each(function(i,x) {
		new FastButton(x,ticketHandler);
	});
	
});