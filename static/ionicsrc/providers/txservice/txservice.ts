import { Injectable } from '@angular/core';
import { Http,Headers } from '@angular/http';
import { ViewController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { AlertController } from 'ionic-angular';
import { ToastController } from 'ionic-angular';
import { NavController, NavParams } from 'ionic-angular';
import { Network } from '@ionic-native/network';
import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
import { SQLitePorter } from '@ionic-native/sqlite-porter';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { NotifyProvider } from '../../providers/notify/notify';
import { HomePage } from '../../pages/home/home';
import 'rxjs/add/operator/map';
declare var Expression:any;
/*
  Generated class for the TxserviceProvider provider.

  See https://angular.io/docs/ts/latest/guide/dependency-injection.html
  for more info on providers and Angular DI.
*/
@Injectable()
export class TxserviceProvider {
    username: any;
    pid: any;
    userid: any;
    projectname: any;
    loadingctrl:any;
    offlineStore :any[] = []; 
    input_values:any;
    modifyMode:any;
    userDetails:any;
	txn_slug:any;
	ismultitenant:any;
	
	constructor(public http: Http, public navCtrl: NavController,public viewCtrl: ViewController,private sqlite: SQLite,private sqlitePorter: SQLitePorter,private network: Network, public navParams: NavParams, public storage: Storage, public singleton: SingletonProvider, 
		private alertCtrl: AlertController,public notifyProvider :NotifyProvider,private toastCtrl: ToastController) {
        console.log('Hello TxserviceProvider Provider');
        this.projectname = this.singleton.projectname;
		this.ismultitenant = this.singleton.ismultitenant;
		this.username= "admin";
		this.userid ="001";		
		
		this.storage.get('userObj').then((loginInfo) => {
            if (loginInfo){
			//let loginDetails = JSON.parse(loginInfo);
            this.username = loginInfo["USERNAME"];
            this.userid = loginInfo["USERID"];
            //console.log(loginInfo);
			}
        });
	}
 
    saveJson(userDetails,url,form,base64Str,selectedOptions,loading,pagenav,preset_value,saveExp,dynamicPopUpKV) {
        this.loadingctrl = loading;
	this.modifyMode = userDetails['modifyMode'];
	this.userDetails = userDetails;
		
	this.input_values = preset_value;
	let sort_component = ""
	let json = [];
        let table_value = [];
        let table = [];
        let errorStatus = "";
        let cbValue = [];
		let epValue = [];
		let eptValue =[];
		//console.log(userDetails);
		if (userDetails){
			this.username = userDetails.USERNAME;
			this.userid = userDetails.USERID;
		}
		this.pid = this.singleton.PID;
        let regpage;
        //let tablename=[]
        this.http.get(url).map(res => res.json()).subscribe(data => {
            let txView = data[0];
			this.txn_slug = txView['idt'];
			let savetype = txView['st'];
            let content = txView['cont_meta'];
            let parentDT = txView['tran_meta'][0]['prm_meta'][0];
            //console.log(content)
            let component = content[0]['comp_meta'];
            let children = content[0]['children'];
            let eupdate = txView['eupdate_meta'];
			let epost = txView['epost_meta'];
			let saveValue =[];//for Epost
            sort_component = component.sort(function(a, b) {
                return a.do - b.do;
            });
            console.log(sort_component);
			if (content[0]['ctype'] == 'list' || content[0]['ctype'] == 'card'){
            for (let i = 0; i < sort_component.length; i++) {
                let referJson = ""
				let constructedJson_status;
				try{
                referJson = JSON.parse(sort_component[i]["cjson"]);
				}
				catch(err){
				referJson = undefined;
				}
				if(referJson != undefined){
				constructedJson_status = this.getConstructedJson(i,sort_component[i],referJson,table,saveValue,cbValue,base64Str,parentDT,selectedOptions,dynamicPopUpKV);
				if(constructedJson_status == "True"){
					errorStatus = "True";
				break;
				}
				}
            }
			}
			else if(content[0]['ctype'] == 'grid'){
			//alert("grid");
	        let gridValues:any;	
			gridValues = this.gridContainer(sort_component,content[0],table,parentDT);
			if(gridValues == "error"){
				errorStatus = "True";
			}			
			}
            if (!errorStatus) {
                if (children.length > 0) {
                    let childrenjson = this.getChildjson(children, table, parentDT, cbValue,saveValue,base64Str,selectedOptions,dynamicPopUpKV)
                    cbValue = childrenjson;
                    if (childrenjson == "error") {
                        errorStatus = "true";
                    }
                }
            }
            let table_sort = table.sort(function(a, b) {
                return a.od - b.od
            });
			if(errorStatus == "false" || errorStatus == ""){
			if(eupdate){
			 let status = this.getEupdate(eupdate,epValue);
				if(status =='error'){
				 errorStatus = "True";
				}
			}
				if(epost){
					let status ="";
					for(let i=0;i<epost.length;i++){
					if(epost[i]['is_act'] == "True"){
					status = this.getEpost(epost[i],eptValue,saveValue);
					}
					}
					if(status =='error')
					{
						errorStatus = "True";
					}
			}
		}
            var layers = {
                    'layers': table_sort,    //save values in transaction
                    'primary_table': parentDT["tb_s"],//for primary table name
                    'user_name': this.username,
                    'pid': this.pid,  //for projectid
                    'user_id': this.userid,//for user id
                    'project_name': this.projectname,//for projectname
				    'efrom_slug':this.txn_slug,
                    'CB': cbValue,
	                'EP':epValue,  //for Eupdate in Transaction
				    'EPT':eptValue,  //for Epost in Transaction
				    'MLT':this.ismultitenant 
                }
                //json.push(layers);
            console.log(layers);
            if (errorStatus == "false" || errorStatus == "") {
				if (savetype == 'online' || savetype =='both'){
					if(this.modifyMode == true){
						this.sendUpdatejson(layers,userDetails).subscribe(updateMessage => {
							this.loadingctrl.dismiss();
							let userMessage = updateMessage.json();
							let Status = userMessage["values"]["SAVED"];
							if(Status == "TRUE"){
								this.getToast('Updated Successfully');
								if(form == "tr"){
									this.notificationAfterSave(saveExp,preset_value,selectedOptions,userDetails,userMessage,pagenav,"MODIFY")
								}
							
							}else{
							    this.getToast('Updated Failed');
							}
							
						},
						err => {
							setTimeout(() => {
								loading.dismiss();
								this.getSaveAlert("Connection To server Failed.Please Try Again.");
								 }, 200);
								 });
					}
					else{
						this.sendSavejson(layers).subscribe(saveMessage => {
							setTimeout(() => {
								this.loadingctrl.dismiss();
								if (saveMessage){
									let userMessage = saveMessage.json();
									let saveStatus = userMessage["values"]["SAVED"];
									try{
										regpage = userDetails.PAGE; 
									}
									catch(e){
										regpage = ""
									}
									if (saveStatus == "TRUE") {
										userDetails['SAVEID'] = userMessage["values"]["SaveId"];
										if (form =="reg"){
											let alert = this.alertCtrl.create({
												title: 'Information',
												subTitle: "Registered Successfully. You can Login In now.",
												buttons: ['OK']
											});
											alert.present();
											this.navCtrl.setRoot(pagenav[0].component);									
										}
										else if(form == "tr"){
											this.notificationAfterSave(saveExp,preset_value,selectedOptions,userDetails,userMessage,pagenav,"NEW");
										}
									} else if(saveStatus == "FALSE") {
										this.getSaveAlert(userMessage["values"]["MESSAGE"]);

									}	   
								}
							}, 200);
						},
						err => {
							setTimeout(() => {
							loading.dismiss();
								this.getSaveAlert("Network Connection Error!Please Check.");
							}, 200);
						});

					}
				
				}
				else if(savetype == 'offline'){
				  	this.offlineSavetb(layers);
				}

            }
			else{
				loading.dismiss();
			}

        });

	}

	notificationAfterSave(saveExp,preset_value,selectedOptions,userDetails,userMessage,pagenav,mode){
		//Process Notification Configuration
		let notificationExp;
		let currentStage : any;
		let expArray = saveExp.split('(');
		if(expArray[0].toLowerCase() == "notify"){
			notificationExp = expArray[1].slice(0, -1);
			let notificationExpArray = notificationExp.split(',');
			this.processStage(notificationExpArray,preset_value,selectedOptions,userDetails,mode);
			if (mode == "NEW"){
				this.openNewModeTxn(userMessage);
			}
			else if (mode == "MODIFY"){
				this.navCtrl.pop();
			}
		}
		
		else if(expArray[0].toLowerCase().includes("viewtxn") || expArray[0].toLowerCase().includes("viewreport")){
			this.navToNextPage(saveExp,pagenav,userDetails)
			
		}
		if(expArray[0].toLowerCase() == "iif"){
			// let condition = saveExp.split(expArray[0])
			// let exp = condition[1].split(":")
			// console.log(exp);
			let GetVal;
			let ExprObj = new Expression("");
			ExprObj.Expression(saveExp, userDetails, "", "");
			GetVal = ExprObj.Evaluate();
			let ifExpArray = GetVal.split('(');
			if(ifExpArray[0].toLowerCase() == "notify"){
				let notificationArray = ifExpArray[1].slice(0, -1);
				let notificationExpArray = notificationArray.split(',');
				this.processStage(notificationExpArray,preset_value,selectedOptions,userDetails,mode);
				if (mode == "NEW"){
					this.openNewModeTxn(userMessage);
				}
				else if (mode == "MODIFY"){
					this.navCtrl.pop();
				}
				
			}
			else if(ifExpArray[0].toLowerCase().includes("viewtxn") || ifExpArray[0].toLowerCase().includes("viewreport")){
				this.navToNextPage(GetVal,pagenav,userDetails)
				
			}



		}
		else{
			if (mode == "NEW"){
				this.openNewModeTxn(userMessage);
			}
			else if (mode == "MODIFY"){
				this.navCtrl.pop();
			}
			
		}
	}
	
	processStage(notificationExpArray,preset_value,selectedOptions,userDetails,mode){
		this.http.get('assets/json/notification.json').map(res => res.json()).subscribe(data => {
			for(let i=0;i<data.length;i++){
				if (data[i].title == notificationExpArray[0]){
					let notificationJson = data[i];
					let stages = notificationJson.config;
					
					for(let j=0;j<stages.length;j++){
						if (stages[j].sname == notificationExpArray[1]){
							let currentStage = stages[j];
							if (currentStage != null){
								let musername : String;
								let basicid : String;
								
								if(currentStage["uf"]){
									musername =  this.getFieldValueForNotification(preset_value,currentStage["uf"],selectedOptions);

								}else{
									musername = ""
								}
								if(currentStage["msg"]){
									var found = [],          // an array to collect the strings that are found
										rxp = /{([^}]+)}/g,
										str = currentStage["msg"],
										curMatch;
					
									while( curMatch = rxp.exec( str ) ) {
										found.push( curMatch[1] );
									}
					
									for(var k=0;k<found.length;k++){
										var keyStr = "{"+found[k]+"}";
										var valueStr = "";
										valueStr = this.getFieldValueForNotification(preset_value,found[k],selectedOptions);
										currentStage["msg"] = currentStage["msg"].replace(keyStr,valueStr)
									}
					
								}
								if(currentStage["idf"]){
									basicid = this.getFieldValueForNotification(preset_value,currentStage["idf"],selectedOptions)
									
								}
								else{
									if(mode == "NEW"){
										basicid = userDetails['SAVEID'];
									}else if(mode == "MODIFY"){
										basicid = userDetails['recordId'];
									}
									
								}
								

								
								//MESSAGE
								if (currentStage["sptype"] == "Message"){
									let notifyJson = {
										"ROLE" : currentStage["rl"],
										"FROMDATE" : this.getFieldValueForNotification(preset_value,currentStage["fdate"],selectedOptions),
										"TODATE" : this.getFieldValueForNotification(preset_value,currentStage["tdate"],selectedOptions),
										"BASICID" : basicid,
										"USERNAME" : musername,
										"MSG" :  currentStage["msg"],
										"JSON": currentStage,
										"APPID" : this.singleton.apikey,
					
									}
									this.notifyProvider.updateNotificationStatus(notifyJson).subscribe(Msgdata => {
										let result = Msgdata.text();
										console.log(result);
										let alert = this.alertCtrl.create({
											title: 'Notification',
											buttons: ['OK']
										});
										if(result == "Notification Error"){
											alert.setSubTitle("Error While Notify"+currentStage["rl"]);
											alert.present();
					
										}
										else if(result == "Save Error"){
											alert.setSubTitle("Error While Saving Notification Status");
											alert.present();
					
										}
					
									});
									
								}
									
							}
							
							break;
						}

					}
				}

			}

		});
        

	}
	
	navToNextPage(saveExp,pagenav,userDetails){
		let txnViewpage;
		let transacionview = saveExp.substring(
			saveExp.lastIndexOf("(") + 1, 
			saveExp.lastIndexOf(")")
		);
		const navpage_filter = pagenav['pages'].filter((item) => {
			return (item['id'] == transacionview);
		});
		if(navpage_filter.length >0){
			let page = navpage_filter[0];
			this.navCtrl.push(page.component,{'userdetails':userDetails}).then(() => {
				const startIndex = this.navCtrl.getActive().index - 1;
				this.navCtrl.remove(startIndex, 1);
			});
		}
	}

	openNewModeTxn(userMessage){
		this.getSaveAlert(userMessage["values"]["MESSAGE"]);
		this.navCtrl.push(this.navCtrl.getActive().component).then(() => {
			let index = this.viewCtrl.index;
			this.navCtrl.remove(index);
		});
	}

	getFieldValueForNotification(preset_value,fieldId,selectedOptions){
		let value = "";
		value = preset_value[fieldId];
		if(value == undefined || value == ""){
			value = "";
		}
		return value;
	}


	getInputfield(input){
		/* function to get input and number value in transaction*/
        let inputValue:any;
        let id = input["idt"];
        inputValue = this.input_values[id];
        if (inputValue == "" || inputValue == undefined) {
            if (input["ire"] == "True") {
                this.getAlert(input["cap"]);
                return "error";
            }
			if(input['ct'] == 'IntegerField'){
				inputValue = 0;
			}
			else{
            inputValue = "";
			}
        }
        return inputValue;
    }
    
    gettextarea(area){
		/* function to get textarea value in transaction*/
     let textarea =""
	 let id = area["idt"];
	 textarea =  this.input_values[id];
		if (textarea == "" || textarea == undefined) {
            if (area["ire"] == "True") {
                this.getAlert(area["cap"]);
                return "error";
            }
            textarea = "";
        }
        return textarea;
	}
    getSelectfield(select,selectedOptions) {
		/* function to get Select value in transaction*/
        let selectValue = ""
        let id = select["idt"];
		//let cap = select["cap"];
		//selectValue = document.getElementsByName(id)[0].textContent;
        selectValue = selectedOptions[id];
        if (selectValue == undefined) {
            if (select["ire"] == "True") {
                this.getAlert(select["cap"]);
                return "error"
            }
            selectValue = "";
        }
        return selectValue;
    }

    getDatefield(date) {
		/* function to get DateField value in transaction*/
        let dateValue:any;
		let ionicdateValue =""
        let id = date["idt"];
        //let cap = date["cap"];
        ionicdateValue = this.input_values[id];
		dateValue = new Date(ionicdateValue).toDateString();
        if (dateValue == "" || dateValue == "Invalid Date" || dateValue == undefined) {
            if (date["ire"] == "True") {
                this.getAlert(date["cap"]);
                return "error"
            }
            dateValue = "";
        }
        return dateValue;
    }

     getTimefield(time) {
		/* function to get DateField value in transaction*/
        let TimeValue = ""
        let id = time["idt"];
        //let cap = date["cap"];
        TimeValue = this.input_values[id];
        if (TimeValue == "" || TimeValue == time["cap"] || TimeValue == undefined) {
            if (time["ire"] == "True") {
                this.getAlert(time["cap"]);
                return "error"
            }
            TimeValue = "";
        }
        return TimeValue;
    }

    getCheckbox(Check) {
        //console.log(Check);
		/* function to get Checkbox value in transaction*/
        let checkValue = "";
        let jsonValue;
        let referJson = ""
		let checkbox_id = Check['idt'];
        referJson = JSON.parse(Check['cjson']);
		
        let enum_length = referJson["enum_meta"].length;
        let keyvalues = referJson["enum_meta"]
        let id = keyvalues[0]["key"];
		let values = keyvalues[0]["value"]
		if(enum_length == 1){
		  if(this.input_values[checkbox_id+"_"+id]){
		    checkValue = values;
		  }
			else{
			 checkValue = '';
			}
		}
		
		if (checkValue == "" || checkValue == Check["cap"] ) {
            if (Check["ire"] == "True") {
                this.getAlert(Check["cap"]);
                return "error"
            }
        }
             
        return checkValue;
    }

    getmultiCheckbox(mcheck) {
		/* function to get MultipleCheckbox value in transaction*/
        let cb = [];
        let jsonValue;
        let referJson;
        let checkValue = "";
        referJson = JSON.parse(mcheck['cjson']);
        let enum_length = referJson["custom_enum"]["key_values"].length;
        let keyvalues = referJson["custom_enum"]["key_values"]
            //alert("hi");
        for (let i = 0; i < enum_length; i++) {
            let id = referJson["custom_enum"]["key_values"][i]["key"];
            checkValue = document.getElementById(id).getElementsByTagName('button')[0].attributes["aria-checked"].value;
            if (checkValue == "true") {
                var key = {
                    'FV': keyvalues[i]["value"],
                    'FN': referJson["db_column"]
                }
            }
        }
        jsonValue = cb;
        return jsonValue;
    }

    uuidGenerator(){
      
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
       
    }

    getRadiobox(radio,selectedOptions) {
		/* function to get RadioBox value in transaction*/
        let radioValue = ""
        let id = radio["idt"];
        //radioValue = document.getElementById(id).getElementsByClassName('item item-block item-md item-radio item-radio-checked')[0]['children'][0]['childNodes'][1]['attributes']['ng-reflect-value']['value'];
		radioValue = selectedOptions[id];
        if (radioValue == null || radioValue == undefined) {
            if (radio["ire"] == "True") {
                this.getAlert(radio["cap"]);
                return "error"
            }
            radioValue = "";
        }
        return radioValue;
    }

 	getScanvalue(scan){
	  	/* function to get Barcode or Qrscan value in transaction*/
		let scanValue =""
		let id = scan["idt"];
		scanValue = document.getElementById(id).getElementsByTagName("input")[0].value;
		if (scanValue == "" || scanValue == undefined) {
			if (scan["ire"] == "True") {
				this.getAlert(scan["cap"]);
				return "error";
			}
			scanValue = "";
		}	  
		return scanValue;  
	}

    getChildjson(child, table, parentDT, cbValue,saveValue,base64Str,selectedOptions,dynamicPopUpKV) {
		/* Generating Meta Json for child in Transaction*/
        //let cbValue =[];
        //console.log(cbValue);
        //console.log(table);
        let sort_component = "";
        let errorStatus = "false";
        for (let n = 0; n < child.length; n++) {
            let component = child[n]['comp_meta'];
            let children = child[n]['children'];
            sort_component = component.sort(function(a, b) {
                return a.do - b.do;
            });
            //console.log(sort_component);
			if (child[n]['ctype'] == 'list' || child[n]['ctype'] == 'card'){
            for (let i = 0; i < sort_component.length; i++) {
                let referJson = ""
                let fieldValue;
				let constructedJson_status="";
                referJson = JSON.parse(sort_component[i]["cjson"])
                let id = sort_component[i]["tt"];
				try{
                referJson = JSON.parse(sort_component[i]["cjson"]);
				}
				catch(err){
				referJson = undefined;
				}
				if(referJson != undefined){
				constructedJson_status = this.getConstructedJson(i,sort_component[i],referJson,table,saveValue,cbValue,base64Str,parentDT,selectedOptions,dynamicPopUpKV);
				if(constructedJson_status == "True"){
					errorStatus = "True";
					break;
				}
            }
			}
			}
			else if(child[n]['ctype'] == 'grid'){
			//alert("grid");
			let gridValues:any;	
			gridValues = this.gridContainer(sort_component,child[n],table,parentDT);
			if(gridValues == "error"){
				errorStatus = "True";
			}	
			}
            if (errorStatus == "True") {
                break;
            }
            if (errorStatus == "false") {
                if (children.length > 0) {
                    let childrenjson = this.getChildjson(children, table, parentDT, cbValue,saveValue,base64Str,selectedOptions,dynamicPopUpKV)
                    cbValue = childrenjson;
                }
            }

        }
        //let componentjson =""
        if (errorStatus == "True") {
            return "error";
        } else {
            return cbValue;
        }
    }

    getAlert(message) {
        //  console.log(message);
        let alert = this.alertCtrl.create({
            title: 'Save Alert',
            subTitle: message + " is required",
            buttons: ['Dismiss']
        });
        alert.present();
    }

    sendSavejson(Json: any) {
		/* Server Request Calling for Save Function*/
        let saveJson = Json;
		//let offlineStore = [];
		console.log(saveJson);
		//console.log(this.network);
		if(this.network.type == "none"){
		 this.offlinesave(saveJson);
		 	
			  return null;
		}
		else{
			var headers = new Headers();
			headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
			let stringify = JSON.stringify(saveJson);
			let params = "saveJson=" + encodeURIComponent(stringify);
			console.log("f");
			return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/saveJsonionic/', params, {
            headers: headers
        });
		}
    }
	
	sendUpdatejson(Json:any,userDetails:any){
		/* Server Request Calling for Save Function*/
        let saveJson = Json;
		//let offlineStore = [];
		console.log(saveJson);
		saveJson['recordId'] = userDetails['recordId'];
		//console.log(this.network);
		if(this.network.type == "none"){
		 this.offlinesave(saveJson);
		 	
			  return null;
		}
		else{
			var headers = new Headers();
			headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
			let stringify = JSON.stringify(saveJson);
			let params = "saveJson=" + encodeURIComponent(stringify);
			console.log("f");
			return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/updateionic/', params, {
            headers: headers
        });
		}
	
	}

  sendSearchjson(Json:any){
  /* Server Request Calling for Save Function*/
        let saveJson = Json;
		//let offlineStore = [];
		console.log(saveJson);
		//console.log(this.network);
		if(this.network.type == "none"){
			return null;
		}
		else{
			var headers = new Headers();
			headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
			let stringify = JSON.stringify(saveJson);
			let params = "searchDetails=" + encodeURIComponent(stringify);
			console.log("f");
			return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/searchIonic/', params, {
            headers: headers
        });
		}
  }
	
  getSearchrecord(Json:any){
  /* Server Request Calling for Save Function*/
        let recordJson = Json;
		//let offlineStore = [];
		console.log(recordJson);
		//console.log(this.network);
		if(this.network.type == "none"){
			return null;
		}
		else{
			var headers = new Headers();
			headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
			let stringify = JSON.stringify(recordJson);
			let params = "particularRecord=" + encodeURIComponent(stringify);
			console.log("fr");
			return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/getsearchRecord/', params, {
            headers: headers
        });
		}
  }
  
   offlinesave(saveJson){
	   /* Offline Save Function For Transaction*/
	   let offlinesql="";
	   let table="";
	   let sqlstart ="";
	   let json= '';
	   let offdata ;
	   console.log(saveJson);
	   json = "'"+JSON.stringify(saveJson)+"'";
       table = 'CREATE TABLE IF NOT EXISTS offlineSync (value VARCHAR(10000) NOT NULL)';
	   sqlstart = 'INSERT OR REPLACE INTO offlineSync SELECT '+json+' AS "value"';
	   offlinesql = table+';'+sqlstart;
	   console.log(offlinesql);
	    this.sqlite.create({
            name: 'data.db',
            location: 'default'
        }).then((db: SQLiteObject) => {
			this.sqlitePorter.importSqlToDb(db, offlinesql)
      		.then(() =>{
				offdata = this.datapresent(db);
				this.offlineSavetb(saveJson);
				 /* Using Cordova Sqlite Porter Plugin*/
			}).catch(e => console.error(e));
		 }).catch(e => console.log(e));
   }

    customSelectService(data:object){
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params = "fieldType="+data['fieldType']+"&eformid="+data['eFormId']+"&fieldName="+data['fieldName']+"&projectid="+data['projectId']+"&projectname="+data['projectName']+"&USERNAME="+data['username']+"&ISMULTITENANT="+this.singleton.ismultitenant+"&TYPE="+data['type']+data['MapValue'];
	
		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/eformsql',params,{headers: headers});
	}

	
 gridContainer(component,container,table,parentDT)
 {
	 /* Meta Json Genertaing For Grid Layout In Transaction */
	 console.log(container); 
	 console.log(component);
	 let tableId ="";
	 
	 if(this.modifyMode == true){
		 tableId = container['idt']+"_ET";
	 }
	 else{
		 tableId = container['idt'];
	 }
	 
	 let tbe = document.getElementsByName(tableId)[0];
	 let tb = tbe.getElementsByTagName('tbody')[0];	 
	 let tbody =tbe.getElementsByTagName('tbody')[0].children;
	 let thead = tbe.getElementsByTagName('thead')[0].children[0].children;  
	 let rowlength = tb.rows.length;
	 let gridValue :any;
	 let addStatus ="True";
	 if(rowlength>0){
		 for(let r=0;r<rowlength;r++){
			 let currentrow = tbody[r];
			 let fromdb ="";
			 if (currentrow['dataset']['fromdb'] != undefined){
				 fromdb = currentrow['dataset']['fromdb'];
			 }
			 else
			 {
				 fromdb = "False";
			 }
			 let table_value =[];
			 let tablename ={};
			 for(let i=0;i<component.length;i++){
				 let referJson ="";
				 let field_slug ="";
				 let fieldValue ="";
				 try{
				 referJson = JSON.parse(component[i]['cjson']);
				 }
				 catch(err){
				 referJson = undefined;
				 }
				 if(referJson != undefined){
					 try{
						 field_slug = referJson['field_slug']+"_"+referJson['txtabledetailid'];
						 
						 if(field_slug == thead[i].id){
							 if(currentrow.children[i]['dataset']["type"] == 'select' || currentrow.children[i]['dataset']["type"] == 'radio' ||currentrow.children[i]['dataset']["type"] == 'time' ||currentrow.children[i]['dataset']["type"] == 'check'){
								 fieldValue = currentrow.children[i]['dataset']["select_value"];
							 }
							 else if (currentrow.children[i]['dataset']["type"] == 'date'){
								 let dateValue = currentrow.children[i]['dataset']["select_value"];
								 if(dateValue =="" || dateValue == undefined){
									 fieldValue = "";
								 }
								 else{
								 fieldValue = new Date(dateValue).toDateString();
								 }
							 
							 }else
							 {
								 fieldValue = currentrow.children[i].textContent;
							 }
							 if (fieldValue == "") {
								 if (component[i]["ire"] == "True") {
									 this.getAlert(component[i]["cap"]);
									 return "error";
								 }
								 fieldValue = "";
							 }
							 var item = {
								 'FN': referJson["field_slug"],
								 'FV': fieldValue,
								 'DT': referJson["datatype"],
								 'SV': referJson["isdbfield"],
								 'AD': component[i]["ad"],
								 'WT': component[i]["wt"]
							 }
							 table_value.push(item);
						 }
						 //console.log(table_value);
						 if (table.length == 0) {
							 let order:any;
							 if (referJson["txtabledetailid"] == parentDT['tb_s']) {
								 order = 1;
							 } else {
								 order = r + 2;
							 }
							 tablename['table_value'] = table_value;
							 tablename['table_name'] = referJson["txtabledetailid"];
							 tablename['od'] = order;
							 if(this.modifyMode == true){
								 tablename['fromdb'] = fromdb;
							 }
						 }
						 else{
							 let order:any;
							 order = r+6;
							 tablename['table_value'] = table_value;
							 tablename['table_name'] = referJson["txtabledetailid"];
							 tablename['od'] = order;
							 if(this.modifyMode == true){
								 tablename['fromdb'] = fromdb;
							 }
						 }
					 }
				 catch(err){
					 console.log(err);
					 addStatus =="False";
				 }
			 }
	 }
	 if(addStatus =="True"){
	 table.push(tablename);
	 }
	
	 }
		  return gridValue;
	 }
	 else{
   for(let i=0;i<component.length;i++){
	 let referJson ="";
	 let field_slug ="";
	 let fieldValue ="";	 
	 referJson = JSON.parse(component[i]['cjson']);
	 field_slug = referJson['field_slug']+"hd";	 
            if (component[i]["ire"] == "True") {
                this.getAlert(component[i]["cap"]);
                return "error";
            }
		 console.log("no data in grid");
	 }
	 return gridValue;
 }
 }

