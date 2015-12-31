acl = {
	action: function(data,set) {
		var output = {};
		var errors = {};
		var set = set||false;
		if(!$(data).is('button')) 
			output[$(data).attr('name')] = $(data).attr('value');

		$.each($(data).siblings(), function(index,value){
			if('undefined' !== typeof $(this).attr('name')) {
				if ($(this).hasClass('required') === true 
						&& ($(this).attr('value') == ''||$(this).attr('value') === 'undefined')) {
					errors['required-'+$(this).attr('name')] = 'Väli "'+$(this).attr('name')+'" on kohustuslik';
				} else {
					output[$(this).attr('name')] = $(this).attr('value');
				}
			};
		});
		
		if ('undefined' !== set.userlevel)
			output['userlevel'] = set.userlevel;
		
		if ('undefined' !== set.group) output['group'] = set.group; 
		if (set.id == 'all') output['save_all'] = true;
		if (Object.keys(output).length > 0 && Object.keys(errors).length < 1)
			$.get(
				'add/', 
				output,
				function(data) {
					if(output['subaction'] == 'insert_page_user_right')
						if(set.id == 'all') {
							for (pages in acl.data.pages[set.user])
								for(page in acl.data.pages[set.user][pages])
									acl.data.pages[set.user][pages][page][1][set.group] = set.userlevel;
							acl.render(set.user);
						} else
							for(pages in acl.data.pages[set.user])
								if('undefined' !== typeof acl.data.pages[set.user][pages][set.pagename])
									acl.data.pages[set.user][pages][set.pagename][1][set.group] = set.userlevel;
					
					alert('Andmed muudetud');
				}
			);
		else acl.show_errors(errors);
	},
	
	show_errors: function(errors) {
		var str = '';
		for (k in errors) {
			str += errors[k]+'\n';
		}
		alert(str);
	},
	
	render: function(actor) {
		var hidden = '<input type="hidden" name="user" value="'+actor+'" />';
		hidden += '<input type="hidden" name="subaction" value="insert_page_user_right" />';
		hidden += '<input type="hidden" name="destination" value="SarvPage" />';

		var html = '<table>';

		html += '<tr><td></td>';
		for(page in acl.data.pages[actor][0])
			for (group in acl.data.pages[actor][0][page][1]) 
				html += '<td style="text-align:center"><u>'+group+'</u></td>';
		html += '</tr>';
		
		html += '<tr style="background-color:#eee;">';
		html += '<td>';
		html += '<strong>Sea kõigil lehtedel:</strong></td>';
				
		for(page in acl.data.pages[actor][0]) {
			for (group in acl.data.pages[actor][0][page][1]) {
				html += '<td><select name="userlevel" ';
				html += 'onchange="acl.action(this,{id:\'all\',';
				html += 'pagename:\''+page+'\',';
				html += 'group:\''+group+'\',user:\''+actor+'\',userlevel:$(this).val()})">';
				html += '<option value="None"></option>';
				for (right in acl.rightsgroups)
					html += '<option value="'+acl.rightsgroups[right]+'">'+acl.rightsgroups[right]+'</option>';
				html += '</select>';
				html += hidden;
				html += '</td>';
			}
		}
		html += '</tr>';
		
		var i=0;
		for(row in acl.data.pages[actor]) {
			for(page in acl.data.pages[actor][row]) {
				if('undefined' !== typeof acl.col_names[i])
					html += '<tr><td class="col_header">'+acl.col_names[i]+'</td></tr>';
				html += '<tr>';
				html += '<td>'+page+'</td>';
				for(group in acl.data.pages[actor][row][page][1]) {
					html += '<td><select name="userlevel" onchange="acl.action(';
					html += 'this,{id:'+acl.data.pages[actor][row][page][0]+',';
					html += 'pagename:\''+page+'\',';
					html += 'group:\''+group+'\',user:\''+actor+'\',userlevel:$(this).val()})">';
					for (right in acl.rightsgroups) {
						html += '<option value="'+acl.rightsgroups[right]+'"';
						if (acl.rightsgroups[right] == acl.data.pages[actor][row][page][1][group])
							html += ' selected="selected"';
						html += '>'+acl.rightsgroups[right]+'</option>';
					}
					html += '</select>';
					html += hidden
					html += '<input type="hidden" name="id" value="'+acl.data.pages[actor][row][page][0]+'" />';
					html += '</td>';				
				}
			}
			i++;
		}
		html += '</tr>';
		html += '</table>';
		document.getElementById('acl-rights-grid').innerHTML = html;
	},
};
