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
import { ModalController } from 'ionic-angular';

import { TxserviceProvider } from '../../providers/txservice/txservice';
import { ExpressionProvider } from '../../providers/expression/expression';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { NotifyProvider } from '../../providers/notify/notify';

import { LoginPage } from '../../pages/login/login';
import { HomePage } from '../home/home';

declare var setEformVarMap : any;
declare var setGetFieldval : any;
//declare var validate:any;
/**
 * Generated class for the TransactionPage page.
 *
 * See http://ionicframework.com/docs/components/#navigation for more info
 * on Ionic pages and navigation.
 */
@Component({
  selector: 'page-registration',
  templateUrl: 'registration.html',
	providers:[TxserviceProvider,ExpressionProvider],
})
export class RegistrationPage {
   
    //cucumber:any; 
    username: any;
    networkStatus: any;
    UserDetails: any;
    public stValues: any;
    pid: any;
    userid: any;
    projectname: any;
    requiredValue: any;
    optionsJson: Object =  {}; 
    sqlSelectFieldValue: Object =  {};
	preset_value: Object =  {};
    elementList: any[] = [];
    selectedOptions: Object =  {};
    selectedRow: any;
    database:any;
    newpics:any[]=[];
    storedpics:any[]=[];
    newdocs:any[]=[];
    private fileCount = 0;
    //blobArray:any[]=[];
    base64Str:any;
    speech: any;
    loginPage: Array<{title: string, component: any}>;

    constructor(public navCtrl: NavController, public navParams: NavParams,public viewCtrl: ViewController, public modalCtrl: ModalController, private network: Network, private sqlite: SQLite, public storage: Storage, public singleton: SingletonProvider, public myexpression: ExpressionProvider, public mytxservice: TxserviceProvider, public http: Http, private alertCtrl: AlertController, 
        private toastCtrl: ToastController,private barcodeScanner: BarcodeScanner,private camera: Camera, private imagePicker: ImagePicker,private actionSheetCtrl: ActionSheetController,private base64: Base64,
            private fileChooser: FileChooser,private filePath: FilePath,
            public loadingCtrl: LoadingController,private speechRecognition: SpeechRecognition,public notifyProvider :NotifyProvider) {
        this.projectname = this.singleton.projectname;
        this.UserDetails = {
            "EMAIL" : "",
            "MOBILENUMBER" : "",
            "ROLE" : "",
            "USERID" : "",
            "USERNAME" : "",
            "pagetype" : "txview"
        }
        this.loginPage = [
            { title: 'login', component: LoginPage}
        ];
    
 
    }

    ionViewDidLoad() {
        let eformid = "";
        let selectFields = document.getElementsByTagName("ion-select");
        if (selectFields != null){
            this.getOptions(selectFields);
        }
        
        let radioFields = document.getElementsByClassName("radio-group");
        if (radioFields != null){
            this.getOptions(radioFields);
        }

        let checkBoxFields = document.getElementsByClassName("checkbox-group");
        if (checkBoxFields != null){
            this.getOptions(checkBoxFields);
        }
        let inputFields = document.getElementsByTagName("ion-input");
        if (inputFields != null){
            this.getOptions(inputFields);
        }

        //ion-textarea
        //ion-datetime
        
        
        this.UserDetails = this.navParams.get("userdetails");
        console.log('ionViewDidLoad TransactionPage');
        let initalHiddenComponents: any[] = [];
        let elements = document.getElementById('signupForm').querySelectorAll('*[name]');

        for (let i = 0; i < elements.length; i++) {
            if (elements[i].id != "" && elements[i].tagName != "ION-CHECKBOX") {
                this.elementList.push(elements[i].id);
            }
        }

        //Checking Elements for hidden and expression
        for (let i of this.elementList) {
            if (document.getElementById(i).dataset.hidden == "True") {
                initalHiddenComponents.push(i);
            } else if (document.getElementById(i).dataset.readonly == "True") {
                let nextElement = document.getElementsByName(i);
                this.myexpression.evaluateExp("", nextElement, this.UserDetails,this.preset_value);
            } else {
                break;
            }
        }

        let formEvent;
        let form;
        //event for Container
        let wholeform = document.getElementsByName('signupForm')[0];
        try{
            eformid = wholeform.dataset["eformid"];
        }
        catch(e){
            eformid = "";
        }
        form = document.getElementsByName('signupForm')[0].children[0];
        
        try{
           formEvent =JSON.parse(form.dataset['event']); 
        }
        catch(e){
            formEvent = "";
        }
        if (formEvent != "") {
            try {
                if (formEvent.onformload.COMPEVENT) {
                    for (let i = 0; i < formEvent.onformload.COMPEVENT.length; i++) {
                        let elementEvent = formEvent.onformload.COMPEVENT[i];
                        this.myexpression.evaluateEventexp(elementEvent, this.UserDetails, eformid);
                    }
                }
            } catch (e) {
                //console.log(e);
            }

        }
        //call hidden function if there is hidden fields 
        if ((initalHiddenComponents.length) != 0) {
            this.myexpression.hiddenElementexp(initalHiddenComponents, this.UserDetails,this.preset_value,this.selectedOptions,"transaction",this,false);
        }
    }

