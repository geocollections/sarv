Ext.define('SarvForm.controller.Record', {
    extend: 'Ext.app.Controller'
    
    , refs: [{
    		ref:'RecordPage',
    		selector:'record-page',
    	},
    	{
    		ref:'RecordForm',
    		selector:'record-form',
    }]

	, gridState: null
	
    , init: function() {
    	// EVENT LISTENERS //
    	this.control({
    		
    		// "LOADING"
    		'viewport': {     			
    			afterrender: function() {
					document
						.getElementById('page-loader-mask')
						.style.display ='none';
    			}
    		},

    		// FORM
    		'record-form': {
    			// form available only after page load
    			afterrender: function() {
    				// If url contains 'add' not record id
    				// call add
    				if(SarvForm.conf.url_end != 'add') {
    					this.setPageData();
    				} else {
    					this.add();
    				}
    			}
    		},
    		
    		// COMBOBOXES
    		'sarv-field-combo, sarv-field-combo-remote': {
    			// Go to page where selected value is
    			beforedestroy: function(e) {
    				e.store.destroyStore();
    			}
    		},
    		
    		
    		// FILE
    		'sarv-file': {
    			afterrender: function(f) {
    				//attach custom event listeners to the mix
    				// põhim vaja 
    				var tc_=this,
    					holder=document
    						.getElementById(
    						f.name+'-dd-dropzone'),
    					inf=holder
    						.getElementsByClassName(
    						'dd-file-name')[0];
    				
    				f.txt={
    					'file-upload-confirm': 'Kas laen faili üles?',
    					'file-upload-done': 'Fail laetud',
    					'file-upload-failed': 'Faili üleslaadimine ebaõnnestus'
    				};
    				
    				f.readFile=function(i) {
    					var t_=this;
    					document.getElementById(t_.id).value = i.name;
    					var reader = new FileReader();
    					reader.onload = function(e) {
    					    t_.setValue(document.getElementById(t_.id).value);
    					}
    					reader.readAsDataURL(i);
    				};
    				
    				holder.ondragover = function (b) {
    					b.preventDefault();
    					return false; 
    				};
    				holder.ondragend = function () {
    					return false; 
    				};
    				
    				holder.ondrop = function (e) {
    					e.preventDefault();
    					var t_=this,
    						c=SarvForm.conf;
    					
    					// If it is update not add 
    					// then confirm and then upload
    					// Otherwise upload on form submit
    					if('undefined' === typeof c.item_id 
    					|| isNaN(c.item_id) 
    					|| c.item_id==null) {
    						c.temp_file=null;
    					    c.temp_file=e.dataTransfer.files[0];
    					    f.readFile(c.temp_file);
    					} else {
    						try{
    							c.temp_file=e.dataTransfer.files[0];
    						}catch(e){
    							console.log(e);
    							return;
    						}
    						if(confirm(f.txt['file-upload-confirm'])) {
    							
    							var fd = new FormData();
    							fd.append('id', c.item_id);
    							fd.append('fieldname', f.name);
    							fd.append(f.name+'-file', 
    								c.temp_file);
    							
    							// * new XHR request
    							var xhr = new XMLHttpRequest(),
    								el=document.getElementById(t_.id)
    									.getElementsByClassName('dd-prgr')[0];
    							
    							// * Progress bar
    							xhr.upload.addEventListener("progress", 
    								function(e) {
    									var a_=e.loaded/e.total*30;
    									el.style.width = a_+'px';
    								}, false);
    													
    							xhr.open('POST', 'set_file');
    							xhr.onload = function () {
    								var m=JSON.parse(this.response);
    								
    								// * remove progress bar
    								el.style.width='0px';
    									
    							    if (xhr.status === 200 
    							    && m.errors.length < 1) {
    								    SarvForm.message({
    								    	success:true,
    								    	message: f.txt['file-upload-done']
    								    });
    								    
    								    var updateFormData = function(){
    								    	try{
								    		f.setValue(c.temp_file.name);
								    		var fhashed=f.file.fieldname_hashed;
								    		if('undefined' !== typeof fhashed
								    		&& 'undefined' !== typeof m.data.hash) {
				    							var form=f.up('record-form').getForm(),
				    								hf=form.findField(fhashed),
				    								el=document.getElementById(f.id)
				    									.getElementsByClassName('dd-icon')[0];
				    							
				    							el.dataset.filename=c.temp_file.name;
				    							if('undefined' !== typeof hf &&
				    							hf != null)
				    								hf.setValue(m.data.hash);
								    		};
    								    	}catch(e){console.log(e);}
    								    };
    								    try{
								    	    SarvForm.given._refreshGrid();
								    	    updateFormData();
    								    }catch(e){
    								    	updateFormData();
    								    }
    							    } else {
    							        SarvForm.message({
    							        	error:true, 
    							        	message: f.txt['file-upload-failed'],
    							        	data: m.errors
    							        });
    							    }
    							};
    							xhr.send(fd);
    						};
    					}
    				}
    			}
    		},
    		
    		// GRIDS
    		'#grid-btn-add-row': {
    			click: this.gridAddEmptyRow
    		},
    		'#grid-btn-delete-row': {
    			click: this.gridDeleteRow
    		},
    		
    		'sarv-grid-panel': {
    			edit: {
    				scope: this,
    				fn: this.gridSetRow
    			} 
    		},
    		
    		// GRID CELLEDITING 
    		'sarv-grid-panel sarv-field-combo, sarv-grid-panel sarv-field-combo-remote': {
    			afterrender: function(cb) {
    				this.setUrlCombo(cb);
    			},
    			focus: function(cb){
    				this.setUrlCombo(cb);
    			},
    			show: function(cb){
    				this.setUrlCombo(cb);
    			}
    		},
    		
    		// GRID COMBOBOXES
    		'sarv-field-combo, sarv-grid-panel sarv-field-combo-remote': { 
    			// Change store page position to 
    			// get right displayvalue
    			focus: function() {
    				var cb=arguments[0];
    				cb.setLabel();
    			},
    			afterrender: function(cb) { // was: afterrender
    				if('undefined' !== typeof cb.up('sarv-grid-panel'))
    					cb.setLabel();
    			}
    		}
    	});
    }

	// METHODS

	, setButtons: function (data) {
		// Salvesta | Uus | Kustuta | Salvesta uue kirjena
		// data = ['<button key:add/save/..>':{enabled:<T/F>},] 
		// if 'cancel', specify return_id in data
		var data=(data||{}),
			pane=this.getRecordPage().items.items[0],
			pr='item-',
			buttons = {
	        	'add': 		{ itemId: pr+'add', iconCls: 'page-add', handler: this.add, 
	        					text: 'Uus', scope: this },
	        	'save':		{ itemId: pr+'save', iconCls:'page-save', handler: this.save, 
	        					text: 'Salvesta', scope: this},
	        	'save-as': 	{ itemId: pr+'save-as', iconCls:'page-save-as', handler: this.saveAs, 
	        					text: 'Salvesta uuena', scope: this},
	        	'cancel': 	{ itemId: pr+'cancel', iconCls: 'page-cancel', handler: this.cancel, 
	        					text: 'Tühista', scope: this },
	        	'delete': 	{ itemId: pr+'delete', iconCls: 'page-delete', handler: this.del, 
	        					scope: this},
	        	'prev': 	{ itemId: pr+'previous', iconCls: 'previous', handler: this.navigator, 
	        					scope: this },
	        	'next': 	{ itemId: pr+'next', iconCls: 'next', handler: this.navigator, 
	        					scope: this }
	    	},
	    	b=[];
		pane.removeAll();
		var sa = false;
		var getButton=function(d) {
			for(var i in d) {
				if (d[i].enabled == false)
					buttons[i].disabled = true;
				if ('undefined' !== typeof d[i].return_id)
					buttons[i].return_id = d[i].return_id;
				if ('undefined' !== typeof d[i].past)
					buttons[i].past = d[i].past;
                if(i == "save-as")
                    sa = Ext.create("SarvForm.view.toolbar.Button", buttons[i]);
                else
				    b.push(Ext.create('SarvForm.view.toolbar.Button', buttons[i]));
			}
		}
		
		if(Object.prototype.toString.call(data) === '[object Array]') {
			for(var i=0,n=data.length;i<n;i++) {
				getButton(data[i]);
			}
		} else {
			getButton(data);
		}

        if(sa) {
		    pane.add([{layout:"hbox",
                items:[
                    {items: b, border: 0},
                    {xtype: "tbspacer", flex:1, border: 0},
                    {items: sa, border: 0}
                ], 
                border: 0
            }]);
        } else 
            pane.add(b);
		
		this.setEnabledButtons();
	}
	
	, setEnabledButtons: function() {
		var c = SarvForm.conf,
			f = this.getRecordForm().getForm().getFields().items,
			f_l = [];
	
		for (var i=f.length;i--;) 
			f_l[f[i].name] = f[i].value;
		var user_added = ('user_created' in f_l) ? f_l['user_created'] : 
							(('user_added' in f_l) ? f_l['user_added'] : false),
			user_changed = ('user_modified' in f_l) ? f_l['user_modified'] :
							(('user_changed' in f_l) ? f_l['user_changed'] : false),
			is_owner = ('number' === typeof c.owner_id 
						&& c.user.id == c.owner_id),
			ids = ['item-save-as','item-add','item-save','item-delete'], n=ids.length,
			cmps = {};
		for (var i=n;i--;)
			cmps[ids[i]] = Ext.getCmp(ids[i]); 
		
		if (c.acl[1]) {
			if (cmps['item-save-as'])
				Ext.getCmp('item-save-as').setDisabled(false);
			if (cmps['item-add'])
				Ext.getCmp('item-add').setDisabled(false);
            if(cmps['item-delete'])
                Ext.getCmp('item-delete').setDisabled(false);
		} else {
			if (cmps['item-save-as'])
				Ext.getCmp('item-save-as').setDisabled(true);
			if (cmps['item-add'])
				Ext.getCmp('item-add').setDisabled(true);
            if(cmps['item-delete'])
                Ext.getCmp('item-delete').setDisabled(false);
		}
		    	
		if (c.acl[2] || c.url_end == 'add' 
			|| (c.acl[2] == 'own' 
				&& (c.user.name === user_added || c.user.name === user_changed))
			|| is_owner
		) {
			if (cmps['item-save']) 
				Ext.getCmp('item-save').setDisabled(false);
		} else {
			if (cmps['item-save']) 
				Ext.getCmp('item-save').setDisabled(true);
		}
		 
		if (c.acl[3] 
			|| (c.acl[3] == 'own' 
				&& (c.user.name == user_added || c.user.name == user_changed))
			|| is_owner
			) {
			if (cmps['item-delete']) Ext.getCmp('item-delete').setDisabled(false);
		} else {
			if (cmps['item-delete']) Ext.getCmp('item-delete').setDisabled(true);
		}
		
		c=null;
	}
	
	// FILL FORM WITH RECORD DATA
	// Record is identified with index
	// referenced by {SarvForm.conf.i}
	, setPageData: function () {
		var r=SarvForm.given.records.d[
		        SarvForm.conf.i],
			c=SarvForm.conf,
			f=SarvForm.given.records.f,
			fv={},
			rf=this.getRecordForm(),
			fo=rf.getForm(),
			t=SarvForm.conf.title;
		// Do not update layout on every value update
		var rp=this.getRecordPage();
		rp.suspendLayouts();
		
		
		for(var i=f.length;i--;)
			fv[f[i]]=r[i];
		
		// * Page title
		if('undefined' !== typeof t) {
			var rep=/{{(.+?)}}+?/g,
				m_l=t.match(rep);
			document.title=t;
			for(var i=m_l.length;i--;) {
				var fn=m_l[i].replace('{{','')
							.replace('}}',''),
					cI=f.indexOf(fn),
					v=cI!==-1?r[cI]:'..';
				document.title=document.title.replace(m_l[i], v);
			}
		} else {
			document.title='Form';
		}

		// * item_id
		c.item_id=r[f.indexOf('id')];
		
		// * owner_id
		if(this.d(fv['owner_id'])) {
			c.owner_id = fv['owner_id'];
			delete fv['owner_id'];
		} else
			c.owner_id = false;
		
		// * Edited fields flag
		c.edited = false;
		// * form items
		try {
			fo.setValues(fv);
		} catch (e) {
			console.log (e);
		}
		// * radio fields
		var ra = rf.query("[xtype='sarv-field-radio']");
		for(var i=ra.length;i--;) {
			for(var ii=ra[i].items.items.length;ii--;) {
				var j=ra[i].items.items[ii],
					is_selected = 
						j.inputValue == fv[ra[i].name]
	    				|| (String(j.inputValue).toLowerCase() == 'none' &&
	    					String(fv[ra[i].name]) == 'null');
				
	    		ra[i].items.items[ii].setValue(is_selected);
			}
		}
		
		// * Checkboxes
		var cb = rf.query("[xtype='checkbox']");
		for(var i in cb) 
			cb[i].setValue((fv[cb[i].name]==true));
		
		// * Parent (optional)
		var btn = Ext.getCmp('parent_url_btn');
		if('undefined' !== typeof btn) {
			if('undefined' === typeof fv['parent_url_val']) 
		    	btn.hide(); 
			else 
				btn.show(); 
		}

		// * Show grids and tab panels with grids
    	var g_l=rf.query('sarv-grid-panel');
    	for(var i=g_l.length;i--;) {
    		var t=g_l[i].up('sarv-tab');
    		if('undefined' !== typeof t) {
    			t.show();
    		} else {
    			g_l[i].show();
    		}
    	}
		
		// * Get active grid
		var t=rf.query('sarv-tab'),
			_g=[]; // for the next query 
		for(var j=t.length;j--;) {
			this.setGridTabStyle(t[j]);
			
			var g=t[j].getActiveTab(),//,
				d=SarvForm.given._getGridData(
						SarvForm.conf.item_id,
						g.name
					);
			g.store.loadRawData(d, false);
			_g.push(g.name);
		}
		
		var gr=rf.query('sarv-grid-panel');
		for(var j=gr.length;j--;) {
			if(_g.indexOf(gr[j].name) !== -1)
				continue;
			var d=SarvForm.given._getGridData(
					SarvForm.conf.item_id,
					gr[j].name
				);
			
			gr[j].store.loadRawData(d, false);
		}
		
		
		// * Combobox default values
		// In theory comboboxes need only to be refreshed
		var c = rf.query('sarv-field-combo');
		for(var i=c.length;i--;) {
			c[i].setLabel();
			this.setUrlCombo(c[i]);
		}
		
		// * Combobox default values
		// In theory comboboxes need only to be refreshed
		var c = rf.query('sarv-field-combo-remote');
		for(var i=c.length;i--;) {
console.log(c[i]);
			c[i].setLabel();
			this.setUrlCombo(c[i]);
		}	
		
		// * Enabled buttons
	   	this.setEnabledButtons();
	   	
	   	// * Change url bar
	   	try {
			
	   		var wl=window.location,
	   			p=wl.pathname.split('/')[1],
	   			iO=wl.href.indexOf('?'),
	   			qM=iO!==-1?wl.href.substring(iO,wl.href.length):'';
	   		window.history.pushState({},'ns',
	   			'/'+p+'/'+SarvForm.conf.item_id+qM);
	   		SarvForm.conf.url_end=SarvForm.conf.item_id;
	   	} catch(e) {console.log(e);}
	   	
	   	// * Add file icons to these fields
	   	var dd=rf.query('sarv-file');
	   	for(var j=dd.length;j--;){
	   		var ddf=fv[dd[j].name];
	   		if('undefined' !== typeof ddf
	   		&& ddf.length > 0) {
	   			var ext=ddf.split('.'),
	   				el=document.getElementById(dd[j].id)
	   					.getElementsByClassName('dd-icon')[0],
	   				ext_l=['pdf','jpg','png','gif','doc','xls','txt','tar.bz2','tar.gz'];
	   			
	   			if(ext.length > 2) {
	   				var ext_=ext[ext.length-2]+'.'+ext[ext.length-1];
	   				ext_=ext_.toLowerCase();
	   				if(ext_l.indexOf(ext_))
	   					ext[ext.length-1]=ext_;
	   			}
	   			
	   			el.removeEventListener('dblclick', 
	   					this.fileImageLink);
	   			//el.dataset.filename=null;
	   			el.dataset.fieldname=null;
	   			for(var k=ext_l.length;k--;) {
	   				var cln=ext_l[k].replace('.','-');
	   				if(el.classList.contains('img-'+cln)) {
	   					el.classList.remove('img-'+cln);
	   				}
	   			}
	   			if(ext.length > 1) {
	   				el.classList.add(
	   					'img-'+ext[ext.length-1].toLowerCase().replace('.','-'));
	   				el.addEventListener('dblclick', 
	   					this.fileImageLink);
	   				//el.dataset.filename=ddf;
	   				el.dataset.fieldname=dd[j].name;
	   			}
	   		} else {
	   			var cll=el.classList;
	   			for(var k=cll.length;k--;) {
	   				if(cll[k].indexOf('img-')) {
	   					el.classList.remove(cll[k]);
	   				}
	   			}
	   		}
	   	}
	   	
		// Set link url
		var urll=document.getElementById("urlAnchor");
		if(urll) {
			var eurl=urll.getAttribute('data-url');
			urll.href=eurl+'/'+SarvForm.conf.item_id;
			urll.innerHTML=urll.href;
		}
	   	
	   	rp.resumeLayouts();
	   	rp.doLayout();
	   	
	}
	
	, fileImageLink: function(e) {
		if('undefined' !== typeof 
		this.dataset.fieldname) {
			//var v = this.nextSibling.nextSibling.value;
			
			window.open([//'files',
				//this.dataset.fieldname, 
				//v
			    SarvForm.conf.item_id,
			    'files'
			].join('/'),
				'_parent', 'download');
		}
	}
		
	, setGridTabStyle: function(t) {
		var c=t.items.items,
			tb=t.tabBar.items.items,
			sf=SarvForm.given.records.g,
			id=SarvForm.conf.item_id;
		for(var i=c.length;i--;){
			if('undefined' !== typeof c[i].name 
			&& 'undefined' !== typeof sf[c[i].name] 
			&& 'undefined' !== typeof sf[c[i].name].m[id] 
			&& sf[c[i].name].m[id].length > 0) {
				tb[i].removeCls('has-no-records');
			} else {
				tb[i].addCls('has-no-records');
			}
		}
	}

	// NAVIGATION BETWEEN RECORDS
	// When prev or next button is clicked, 
	// load new data and update data accordingly
	// {e}: this.controller
	, navigator: function(e) {
		// * Local version doesn't have 
		// navigation
		if(SarvForm.isLocal)
			return;
		
    	var txt={
        		'error-logged-out':'Kirjetel liikumiseks peab veebisirvijas'+ 
    				'olema avatud kirjete tabeli aken',
    			'confirm-unsaved-changes':'Lehel on salvestamata uuendusi. Kas soovid jätkata?'
        	};
        var c=SarvForm.conf,
        	ls=c.list_store,
        	// * Position based on direction
        	x=c.i + (e.itemId == 'item-next'?1:(-1)),
        	t_=this; 
        // * Opener is missing. Can't function without it.
    	if(!SarvForm.isLocal && !opener) {
    		SarvForm.message({ 
    			message: txt['error-logged-out'], 
    			error: true, 
    		});
    		return;
    	}
    	// * There are unsaved changes
    	// [bug:] Rendering comboboxes (?) triggers c.edited
    	// so confirmation message is displayed even when
    	// no actual changes were made to form
    	//if (c.edited 
    	//&& !confirm(txt['confirm-unsaved-changes'])) 
    	//	return;
    	if(x == -1) {
    		// * Is not the first record
    		// * Turn the previous page
    		if(ls.offset != 0 
    		&& SarvForm.given._listGridPageTurner(-1, null, false, function(){
    			SarvForm.conf.i = ls.pageSize-1;
    	    	t_.setPageData();
    		}))
    			x = (ls.pageSize-1);
    		else
    			return;
    	// * Is the last record
    	} else if (ls.offset + x == ls.total) {
    		return;
    	// * Turn next page
    	} else if (x >= ls.pageSize) {
    		if(SarvForm.given._listGridPageTurner(1, null, false, function(){
    			SarvForm.conf.i = 0;
    	    	t_.setPageData();
    		}))
    			x = 0;
    		else
    			return;
    	} else {
    		// * Change the selected row
    		SarvForm.given._listGridPageTurner(null, x);
    		SarvForm.conf.i=x; // 14.12
    		this.setPageData(); // 14.12
    	}
    	//SarvForm.conf.i = x;
    	//this.setPageData();
	}
	
	// LOAD 'ADD RECORD' EMPTY FORM
    // Caller must have scope:this
	// {e} - this.controller
    , add: function(e) {
    	var txt={
    		'title-add-record':'Lisa uus kirje'
    	}
    	var f=this.getRecordForm(),
    		v=f.getValues();
    	// * Change page title
    	document.title = txt['title-add-record'];
    	// * Unset form field values
    	var fs=f.getForm().getFields().items;
    	for(var i=fs.length;i--;) {
    		fs[i].setValue();
    		fs[i].validate(); // added 8.10.14
    	}
    	
    	// * Remove grid data
    	var g_l=f.query('sarv-grid-panel');
    	for(var i=g_l.length;i--;) {
    		g_l[i].store.removeAll();
    		g_l[i].store.sync();
    		// * Hide tab panels with grids
    		var t=g_l[i].up('sarv-tab');
    		if('undefined' !== typeof t) {
    			t.hide();
    		} else {
    			g_l[i].hide();
    		}
    	}
    	    	    	
    	// * Set menu buttons
    	this.setButtons({
			cancel:{
				past: {
					i: SarvForm.conf.i,
					store: SarvForm.conf.list_store,
					id: SarvForm.conf.item_id
				}
			},
			save:{}
		});
		// * Remove references to any records 
		//   in parent grid and data 
		SarvForm.given.form.i = null;
		SarvForm.conf.item_id = null;
		
		if(!SarvForm.isLocal)
			SarvForm.given._listGridDeselectAll();
		
		// Set proper url
		try {
	   		var wl=window.location,
	   			p=wl.pathname.split('/')[1],
	   			iO=wl.href.indexOf('?'),
	   			qM=iO!==-1?wl.href.substring(iO,wl.href.length):'';
	   		window.history.pushState({},'ns',
	   			'/'+p+'/add'+qM);
	   		SarvForm.conf.url_end='add';
	   	} catch(e) {
	   		console.log(e);
	   	}
    }
    
    // DELETE RECORD
    
    , del: function(e) {
    	txt={
    		'confirm-delete-record':'Do you really want to delete this item?',
    		'error-record-not-deleted':'Kirjet ei kustutatud:'
    	};
    	//json request to .py | pass item id 
    	//if response ok, close window. otherwise message
    	if (confirm(txt['confirm-delete-record'])) {
    		Ext.Ajax.request({
                url: 'delete?id='+SarvForm.conf.item_id,
                success: function(r,a) {
                	var d = JSON.parse(r.responseText);
                	if(d.success) {
	                	if(!SarvForm.isLocal) 
	                		SarvForm.given._refreshGrid();
	                    window.close();
                	} else 
                		SarvForm.message({ 
                			message: txt['error-record-not-deleted'], 
                			error: true, 
                			data: d.errors
                		});
                }
            });
    	}
    }
        
    , save: function() {
    	var txt={
    		'error-form-not-valid':'Vormi väljade sisu ei vasta nõuetele',
    		'message-record-saved':'Kirje salvestatud',
    		'message-record-updated':'Kirje muudetud',
    		'error-on-save':'Kirje salvestamisel esines vigu:',
    		'error-double-ids':'Vormil tohib olla üks id väli. Võta ühendust süsteemihalduriga.'
    	};
    	var rf=this.getRecordForm(),
    		f=rf.getForm(), 
    		t_=this,
    		e_l=[];

    	// Check whether, typically because 
    	// id field is inserted in config.py
    	// there are two fields with key 'id'
    	// in form - this causes 'id' in post
    	// to become empty even when the
    	// record has id and is being updated.
    	var f_l=f.getFields().items,
    		isId=false;
    	
    	for(var i=f_l.length;i--;) {
    		if(f_l[i].name=='id')
    			if(!isId)
    				isId=true;
    			else
    				e_l.push(txt['error-double-ids']);
    	}    	
    	
    	if(!f.isValid()) {
    		// Get fields not valid
    		var if_=rf.getInvalidFields();
    		for(var j=if_.length;j--;) {
    			e_l.push(if_[j].fieldLabel);
    		}
    	}
    	
    	if(e_l.length > 0) {
    		SarvForm.message({
    			message: txt['error-form-not-valid'],
    			error: true,
    			data: e_l
    		});
    		return;
    	}
    	    	
    	var cf=rf.query('sarv-field-combo')
    			.concat(rf.query('sarv-field-combo-remote'));
    	
    	// Replace combofield textual values with keys
    	if(cf.length > 0) {
	    	var d=SarvForm.conf.stores.data;
    		for(var i=cf.length;i--;) {
	    		if('undefined' !== typeof cf[i].value
	    		&& cf[i].value != null
	    		&& isNaN(cf[i].value)
	    		&& cf[i].value.replace(" ","").length > 0) {
	    			if(cf[i].xtype=='sarv-field-combo') {
	    				var c_l=d[cf[i].name].d;//sarv.store_name].d;
	    				for(var j=c_l.length;j--;)
		    				if(c_l[j][1] == cf[i].value)
		    					cf[i].value = c_l[j][0];
	    			} else if(cf[i].xtype == 'sarv-field-combo-remote') {
	    				try {
	    					if(cf[i].value == cf[i].sarv.defaults[1])
	    						cf[i].value = cf[i].sarv.defaults[0];
	    				
	    				} catch (e) {}
	    			}
	    		}
	    	}
    	}
    	    	
    	f.submit({
    		params: {
    			get_page_by_id: (!SarvForm.isLocal) ? 
    				JSON.stringify(SarvForm.given._getFilterParams()) :
    				null
    		},
    		success: function(f, action) {
    			var result=action.result;
    			if('undefined' !== typeof result.isUpdate 
    			&& result.isUpdate) {
    				SarvForm.message({
    					message: txt['message-record-updated'],
    					success: true
    				})
    				SarvForm.given._refreshGrid();
    				return;
    			}
    				
    			if(SarvForm.isLocal)
    				window.location.replace(result.id);
    			var c = SarvForm.conf;
    			
    			if(result.id) {
    				//If files were in form, get them
    		    	var dd=rf.query('sarv-file');
    		    	if(dd.length > 0 
    		    	&& 'undefined' !== typeof SarvForm.conf.temp_file
    		    	&& SarvForm.conf.temp_file != null) {
    		    		var formData = new FormData();
						formData.append('id', 
							result.id);
						formData.append('fieldname',
							dd[0].name);
						formData.append(dd[0].name+'-file',
							SarvForm.conf.temp_file);
						
						var xhr = new XMLHttpRequest();
						xhr.open('POST', 'set_file');
						xhr.onload = function () {
							var m=JSON.parse(this.response);
							
							SarvForm.conf.temp_file=null;
							t_.postSaveActions(result);
						};
						xhr.send(formData);
    		    	} else {
    		    		t_.postSaveActions(result);
    		    	}
    			}
    		},	
    		failure: function(form, action) {
    			SarvForm.message({
    				message: txt['error-on-save'], 
    				error: true, 
    				data: action.result.errors, 
    			})
    		},
    	});
    }
    
    , postSaveActions: function(result) {
    	var t_=this,
    		rf=this.getRecordForm(),
    		f=rf.getForm(),
    		c=SarvForm.conf;
    	
    	var txt={
        		'error-form-not-valid':'Vormi väljade sisu ei vasta nõuetele',
        		'message-record-saved':'Kirje salvestatud',
        		'message-record-updated':'Kirje muudetud',
        		'error-on-save':'Kirje salvestamisel esines vigu:',
        		'error-double-ids':'Vormil tohib olla üks id väli. Võta ühendust süsteemihalduriga.'
        	};
		
    	SarvForm.message({ 
			message: txt['message-record-saved'], 
			success: true 
		});
	
		// * Load list grid on right page
		if(result.page) {
			SarvForm.given._listGridPageTurner(
				result.page, 
				null, true, function(){
					// Find index based on id 
					// (always the first item in record array)
					var d=SarvForm.given.records.d;
					for(var j=0,n=d.length;j<n;j++) {
						if(result.id == d[j][0]) {
							SarvForm.conf.i = j;
							break;
						}
					}
					if(c.url_end == 'add') {
						window.location = document.URL 
							.replace('add','').replace('?o','')+
							result.id+(opener?'?o':'');
					} else {
						t_.setPageData();
					}
				});
		} else {
			SarvForm.given._refreshGrid({
				fn: function() {
					if(c.url_end == 'add') {
						window.location = document.URL 
							.replace('add','').replace('?o','')+
							result.id+(opener?'?o':'');
					}
				}
			});
		}
		
		// * Set hidden values
		f.setValues({
			id_hidden: result.id,
			id: result.id
		});
		
		// * Set item id
		c.item_id = result.id;
		
		// * Set button pane
		t_.setButtons([
			{save: {}},
			{add: {}},
			{'delete': {}},
			{'save-as': {}},
			{prev: {}},
			{next: {}}
		]);    	
    }
    
    , saveAs: function() { 
    	var rf=this.getRecordForm(),
    		f=rf.getForm(), 
    		t_=this,
    		cf=rf.query('sarv-field-combo')
    			.concat(rf.query('sarv-field-combo-remote'));

    	// Replace combofield textual values with keys
		if(cf.length > 0) {
			var d=SarvForm.conf.stores.data;
			for(var i=cf.length;i--;) {
				if('undefined' !== typeof cf[i].value
				&& cf[i].value != null
				&& isNaN(cf[i].value)
				&& cf[i].value.replace(" ","").length > 0) {
					var sd_l = cf[i].sarv.defaults;
					if(cf[i].xtype=='sarv-field-combo') {
						var c_l=d[cf[i].name].d;
						for(var j=c_l.length;j--;)
		    				if(c_l[j][1] == cf[i].value)
		    					cf[i].value = c_l[j][0];
					} else if(cf[i].xtype == 'sarv-field-combo-remote') {
						try {
							if(cf[i].value == sd_l[1])
								cf[i].value = sd_l[0];
						} catch (e) {}
					}
				}
			}
		}
    	
    	f.submit({
    		params:{
    			saveAs: true,
    			get_page_by_id: (!SarvForm.isLocal) ? 
        			JSON.stringify(SarvForm.given._getFilterParams()) :
        			null
    		},
    		success: function(f, action) {
    			if (action.result.id) {
    				SarvForm.conf.item_id = action.result.id;
    				// ->
    				f.setValues({id:action.result.id});
    				// * Change url bar
    			   	try {
    			   		var wl=window.location,
    			   			p=wl.pathname.split('/')[1],
    			   			iO=wl.href.indexOf('?'),
    			   			qM=iO!==-1?wl.href.substring(iO,wl.href.length):'';
    			   		window.history.pushState({},'ns',
    			   			'/'+p+'/'+SarvForm.conf.item_id+qM);
    			   		SarvForm.conf.url_end=SarvForm.conf.item_id;
    			   	} catch(e) {console.log(e);}
    				
    				// <-
    				if(action.result.page)
    					SarvForm.given._listGridPageTurner(
    						action.result.page, 
    						null, true, function(){
    							var d=SarvForm.given.records.d;
    	    					for(var j=0,n=d.length;j<n;j++) {
    	    						if(action.result.id == d[j][0]) {
    	    							SarvForm.conf.i = j;
    	    							break;
    	    						}
    	    					}
    							t_.setPageData();
    						})
    			}
    			SarvForm.message({
    				message: 'Kirje salvestatud', 
    				success: true
    			})
    			
    			if(!SarvForm.isLocal)
    				SarvForm.given._refreshGrid();
    		},
    		failure: function(f, action) { 
    			SarvForm.message({
    				message: 'Kirje salvestamisel esines vigu:', 
    				error: true, 
    				data: action.result.errors, 
    			});
    		},
    	});
    }
    
    , cancel: function(e) {
    	var o = e.past,
    		f = this.getRecordForm();
    	SarvForm.given.form.i = o.i;
    	SarvForm.conf.item_id = o.id;
    	// todo * store.page could be used to avoid calculation
    	var p = o.store.offset > 0 ?
    		((o.store.offset + o.store.pageSize) / 
    		o.store.pageSize) : 1;
    	SarvForm.given._listGridPageTurner(p,o.i,true);
    	// As this method uses index, index is set beforehand
    	
    	// * Show grids and tab panels with grids
    	var g_l=f.query('sarv-grid-panel');
    	for(var i=g_l.length;i--;) {
    		var t=g_l[i].up('sarv-tab');
    		if('undefined' !== typeof t) {
    			t.show();
    		} else {
    			g_l[i].show();
    		}
    	}
    	
    	this.setPageData(); 
    	this.setButtons(SarvForm.isLocal ? 
    		[{save:{}}, {'delete':{}}, {'save-as':{}}] :
			[{save:{}}, {add:{}}, {'delete':{}}, {'save-as':{}}, {prev:{}}, {next:{}}]);
    }
    
    //  CLICKABLE COMBOBOXES  //
    
    , setUrlCombo: function(cb){
    	var pre='';
		//if('undefined' !== typeof cb.column) {
		//	pre=cb.column.up('sarv-grid-panel').name+'__';
		//}
		cb.sarv.store_name=pre+cb.name;
    	try {
    		var href = SarvForm.conf.urls[cb.sarv.store_model];
    	} catch(e) {
    		var href = false;
    	}
    	if(this.d(href) && href) {
    		cb.el.on('dblclick', 
    				this.openUrlComboPopup, 
    				this, {href: href, name: cb.sarv.store_model, cb:cb});
    		cb.setFieldStyle('background-color: #ffb; background-image: none;');
    	} else {
    		try {
    			// detach listener
    			cb.el.un('dblclick', 
    					this.openUrlComboPopup,
    					this);
    		} catch (e) {
    			console.log(e);
    		}
    		cb.setFieldStyle('background-color: #fff; background-image: none;');
    	}
    }
    
    // * Clicked combo. 
    //	Sarv object needs to be established
    // without nav keys etc
    , openUrlComboPopup: function(a,b,o){
    	// Here will be the init of Sarv object mimicing the
    	// parent one
    	var v=b.value;
    	if(!v || v.length < 1)
    		return;
    	    	
    	// Leida vormist 
    	//var f=this.getRecordForm()
    	//		.getForm().findField(b.name);
    	var f=o.cb;
    	
    	var uid=f.sarv.defaults[0];
    	if(isNaN(uid))
    		return;
    	
    	var url='/'+o.href+'/'+uid,
    		t_=this;
    	
    	// 'self' - open in this same window
    	if(SarvForm.given.conf.name==o.href) {
    		
    		// Is item id in data available in store
			var r_o=SarvForm.given.records,
				d_l=r_o.d,
				cI=r_o.f.indexOf('id'),
				rI=-1;
			for(var i=0,n=d_l.length;i<n;i++) {
				if(uid==d_l[i][cI])
					rI=i;
			}
			
			SarvForm.conf.item_id=uid;
			if(rI!=-1) {
				SarvForm.conf.i=rI;
				this.setPageData();
			} else {
				// If record was found not found locally,
				// load from server
				Ext.Ajax.request({
					url: 'everything?fp={"fp":[["id","exact","numeric","'+uid+'"]]}',
					success: function(res) {
						var r = SarvForm.given.records,
							d=JSON.parse(res.responseText);
						r.g = d.grids;
						r.d = d.records.d;
						r.f = d.records.f;
						SarvForm.conf.i=0;
						t_.setPageData();
					},
					failure: function() {}
				});
			}
    		
    	// popup window is already open
    	// but it is another page
    	} else if(SarvForm.forms) {
    		SarvForm.forms.location=url;
    	// open new popup window
    	} else {
	    	SarvForm.forms=window.open(
	    		url,'_blank',
				'width='+(400)+
				',height='+(500)+
				',location=0,status=0,toolbar=0');
    	}
    }
    
    // FILES //
    , fileSend: function() {
    	
    }
    
    // GRIDS //
    , gridAddEmptyRow: function(e) {
    	var g=e.up('gridpanel'),
    		s=g.store;
    	
    	var p=g.getPlugin('sarv-grid-rowediting');
    	var f=SarvForm.given.records.g[g.name].f,
    		u=[],
    		dv={};
    	for(var i=0,n=f.length;i<n;i++)
    		u.push({name:f[i]});
    	
    	for(var i=g.columns.length;i--;) {
			var c=g.columns[i];
			
			dv[c.dataIndex]='undefined'!== typeof c.defaultValue?
					c.defaultValue : null;
		}
		Ext.define('NewRecord', {
			extend: 'Ext.data.Model',
			fields: u});
		var nr=Ext.create('NewRecord', dv);
		s.insert(0, nr);
		p.startEdit(0, 0);
    }
    

    // e - reference to button component
    , gridDeleteRow: function(e) {
    	var txt={
    		'confirm-delete-row':'Kas soovid kustutada valitud rea?',
    		'message-record-deleted':'Kirje kustutatud',
    		'error-no-records-selected':'Ühtegi kirjet polnud valitud.',
    		'error-while-record-delete':'Kirje kustutamisel esines vigu.',
    		'error-db-connection':'Ühendus andmebaasiga',
    		'error-bound-record':'Kirje on seotud'
    	};
    	
    	var g=e.up('gridpanel'),
    		sel=g.getSelectionModel().getSelection();
		if(sel.length < 1) {
			SarvForm.message({ 
				message: txt['error-no-records-selected'], 
				error: true, 
				data:[], 
			});
			return false;
		}
		
		if(confirm(txt['confirm-delete-row'])) {
	    	var idr = sel[0].get('id');
	    	Ext.Ajax.request({
				url: 'delete?id='+idr+'&gridname='+g.name,
	    		success: function(res){
	                var msg={};
	                if(JSON.parse(res.responseText).response == 'success') {
	                	msg={
	                		message:txt['message-record-deleted'],
	                		success:true,
	                		data:[]
	                	};
	                	// * Remove relation mapping from records
	                	var gm=SarvForm.given.records
                			.g[g.name].m[SarvForm.conf.item_id];
	                	gm.splice(gm.indexOf(idr),1);
	                	//g.store.remove(sel);
	                	var d=SarvForm.given._getGridData(
								SarvForm.conf.item_id,
								g.name
							);
						g.store.loadRawData(d, false);
	                } else {
	                	msg={
	                		message:txt['error-while-record-delete'],
	                		error:true,
	                		data:[txt['error-bound-record']]
	                    };
					}
	                SarvForm.message(msg);
				},
	    		failure: function(){ 
				    SarvForm.message({ 
				    	message:txt['error-while-record-delete'], 
				    	error:true, 
				    	data:[txt['error-db-connection']]
				    });
				} 		
	    	});
		}
    }    
    
	// GRID EDITING
    , gridSetRow: function(n,d) {
    	var txt={
        		'error-no-changes':'Rea andmeid ei muudetud'
        	};
    	var r=d.record,		// get id & fields - tüübid
    		g=d.grid,
    		f_l=SarvForm.given.records.g[g.name].f,
    		nv_d=d.newValues,
    		ov_d=d.originalValues,
    		fc_d=(function(){
    			var fcd={},
    				r_=r.fields;
    			for(var i=r_.length;i--;)
    				fcd[r_[i].name]=r_[i].type;
    			return fcd;
    		}()),
    		bl_l=[],
    		out_d=nv_d,
			isChanged=false;
    	
		for(var j=g.columns.length;j--;) {
			var bl=g.columns[j].allowBlank,
				k=g.columns[j].dataIndex;
			// * Validation for required fields (allowBlank:false).
			if('undefined' !== typeof bl && !bl) {
				if(!nv_d[k]||[null,'',' '].indexOf(nv_d[k])!==-1)
					bl_l.push(g.columns[j].text);
			}
			
			// * Check if any value was changed
			var t=(fc_d[g.columns[j].dataIndex]||null),
				ov=String(ov_d[k]),
				nv=String(nv_d[k]);
			if(ov!=nv) 
				isChanged=true;
		}
		if(bl_l.length > 0) {
			SarvForm.message({
				message: 'Value missing for: ',
				error: true,
				data: bl_l
			})
			this.gridState=null;
			if(isNaN(r.id)){
				g.getView().refresh();
			}
			return;
		}
    	
    	// * Replace combo values that happen
		// to have string as labels with keys 
		for(var j=g.columns.length;j--;) {
			var col=g.columns[j],
				di=col.dataIndex;
			//console.log(col);
			if(col['sarv-type']=='combo' 
			&& Object.keys(out_d).indexOf(di) !== -1) {
				if('undefined' !== typeof out_d[di] 
				&& isNaN(out_d[di]) && out_d[di].length > 0) {
					var d=SarvForm.conf.stores.data[
					        col.sarv.store_name];
					// remote combos get away with it
					if('undefined' === typeof d)
						continue;
					for(var jj=d.d.length;jj--;) {
						if(d.d[jj][1] == out_d[di]) {
							out_d[di] = d.d[jj][0];
						}
					}
				}
			}
		}
    	if(!r.id||isNaN(r.id)) {    		
    		this.gridRowAdd({g:g,r:out_d});
    	} else {
    		if(isChanged) {
    			this.gridRowUpdate({g:g,r:out_d,id:r.id}, g.store.currentPage);
            }
    	}
    }
	
	, gridRowAdd: function(d) {		
		var g=d.g,
			fr=g.store.first(),
			t_=this;
		
		if(isNaN(fr.get('id'))) {
			var empty = true,
				out = {
					gridname: g.name, 
					grid_parent_id: SarvForm.conf.item_id,
				};
			for(var k in d.r) {
				if(k=='fields' || k=='id' || k=='id_')
					continue;
				out[k] = d.r[k];
			}
			if (Object.keys(out).length > 2) 
				empty = false;
			if(empty) {
				g.store.remove(fr);
			} else {
				Ext.Ajax.request({
					url: 'save',
					params: out,
					success: function(response) {
						var r = JSON.parse(response.responseText);
						var msg = ('undefined' !== typeof r.success 
								&& r.success == true) ?
							{
								message: 'Kirje lisatud.', 
								success: true, 
								data:[]
							} : { 
								message: 'Viga.',
								error: true, 
								data: r.errors
							};
						SarvForm.message(msg);
						
						// If there was an error on server side, 
						// remove the first row
						if('undefined' !== typeof msg.error && msg.error) {
							g.store.remove(fr);
							return;
						}
						// insert one to the end of the grid
						
						var d=SarvForm.given.records.g[g.name],
							r_l=[];
						
						if('undefined' !== typeof r.data) { 
							for(var i in r.data) {
								out[i]=r.data[i];
							}
						}
						if('undefined' !== typeof r.id) {
							out['id']=r.id;
							out['id_']=r.id;
						}
						
						for(var i=0,n=d.f.length;i<n;i++)
							if('undefined' !== typeof out[d.f[i]])
								r_l.push(out[d.f[i]]);
							else
								r_l.push(null);
						try{
							d.r[r.id]=r_l;
							if('undefined' === typeof d.m[SarvForm.conf.item_id])
								d.m[SarvForm.conf.item_id]=[];
							d.m[SarvForm.conf.item_id].push(r.id);
						}catch(e){
							console.log(e);
						}
						
						//Refresh store grid
						var d=SarvForm.given._getGridData(
								SarvForm.conf.item_id,
								g.name
							);
						g.store.loadRawData(d, false);
						
						var t=g.store.getTotalCount(),
							np=Math.ceil(t/g.store.pageSize);
						try{
							g.store.loadPage(np);
						}catch(e){
							console.log(e);
						}
						
					},
					failure: function() {},
				});
			}
		}
	}
	
    , gridRowUpdate: function(d, currPage) {
    	var t_ = this,
    		g=d.g,
			s=g.store,
			r=d.r,
			//m=t_.gridState.m,
			out={ 
				gridname: g.name, 
				grid_parent_id: SarvForm.conf.item_id,
				id: parseInt(d.id)
			},
            currPage = currPage||1;
    	//this.gridState=null;

    	// Take only values from grid columns
    	var gc_l=g.columns;
    	for(var i=gc_l.length;i--;) {
    		var f=gc_l[i].dataIndex;
    		if('undefined' !== typeof r[f]) {
    			out[f]=r[f];
    		}
    	}
    	
    	// If no fields had new content, return
    	if(out.length == 3) {
    		s.load();
    		return;
    	}
    	// If there are remote combos
    	var rcdv_d={};
    	for(var i=gc_l.length;i--;) {
    		if('undefined' === typeof gc_l[i].sarv)
    			continue;
    		var sdf=gc_l[i].sarv.store_default_field;
    		if('undefined' !== typeof sdf) {
    			rcdv_d[sdf]=gc_l[i].sarv.defaults[1];
    		}
    	}
		Ext.Ajax.request({
			url:'save',
			params: out,
			success: function (rsp) {
				var rsp = JSON.parse(rsp.responseText);
				var msg = ('undefined' !== typeof rsp.success && rsp.success == true) ?
					{
						message: 'Kirje uuendatud', 
						success: true, 
						data:[]
					} : { 
						message: 'Viga rea salvestamisel', 
						error: true, 
						data: rsp.errors
					};
				var u_l=[];
				SarvForm.message(msg);
				// * If error occurred on server side
				if('undefined' !== typeof msg.error && msg.error) {
					//if('undefined'!== typeof m.data[d.f.name])
					//	m.data[d.f.name]=d.f.originalValue;
				} else {
					if('undefined' !== typeof rsp.data) { 
						for(var i in rsp.data) {
							r[i]=rsp.data[i];
						}
					}
					// * Update data repository in opener window
					try {
						var g_d=SarvForm.given.records.g[g.name],
							f_l=g_d.f,
							cr_d=g_d.r[d.id];
						for(var i in r) {
							var fI=f_l.indexOf(i);
							if(fI !== -1) {
								cr_d[fI]=r[i];
								u_l.push(i);
							}
						}
						// Add default values to remote combo fields
						for(var i in rcdv_d){
							var fI=f_l.indexOf(i);
							if(fI !== -1) {
								cr_d[fI]=rcdv_d[i];
							}
						}
					} catch (e) {
						// Invalid grid data structure from opener side
						SarvForm.message({
							message: 'Internal data error.'+
									'Could not update cell data.',
							error: true
						})
					}
				}
				
                s.currentPage = currPage;
				s.load();
                
				t_.setPageData();
			},
			failure: function () {},
		});
    } 

    , gridSync: function (d) {
    	var g=d.f.up('sarv-grid-panel'),
			s = g.store,
			r = s.first(),
			id=r.get('id'), 
			// if first row doesn't have id, row is being inserted
			is_insert = (!id || id.length < 1 || isNaN(id));
		
		if(is_insert && d.rowIdx != 0)
			s.remove(r);
		if(!is_insert || d.rowIdx != 0)
			s.sync();
    }    
    
    //  COMBOBOXES //
    , setComboPage: function(e){
    	var smn=e.sarv.store_name,
    		d=SarvForm.conf.stores.data[smn]['d'],
			n=d.length,
			ps=10,
			j=0,
			sd=e.sarv.defaults,
			dv = 'undefined' !== typeof sd ?
				sd.value : false;
		for(var i=0; i<n; i++)
			if(d[i][0] == dv)
				j=i+1;
		var r=j/ps;
		e.store.loadPage(
			(j >= ps) ? parseInt(r>Math.floor(r) ?
					r+1 : r) : 1);
    }
        
    // UTILS //
    
    // Checks type of given object
    // Default check without second argument:
    // 'is defined?' (e.g. is not undefined?)
    // Otherwise 'is type of' <second argument>
    , d: function(i,type){
    	var t=(type||'undefined'),
    		x=(t===typeof i);
    	//if type is checkeg against undefined
    	//return inverted value
    	return t=='undefined'?(!x):x;
    }
});
