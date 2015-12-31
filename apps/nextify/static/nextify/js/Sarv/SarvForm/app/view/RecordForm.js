Ext.define('SarvForm.view.RecordForm', {
	extend: 'Ext.form.Panel',
	itemId: 'record-form',
	alias: 'widget.record-form',
	autoScroll: true,
	hideMode: "offsets",
	autoDestroy: true,
	scope: this,
	url: 'save', //url called when form is submitted
	defaults: {
        xtype: 'textfield',
        anchor: '100%',
        labelAlign : 'right',
        listeners: {
        	change: function() {
        		SarvForm.conf.edited = true;
        	}
        },
    },
    initComponent: function() {
    	this.items=SarvForm.conf.formFields;
    	this.callParent(arguments);
    },
    getInvalidFields: function() {
        var invalidFields = [];
        Ext.suspendLayouts();
        this.form.getFields().filterBy(function(field) {
            if (field.validate()) return;
            invalidFields.push(field);
        });
        Ext.resumeLayouts(true);
        return invalidFields;
    },
    listeners: {
    	beforecontainerclickexi: function() {
    		console.log('vc');
    	}
    }
});