import { Injectable} from '@angular/core';
import { Http,Headers } from '@angular/http';
import { AlertController } from 'ionic-angular';
import { Network } from '@ionic-native/network';
import 'rxjs/add/operator/map';

import { SingletonProvider } from '../../providers/singleton/singleton';
import { Storage } from '@ionic/storage';
declare var Expression:any;
/*
  Generated class for the CmserviceProvider provider.

  See https://angular.io/docs/ts/latest/guide/dependency-injection.html
  for more info on providers and Angular DI.
*/
@Injectable()
export class CmserviceProvider {
 	subtitles:any;
	lastname:any;
	firstname:any;
	projectname:any;
	pid:any;
	reportid:any;
	show_grand_total:any;
	groupfield:any;
	columnproperty:any;
	pageHeaderFooter : any;
	reportHeaderFooter : any;
    enter:any;
    pdfinput:any[] =[];
	inputValue:string;
    username:any;
    userid:any;
    userDetails:any;


	constructor(public http: Http,public singleton: SingletonProvider,private network: Network,public storage: Storage,private alertCtrl: AlertController) {
		console.log('Hello Cmservice Provider');		
		
		this.projectname = this.singleton.projectname;
		this.pid = this.singleton.PID;
		this.http.get('assets/json/report.json').map(res => res.json()).subscribe(data => {
			this.subtitles = data;
		});
		this.storage.get('userObj').then((loginInfo) => {
            if (loginInfo){
			//let loginDetails = JSON.parse(loginInfo);
            this.username = loginInfo["USERNAME"];
            this.userid = loginInfo["USERID"];
            this.userDetails = loginInfo;			
            //console.log(loginInfo);
			}
        })
	}

sendReportParams(inputValue,projectname,reportid,multiselectvalues,groupfield,columnproperty,stl,multitenant){
	
    let params = {	           	                 	   
			"projectname": projectname,
		   	"reportid":reportid,
		   	"multiselectvalues":multiselectvalues,		   	
			"groupfield":groupfield,
			"columnproperty":columnproperty,
			"stl":stl,
			"multitenant":multitenant,		
		}
		var Keys = Object.keys(inputValue);	
	        for(var j = 0; j < Keys.length; ++j) {
				if (inputValue.hasOwnProperty(Keys[j])) 
				{
					console.log(Keys[j], inputValue[Keys[j]]);
					params [Keys[j]]=inputValue[Keys[j]]
				}
		 }
	   	console.log(params);
	   	this.pdfinput.push(params);
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let report = "PID="+this.pid+"&params="+JSON.stringify(params);		
		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/getReportData/', report , {headers: headers});

	}
sendReportwithoutParams(projectname,reportid,multiselectvalues,groupfield,columnproperty,stl,multitenant){
	let params = {	           	                 	   
			"projectname": projectname,
		   	"reportid":reportid,
		   	"multiselectvalues":multiselectvalues,		   	
			"groupfield":groupfield,		
			"columnproperty":columnproperty,
			"stl":stl,
			"multitenant":multitenant,
		}
		console.log(params);
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let report = "PID="+this.pid+"&params="+JSON.stringify(params);		
		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/getReportData/', report , {headers: headers});

	}
 
  sendpdfParams(title,stl,username,reportHeaderFooter,columnhid,multitenant){
  let pdf=this.pdfinput[0]
  console.log(pdf);
	 	let pdfParams ={	 		
	 		"title":title,
	 		"stl":stl,
	 		"username":username,
	 		"paperSize":"A4",
	 		"pageLayout":"portrait",
	 		"pdfFont":"arial",	 		
	 		"scheduler":"",	 		
	 		"reportHeaderFooter":reportHeaderFooter,
	 		"ih":columnhid,
	 		"multitenant":multitenant,
	 	};
      var Keys = Object.keys(pdf);	
	        for(var k = 0; k < Keys.length; ++k) {
	
   if (pdf.hasOwnProperty(Keys[k])) {
     console.log(Keys[k], pdf[Keys[k]]);
       pdfParams [Keys[k]]=pdf[Keys[k]]
            }
		 }
	 	console.log(pdfParams);
	 	//pdfParams.push({pdf})
	 	var headers = new Headers();
	 	headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	 	let report = "PID="+this.pid+"&params="+JSON.stringify(pdfParams); 
	 	console.log(report);
	 	return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/ereporthtml/', report, {headers: headers});
		
	 }
 
