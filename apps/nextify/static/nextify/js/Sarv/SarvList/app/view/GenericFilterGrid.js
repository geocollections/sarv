Ext.define('SarvList.view.GenericFilterGrid', {
    extend: 'Ext.grid.Panel',
    requires: ['SarvList.view.element.GenericFilterFieldCombo',
               ],
    alias: 'widget.genericfiltergrid',
    id: 'genericfiltergrid',
    width: 383,
    scroll : false,
    plugins: [
              Ext.create('Ext.grid.plugin.CellEditing', {
                  clicksToEdit: 1,
              })
          ],
    store: Ext.create('Ext.data.ArrayStore', {
        		fields: [
        		         {name: 'field'},
        		         {name: 'filter'},
        		         {name: 'filter_type'},
        		         {name: 'filter_default_num'},
        		         {name: 'value'},
                 ],
                data: filters.filters_default
          }),
    columns: [ {
              text     : 'Field',
              dataIndex: 'field',
              width : 161,
              sortable : false,
              hideable : false,
              editor: 'genericfilterfieldcombo',
           	},{
              text     : 'Filter',
              dataIndex: 'filter',
              width: 111,
              sortable : false,
              hideable : false,
              getEditor : function(record, defaultField) {
            	  
            	  filter_types = filters.filters_types;
            	  
            	  //TODO: Extra bug security feature to delineate filter keys?
            	  var filter_type = record.get('filter_type');            	  
            	  
            	  var combostore = Ext.create('Ext.data.ArrayStore', {
            		  	autoLoad:true,
		  		   		fields:[{name:'filtername'},{name:'filtervalue'}],
		  		   		data: filter_types[ filter_type ],
            	  });

            	  var combobox = Ext.create('Ext.form.field.ComboBox',{ 
            		  	valueField: 'filtervalue',
            		    displayField: 'filtervalue',
            		    store: combostore,
            	  });

            	  return Ext.create('Ext.grid.CellEditor', { field: combobox }); 
              },
              
           	},{  
              dataIndex: 'filter_type',
              hidden: true,
              hideable: false,
			},{
           		text	: 'Value',
           		dataIndex: 'value',
           		width: 111,
           		sortable : false,
           		hideable : false,
           		editor: {
           			xtype: 'textfield',
           			listeners: {
               	    	specialkey: function(field, e){
               	            if (e.getKey() == e.ENTER) {
               	            	setTimeout(function(){ 
               	            		var controller = new Sarv.controller.Filter();
	               	            	controller.filteredQuery();
               	            	},50);
               	            }
               	        }
               	    },
               	},
           	},
           	],
     autoHeight: true,
});
