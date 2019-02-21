import { Component } from '@angular/core';
import { NavController, NavParams, Platform } from 'ionic-angular';
import { Http } from '@angular/http';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { Storage } from '@ionic/storage';
import { ToastController } from 'ionic-angular';
import { AlertController } from 'ionic-angular';
import 'rxjs/add/operator/map';

import { HomePage } from '../home/home';

/**
 * Generated class for the Grid page.
 *
 * See http://ionicframework.com/docs/components/#navigation for more info
 * on Ionic pages and navigation.
 */

@Component({
  selector: 'page-grid',
  templateUrl: 'grid.html',
})
export class GridPage {
 
  grid : any;
  userdetails : any;
  public alertShown:boolean = false;
  
  constructor(public navCtrl: NavController, public navParams: NavParams,public http: Http,public storage:Storage,private toastCtrl: ToastController,public platform: Platform,public singleton:SingletonProvider,public alertCtrl: AlertController) {
	  //array pages for grid menu 
      this.userdetails = navParams.get("userdetails");
      
  }
  
 openPage(page) {
    // Reset the content nav to have just this page
    // we wouldn't want the back button to show in this scenario 
    this.navCtrl.push(page.component,{'userdetails':this.userdetails});
  }
 
 ionViewDidEnter() {
	this.platform.registerBackButtonAction(() => {
			if (this.alertShown==false) {
			  this.presentConfirm();  
			}
		  }, 0)
	}

 ionViewWillLeave() {
		this.platform.registerBackButtonAction(() => {
			this.navCtrl.pop();
		});
	}

logout(){
 this.navCtrl.setRoot(HomePage);
   let toast = this.toastCtrl.create({
    message: 'User Logged Out Successfully',
    duration: 3000,
    position: 'bottom'
  });

  toast.onDidDismiss(() => {
    console.log('Dismissed toast');
  });

  toast.present();	 
 }

  presentConfirm() {
    let alert = this.alertCtrl.create({
      title: 'Confirm Exit',
      message: 'Do you want Exit?',
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel',
          handler: () => {
            console.log('Cancel clicked');
            this.alertShown=false;
          }
        },
        {
          text: 'Yes',
          handler: () => {
            console.log('Yes clicked');
            this.platform.exitApp();
          }
        }
      ]
    });
     alert.present().then(()=>{
      this.alertShown=true;
    });
  }
}
