import { Component } from '@angular/core';
import { NavController, NavParams, Platform } from 'ionic-angular';
import { ViewController } from 'ionic-angular';
import { Http } from '@angular/http';
import { AlertController } from 'ionic-angular';
import { TxserviceProvider } from '../../providers/txservice/txservice';
import { Storage } from '@ionic/storage';
import { Network } from '@ionic-native/network';
import { BarcodeScanner } from '@ionic-native/barcode-scanner';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { ExpressionProvider } from '../../providers/expression/expression';
import { ToastController } from 'ionic-angular';
import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
import { SpeechRecognition } from '@ionic-native/speech-recognition';
declare var setEformVarMap : any;
declare var setGetFieldval : any;

/**
 * Generated class for the ModalPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-modal',
  templateUrl: 'modal.html',
  providers:[TxserviceProvider,ExpressionProvider]
})
export class ModalPage {
	elementmodelList: any[] = [];
	username: any;
	networkStatus: any;
	UserDetails: any;
	public stValues: any;
	pid: any;
	userid: any;
	projectname: any;
	requiredValue: any;
	elementList: any[] = [];
	selectoptionsJson: Object =  {}; 
	optionsJson: Object =  {}; 
	sqlSelectFieldValue: Object =  {};
	database:any;
	selectedOptions: Object =  {};
	already_selectedOptions: Object =  {};
	speech: any;
	preset_value: Object =  {};


  constructor(public navCtrl: NavController, public navParams: NavParams,public platform: Platform,public viewCtrl: ViewController,public http: Http,public storage: Storage,private network: Network, public singleton: SingletonProvider, public myexpression: ExpressionProvider,private barcodeScanner: BarcodeScanner,
    private alertCtrl: AlertController,public mytxservice: TxserviceProvider,private sqlite: SQLite,private speechRecognition: SpeechRecognition) {
	//console.log('UserId', navParams.get('rowValues'));
	 this.projectname = this.singleton.projectname;
        this.UserDetails = this.navParams.get("userdetails");
        this.selectoptionsJson = this.navParams.get("options");
        if (this.UserDetails == undefined) {
            this.storage.get('userObj').then((loginInfo) => {
                //console.log(loginInfo);
                this.UserDetails = loginInfo;
				this.UserDetails['pagetype'] = 'txview';//for differentiate transaction or report in expr.js
            });
        }
		else{
		    this.UserDetails['pagetype'] = 'txview';//for differentiate transaction or report in expr.js
		}
 }

 ionViewDidLoad() {
        console.log('ionViewDidLoad ModalPage');       


        this.UserDetails = this.navParams.get("userdetails");
        let initalHiddenComponents: any[] = [];
         let elements = document.getElementById('modelForm').querySelectorAll('*[name]');
		 //console.log(elements);
		 for (let i = 0; i < elements.length; i++) {
			 if (elements[i].id != "" && elements[i].tagName != "ION-CHECKBOX") {
				 this.elementmodelList.push(elements[i].id);
				 if(this.selectoptionsJson){
					 if (elements[i]['dataset']['widgettype'] == "select" || elements[i]['dataset']['widgettype'] == "radio" || elements[i]['dataset']['widgettype'] == "check"){
						 let dataset = elements[i]['dataset'];
						 if(dataset['sql'] != null || dataset['sql'] !=""){
							 let id = dataset['id'];
							 let referson = JSON.parse(dataset['referjson']);
							 let tb_id = referson['txtabledetailid'];
							 if(this.selectoptionsJson[id+"_"+tb_id] !=undefined){
								 this.optionsJson[id] = this.selectoptionsJson[id+"_"+tb_id];
							 }
					
					}
				
				}
				
			
			}
			 }
		 }

        for (let i of this.elementmodelList) {
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
        let wholeform = document.getElementsByName('myForm')[0];
        let eformid = wholeform.dataset["eformid"];
        form = document.getElementsByName('myForm')[0].children[0];
        
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

     let rowValues = this.navParams.get('rowValues');
     if (rowValues) {
         for (let i = 0; i < this.elementmodelList.length; i++) {
             let id = this.elementmodelList[i];
             let DOM = document.getElementsByName(id);
			 if(DOM[0]["previousElementSibling"]){
			 let floating = DOM[0]['previousElementSibling']['attributes']['floating'];
			 if(floating){
				 document.getElementsByName(id+"item")[0]['className'] = "item item-block item-md item-input item-label-floating input-has -focus item-input-has-focus";
			 }
			 }
             let DOMbyId = document.getElementById(id);
             let tagName = DOM[0].tagName;
             //console.log(tagName);
             if (tagName == 'ION-SELECT' || DOMbyId.getAttribute('role') == "radiogroup") {
                 //DOM[0].firstElementChild.firstChild.textContent = rowValues[i].textContent;
				 this.preset_value[id] = rowValues[i]["dataset"]["select_value"];
				 this.already_selectedOptions[id] = rowValues[i]["dataset"]["select_value"];
                 //items.push(fieldValue);  	
             } else if (tagName == 'ION-INPUT') {
                 //DOMbyId.getElementsByTagName("input")[0].value = rowValues[i].textContent;
				 this.preset_value[id] = rowValues[i].textContent;
             } else if (tagName == 'ION-TEXTAREA') {
                 //DOMbyId.getElementsByTagName("textarea")[0].value = rowValues[i].textContent;
				 this.preset_value[id] = rowValues[i].textContent;
             }  else if (tagName == 'ION-DATETIME') {
				 if(DOM[0]['dataset']['format'] == 'date'){					 
				 let preset_date = rowValues[i].textContent;
				 if(preset_date !=""){
				 var newdate = rowValues[i]["dataset"]["select_value"];
                 this.preset_value[id] = new Date(Date.parse(newdate)).toISOString();
				 }
				 }
				 else{
					 let preset_time = rowValues[i]["dataset"]["select_value"];
					 if(preset_time !=""){
						 this.preset_value[id] = preset_time;
					 }
				 }
				
             } else if (DOMbyId.getAttribute('role') == "checkgroup"){
				 let select_value = rowValues[i]["dataset"]['select_value'];
				 let header_id = rowValues[i]["dataset"]['header_id'];
				 if(select_value != ""){
					 let myarray = select_value.split(',');
					 let json = JSON.parse(rowValues[i]["dataset"]['carray']);
					 for(let i=0;i<myarray.length;i++){
						 const filter = json.filter((item) => {
							 return (item['value'] == myarray[i]);
						 });
						 console.log(filter);
						 if(filter.length>0){
							 let cid = filter[0]['id'];
							 this.preset_value[cid] = filter[0]['checked'];
						 }
					 }
					 this.already_selectedOptions[header_id+"_Cvalue"] = rowValues[i]["dataset"]["select_value"];
					 this.already_selectedOptions[header_id+"_Cbox"] = json;
				 }
				 else{
					 this.already_selectedOptions[header_id+"_Cvalue"] = rowValues[i]["dataset"]["select_value"];
					 this.already_selectedOptions[header_id+"_Cbox"] = rowValues[i]["dataset"]['carray'];
				 }
         }
         //console.log(this.elementmodelList);	 
     }
 }
 }

    onFocus(event) {
        let formEvent;
        let form;
        let id = event._elementRef.nativeElement.dataset["id"];
        let sqlValue = event._elementRef.nativeElement.dataset["sqlvalue"];
        let wholeform = document.getElementsByName('myForm')[0];
        let eformid = wholeform.dataset["eformid"];
        form = document.getElementsByName('myForm')[0].children[0];
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
        //console.log(event);
        let formEvent;
        let form;
        let id = event._elementRef.nativeElement.dataset["id"];
        form = document.getElementsByName('myForm')[0].children[0];
	    try{
		   formEvent =JSON.parse(form.dataset['event']);
			 if (formEvent != "") {
				 try {
            if (formEvent.onexit[id]) {
                for (let i = 0; i < formEvent.onexit[id].length; i++) {
                    let elementEvent = formEvent.onexit[id][i];
                    this.myexpression.evaluateEventexp(elementEvent, this.UserDetails,"");
                }
            }
				 }
				  catch(e){
				  }
        }
		 }
		 catch(e){
			formEvent = "";
		 }
       
        let indexValue = this.elementmodelList.indexOf(id);
        //console.log(indexValue);
        //console.log(this.elementmodelList[indexValue + 1]);
        for (let i = indexValue + 1; i < this.elementmodelList.length; i++) {
            //console.log(document.getElementsByName(this.elementmodelList[i]));
            let nextElement = document.getElementsByName(this.elementmodelList[i]);
            let readonly = nextElement[0].dataset['readonly'];
            if (readonly == "True") {
                this.myexpression.evaluateExp("", nextElement, this.UserDetails,this.preset_value);
            } else if (readonly == "False") {
                break;
            }
        }
        //console.log("focusOut");


    }


 checkSelect(event, id) {
     //console.log(event);
     let combObj = document.getElementsByName(id)[0].children;
     for (let j = 1; j < combObj.length; j++) {
         combObj[j].firstChild["lastElementChild"].firstChild.className = "radio-icon";
     }
     //console.log(id);
     //console.log("Select");
 }

    checkChange($event, elemtId) {
		if($event != undefined){
        let nextHiddenComponents: any[] = [];
        let formEvent;
        let form;
        let id = elemtId;
        let ctEform;
        let eformVarMap = {};
        let selectedOptionValues = {}
        let elementIdList = []
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

        //********************************/
        //Checking Elements for hidden and expression
        
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
    }
