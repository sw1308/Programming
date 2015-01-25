$(document).ready(function(){
	$(".hiddenTop").removeClass("hiddenTop");
	$(".stdContainer ul li").addClass("selectable");
	$(".selectable").parents().css("overflow", "hidden");
	var parent, ink, d, x, y;
	$(".selectable").click(function(e){
		parent = $(this).parent();
		if(parent.find(".ink").length == 0)
			parent.prepend("<span class='ink'></span>");

		ink = parent.find(".ink");
		ink.removeClass("animate");
		if(!ink.height() && !ink.width())
		{
			d = Math.max(parent.outerWidth(), parent.outerHeight());
			ink.css({height: d, width: d});
		}
		x = e.pageX - ink.width()/2;
		y = e.pageY - ink.height()/2;
		ink.css({top: y+'px', left: x+'px'}).addClass("animate");
	});
});