offlineSavetb(layers){
	/* Generating Sql For Offline Save in Sqlite */
	console.log(layers);
   this.sqlite.create({
	name: 'data.db',
	location: 'default'
        }).then((db: SQLiteObject) => {
	   this.sqlitePorter.exportDbToJson(db)
	.then((data) => {console.log(data);
					 let databaseDt = data;
					 let pid = layers.pid;
					 let pname = layers.project_name;
					 let userid = layers.user_id;
					 let username = layers.user_name;
					 let primarytable = layers.primary_table;
					 let colvalues = layers.layers;
					 let epValues = layers.EP;
					 let epost = layers.EPT;					 
					 let primaryUniqueid ={};
					 let sql ="";
					 let finalsql="";
					 let status = false;
					 finalsql = this.offlineSavequery(colvalues,primarytable,status,finalsql,databaseDt,pid,primaryUniqueid,username);
					 if (finalsql == "true"){
						 status = true;
					 }
					 // For Eupdate Offline Save
					 if (epValues.length>0){
						 console.log(epValues);
						 for(let i=0;i<epValues.length;i++){
							 let eupdatesql = "";
							 let sqlStart = "";
							 let sqlEnd ="";
							 let value :any;
							 let TB = epValues[i].TB;//for Table Name
							 let FC = epValues[i].FC;//for Filter Clause
							 let TR = epValues[i].TR;//for Target Field
							 sqlStart = 'UPDATE '+TB+' SET '+TR+' =';
							 let fcValue = FC.split('=');	
							 if(epValues[i].UC == 'T' || epValues[i].UC == ''){
								 let srValue = epValues[i].SC;
								 if(epValues[i].AT == 'add'){
									 sqlEnd = '('+TR+'+'+parseInt(srValue)+')'+' WHERE '+FC+';';	
								 }
								 else if(epValues[i].AT == 'sub')
								 {
									 sqlEnd = '('+TR+'-'+parseInt(srValue)+')'+' WHERE '+FC+';';	
								 }
								 else if(epValues[i].AT == 'inc'){
									 sqlEnd = '('+TR+'+1)'+' WHERE '+FC+';';					
								 }
								 else if(epValues[i].AT == 'dec'){
									 sqlEnd = '('+TR+'-1)'+' WHERE '+FC+';';				
								 }
								 else if(epValues[i].AT == 'replace'){
									 sqlEnd = '"'+srValue+'"'+' WHERE '+FC+';';				
								 }
								 eupdatesql = sqlStart+sqlEnd;
								 console.log(eupdatesql);
							 }
							 finalsql+= eupdatesql;
						 }	
					 }
					 // For Epost Save in Transaction
					 if(epost.length>0){
						 for(let i=0;i<epost.length;i++){
							 let epostlayers = epost[i].layesrs;
							 let epostPrimary = epost[i].primary_table;
							 let epostQuery ="";
							 epostQuery = this.offlineSavequery(epostlayers,epostPrimary,status,epostQuery,databaseDt,pid,primaryUniqueid,username);
							 if(epostQuery == "true"){
							 status = true;
							 }
							 else{
							 finalsql +=epostQuery;
							 }
						 }
					 
					 }
					 
					 if (finalsql && status == false){ 
						 this.sqlitePorter.importSqlToDb(db, finalsql)
							 .then(() =>{
							 this.datapresent(db);
							 console.log('imported');
							 this.navCtrl.push(this.navCtrl.getActive().component).then(() => {
								 let index = this.viewCtrl.index;
								 this.navCtrl.remove(index);
								});
							 setTimeout(() => {
							 this.loadingctrl.dismiss();
							 this.savealert("Saved SuccessFully To Local Store");
						      }, 100);		 
						 })
							 .catch(e => {console.error(e);
										  setTimeout(() => {
										  console.log(e.message)
										  this.loadingctrl.dismiss();
										  this.savealert(e.message);
											  }, 100);		 
										 });
					 }
					}).catch(e => console.error(e));
   })
	   .catch(e => console.error(e));
}

