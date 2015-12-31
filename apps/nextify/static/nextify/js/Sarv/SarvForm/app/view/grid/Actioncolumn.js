Ext.define("SarvForm.view.grid.Actioncolumn",{
	extend:"Ext.grid.column.Action",
	xtype:"sarv-grid-actioncolumn",
	sarv:{},
	width:20,
	items:[{
		getClass:function(d,e,f){return"undefined"===typeof f.data.id||isNaN(f.data.id)?"x-hide-display":"next"},}
	],
	handler:function(k,g){
		var j=k.grid.columns[0].sarv.urlpart,h=k.store.getAt(g).data.id;
		if(!opener||j.length<1){
			console.log("error")}
		if("undefined"===typeof h||isNaN(h)){
			return;
		}
		var f="/"+j+"/"+h;
		if(SarvForm.forms){
			SarvForm.forms.location=f
		} else {
			SarvForm.forms=window.open(f,"_blank","width="+(400)+",height="+(500)+",location=0,status=0,toolbar=0")
		}
	}
});
