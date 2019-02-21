import { Component, ViewChild  } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { Http } from '@angular/http';
import { Network } from '@ionic-native/network';
import { AlertController } from 'ionic-angular';
import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
import { SQLitePorter } from '@ionic-native/sqlite-porter';
import { OneSignal } from '@ionic-native/onesignal';
import { Events } from 'ionic-angular';

/* import { Userinfo } from '../../providers/userinfo/userinfo'; */
import { LoginserviceProvider } from '../../providers/loginservice/loginservice';
import { ToastController } from 'ionic-angular';
import { LoadingController } from 'ionic-angular';
import { SyncmasterPage } from '../syncmaster/syncmaster';
import { SidemenuPage } from '../sidemenu/sidemenu';
import { HomePage } from '../home/home';
import { Uid } from '@ionic-native/uid';
import { AndroidPermissions } from '@ionic-native/android-permissions';

/**
 * Generated class for the LoginPage page.
 *
 * See http://ionicframework.com/docs/components/#navigation for more info
 * on Ionic pages and navigation.
 */
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
  providers:[ LoginserviceProvider ],
})
export class LoginPage {
	
	private options = { name: "data.db", location: 'default', createFromLocation: 1 }; 
  	networkStatus:any;
	sqlString : any;
    database : any;
    syncstatus : any;
	playerID : any;
	responseOtp : any;
	

	constructor(public navCtrl: NavController,private sqlitePorter: SQLitePorter,private alertCtrl: AlertController, private network: Network,private sqlite: SQLite, public navParams: NavParams,public http: Http, 
		public storage: Storage,public toastCtrl: ToastController,public events: Events,private oneSignal: OneSignal,public loadingCtrl: LoadingController, public myservice: LoginserviceProvider, public singleton:SingletonProvider,
		public uid: Uid, public androidPermissions: AndroidPermissions) {
		this.storage.get('offStore').then((offlineStore) => {
		});
		let disconnectSubscription = this.network.onDisconnect().subscribe(() => {
			this.networkStatus = "offline";	
		});
		
		let connectSubscription = this.network.onConnect().subscribe(() => {
            this.networkStatus = "online";	});
		this.storage.get('database_filled').then((store) => {
		});
		this.copydb();
	    oneSignal.getIds().then((data)=> {
		this.playerID = data.userId;
		console.log(this.playerID);	
			}).catch(e =>{
		console.log(e);
		this.playerID="";
		});
	}