 sendtemplate(projectname,reportid,multiselectvalues,groupfield,columnproperty,stl,multitenant){
	let params = {	           	                 	   
			"projectname": projectname,
		   	"reportid":reportid,
		   	"multiselectvalues":multiselectvalues,		   	
			"groupfield":groupfield,		
			"columnproperty":columnproperty,
			"stl":stl,
			"multitenant":multitenant
			
		}
		console.log(params);
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let report = "PID="+this.pid+"&params="+JSON.stringify(params);		
		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/getReportData/', report , {headers: headers});

	}


	 sendwithoutpdfParams(projectname,reportid,multiselectvalues,groupfield,columnproperty,title,stl,username,reportHeaderFooter,columnhid,multitenant){
  
	 	let pdfParams ={
	 		 "projectname": projectname,
		   	"reportid":reportid,
		   	"multiselectvalues":multiselectvalues,		   	
			"groupfield":groupfield,
			"columnproperty":columnproperty,	 		 		
	 		"title":title,
	 		"stl":stl,
	 		"username":username,
	 		"paperSize":"A4",
	 		"pageLayout":"portrait",
	 		"pdfFont":"arial",	 		
	 		"scheduler":"",	 		
	 		"reportHeaderFooter":reportHeaderFooter,
	 		"ih":columnhid,
	 		"multitenant":multitenant,
	 	};
     
	 	var headers = new Headers();
	 	headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	 	let report = "PID="+this.pid+"&params="+JSON.stringify(pdfParams); 
	 	console.log(report);
	 	return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/ereporthtml/', report, {headers: headers});
		
	 }   
	csvFormatwithoutparam(projectname,reportid,multiselectvalues,groupfield,columnproperty,title,stl,username,reportHeaderFooter,columnhid,multitenant){
		let pdfParams ={
		"projectname": projectname,
		   	"reportid":reportid,
		   	"multiselectvalues":multiselectvalues,		   	
			"groupfield":groupfield,
			"columnproperty":columnproperty,	 		 		
	 		"title":title,
	 		"stl":stl,
	 		"username":username,
	 		"paperSize":"A4",
	 		"pageLayout":"portrait",
	 		"pdfFont":"arial",	 		
	 		"scheduler":"",	 		
	 		"reportHeaderFooter":reportHeaderFooter,
	 		"ih":columnhid,
	 		"multitenant":multitenant,
		};
		console.log(pdfParams);
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let report = "PID="+this.pid+"&params="+JSON.stringify(pdfParams); 
		console.log(report);
		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/ereportcsv/', report, {headers: headers});		
	}

csvFormatparam(projectname,reportid,multiselectvalues,groupfield,columnproperty,title,stl,username,reportHeaderFooter,columnhid,multitenant){
let pdf=this.pdfinput[0]
  console.log(pdf);
		let pdfParams ={
		"projectname": projectname,
		   	"reportid":reportid,
		   	"multiselectvalues":multiselectvalues,		   	
			"groupfield":groupfield,
			"columnproperty":columnproperty,	 		 		
	 		"title":title,
	 		"stl":stl,
	 		"username":username,
	 		"paperSize":"A4",
	 		"pageLayout":"portrait",
	 		"pdfFont":"arial",	 		
	 		"scheduler":"",	 		
	 		"reportHeaderFooter":reportHeaderFooter,
	 		"ih":columnhid,
	 		"multitenant":multitenant,
		};
		  var Keys = Object.keys(pdf);	
	        for(var k = 0; k < Keys.length; ++k) {
	
   if (pdf.hasOwnProperty(Keys[k])) {
     console.log(Keys[k], pdf[Keys[k]]);
       pdfParams [Keys[k]]=pdf[Keys[k]]
            }
		 }
		console.log(pdfParams);
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let report = "PID="+this.pid+"&params="+JSON.stringify(pdfParams); 
		console.log(report);
		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/ereportcsv/', report, {headers: headers});
	}
 
