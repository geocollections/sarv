Ext.define('SarvList.controller.Filter', {
    extend: 'Ext.app.Controller',
    init: function() {

    },
	add: function(myResults) {
		var grid_from = Ext.getCmp("genericfilteradd");
		var grid_to = Ext.getCmp("genericfiltergrid");
		var store_from = grid_from.getStore().first();
		var store_to = grid_to.getStore();
		
		if( store_from.get('field') != "Vali väli" 
			&& store_from.get('value')!="" 
			&& store_from.get('value')!=" " 
			//TODO: is filter type set
			) {
			//console.log('filter here - add');
			store_to.add({
		    				field	:	store_from.get('field'),
		    				filter	:	store_from.get('filter'),
		    				value	:	store_from.get('value'),
		    				filter_type : store_from.get('filter_type'),
		   	});
			
		    store_to.commitChanges();
		    setTimeout(function(){
		    	grid_to.getView().refresh();
		    	grid_from.getStore().reload();
		    },50);
		}
		
		 
	},
    
	remove: function() {
    	var grid = Ext.getCmp('genericfiltergrid');
        if (grid) {
            var sm = grid.getSelectionModel();
            var rs = sm.getSelection();
            if (!rs.length) {
                Ext.Msg.alert('Info', 'No Records Selected');
                return;
            }
            //Ext.Msg.confirm('Remove Record', 'Are you sure?', function (button) {
            //    if (button == 'yes') {
                    grid.store.remove(rs[0]);
                    //TODO: update grid
            //    }
            //});
        }
	},
	
	updateComboBox: function(combo,gridName) { 
		
		var grid = Ext.getCmp(gridName);
		var selection_model = grid.getSelectionModel();
		var cs = selection_model.getSelection();
		
		var selection_store = selection_model.getStore();
		var field_name = combo.getValue();
		
		var filter_type = filters.fields_filter_types[field_name];
		cs[0].set({
					filter : filters.filters_types[filter_type][0][1],
					filter_type : filter_type,
					filter_default_num : 0 
				});
		/*
		if (filter_type == 'boolean'||filter_type == 'nullboolean') {
			console.log(filter_type);
			var formvalues = [{'name':'tõene'},{'name':'väär'}];
			if (filter_type == 'nullboolean') formvalues.unshift({'name':'puudub'});
			var booleanValueCombo = Ext.create('Ext.form.field.ComboBox', {
				store: Ext.create('Ext.data.ArrayStore', {
	  		   		fields:[{name:'name'}],
	  		   		data: formvalues,}),
				valueField: 'name',
				displayField: 'name',
			});
			var booleanValueEditor = Ext.create('Ext.grid.CellEditor', {field: booleanValueCombo});
			grid.columns[2].setEditor(booleanValueEditor);
		}*/
		
		grid.getStore().commitChanges();
		grid.getView().refresh();
		
		
	},
	
	filteredQuery: function(myResults) {
		this.add();
		//var grid_from = Ext.getCmp('genericfiltergrid');
		var grid_to = Ext.getCmp('genericgrid');
		//var store_from = grid_from.getStore().getRange();
		var store_to = grid_to.getStore();
		
		var queryValues = this.getQueryValues();
		/*
		var queryValues = [];
		for(var i=0,totalRecords = store_from.length;i<totalRecords;i++){
			 var row = store_from[i].data;
			 var row_filter = '';
			 var this_filter_type = filters.filters_types[row['filter_type']];
			 for(var j=0, totalFilters = this_filter_type.length;
			 		j<totalFilters;j++) {
				 if(this_filter_type[j][1] == row['filter'])
					 row_filter = this_filter_type[j][0];
			 }	 
		     queryValues.push([filters.fields_verbosenames[row['field']],row_filter,row['filter_type'],row['value']]);
		}
		*/
		if (myResults) {
			store_to.getProxy().extraParams.myresults = 'yes';
		}
		//console.log(JSON.stringify(queryValues));
		store_to.getProxy().extraParams.fp = JSON.stringify({fp:queryValues});

		store_to.load({params:{start:0}});

		if(!store_to.isLoading()) 
			store_to.loadPage(1);
		
		store_to.currentPage = 1; 
		useFilters = true;
	},
	
	saveQuery: function() {
		var queryValues = this.getQueryValues();
		var selectionNameCombo = Ext.getCmp('custom_datasets_combo');
		//console.log(selectionNameCombo.getRawValue());
		if (typeof selectionNameCombo.getRawValue() != 'undefined') {
			Ext.Ajax.request({
				url:'set_custom_dataset',
				params: {
					name: selectionNameCombo.getRawValue(), //.getValue(),
					params: JSON.stringify(queryValues),
				},
				success: function(response) {
					show_message({message:'Salvestatud', success:true});
					var cnt = Ext.create('SarvList.controller.Filter');
					cnt.filteredQuery();
				},
				failure: function(response) {
					show_message({message:'Salvestamine ebaõnnestus', error:true});
				},
			});
		} else {
			window.show_message({message:'Vaja sisestada nimi', error:true});
		}
	},
	
	savedQuery: function(params) {
		if (typeof params == 'undefined') return;
		var grid_to = Ext.getCmp('genericgrid');
		var store_to = grid_to.getStore();
		var inputparams = JSON.parse(params);
		for (var key in inputparams) break;
		inputparam = JSON.parse(inputparams[key])
		console.log(inputparams);
		store_to.getProxy().extraParams.fp = JSON.stringify({fp:inputparam});
		store_to.load({params:{start:0}});
		if(!store_to.isLoading()) store_to.loadPage(1);
		store_to.currentPage = 1; 
		useFilters = true;	
		
		var grid_from = Ext.getCmp('genericfiltergrid');
		var store_from = grid_from.getStore();
		store_from.removeAll();
		//console.log(filters);
		
		var fieldverbosenames = []
		for (var n in filters.fields_verbosenames) 
			fieldverbosenames[filters.fields_verbosenames[n]] = n;
		//console.log(fieldverbosenames);
		
		for (var i in inputparam) { //filters.filters_default) {
			//console.log(inputparam[i]);
			var value = '';
			for (var j in filters.filters_types[inputparam[i][2]]) 
				if (filters.filters_types[inputparam[i][2]][j][0] == inputparam[i][1]) {
					value = filters.filters_types[inputparam[i][2]][j][1];
					break;
				}
			
			store_from.add({
				field	:	fieldverbosenames[inputparam[i][0]],//inputparam[i][0],//filters.filters_default[i][0],
				filter	:	value,//inputparam[i][1],//filters.filters_default[i][1],
				value	:	inputparam[i][3],//filters.filters_default[i][3],
				filter_type : inputparam[i][2],//filters.filters_default[i][2],
			});
			store_from.commitChanges();
		}
	   // setTimeout(function(){
	   // 	grid_to.getView().refresh();
	   //store_from.load();
	   // },150);
	},
	
	deleteQuery: function() {
		var selectionNameCombo = Ext.getCmp('custom_datasets_combo');
		if (typeof selectionNameCombo.getRawValue() != 'undefined' 
			&& confirm('Soovid kustutada valikut "'+selectionNameCombo.getRawValue()+'"?')) {
			Ext.Ajax.request({
				url:'delete_custom_dataset',
				params: { name: selectionNameCombo.getRawValue(), //.getValue(), 
				},
				success: function(response) {
					show_message({message:'Kustutatud', success:true});
					
					for (var v in filters.filters_default) {
					store_from.add({
						field	:	inputparam[i][0],
						filter	:	inputparam[i][1],
						value	:	inputparam[i][3],
						filter_type : inputparam[i][2],
					});
					store_from.commitChanges();
					}
				    setTimeout(function(){
				    	grid_from.getView().refresh();
				    	//store_from.load();
				    },150);
				},
				failure: function(response) {
					show_message({message:'Kustutamine ebaõnnestus', error:true});
				},
			});
		} 
	},
	
	showAll: function() {
		var grid_to = Ext.getCmp('genericgrid');
		var store_to = grid_to.getStore();
		store_to.getProxy().extraParams.fp = '';
		store_to.getProxy().extraParams.myresults = '';
		//store_to.load();		
		if(!store_to.isLoading()) { 
			store_to.loadPage(1);
			//console.log('oo');
		}
		
		useFilters = false;
	},
	
	getQueryValues: function() {
		var grid_from = Ext.getCmp('genericfiltergrid');
		var store_from = grid_from.getStore().getRange();
		var queryValues = [];
		for(var i=0,totalRecords = store_from.length;i<totalRecords;i++) {
			 var row = store_from[i].data;
			 var row_filter = '';
			 var this_filter_type = filters.filters_types[row['filter_type']];
			 for(var j=0, totalFilters = this_filter_type.length;
			 		j<totalFilters;j++) {
				 if(this_filter_type[j][1] == row['filter'])
					 row_filter = this_filter_type[j][0];
			 }	 
		     queryValues.push([filters.fields_verbosenames[row['field']],row_filter,row['filter_type'],row['value']]);
		}
		return queryValues;
	},
	
	openPopup: function(settings) {
		childPopupWindow['addrecord'] = window.open('add','_blank',
    			'width='+(settings.popup.width?settings.popup.width:400)+
    			',height='+(settings.popup.height?settings.popup.height:500)+
    			',location=0,status=0,toolbar=0');
	},
	

	
 });