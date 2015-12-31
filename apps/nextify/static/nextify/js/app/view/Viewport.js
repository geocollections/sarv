/*
 * Sarv list view ExtJS definitions
 * 
 * TODO: Language support
 */

// 
//FilterFieldCombo
//

Ext.define('Sarv.view.element.FilterFieldCombo', {
	extend: 'Ext.form.field.ComboBox',
	xtype: 'filter-field-combo',
    valueField: 'name',
    displayField: 'name',
    alias: 'widget.filterfieldcombo',
    lazyRender:true,
    autoDestroy: true,
    valueNotFoundText: 'Value Not Found',
    store: Ext.create('Ext.data.ArrayStore', {
        fields:[{name:'name'},{name:'filter_type'}],
        data: Sarv.conf.fields 
    }),
    triggerAction: 'all',
    forceSelection: true,
    selectOnFocus: true,
	typeAhead: true,
	minChars: 0,
	mode: 'local'
});

//
// FilterGrid
//

Ext.define('Sarv.view.FilterGrid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.filtergrid',
    id: 'filtergrid',
    width: 383,
    autoHeight: true,
    scroll: false,
    viewConfig:{
        markDirty:false
    },
    autoDestroy: true,
    plugins: [
        Ext.create('Ext.grid.plugin.CellEditing', 
        	{clicksToEdit: 1})
    ],
    store: Ext.create('Ext.data.ArrayStore', {
        fields: [
            {name: 'field'},
        	{name: 'filter'},
        	{name: 'filter_type'},
        	{name: 'filter_default_num'},
        	{name: 'value'}
        ],
        data: Sarv.conf.filters_default
    }),
    columns: [{
        text: 'Field',
        dataIndex: 'field',
        width: 161,
        sortable: false,
        hideable: false,
        editor: 'filterfieldcombo',
    },{
        text: 'Filter',
        dataIndex: 'filter',
        width: 111,
        sortable: false,
        hideable: false,
        getEditor: function(record, defaultField) {  
    	    var filter_types = Sarv.conf.filters_types,
    	    	filter_type = record.get('filter_type'),
    	    	s = Ext.create('Ext.data.ArrayStore', {
    	    		autoLoad: true,
    	    		autoDestroy: true,
    	    		fields:[{name:'filtername'},
    	    		        {name:'filtervalue'}],
    	    		data: filter_types[ filter_type ],
    	    	}),
    	    	cb = Ext.create('Ext.form.field.ComboBox', { 
    	    		valueField: 'filtervalue',
    	    		displayField: 'filtervalue',
    	    		store: s
    	    	});
    	    return Ext.create('Ext.grid.CellEditor', {field: cb}); 
        }
    },{  
        dataIndex: 'filter_type',
        hidden: true,
        hideable: false,
	},{
        text: 'Value',
        dataIndex: 'value',
        width: 111,
        sortable: false,
   		hideable: false,
   		editor: {
   			xtype: 'textfield',
   			itemId: 'sarv-filter-editor',
       	}
   	}]
});

//
// Filter Grid savedset button column
//

Ext.define("Sarv.grid.column.Boolean", {
	extend: 'Ext.grid.column.Boolean',
	xtype: 'sarv-booleancolumn',
	renderer: function(value) {
		return "<input type='checkbox'" + (value ? "checked='checked'" : "") + ">";
	}
});

//
// FilterAdd 
// Optimizable: Extend from FilterGrid to reduce overhead
//

