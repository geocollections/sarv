Ext.define("SarvForm.view.field.ComboFieldRemote",{
	extend:"Ext.form.field.ComboBox",
	xtype:"sarv-field-combo-remote",
	sarv: { 
		link:null,
		href:false,
		defaults:null,
		store_model:null,
		pageSize:10,
		isTyped:false,
		isExpandEvent:false
	},
	labelAlign:"right",
	multiSelect:false,
	autoSelect:false,
	selectOnFocus:true,
	typeAhead:true,
	minChars:1,
	matchFieldWidth:false,
	autoDestroy:true,
	displayField:"value",
	valueField:"name",
	queryMode:"remote",
	constructor:function(b){
		this.sarvConstructor(b);
		this.initConfig(b);	
		this.callParent([b]);
	},
	sarvConstructor:function(d){
		d.sarv.pageSize=(d.sarv.pageSize||10);
		this.pageSize=d.sarv.pageSize;
		var f=this,
			e=this.up("sarv-grid-panel"),
			e="undefined"===typeof e?false:e;
		if("undefined"===typeof d.sarv.defaults||d.sarv.defaults==null){
			d.sarv.defaults=[null,null]
		}
		d.store=Ext.create("Ext.data.Store",{
			storeId: d.sarv.store_model,
			fields:["name","value"],
			pageSize:d.sarv.pageSize,
			proxy:{
				type:"ajax",
				autoLoad:false,
				url:"store?field="+d.name,
				reader:{
					type:"json",
					root:"store_records",
					totalProperty:"store_record_count"
				}
			},
			listeners:{
				beforeload:function(){
					var a=f.up("sarv-grid-panel");
					if("undefined"!==typeof a){

					}
					if(f.sarv.isExpandEvent&&!f.sarv.isTyped){
						this.proxy.extraParams.id_to_page=f.sarv.defaults[0];
						f.sarv.isExpandEvent=false
					}else{
						if("undefined"===typeof a)
							delete this.proxy.extraParams.id_to_page
					}
				},
				load:function(){
					var m=arguments[0],
						c=m.proxy.reader.rawData,
						l=arguments[3].getParams(),
						a="undefined"!==typeof c.page?c.page:false;
					if(a){m.currentPage=a}
					if("undefined"===typeof l.isSetLabel){
						try{
							if(arguments[1].length>0&&!f.sarv.isTyped){
								f.setValue(f.sarv.defaults[1])
							}
						}catch(b){console.log("load: "+b)}
					}
					try{
						var n=f.picker.getWidth();
						if(n<250){f.picker.setWidth(250)}
					}catch(b){}
				}
			}
		})
	},
	setLabel:function(){
		var o=this.up("sarv-grid-panel"),
			o="undefined"!==typeof o?o:false,
			u=SarvForm.given.records,
			u=!o?u:u.g[o.name];
		if(!o){
			if(this.sarv.isTyped){
				this.value=this.sarv.defaults[0]
			}
			if(this.value==null){
				this.sarv.defaults=[null,null]
			}else{
				if(!isNaN(this.value)){
					var g=this.sarv.store_default_field,
						p=u.f,
						r=p.indexOf(g);
					if(r!==-1&&p.indexOf(this.sarv.store_name)!==-1
					&&"undefined"!==typeof u.d[SarvForm.conf.i]
					&&"undefined"!==typeof u.d[SarvForm.conf.i][r]){
						var t=u.d[SarvForm.conf.i][r];
						this.sarv.defaults=[this.value,t];
						this.setValue(t)
					}else{
						var n=this;
						this.store.load({
							params:{id_to_page:this.value,isSetLabel:true},
							scope:this,
							callback:function(){
								n.setValue(n.value);	
								var b=n.displayTplData[0],
									a=("undefined"!==typeof b)?b.value:null;
								n.sarv.defaults=[n.value,a]
							}
						})
					}
				}
			}
		}else{
			var s=o.editingPlugin.rowIdx,
				q=o.store.getAt(s);
			try{
				this.value=q.data[this.name]
			}catch(e){}
			var n=this;
			this.store.load({
				params:{
					id_to_page:this.sarv.defaults[0], //this.value,
					isSetLabel:true
				},
				scope:this,
				callback:function(){
					n.setValue(n.value);
					var a=n.displayTplData[0];
					try{
						n.sarv.defaults=[n.value,a.value]
					}catch(b){}
				}
			})
		}
	},
	listeners:{
		expand:function(f){
			this.sarv.isExpandEvent=true;
			var h=this.up("sarv-grid-panel");
			if(!h){
				var g=f.store.data.items;
				for(var d=g.length;d--;){
					if(g[d].data.name==f.value){
						return;
					}
				}
				// No need to duplicate loading as there is 
				// default loading anyway. Just pass correct
				// extra params to proxy.
				//f.store.load({
				//	params:{id_to_page:f.sarv.defaults[0],isSetLabel:true}
				//})
				f.store.proxy.extraParams.id_to_page=f.sarv.defaults[0];
				f.store.proxy.extraParams.isSetLabel=true;
			}
		},
		select:function(){
			var b=this.displayTplData[0];
			this.sarv.defaults=[b.name,b.value];
			this.sarv.isTyped=false
		},
		blur:function(){
			if(this.sarv.isTyped){
				if(this.rawValue==""
				&&this.sarv.defaults!=""
				&&this.sarv.defaults!=null){
					this.sarv.defaults=[null,null];
					this.sarv.isTyped=false;
					return;
				}
				this.reset();
				this.setLabel();
				this.sarv.isTyped=false
			}
		},
		keypress:function(b){
			b.sarv.isTyped=true
		},	
		change:function(e,d,f){
			if(!e.sarv.isTyped||(String(d)&&d.length<e.minChars)){
				return;
			}
		}
	},
	enableKeyEvents:true
});						this.proxy.extraParams.gridname=a.name
