Ext.define('SarvForm.view.RecordPage', {
    extend: 'Ext.container.Viewport',
    alias: 'widget.record-page',
    xtype: 'record-page',
    autoScroll: false,
    autoDestroy: true,
    layout: 'border',
    items:[{
    	xtype: 'container',
    	id: 'item-toolbar',
    	scope: this,
    	region: 'north',
    	border: false,
    	overClass: 'x-view-over'
    },{
        xtype: 'record-form',
		scope: this, 
		region: 'center',
		border: false,
		height: 800
    }]
});
