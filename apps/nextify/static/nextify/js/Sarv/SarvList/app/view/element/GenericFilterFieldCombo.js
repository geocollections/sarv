Ext.define('SarvList.view.element.GenericFilterFieldCombo',{
	extend: 'Ext.form.field.ComboBox',
    valueField: 'name',
    displayField: 'name',
    alias: 'widget.genericfilterfieldcombo',
    lazyRender:true,
    //mode: 'local',
    valueNotFoundText: 'Value Not Found',
    store: Ext.create('Ext.data.ArrayStore',{
           		fields:[{name:'name'},{name:'filter_type'}],
            	data: filters.fields 
           }),
    triggerAction: 'all',
    forceSelection: true, 
    listeners: { 
       select: function(combo,record,index) { 
            var controller = new Sarv.controller.Filter();
            controller.updateComboBox(combo,'genericfiltergrid');
       } 
    },
    
    selectOnFocus	: true,
	typeAhead		: true,
	minChars		: 0,
	mode: 'local',
});
