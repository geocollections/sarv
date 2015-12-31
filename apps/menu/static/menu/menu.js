$(function() {
	$('.menu-column').live("mouseover", function(){
		
		$('.sortable-column').sortable(
				 { connectWith: '.sortable-column', /*cancel: '.ui-state-disabled'*/},
				 { 
				   start: function(event, ui) {
					 from_to = false
					 column_from = ui.item.parent().attr('id');
				   }, 
				   update: function(event, ui) { 
					 sorted = $(this).sortable('serialize');
					 console.log(sorted);
					 column_to = ui.item.parent().attr('id');
					 column_update = !from_to ? column_from : column_to;
					 console.log(from_to+' '+column_from+' '+column_to);
					 menu.action ('set_row_order',{sorted:sorted,column_update:column_update})
					 
					 from_to = true;
				   }  
				 }
		);
		//$('.ui-state-disabled').disableSelection();
	});
	
	$('.menu-column').live("mouseover", function() {
		$('.menu').sortable(
				 { update: function(event, ui) { 
					 sorted = $(this).sortable('serialize');
					 menu.action ('set_column_order', {sorted:sorted})
					 } 
				 }
			);
	});
});

var menu = {
	action: function (type, values) {
		$.get(type+'/', values,
				function(data) {
					var data = JSON.parse(data);
					$('input').val('');
					if(data.error == 'session_expired') 
						window.location.reload(); 
					if(data.f) { data.f(data); 
					} else if(data.reload) {
						$.get(data.reload+'/', false, function(response){
							var destination = data.destination?data.destination:'document';
							$(destination).html(response);
						});
					} 
					if('undefined' !== typeof data.message) menu.message(data.message);
				}		
			);
	},	
		
	message: function(data) {
			var sm = $('#site-messages');
			sm.html('<span style="background-color:#000">'+data+'</span>');
			sm.fadeIn().delay(4000).fadeOut();
	},
	
	toggle: function (id) {
		$('div[id^="do-menuitem-edit"]:not(div[id="do-menuite-edit-'+id+'"])').slideUp();
		var element = $('#do-menuitem-edit-'+id); 
		element.css('display') == 'none' ? element.slideDown() : element.slideUp();
	},
}














