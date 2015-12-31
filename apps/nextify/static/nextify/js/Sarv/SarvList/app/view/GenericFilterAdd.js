Ext.define('SarvList.view.GenericFilterAdd', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.genericfilteradd',
    id: 'genericfilteradd',
    plugins: [
        Ext.create('Ext.grid.plugin.CellEditing', {clicksToEdit:1})
    ],
    hideHeaders: true,
    width: 383,
    scroll: false,
    store: Ext.create('Ext.data.ArrayStore', {
    			fields: [
        		         {name: 'field'},
        		         {name: 'filter'},
        		         {name: 'filter_type'},
        		         {name: 'filter_default_num'},
        		         {name: 'value'},
        		         ],
                data: [['Vali väli','','','']],
    }),
    columns: [ {
              sortable : false,
              dataIndex: 'field',
              width: 161,
              editor: new Ext.form.field.ComboBox({
            	  		displayField: 'name',
            	  		valueField: 'name',
            	  		store: Ext.create('Ext.data.ArrayStore',{
            	  				fields:[{name:'name'},{name:'filter_type'}],
            	  				data: filters.fields 
              				}),
              			triggerAction: 'all',
              			forceSelection: true, // u. nagu editable: false, kuid saab teksiväljal otsida
              			emptyText: 'Vali väli',
              			listeners: { 
              				select: function(combo, records, index) { 
	              		            var controller = new Sarv.controller.Filter();
	              		            controller.updateComboBox(combo,'genericfilteradd');
	              		            
              				},
              				
              			},
              			
              		    selectOnFocus	: true,
              			typeAhead		: true,
              			minChars		: 0,
              			mode: 'local',
              		}),
            	      
           	},{
           		sortable : false,
                id: 'filter_combo',
                dataIndex: 'filter',
                width: 111,
                sortable : false,
                hideable : false,
                getEditor : function(record, defaultField) {
            	  
            	    if(record.get('filter_type')=='') return false;
            	  
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
           		sortable: false,
           		hideable: false,
           		width: 111,
           		dataIndex: 'value',
           		getEditor : function(record) {
           			if(record.get('filter_type')!="")
           				return {
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
           				};
           		},	
           	},
           	],
     autoHeight: true,
});