 reportEpostSave(service_meta,json_meta,userDetails,pagenav,navCtrl,selectedOptions){
	 let eptValue =[];
	 let s_meta = service_meta;
	 let data =  json_meta;
	 let report_submit ="";
	 let display_records:any;
	 let type;
	 let errorStatus ="";
	 let description = json_meta['rep_des'];
	 let rep_des = JSON.parse(description);
	 let external_con ="";
	 if (userDetails){
			this.username = userDetails.USERNAME;
			this.userid = userDetails.USERID;
		}
	 report_submit = data['repaction_meta'][0]['ReportSubmit'];
	 let viewreport = report_submit['exp'];
	 console.log(report_submit);
	 type = data['tem_type'];
	 display_records  = document.getElementById('displayreport').getElementsByTagName('ion-'+type);
	 let epost = report_submit['rep_epost'];
	 const non_grid_fields = epost.filter((item) => {
					console.log(item);console.log(item['is_gd']);return (item['is_gd'] == "False");
				});
	 const grid_fields = epost.filter((item) => {
					console.log(item);console.log(item['is_gd']);return (item['is_gd'] == "True");
				});
	 if(non_grid_fields.length>0){
		 let fieldValue="";
		 let table = [];
		 let epostJson ={};
		 for(let i=0;i<non_grid_fields.length;i++){
			 var tableObj = {
				 'table_value': [],
                        }
			 let target = non_grid_fields[i]["tr_fld"][0];
			 let referJson = JSON.parse(target['cjson']);
			 let source =  non_grid_fields[i]["so_fld"];
			 let expression = non_grid_fields[i]['exp'];
			 let dbTable = referJson["txtabledetailid"];
			 if(target['pt'] == null){
			 epostJson['primary_table'] = dbTable;
			 }
			 if(source == null){
				 if(expression){
					 let ExprObj = new Expression("");
					 ExprObj.Expression(expression, this.userDetails, "", "");
					 let GetVal = ExprObj.Evaluate();
					 if(GetVal == 'AUTOGENERATE'){
						 let prefix = referJson['field_slug'].substring(0, 3).toUpperCase();
						 let uniqueId = new Date().valueOf().toString();
						 fieldValue = prefix+uniqueId;
					 }
					 else{
					 fieldValue = GetVal;
					 }
				 }
				 else{
				 
				 }
				 
				 
			 }
			 var item ={
				'FN':target['idt'],
				'FV':fieldValue,
				'DT': referJson['datatype'],
				'SV': referJson['isdbfield'],
				'AD': target["ad"],
				'WT': target["wt"]
			}
			 if(table.length>0){
				 const filteredResult = table.filter((item) => {
					console.log(item);console.log(item['table_name']);return (item['table_name'] == dbTable);
				});
				if(filteredResult.length>0){
					filteredResult[0].table_value.push(item);
				}
				 
			 }
			 else{
				tableObj.table_value.push(item);
				tableObj['table_name'] = dbTable;
				tableObj['od'] = 1;
				table.push(tableObj);
				 console.log(table);
			 }
			 
		 }
		 if(grid_fields.length>0){
			 let grid_list =[];
			 for (let i=0;i<display_records.length;i++){
			 let record = display_records[i];
			 let id = display_records[i].id;
			 let index = id.split('-')[1];
			 console.log(index);
			 var tableObj = {
			'table_value': [],
                        }
			 let condition = rep_des['condition'];
			 for(let j=0;j<grid_fields.length;j++){
				 let source = grid_fields[j]['so_fld'];
				 let target = grid_fields[j]['tr_fld'][0];
				 let referJson = JSON.parse(target['cjson']);
				 let dbTable = referJson["txtabledetailid"];
				 let fieldValue="";
				try{
					let content = rep_des['comp'];
					const jsonComp = content.filter((item) => {
					console.log(item);console.log(item['id']);return (item['id'] == source);
				});
					console.log(jsonComp);
					if(jsonComp.length >0){
						let comp_type = jsonComp[0]['type'];
						let comp_id ="";
					
						if(comp_type == 'text'){
						   comp_id = "input-"+index+"-"+jsonComp[0]['id'];
						   try{
						   document.getElementById(comp_id).setAttribute('name',comp_id)
						   let input = document.getElementsByName(comp_id);
						   console.log(comp_id);
							fieldValue =  input[0]['children'][0]['value'];
							  
						   }
							catch(err){
							this.getEpostAlert("Input Field id in Row Template Html is not correct");
							errorStatus = "true";	
							}
						}
						else if(comp_type =='select'){
						  comp_id = "select-"+index+"-"+jsonComp[0]['id'];
						   console.log(comp_id);
							try{
						   //document.getElementById(comp_id).setAttribute('name',comp_id)
						   //let select = document.getElementsByName(comp_id);
								selectedOptions[comp_id]
								fieldValue =  selectedOptions[comp_id];
							}
							catch(err){
							this.getEpostAlert("Select Field id in Row Template Html is not correct");
								errorStatus = "true";
							}
						}
					}
					else{
					fieldValue = service_meta[index][source];
					}
				}
				catch(err){
					fieldValue = service_meta[index][source];
				}
				var item ={
				'FN':target['idt'],
				'FV':fieldValue,
				'DT': referJson['datatype'],
				'SV': referJson['isdbfield'],
				'AD': target["ad"],
				'WT': target["wt"]
			}
				
			if(table.length >0){
				tableObj['od'] = 2+j;
			}
				 else{
					 tableObj['od'] = 2;
				 }
				 tableObj.table_value.push(item);
				tableObj['table_name'] = dbTable;
				
			}
				 if(condition){
					 let getVal ="";
					 userDetails['pagetype'] = 'displayreport';
					 userDetails['item_index'] = index;
					 userDetails['desc_json'] = rep_des;
					 let ExprObj = new Expression("");
					 ExprObj.Expression(condition, userDetails, "reportview", "");
					 getVal = ExprObj.Evaluate();
					 if(getVal == "T"){
						 table.push(tableObj);
						 grid_list.push(tableObj);
					 }
				 }
				 else{
					 table.push(tableObj);
					 grid_list.push(tableObj);
				 }
				  if (errorStatus == "true"){
				 break;
			 }
		 
		 }
			if(grid_list.length == 0){
				this.getEpostAlert("Please Order Items.");
				errorStatus  ="true";
			}
	 
	 }
		 console.log(table);
		 epostJson['layesrs'] = table;
		 eptValue.push(epostJson);
	 }
	 else{
		 for (let i=0;i<display_records.length;i++){
			 let record = display_records[i];
			 let id = display_records[i].id;
			 let index = id.split('-')[1];
			 console.log(index);
			 var tableObj = {
			'table_value': [],
                        }
			 var epostJson ={};
			 let table = [];
			 let condition = rep_des['condition'];
			for(let j=0;j<epost.length;j++){
				let source = epost[j]['so_fld'];
				let target = epost[j]['tr_fld'][0];
				let referJson = JSON.parse(target['cjson']);
				let dbTable = referJson["txtabledetailid"];
			    let fieldValue="";
				try{
					let content = rep_des['comp'];
					const jsonComp = content.filter((item) => {
					console.log(item);console.log(item['id']);return (item['id'] == source);
				});
					console.log(jsonComp);
					if(jsonComp.length >0){
						let comp_type = jsonComp[0]['type'];
						let comp_id ="";
					
						if(comp_type == 'text'){
						   comp_id = "input-"+index+"-"+jsonComp[0]['id'];
						   try{
						   document.getElementById(comp_id).setAttribute('name',comp_id)
						   let input = document.getElementsByName(comp_id);
						   console.log(comp_id);
							fieldValue =  input[0]['children'][0]['value'];
							  
						   }
							catch(err){
							this.getEpostAlert("Input Field id in Row Template Html is not correct");
							errorStatus = "true";	
							}
						}
						else if(comp_type =='select'){
						  comp_id = "select-"+index+"-"+jsonComp[0]['id'];
						   console.log(comp_id);
							try{
						   //document.getElementById(comp_id).setAttribute('name',comp_id)
						   //let select = document.getElementsByName(comp_id);
								selectedOptions[comp_id]
								fieldValue =  selectedOptions[comp_id];
							}
							catch(err){
							this.getEpostAlert("Select Field id in Row Template Html is not correct");
								errorStatus = "true";
							}
						}
					}
					else{
					fieldValue = service_meta[index][source];
					}
				}
				catch(err){
					fieldValue = service_meta[index][source];
				}
				var item ={
				'FN':target['idt'],
				'FV':fieldValue,
				'DT': referJson['datatype'],
				'SV': referJson['isdbfield'],
				'AD': target["ad"],
				'WT': target["wt"]	
			}
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
				table.push(tableObjad);
			}
			
			}else{
				tableObj.table_value.push(item);
				tableObj['table_name'] = dbTable;
				tableObj['od'] = 1;
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
				tableObjad['od'] = 2+j;
				table.push(tableObjad);
			}
			console.log(filteredResult);	
			}else{
			tableObj.table_value.push(item);
			tableObj['table_name'] = dbTable;
			tableObj['od'] = 2;
			table.push(tableObj);
		}
		}
				
			}
			 table.sort(function(a, b){return a.od - b.od;});
			 
			 epostJson['layesrs'] = table;
			  if(condition){
				  let getVal ="";
				  userDetails['pagetype'] = 'displayreport';
				  userDetails['item_index'] = index;
				  userDetails['desc_json'] = rep_des;
				  let ExprObj = new Expression("");
				  ExprObj.Expression(condition, userDetails, "reportview", "");
				  getVal = ExprObj.Evaluate();
				  if(getVal == "T"){
				   eptValue.push(epostJson);
				  }
			 }
			 else{
			 eptValue.push(epostJson);
			 }
			 console.log(eptValue);
			
			 if (errorStatus == "true"){
				 break;
			 }
		 }
	       if (eptValue.length == 0){
				 this.getEpostAlert("Please Fill All Columns.");
				errorStatus = "true";
			 }
	 }
		
	       if (eptValue.length == 0){
				 this.getEpostAlert("Please Fill All Columns.");
				errorStatus = "true";
			 }
	  
	 var layers = {
                    'layers': [],    //save values in transaction
                    'primary_table': '',//for primary table name
                    'user_name': this.username,
                    'pid': this.pid,  //for projectid
                    'user_id': this.userid,//for user id
                    'project_name': this.projectname,//for projectname
                    'CB': [],
	                'EP':[],  //for Eupdate in Transaction
				    'EPT':eptValue  //for Epost in Transaction
                }
	 
	 if (errorStatus == "false" || errorStatus == "") {
		 let savetype = 'online';
		 if (savetype == 'online' || savetype =='both'){
			 this.sendSavejson(layers).subscribe(saveMessage => {
				 let saveStatus;
				 if (saveMessage){
					 let userMessage = saveMessage.json();
					 saveStatus = userMessage["values"]["SAVED"];
					 userDetails['SUBMITID'] = userMessage["values"]["EpostId"];
					 if (saveStatus == "TRUE") 
					 {                          
						 if(viewreport){
							 this.navReport(viewreport,pagenav,navCtrl,userDetails);				 
						 }
					 } 
					 else if(saveStatus == "FALSE") {
						 let alert = this.alertCtrl.create({
							 title: 'Information',
							 subTitle: userMessage["values"]["MESSAGE"],
							 buttons: ['OK']
						 });
						 alert.present();
					 }
					 return saveStatus;
				 }
			 },
                                                    err => {
                  //console.log("Oops!");
                  let alert = this.alertCtrl.create({
                    title: 'Information',
                    subTitle: 'Server Connection Error.',
                    buttons: ['OK']
                  });
                  alert.present();
                  return "error"
                });
        }
   }
	 
 }
 
 navReport(expr,pagenav,navCtrl,userDetails){
	 let split_data = this.datasplitting(expr);
	 let pageid = split_data['id'];
	 const navpage_filter = pagenav['pages'].filter((item) => {
		 return (item['id'] == pageid);
	 });
	 //console.log(navpage_filter);
	 if(navpage_filter.length >0){
		 let page = navpage_filter[0];
		 navCtrl.push(page.component,{'userdetails':userDetails}).then(() => {
			 const startIndex = navCtrl.getActive().index - 1;
			 navCtrl.remove(startIndex, 1);
		 });
	 }	
 
 }
 
