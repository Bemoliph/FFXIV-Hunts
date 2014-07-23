function getTargets() {
	$.getJSON('/api/getTargets', function(data) {
		$.each(data, function(index, element) {
			
			$("#" + element.rankname).append($('<div>', {
				text: element.targetname
			}));
		});
	});
}

/* http://www.sitepoint.com/structural-markup-javascript/ */
function addEvent(obj, evType, fn)
{
	if (obj.addEventListener){obj.addEventListener(evType, fn, false); return true;}
	else if (obj.attachEvent){var r = obj.attachEvent("on"+evType, fn); return r;}
	else {return false;}
 }

addEvent(window, 'load', getTargets);