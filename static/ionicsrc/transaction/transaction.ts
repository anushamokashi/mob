import { Component ,ViewChild } from '@angular/core';
import { IonicPage, NavController, NavParams, Platform } from 'ionic-angular';
import { Http } from '@angular/http';
import { ViewController } from 'ionic-angular';
import { AlertController } from 'ionic-angular';
import { ToastController } from 'ionic-angular';
import { LoadingController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { Network } from '@ionic-native/network';
import { BarcodeScanner } from '@ionic-native/barcode-scanner';
import {Validators, FormBuilder, FormGroup } from '@angular/forms';
import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
import { Camera } from '@ionic-native/camera';
import { ImagePicker } from '@ionic-native/image-picker';
import { ActionSheetController } from 'ionic-angular';
import { FileChooser } from '@ionic-native/file-chooser';
import { FilePath } from '@ionic-native/file-path';
import { Base64 } from '@ionic-native/base64';
import { SpeechRecognition } from '@ionic-native/speech-recognition';
import { SQLitePorter } from '@ionic-native/sqlite-porter';

import { TxserviceProvider } from '../../providers/txservice/txservice';
import { ExpressionProvider } from '../../providers/expression/expression';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { NotifyProvider } from '../../providers/notify/notify';
import { PagenavProvider } from '../../providers/pagenav/pagenav';
import { Injector } from '@angular/core';
import { CmserviceProvider } from '../../providers/cmservice/cmservice';

import { ModalController } from 'ionic-angular';
import { SearchmodalPage } from '../searchmodal/searchmodal';
import { HomePage } from '../home/home';
declare var setEformVarMap : any;
declare var setGetFieldval : any;
declare var Mustache:any;
declare var cordova : any;
declare var convertTime24to12 :any;
declare var window: any;
declare var gapi: any;
//declare var validate:any;
/**
 * Generated class for the TransactionPage page.
 *
 * See http://ionicframework.com/docs/components/#navigation for more info
 * on Ionic pages and navigation.
 */
@Component({
  selector: 'page-transaction',
  templateUrl: 'transaction.html',
	providers:[TxserviceProvider,ExpressionProvider],
})
export class TransactionPage {
   
    //cucumber:any; 
    username: any;
    networkStatus: any;
    UserDetails: any;
    public stValues: any;
	public viewMode: boolean = false;
	public modifyMode: boolean = false;
    pid: any;
    userid: any;
    projectname: any;
    requiredValue: any;
    optionsJson: Object =  {}; 
    sqlSelectFieldValue: any[] = [];
    elementList: any[] = [];
    selectedOptions: Object =  {};
    preset_value: Object =  {};
    selectedRow: any;
    jsonUrl:any;
    database:any;
    modelpages: Array < {
        id: string,
        component: any
    } > ;
    newpics:any[]=[];
    storedpics:any[]=[];
    newdocs:any[]=[];
    private fileCount = 0;
    //blobArray:any[]=[];
    base64Str:any;
    speech: any;
    pagenav:any;
    viewJson : any;
    ismultitenant:any;
    dynamicpopup_key_value_array : Object =  {};

    constructor(public navCtrl: NavController, public navParams: NavParams,public viewCtrl: ViewController, public modalCtrl: ModalController, private network: Network, private sqlite: SQLite, public storage: Storage, public singleton: SingletonProvider, public myexpression: ExpressionProvider, public mytxservice: TxserviceProvider, public http: Http, private alertCtrl: AlertController, 
        private toastCtrl: ToastController,private barcodeScanner: BarcodeScanner,private camera: Camera, private imagePicker: ImagePicker,private actionSheetCtrl: ActionSheetController,private base64: Base64,
            private fileChooser: FileChooser,private filePath: FilePath,private injector: Injector,private sqlitePorter: SQLitePorter,
            public loadingCtrl: LoadingController,private speechRecognition: SpeechRecognition,public notifyProvider :NotifyProvider,
            public mycmservice: CmserviceProvider) {
		this.jsonUrl = 'assets/json/transaction.json';
        this.projectname = this.singleton.projectname;
        this.UserDetails = this.navParams.get("userdetails");
        this.pagenav = this.injector.get(PagenavProvider);
		this.pid = this.singleton.PID;
		this.ismultitenant = this.singleton.ismultitenant;
		
		if (this.UserDetails != undefined && this.UserDetails['viewMode'] !=undefined )
		{
		  this.viewMode = this.UserDetails['viewMode'];
		  this.modifyMode = this.UserDetails['modifyMode'];
		}
		
        if (this.UserDetails == undefined) {
            this.storage.get('userObj').then((loginInfo) => {
                //console.log(loginInfo);
                this.UserDetails = loginInfo;
				this.UserDetails['pagetype'] = 'txview';//for differentiate transaction or report in expr.js
				this.UserDetails['modifyMode'] = this.modifyMode;
            });
        }
		else{
		    this.UserDetails['pagetype'] = 'txview';//for differentiate transaction or report in expr.js
			this.UserDetails['modifyMode'] = this.modifyMode;
		}
        this.modelpages = [
        ];
       
    }

    ionViewDidLoad() {
    
        this.UserDetails = this.navParams.get("userdetails");
        console.log('ionViewDidLoad TransactionPage');
        let initalHiddenComponents: any[] = [];

        //GET ALL ELEMENTS
        let elements = document.getElementById('myForm').querySelectorAll('*[name]');
        for (let i = 0; i < elements.length; i++) {
            if (elements[i].id != "" && elements[i].tagName != "ION-CHECKBOX") {
                this.elementList.push(elements[i].id);
            }
        }

        //GET INITIAL HIDDEN ELEMENTS AND READONLY ELEMENTS
        for (let i of this.elementList) {
            if (document.getElementById(i).dataset.hidden == "True" || document.getElementById(i).dataset.readonly == "True") {
                initalHiddenComponents.push(i);
            } else {
                break;
            }
        }

        //IF ININITAL ELEMET EXIST CALL EXPRESSION.TS 
        if ((initalHiddenComponents.length) != 0) {
            this.myexpression.hiddenElementexp(initalHiddenComponents, this.UserDetails,this.preset_value,this.selectedOptions,"transaction",this,false);
        }
		
        this.http.get('assets/json/transaction.json').map(res => res.json()).subscribe(data => {
            this.viewJson = data[0];
            let containerFieldsObj = {};
            
            let eFormId = this.viewJson['idt']
            let projectId = this.viewJson['pt']
            let containerMeta = this.viewJson['cont_meta']
            
            //ONFORMLOAD EVENT
            let eventStr =   this.viewJson['pos'];
            if (eventStr){
                let eventJson = JSON.parse(eventStr);
                try {
                    if (eventJson.onformload.COMPEVENT) {
                        for (let i = 0; i < eventJson.onformload.COMPEVENT.length; i++) {
                            let elementEvent = eventJson.onformload.COMPEVENT[i];
                            this.myexpression.evaluateEventexp(elementEvent, this.UserDetails, eFormId);
                        }
                    }
                } catch (e) {
                    console.log(e);
                }
            }
            
            
            
            
            //CHECK SQL FOR PARENT AND CHILD CONTAINER'S NON-HIDDEN COMPONENTS 
            for(let i=0;i<containerMeta.length;i++){
                let ComponentMeta = containerMeta[i]['comp_meta']
                let childrenMeta = containerMeta[i]['children']
                let SqlCompFields = this.filterSqlFields(ComponentMeta);
                if(SqlCompFields.length>0){
                    this.getOptions(eFormId,SqlCompFields,containerMeta[i]['ctype'],containerMeta[i]['db']);
                }
                for (let j=0;j<childrenMeta.length;j++){
                    let ChildrenComponentMeta = childrenMeta[j]['comp_meta']
                    let childrenSqlCompFields = this.filterSqlFields(ChildrenComponentMeta);
                   
                    if(childrenSqlCompFields.length>0){
                        this.getOptions(eFormId,childrenSqlCompFields,childrenMeta[j]['ctype'],childrenMeta[j]['db']);
                    }
                    
                }
            }
			
			if (this.UserDetails != undefined && this.UserDetails['viewMode'] !=undefined ){
				let recordId = this.UserDetails['recordId'];
				let parent_table = data[0]['tran_meta'][0]["prm_meta"][0]['tb'];
				let tx_id = data[0]['idt'];
				let parent_tableid = parent_table+'id';
				let json ={};
				let table_list =[];
				let cont_meta = data[0]['cont_meta'];
				
				for(let k= 0;k<cont_meta.length;k++){
					let children  = cont_meta[k]['children'];
					this.field_json(table_list,cont_meta[k]);
					
					if(children.length >0){
						for(let j=0;j<children.length;j++){
							this.field_json(table_list,children[j]);
							if(children[j]['children'].length >0){
								for(let l=0;l<children[j]['children'].length;l++){
									this.field_json(table_list,children[j]['children'][l]);
								}
							}
						}
					}
				}
				console.log(table_list);
				json['table_list'] = table_list;
				json['recordId'] = recordId;
				json['parent_id'] = parent_tableid;
				json['pid'] = this.pid;
				json['mlt'] = this.ismultitenant;
				this.mytxservice.getSearchrecord(json).subscribe(response => {
					console.log(response);
					let dataSet = response['_body'];
					this.presetInputValue(dataSet);
				});
			}
			
        });
	}
		
	
	field_json(table_list,cont_meta){
		let table = {};
		let fields =[];
		table['tablename'] = cont_meta['db'];
		let component = cont_meta['comp_meta'];
		for(let i =0;i<component.length;i++){
			if(component[i]['cjson'] != ""){
			let field = this.fields_get(component[i]);
			fields.push(field);
			}
		}
		table['fields'] = fields;
		table_list.push(table);
	}
	
	fields_get(component){
		let cjson = JSON.parse(component['cjson']);
		let field_slug = cjson['field_slug'];
		return field_slug
	}

    filterSqlFields(componentsArray){
        //WILL ONLY GET NON HIDDEN SQL FIELDS
        let sqlCompFields = componentsArray.filter((item)=>{
            return (item['wt'] == 'select' && item['sql'] != null && item['sql'] != "" && item['ih'] == "False" && item['isdep'] == "False" || 
            item['wt'] == 'radio' && item['sql'] != null && item['sql'] != "" && item['ih'] == "False" && item['isdep'] == "False" ||
            item['wt'] == 'check' && item['sql'] != null && item['sql'] != "" && item['ih'] == "False" && item['isdep'] == "False" ||
            item['wt'] == 'email' && item['sql'] != null && item['sql'] != "" &&  item['ih'] == "False" && item['isdep'] == "False" || 
            item['wt'] == 'number' && item['sql'] != null && item['sql'] != "" && item['ih'] == "False" && item['isdep'] == "False" || 
            item['wt'] == 'text' && item['sql'] != null && item['sql'] != "" && item['ih'] == "False" && item['isdep'] == "False")
        });
        return sqlCompFields;

    }

    getOptions(eFormId,fields,ctype,dbName){
        for (let i=0;i<fields.length;i++){
            
            let currentField = fields[i];
            let fieldID;
            if(ctype == "grid"){
                fieldID = currentField['idt']+"_"+dbName;
            }
            else{
                fieldID = currentField['idt'];                        
            }
            let widgetType = currentField['wt'];
            let sqlObj = JSON.parse(currentField['sql']);
            let sql = sqlObj["Sql"]
            let sqlDbType = sqlObj["sqlDbType"];
            let key = sqlObj["key"]
            let value = sqlObj["value"]
            let paramStr = this.myexpression.findParamValues(sql,this.preset_value);
            
            if (sqlDbType == "server"){
            
                //Assiging values 
                let data  = {
                    fieldType : "combofield",
                    eFormId :eFormId,
                    fieldName : currentField['idt'],
                    projectName : this.singleton.projectname,
                    projectId : this.singleton.PID,
                    username : this.UserDetails["USERNAME"], 
                    type : "transaction",  
                    MapValue : paramStr,                  
                
                };
                console.log(data); 
                //call service
                this.mytxservice.customSelectService(data).subscribe(loginData => {
                    let result = [];
                    this.sqlSelectFieldValue = loginData.json();
                    console.log(this.sqlSelectFieldValue);
                    // for (let i = 0; i < this.sqlSelectFieldValue.length; i++) {
                    //     result.push(this.sqlSelectFieldValue[i][Object.keys(this.sqlSelectFieldValue[i])[0]]);
                    // }
                    // this.optionsJson[currentField.id] = result;
                    if(widgetType == "select" || widgetType == "check" || widgetType == "radio" ){
                        this.optionsJson[fieldID] = this.sqlSelectFieldValue;
                    }
                    else if(widgetType == "dpop"){
                        this.optionsJson[fieldID] = this.sqlSelectFieldValue;
                        let radioAlert = this.alertCtrl.create();
                        radioAlert.setTitle('Select');
                        let isChecked = false;
                       
                        for(let i=0;i<this.sqlSelectFieldValue.length;i++){
                            if(this.preset_value[fieldID]!= null && this.preset_value[fieldID] != undefined && this.preset_value[fieldID] == this.sqlSelectFieldValue[i][value]){
                                isChecked = true;
    
                            }
                            else{
                                isChecked = false;
                            }
                            radioAlert.addInput({
                                type: 'radio',
                                label: this.sqlSelectFieldValue[i][key],
                                value: this.sqlSelectFieldValue[i][value],
                                checked: isChecked
                            })

                        }
                        radioAlert.addButton('Cancel');
                        radioAlert.addButton({
                            text: 'OK',
                            handler: data => {
                                console.log("Ordered",data);
                                this.preset_value[fieldID] = data;
                                
                                const filter = this.sqlSelectFieldValue.filter((item) => {
                                    return (item[value] == data);
                                });
                                if(filter.length >0){
                                    try{
                                        let keyValueJson = {
                                            key : filter[0][key],
                                            value : filter[0][value]
                                        }
                                        this.dynamicpopup_key_value_array[fieldID] = keyValueJson;
                                        this.preset_value[fieldID] = filter[0][key];
                                    }catch(err){
                                        this.dynamicpopup_key_value_array[fieldID] = "";
                                    }
                                    
                                    
                                }
                                this.setValueForLogicalField(fieldID,data);
                           
                            }
                        });
                        radioAlert.present();
                        
                       
                    }
                    else{
                        this.preset_value[fieldID] = this.sqlSelectFieldValue[0][sqlObj["value"]]
                    }
                    
                    
                   
                });

            }
            
            else if (sqlDbType == "client"){
                
                let optionArray = [];
                console.log("client db sql")
                this.sqlite.create({
                    name: 'data.db',
                    location: 'default'
                })
                .then((db: SQLiteObject) => {
                    this.database = db;
                    db.executeSql(sql,{})
                        .then((data) => {
                            let result = [];
                            console.log(data.rows);
                           
                            for (var i = 0; i < data.rows.length; i++) {
                                for (var index in data.rows.item(i)) {
                                    let optionObj = {};
                                    optionObj[index] = data.rows.item(i)[index];
                                    optionArray.push(optionObj);
                                    result.push(data.rows.item(i)[index]);
                                }
                            } 
                           
                            if(widgetType == "select" || widgetType == "check" || widgetType == "radio" ){
                                this.optionsJson[fieldID] = optionArray;
                            }
                            else{
                                this.preset_value[fieldID] = optionArray[0][sqlObj["value"]]
                            }
                                                      
                        })
                        .catch(e => console.log(e));                    
                })
                .catch(e => console.log(e));
            }

        }
    }

    new() {
        this.navCtrl.push(this.navCtrl.getActive().component,{'userdetails':this.UserDetails}).then(() => {
            let index = this.viewCtrl.index;
            this.navCtrl.remove(index);
        });
    }

    save($event) {
        let saveStatus;
        let saveExp =  "";
		let action_meta = this.viewJson.action_meta;
		if(action_meta.length > 0){
			const filter = action_meta.filter((item) => {
					 return (item['at'] == 'Save');
			});
			if(filter.length >0){
				try{
					saveExp =  filter[0]['save']['exp'];
				}catch(err){
					saveExp =  "";
				}
				
			  
			}
        }
        
        let expArray = saveExp.split('(');
        
       
        

		const loading = this.loadingCtrl.create({
			spinner: 'bubbles',
			content: 'Saving! Please Wait...'
		});
		loading.present();
        saveStatus = this.mytxservice.saveJson(this.UserDetails,this.jsonUrl,"tr",this.base64Str,this.selectedOptions,loading,this.pagenav,this.preset_value,saveExp,this.dynamicpopup_key_value_array);
    }

    googleSync(event){
        let syncExp;
        var thisAfterCallback  =this;
        let action_meta = this.viewJson.action_meta;
		if(action_meta.length > 0){
			const filter = action_meta.filter((item) => {
					 return (item['at'] == 'GoogleSync');
			});
			if(filter.length >0){
				try{
					syncExp =  filter[0]['googlesync']['exp'];
				}catch(err){
					syncExp =  "";
				}
				
			  
            }
            console.log(syncExp);
            if(syncExp == "googlecalendar()"){
                this.http.get('assets/json/calendarevent.json').map(res => res.json()).subscribe(data => {
                    let eventjson = data;
                    let desc,location,endDate,endTime,email,popup = "";

                    if(eventjson.desc == null || this.preset_value[eventjson.desc] == undefined){
                        desc = null;
                    }
                    else{
                        desc = this.preset_value[eventjson.desc];
                    }
                    
                    if(eventjson.location == null || this.preset_value[eventjson.location] == undefined){
                        location = null;
                    }
                    else{
                        location = this.preset_value[eventjson.location];
                    }
                    
                    if(eventjson.end_day == null || this.preset_value[eventjson.end_day] == undefined){
                        endDate = this.preset_value[eventjson.start_day];
                        endTime = "24:00"
                       
                    }
                    else{
                        endDate = this.preset_value[eventjson.end_day];
                    }
                    
                    if(eventjson.end_time == null || this.preset_value[eventjson.end_time] == undefined){
                        endTime = "24:00"
                        
                    }
                    else{
                        endTime = this.preset_value[eventjson.end_day];
                    }
                    if(eventjson.email == null || this.preset_value[eventjson.email] == undefined){
                        email = "60"
                    }
                    else{
                        email = this.preset_value[eventjson.email];
                    }
                    if(eventjson.popup == null || this.preset_value[eventjson.popup] == undefined){
                        popup = "10"
                    }
                    else{
                        popup = this.preset_value[eventjson.popup];
                    }
                    
                    let calendarEvent:any = {};
                    let validation:any = {};
                    let attendees = [{
                       email:""
                    }];
                    let CLIENT_ID = this.singleton.googleclientid; // Client ID of your google console project
                    let SCOPES = ["https://www.googleapis.com/auth/calendar"];
                    let APIKEY = this.singleton.googleapikey;  // API key of your google console project
                    let REDIRECTURL ="http://localhost/callback";

                    var startDateTimeISO = this.buildISODate(this.preset_value[eventjson.start_day], this.preset_value[eventjson.start_time]);
                    var endDateTimeISO = this.buildISODate(endDate, endTime);
                
                    validation.failure = false;
                    var browserRef = window.cordova.InAppBrowser.open('https://accounts.google.com/o/oauth2/auth?client_id=' + CLIENT_ID + '&redirect_uri=' + REDIRECTURL + '&scope=https://www.googleapis.com/auth/calendar&approval_prompt=force&response_type=token', '_blank', 'location=no,zoom=no');         //clearsessioncache=yes,clearcache=yes
                    browserRef.addEventListener("loadstart", (event) => {
                        if ((event.url).indexOf("http://localhost/callback") === 0) {
                            browserRef.removeEventListener("loaderror", (event) => { 
                                console.log(event.message);
                            });
                            browserRef.removeEventListener("exit", (event) => { 
                                console.log(event);
                            });
                            browserRef.close();
                            var url = event["url"];
                            var token = url.split('access_token=')[1].split('&token_type')[0];
                            console.log("***********");
                            console.log(token);
                            
                            //SENDING THE INVITE USING THE GOOGLE CALENDAR API
                            gapi.client.setApiKey(APIKEY);
                            var request = gapi.client.request({
                                'path': '/calendar/v3/calendars/primary/events?alt=json',
                                'method': 'POST',
                                'headers': {
                                    'Authorization': 'Bearer ' + token
                                },
                                'body': JSON.stringify({
                                    "summary": this.preset_value[eventjson.title],
                                    "location": location,
                                    "description": desc,
                                    "start": {
                                        "dateTime": startDateTimeISO,
                                        "timeZone": "Asia/Kolkata" // TODO : Parameterize this
                                    },
                                    "end": {
                                        "dateTime": endDateTimeISO,
                                        "timeZone": "Asia/Kolkata" // TODO : Parameterize this
                                    },
                                    "recurrence": [
                                        "RRULE:FREQ=DAILY;COUNT=1" //// TODO : Parameterize this, Frequency of the event
                                    ],
                                    // "attendees": "arunjack21@gmail.com",
                                    "reminders": {
                                        "useDefault": false,
                                        "overrides": [
                                            {
                                                "method": "email",
                                                "minutes": email  // TODO : Parameterize this, No. of minutes before you want google services to send an email reminder
                                            },
                                            {
                                                "method": "popup",
                                                "minutes": popup  	// TODO : Parameterize this, No. of minutes before you want google services to send an popup reminder
                                            }
                                        ]
                                    }
                                }),
                                'callback': function (jsonR, rawR) {
                                    if(jsonR.id){
                                        let alert = thisAfterCallback.alertCtrl.create({
                                            title: 'Sync Alert',
                                            subTitle: "Successfully synced with your google calendar.",
                                            buttons: ['Dismiss']
                                        });
                                        alert.present();
                                        thisAfterCallback.save(event);

                                    } else {
                                        let alert = thisAfterCallback.alertCtrl.create({
                                            title: 'Sync Alert',
                                            subTitle: "Failed to sync!",
                                            buttons: ['Dismiss']
                                        });
                                        alert.present();
                                    }
                                    console.log(jsonR); // Everything related to invite once created, use this for further enhancements
                                }
                            });
                        }
                    });
                    browserRef.addEventListener('loaderror', function(event) { 
                        // alert('error: ' + event.message); 
                    });
                });


            }

        }
    }

    buildISODate(date, time){
        var dateArray = date && date.split('-');
        var timeArray = time && time.split(':');
        var normalDate = new Date(parseInt(dateArray[0]), parseInt(dateArray[1])-1, parseInt(dateArray[2]), parseInt(timeArray[0]), parseInt(timeArray[1]), 0, 0);
        return normalDate.toISOString();
    }

    uploadedFileData(){
        
        let fileuris;
        this.base64Str = "";
        console.log("URL LENGTH");
        console.log(this.fileCount);
        
        if(this.fileCount>0){
            if(this.storedpics.length == 0 && this.newdocs.length == 0 && this.newpics.length >0){
                fileuris = this.newpics

            }
            else if(this.newpics.length == 0 && this.newdocs.length == 0 && this.storedpics.length >0 ){
                fileuris = this.storedpics

            }
            else if(this.storedpics.length == 0 && this.newpics.length == 0 && this.newdocs.length >0 ){
                fileuris = this.newdocs

            }
            else{
                fileuris = null;
            }

        }
        for(let i=0;i<fileuris.length;i++){
            this.base64.encodeFile(fileuris[i])
            .then((base64File: string) =>{
                this.base64Str = (base64File.split(',')[1]);
            });
        }
    }
    
    checkFocus(event) {

    }

    runTimeChange(event) {
        //console.log(event);
    }

    onFocus(event) {
        //console.log("focus");
        let formEvent;
        let form;
        let id = event._elementRef.nativeElement.dataset["id"];
        let widgetType = event._elementRef.nativeElement.dataset["widgettype"];
        let wholeform = document.getElementsByName('myForm')[0];
        let eformid = wholeform.dataset["eformid"];
        form = document.getElementsByName('myForm')[0].children[0];

        //IF COMPONENT HAVING SQL
        let sql = event._elementRef.nativeElement.dataset["sql"];
     
        if(sql != ""){
            let sqlValueDependent = event._elementRef.nativeElement.dataset["sqlvaluedependent"];
            if (sqlValueDependent == "True"){
                let ctype = ""
                let db = "";
                let currentFieldJson;
                let containerMeta = this.viewJson['cont_meta']
                for(let i=0;i<containerMeta.length;i++){
                    let componentMeta = containerMeta[i]['comp_meta'];
                    const filter = componentMeta.filter((item) => {
                        return (item['idt'] == id);
                    });
                    if(filter.length>0){
                        ctype = containerMeta[i].ctype;
                        db = containerMeta[i].db;
                        this.getOptions(eformid,filter,ctype,db);
                        break;
                    }
                    

                }

            }
            else{
                if(widgetType == "select" || widgetType == "radio" || widgetType == "check"){

                }
                else{
                    let sqlValue = event._elementRef.nativeElement.dataset["sqlvalue"];
                    let inputValArray:any;
                    try{
                        inputValArray = this.optionsJson[id]
                    }
                    catch(err){
                        inputValArray = [];
                    }
                    if (inputValArray != undefined){
                        if (inputValArray.length>0){
                            let valStr = inputValArray[0][sqlValue];
                            (<HTMLInputElement>document.getElementById(id)).value = valStr;
                            (<HTMLInputElement>document.getElementById(id)).textContent = valStr;
                        }
            
                    }
                }
            }
        }
       
       //IF COMPONENT HAVING ONENTER EVENT
        try{
           formEvent =JSON.parse(form.dataset['event']); 
        }
        catch(e){
            formEvent = "";
        }
        if (formEvent != "") {
            try {
                if (formEvent.onenter[id]) {
                    for (let i = 0; i < formEvent.onenter[id].length; i++) {
                        let elementEvent = formEvent.onenter[id][i];
                        this.myexpression.evaluateEventexp(elementEvent, this.UserDetails, eformid);
                    }
                }
            } catch (e) {
                console.log(e);
            }

        }

        //IF COMPONENT HAVING EXPRESSION
        let DOM = document.getElementsByName(id);
		try {
            this.myexpression.evaluateExp(event, DOM, this.UserDetails,this.preset_value);
		}
		catch(e){
            console.log(e);
		}
    }

    checkBlur(event) {
        let formEvent;
        let form;
        let id = event._elementRef.nativeElement.dataset["id"];

        //CHECK FOR ONEXIT EVENT
        let wholeform = document.getElementsByName('myForm')[0];
        let eformid = wholeform.dataset["eformid"];
        form = document.getElementsByName('myForm')[0].children[0];
        try {
            formEvent = JSON.parse(form.dataset['event']);
        } catch (e) {
            formEvent = "";
        }

        if (formEvent != "") {
            try {
                if (formEvent.onexit[id]) {
                    for (let i = 0; i < formEvent.onexit[id].length; i++) {
                        let elementEvent = formEvent.onexit[id][i];
                        this.myexpression.evaluateEventexp(elementEvent, this.UserDetails, eformid);
                    }
                }

            } catch (e) {
                //console.log(e);
            }

        }

        //CHECK FOR NEXT HIDDEN ELEMENTS		
		this.next_hiddenelements(id);
    }

    checkChange($event, elemtId) {
        let formEvent;
        let form;
        let id = elemtId;
        let ctEform;
        let eformVarMap = {};
        let elementIdList = []
        let choosenValue = $event;
	try{
			if($event._componentName =="checkbox"){
				let check_array = {};
				let check_id = $event._elementRef['nativeElement']['id'];
				let checked = $event._value;
				let check_value = $event._elementRef['nativeElement']['dataset']['value'];
				check_array['id'] = check_id;
				check_array['checked'] = checked;
				check_array['value'] = check_value;
				if (this.selectedOptions[elemtId] != undefined){
						const index = this.selectedOptions[elemtId].findIndex((item) => {
							return (item['id'] == check_id);
						});
					if (index != -1){
						this.selectedOptions[elemtId][index]['id'] = check_id;
						this.selectedOptions[elemtId][index]['checked'] = checked;
						this.selectedOptions[elemtId][index]['value'] = check_value;
					}
					else
					{
					    this.selectedOptions[elemtId].push(check_array);
					}
					
					
				}else{
				    this.selectedOptions[elemtId] = [check_array];
				}
			}
		else{
				this.selectedOptions[elemtId] = $event;
			}

		}
		catch(err){
			console.log(err);
		}
        
        //*******************************************//
        //Do this under condition
        this.setValueForLogicalField(id,choosenValue);
       
       

        
        //************************************************************** */

		let radio_group = document.getElementsByName(id)[0]['attributes']['radio-group'];
		if (radio_group){
        let combObj = document.getElementsByName(id)[0].children;
        for (let j = 1; j < combObj.length; j++) {
            combObj[j].firstChild["lastElementChild"].firstChild.className = "radio-icon";
        }
		}
        let wholeform = document.getElementsByName('myForm')[0];
        let eformid = wholeform.dataset["eformid"];
        form = document.getElementsByName('myForm')[0].children[0];
        try {
            formEvent = JSON.parse(form.dataset['event']);
        } catch (e) {
            formEvent = "";
        }
        ctEform = eformid;
        if (formEvent != "") {
            try {
                if (formEvent.onchange[id]) {
                    for (let i = 0; i < formEvent.onchange[id].length; i++) {
                        let elementEvent = formEvent.onchange[id][i];
                        let hasVariable = elementEvent.split(":=");
                        if (hasVariable.length === 1) {
                            this.myexpression.evaluateEventexp(hasVariable[0], this.UserDetails, eformid);
                        } else {
                            let cache = hasVariable[0].replace(/^\s*/, "").replace(/\s*$/, "");
                            setGetFieldval(event);
                            let resultSet = this.myexpression.evaluateEventexp(hasVariable[1], this.UserDetails, eformid);
                            if (cache !== null && resultSet !== null) {
                                eformVarMap[ctEform + "-" + cache.toLowerCase()] = " :-:" + resultSet;
                                setEformVarMap(eformVarMap);
                            } else {
                                return null;
                            }
                        }

                    }
                }

            } catch (e) {
                //console.log(e);
            }
        }
         
		this.next_hiddenelements(elemtId);

    }

    next_hiddenelements(elemtId){
        //GET NEXT HIDDEN ELEMENTS FOR SQL AND EXP
        
        let nextHiddenComponents: any[] = [];
		let elementIdList = [];

        let elements = document.getElementById('myForm').querySelectorAll('*[name]');
        
        for (let i = 0; i < elements.length; i++) {
            if (elements[i].id != "") {
                elementIdList.push(elements[i].id);
            }
        }
        var unique = elementIdList.filter(function(elem, index, self) {
            return index === self.indexOf(elem);
        })
        var remainigArray  = unique.slice((unique.indexOf(elemtId)+1),(unique.length+1));
       
        for (let i of remainigArray) {
            if (document.getElementById(i).dataset.hidden == "True" || document.getElementById(i).dataset.readonly == "True") {
                nextHiddenComponents.push(i);
            }
            // else if(document.getElementById(i).dataset. sqlvaluedependent == "True"){

               
            //     break;
            // }
            else{
                break;
            }
        }

        if ((nextHiddenComponents.length) != 0) {
            this.myexpression.hiddenElementexp(nextHiddenComponents, this.UserDetails,this.preset_value,this.selectedOptions,"transaction",this,false);
        }
        
	}

    checkClick(event) {
        //console.log(event);
        //console.log("Button");
    }

    setValueForLogicalField(id,choosenValue){
        let selectedOptionValues = {}
        var cjsonStr = document.getElementById(id).dataset.referjson
        var cjson = JSON.parse(cjsonStr);
        if (cjson.datatype == "OneToOneField"){

            var logicalFieldValues = this.optionsJson[id]
            for(var values of logicalFieldValues)
            {
                let singleObj = {}
                singleObj = values;
                for(var key in singleObj){
                    if(singleObj[key] == choosenValue){
                        console.log(choosenValue) 
                        selectedOptionValues = singleObj
                    }

                }

            }
            for(var key in selectedOptionValues){

                let logicalFieldID = "logical_"+id+"_"+key;
                // (<HTMLInputElement>document.getElementById(logicalFieldID)).value = selectedOptionValues[key];
                // (<HTMLInputElement>document.getElementsByName(logicalFieldID)[1]).value = selectedOptionValues[key];
                this.preset_value[logicalFieldID] = selectedOptionValues[key];
            

            }

        }
    }


    presentModal(id) {
        //console.log(id);
        let pg;
        for (let i = 0; i < this.modelpages.length; i++) {
            if (this.modelpages[i].id == id) {
                pg = i;
            }
        }

        let tableId = id;
		if(this.viewMode == true){
			tableId = id+"_ET";
		}
        let modal = this.modalCtrl.create(this.modelpages[pg].component,{'options':this.optionsJson});
        modal.onDidDismiss(data => {
            //console.log(data);
            if (data) {
                //console.log(this.elementList);
                let table = document.getElementsByName(tableId)[0];
				let tableid = table.id; 
                let tbody = table.getElementsByTagName('tbody')[0];
                let rowlength = tbody.rows.length;
                let newRow = tbody.insertRow(tbody.rows.length);
                //let row = table["insertRow"](rowlength);
                let headerColumn = table.getElementsByTagName('th');
                newRow.id = tableid + rowlength;
                let cellength = table["rows"][0].cells.length;
                //row.addEventListener('click', handleEvent);		
                newRow.addEventListener("click", event => {
                    newRow.style.background = "lightgrey";
                    this.selectedRow = newRow.id;
                });

                for (let i = 0; i < cellength; i++) {

                    let newCell = newRow.insertCell(i);
                    // Append a text node to the cell
					let fieldValue ="";
					newCell['dataset']['type']=headerColumn[i]['dataset']['type'];
					let check_element_id = headerColumn[i]['dataset']['elementid'];
					newCell['dataset']['header_id'] = check_element_id;
					if(headerColumn[i]['dataset']['type'] == 'select' || headerColumn[i]['dataset']['type'] == 'radio'){
						if(data.items[i] != ""){
						fieldValue = data['item_choosed'][check_element_id][0][data.items[i]];
						newCell['dataset']['select_value'] = data.items[i];
						}
						else
						{
							fieldValue = "";
							newCell['dataset']['select_value'] = data.items[i];
						}
						
					}
					else if(headerColumn[i]['dataset']['type'] == 'check'){
						let value = check_element_id+"_Cvalue";
						let box = check_element_id+"_Cbox";
						fieldValue = data.items[i];
						newCell['dataset']['select_value'] = data['item_choosed'][value];
						newCell['dataset']['carray'] = JSON.stringify(data['item_choosed'][box]);
					}
					else if(headerColumn[i]['dataset']['type'] == 'time' || headerColumn[i]['dataset']['type'] == 'date'){
						fieldValue = data.items[i];
						newCell['dataset']['select_value'] = data['item_choosed'][check_element_id];
					}
					else
					{
						fieldValue = data.items[i];
						newCell['dataset']['select_value'] = data.items[i];
					}
					let newText = document.createTextNode(fieldValue);
                    newCell.appendChild(newText);
                    if (headerColumn[i].hidden == true) {
                        newRow.cells[i].hidden = true;
                    }
                }
            }
        });
        modal.present();
    }
    editModal(id) {
        //console.log(this.selectedRow);
        if (this.selectedRow) {
            let row = document.getElementById(this.selectedRow)
            let rowElement = document.getElementById(this.selectedRow).childNodes;
            //console.log(rowElement);
			let pg;
			for (let i = 0; i < this.modelpages.length; i++) {
				if (this.modelpages[i].id == id) {
					pg = i;
				}
			}
            let modal = this.modalCtrl.create(this.modelpages[pg].component, {
                rowValues: rowElement,'options':this.optionsJson
            });
            modal.onDidDismiss(data => {
                if (data) {
                    for (let i = 0; i < rowElement.length; i++) {
						let header_id = rowElement[i]['dataset']['header_id'];
						if(rowElement[i]['dataset']['type'] == "select" || rowElement[i]['dataset']['type'] == 'radio'){
							rowElement[i].textContent = data["item_choosed"][header_id][0][data.items[i]];
							rowElement[i]['dataset']['select_value'] = data.items[i];							
						}
						else if(rowElement[i]['dataset']['type'] == "check") {
							
							let value = header_id+"_Cvalue";
							let box = header_id+"_Cbox";
							rowElement[i].textContent = data.items[i];
							rowElement[i]['dataset']['select_value'] = data['item_choosed'][value];
							rowElement[i]['dataset']['carray'] = JSON.stringify(data['item_choosed'][box]);
						}
						else if(rowElement[i]['dataset']['type'] == 'time')
						{
							rowElement[i].textContent = data.items[i];
							rowElement[i]['dataset']['select_value'] = data['item_choosed'][header_id];
						}
						else{
							rowElement[i].textContent = data.items[i];
							rowElement[i]['dataset']['select_value'] = data['item_choosed'][header_id];
							
						}
                    }
                }
            });
            modal.present();
            row.style.background = "white";
            this.selectedRow = "";
        }
    }

    offlineSync() {
        if (this.network.type == "none") {
            let alert = this.alertCtrl.create({
                title: 'Sync Alert',
                subTitle: "Internet Connection Needed",
                buttons: ['Dismiss']
            });
            alert.present();
        } else {
            this.storage.get('offStore').then((offlineStore) => {
                //console.log(offlineStore);
                if (offlineStore != null) {
                    for (let i = 0; i < offlineStore.length; i++) {
                        this.mytxservice.sendSavejson(offlineStore[i]).subscribe(saveMessage => {
                                // console.log(saveMessage.json());
                                this.storage.remove('offStore');
                                let alert = this.alertCtrl.create({
                                    title: 'Alert',
                                    subTitle: "Offile Stored Data Updated",
                                    buttons: ['Dismiss']
                                });
                                alert.present();
                            },
                            err => {
                                //console.log("Oops!");
                                let alert = this.alertCtrl.create({
                                    title: 'Information',
                                    subTitle: 'Server Connection Error.',
                                    buttons: ['OK']
                                });
                                alert.present();
                                //return saveStatus;
                            });
                    }
                }
                if (offlineStore == null) {
                    let alert = this.alertCtrl.create({
                        title: 'Alert',
                        subTitle: "No Offile Stored Data",
                        buttons: ['Dismiss']
                    });
                    alert.present();
                }
            });
        }
    }

    scan(event, id) {
        this.barcodeScanner.scan({
            showTorchButton: true
        }).then((barcodeData) => {
            //console.log(barcodeData);
            //console.log(event);
            //console.log(id);
            if (barcodeData['cancelled'] == false) {
                document.getElementById(id).getElementsByTagName("input")[0].value = barcodeData['text'];
            } else if (barcodeData['cancelled'] == true) {
                let alert = this.alertCtrl.create({
                    title: 'Alert',
                    subTitle: 'User Cancelled Operation.',
                    buttons: ['Dismiss']
                });
                alert.present();
            }

        }, (err) => {
            // An error occurred
        });

    }

    togglecolumn(id) {
		let table_id  =id;
		if(this.viewMode == true){
			table_id = id+"_ET";
		}
        let alert = this.alertCtrl.create();
        alert.setTitle('Select Column To Show');
        let table = document.getElementById(table_id);
        for (let i = 0; i < table['rows'][0].cells.length; i++) {
            let checkvalue: any;
            let labelvalue: any;
            if (table['rows'][0].cells[i].hidden == false) {
                checkvalue = true;
            }
            if (table['rows'][0].cells[i].dataset['hidden'] == "false") {
                alert.addInput({
                    type: 'checkbox',
                    label: table['rows'][0].cells[i].textContent,
                    name: 'input-mango',
                    id: 'input-mango',
                    value: table['rows'][0].cells[i].id,
                    checked: checkvalue
                });
            }

        }

        alert.addButton('Cancel');
        alert.addButton({
            text: 'Okay',
            handler: data => {
                //console.log('Checkbox data:', data);
                //console.log(table);
                if (data) {
                    let rlength = table['rows'].length;
                    for (let i = 0; i < rlength; i++) {
                        let cells = table['rows'][i].childNodes;
                        for (let j = 0; j < cells.length; j++) {
                            cells[j].hidden = true;
                        }
                        for (let k = 0; k < data.length; k++) {
                            let headerId = data[k];
                            let colHeader = document.getElementsByName(headerId);
                            let cellIndex = colHeader[0]["cellIndex"];
                            for (let i = 0; i < rlength; i++) {
                                let cells = table['rows'][i].childNodes;
                                cells[cellIndex].hidden = false;
                            }
                        }

                    }


                }
            }
        });
        alert.present();
    }
        

    takePicture(sourceType) {
        
       
        var options = {
            quality: 100,
            sourceType: sourceType,
            saveToPhotoAlbum: true,
            correctOrientation: true,
            mediaType: this.camera.MediaType.PICTURE,
            encodingType:this.camera.EncodingType.PNG,
            targetWidth : 1024,
            targetHeight : 1024,
        };
        
        
        this.camera.getPicture(options)
            .then((imagePath) => {
               
                this.newpics.push(imagePath);
                this.fileCount = this.newpics.length;
                this.uploadedFileData();
               
            
            }, (err) => {
               console.log(err);
           });                
            
    }

    choosePicture(){
        let options = {
            maximumImagesCount: 1,
            quality : 100,
            width : 1024,
            height : 1024,

        }
        
        this.imagePicker.getPictures(options).then(
        file_uris =>{
              
            this.storedpics=file_uris;
            this.fileCount = this.storedpics.length; 
            this.uploadedFileData();          
        }),
        err => console.log(err);

    }

    chooseDocs(){
        this.fileChooser.open()
        .then(uri => {
            console.log(uri);
            this.filePath.resolveNativePath(uri)
                .then(filePath => {
                    console.log(filePath);
                    this.newdocs.push(filePath);
                    this.fileCount = this.newdocs.length;
                    this.uploadedFileData();
                })
                .catch(err => console.log(err));
           
        })
        .catch(e => console.log(e));
    }


    upload(){
        let actionSheet = this.actionSheetCtrl.create({
            title: 'Select Files',
            buttons: [
            {
                text: 'Choose Photo',
                handler: () => {
                    console.log('Choose Photo clicked');
                    this.newdocs=[];
                    this.storedpics=[];
                    this.newpics=[];   
                    this.choosePicture();
                }
            },
            {
                text: 'Take Photo',
                handler: () => {
                    console.log('Take Photo clicked');
                    this.storedpics=[];
                    this.newdocs=[];
                    if (this.newpics.length < 1){
                        this.takePicture(this.camera.PictureSourceType.CAMERA);
                    }
                    if (this.newpics.length == 1){
                        let alert = this.alertCtrl.create({
                            title: 'Alert',
                            subTitle: 'Only 1 photos can be uploaded...',
                            buttons: ['Dismiss']
                        });
                        alert.present();
                    
                    }
                    
                    
                }
            },
            {
                text: 'Choose Documents',
                handler: () => {
                    console.log('Choose Documents clicked');
                    this.newpics=[];
                    this.storedpics=[];
                    if (this.newdocs.length < 1){
                        this.chooseDocs();
                    }
                    if (this.newdocs.length >= 1){
                        let alert = this.alertCtrl.create({
                            title: 'Alert',
                            subTitle: 'Only 1 documents can be uploaded.',
                            buttons: ['Dismiss']
                        });
                        alert.present();
                    
                    }
                    
                  
                }
            },
            {
                    text: 'Cancel',
                    role: 'cancel',
                    handler: () => {
                        console.log('Cancel clicked');
                    }
            }]
        });

        actionSheet.present();
        
        
    }



    mic(){
        this.speechRecognition.isRecognitionAvailable()
            .then((available: boolean) => {
                console.log(available);
                
                this.speechRecognition.requestPermission()
                    .then(
                        () => {
                            console.log('Granted');
                            let options = {
                                language: 'en-IN',
                            }
                            this.speechRecognition.startListening(options)
                            .subscribe(
                                (matches: Array<string>) =>{
                                     console.log(matches);
                                     this.speech = matches[0];
                                    },
                                (onerror) => {
                                    console.log('error:', onerror);
                                   
                                    let alert = this.alertCtrl.create({
                                        title: 'Error',
                                        subTitle: 'Try Again',
                                        buttons: ['Dismiss']
                                    });
                                    alert.present();
                                       

                                }
                            )
                        },
                        () => {
                            console.log('Denied');
                             let alert = this.alertCtrl.create({
                                title: 'Error',
                                subTitle: 'Access Denied',
                                buttons: ['Dismiss']
                            });
                            alert.present();
                        }
                    )
            })
            .catch(err => {
                console.log(err);
                 let alert = this.alertCtrl.create({
                    title: 'Error',
                    subTitle: 'Speech Recognition is not supported in your mobile',
                    buttons: ['Dismiss']
                });
                alert.present();
            });
    }

    printPreview($event){
        let mapValue = {};
        let mustacheJson = {};
        let actions = this.viewJson["action_meta"];
        for(let i =0;i<actions.length;i++){
            if(actions[i]["at"] == "PrintFormat"){
                let pfActionObj = actions[i]["printformat"]["pfc"]; //PF Action Object
                console.log(pfActionObj);

                if(pfActionObj){
                    let sqlArray = pfActionObj["sql"];  //SQL Object
                
                    for(let j =0;j<sqlArray.length;j++){
                        //Getting Params in SQL
                        var found = [],          // an array to collect the strings that are found
                            rxp = /\:(\w+)/g,
                            str = sqlArray[j].sql,
                            curMatch;
        
                        while( curMatch = rxp.exec( str ) ) {
                            found.push( curMatch[1] );
                        }
                        console.log(found);

                        //Creating JSON Object
                        if(found.length>0){
                            for(let k=0;k<found.length;k++){
                                mapValue[found[k]] = this.preset_value[found[k]]
                                
                            }

                        }
                        if(pfActionObj["at"]=="Server"){
                            this.mycmservice.printFormtSql(sqlArray[j].sql,sqlArray[j].st,mapValue).subscribe(result => {
                                console.log(result);
                                let resJson = JSON.parse(result.text());
                                if (sqlArray[j]["st"] == "Nongrid"){
                                    mustacheJson = resJson;
                                }
                                else if (sqlArray[j]["st"] == "Grid"){
                                    mustacheJson[sqlArray[j]["do"]] = resJson;
                                }

                                if(j==sqlArray.length-1){
                                    this.http.get('assets/mustache/transaction.html').map(res => res.text()).subscribe(html => {
                                        let template = html;
                                        var output = Mustache.render(template, mustacheJson);
                                        cordova.plugins.pdf.htmlToPDF({
                                            data: output,
                                            documentSize: "A4",
                                            landscape: 'portrait',
                                            type: "share"
                                        },
                                        (sucess) => console.log('sucess: ', sucess),
                                        (error) => console.log('error:', error));
            
                                    });
        
                                }

                            });
                        

                        }
                        else if(pfActionObj["at"]=="Client"){
                            let finalSql = "";
                            for (var key in mapValue) {
                                finalSql = sqlArray[j].sql.replace(":"+key,mapValue[key])

                            }
                            
                            this.sqlite.create({
                                name: 'data.db',
                                location: 'default'
                            }).then((db: SQLiteObject) => {
                    
                                db.executeSql(finalSql, []).then((data) => {
                                    console.log(JSON.stringify(data));
                                    let resJson = [];
                                    if (data.rows.length > 0) {
                                        
                                        for (var i = 0; i < data.rows.length; i++) {
                                            console.log(data.rows.item(i).name);
                                            resJson.push(data.rows.item(i));
                                        }
                                        if (sqlArray[j]["st"] == "Nongrid"){
                                            for (var key in resJson[0]) {
                                                mustacheJson[key] = resJson[0][key];
                                            }
                                            // mustacheJson = resJson;
                                        }
                                        else if (sqlArray[j]["st"] == "Grid"){
                                            mustacheJson[sqlArray[j]["do"]] = resJson;
                                        }
                                    }
                                    

                                    if(j==sqlArray.length-1){
                                        this.http.get('assets/mustache/transaction.html').map(res => res.text()).subscribe(html => {
                                            let template = html;
                                            var output = Mustache.render(template, mustacheJson);
                                            cordova.plugins.pdf.htmlToPDF({
                                                data: output,
                                                documentSize: "A4",
                                                landscape: 'portrait',
                                                type: "share"
                                            },
                                            (sucess) => console.log('sucess: ', sucess),
                                            (error) => console.log('error:', error));
                
                                        });
            
                                    }
                                }).catch(e => console.log(e));

                            }).catch(e => console.log(e));

                        }
                        
                        

                    
                    }
                   

                }
            }
        }

    }


 search($event){
	 let profileModal = this.modalCtrl.create(SearchmodalPage,{jsonUrl : this.jsonUrl,txservice :this.mytxservice,userDetails:this.UserDetails,selectoptions:this.optionsJson});
	 profileModal.present();
	  profileModal.onDidDismiss(data => {
		  console.log(data);
		  this.UserDetails = data;
	  });
	 
 }	
	
presetInputValue(dataset){
	this.http.get(this.jsonUrl).map(res => res.json()).subscribe(data => {
		let content_meta = data[0]['cont_meta'];
		let eupdate_meta = data[0]['eupdate_meta'];
		let datasetValue = JSON.parse(dataset);
		for(let j=0;j<content_meta.length;j++){
			let children = content_meta[j]['children'];
			let identifiers = content_meta[j]['idt'];
			let component = content_meta[j]['comp_meta'];
			let ctype = content_meta[j]['ctype'];
			let table_name = content_meta[j]['db'];
			let required_value = datasetValue[table_name];
			this.setValues(component,ctype,required_value,identifiers);
			if (children.length >0){
				for(let k=0;k<children.length;k++){
					let c_children = children[k]['children'];
					let c_component = children[k]['comp_meta'];
					let c_identifiers = children[k]['idt'];
					let c_ctype = children[k]['ctype'];
					let c_table_name = children[k]['db'];
					let c_required_value = datasetValue[c_table_name];
					this.setValues(c_component,c_ctype,c_required_value,c_identifiers);
				}
			
			
			}
			}
		if(eupdate_meta.length >0)
		{
			let source = eupdate_meta[0]['so_meta'];
			let eup = [];
			let eupdate ={};
			if(source[0]['ctype'] == 'card' || source[0]['ctype'] == 'list'){
				let sid = source[0]['idt'];
				eupdate[sid] = this.preset_value[sid];
				this.UserDetails['eupdate'] = eupdate;
			
			}
			else if(source[0]['ctype'] == 'grid'){
				let table = document.getElementById(source[0]['cid']+"_ET");
				let gridID = source[0]['idt']+'_'+source[0]['dbtable'];
				let table_header = table.getElementsByTagName('thead')[0]['children'][0]['children'];
				let cellIndex = table_header[gridID]['cellIndex'];
				let tbody = table.getElementsByTagName('tbody');
				let children = tbody[0]['children'];
				for(let i=0;i<children.length;i++){
					let obj = {};
					obj['old_value'] = children[i]['cells'][2]['dataset']['select_value'];
					obj['rowid'] = children[i]['id'];
					eup.push(obj);
				}
			   this.UserDetails['eupdate'] = eup;
			   
			}
			
		
		}
		
		console.log(dataset);
        });
}

setValues(comp,ctype,dataset,idt){
	
	if(ctype == 'card'|| ctype == 'list'){
		for (let i=0;i<comp.length;i++){
			let id = comp[i]['idt'];
			let cjson = JSON.parse(comp[i]['cjson']);
			let wiget = comp[i]['wt'];
			if(cjson['isdbfield'] == true){
				if(wiget == 'check'){
					let value = dataset[0][id].split(',');
					let enums = cjson['enum_meta'];
					if(value.length >0){
					for(let i=0;i<value.length;i++){
					const filter = enums.filter((item) => {
							 return (item['value'] == value[i]);
					});
						if(filter.length >0){
							let check_id = id+"_"+filter[0]['key'];
							this.preset_value[check_id] = true;
						  
						}
					}
					}
				}
				else{
					if(dataset[0][id] != ""){
						this.preset_value[id] = dataset[0][id];
					}
				}
				
			}
		}
	
	}
	else if(ctype == "grid"){
		let table = document.getElementById(idt+"_ET");
		let headerColumn = table.getElementsByTagName('th');
		let tbody = table.getElementsByTagName('tbody');
		let rowlength = tbody[0].rows.length;
		let tableid = table.id;
		for (let k=0;k<dataset.length;k++){
			let rowValue = dataset[k];
			let newRow = tbody[0].insertRow(tbody[0].rows.length);
			newRow.id = tableid + rowlength;
			let cellength = table["rows"][0].cells.length;
			newRow["dataset"]['fromdb'] = "True";
			newRow.addEventListener("click", event => {
			newRow.style.background = "lightgrey";
			this.selectedRow = newRow.id;
                });
			for (let i = 0; i < cellength; i++) {
				console.log(comp);
				let fieldValue = "";
				let newCell = newRow.insertCell(i);
				let elementid = headerColumn[i]['dataset']['elementid'];
				
				const comp_obj = comp.filter((item) => {
							 return (item['idt'] == elementid);
					});
				console.log(comp_obj);
				let cjson:any;
				if(comp_obj.length >0){
					if(comp_obj[0]['cjson'] != ""){
					cjson = JSON.parse(comp_obj[0]['cjson']);
					newCell["dataset"]['type'] = comp_obj[0]['wt'];	
				}
				}
				newCell["dataset"]['header_id'] = elementid;
				if(headerColumn[i]['dataset']['type'] == 'time'){
				
				
					fieldValue = convertTime24to12(rowValue[elementid]);
					newCell['dataset']['select_value'] =  rowValue[elementid];
				}
				 
				else if(headerColumn[i]['dataset']['type'] == 'date'){
					if(rowValue[elementid] == null){
					     fieldValue ="";
					}
					else{
					newCell['dataset']['select_value'] =  rowValue[elementid];
					var date = new Date(rowValue[elementid]);
					fieldValue = date.toLocaleDateString();
					}
				}
				else if(headerColumn[i]['dataset']['type'] == 'select' || headerColumn[i]['dataset']['type'] == 'radio' )
				{
					let select_key ="";
					console.log(this.optionsJson);
					if(cjson['enum_meta'].length>0)
					{
					const filter_obj = cjson['enum_meta'].filter((item) => {
							 return (item['value'] == rowValue[elementid]);
					});	
						select_key = filter_obj[0]['key'];
					}
					else if(comp_obj[0]['sql'] != "" ||comp_obj[0]['sql'] != null){
						let sql = JSON.parse(comp_obj[0]['sql']);
						let tb_id = cjson['txtabledetailid'];
						let key = sql['key'];
						let values = sql['value'];
						let options = this.optionsJson[elementid+"_"+tb_id];
						const filter = options.filter((item) => {
							 return (item[values] == rowValue[elementid]);
						});
						if(filter.length>0){
							select_key = filter[0][key];
						}
					
					}
					fieldValue =  select_key;
					newCell['dataset']['select_value'] = rowValue[elementid];
                     
				}
				else if(headerColumn[i]['dataset']['type'] == 'check')
				{
					let check_value = rowValue[elementid].split(',');
					let Check_key = [];
					let Check_value =[];
					let Check_carry =[];
					
					if(cjson['enum_meta'].length>0){
						for(let ck=0;ck <check_value.length ;ck++){
							let obj = {};
						const filter_obj = cjson['enum_meta'].filter((item) => {
							 return (item['value'] == check_value[ck]);
						});
						 if(filter_obj.length>0){
							 let key = filter_obj[0].key;
							 let value = filter_obj[0].value;
							 Check_key.push(key);
							 Check_value.push(value);
							 obj['id'] = elementid+"_"+key;
							 obj['checked'] = true;
							 obj['value'] = value;
							 Check_carry.push(obj);
						 }
						}
						fieldValue =  Check_key.toString();
						newCell['dataset']['select_value'] = rowValue[elementid];
						newCell['dataset']['carray'] = JSON.stringify(Check_carry);
					
					}
				}
				else
				{   
					if(rowValue[elementid] == null){
						fieldValue = "";
					}
					else{
						fieldValue =  rowValue[elementid];
						}
					newCell['dataset']['select_value'] = fieldValue;
				}
				let newText = document.createTextNode(fieldValue);
				newCell.appendChild(newText);
				if (headerColumn[i].hidden == true) {
					newRow.cells[i].hidden = true;
				}
			
				}
	}
	}
}
		buttonClick(event){
			console.log(event);
			let expression = event['currentTarget']['dataset']['expression'];
			let actiontype = expression.split('(');
			if(actiontype[0] == "txnbuttonaction"){
			  let values = actiontype[1].replace(/["'({})]/g,"");
			  let  split_value = values.split(',');
			  let method = split_value[0];
				if(method == 'eupdate'){
					let pageid = split_value[1].toLowerCase();
					let storeValue = split_value[2].split(':')
					let inputId = storeValue[0];
					let storeId = storeValue[1];
					let inputValue = this.preset_value[inputId];
					if(inputValue != undefined){
					const pages = this.pagenav.pages.filter((item) => {
						return (item['id'] == pageid);
					});
					
					this.UserDetails[storeId] = inputValue;
					if(pages.length >0){
					this.navCtrl.setRoot(pages[0]['component'], {
						userdetails : this.UserDetails,
					});
					}
					 this.sqlite.create({
						name: 'data.db',
						location: 'default'
					}).then((db: SQLiteObject) => {
						    db.executeSql('INSERT INTO control VALUES (?,?,?)', [45,storeId,inputValue])
								  .then(() => {
								  console.log('Sync');  
								 this.datapresent(db);
								  })
								  .catch(e => console.log(e));
					 
					 });
					}
					else{
						let toast = this.toastCtrl.create({
							message: 'Please Select Value From List',
							duration: 3000,
							position: 'top'
						  });

						  toast.onDidDismiss(() => {
							console.log('Dismissed toast');
						  });

						  toast.present();
					
					}
				
				}
			}
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
	
	logout(){
		const pages = this.pagenav.pages.filter((item) => {
						return (item['id'] == 'login');
					});
		if(pages.length >0){
					this.navCtrl.setRoot(pages[0]['component']);
		
	}
	}
 
}


