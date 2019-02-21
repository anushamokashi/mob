import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { ViewController } from 'ionic-angular';
import { Injector } from '@angular/core';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { PopoverController } from 'ionic-angular';
import { PagenavProvider } from '../../providers/pagenav/pagenav';
import { HomePage } from '../home/home';
import { PopoverPage } from '../searchmodal/popover';
import { Http,Headers } from '@angular/http';

/**
 * Generated class for the SearchmodalPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-searchmodal',
  templateUrl: 'searchmodal.html',
})
export class SearchmodalPage {
	searchQuery: string = '';
    items: any;
    public pagingEnabled: boolean = true;
    jsonUrl :any;
	viewjson :any;
    txservice :any;
	pid :any;
    searchJson:any;
	field_names:any;
	parent_tableid:any;
	UserDetails:any;
	pagenav:any;
	searchfield:any;
	optionsJson:any;
	ismultitenant:any;

  constructor(public navCtrl: NavController, public navParams: NavParams,public viewCtrl: ViewController,public http: Http,public popoverCtrl: PopoverController,public singleton: SingletonProvider,private injector: Injector) {
	  this.pagenav = this.injector.get(PagenavProvider);
	  this.txservice = navParams.get('txservice');
	  this.jsonUrl = navParams.get('jsonUrl');
	  this.UserDetails = navParams.get('userDetails');
	  this.optionsJson = navParams.get('selectoptions');
	  this.pid = this.singleton.PID;
	  this.ismultitenant = this.singleton.ismultitenant;
	  this.initializeItems();
	 
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad SearchmodalPage');
  }
	
	dismissModal() {
		this.UserDetails['editMode'] = undefined;
		this.UserDetails['modifyMode'] = undefined;
		this.UserDetails['recordId'] = "";
		this.UserDetails['dataSet'] = [];
		this.viewCtrl.dismiss( this.UserDetails);
 }

  initializeItems() {
	   this.http.get(this.jsonUrl).map(res => res.json()).subscribe(data => {
		   this.viewjson = data;
		   let sql ="";
		   let sort_field = "";
		   let sort_type ="";
		   let chunk_size :any;
		   console.log(this.viewjson);
		   let action_meta = this.viewjson[0]['action_meta'];
		   let parent_table = data[0]['tran_meta'][0]["prm_meta"][0]['tb'];
		   this.parent_tableid = parent_table+'id';
		   const filter = action_meta.filter((item) => {
											 return (item['at'].toLocaleLowerCase() == 'search');
											 });
		   
		   console.log(filter);
		   if(filter.length >0){
			   let search  = filter[0]['search'];
			   sql = search['Sql'].replace(/;/g, "");
			   this.searchfield = search['sc'];
			   this.field_names = JSON.parse(search['pam']);
			   chunk_size = parseInt(search['cs'])
			   sort_field = search['sf'];
			   if(search['st'] == "ascending"){
				   sort_type = 'ASC';
			   }
			   else{
			      sort_type = 'DESC';
			    }
			   this.searchJson ={
				   'sql' : sql,
				   'se_f': this.searchfield,
				   'so_f': sort_field,
				   'st_e': 0,
				   'cs'  : chunk_size,
				   'st'  : sort_type,
				   'pid': this.pid,
				   'mode': 'default',
				   's_value':'',
				   'mlt': this.ismultitenant
			   };
			   
			   this.txservice.sendSearchjson(this.searchJson).subscribe(response => {
				   this.items = JSON.parse(response._body);
			   
			   });			   
		   }
		   
	  });

  }

  presentPopover(myEvent) {
	  console.log(myEvent);
	  let recordId = myEvent['target']['dataset']['recordid'];
	  let popover = this.popoverCtrl.create(PopoverPage,{jsonUrl:this.jsonUrl,recordId:recordId,txservice:this.txservice,userDetails:this.UserDetails,pagenav:this.pagenav,selectoptions:this.optionsJson});
	  popover.present({
		  ev: myEvent
	  });
  }
		
 getItems(ev: any) {
    // Reset items back to all of the items
	 console.log(this.items);

    // set val to the value of the searchbar
    const val = ev.target.value;
   if(val != undefined){
    // if the value is an empty string don't filter the items
    if (val.length >= 3 && val.trim() != '') {
		this.pagingEnabled = true;
		  this.items =[];
		  this.searchJson['mode'] = 'search';
		  this.searchJson['st_e'] = 0;
		  this.searchJson['s_value'] = val;
		  this.txservice.sendSearchjson(this.searchJson).subscribe(response => {
			  let item_list =  JSON.parse(response._body);
			  if(item_list.length >0){
			  for(let i= 0;i<item_list.length;i++){
				  this.items.push(item_list[i]);
			  }
			  }
			   });
      //this.items = this.items.filter((item) => {
		//  let value;
		  //if(isNaN(item['DOC ID']) == false){
			//  value = item['DOC ID'].toString();
		  //}
		  //else{
			//    value = item['DOC ID']
		  //}
        //return (value.toLowerCase().indexOf(val.toLowerCase()) > -1);
      //})
    }
	   else if(val.trim() == ''){
		   this.pagingEnabled = true;
		   this.initializeItems();
	   
	   
	   }
  }
 }

doInfinite(infiniteScroll: any){
    console.log('Begin async operation');
	this.searchJson['st_e'] = this.items.length+1;
	setTimeout(() => {
		  this.txservice.sendSearchjson(this.searchJson).subscribe(response => {
			  let item_list =  JSON.parse(response._body);
			  if(item_list.length >0){
			  for(let i= 0;i<item_list.length;i++){
				  this.items.push(item_list[i]);
			  }
			  }
			  else{
			    this.pagingEnabled = false;
			  }
			   infiniteScroll.complete();
			   });
		
		 }, 500);
	
  }


onCancel($event){
	this.pagingEnabled = true;
	this.initializeItems();
}
	
}