Ext.define('Sarv.view.FilterAdd', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.filteradd',
    id: 'filteradd',
    plugins: [Ext.create('Ext.grid.plugin.CellEditing', 
    	{clicksToEdit: 1})],
    hideHeaders: true,
    width: 383,
    autoHeight: true,
    scroll: false,
    viewConfig:{
        markDirty:false
    },
    store: Ext.create('Ext.data.ArrayStore', {
    	fields: [
    	    {name: 'field'},
        	{name: 'filter'},
        	{name: 'filter_type'},
        	{name: 'filter_default_num'},
        	{name: 'value'}
        ],
        data: [['Vali väli','','','']]
    }),
    columns: [{
        sortable: false,
        dataIndex: 'field',
        width: 161,
        editor: new Ext.form.field.ComboBox({
        	autoDestroy: true,
	  		displayField: 'name',
	  		valueField: 'name',
	  		itemId: 'filter-type-editor',
	  		store: Ext.create('Ext.data.ArrayStore', {
	  			fields: [{name:'name'}, {name:'filter_type'}],
	  			data: Sarv.conf.fields 
  			}),
  			triggerAction: 'all',
  			forceSelection: true,
  			emptyText: 'Vali väli',
  		    selectOnFocus: true,
  			typeAhead: true,
  			minChars: 0,
  			mode: 'local'
  		})
   	},{
   		sortable: false,
        id: 'filter_combo',
        dataIndex: 'filter',
        width: 111,
        sortable: false,
        hideable: false,
        getEditor: function(rec) {
    	    if(rec.get('filter_type')=='') 
    	    	return false;
    	    var filter_types = Sarv.conf.filters_types,
    	    	ft = rec.get('filter_type'),            	  
    	    	s = Ext.create('Ext.data.ArrayStore', {
    	    			autoLoad:true,
    	    			fields:[{name:'filtername'},
    	    			        {name:'filtervalue'}],
    	    			data: filter_types[ ft ]
    	    	}),
    	    	cb = Ext.create('Ext.form.field.ComboBox',{ 
	    		  		valueField: 'filtervalue',
	    		  		displayField: 'filtervalue',
	    		  		store: s
	    	    });
    	    return Ext.create('Ext.grid.CellEditor', 
    	    		{field: cb}); 
        }
   	},{ 
   		sortable: false,
   		hideable: false,
   		width: 111,
   		dataIndex: 'value',
   		getEditor: function(rec) {
   			if(rec.get('filter_type') != "") {
   				return {
   					xtype: 'textfield',
   					itemId: 'filter-value-editor'
   				};
   			}
   		}
   	}]
});

//
// FilterMenu
//

Ext.define('Sarv.view.FilterMenu', {
	extend: 'Ext.toolbar.Toolbar',
	alias: 'widget.filtermenu',
	items: [{
        text: 'Eemalda filter',
        itemId: 'btn-filter-remove',
        scope: this
    },'->',{
    	xtype: 'fieldcontainer',
    	defaultType: 'radiofield',
    	layout: 'hbox',
    	items: [{
    		boxLabel: 'Minu kirjed',
    		name: 'sarv-filter-type',
    		inputValue: 'my',
    		itemId: 'btn-list-showmy',
    		margin: '-4 10 0 0'
    	},{
    		boxLabel: 'Näita kõiki',
    		name: 'sarv-filter-type',
    		inputValue: null,
    		itemId: 'btn-list-showall',
    		margin: '-4 10 0 0',
    		checked: true
    	},{
    		boxLabel: 'Muu',
    		name: 'sarv-filter-type',
    		inputValue: null,
    		readOnly: true,
    		itemId: 'btn-list-other',
    		margin: '-4 10 0 0',
    		checked: false
    	}]
    },{
    	text: 'Filtreeri',
    	itemId: 'btn-list-filter',
    	iconCls: 'search'
    }]
});

//
// SavedSetMenu
//

Ext.define('Sarv.view.SavedSetMenu',{
	extend: 'Ext.toolbar.Toolbar',
	alias: 'widget.savedsetmenu',
	items: [{
    	xtype: 'combo',
    	id: 'custom_filtersets_combo',
    	name: 'custom_filtersets_combo',
		displayField: 'name',
		valueField: 'params',
		queryMode: 'remote',
		multiSelect: false,
		autoSelect: false,
		matchFieldWidth: false,
    	store: Ext.create('Ext.data.Store', {
  			autoLoad:true,
  			fields:['name','params'],
        	proxy: {
		        type: 'ajax',
		        autoLoad: true,
		        url: 'get_custom_filtersets',
		        reader: {
		        	type: 'json',
		            root: 'data',
		            totalProperty: 'store_record_count',
		        }
        	}
		}),
    	pageSize: 10
    },'->',{
    	text: 'Salvesta',
    	itemId: 'custom_filtersets_set',
    	tooltip: 'Salvesta päring',
    	iconCls: 'page-save'
    },{
    	text: 'Kustuta',
    	itemId: 'custom_filtersets_delete',
    	tooltip: 'Kustuta päring',
    	iconCls: 'page-delete'
    }]
});

// 
// GridStore
//

