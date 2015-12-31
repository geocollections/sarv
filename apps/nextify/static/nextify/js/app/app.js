/**
 * GI
 */

var Sarv = ({
		
	// * Form record structure
	// * d - data; f - fields; g - grids;
	// * rsl - labels for remote stores
	records: {
		d:[], 
		f:[], 
		g:{}
	}
	
	// Popup window record view data structure (config)
	// Child popup window config and data is preloaded.
	// 
	, form: {
		formFields:[],
		stores:{
			data:{}
		}
	}
	
	// Form instances (currently there's one instance per parent page)
	, forms: null

	//
	, _openPopup: function(c, id, no_rel) {
		var c=c||this.conf,
			no_rel=(no_rel||false);
		if(id == 'add' && this.forms != null){
			if(this.forms.SarvForm.conf.url_end=='add') 
				return;
			this.forms.SarvForm.app
				.controllers.items[0].add();
		} else {
 			var w_o = window.open(id+(no_rel?'':'?o'), '_blank',
 	    		'width='+(c.popup.width ? c.popup.width : 400)+
 	    		',height='+(c.popup.height? c.popup.height : 500)+
 	    		',location=0,status=0,toolbar=0');
 			if(!no_rel)
 				Sarv.forms=w_o;
 			// garbage collection
 			if(Sarv.forms!=null)
	 			Sarv.forms.addEventListener(
	 				'onbeforeunload', function(e){
	 					//carbage collection
	 					e.SarvForm.conf=null;
	 					e.SarvForm=null;
	 					e=null;
	 				}
	 			);
		}
	}
	
	//
	, _getFilterParams: function() {
		var d={fp:[],sort:'',records_per_page:0},
			g=Ext.getCmp('listgrid'),
			s=g.store,
			fs = Ext.getCmp('filtergrid').getStore().getRange(),
			fp = [];

		d.records_per_page = s.pageSize;
		for(var i=0,n=fs.length; i<n; i++){
			 var r = fs[i].data,
			 	 r_f = '',
			 	 ft = Sarv.conf.filters_types[r['filter_type']];
			 	 if('undefined'===typeof ft)
			 		 continue;
			 for(var j=0, n_ = ft.length; j<n_; j++) {
				 if(ft[j][1] == r['filter'])
					 r_f = ft[j][0];
			 }
		     fp.push([Sarv.conf.fields_verbosenames[
		     	r['field']], r_f, r['filter_type'], r['value']]);
		}
		d.fp=fp;

		if(s.getSorters().length > 0) {
			d.sort=JSON.stringify(s.getSorters());
		}

		if("undefined" !== typeof s.proxy.extraParams.myresults)
			d.myresults = s.proxy.extraParams.myresults;

		return d;
	}

	// {add} (opt): -1 - prev, +1 - next page 
	// {rA} (opt): index of selected row
	// {a} (opt): if true, then {add} is absolute page nr
	// {f} (opt): closure that fires with callback
	, _listGridPageTurner: function(add, rA, a, f) {
		var g=Ext.getCmp('listgrid'),
			s=g.store;
		if(add !== null) {
			var nr=a ? 0 : s.lastOptions.page;
			// if rA is present while new page is loaded,
			// use that rA to select active record after
			// the page has been turned
			// Used by child controller method 'cancel' 
			// for example.
			rA = (isNaN(rA) || rA === null) ? false : rA;
			if(!rA)
				rA = (!rA && add !== null) ? rA : null;
			if(!rA || isNaN(rA))
				rA = (add > 0) ? 0 : (s.pageSize-1);
			s.loadPage((nr + add), {
				scope: this,
				callback: function() {
					this._listGridPageTurner(null, rA);
					if(f) {
						f();
					}
				}
			}); 				
		}
		if(!isNaN(rA) && rA !== null) {
			g.getSelectionModel()
				.select(rA);
		}
		return true;
	}
	
	// Removes select from list grid
	// 
	, _listGridDeselectAll: function() {
		var g = Ext.getCmp('listgrid');
		g.getSelectionModel().deselectAll();
	}

	// When a record is updated via form page
	// this function is called to update 
	// list grid
	, _refreshGrid: function(callback) {
		var s = Ext.getCmp('listgrid').getStore();
		s.loadPage(s.currentPage);
		if('undefined' !== typeof callback) {
			var args='undefined' !== typeof callback.args ?
					callback.args : null;
			if('undefined' !== typeof callback['return'])
				return callback.fn(args);
			else
				callback.fn(args);
		}
	}
	 		
	// DATA MANAGEMENT
	
	// Child popup window data loader
	, _formConfLoader: function() {
		Ext.Ajax.request({
			url: 'form_page_conf',
			scope: this,
			success: function (r) {
				var d = JSON.parse(r.responseText);
				this.form.stores.data = d['stores'];
				this.form.formFields = d['formFields'];
				this.form.user = d['user'];
				this.form.urls = d['urls'];
				this.form.title = d['title'];
				if('undefined' !== typeof d['download_url'])
					this.form.download_url = d['download_url'];
			},
			failure: function (r) {console.log(f);}
		});
	}
	
	// Child popup window stores' content loader
	, _storeManager: function(idp,idr,cn,dk) {
		var t=this;
		if(!(cn||false))
			Ext.Ajax.request({
				url: 'stores',
				scope: this,
				success: function (r) {
					this.stores.data = JSON.parse(r.responseText);
				},
				failure: function(f){console.log(f);}
			});
	}
	
	//
	, _getGridData: function(id,name) {
		// data is present as grid records + reference -
		var d=[],
			g=(this.records.g[name]||{}),
			m=(g.m[id]||false);

		if(m) {
			for(var i=0,n=m.length;i<n;i++){
				try {
					var rec={'id':m[i]};
					for(var j=0,l=g.r[m[i]].length;j<l;j++) {// records
						rec[g.f[j]]=g.r[m[i]][j];
					}
					d.push(rec);
				} catch (e) {
					console.log(e);
				}
			}
		}
		return d;
	}
	
	//
	, _setGridData: function() {
		Ext.Ajax.request({
			url: 'grids',
			params: {k:JSON.stringify(keys)},
			scope: this,
			success: function (r) {
				var g=JSON.parse(r.responseText);
				for(var i in g) {
					t_.records.g[i] = g[i];
					var h=g[i].f.indexOf('id');
					if (h!==-1) {
					    t_.records.g[i].f[h] = 'id_';
					}
				}
			},
			failure: function(f){
				console.log(f);
			}
		});
	}
	
			
	// {message} - form messaging. Used throughout 
	// the form lifecycle.
	, message: function(d) {
		var o=document.getElementById('page-messagebox'),
			i=document.getElementById('page-messagebox-inner');
		if (d.success) {
			o.style.backgroundColor='#bfa';
			o.style.zIndex=100;
			i.style.color='#5a3';
		} 
		if (d.error) {
			o.style.backgroundColor='#fab';
			o.style.zIndex=100;
			i.style.color='#700';
		}
		if (typeof d.data === 'undefined') 
			d.data=[];
		var h=d.message+'<ul>';
		for(var j=0, n=d.data.length; j<n; j++)
			h+='<li style="margin-top:5px">'+d.data[j]+'</li>';
		i.innerHTML+=h+'</ul>';
		o.style.display='block';
		o.style.opacity=1;
		var t_=this,
			t=setInterval(function(){ 
				clearInterval(t);
				t_.fade(o,i);
			}, 3000);
		d=null;
		h=null;
	}
	
	, fade: function(e,i) {
	    var op = 1;  // initial opacity
	    var timer = setInterval(function () {
	        if (op <= 0.1){
	            clearInterval(timer);
	            e.style.filter='alpha(opacity=1)';
	            e.style.display = 'none';
	            i.innerHTML='';
	        }
	        e.style.opacity = op;
	        e.style.filter = 'alpha(opacity=' + op * 100 + ')';
	        op -= op * 0.1;
	    }, 50);
	}
	

	// UTILS
	
	, _d: function(i,type) {
    	var t=(type||'undefined'),
    		x=(t===typeof i);
    	//if type is checkeg against undefined
    	//return inverted value
    	return t=='undefined'?(!x):x;
    }
}||{});

//
//Application
//

Ext.suspendLayouts();
Ext.application({
    name: 'Sarv',
    appFolder: 'static/js/app',
    autoCreateViewport: 'Sarv.view.Viewport', //true,
    controllers: ['List'],
    launch: function() {
    	if(Sarv.form) {
    		Sarv.form.acl = Sarv.conf.acl;
    		Sarv._formConfLoader();
        }
    	
    }
});
Ext.resumeLayouts(true);

function deleteGridRow(item_id) {
	var store = Ext.getCmp('genericgrid').getStore();
	var record = store.findRecord('id', item_id);
	store.remove(record);
}