datasplitting(value){
	let obj ={};
	let data = value.split(/[ .:;?!~,`"&|()<>\[\]\r\n/\\]+/);
	obj['type'] = data[0];
	obj['id'] = data[1].replace(/["'{}]/g,"");
	return obj;
}
 sendSavejson(Json: any) {
		/* Server Request Calling for Save Function*/
        let saveJson = Json;
		//let offlineStore = [];
		console.log(saveJson);
		//console.log(this.network);
		if(this.network.type == "none"){
		 //this.offlinesave(saveJson);
		 	
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

getEpostAlert(message){
	let alert = this.alertCtrl.create({
									title: 'Information',
									subTitle: message,
									buttons: ['OK']
								});
								alert.present();

}

showResults(value, index){
console.log(index);
}

savePaymentstatus(pay,userDetails,pagenav,navCtrl,expression){
	let table_id = ['customer_email','amount','payment_id','razor_pay_id','order_no','payment_status'];
	let table_name = 'payment_info';
	let cb =[];
	let value =[];
	let table =[];
	for(let i=0;i<table_id.length;i++){
		let datatype="";
		if(table_id[i] == 'amount'){
			datatype= "IntegerField";	
		}
		else{
			 datatype= "CharField";		
		}
		var item = {
			"AD":"True",
			"DT": datatype,
			"FN":table_id[i],
			"FV":pay[table_id[i]],
			"SV":true,
			"WT":"text"
		}
		value.push(item);	
	}
	
	let table_value ={
		'od':1,
		'table_name' :table_name,
		"table_value" :value
	}
	table.push(table_value);
	
	let layers ={
		'CB':cb,
		'EP':cb,
		'EPT':cb,
		'layers':table,
		'primary_table':table_name,
		'user_name': this.username,
		'pid': this.pid,  //for projectid
        'user_id': this.userid,//for user id
        'project_name': this.projectname,//for projectname
	};
	 this.sendSavejson(layers).subscribe(saveMessage => {
		 if(saveMessage){
		 console.log(saveMessage);
			 let userMessage = saveMessage.json();
			 let saveStatus = userMessage["values"]["SAVED"];
			 userDetails['PAYID'] = userMessage["values"]["SaveId"];
			  if (saveStatus == "TRUE") 
					 {    
						 if(expression){
							 this.navReport(expression,pagenav,navCtrl,userDetails);				 
						 }
						 
					 } 
					 else if(saveStatus == "FALSE") {
						 let alert = this.alertCtrl.create({
							 title: 'Information',
							 subTitle: userMessage["values"]["MESSAGE"],
							 buttons: ['OK']
						 });
						 alert.present();
					 }
			 
		 }
		 //alert(saveMessage);
	 },err => {
		 let alert = this.alertCtrl.create({
			 title: 'Information',
			 subTitle: 'Server Connection Error.',
			 buttons: ['OK']
		 });
		 alert.present();
		 return "error"
	 });
}

printFormtSql(sql,type,mapValue){
	var headers = new Headers();
	var item = {
		"SQL"  : sql,
		"TYPE" :  type,
		"MAP" : mapValue,
		"ISMULTITENANT" : this.singleton.ismultitenant,
		"PROJECTID" : this.singleton.PID,
	}
	headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	let report = "PID="+this.pid+"&params="+JSON.stringify(item); 
	console.log(report);
	return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/printFormatSql/', report, {headers: headers});		
}
}
