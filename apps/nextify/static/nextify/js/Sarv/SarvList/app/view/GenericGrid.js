Ext.define('SarvList.view.GenericGrid', {
    extend: 'Ext.grid.Panel',
    requires: ['SarvList.store.GenericGridStore'],
    alias: 'widget.genericgrid',
    id: 'genericgrid',
    viewConfig: {
	    listeners: {
	    	load: function() { 
	    		this.getColumnModel().setHidden(0, true); 
	    	}, 
	    	/*
	    	itemclick: function(dataview, record, item, e) {
	    		clicked = 'undefined' !== typeof(clicked) ? clicked : false;
	    		locked = 'undefined' !== typeof(locked) ? locked : false;
		    	if (!locked) {
		    		window.setTimeout(function() {
		    			function open_popup (record,settings) {
		    				childPopupWindow[record.get('id')] = window.open(record.get('id'),'_blank',
					    			'width='+(settings.popup.width?settings.popup.width:400)+
					    			',height='+(settings.popup.height?settings.popup.height:500)+
					    			',location=0,status=0,toolbar=0');
		    			}
			    		if (clicked) open_popup(record,records.settings); //dblclick
			    		else { //click
			    			var child_ids = [];
			    			for (var child_id in childPopupWindow) {
			    				if(childPopupWindow[child_id].closed)
			    					delete childPopupWindow[child_id];
			    				else child_ids.push(child_id); 
			    			}
			    			if (child_ids.length < 1) 
			    				open_popup(record,records.settings);
			    			else childPopupWindow[child_ids[0]].parentCallback(record.get('id'));
			    			
			    		}
			    		clicked = false;
			    		locked = false;
			    	}, 400);
		    		locked = true;
		    	} else clicked = locked ? true : false;
		    	
	    	},
	    	itemdblclick: function() { console.log('d'); return false; }
	    	*/
	    	//itemdblclick: function(dataview, record, item, e) {
	    	//	childPopupWindow[record.get('id')] = window.open(record.get('id'),'_blank',
	    	//			'width='+(records.settings.popup.width?records.settings.popup.width:400)+
	    	//			',height='+(records.settings.popup.height?records.settings.popup.height:500)+
	    	//			',location=0,status=0,toolbar=0');
	        //}
	    }
    },
    columns: records.columns,
    store: 'GenericGridStore',   
   	dockedItems: [{
        xtype: 'pagingtoolbar',
        store: 'GenericGridStore',
        dock: 'bottom',
        displayInfo: true,
        viewConfig: { loadMask: true },
    }],
    
});