savealert(message){
 let alert = this.alertCtrl.create({
                                    title: 'Information',
                                    subTitle: message,
                                    buttons: ['OK']
                                });
                                alert.present();
}


offlineSavequery(colvalues,primarytable,status,finalsql,databaseDt,pid,primaryUniqueid,username){
	//Offilne Save Query Construction in transaction
	for(let i=0;i<colvalues.length;i++){
		
		let uniqueid = new Date().valueOf();
		if(colvalues[i].table_name == primarytable){
		let sqlstart = 'INSERT INTO '+colvalues[i].table_name;
		let fields = colvalues[i].table_value;
			let datevalue =new Date().toLocaleDateString()+" "+new Date().toLocaleTimeString();
			primaryUniqueid['puniqueid'] = uniqueid;
			let sqlcolumns = colvalues[i].table_name + "id,created_by,created_on,projectid,modified_by,modified_on";
			let sqlfields = uniqueid+",'"+username+"','"+datevalue+"','"+pid+"','"+username+"','"+datevalue+"'";
			for(let j=0;j<fields.length;j++){
				if(fields[j].SV == true){
					if(fields[j].AD == "False"){
					  let ad = this.checkingDb(databaseDt,fields[j].FN,fields[j].FV,fields[j].DT,colvalues[i].table_name);
					   if (ad.length >0){
						status = true;
						this.adalert(fields[j].FV);
						 return "true";
						}
						
					}
				  let fieldcol = fields[j].FN;
				  let fieldvalue = fields[j].FV;
				  sqlcolumns+= ","+fieldcol;
				  sqlfields+=",'"+fieldvalue+"'";	
				  }
				if(status == true){
				break;
				}
			}
			finalsql = sqlstart+' ('+sqlcolumns.toString()+') VALUES'+' ('+sqlfields.toString()+');';
			console.log(finalsql);
		}
		else{
		   let sqlstart = 'INSERT INTO '+colvalues[i].table_name;
		   let fields = colvalues[i].table_value;
			let uniqueid :any;
			let d = new Date();
			uniqueid = d.getTime()+i;
			let puniqueId = primaryUniqueid["puniqueid"];
			//console.log(primaryUniqueid);
			let sqlcolumns =colvalues[i].table_name + "id,"+primarytable+"id";
			let sqlfields=uniqueid+","+puniqueId;
		   for(let j=0;j<fields.length;j++){
				if(fields[j].SV == true){
					if(fields[j].AD == "False"){
					  let ad = this.checkingDb(databaseDt,fields[j].FN,fields[j].FV,fields[j].DT,colvalues[i].table_name);
						if (ad.length >0){
						status = true;
					    this.adalert(fields[j].FV);
						  return "true";	
						}
					}
				  let fieldcol = fields[j].FN;
				  let fieldvalue = fields[j].FV;
				  sqlcolumns+= ","+fieldcol;
				  sqlfields+=",'"+fieldvalue+"'";	
				  }
			   if(status == true){
				break;
				}
			}
			finalsql += sqlstart+' ('+sqlcolumns.toString()+') VALUES'+' ('+sqlfields.toString()+');';	
			
		}
		//console.log(finalsql);
		if(status == true){
				break;
				}
	}
	return finalsql;
}

 datapresent(db){
		this.sqlitePorter.exportDbToJson(db)
	.then((data) => {console.log(data);
					return data;})
	.catch(e => console.error(e));
		
		var successFn = function(json, count){
        //console.log("Exported JSON: "+json);
        alert("Exported JSON contains equivalent of "+count+" SQL statements");
    };
	}

 checkingDb(Dbdata,FN,FV,DT,TB){
  	let filter:any;
	 if(DT == "IntegerField"){
	  filter = parseInt(FV);
	 }
	 else{
	 filter = FV;
	 }
	 if(Dbdata.data.inserts[TB].length >0){
		const filteredResult = Dbdata.data.inserts[TB].filter((item) => {
		return (item[FN] == filter);
	});
	 //console.log(filteredResult);
		 return filteredResult;
	 }
	 else{
		 let result ="";
		 return result;
	 }
	 
 }

