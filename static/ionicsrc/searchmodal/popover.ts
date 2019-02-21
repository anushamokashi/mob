import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { Http,Headers } from '@angular/http';
import { HomePage } from '../home/home';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { Item_avaliable_txnPage } from '../item_avaliable_txn/item_avaliable_txn';

/**
 * Generated class for the PopoverPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-popover',
  templateUrl: 'popover.html',
})
export class PopoverPage {
	jsonUrl:any;
	txservice:any;
	recordId:any;
	pid:any;
	parent_tableid:any;
	UserDetails:any;
	pagenav:any;
	optionsJson:any;

  constructor(public navCtrl: NavController, public navParams: NavParams,public http: Http,public singleton: SingletonProvider) {
	  this.txservice = navParams.get('txservice');
	  this.jsonUrl = navParams.get('jsonUrl');
	  this.recordId = navParams.get('recordId');
	  this.UserDetails = navParams.get('userDetails');
	  this.pagenav = navParams.get('pagenav')
	  this.optionsJson = navParams.get('selectoptions');
	  this.pid = this.singleton.PID;
	  console.log(this.jsonUrl);
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad PopoverPage');
  }

	view($event){
		this.UserDetails['viewMode'] = true;
		this.UserDetails['optionJson'] = this.optionsJson;
		this.UserDetails['recordId'] = this.recordId;
		if($event =="modify"){
			this.UserDetails['modifyMode'] = true;
		}
		else{
			this.UserDetails['modifyMode'] = false;
		}
		this.http.get(this.jsonUrl).map(res => res.json()).subscribe(data => {
			let tx_id = data[0]['idt'];
			console.log(this.pagenav);
			const page_filter = this.pagenav['pages'].filter((item) => {
				return (item['id'] == tx_id);
			});
			this.navCtrl.push(page_filter[0]['component'],{userdetails:this.UserDetails});
		});
	
	
	}
}
