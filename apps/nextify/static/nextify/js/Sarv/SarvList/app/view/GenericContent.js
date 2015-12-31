Ext.define('SarvList.view.GenericContent', {
    extend: 'Ext.panel.Panel', 
	closable:false,
    alias: 'widget.genericcontent',
	requires: ['SarvList.view.element.GenericFilterFieldCombo',
	           'SarvList.view.GenericFilterGrid',
	           'SarvList.view.GenericFilterAdd',
	           'SarvList.view.GenericFilterMenu',
	           'SarvList.view.GenericGrid',
	           ],
	layout: 'border',
    items: [
        	{
        		xtype: 'panel',
        		title: 'Filtrid',
        		region: 'west',
        		width:383,
        		//height:80,
        		scroll: false,
        		collapsible: true,        		
        		items: [
		        		    {  
							    xtype: 'genericfiltergrid',
					        },{
					        	xtype: 'genericfilteradd',
					        },{
							    xtype: 'genericfiltermenu',
					        },
			        	]
        	},{ 
        		//xtype: 'container',
        		xtype: 'genericgrid',
	        	region: 'center',
	        	//layout: 'fit',
	        	//height: 400, 
	        	collapsible: false
	        }]
});
