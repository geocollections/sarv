Ext.define('SarvList.view.GenericFilterMenu',{
	extend: 'Ext.toolbar.Toolbar',
	alias: 'widget.genericfiltermenu',
	items: [{
            text: 'Eemalda filter',
            //iconCls: 'row-delete',
            scope: this,
            handler: function () { 
            			var controller = new Sarv.controller.list.Filter(); 
            			controller.remove(); 
            	},
        }, 
        '->',
        {
        	text: 'Minu kirjed',
        	handler: function() {
        		var controller = new Sarv.controller.list.Filter(); 
    			controller.filteredQuery('yes'); 
        	},
        	scope: this
        },{
        	text: 'Näita kõiki',
        	handler: function() {
        		var controller = new Sarv.controller.list.Filter(); 
    			controller.showAll(); 
        	},
        },
        {
        	text: 'Filtreeri',
        	iconCls: 'search',
        	handler: function() {
    			var controller = new Sarv.controller.list.Filter(); 
    			controller.filteredQuery();
        	},
        }
        ],
});
