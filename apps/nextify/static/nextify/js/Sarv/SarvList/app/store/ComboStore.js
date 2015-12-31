Ext.define('Ext.data.Store',{
	fields: ['name','value'],
    proxy: {
        type: 'ajax',
        autoLoad: true,
        url: 'store?field=',
        reader: {
        	type: 'json',
            root: 'store_records',
            totalProperty: 'store_record_count',
        },
    },
    pageSize:10,
    autoDestroy: true
});