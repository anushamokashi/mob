import { Injectable } from '@angular/core';
import { Http,Headers } from '@angular/http';
import 'rxjs/add/operator/map';
import { Storage } from '@ionic/storage';

import { SingletonProvider } from '../../providers/singleton/singleton';

/*
  Generated class for the LoginserviceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class LoginserviceProvider {
	resturl :any;

  	constructor(public http: Http,public storage: Storage,public singleton: SingletonProvider) {		
		console.log('Hello LoginserviceProvider Provider');
		this.resturl = this.singleton.resturl;
	}
	
	customLoginNew(sql:string,loginType:string,testJson:object,pid:string,playerId:string) {
		let quickDetails= {
			"SQL":sql,
			"SQLPARAMS":testJson,
			"LOGINTYPE":loginType,
			"PROJECTNAME":this.singleton.projectname,
			"PLAYERID":playerId,
			"MULTITENANT" :this.singleton.ismultitenant,
		};
		
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params ="PID="+pid+"&quickDetails="+JSON.stringify(quickDetails); 
	    if(loginType == "form"){
			return this.http.post(this.resturl+'mobileserviceapi/customLogin',params,{headers: headers});
		}
	   	else if(loginType =="otp"){
		 	return this.http.post(this.resturl+'mobileserviceapi/customOtpNew',params,{headers: headers});

		}
		
	}

	customOtpNew(sql:string,loginType:string,testJson:object,pid:string,projectname:string,playerId:string) {
		let quickDetailsOtp= {
			"SQL":sql,
			"SQLPARAMS":testJson,
			"LOGINTYPE":loginType,
			"PROJECTNAME":projectname,
			"PLAYERID":playerId,
		};
		
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params = "PID="+pid+"&quickDetailsOtp="+JSON.stringify(quickDetailsOtp);   

		return this.http.post(this.resturl+'mobileserviceapi/customOtpNew',params,{headers: headers});
		
	}

	customSearch(data:object,pid:string,projectname:string){
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params = "PID="+pid+"&searchButton="+JSON.stringify(data);   

		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/customSearchButton',params,{headers: headers});
	}

	// duplicateCheking(checklist:any){
	// 	var headers = new Headers();
	// 	headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	// 	let params = "checkList="+JSON.stringify(checklist);    

	// 	return this.http.post('http://192.168.125.75:32923/mfginventory/mobileserviceapi/duplicateCheking',params,{headers: headers});
	// }
	
	hiddenSqlService(data:object){
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params = "fieldType="+data['fieldType']+"&eformid="+data['eFormId']+"&fieldName="+data['fieldName']+"&projectid="+data['projectId']+"&projectname="+data['projectName']+"&USERNAME="+data['username']+"&ISMULTITENANT="+this.singleton.ismultitenant+"&TYPE="+data['type']+data['MapValue'];
	
		return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/eformsql',params,{headers: headers});
	}
   
    sendMapjson(Json: any) {
        let MapJson = Json;
		console.log(MapJson);
        var headers = new Headers();
        headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        let params = "PID="+this.singleton.PID+"&mapJson="+JSON.stringify(MapJson);
        console.log("f");
        return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/syncmaster/',params,{headers: headers});
	}	
}
