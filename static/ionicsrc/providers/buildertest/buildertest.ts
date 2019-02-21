import { Injectable } from '@angular/core';
import { Http,Headers } from '@angular/http';
import 'rxjs/add/operator/map';
import { Storage } from '@ionic/storage';

/*
  Generated class for the BuildertestProvider provider.

  See https://angular.io/docs/ts/latest/guide/dependency-injection.html
  for more info on providers and Angular DI.
*/
@Injectable()
export class BuildertestProvider {

  constructor(public http: Http,public storage: Storage) {
    console.log('Hello BuildertestProvider Provider');
  }
  
	
	customLoginNew(sql:string,loginType:string,testJson:object,pid:string) {
		let quickDetails= {
			"SQL":sql,
			"SQLPARAMS":testJson,
			"LOGINTYPE":loginType,			
		};
		
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params ="PID="+pid+"&quickDetails="+JSON.stringify(quickDetails);  
		return this.http.post('http://192.168.125.75:32923/mfginventory/mobileserviceapi/customLogin',params,{headers: headers});
		
	}

	customOtpNew(sql:string,loginType:string,testJson:object,pid:string,projectname:string) {
		let quickDetailsOtp= {
			"SQL":sql,
			"SQLPARAMS":testJson,
			"LOGINTYPE":loginType,
			"PROJECTNAME":projectname
		};
		
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params = "PID="+pid+"&quickDetailsOtp="+JSON.stringify(quickDetailsOtp);   

		return this.http.post('http://192.168.125.75:32923/mfginventory/mobileserviceapi/customOtpNew',params,{headers: headers});
		
	}

	customSelectService(data:object){
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params = "PID="+data['pid']+"&fieldType="+data['fieldType']+"&eformid="+data['eFormId']+"&fieldName="+data['fieldName']+"&projectid="+data['projectId']+"&USERNAME="+data['username'];
	
		return this.http.post('http://192.168.125.75:32923/mfginventory/mobileserviceapi/eformsql',params,{headers: headers});
	}
	
	customSearch(data:object,pid:string,projectname:string){
		var headers = new Headers();
		headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		let params = "PID="+pid+"&searchButton="+JSON.stringify(data);   

		return this.http.post('http://192.168.125.75:32923/mfginventory/mobileserviceapi/customSearchButton',params,{headers: headers});
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
		let params = "PID="+data['pid']+"&fieldType="+data['fieldType']+"&eformid="+data['eFormId']+"&fieldName="+data['fieldName']+"&projectid="+data['projectId']+"&USERNAME="+data['username']+"&limit="+data['limit']+"&limitvalue="+data['limitvalue'];
	
		return this.http.post('http://192.168.125.75:32923/mfginventory/mobileserviceapi/eformsql',params,{headers: headers});
	}

}
