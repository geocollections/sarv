Ext.define('SarvForm.view.field.ComboField', {
	extend: 'Ext.form.field.ComboBox',
	xtype: 'sarv-field-combo',
	sarv: {
		link: null,		// if combobox is a link
		href: false, 	// link url
		defaults: null,	// set default values to combobox
		store_model: null, // lowercased model number used in store name
		store_name: null,
		pageSize: 10,
		isTyped: false, // distinction flag (typeahead vs setlabel) in event handling
	},
	labelAlign : 'right',
	multiSelect: false,
	autoSelect: false,
    selectOnFocus: true,
	typeAhead: true,
	minChars: 0,
	matchFieldWidth: false,
	autoDestroy: true,
	displayField: 'value',
	valueField: 'name',
	//pageSize: this.sarv.pageSize,
	queryMode: 'local',
	constructor: function(conf) {
		this.sarvConstructor(conf);
		this.initConfig(conf);
		this.callParent([conf]);
		
	},
	sarvConstructor: function(conf) {
		
		// set pagesize
		conf.sarv.pageSize = (conf.sarv.pageSize||10);
		conf.pageSize = conf.sarv.pageSize;
		var t_=this,
			pre='';

		if('undefined' !== typeof conf.column) {
			pre=conf.column.up('sarv-grid-panel').name+'__';
		}
		t_.sarv.store_name=pre+conf.name;
		conf['store'] = Ext.create('Ext.data.ArrayStore', {
			storeId: conf.sarv.store_model,
			fields:['name','value'],
			pageSize: t_.sarv.pageSize,
			proxy:{
				enablePaging: true,
				type: 'memory',
				reader:{
					type:'array',
					root:'data'
				}
			},
			data: SarvForm.conf
				.stores.data[
				     t_.sarv.store_name //conf.sarv.store_model
				]['d'],
			
			// override loadRawData. Goes with change event
			// for _filtering_ (typeforward) 
			// http://www.sencha.com/forum/showthread.php?152216-Ext.data.Store.loadRawData-does-not-set-total-property
			
			loadRawData: function(data, append){
		        var r=this.proxy.reader.read(data),
		        	th_=this;
		        if (r.success) {
		        	th_.currentPage=1;
		            th_.totalCount=r.total;
		            th_.pageSize=t_.sarv.pageSize;
		            th_.proxy.data=r.records; // added
		            //th_.loadRecords(
		            //	r.records.splice(0, t_.sarv.pageSize),
		            //	{addRecords: append}); // added splice
		            th_.sync();
		            th_.load();
		            //th_.fireEvent('load', th_, r.records, true);
		        }
			},
			
			listeners: {
				// Set display value.
				// Mainly for paging.
				// Disabled for filtering load
 				load: function() {
 					try {
	 					if(arguments[1].length > 0 
	 					&& !t_.sarv.isTyped) {
	 						t_.setValue(t_.sarv.defaults[1]);
	 					}
 					} catch(e) {}
 					try {
 						t_.setPickerWidth();
 					} catch(e) {console.log(e);}
				}
			}
		});
	},
	
	// setLabel - turns the correct 
	// page of combo dropdown. This
	// allows displayfield to be shown
	// instead of valuefield.
	
	// Remote store uses other approach
	// Default value is given with data
	setLabel: function() {
		// * Roweditor hack
		var p=this.up('sarv-grid-panel');
		if('undefined' !== typeof p 
		&& 'undefined' !== p.editingPlugin.tmpValue) {
			this.value=p.editingPlugin.tmpValue;
		}
		// * If combofield is empty
		if(this.value==null)
			return;
		
		var kc=(isNaN(this.value))?1:0;
				
		pre='';
		if('undefined' !== typeof this.column) {
			pre=this.column.up('sarv-grid-panel').name+'__';
		}
				
		var d=SarvForm.conf.stores.data[
		        pre+this.name].d,
			n=d.length,
			ps=this.sarv.pageSize;
		
		// Find the correct page
		for(var i=0;i<n;i++) {
			if(d[i][kc] == this.value) {
				this.sarv.defaults=d[i];
				var z = Math.floor(((i)-(i)%ps)/ps);
				// not a filtering process 
				// (no text is entered to combobox input
				// field by the user)
				this.sarv.isTyped=false;
				
				this.store.loadPage(z+1);
			}
		}
	},
	
	// To resolve hiding the pager
	// when list width is smaller
	// than the pager width
	setPickerWidth: function() {
		try {
			var w=this.picker.getWidth();
			if(w < 250) {
				this.picker.setWidth(250);
			}
		} catch(e){}
	},
	
	listeners: {
		//afterrender: function(cb){
			//if('undefined' !== typeof cb.column) {
				
		//		cb.setFieldStyle('background-color: #ffb; background-image: none;');
		//	}
		//},
		focus: function(cb){
			cb.setLabel();
		},
		
		expand: function(cb){
			try{
				this.setPickerWidth();
			}catch(e){
				console.log(e);
			}
		},
					
		blur: function(cb) {
			var pre='';
			if('undefined' !== typeof cb.column) {
				pre=cb.column.up('sarv-grid-panel').name+'__';
			}
			cb.sarv.store_name=pre+cb.name;
			
			//when local combobox is blurred
			//restore original state
			// - restore array of combobox array
			// - set value
			// - set page of picker
			if(this.sarv.isTyped ) {
            //&& cb.value != "") {
				var d=SarvForm.conf
						.stores.data[
						    cb.sarv.store_name
						]['d'],
					d_=[];
				
				for(var i=d.length;i--;) {
					d_.push(d[i]);
				}
				d_.reverse();
                if(cb.value != "")
				    this.setValue(this.sarv.defaults[1]);
				cb.store.loadRawData(d_, false);
				this.setLabel();
				this.sarv.isTyped=false;
			}
		},
		
		// select - When a value is selected 
		// from dropdown, set it to be default 
		// value for combo.
		select: function() {
			var tpld=this.displayTplData[0];
			this.sarv.defaults=[
			    tpld['name'], 
			    tpld['value']
			];
			var p=this.up('sarv-grid-panel');
			if('undefined' !== typeof p)
				p.editingPlugin.tmpValue=tpld['value'];

			// Local store events
			// Remove filtered store dataset
			if(this.sarv.isTyped) {
				var d=SarvForm.conf
					.stores.data[this.sarv.store_name//model
					    ]['d'];
				this.store.clearFilter();
				this.store.loadRawData(d, false);
				this.setLabel();
			}
			this.sarv.isTyped = false;
		},
		
		keypress: function(cb) {
			cb.sarv.isTyped=true;
		},
		
		// keyup - For typeAhead filtering
		// Therefore other change triggers 
		// should be disabled otherwise
		change: function(cb,v,ov){
			if(!cb.sarv.isTyped) 
				return;
			
			var pre='';
			if('undefined' !== typeof cb.column) {
				pre=cb.column.up('sarv-grid-panel').name+'__';
			}
			cb.sarv.store_name=pre+cb.name;
			
			var d=SarvForm.conf
					.stores.data[
					     cb.sarv.store_name //model
					]['d'],
				d_=[];
			if(String(v)&&v.length>0) {
				var x=new RegExp('^'+v, 'i');
				for(var i=0,n=d.length;i<n;i++)
					if(x.test(d[i][1])) {
						d_.push(d[i]);
					}
			} 
			cb.store.loadRawData(d_.length<1?d:d_, false);
			if (d_.length > 0 || d.length > 0)
				cb.expand();
			d_=null;
		}
		
	},
	// enableKeyEvents - allows keyup listener
	enableKeyEvents: true
});
