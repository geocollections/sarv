Ext.define('SarvList.view.Viewport', {
    extend: 'Ext.container.Viewport',
    requires: [
               'SarvList.view.ModalWindow', 
               'SarvList.view.element.GenericFilterFieldCombo',
	           'SarvList.view.GenericFilterGrid',
	           'SarvList.view.GenericFilterAdd',
	           'SarvList.view.GenericFilterMenu',
	           'SarvList.view.GenericSavedSetMenu',
	           'SarvList.view.GenericGrid',
               ],
    layout: 'border',
    items:[{
	       		title: 'Filtrid',
	       		region: 'west',
	       		id: 'filtrid',
	       		width:383,
	       		scroll: false,
	       		collapsible: true,        		
	       		items: [
	        		    {  
						    xtype: 'genericfiltergrid',
				        },{
				        	xtype: 'genericfilteradd',
				        },{
						    xtype: 'genericfiltermenu',
				        },{
				        	title: 'Salvestatud päringud',
				        	border: 0,
				        	items: [{xtype: 'genericsavedsetmenu',}],
				        },{
				        	title: 'Funktsioonid',
				        }
				        ]
           },{ 
	    		xtype: 'genericgrid',
	        	region: 'center',
	        	collapsible: false,
           }],
    initComponent: function() {
    	this.callParent();
    	var cnt = new Sarv.controller.Filter();
    	if(records.settings.acl[1] == true 
    		|| records.settings.acl === 'own') {
    		var btn = Ext.create('Ext.Button', {
    			id:'item-add', 
    			text:'Lisa uus kirje',
    			iconCls:'page-add', 
    			handler: function() {
	        		cnt.openPopup(records.settings);
    			},
    			});
    		Ext.getCmp('filtrid').add(btn);
    	} 
    	
    	if('undefined'!==records.settings.doFilteredQuery) {
    		switch (records.settings.doFilteredQuery) {
    			case 'my':
    				cnt.filteredQuery(true);
    				break;
    			case 'all':
    				cnt.showAll();
    				break;
    		}
    	}
    },
});