  	ionViewDidLoad() {
		  if(this.network.type == "none")
		  {
			const alert = this.alertCtrl.create({
			title: 'Network Status',
			message: 'Do you want to Continue Offline or Online ?',
			buttons: [
				{
					text: 'Offline',
					role: 'Offline',
					handler: () => {
					//console.log('Offline clicked');
					this.networkStatus = "offline";	
					}
				},
				{
					text: 'Online',
					handler: () => {
					//console.log('Buy Online');
					this.networkStatus = "online";	
					let alert = this.alertCtrl.create({
						title: 'Alert',
						subTitle: "Please Connect to Network.",
						buttons: ['Dismiss']
					});
					alert.present();
					
					}
				}
			]
  	});
  alert.present();
}
	}


customLogin(event) {
	
	let pid : any;
	let sql :any;
	let sqlParams : any;
	let loginType : any;
	let paramArray : any;
	let idArray : any[] = [];
	let testJson = {};
        this.playerID = "";
	this.oneSignal.getIds().then((data)=> {
		this.playerID = data.userId;
		console.log(this.playerID);	
			}).catch(e =>{
		console.log(e);
		this.playerID="";
		});
	loginType = event.currentTarget.dataset.logintype;
	sql=event.currentTarget.dataset.sql;
	sqlParams=event.currentTarget.dataset.sqlparams;
	pid = this.singleton.PID;

 	paramArray = sqlParams.split(',');

	for(let i=0; i<paramArray.length; i++){
		idArray.push("login_"+paramArray[i].toLowerCase()+"_id");
	}

		for(let j=0;j<paramArray.length; j++){
			if((document.getElementById(idArray[j]) as HTMLInputElement).value != ""){
				testJson[paramArray[j]] = (document.getElementById(idArray[j]) as HTMLInputElement).value;
			}
			else {
				alert ("Please Enter "+ paramArray[j].toLowerCase());
				return;
			}			
		}
		if (this.networkStatus =="offline"){
		//let offlineLogin = this.storage.get('userObj');
		console.log("offlineLogin");
		let offpassword = testJson["PASSWORD"];
		let offusername = testJson["USERNAME"];
		let items = [];	
		//console.log(testJson);
		this.sqlite.create({
					  name: 'data.db',
					  location: 'default'
						}).then((db: SQLiteObject) => {	

				db.executeSql('select * from muser where mobile_number =? and pwd =?', [offusername,offpassword]).then((data) => {
				//console.log(JSON.stringify(data));
				if(data.rows.length > 0) {
				for(var i = 0; i < data.rows.length; i++) {
				//alert(data.rows.item(i).name);
				items.push({USERNAME: data.rows.item(i).mobile_number,mobile_number: data.rows.item(i).mobile_number,first_name:data.rows.item(i).first_name,PASSWORD: data.rows.item(i).pwd,USERID: data.rows.item(i).muserid,ROLE:data.rows.item(i).role});
				//console.log(data.rows.item(i));	
				}
				}
				//console.log(items[0]);
				//console.log(items[0]['USERNAME']);
				  try {	
				if (offusername == items[0]['USERNAME'] &&  offpassword == items[0]['PASSWORD']){
					let role = items[0]['ROLE'];
					this.events.publish('user:role', role);
					this.singleton.role = role;
					this.toast(items[0],this.networkStatus);	
				//this.navCtrl.setRoot(TransactionPage,{'userdetails':items[0]});
				}
				  }
				catch (e) {
					this.successFailureToast("Username or Password is incorrect",3000);
				}	
				}).catch(e => console.log(e));
			 	db.executeSql('select * from control', {}).then((data) => {
						console.log(JSON.stringify(data));
						let items = [];
						if(data.rows.length > 0) {
						for(var i = 0; i < data.rows.length; i++) {
						//alert(data.rows.item(i).name);
						//items.push({USERNAME: data.rows.item(i).username,PASSWORD: data.rows.item(i).password});
						//items.push({PASSWORD: data.rows.item(i).password});
						//items.push({USERID: data.rows.item(i).userid});
						//items.push({PROJECTID: data.rows.item(i).pid});
						//console.log(data.rows.item(i));	
						}
						//console.log(items);	
						}	
						}).catch(e => console.log(e));
			  })
			  .catch(e => console.log(e));
		      
	
		}
		else{

		//console.log((this.testJson=={}));
				this.sqlite.create({
					  name: 'data.db',
					  location: 'default'
						}).then((db: SQLiteObject) => {	
	
			 	db.executeSql('select * from control where key=?', ['sync']).then((data) => {
						//console.log(JSON.stringify(data));
						let items = [];
						if(data.rows.length > 0) {
						for(var i = 0; i < data.rows.length; i++) {
						//alert(data.rows.item(i).name);
						items.push({VALUE: data.rows.item(i).value});
						//console.log(data.rows.item(i));	
						}
						}
					    //console.log(items[0]['VALUE']);
					  this.syncstatus = items[0]['VALUE'];
						}).catch(e => console.log(e));
			  })
			  .catch(e => console.log(e));	
		
		this.myservice.customLoginNew(sql,loginType,testJson,pid,this.playerID).subscribe(loginData => {
			//console.log(this.testJson);
			let loginInfo = loginData.json();
			if (loginType == "form"){

				for (var i=0; i<loginInfo.length; i++){
					if (loginInfo[i].TYPE == 'SUCCESS') {
						let loginDetails = loginInfo[i];
						
						let role = loginInfo[0]["role"];
						this.singleton.role = role;
						this.events.publish('user:role', role);
							
						let offpassword = testJson["PASSWORD"];
						let offusername = testJson["USERNAME"];
						
						this.toast(loginDetails,"");

					}
				}
				
				if(loginInfo.TYPE === "FAILURE"){
					this.successFailureToast("Username or Password is incorrect",3000);
				}
			

				//this.storage.get('userObj').then((val) => {
				//	console.log('Your age is',JSON.parse(val));
				//});

			}
			else if(loginType == "otp"){

				if (loginInfo.TYPE === 'SUCCESS') {
					
					console.log(loginInfo.DAORESPONSE);
					for(let i=0; i<loginInfo.DAORESPONSE.length; i++){
						console.log(loginInfo.DAORESPONSE[i]);
						this.responseOtp = loginInfo.DAORESPONSE[i].MSG
						console.log(this.responseOtp);
						this.singleton.role = loginInfo.DAORESPONSE[i].role;
						this.events.publish('user:role', loginInfo.DAORESPONSE[i].role);

					}

					let alert = this.alertCtrl.create({
						title: 'Enter OTP',
						inputs: [
						{
							name : 'otp',
							placeholder: 'OTP',
							type: 'password'
						}
						],
						buttons: [
						{
							text: 'Cancel',
							role: 'cancel',
							handler: data => {
							console.log('Cancel clicked');
							}
						},
						{
							text: 'Ok',
							handler: data => {
								if (data.otp == this.responseOtp){
									
									let loginDetails =  loginInfo.DAORESPONSE[0];
									this.toast(loginDetails,"");
								}
								else{
									let otptoast = this.toastCtrl.create({
										message: 'Incorrect OTP',
										duration: 3000,
										position: 'bottom'
									});

									otptoast.present();
								}
							
							}
						}
						]
					});
					alert.present();
					
					
				}
				else{
					this.successFailureToast("Username or Password is incorrect",3000);
				}

			}
		
		});
  		
	}
		
}