    getOptions(fields){
        for (let i=0;i<fields.length;i++){
            
            let currentField = fields[i];
            //console.log(currentField);
            let sql = currentField['dataset']['sql'];
            let sqlDbType = currentField['dataset']['sqldbtype'];
            
            if (sqlDbType == "server"){
            
                //Assiging values 
                let data  = {
                    fieldType : "combofield",
                    eFormId : currentField['dataset']['eformid'],
                    fieldName : currentField['dataset']['fieldname'],
                    projectId : currentField['dataset']['projectid'],
                    //username : this.UserDetails["first_name"], //this.username.USERNAME
                    pid: this.singleton.PID
                
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
                    this.optionsJson[currentField.id] = this.sqlSelectFieldValue;
                   
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
                            this.optionsJson[currentField.id] = optionArray;                           
                        })
                        .catch(e => console.log(e));                    
                })
                .catch(e => console.log(e));
            }

        }
    }

    new() {
        this.navCtrl.push(this.navCtrl.getActive().component).then(() => {
            let index = this.viewCtrl.index;
            this.navCtrl.remove(index);
        });
    }

    save($event) {
        let saveStatus;
      
        let url = 'assets/json/registration.json';

		const loading = this.loadingCtrl.create({
			spinner: 'bubbles',
			content: 'Saving! Please Wait...'
		});
		loading.present();
        this.mytxservice.saveJson(this.UserDetails,url,"reg",this.base64Str,this.selectedOptions,loading,this.loginPage,this.preset_value,"","");
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
        let eformid= "";
        let id = event._elementRef.nativeElement.dataset["id"];
        let sqlValue = event._elementRef.nativeElement.dataset["sqlvalue"];
        let wholeform = document.getElementsByName('signupForm')[0];
        try{
            eformid = wholeform.dataset["eformid"];
        }
        catch(e){
            eformid = "";
        }
        form = document.getElementsByName('signupForm')[0].children[0];
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
                //console.log(e);
            }

        }
        let elelmentId = event._elementRef.nativeElement.dataset["id"];
        let DOM = document.getElementsByName(elelmentId);
		 try {
        this.myexpression.evaluateExp(event, DOM, this.UserDetails,this.preset_value);
		 }
		catch(e){
		}
    }

    checkBlur(event) {
        let formEvent;
        let form;
        let eformid = "";
        let id = event._elementRef.nativeElement.dataset["id"];
        let wholeform = document.getElementsByName('signupForm')[0];
        
        try{
            eformid = wholeform.dataset["eformid"];
        }
        catch(e){
            eformid = "";
        }

        form = document.getElementsByName('signupForm')[0].children[0];
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
        let indexValue = this.elementList.indexOf(id);

        for (let i = indexValue + 1; i < this.elementList.length; i++) {
            let nextElement = document.getElementsByName(this.elementList[i]);
            if(nextElement){
                let readonly = nextElement[0].dataset['readonly'];
                if (readonly == "True") {
                    this.myexpression.evaluateExp("", nextElement, this.UserDetails,this.preset_value);
                } else if (readonly == "False") {
                    break;
                }

            }
            
        }
    }

    checkChange($event, elemtId) {
        let nextHiddenComponents: any[] = [];
        let formEvent;
        let form;
        let id = elemtId;
        let ctEform;
        let eformVarMap = {};
        let selectedOptionValues = {}
        let elementIdList = []
        let eformid = "";
        this.selectedOptions[elemtId] = $event;
        
        //*******************************************//
        //Do this under condition
        var cjsonStr = document.getElementById(id).dataset.referjson
        var cjson = JSON.parse(cjsonStr);
        if (cjson.datatype == "OneToOneField"){

            var logicalFieldValues = this.optionsJson[elemtId]
            for(var values of logicalFieldValues)
            {
                let singleObj = {}
                singleObj = values;
                for(var key in singleObj){
                    if(singleObj[key] == $event){
                        console.log($event) 
                        selectedOptionValues = singleObj
                    }

                }

            }
            for(var key in selectedOptionValues){

                let logicalFieldID = "logical_"+elemtId+"_"+key;
                (<HTMLInputElement>document.getElementById(logicalFieldID)).value = selectedOptionValues[key];
                (<HTMLInputElement>document.getElementsByName(logicalFieldID)[1]).value = selectedOptionValues[key];
            

            }

        }
       

        
        //************************************************************** */

		let radio_group = document.getElementsByName(id)[0]['attributes']['radio-group'];
		if (radio_group){
        let combObj = document.getElementsByName(id)[0].children;
        for (let j = 1; j < combObj.length; j++) {
            combObj[j].firstChild["lastElementChild"].firstChild.className = "radio-icon";
        }
		}
        let wholeform = document.getElementsByName('signupForm')[0];
        try{
            eformid = wholeform.dataset["eformid"];
        }
        catch(e){
            eformid = "";
        }
        form = document.getElementsByName('signupForm')[0].children[0];
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

        //********************************/
        //Checking Elements for hidden and expression
        
        let elements = document.getElementById('signupForm').querySelectorAll('*[name]');
        
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
            if (document.getElementById(i).dataset.hidden == "True") {
                nextHiddenComponents.push(i);
            }
            else{
                break;
            }
        }

        if ((nextHiddenComponents.length) != 0) {
            this.myexpression.hiddenElementexp(nextHiddenComponents, this.UserDetails,this.preset_value,this.selectedOptions,"transaction",this,false);
        }
        //********************************* */
    }

    checkClick(event) {
        //console.log(event);
        //console.log("Button");

    }

    logout() {
        //this.navCtrl.setRoot(HomePage);
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

    login(){
        this.navCtrl.setRoot(LoginPage);
    }

    
	
 
}


