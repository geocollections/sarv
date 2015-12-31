/*
 * This file is generated and updated by Sencha Cmd. You can edit this file as
 * needed for your application, but these edits will have to be merged by
 * Sencha Cmd when upgrading.
 */
Ext.Loader.setConfig({enabled:true});

Ext.require([/*'Ext.ux.data.PagingMemoryProxy','Ext.ux.data.PagingStore',*/'SarvForm.*']);

Ext.application({
    name: 'SarvForm',
    extend: 'Ext.app.Application',
    appFolder: 'static/js/Sarv/SarvForm/app',
    controllers:['Record'],
    autoCreateViewport: 'SarvForm.view.RecordPage',
    launch: function() {
    	var b = SarvForm.conf.url_end == 'add' ?
    			{save: {enabled:true}} :
    			(SarvForm.isLocal ? {add:{}, save:{}, 'delete':{}, 'save-as':{}} :
    				{add:{}, save:{},'delete':{}, prev:{}, next:{}, 'save-as':{}});
        if("delete" in b 
        && (!SarvForm.conf.acl[3]
        ||SarvForm.conf.acl[3]=="own")){
            b["delete"] = null;
            delete b["delete"];
        }
    	this.controllers.items[0].setButtons(b);
    	Ext.Ajax.on('beforerequest', function(){ Ext.get('page-loader-mask').show(); }, Ext.getBody());
    	Ext.Ajax.on('requestcomplete', function(){ Ext.get('page-loader-mask').hide(); } ,Ext.getBody());
    	Ext.Ajax.on('requestexception', function(){ Ext.get('page-loader-mask').hide(); } , Ext.getBody());
    },
});
