//if(records.settings.pagesize == 'undefined') {
//	records.settings.pagesize = 30;
//}

Ext.define('SarvList.store.GenericGridStore', {
    extend: 'Ext.data.Store',
    requires: ['SarvList.model.GenericGridModel'],
    model: 'SarvList.model.GenericGridModel',
    pageSize: typeof records.settings.pagesize == 'undefined' ? 30 : records.settings.pagesize,
    autoLoad: false,
    //autoLoad: { params: { start: 0, limit: 30 } }, //on pageload add records
    //autoLoad: 'undefined'!== typeof records.settings.autoload?true:false,
    remoteSort: true,
    buffered: false,
    listeners: {
    	//beforeload: function() { console.log('tt'); } 
    },
    
    proxy: {
    	actionMethods: {
            create: 'GET',
            read: 'GET',
            update: 'GET',
            destroy: 'GET',
        },
        
        type: 'ajax',
        url: 'records',
        reader: {
            type: 'json',
            totalProperty: 'records_total',
            root: 'records'
        },
    },
});
