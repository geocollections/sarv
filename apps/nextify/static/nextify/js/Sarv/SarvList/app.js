/*
 * This file is generated and updated by Sencha Cmd. You can edit this file as
 * needed for your application, but these edits will have to be merged by
 * Sencha Cmd when upgrading.
 */

Ext.require(['SarvList.*']);
Ext.Ajax.request({
    url: 'records',
    params: {
    	type: 'silent',
    },
    success: function(response){
        records = JSON.parse(response.responseText);
		Ext.application({
		    name: 'SarvList',
		    extend: 'Ext.app.Application',
		    controllers:['Filter'],
		    autoCreateViewport: true,
		});
    }
});