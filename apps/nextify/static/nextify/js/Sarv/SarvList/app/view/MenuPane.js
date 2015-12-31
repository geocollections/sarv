Ext.define('SarvList.view.MenuPane',{
	extend: 'Ext.toolbar.Toolbar',
	alias: 'widget.menupane',
	items: [
			'<img src="/static/images/logo_small.png" style="margin: 0px 8px;"/>', 
			'-',
			{ 
				text: 'Menüü',
				id: 'main-menu-btn',
				handler: show_menu,
			},
/*			{
				text: 'Kollektsioonid',
				menu: {
					items: [{
						text: 'Nimekiri',
						icon: '/static/images/application_view_columns.png',
						model: 'Collection',
						handler: this.list
					},{
						text: 'Vorm',
						icon: '/static/images/application_form.png',
						model: 'Collection',
						handler: this.show
					}]
				}
			},{
				text: 'Eksemplarid', 
				menu: {

					items: [{
						text: 'Nimekiri',
						icon: '/static/images/application_view_columns.png',
						model: 'Specimen',
						handler: this.list
					},{
						text: 'Vorm',
						icon: '/static/images/application_form.png',
						model: 'Specimen',
						handler: this.show
					},{
						text: 'Valikud',
						model: 'SelectionSeries',
						handler: this.list
					}]
				
					items: [{
						text: 'Eksemplarid', 
						menu: {
							items: [{
								text: 'Nimekiri',
								icon: '/static/images/application_view_columns.png',
								model: 'Specimen',
								handler: this.list
							},{
								text: 'Vorm',
								icon: '/static/images/application_form.png',
								model: 'Specimen',
								handler: this.show
							}]
						}
					},{
						text: 'Valikud',
						model: 'SelectionSeries',
						handler: this.list
					}]
 				
				}
			},{
				text: 'Proovid', 
				menu: {
					items: [{
						text: 'Proovid', 
						menu: {
							items: [{
								text: 'Nimekiri',
								icon: '/static/images/application_view_columns.png',
								model: 'Sample',
								handler: this.list
							},{
								text: 'Vorm',
								icon: '/static/images/application_form.png',
								model: 'Sample',
								handler: this.show
							}]
						}
					},{
						text: 'Preparaadid', 
						menu: {
							items: [{
								text: 'Nimekiri',
								icon: '/static/images/application_view_columns.png',
								model: 'Preparation',
								handler: this.list
							},{
								text: 'Vorm',
								icon: '/static/images/application_form.png',
								model: 'Preparation',
								handler: this.show
							}]
						}
					},{
						text: 'Analüüsid', 
						menu: {
							items: [{
								text: 'Nimekiri',
								icon: '/static/images/application_view_columns.png',
								model: 'SampleAnalysis',
								handler: this.list
							},{
								text: 'Vorm',
								icon: '/static/images/application_form.png',
								model: 'SampleAnalysis',
								handler: this.show
							}]
						}
					}]
				}
			},
			'-',
			{text:'Ülejäänud funktsioonid', handler: function() { window.location = 'sarv_intra'; }
			},*/
			
			'->',
			//'<span class="user">Kasutaja: <b>'+username+'</b></span>', 
			//'<span class="database">Andmebaas: <b>'+database+'</b></span>',
			'-',
			//(userpriv?{text:'Admin', handler: function(){ window.location = 'admin';}}:''),
			//{text: 'Logi välja', icon: '/static/images/door_out.png', iconAlign: 'right', handler: function() {
			//	window.location = '/logout';
			//}}
		]
});