Ext.define('Sarv.store.GridStore', {
    extend: 'Ext.data.Store',
    xtype: 'gridstore',
    autoDestroy: true,
    autoLoad: false,
    remoteSort: true,
    buffered: false,
    constructor: function (conf) {
    	var c = Sarv.conf.records;
    	this.fields = c.fields;
    	this.pageSize = 'undefined' === typeof 
    		c.settings.pageSize ? 
    		30 : c.settings.pageSize,
    	c=null;
    	this.initConfig(conf);
    	this.callParent(arguments);
    },
    proxy: {
    	actionMethods: {
            create: 'GET',
            read: 'GET',
            update: 'GET',
            destroy: 'GET',
        },
        type: 'ajax',
        url: 'everything',
        reader: {
            type: 'array',
            totalProperty: 'records.n',
            root: 'records.d'
        }
    },
    listeners: {
    	load: function(s) {
    		try {
    			var d = s.proxy.reader.jsonData,
    				r = Sarv.records,
    				lc = s.lastOptions;
    			r.g = d.grids;
    			r.d = d.records.d;
    			r.f = d.records.f;
    			Sarv.form.list_store={
    				pageSize: s.pageSize,
    				offset: lc.start,
    				total: s.totalCount
    			}
    		} catch(e) {
    			console.log(e);
    		}	
			var t=['records','grids','rsl'], 
				errors=[],
				success=[];
			for(var i=t.length;i--;) {
    			if('undefined' !== typeof d[t[i]]
    			&& 'undefined' !== typeof d[t[i]].msg) {
    				var m=d[t[i]].msg,
    					k=Object.keys(m);
    				for(var j=k.length;j--;) {
    					if(k[j] == 'error')
        					errors=errors.concat(m.error);
    				}
    			}
			}
			if(errors.length > 0)
				Sarv.message({
					error: true,
					message: 'Errors occurred while retrieving data',
					data: errors
				});
			if(success.length > 0) {
				Sarv.message({
					success: true,
					data: success
				})
			}
    	}
    }
});

//
// ListGrid
//

Ext.define('Sarv.view.ListGrid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.listgrid',
    id:'listgrid',
    constructor: function() {
    	this.columns = Sarv.conf.records.columns;
    	this.store = Ext.create('Sarv.store.GridStore', {
    		xtype: 'gridstore'
    	});
    	this.dockedItems = [{
            xtype: 'pagingtoolbar',
            store: this.store,
            dock: 'bottom',
            displayInfo: true,
            viewConfig: { 
            	loadMask: true 
            }
        }]; 	
    	this.initConfig();
    	this.callParent(arguments);
    }    
});

//
// Viewport
//

Ext.define('Sarv.view.Viewport', {
    extend: 'Ext.container.Viewport',
    xtype: 'sarv-viewport',
    requires: [
        'Sarv.view.element.FilterFieldCombo',
        'Sarv.view.FilterGrid',
        'Sarv.view.FilterAdd',
        'Sarv.view.FilterMenu',
        'Sarv.view.SavedSetMenu',
        'Sarv.view.ListGrid'
    ],
    layout: 'border',
    items:[{
   		title: 'Filtrid',
   		region: 'west',
   		itemId: 'filtrid',
   		width:383,
   		scroll: false,
   		collapsible: true,        		
   		items: [
   		    { xtype: 'filtergrid' },
   		    { xtype: 'filteradd' },
   		    { xtype: 'filtermenu' },
   		    {
   		    	title: 'Salvestatud päringud',
		        border: 0,
		        items: [{ xtype: 'savedsetmenu' }]
   		    },{
   		    	title: 'Valikud'
   		    },{
   		    	xtype: 'toolbar',
   		    	items:[{
					xtype: 'combo',
					id: 'combo-custom_dataset',
					name: 'combo-custom_dataset',
					displayField: 'display',//'value',
					valueField: 'name',
					queryMode: 'remote',
					multiSelect: false,
					autoDestroy: true,
					autoSelect: false,
					minChars: 1,
					matchFieldWidth: false,
					pageSize: 10,
					enableKeyEvents: true,
					store: Ext.create('Ext.data.Store', {
					  	autoLoad: false,
					  	fields:['name','value',
					  	    {
					  	        name: 'display',
					  	        mapping: 'value',
					  	        convert: function(v, record) {
					  	            return v + ' ('+record.data.name+')';
					  	        }
					  	    }        
					  	],
					    proxy: {
				    		type: 'ajax',
				    		autoLoad: false,
				    		url: 'get_custom_datasets',
				    		reader: {
				    			type: 'json',
				    		    root: 'd',
				    		    totalProperty: 'n'
				    		}
					    }
					})
					
				},'->',{
					xtype: 'button',
					name: 'btn-custom_dataset-show',
					id: 'btn-custom_dataset-show',
					text: 'Näita'
				},{
					xtype: 'button',
					name: 'btn-custom_dataset-addto',
					itemId: 'btn-custom_dataset-addto',
					text: 'Lisa valikusse'
				},{
					xtype: 'button',
					name: 'btn-custom_dataset-delete',
					itemId: 'btn-custom_dataset-delete',
					text: 'Kustuta'
				}]
   		    },{
		        title: 'Funktsioonid',
		        items: [{
		            xtype: 'button',
		            itemId: 'btn-form-add', 
		    		text: 'Lisa uus kirje',
		    		iconCls: 'page-add', 
		    		hidden: true
		    	}]
   		    }]
    },{ 
		xtype: 'listgrid',
    	region: 'center',
    	collapsible: false
    }]
});
