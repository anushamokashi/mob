import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { Http } from '@angular/http';
import { AlertController } from 'ionic-angular';
import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
import { SQLitePorter } from '@ionic-native/sqlite-porter';
import { ActionSheetController } from 'ionic-angular'
import { Storage } from '@ionic/storage';

import { NotifyProvider } from '../../providers/notify/notify';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { PagenavProvider } from '../../providers/pagenav/pagenav';
import { ExpressionProvider } from '../../providers/expression/expression';
import { Injector } from '@angular/core';

/**
 * Generated class for the NotificationPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-notification',
  templateUrl: 'notification.html',
  providers:[ExpressionProvider],
})
export class NotificationPage {
    UserDetails:any;
    msgArray = [];
    buttonArray : object = {};
    pagenav:any;
    constructor(public navCtrl: NavController, public navParams: NavParams,private sqlite: SQLite,
        public notifyProvider:NotifyProvider,public actionSheetCtrl: ActionSheetController,private sqlitePorter: SQLitePorter,
        public singleton: SingletonProvider,public http: Http,private alertCtrl: AlertController,
        public storage: Storage,private injector: Injector,public myexpression: ExpressionProvider) {
            this.UserDetails = this.navParams.get("userdetails");
            this.pagenav = this.injector.get(PagenavProvider);
            if (this.UserDetails == undefined) {
                this.storage.get('userObj').then((loginInfo) => {
                    this.UserDetails = 	loginInfo;
                    this.UserDetails['pagetype'] = 'txview';
                });

            }
            else{
                this.UserDetails['pagetype'] = 'txview';//for differentiate transaction or report in expr.js
            }
            
            
    }

  ionViewDidLoad() {
        console.log('ionViewDidLoad NotificationPage');
        let items = [];
        let tbmeta = {};
        let masterdata = [];
        let roleJson = {
            "ROLE" : this.singleton.role,
            "USERNAME" : this.UserDetails["USERNAME"]
        }
        this.notifyProvider.getNotificationMsg(roleJson).subscribe(response => {
            console.log(response);
            let Messages =response.json();
            for(let i=0;i<Messages.length;i++){
                Messages[i]['json'] = JSON.parse(Messages[i]['json']);
            }
            this.msgArray = Messages;
        });
    
    }
    
    processButtonAction(event,stage,currentNotifcationMsg){
        console.log(stage);
        this.UserDetails['recordId'] = currentNotifcationMsg.basicid;
        
        if (stage.rl == this,this.singleton.role){

            if(stage.ae == "notify()"){
                let msg: String;
                let musername : String;
    
                if(stage.msg == ""){
                    msg = currentNotifcationMsg.msg;
                }
                else{
                    msg = stage.msg
                }

                if(stage["uf"]){
                    musername = (<HTMLInputElement>document.getElementById(stage["uf"])).value
                }else{
                    musername = ""
                }
                
                let notifyJson = {
                    "ROLE" : stage.rl,
                    "FROMDATE" : currentNotifcationMsg.from_date.split('-').reverse().join('/'),
                    "TODATE" : currentNotifcationMsg.to_date.split('-').reverse().join('/'), 
                    "BASICID" : currentNotifcationMsg.basicid,
                    "USERNAME" : musername,
                    "MSG" :  msg,
                    "JSON": stage,
                    "APPID" : this.singleton.apikey,
    
                }
                this.notifyProvider.updateNotificationStatus(notifyJson).subscribe(Msgdata => {
                    let result = Msgdata.text();
                    console.log(result);
                });
                
            }
    
            if(stage.ae == "reject()"){
    
                let alert = this.alertCtrl.create({
                    title: 'Confirm Delete?',
                    buttons: [
                      {
                        text: 'Cancel',
                        role: 'cancel',
                        handler: () => {
                          console.log('Cancel clicked');
                        }
                      },
                      {
                        text: 'Okay',
                        handler: () => {
                          console.log('Buy clicked');
                          event.path[4].remove();
                          let id = currentNotifcationMsg.id;
                          let delJson = {
                              "ID" : id,
                          }
                         
                          this.notifyProvider.deleteNotification(delJson);
                        }
                      }
                    ]
                  });
                  alert.present();
                
            }
    
            if(stage.ae.includes("viewtxn") || stage.ae.includes("viewreport")){
                let txnViewpage;
                let transacionview = stage.ae.substring(
                    stage.ae.lastIndexOf("(") + 1, 
                    stage.ae.lastIndexOf(")")
                );
                if(stage.ae.includes("viewtxn")){
                    let txnviewArray = transacionview.split(",");
                    if(txnviewArray[1].toUpperCase( ) == "N"){
                        this.UserDetails['viewMode'] = false;
                        this.UserDetails['modifyMode'] = false;
                    }else if (txnviewArray[1].toUpperCase( ) == "V"){
                        this.UserDetails['viewMode'] = true;
                        this.UserDetails['modifyMode'] = false;
                    }else if (txnviewArray[1].toUpperCase( ) == "M"){
                        this.UserDetails['modifyMode'] = true;
                        this.UserDetails['viewMode'] = true;
                    }
                    for (let i=0;i<this.pagenav.pages.length;i++){
                        if(this.pagenav.pages[i]['id'] == txnviewArray[0]){
                            txnViewpage = this.pagenav.pages[i]['component'];
        
                        }
        
                    }
                }else if(stage.ae.includes("viewreport")){
                    for (let i=0;i<this.pagenav.pages.length;i++){
                        if(this.pagenav.pages[i]['id'] == transacionview){
                            txnViewpage = this.pagenav.pages[i]['component'];
        
                        }
        
                    }

                }
                
                this.navCtrl.push(txnViewpage,{'userdetails':this.UserDetails}).then(() => {
                    const startIndex = this.navCtrl.getActive().index - 1;
                    this.navCtrl.remove(startIndex, 1);
                });
    
    
            }
            if(stage.ae.toLocaleLowerCase().includes("firesql")){
                let resultSet = this.myexpression.evaluateEventexp(stage.ae, this.UserDetails, stage.sp);

            }

        }

        

    }

    
    
    buttonClick(event){
        console.log(event);
        let currentNotifcationMsg = {
            'basicid' : event.currentTarget.dataset['basicid'],
            'from_date' : event.currentTarget.dataset['fromdate'],
            'to_date' : event.currentTarget.dataset['todate'],
            'msg' : event.currentTarget.dataset['msg'],
            'id' : event.currentTarget.dataset['notificationbasicid']

        }
        
        let currentStage;
        let configured_notification =  event.currentTarget.dataset['congfigurednotification']
        let congfigured_stage = event.currentTarget.dataset['configuredstage']
        this.http.get('assets/json/notification.json').map(res => res.json()).subscribe(data => {
            for(let i=0;i<data.length;i++){
                if (data[i].title == configured_notification){
                    let notificationJson = data[i];
                    let stages = notificationJson.config;
                    
                    for(let j=0;j<stages.length;j++){
                        if (stages[j].sname == congfigured_stage){
                            currentStage = stages[j];
                            this.processButtonAction(event,currentStage,currentNotifcationMsg);
                            break;
                        }

                    }
                }

            }

        });


    }
 
    messagetoggle(event){
        var x = document.getElementById("message");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
    sendNotfication(){
        let textarea ="";
        textarea = document.getElementById('messagearea').getElementsByTagName("textarea")[0].value
        this.notifyProvider.notification(textarea).subscribe(response => {
            console.log(response);
        });
    }
}
 
