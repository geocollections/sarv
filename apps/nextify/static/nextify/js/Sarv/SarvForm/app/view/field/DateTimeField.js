Ext.define('SarvForm.view.field.DateTimeField', {
	extend: 'SarvForm.view.field.Hbox',
	xtype: 'datetimefield',
	items:[{
		xtype: 'datefield',
		fieldLabel: 'Aeg'
	},{
	    xtype: 'sarv-timefield',
	    width:50
	}],
	initConfig: function() {
		this.callParent();
	}
});