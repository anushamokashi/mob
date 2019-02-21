import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { Http,Headers} from '@angular/http';
import { Storage } from '@ionic/storage';
import { ToastController } from 'ionic-angular';
import { AlertController } from 'ionic-angular';
import { LoadingController } from 'ionic-angular';
import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
import { SQLitePorter } from '@ionic-native/sqlite-porter';
import { SingletonProvider } from '../../providers/singleton/singleton';
import 'rxjs/add/operator/map';

import { HomePage } from '../home/home';
import { LoginPage } from '../login/login';
import { LoginserviceProvider } from '../../providers/loginservice/loginservice';


/**
 * Generated class for the SyncmasterPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-syncmaster',
  templateUrl: 'syncmaster.html',
})
export class SyncmasterPage {
    resturl: any;
    mdata: Object = {};
    coldata: Object = {};

    constructor(public navCtrl: NavController, public navParams: NavParams, private sqlitePorter: SQLitePorter, public loadingCtrl: LoadingController, private sqlite: SQLite, public http: Http, public storage: Storage, private toastCtrl: ToastController, public singleton: SingletonProvider, private alertCtrl: AlertController, public myservice: LoginserviceProvider) {
        this.resturl = this.singleton.resturl;
    }

    ionViewDidLoad() {
        let items = [];
        let tbmeta = {};
        let masterdata = [];
        console.log('ionViewDidLoad SyncmasterPage');
        this.sqlite.create({
            name: 'data.db',
            location: 'default'
        }).then((db: SQLiteObject) => {

            db.executeSql('select * from mastermap', {}).then((data) => {
                console.log(JSON.stringify(data));
                if (data.rows.length > 0) {
                    for (var i = 0; i < data.rows.length; i++) {
                        //alert(data.rows.item(i).name);
                        items.push({
                            ST: data.rows.item(i).stname,
                            TT: data.rows.item(i).ttname,
                            URL: data.rows.item(i).url,
                            OD: data.rows.item(i).orderno,
                            DP: data.rows.item(i).dependson,
                            MD: data.rows.item(i).moduleid,
                            WH: data.rows.item(i).wherecon
                        });
                        //items.push({PASSWORD: data.rows.item(i).password});
                        //items.push({USERID: data.rows.item(i).userid});
                        //items.push({PROJECTID: data.rows.item(i).pid});
                    }
                }
                for (let j = 0; j < items.length; j++) {
                    let fields;
					let tbcolumns;
                    fields = this.fielddata(items[j], db);
				    tbcolumns = this.column(items[j], db);
                    masterdata.push({
                        TBR: items[j],
                        FDR: fields,
						COL:tbcolumns
                    });
                    //tbmeta[items[j]['TT']] = [fields];	
                }
                //console.log(tbmeta);
                this.mdata = {
                    'Mapdata': masterdata,
                    'PID': this.singleton.PID
                }
            }).catch(e => console.log(e));

        }).catch(e => console.log(e));
    }

    logout() {
        this.navCtrl.setRoot(LoginPage);
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

    syncmaster() {
        const loading = this.loadingCtrl.create({
            spinner: 'hide',
            content: 'Downloading Please Wait...'
        });

        loading.present();
        this.myservice.sendMapjson(this.mdata).subscribe(response => {
                loading.dismiss();
                //this.tableinsertJson(response.json());
          let serverdata = response.json();
           if(serverdata[0].TYPE == 'SUCCESS'){
			      this.tableinsertSql(serverdata,loading);
           }else{
            loading.dismiss(); 
            let alert = this.alertCtrl.create({
                    title: 'Information',
                    subTitle: 'Please Contact System Admin(OR)Login after Sometime.',
                    buttons: ['OK']
                });
                alert.present();
           }
            },
            err => {
                 loading.dismiss();
                //console.log("Oops!");
                let alert = this.alertCtrl.create({
                    title: 'Information',
                    subTitle: 'Network Connection Error.Please Check',
                    buttons: ['OK']
                });
                alert.present();
                //return saveStatus;
            }

        );

    }


    fielddata(items, db) {
        let fields = [];
        db.executeSql('select * from mastermapdetail where moduleid =? ', [items['MD']]).then((data) => {
            if (data.rows.length > 0) {
                for (var i = 0; i < data.rows.length; i++) {
                    //alert(data.rows.item(i).name);
                    fields.push({
                        SF: data.rows.item(i).sfname,
                        TF: data.rows.item(i).tfname,
                        SI: data.rows.item(i).shortid
                    });
                    //items.push({PASSWORD: data.rows.item(i).password});
                    //items.push({USERID: data.rows.item(i).userid});
                    //items.push({PROJECTID: data.rows.item(i).pid});
                }
            }
        }).catch(e => console.log(e));
        return fields;
    }

 column(items, db){
	 let fields = [];
	 let tbcol ={};
   db.executeSql('PRAGMA table_info('+items['TT']+')',[]).then((data) => {
            if (data.rows.length > 0) {
                for (var i = 0; i < data.rows.length; i++) {
                    //alert(data.rows.item(i).name);
					fields.push(data.rows.item(i).name);
                    //items.push({PASSWORD: data.rows.item(i).password});
                    //items.push({USERID: data.rows.item(i).userid});
                    //items.push({PROJECTID: data.rows.item(i).pid});
                }
            }
        }).catch(e => console.log(e));
	 
	 this.sqlitePorter.exportDbToJson(db)
	.then((data) => console.log(data))
	.catch(e => console.error(e));
	 tbcol[items['TT']] = fields;
	 return tbcol;
 }

   // tableinsertJson(data) {
		//let insertvalue = {};
	 //for(let k=0;k<data[1].length;k++){
		//insertvalue["inserts"] = data[1][k];
		//}
		// let json = {
    //        "data": insertvalue
     //   };
		//console.log(json);
		  // this.sqlite.create({
       //     name: 'data.db',
       //     location: 'default'
      //  }).then((db: SQLiteObject) => {
		//this.sqlitePorter.importJsonToDb(db, json).then(() => {
		// this.datapresent(db);
		//}).catch(e => console.error(e));
      // }).catch(e => console.error(e));
	//}

    tableinsertSql(data,loading){
		console.log(data);
     let query =""; 
    let finalsql = []; 
     let sql = "";  
		for(let k=0;k<data[1].length;k++){
		let sqlstart ="";
		let sqlbody ="";  
		let kdata = data[1];	
		let key = Object.keys(kdata[k]);
		sqlstart = 'INSERT OR REPLACE INTO '+key+' SELECT ';
		for(let i=0;i<kdata[k][key[0]].length;i++){
			let rowdata = kdata[k][key[0]][i];
			let colname = this.mdata["Mapdata"][k]["COL"][key[0]];
			for(let j=0;j<colname.length;j++){
				let newdata ="";
				let sqlsubbody ="";
			if(j+1 == colname.length){
			 if(rowdata[colname[j]] == undefined){
			  newdata = "";
			 }
				else{
				newdata = rowdata[colname[j]];
				}
       if (i+1 == kdata[k][key[0]].length){
         sqlsubbody+= '"'+newdata+'"'+' AS '+'"'+ colname[j]+'"'; 
       }
        else{
			sqlsubbody+= '"'+newdata+'"'+' AS '+'"'+ colname[j]+'"'+' UNION SELECT '; 
        }
			}
			else{
				if(rowdata[colname[j]] == undefined){
			  newdata = "";
			 }
				else{
				newdata = rowdata[colname[j]];
				}
			sqlsubbody+=  '"'+newdata+'"'+' AS '+'"'+ colname[j]+'"'+',';  
			}
				sqlstart += sqlsubbody
			}
		}	
		
		sql = sqlstart;
   finalsql.push(sql);  
		}
		
     for(let a=0;a<finalsql.length;a++){
     query+= finalsql[a]+';';
     }
      if (query){
       this.sqlite.create({
            name: 'data.db',
            location: 'default'
        }).then((db: SQLiteObject) => {  
      this.sqlitePorter.importSqlToDb(db, query)
      .then(() =>{
      this.datapresent(db);
      this.redirectpage(db,loading);
      console.log('imported');  
      })
      .catch(e => console.error(e));
          }).catch(e => console.error(e));
      }
  }
 
 redirectpage(db,loading){
        loading.dismiss();
   db.executeSql('UPDATE control SET value=? WHERE key="sync"', ['true'])
      .then(() => {
      this.datapresent(db);
      console.log('Sync');  
      })
      .catch(e => console.log(e));
   this.navCtrl.setRoot(HomePage);
 }

 datapresent(db){
		this.sqlitePorter.exportDbToJson(db)
	.then((data) => console.log(data))
	.catch(e => console.error(e));
		
		var successFn = function(json, count){
        console.log("Exported JSON: "+json);
        alert("Exported JSON contains equivalent of "+count+" SQL statements");
    };
	}
}