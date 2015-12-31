Ext.define('SarvList.view.GenericSavedSetMenu',{
	extend: 'Ext.toolbar.Toolbar',
	alias: 'widget.genericsavedsetmenu',
	items: [{
        	xtype: 'combo',
        	id: 'custom_datasets_combo',
        	name: 'custom_datasets_combo',
    		displayField	: 'name',
    		valueField		: 'params',
    		queryMode		: 'remote',
    		multiSelect 	: false,
    		autoSelect		: false,
    		matchFieldWidth	: false,
        	store:  Ext.create('Ext.data.Store', {
    		  			autoLoad:true,
    		  			fields:[{name:'name'},{name:'params'}],
    		        	proxy: {
            		        type: 'ajax',
            		        autoLoad: true,
            		        url: 'get_custom_datasets',
            		        reader: {
            		        	type: 'json',
            		            root: 'data',
            		            totalProperty: 'store_record_count',
            		        },
    		        	},
        			}),
        	pageSize: 10,
        	listeners: {
        		specialkey: function(field, e){
       	            if (e.getKey() == e.ENTER) { 
       	            	var cnt = Ext.create('Sarv.controller.Filter');
       	            	//console.log(field.value);
       	            	cnt.savedQuery(field.value);
       	            }
        		},
        		select: function(field,e) {
        			var cnt = Ext.create('Sarv.controller.Filter');
        			//console.log(field.value);
        			cnt.savedQuery(field.value);
        		},
        	},
        },
        '->',
        {
        	text: 'Salvesta',
        	tooltip: 'Salvesta päring',
        	iconCls: 'page-save',
        	handler: function() {
        		var cnt = new Sarv.controller.Filter();
        		cnt.saveQuery(); 
        	},
        	scope: this
        },
        {
        	text: 'Kustuta',
        	tooltip: 'Kustuta päring',
        	iconCls: 'page-delete',
        	handler: function() {
        		var cnt = new Sarv.controller.Filter();
        		cnt.deleteQuery();
        		cnt.showAll(); 
        	},
        	scope: this
        },
        ],
});