adalert(fieldvalue){
	setTimeout(() => {
		this.loadingctrl.dismiss();
		let alert = this.alertCtrl.create({
			title: 'Save Alert',
			subTitle: fieldvalue+" is already Exists",
			buttons: ['OK']
		});
		alert.present();
	});
}

getEupdate(eupdate,epValue){
	/* Meta Json Genertaing For Eupdate in Transaction */
	//console.log(eupdate);
	for(let i=0;i<eupdate.length;i++){
	let evalue ={};
	let sourceField = eupdate[i]['so_meta'];
	let targetFiled = eupdate[i]['tr_meta'];
	let cType = sourceField[0]['ctype'];
	let actiontype = eupdate[i]['act'];
	let sid = sourceField[0]['idt'];
	let filter_clause = eupdate[i]['ft_c'];
	let splitValue = filter_clause.split(":");	
  	if (cType == "grid"){
		let tableId = sourceField[0]['cid'];
		if(this.modifyMode == true){
			tableId = sourceField[0]['cid']+"_ET";
		}
		let table = document.getElementById(tableId);
		let tbody = table.getElementsByTagName('tbody');
		let children = tbody[0]['children'];
		let filterIndex ="";
		let controlIndex  ="";
		let sorcecellIndex = document.getElementsByName(sid+'_'+sourceField[0]['dbtable'])[0]['cellIndex'];
		try{
			let fid = splitValue[1]+'_'+sourceField[0]['dbtable'];
			filterIndex = document.getElementsByName(fid)[0]['cellIndex'];
			if(eupdate[i]['ui_meta'].length>0){
			if(eupdate[i]['ui_meta'][0]['ctype'] == 'grid'){
				let uid = eupdate[i]['ui_meta'][0]['idt'];
				controlIndex = document.getElementsByName(uid+'_'+sourceField[0]['dbtable'])[0]['cellIndex'];
			}
			else{
			   controlIndex ="";
			}
			}
			}
		catch(err){
		 this.getEupdateAlert("Eupdate Configuration Error");
		  return 'error';
		}
		for(let j=0;j< children.length;j++){
			let rowid = children[i]['id'];
			let value = {};
			let sourcevalue ="";
			let fValue ="";
			let where_clause = "";
			where_clause = filter_clause;
			sourcevalue = children[j]['children'][sorcecellIndex]['textContent'];
			fValue = children[j]['children'][filterIndex]['textContent'];
			//console.log(sourcevalue);
			let trjson = JSON.parse(eupdate[i]["tr_meta"][0]["cjson"]);
			let UiControlField = "";
			value['SC'] =  sourcevalue;//for source filed
			value['TR'] = 	trjson['field_slug'];//for target field
			value['TB'] = eupdate[i]['tr_meta'][0]['dbtable'];//for target table
			where_clause = where_clause.replace(":"+splitValue[1],"'"+fValue+"'");
			value['FC'] = where_clause;
			value['FCV'] = fValue;
			value['AT'] = eupdate[i]['act'];//for action type
			value['UP'] = eupdate[i]['upt'];//for update type
			evalue['TR_DT'] = trjson['datatype'];//for Target Field DataType
			if (controlIndex){
				UiControlField = children[j]['children'][controlIndex]['textContent'];//for Ui control Field
			}
			else{
				let uid = eupdate[i]['ui_meta'][0]['idt'];
				UiControlField = this.input_values[uid];//for Ui control Field
				//value['UC'] = controlValue;
			}
			if (UiControlField =="T" ||UiControlField=="F"){
				value['UC'] = UiControlField;
			}else
			{
				let message = "Control Field Not Correctly Given";
				this.getEupdateAlert(message);
				return 'error';
			}
			if(this.modifyMode == true){
				let old  = this.userDetails['eupdate'];
				const filteredResult = old.filter((item) => {
					return (item['rowid'] == rowid);
				});
				if(filteredResult.length >0){
				if(filteredResult[0]['old_value'] == null){
				   value['PV'] = 0
				}
				else{
					value['PV'] = filteredResult[0]['old_value'];
				}
				if(value['SC'] != value['PV']){
					epValue.push(value);
				}
				}
			}
			else{
				epValue.push(value);
			}
			//console.log(epValue);
			
		}
	}
	else{
	let trjson = JSON.parse(eupdate[i]["tr_meta"][0]["cjson"]);
	let sElement = document.getElementById(sid).getElementsByTagName("input");
	let sField ="";
	if (actiontype =="add" || actiontype =="sub" || actiontype =="inc" || actiontype =="dec"){
	if(sElement[0].type =="number")
	{
	  sField = this.input_values[sid];
	}
	else
	{   let message = sElement[0]['offsetParent']['textContent'] +" is Not Number Field";
		this.getEupdateAlert(message);
		return 'error';
	}
	}
	else if(actiontype =="replace")
	{
		evalue['TR_DT'] = trjson['datatype']; //for target field datatype 
		let element :any;
		if(document.getElementsByName(sid)[0].nodeName == "ion-input"){
			sField = this.input_values[sid];
		}
		else if (document.getElementsByName(sid)[0].nodeName == "ION-DATETIME" || document.getElementsByName(sid)[0].nodeName == "ION-SELECT"){
		   sField = this.input_values[sid];			
		}
	}
	evalue['SC'] =  sField;//for source filed
	evalue['TR'] = 	trjson['field_slug'];//for target field
	evalue['TB'] = eupdate[i]['tr_meta'][0]['dbtable'];//for target table
	//for filter Clause	
	if(filter_clause.search(":") != -1)
	{
		try{
         filter_clause = this.getFilterClause(splitValue,filter_clause,evalue);
		 if(filter_clause == 'error'){
		 return 'error';
		 }
		
		 evalue['FC'] = filter_clause;
		}
		catch(err) {
		console.log(err);
		}
		
	}
	else{
	evalue['FC'] = eupdate[i]['ft_c'];
	}
	evalue['AT'] = eupdate[i]['act'];//for action type
	evalue['UP'] = eupdate[i]['upt'];//for update type	
	if (eupdate[i]['ui_meta'].length > 0)	{
	 let uid = eupdate[i]['ui_meta'][0]['idt'];
	 let controlValue = this.input_values[uid];//for Ui control Field
		if (controlValue == "T" || controlValue =="F"){
		evalue['UC'] = controlValue; 
		}
		else{
		let message = "Control Field Not Correctly Given";
		this.getEupdateAlert(message);
		return 'error';
		}
		}
		else{
		evalue['UC'] = "";
		}
		if(this.modifyMode == true){
			
			let old  = this.userDetails['eupdate'];
			if(old[sid] != null){
				evalue['PV'] = old[sid];
				if(old[sid] != evalue['SC']){
					epValue.push(evalue);
				}
				else{
					epValue.push(evalue);
				}
		}
		else if(old[sid] == null){
			evalue['PV']  =0;
			epValue.push(evalue);
		}
		
		}
	}
	}

	//console.log(epValue);
}