getSqlDataForSelectField(event) {
}
 dismiss() {
     this.viewCtrl.dismiss();
 }

 submit() {
     let items = [];
	 let item_choosed ={};
     //console.log(this.elementmodelList);
     for (let i = 0; i < this.elementmodelList.length; i++) {
         let id = this.elementmodelList[i];
         let DOM = document.getElementsByName(id);
		 let DOMbyId = document.getElementById(id);
         let tagName = DOM[0].tagName;
		 let fieldValue ="";
         //console.log(tagName);
         if (tagName == 'ION-SELECT') {
             let select_value =  this.selectedOptions[id];
			 let value ={};
			 let value_list =[];
			 if(select_value == undefined){
				 
				 if(this.already_selectedOptions[id]!=undefined){
					 fieldValue = this.already_selectedOptions[id];
					 value[this.already_selectedOptions[id]] =  DOM[0].textContent;
					 value_list.push(value);
					 item_choosed[id] = value_list;				 
				 }
				 else{
					 fieldValue = "";
				 }
			 }
			 else{
				 fieldValue = this.selectedOptions[id];
				 value[this.selectedOptions[id]] =  DOM[0].textContent;
				 value_list.push(value);
				 item_choosed[id] = value_list;
			 }
             //items.push(fieldValue);  	
         } else if (DOMbyId.getAttribute('role') == "radiogroup") {
             //fieldValue = document.getElementById(id).getAttribute("ng-reflect-model");
			 let select_value =  this.selectedOptions[id];
			 let value ={};
			 let value_list =[];
			 let referjson = document.getElementsByName(id)[0]['dataset']['referjson'];
			 let cjson  = JSON.parse(referjson);
			 if(select_value == undefined){
				 if(this.already_selectedOptions[id]!=undefined){
					 fieldValue = this.already_selectedOptions[id];
					 const filter = cjson['enum_meta'].filter((item) => {
							 return (item['value'] == fieldValue);
						 });
					 if(filter.length>0){
					 value[this.already_selectedOptions[id]] =  filter[0]['key'];
					 }	 
					 value_list.push(value);
					 item_choosed[id] = value_list;	
				 }
				 else{
				 fieldValue ="";
				 }
			 }
			 else{
				 fieldValue = this.selectedOptions[id];
				 const filter = cjson['enum_meta'].filter((item) => {
							 return (item['value'] == fieldValue);
						 });
					 if(filter.length>0){
						 value[this.selectedOptions[id]] =  filter[0]['key'];
					 }
				 value_list.push(value);
				 item_choosed[id] = value_list;
			 }
         } else if (tagName == 'ION-INPUT') {
             fieldValue = document.getElementById(id).getElementsByTagName("input")[0].value;
			 item_choosed[id] = document.getElementById(id).getElementsByTagName("input")[0].value;
         }else if (tagName == 'ION-TEXTAREA') {
             fieldValue = document.getElementById(id).getElementsByTagName("textarea")[0].value;
			 item_choosed[id] = this.preset_value[id];
         }else if (tagName == 'ION-DATETIME') {
			    if(this.preset_value[id] != undefined){
			     var date = new Date(this.preset_value[id]);
				 fieldValue = date.toLocaleDateString();
				 item_choosed[id] = this.preset_value[id];
				}else{
					fieldValue = "";
					item_choosed[id] ="";
				}
			 
         } else if(DOMbyId.getAttribute('role') == "checkgroup"){
			 let check_value ="";
			 let multiList = [];
			 let fieldList =[];
			 let valueList =[];
			 let item_chooseid = id+"_Cbox";
			 let item_choosevalue = id+"_Cvalue";
			 if(this.selectedOptions[id] != undefined){
				 let checkList = DOMbyId.getElementsByTagName('ion-checkbox');
				 for(let j=0;j< checkList.length;j++){
					 let checkListId = checkList[j].attributes['id'].value;
					  const filter = this.selectedOptions[id].filter((item) => {
							 return (item['id'] == checkListId);
						 });
					 let checked = document.getElementById(checkListId).getElementsByTagName('button')[0].attributes["aria-checked"].value;
					 if(checked == "true" && checkList.length == 1){
						 fieldValue = document.getElementById(checkListId).getAttribute("data-key");
						 if(filter.length == 0){
							 if(this.already_selectedOptions[item_choosevalue] != ""){
								 const ald_filter = this.already_selectedOptions[item_chooseid].filter((item) => {
									 return (item['id'] == checkListId);
								 });
								 fieldList.push(ald_filter[0]);
							 }
						 }
						 else{
							 fieldList.push(filter[0]);
						 }
						 check_value = checkList[j]['dataset']['value']
					 
				 }
				 else if(checked =="true" && checkList.length >1){
					multiList.push(document.getElementById(checkListId).getAttribute("data-key"));
					valueList.push(checkList[j]['dataset']['value']);
					fieldValue = multiList.toString();
					check_value = valueList.toString();
					if(filter.length == 0){
							 if(this.already_selectedOptions[item_choosevalue] != ""){
								 const ald_filter = this.already_selectedOptions[item_chooseid].filter((item) => {
									 return (item['id'] == checkListId);
								 });
								 fieldList.push(ald_filter[0]);
							 }
						 }
						 else{
							 fieldList.push(filter[0]);
						 } 
				}	
			}
				 item_choosed[item_chooseid] = fieldList;
				 item_choosed[item_choosevalue] = check_value;
				 
			 }
			 else{
				 if(this.already_selectedOptions[item_choosevalue] != "" && this.already_selectedOptions[item_choosevalue] != undefined){
					 for(let n=0;n<this.already_selectedOptions[item_chooseid].length;n++){
						 let checkList = this.already_selectedOptions[item_chooseid][n];
						 if(checkList['checked'] == true && this.already_selectedOptions[item_chooseid].length == 1){
							 fieldValue = document.getElementById(checkList['id']).getAttribute("data-key");
							 fieldList.push(checkList);
							 check_value = checkList['value'];
						 }
						 else if(checkList['checked'] == true && this.already_selectedOptions[item_chooseid].length >1){
							 multiList.push(document.getElementById(checkList['id']).getAttribute("data-key"));
							 valueList.push(checkList['value']);
							 fieldValue = multiList.toString();
							 check_value = valueList.toString();
							 fieldList.push(checkList); 
					 }
				 }
				 }
				 else{
				 fieldValue ="";
				 }
				 item_choosed[item_chooseid] = fieldList;
				 item_choosed[item_choosevalue] = check_value;
			 }
			//let checkList = DOMbyId.getElementsByTagName('ion-checkbox');
			//for(let i=0;i<checkList.length;i++){
			//let checkListId = checkList[i].attributes['id'].value;
			//let checked = document.getElementById(checkListId).getElementsByTagName('button')[0].attributes["aria-checked"].value;
			//if(checked == "true" && checkList.length == 1){
				//fieldValue = document.getElementById(checkListId).getAttribute("data-value");	
			//}
			//else if(checked =="true" && checkList.length >1){
			//multiList.push(document.getElementById(checkListId).getAttribute("data-value"));
			//fieldValue = multiList.toString();	
			//}	
		 //}
		 }
         items.push(fieldValue);
		 
     }
     let data = {
         items,
         item_choosed
     };
     //console.log(data);
     this.viewCtrl.dismiss(data);
	 }

    scan(event,id){
        this.barcodeScanner.scan({showTorchButton : true}).then((barcodeData) => {
        //console.log(barcodeData);
            //console.log(event);
            //console.log(id);
            if (barcodeData['cancelled'] == false){
            document.getElementById(id).getElementsByTagName("input")[0].value  = barcodeData['text'];
            }else if(barcodeData['cancelled'] == true){
            let alert = this.alertCtrl.create({
                            title: 'Alert',
                            subTitle:  'User Cancelled Operation.',
                            buttons: ['Dismiss']
                        });
                        alert.present();	
            }
            
        }, (err) => {
            // An error occurred
        });

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
}
