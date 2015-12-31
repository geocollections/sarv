Ext.define('SarvForm.view.grid.Panel', {
	extend: 'Ext.grid.Panel',
	title: 'Tabel',
	xtype: 'sarv-grid-panel',
	buttonAlign: 'left',
	sarv: {
		model:{},
		remoteComboDefaults: {},
	},
	header: true,
	constructor: function(conf) {
		var ps=(conf.pageSize||10),
			d=SarvForm.given._getGridData(
					SarvForm.conf.item_id,
					conf.name),
			t=this,
			f_l=SarvForm.given.records.g[conf.name].fc;
		
		// Explicit model to fix null problem of the numeric
		// fields (null being replaced with zeros)
		this.sarv.model = Ext.create('SarvForm.model.Grid', {
			fields: f_l
		});

		conf['store'] = Ext.create('Ext.data.Store', {
			storeId: conf.name,
			model: this.sarv.model,
			autoDestroy: true,
			pageSize: ps,
			proxy:{
				enablePaging: true,
				model: this.sarv.model,
				type: 'memory',
				reader: {
		            type: 'json',
		            root: 'items',
		            idProperty: 'id'
		        }
			},
			data: {
				items: d
			},
			loadRawData: function(data, append){
		        var r=this.proxy.reader.read(data),
		        	th_=this;
		        if (r.success) {
		        	//th_.currentPage=1;
		            th_.totalCount=r.total;
		            th_.pageSize=ps;
		            th_.proxy.data=r.records; // added
		            th_.sync();
		            th_.load();
		        }
			},
            sort: function() {
                var colName = arguments[0],
                    dir = "undefined" === typeof arguments[1] || arguments[1]=="ASC"; // asc - true; desc - false 
                // strategy: on sort re-order SarvForm.given.records.g[grid_name].m[<record_id>] or this.data.items then reload grid on given page
                // t.config.name is grid name . SarvForm.given.records.g[<grid name>].m[<record_id>] 
                // t.columns[kus <t.columns[i].dataIndex> == this.name?].editor
                //var data = this.config.data.items;
                var data = this.proxy.data;
                // get current column xtype
                var colConfig = {};
                for(var i=t.columns.length;i--;){
                    if(t.columns[i].dataIndex == colName)
                        colConfig = t.columns[i].config.editor;
                }
                // create array of current values
                var key_order = [], sortable = [];
                for(var i=data.length;i--;) {
                    key_order.push(data[i].data[colName]);
                    sortable.push({ 
                        value: data[i].data[colName],
                        data: data[i].data
                    });
                }
                // Get values for combo fk numbers
                if(colConfig.xtype.indexOf("combo") != -1) {
                    // iterate over store dataset in SarvForm.conf to get values
                    // store_data = [[<key>,<value>],..,[<key>,<value>]]
                    var store_data = SarvForm.conf.stores.data[this.storeId+"__"+colName].d;
                    for(var i=store_data.length;i--;){
                        if(key_order.indexOf(store_data[i][0])!=-1){
                            var n = key_order.indexOf(store_data[i][0]);
                            sortable.splice(
                                n, 1,
                                {key: store_data[i][0],
                                 value: store_data[i][1],
                                 data: sortable[n].data}
                            );
                        }
                    }
                }
                // Sorting itself
                sortable.sort(function (a, b) {
                    if(a.value == null)
                        return dir ? -1 : 1;
                    if(b.value == null)
                        return dir ? 1 : -1;
                    if (a.value > b.value) {
                        return dir ? 1 : -1;
                    }
                    if (a.value < b.value) {
                        return dir ? -1 : 1;
                    }
                    // a must be equal to b
                    return 0;
                })

                // Add sorted data to store
                var r=this.proxy.reader.read(
                    sortable.map(function(d){
                        return d.data;
                    })
                );

		        if (r.success) {
		        	this.proxy.data=r.records; // added
		            this.sync();
                    this.load();
                }
            }
		});
		
		// Cell editor types: textfield or combobox
		// Perhaps it is not optimal to separately
		var c=conf.columns;
		for(var i=c.length;i--;) {
			
			if('undefined' !== typeof c[i]['readOnly'] 
			&& c[i]['readOnly']) {
				continue;
			}
			var type=('undefined' !== typeof c[i]['sarv-type']) ?
					c[i]['sarv-type'] : false;
				
			conf.columns[i]['editor']={};
			
			if('undefined' !== typeof c[i]['allowBlank']) {
				conf.columns[i]['editor']['validator'] = function(v) {
					return (v.replace(' ','').length < 1) ? 
						'Field must not be empty' : true;
				}
			}
			
			if(type=='combo') {
				var c_=c[i];
				c_.sarv.defaults=(c_.sarv.defaults||{});
				
				conf.columns[i]['editor'] = {
					xtype: 'sarv-field-combo',
					sarv: c_.sarv
				};
				
				if('undefined' !== typeof c_.sarv.store_type 
				&& c_.sarv.store_type == 'remote')
					conf.columns[i]['editor'].xtype='sarv-field-combo-remote'
				
				conf.columns[i]['renderer'] = function(v,m) {
					
					// Set column background yellow if clickable combobox
					try { var href = SarvForm.conf.urls[c_.sarv.store_model];
			    	} catch(e) { var href = false; }
			    	if(href) m.style='background-color:#ffb';
			    	
					// Blank FK
					if(v==0||v==null)
						return '';
					// After the combobox is selected, 
					// different set of parameters is
					// passed to renderer closure
					try {
						if('undefined' === typeof arguments[1]
						||arguments[1]==null) {
							var f=this.field;
						} else {
							var f=arguments[1].column;
						}
					}catch(e) {console.log(e);}
					
					if('undefined' !== typeof f.sarv)
						if('undefined' !== typeof f.sarv.store_model) {
							// Remote combo labels vs local
							// If store_default_field is defined
							// then combo is remote
							var sdf=f.sarv.store_default_field;
							
							if('undefined' !== typeof sdf) {
								if('undefined'!==typeof arguments[2]
								&&arguments[2]!=null) {
									try{
									var rsd=SarvForm.conf.stores,
										nd=arguments[2].data[sdf];
										v=nd;
									}catch(e){console.log(e);}
								}
							} else {
								var sn=this.name+'__'+f.dataIndex;//sn=f.sarv.store_model;
								
								if('undefined' !== typeof 
								SarvForm.conf.stores.data[sn]) {
									d=(SarvForm.conf.stores
										.data[sn]['d']||false);
								} else 
									d=false;
								if(d) {
									for(var j=d.length;j--;)
										if(d[j][0]==v) {
											v=d[j][1];
											f.sarv.defaults=d[j];
										}
								}
							}
						}
					return v;
					
				}
				continue;
			} else if(type == 'checkcolumn') {
				conf.columns[i]['xtype'] = 'sarv-grid-checkcolumn'; //'checkcolumn';
				conf.columns[i]['editor']['xtype'] = 'checkbox';
			} else if(type == 'actioncolumn') {
				conf.columns[i]['xtype'] = 'sarv-grid-actioncolumn';
				conf.columns[i]['editor'] = null;
			} else if(type == 'radiocolumn') {
				conf.columns[i]['xtype'] = 'sarv-grid-radio';
				conf.columns[i]['editor'] = null;
			} else {
				conf.columns[i]['editor']['xtype'] = 'textfield';
			}

		}
		
		// Cell edit //
		this.plugins = [ 
			Ext.create('Ext.grid.plugin.RowEditing', {
				clicksToEdit: 1,
				pluginId:  'sarv-grid-rowediting',
				saveBtnText: 'Salvesta',
				cancelBtnText: 'Tühista',
				listeners: {
					beforeedit: function(obj,o) {
						var g=obj.grid,
							f=g.up('record-form').form,
							c=SarvForm.conf,
							ua=f.findField('user_added').getValue(),
							uc=f.findField('user_changed').getValue();
												
						// Does user have right to edit this field
						if(c.acl[2] != true 
						&& (c.acl[2] != 'own' 
	                	|| (c.username !== ua 
	                	&& c.username !== uc)))
							return false;
						this.tmpValue=arguments[1].value; // tmpValue because combobox seems otherwise not be getting value
					},
					afteredit: function() {
						this.tmpValue=null;
					},
					cancelEdit: function() {
						var o=arguments[1],
							s=o.store,
							r=o.record;

						if(!r.data.id||isNaN(r.data.id))
							s.remove(r);
					}
				}
			})
		];
		
		// Create delete row button //
		this.dockedItems = [{
	        xtype: 'pagingtoolbar',
	        store: conf['store'],
	        dock: 'bottom',
	        displayInfo: true,
	        viewConfig: { loadMask: true },
	        items: ['-',
	            {
    				xtype:'button',
    			    itemId: 'grid-btn-add-row',
    			    iconCls: 'row-add',
    			    //text: 'Lisa rida'
				},{
					xtype: 'button',
					itemId: 'grid-btn-delete-row', // event handler in controller
					iconCls: 'row-delete',
					//text: 'Kustuta rida',
					scale: 'small',
			 }]
		}];

		this.initConfig(conf);
		this.callParent(arguments);
				
	}
});