	toast(loginDetails,mode){
		let user_details = {};
		let is_user_active  = loginDetails['is_active'];
		
		if(is_user_active == "T"){ 
			if(this.singleton.imei_based_login == "True"){
				let imei_no  = loginDetails['imei_no'];
				this.androidPermissions.checkPermission(this.androidPermissions.PERMISSION.READ_PHONE_STATE)
				.then(result => {
					console.log('Has permission?',result.hasPermission);
					if (result.hasPermission){
						//IF IT HAVE PERMISSION
						if (this.uid.IMEI == imei_no ){
							this.setUserDetails(loginDetails,user_details);
							this.successFailureToast("User Logged In Successfully",2000);
							this.moveToNextPage(user_details);
						}
						else{
							console.log("IMEI No is not matched")
							this.successFailureToast("You Are Not A Registered User. Please Contact Admin.",3000);
						}
					}
					else{
						this.androidPermissions.requestPermission(this.androidPermissions.PERMISSION.READ_PHONE_STATE)
						.then(result => {
							console.log('Has permission?',result.hasPermission);
							if(result.hasPermission){
								//IF IT HAVE PERMISSION
								if (this.uid.IMEI == imei_no ){
									this.setUserDetails(loginDetails,user_details);
									this.successFailureToast("User Logged In Successfully",2000);
									this.moveToNextPage(user_details);
								}
								else{
									console.log("IMEI No is not matched");
									this.successFailureToast("You Are Not A Registered User. Please Contact Admin.",3000);
								}
							}
							else{
								console.log("Permission Denied");
								this.successFailureToast("You should allow your app to manage and make phone calls to login!!",3000);
							}
						});
					}
				});
			}	
			else{
				this.setUserDetails(loginDetails,user_details);
				this.successFailureToast("User Logged In Successfully",2000);
				this.moveToNextPage(user_details);
			}	

		}
		else{
			console.log("Not an active user");
			this.successFailureToast("You Are Not An Active User. Please Contact Admin",3000);
		}
	}

	successFailureToast(msg,duration){
		const toast = this.toastCtrl.create({
			message : msg,
			duration: duration,
			position: 'bottom'
		});
		toast.present();
	}

	moveToNextPage(user_details){
		const loading = this.loadingCtrl.create({
			spinner: 'hide',
			content: 'Loading Please Wait...'
		});
	
		loading.present();
		setTimeout(() => {
			if(this.syncstatus == "false"){
				this.navCtrl.setRoot(SyncmasterPage, {
					userdetails : user_details,
				});
			}
			else{
				this.navCtrl.setRoot(SidemenuPage, {
					userdetails : user_details,
				});
			}
		
			this.storage.set('userObj', user_details);
		}, 1000);
	
		setTimeout(() => {
			loading.dismiss();
		}, 3000);{}
	}

	setUserDetails(loginDetails,user_details){
		user_details['USERNAME'] = loginDetails['first_name'];
		user_details['EMAIL'] = loginDetails['email_id'];
		user_details['MOBILENUMBER'] = loginDetails['mobile_number'];
		user_details['ROLE'] = loginDetails['role'];
		user_details['USERID'] = loginDetails['muserid'];
		user_details['PROJECTID'] = loginDetails['projectid'];
		this.singleton.PID = loginDetails['projectid'];
		this.singleton.userid = loginDetails['muserid'];
		
		if(this.singleton.ismultitenant == "True"){
			this.singleton.dynamicresturl = loginDetails['mservice_url'];
		}else if(this.singleton.ismultitenant == "False"){
			this.singleton.dynamicresturl = this.singleton.resturl;
		}
	}

	copydb(){
		console.log("entered Db");
		this.http.get('assets/db.sql').map(res => res.text()).subscribe(data => {
					this.sqlString = data;
					//console.log(this.sqlString);
			},
						err => {

						console.log("No file found");
						}

					);

		this.sqlite.create(this.options)
		.then((db: SQLiteObject) => {
			this.database = db;
			this.dbimporter();
				})
		.catch(e => console.error(e));
		
	}
	dbimporter(){
		this.sqlitePorter.importSqlToDb(this.database, this.sqlString)
			.then(data => {
				console.log(data);
				// db.executeSql('select * from sqlite_master;',{})
				//   .then((data) => console.log(data))
				//   .catch(e => console.log(e));
				//this.databaseReady.next(true);
			this.storage.set('database_filled', true);
			})
			.catch(e => console.error(e));
		this.sqlite.create(this.options)
		.then((db: SQLiteObject) => {
			this.database = db;
			db.executeSql('select * from control;',{})
				.then((data) => console.log(data))
				.catch(e => console.log(e));
				})

		.catch(e => console.error(e));
	}

	async getImei() {
		
		
	}

}