getFilterClause(splitValue,filter_clause,evalue){
	    let element = document.getElementsByName(splitValue[1]);
		if (element[0].tagName == 'ION-INPUT'){
		  let value = document.getElementById(splitValue[1]).getElementsByTagName("input")[0].value;
			if(value == ""){
			this.getEupdateAlert("Eupdate Filter Clause Value Should Not Be Empty");
			return 'error'
			}
			let type = document.getElementById(splitValue[1]).getElementsByTagName("input")[0].type;

			 filter_clause = filter_clause.replace(":"+splitValue[1],'"'+value+'"');
			evalue['FCI'] = value;
			return filter_clause;
}
}


getEupdateAlert(message){
	let alert = this.alertCtrl.create({
									title: 'Eupdate Alert',
									subTitle: message,
									buttons: ['OK']
								});
								alert.present();

}

getEpost(epost,eptValue,saveValue){
	console.log(epost);
	console.log(saveValue);
	let map = epost['map_meta'];
	let map_details;	
	map_details = map.sort(function(a, b) {
		return a.od > b.od;
	});
	let epost_uid ="";
	try{
	let epost_ui_controlfield = epost['ucf_meta'][0]['idt'];
	epost_uid = document.getElementById(epost_ui_controlfield).getElementsByTagName("input")[0].value;
	}catch(err){
	epost_uid ="";
	}
	if(epost_uid=="T" || epost_uid==""){
		let tablevalue = [];
		let table = [];
		var tableObj = {
			'table_value': [],
                        }
		var epostJson ={};
		for(let m=0;m<map_details.length;m++){
			let control_field = "";
			console.log(map_details[m]);
			let source = map_details[m]['so_fld'][0];
			let fieldValue ="";
			let target = map_details[m]['tr_fld'][0];
			let referJson = JSON.parse(target['cjson']);
			let dbTable = referJson["txtabledetailid"];
			try{
			if(map_details[m]['tfv'] == null){
				fieldValue = saveValue[source['idt']];
			}
			else{
			  fieldValue = map_details[m]['tfv'];
			}
			}catch(err){
			 this.getEpostAlert("Map Configuration Error for Field : Order of "+map_details[m]['od']);
				return "error"
			}
			try{
				let uid = map_details[m]['co_fld'][0]["idt"];
				control_field = saveValue[uid]
			}
			catch(err){
				control_field = "";
			}
			var item ={
				'FN':target['idt'],
				'FV':fieldValue,
				'DT': referJson['datatype'],
				'SV': referJson['isdbfield'],
				'AD': target["ad"],
				'WT': target["wt"]
			}
		if (control_field == "T" || control_field ==""){
		if(target['pt'] == null)
		{  
			epostJson['primary_table'] = dbTable;
			if(table.length >0){
				const filteredResult = table.filter((item) => {
					console.log(item);console.log(item['table_name']);return (item['table_name'] == dbTable);
				});
				if(filteredResult.length>0){
					filteredResult[0].table_value.push(item);
				}
				else
				{
				var tableObjad = {
					'table_value': [],
				}
				tableObjad.table_value.push(item);
				tableObjad['table_name'] = dbTable;
				tableObjad['od'] = 1;
				if(this.modifyMode == true){
					tableObjad['fromdb'] = 'True';
				}
				table.push(tableObjad);
			}
			
			}else{
				tableObj.table_value.push(item);
				tableObj['table_name'] = dbTable;
				tableObj['od'] = 1;
				if(this.modifyMode == true){
					tableObj['fromdb'] = 'True';
				}
				table.push(tableObj);
			}
			
		}
		else
		{
			if(table.length >0){
			const filteredResult = table.filter((item) => {
   		 	console.log(item);console.log(item['table_name']);return (item['table_name'] == dbTable);
			});
			if(filteredResult.length>0){
			  filteredResult[0].table_value.push(item);
			}else{
				var tableObjad = {
					'table_value': [],
				}
				tableObjad.table_value.push(item);
				tableObjad['table_name'] = dbTable;
				tableObjad['od'] = 2+m;
				if(this.modifyMode == true){
					tableObjad['fromdb'] = 'True';
				}
				table.push(tableObjad);
			}
			console.log(filteredResult);	
			}else{
				tableObj.table_value.push(item);
				tableObj['table_name'] = dbTable;
				tableObj['od'] = 2;
				if(this.modifyMode == true){
					tableObj['fromdb'] = 'True';
				}
				table.push(tableObj);
		}
		}
		}
		}
		epostJson['layesrs'] = table;
		eptValue.push(epostJson);
		console.log(eptValue);
	}
	 
	return eptValue
}

