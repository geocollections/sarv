/*
 * Sarv list view controller
 */

Ext.define('Sarv.controller.List', {
    extend: 'Ext.app.Controller'

    , sarv:{
    	dblclick: false, // distinguish click from dblclick
    	isFilteredQueryRadioClick: true // flag to tell whether user toggles "My records"/"All records" or is radio change event triggered by some other action  
    }

    , refs:[{
    	ref: 'Viewport',
    	selector: 'sarv-viewport'
    },{
    	ref: 'ListGrid',
    	selector: 'sarv-listgrid',
    	autoCreate: true
    }]
    
    // Up & down arrow navigation in list grid
    , registerKeyBindings: function(view, options){
    	var t_=this;
        Ext.EventManager.on(view.getEl(), 'keyup', function(evt, t, o) {
        	var iid=false;
        	if('undefined' !== typeof Sarv.forms.SarvForm 
        	&& 'undefined' !== typeof Sarv.records) {
	            if (evt.keyCode === Ext.EventObject.UP) {
	                iid='item-previous';
	            } else if (evt.keyCode === Ext.EventObject.DOWN){
	            	iid='item-next';
	            }
	            if(iid) {
	            	Sarv.forms.SarvForm.app
	    			.controllers.items[0]
	    			.navigator({itemId: iid});
	            }
        	}
        }, this);
    }
    
    , init: function() {
    	var c = Sarv.conf;
    	
    	this.control({
    		
    		// * Viewport
    		'viewport': {
    			afterrender: function() {
    				// Ajax loading mask on ajax request 
    				document
	    				.getElementById('page-loader-mask')
	    				.style.display ='none';
    			}
    		},
    		
    		// * Filter grid
    		
    		'#filter-field-combo': {
    			select: function(cb) {
    	            this.updateComboBox(cb,
    	            	'filtergrid');
    	        }
    		},
    		
    		'#filter-type-editor': {
    			select: function(cb) {
      		        this.updateComboBox(cb, 
      		        	'filteradd');    
  				}
    		},
    		
    		'#filter-value-editor': {
    			specialkey: function(f, e){
    				var t_=this;
       	            if (e.getKey() == e.ENTER) {
       	            	setTimeout(function(){ 
       	            		t_.filteredQuery();
       	            	}, 50);
       	            }
       	        }
    		},
    		
    		// * Filter menu buttons
    		
    		'#btn-filter-remove': {
    			click: this.remove
    		},
    		'#btn-list-showmy': {
    			change: function() {
    				if(arguments[1] 
    				&& this.sarv.isFilteredQueryRadioClick) {
    					this.filteredQuery(true);
    				}
    			}
    		},
    		'#btn-list-showall': {
    			change: function() {
    				if(arguments[1]
    				&& this.sarv.isFilteredQueryRadioClick) {
    					this.showAll();
    				}
    			}
    		},
    		'#btn-list-filter': {
    			click: function () {
    				this.filteredQuery('filtered');
    			}
    		},
    		
    		// * 'Add record' button 

    		'#btn-form-add': {
    			afterrender: function(e) {
    				var c=Sarv.conf;
    				if(c.acl[1] == true || c.acl === 'own')
    					e.show();
    				else
    					e.hide();
    			},
    			click: function(e) {
    				if('undefined' !== typeof Sarv.forms 
    				&& Sarv.forms != null 
    				&& 'undefined' !== typeof Sarv.forms.windows) {
    					Sarv.forms.SarvForm.app.controllers.items[0].add();
    			    } else {
	    				Sarv._openPopup(c, 'add');
    				}
    			}
    		},

    		// * Saved queries
    		
    		'#custom_filtersets_combo': {
    			expand: function(cb) {
 					// To resolve hiding the pager
 					// when list width is smaller
 					// than the pager width
        			try {
 						var w=cb.picker.getWidth();
 						if(w < 250) {
 							cb.picker.setWidth(250);
 						}
 					} catch(e) {
 						console.log(e);
 					}
        		},
        		specialkey: function(f, e){
       	            if (e.getKey() == e.ENTER) { 
       	            	this.savedQuery(f.value);
       	            }
        		},
        		select: function(f,e) {
        			this.savedQuery(f.value);
        		}
    		},
    		
    		'#custom_filtersets_set': {
    			click: this.saveQuery
    		},
    		
    		'#custom_filtersets_delete': {
    			click: function() {
    				this.deleteQuery();
    	    		this.showAll(); 
    			}
    		},
    		
    		// * Custom sets
    		
    		'#combo-custom_dataset': {
    			expand: function(cb) {
    				try {
 						var w=cb.picker.getWidth();
 						if(w < 250) {
 							cb.picker.setWidth(250);
 						}
 					} catch(e) {
 						console.log(e);
 					}
    			},
				select: function(cb) {
					var lg = Ext.ComponentQuery.query("#listgrid")[0];
					if(!isNaN(cb.value) && cb.value != 0) {
					//	lg.columns[0].hide();
					//} else {
						this.filteredQuery();
						lg.columns[0].show();
					}
				},
				blur: function(cb) {
					if(isNaN(cb.value) || cb.value < 1) {
						this.filteredQuery();
						var lg = Ext.ComponentQuery.query("#listgrid")[0];
						lg.columns[0].hide();
					}
				}
    		},
    		
    		'#btn-custom_dataset-show': {
    			click: function(b) {
    				var s=Ext.getCmp('combo-custom_dataset'),
    					d_id=s.value;
    				if('undefined' !== typeof d_id 
    				&& d_id != null && !isNaN(d_id)) {
    					this.filteredQuery(d_id);
    				}
    			}
    		},
    		'#btn-custom_dataset-addto': {
    			click: this.setCustomDataset
    		},
    		'#btn-custom_dataset-delete': {
    			click: this.deleteCustomDataset
    		},
    		
    		// Filter grid Enter event
    		'#sarv-filter-editor': {
    			specialkey: function(field, e) {
    				var t_=this;
    				if (e.getKey() == e.ENTER) {
       	            	setTimeout(function(){
       	            		t_.filteredQuery('filtered');
       	            	}, 50);
       	            }
    			}
    		},
    		
    		// * List grid actions
    		'listgrid': {
    	    	afterrender: function(e) {
    	    		// Load store
    	        	if('undefined' !== typeof 
    	        	c.records.settings.doFilteredQuery) {
    	        		switch (c.records.settings.doFilteredQuery) {
    	        			case 'my':
    	        				this.filteredQuery(true);
    	        				break;
    	        			case 'all':
    	        				this.showAll(e);
    	        				break;
    	        		}
    	    		}
    	        	this.registerKeyBindings(arguments[0], arguments[1]);

					e.columns[0].hide();
    	    	},
    	    	
    	    	//itemclick: function(g, r, i, n){ 
				cellclick: function(th, td, cI, r, tr, n){
					var i=null, g=null;
					if(cI == 0) {
						var cls_l=td.classList;
						if(cls_l.contains('x-grid-cell-first')) {
							this.setSelectionValue(r, tr);
							return;
						}
					}
    	    		this.gridClickHandler(g, r, i, n);
    	    	},
    	    	
    	    	itemdblclick: function(dw, r) {
    	    		this.sarv.dblclick=true;
    	    		try {
    	    			var id=r.data.id;
    	    		} catch (e) {
    	    			return;
    	    		}
    	    		Sarv._openPopup(c, id, true);
    	    	}
    	    } // /listgrid
    	});

    }
    
 // Removes select from list grid
	// 
	, _listGridDeselectAll: function() {
		var g = Ext.getCmp('listgrid');
		g.getSelectionModel().deselectAll();
	}

    , add: function(myResults) {
		var fg = Ext.getCmp("filteradd"),
			g = Ext.getCmp("filtergrid"),
			fs = fg.store.first(),
			s = g.getStore();
		
		if(fs.get('field') != "Vali väli" 
		&& fs.get('value').replace(" ","") != "") {
			s.add({
		    	field: fs.get('field'),
		    	filter: fs.get('filter'),
		    	value: fs.get('value'),
		    	filter_type: fs.get('filter_type'),
		   	});
		    s.commitChanges();
		    setTimeout(function(){
		    	g.getView().refresh();
		    	fg.getStore().reload();
		    }, 50);
		}
	}
    
	, remove: function() {
    	var g = Ext.getCmp('filtergrid');
        if (g) {
            var sm = g.getSelectionModel(),
            	rs = sm.getSelection();
            if (!rs.length) {
                Sarv.message({
                	message: 'No Records Selected',
                	error: true
                })
                return;
            }
            g.store.remove(rs[0]);
        }
	}
	
	, updateComboBox: function(cb, gname) { 
		var g = Ext.getCmp(gname),
			sm = g.getSelectionModel(),
			cs = sm.getSelection(),
			f = cb.getValue(),
			ft = Sarv.conf.fields_filter_types[f];
		cs[0].set({
			filter: Sarv.conf.filters_types[ft][0][1],
			filter_type: ft,
			filter_default_num: 0 
		});
		g.getStore().commitChanges();
		g.getView().refresh();
	}
	
	// 
	// {type} - if integer, then custom selection, if true then user's records, if false then all records
	, filteredQuery: function(type) {
		this.add();
		var g=Ext.getCmp('listgrid'),
			s=g.getStore(),
			qv=this.getQueryValues(),
			pr=s.getProxy();
		
		pr.extraParams.myresults = 'no';
				
		var btn='showall';
		if (typeof type === 'number') { // if type is integer
			qv=[];
			pr.extraParams.custom_dataset_id = type;
			btn='other';
		} else if (type == 'filtered') {
			btn='other';
		} else if(type) {
			pr.extraParams.myresults = 'yes';
			btn='showmy';
		} 

		//if selection combobox has value then include selection values in grid response
		//pr.extraParams.custom_dataset_id = null;
		var cb=Ext.ComponentQuery.query("#combo-custom_dataset")[0];
		if(!isNaN(cb.value) && cb.value > 0) {
			pr.extraParams.in_custom_dataset=cb.value;
			btn='other';
		} else {
			pr.extraParams.in_custom_dataset=null;
		}


		this.sarv.isFilteredQueryRadioClick = false;
		g.up()
			.query('#btn-list-'+btn)[0]
			.setValue(true);
		this.sarv.isFilteredQueryRadioClick = true;
		
		pr.extraParams.fp = JSON.stringify({fp: qv});

		s.load({params: {start: 0}});

		if(!s.isLoading()) {
			s.loadPage(1);
		}
		
		s.currentPage = 1; 
		useFilters = true;
	}
	
	, saveQuery: function() {
		var fsc=Ext.getCmp('custom_filtersets_combo'),
			v=fsc.getRawValue(),
			qv=this.getQueryValues(),
			t_=this;
		if ('undefined' !== typeof v) {
			Ext.Ajax.request({
				url:'set_custom_filterset',
				params: {
					name: v,
					params: JSON.stringify(qv),
				},
				success: function(r) {
					Sarv.message({
						message: 'Salvestatud', 
						success: true
					});
					t_.filteredQuery();
				},
				failure: function(r) {
					Sarv.message({
						message: 'Salvestamine ebaõnnestus', 
						error: true
					});
				},
			});
		} else {
			Sarv.message({
				message: 'Vaja sisestada nimi', 
				error: true
			});
		}
	}
	
	, savedQuery: function(params) {
		if ('undefined' === typeof params) 
			return;
		var g = Ext.getCmp('listgrid'),
			s = g.getStore(),
			i_d = JSON.parse(params);
		for (var k in i_d) 
			break;
		p_d = JSON.parse(i_d[k]);
		s.getProxy().extraParams.fp = JSON.stringify({fp: p_d});
		s.load({params: { start: 0 }});
		if(!s.isLoading()) 
			s.loadPage(1);
		s.currentPage = 1;
		useFilters = true;	
		
		var fg = Ext.getCmp('filtergrid');
		var fs = fg.getStore();
		fs.removeAll();

		var fv=[],
			fv_d=Sarv.conf.fields_verbosenames;
		for (var i in fv_d) 
			fv[fv_d[i]] = i;

		for (var i in p_d) { 
			var v = '',
				ft_d = Sarv.conf.filters_types[p_d[i][2]];
			for (var j in ft_d) 
				if (ft_d[j][0] == p_d[i][1]) {
					v = ft_d[j][1];
					break;
				}
			
			fs.add({
				field: fv[p_d[i][0]],
				filter:	v,
				value: p_d[i][3],
				filter_type: p_d[i][2]
			});
			fs.commitChanges();
		}
	}
	
	, deleteQuery: function() {
		var cb=Ext.getCmp('custom_filtersets_combo'),
			rv=cb.getRawValue();
		if ('undefined' !== typeof rv
		&& confirm('Kas soovid kustutada valikut "'+rv+'"?')) {
			Ext.Ajax.request({
				url:'delete_custom_filterset',
				params: { name: rv },
				success: function(response) {
					Sarv.message({
						message: 'Kustutatud', 
						success: true
					});
					
					var fg=Ext.getCmp('filtergrid'),
						fs=fg.store,
						i_d={};
					
					for (var v in Sarv.conf.filters_default) {
						fs.add({
							field: i_d[i][0],
							filter: i_d[i][1],
							value: i_d[i][3],
							filter_type: i_d[i][2],
						});
						fs.commitChanges();
					}
				    setTimeout(function(){
				    	fg.getView().refresh();
				    },150);
				},
				failure: function(r) {
					Sarv.message({
						message: 'Kustutamine ebaõnnestus',
						error: true
					});
				}
			});
		} 
	}
	
	
	// LIST GRID METHODS
	
	, showAll: function() {
		//Sarv.conf.custom_dataset = null;
		var g=Ext.getCmp('listgrid'),
			s=g.store,
			ep=s.proxy.extraParams;
		ep.custom_dataset_id = null;
		ep.fp='';
		ep.myresults='';	
		if(!s.isLoading()) 
			s.loadPage(1);
		Sarv.conf.records.settings.useFilters = false;
	}
	
	, getQueryValues: function() {
		var g=Ext.getCmp('filtergrid'),
			s=g.store.getRange(),
			qV=[],
			c=Sarv.conf;
		for(var i=0, n=s.length; i<n; i++) {
			 var r=s[i].data,
			 	rf='',
			 	ft=c.filters_types[r['filter_type']];
			 if('undefined' === typeof ft)
				 continue;
			 
			 for(var j=0, nf=ft.length; j<nf;j++) {
				 if(ft[j][1] == r['filter'])
					 rf = ft[j][0];
			 }	 
		     qV.push([c.fields_verbosenames[r['field']],
		          rf, r['filter_type'], r['value']]);
		}
		return qV;
	}
	
	, setCustomDataset: function(s) {
		var cb=s.up('sarv-viewport')
				.query('#combo-custom_dataset')[0],
			label,
			t_=this;
		if('undefined' === typeof cb.value 
		|| cb.value == null || isNaN(cb.value)) {
			label=cb.rawValue;
			var s_l=cb.store.data.items;
			for(var i=s_l.length;i--;) {
				if(label==s_l[i].data.value) {
					label=s_l[i].data.name;
					break;
				}
			}
		} else {
			label=cb.value;
		}
		
		// get all filter data
		this.add();
		var g=Ext.getCmp('listgrid'),
			s=g.getStore(),
			qv=this.getQueryValues();
		if(qv.length < 1)
			return;
		
		Ext.Ajax.request({
			url:'set_custom_dataset',
			params: {
				k: label,
				fp: JSON.stringify({fp: qv})
			},
			success: function(r) {
				//Sarv.conf.custom_dataset=r.id;
				var rp=JSON.parse(r.responseText);
				if(!isNaN(rp.id)) {
					t_.filteredQuery(rp.id);
				}
				Sarv.message({
					success: true,
					message: 'Valik seatud'
				});
			},
			failure: function(r) {
				Sarv.message({
					error: true,
					message: 'Viga valiku seadmisel'
				});
			}
		})
	}
	
	, deleteCustomDataset: function(s) {
		var cb=s.up('sarv-viewport')
				.down('#combo-custom_dataset'),
			d_id=cb.value,
			t_=this;
		
		if(isNaN(d_id))
			return;
		
		Ext.Ajax.request({
			url:'delete_custom_dataset',
			params:{
				id: d_id
			},
			success: function(r) {
				cb.reset();
				cb.store.load();
				t_.filteredQuery();
				Sarv.message({
					success: true,
					message: 'Valik kustutatud'
				});
			},
			failure: function(r) {
				Sarv.message({
					error: true,
					message: 'Valiku kustutamine ebaõnnestus'
				});
			}
		})
	}

	, gridClickHandler: function(dw, r, i, n) {
		var t_=this,
			s=Sarv,
			c=Sarv.conf,
			clickHandler=function() {
				try {
					var id=r.data.id;
				} catch (e) {
					return;
				}
				
				if(s.form.formFields.length==0) {
					s.message({
						error: true,
						message: "Vormi elemente laetakse veel."
					});
					return;
				}
				
				// If no related child 
				// popup window is open, 
				// create one. Otherwise
				// update child's data
				if(s.forms == null) {
					s._openPopup(c, id);
				} else {
					s.forms.SarvForm.conf.i = n;
					s.forms.SarvForm.app
						.controllers.items[0]
						.setPageData();
				}
			},
			locked=(locked||false);
		
		// Distinguish dblclick from click
		if(!locked) {
			locked=true;
			window.setTimeout(function(){
				if(!t_.sarv.dblclick 
				&& locked) { 
					clickHandler();
				}
				locked=false;
			}, 400);
			if(t_.sarv.dblclick)
				t_.sarv.dblclick=false;
		} 
	}
	
	// Set single selection value via grid button push
    , setSelectionValue: function(r, tr) {
		var cb = Ext.ComponentQuery.query("#combo-custom_dataset")[0];
		// Ajax call
		Ext.Ajax.request({
			url:'set_custom_dataset_item',
			params:{
				idr: r.get('id'),
                ids: cb.value
			},
			success: function(r) {
                var rp=JSON.parse(r.responseText);
                if('undefined' !== typeof rp.error) {
					Sarv.message({
						error:true,
						message: 'Kirje valikusse lisamine ebaõnnestus',
						data: rp.error
           			})
				} else {
					// change icon for that row
				}
			},
			failure: function(r) {
				Sarv.message({
					error: true,
					message: 'Kirje valikusse lisamine ebaõnnestus'
				});
			}
		})
	}

});
