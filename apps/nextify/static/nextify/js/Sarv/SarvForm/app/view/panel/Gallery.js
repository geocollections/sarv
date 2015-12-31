Ext.define("SarvForm.view.panel.Gallery",{
	extend:"Ext.panel.Panel",
	xtype:"sarv-gallery",
	sarv:{},
	constructor:function(g){
		this.sarv.model=Ext.create("SarvForm.model.Grid",{fields:f_l});
		var h=(g.pageSize||10),
			j=SarvForm.given._getGridData(SarvForm.conf.item_id,g.name),
			d=this,
			k=Ext.create("Ext.data.Store",{
				storeId:"store-"+g.name,model:this.sarv.model,
				autoDestroy:true,
				pageSize:h,	
				proxy:{
					enablePaging:true,
					model:this.sarv.model,
					type:"memory",
					reader:{type:"json",root:"items",idProperty:"id"}},
				data:{items:j},
				loadRawData:function(a,c){
					var b=this.proxy.reader.read(a),
						e=this;
					if(b.success){
						e.currentPage=1;
						e.totalCount=b.total;
						e.pageSize=h;
						e.proxy.data=b.records;
						e.sync();
						e.load()
					}
				}
			});
		g.items=Ext.create("Ext.view.View",{
			store:k,
			tpl:[g.tpl],
			multiSelect:true,
			height:310,
			trackOver:true,
			overItemCls:"x-item-over",
			itemSelector:"div.thumb-wrap",
			emptyText:(g.txt.no-images||"No images to display"),
			plugins:[],
			prepareData:function(a){
				Ext.apply(a,{});
				return a
			},
			listeners:{
				selectionchange:function(b,c){
					var e=c.length,
						a=e!==1?"s":"";
					this.up("panel").setTitle("Simple DataView ("+e+" item"+a+" selected)")
				}
			}
		});
		this.initConfig(g);
		this.callParent(arguments)
	}
});