getEpostAlert(message){
	let alert = this.alertCtrl.create({
									title: 'Epost Alert',
									subTitle: message,
									buttons: ['OK']
								});
								alert.present();

}

getSaveAlert(message){
	let alert = this.alertCtrl.create({
									title: 'Information',
									subTitle: message,
									buttons: ['OK']
								});
								alert.present();

}

getConstructedJson(i,component,referJson,table,saveValue,cbValue,base64Str,parentDT,selectedOptions,dynamicPopUpKV)
{
	let errorStatus ="";
	let fieldValue;
	// let id = component["tt"];
	if (component["wt"] == 'text' || component["wt"] == 'password' || component["wt"] == 'email' || component["wt"] == 'number') {
		//fieldvalue = document.getElementById(id).getElementsByTagName("input")[0].value;
		fieldValue = this.getInputfield(component);
	}else if (component["wt"] == 'dpop'){
		fieldValue = dynamicPopUpKV[component["idt"]]["value"];
	} 
	else if (component["wt"] == 'select') {
                    //fieldvalue = document.getElementsByName(id)[0].textContent;
                    fieldValue = this.getSelectfield(component,selectedOptions);
                } else if (component["wt"] == 'date') {
                    //fieldvalue = document.getElementsByName(id)[0].textContent;
                    fieldValue = this.getDatefield(component);
                } else if(component["wt"] == 'textarea')
				{
					fieldValue = this.gettextarea(component);
				} else if (component["wt"] == 'time') {
                    //fieldvalue = document.getElementsByName(id)[0].textContent;
                    fieldValue = this.getTimefield(component);
                } 
				else if (component["wt"] == 'check') {
                    let enum_length = referJson["enum_meta"].length;
                    let keyvalues = referJson["enum_meta"]
                    if (enum_length == 1) {
                        fieldValue = this.getCheckbox(component);
                    } else {
                        cbValue = this.getmultiCheckbox(component);
                        //break;
                    }
                } else if (component["wt"] == 'radio') {
                    fieldValue = this.getRadiobox(component,selectedOptions);
                }
				else if(component["wt"] == 'scan'){
				fieldValue = this.getScanvalue(component);
				}
                else if (component["wt"] == 'upload') {
					let uploadedFileJson: Object =  {};
                    if (base64Str){
                        let uuidVal = this.uuidGenerator();
                        uploadedFileJson['objectid']=uuidVal;
                        uploadedFileJson['base64Val'] = base64Str;
						uploadedFileJson['isExist'] = true;
                        fieldValue = JSON.stringify(uploadedFileJson);
                    }
					else
					{
						uploadedFileJson['isExist'] = false;
                        fieldValue = JSON.stringify(uploadedFileJson);
                       
                    }

                }
                else if (component["wt"] == 'stot') {
                   fieldValue = this.getInputfield(component);

                }
                //layers.push(tablename["table_name"]=component["tt"]);
                if (fieldValue == "error") {
                    errorStatus = "True"
                    return errorStatus;
                } else {
                    var item = {
                        'FN': referJson["field_slug"],
                        'FV': fieldValue,
                        'DT': referJson["datatype"],
                        'SV': referJson["isdbfield"],
                        'AD': component["ad"],
			'WT': component["wt"]
                    }
					saveValue[referJson["field_slug"]] = fieldValue;
					console.log(saveValue);

                    if (table.length == 0) {
                        let order;
                        if (referJson["txtabledetailid"] == parentDT['tb_s']) {
                            order = 1;
                        } else {
                            order = i + 2;
                        }
                        var tablename = {
                            'table_name': referJson["txtabledetailid"],
                            'table_value': [item],
                            'od': order
                        }
						if(this.modifyMode == true){
							tablename['fromdb'] = 'True';
						}
                        table.push(tablename);
                    }
					else
					{
                        let referJson = ""
                        let addStatus = ""
                        referJson = JSON.parse(component["cjson"])
                        for (let j = 0; j < table.length; j++) {
                            //addStatus = false;
                            let tname = table[j].table_name;

                            var index = tname.indexOf(referJson["txtabledetailid"]);
                            //if (table[j].table_name == referJson["tablename"])
                            if (index == 0) {
                                //tvalue.push(table[j].table_value)
                                //console.log("hi");
                                table[j].table_value.push(item);
                                addStatus = "true";
                                if (addStatus == "true") {
                                    continue;
                                }
                            }
                            if (addStatus == "") {
                                if (table[j].table_name != referJson["txtabledetailid"]) {
                                    let order;
                                    if (referJson["txtabledetailid"] == parentDT['tb_s']) {
                                        order = 1;
                                    } else {
                                        order = i + 2;
                                    }

                                    //table.push(tablename);
                                    var tablename = {
                                        'table_name': referJson["txtabledetailid"],
                                        'table_value': [item],
                                        'od': order
                                            //addStatus = false;
                                    }
									if(this.modifyMode == true){
										tablename['fromdb'] = 'True';
									}
                                    addStatus = "True";

                                    if (addStatus == "false") {
                                        break;
                                    }
                                    //addStatus = true;
                                    //table.push(tablename);	
                                }
                            }
                        }
                        if (addStatus == "True") {
                            table.push(tablename);
                        }
                    }

                    //table.push(tablename);
                }
	return errorStatus;
}
	getToast(msg){
		let toast = this.toastCtrl.create({
								 message: msg ,
								 duration: 3000,
								 position: 'bottom'
							 });
							toast.present();
	}

}
