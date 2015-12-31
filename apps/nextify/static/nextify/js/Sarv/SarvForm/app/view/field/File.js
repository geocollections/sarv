Ext.define("SarvForm.view.field.File",{
	extend:"Ext.form.field.Text",
	xtype:"sarv-file",
	sarv:{},
	border:0,
	autoDestroy:true,
	constructor: function(b){
		b.fieldSubTpl=['<div id="'+b.name+'-dd-dropzone" class="{fieldCls} dd-dropzone">',
			'<img class="dd-icon"/>',
			'<div class="dd-prgr" style=""></div>',
			'<input id="{id}" type="{type}" ',
			'<tpl if="name">name="{name}" </tpl>',
			'<tpl if="size">size="{size}" </tpl>',
			'<tpl if="tabIdx">tabIndex="{tabIdx}" </tpl>',
			'class="{fieldCls} {typeCls} dd-file-name"',
			"readonly /></div>",
			{
				compiled:true,
				disableFormats:true
		}];
		this.initConfig(b);
		this.callParent(arguments)
	}
});
