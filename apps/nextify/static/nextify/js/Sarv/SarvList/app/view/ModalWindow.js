Ext.define('SarvList.view.ModalWindow', {
	extend: 'Ext.window.Window',
	alias: 'widget.modalwindow',
	requires: ['SarvList.view.GenericContent'],
	title: 'Generic',
	border: 0,
	width: 900,
	closable:false,
	align: 'center',
	items: [{ 
		xtype: 'genericcontent',
		border:0,
	}]
});
