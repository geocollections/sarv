Ext.define('Sarv.view.Viewport', {
    extend: 'Ext.container.Viewport',
    xtype: 'sarv-viewport',
    requires: [
               'Sarv.view.ModalWindow', 
               'Sarv.view.element.GenericFilterFieldCombo',
	           'Sarv.view.GenericFilterGrid',
	           'Sarv.view.GenericFilterAdd',
	           'Sarv.view.GenericFilterMenu',
	           'Sarv.view.GenericSavedSetMenu',
	           'Sarv.view.GenericGrid',
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
   		    { xtype: 'genericfiltergrid' },
   		    { xtype: 'genericfilteradd' },
   		    { xtype: 'genericfiltermenu' },
   		    {
   		    	title: 'Salvestatud päringud',
		        border: 0,
		        items: [{xtype: 'genericsavedsetmenu'}]},
		    { title: 'Funktsioonid' }]
    },{ 
		xtype: 'genericgrid',
    	region: 'center',
    	collapsible: false,
    }],
    initComponent: function(e) {
    	var c = Sarv.conf;
    	this.callParent();
    	
    	if(c.acl[1] == true || c.acl === 'own') {
    		var btn = Ext.create('Ext.Button', {
    			itemId:'btn-form-add', 
    			text:'Lisa uus kirje',
    			iconCls:'page-add', 
    		});
    		this.items.items[0].add(btn);
    	}
    },
});
