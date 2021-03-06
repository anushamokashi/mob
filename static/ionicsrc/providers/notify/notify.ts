import { Http,Headers } from '@angular/http';
import 'rxjs/add/operator/map';
import { Injectable } from '@angular/core';

import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
import { SQLitePorter } from '@ionic-native/sqlite-porter';
import { SingletonProvider } from '../../providers/singleton/singleton';
/*
  Generated class for the NotifyProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class NotifyProvider {
	constructor(public http: Http,private sqlite: SQLite,private sqlitePorter: SQLitePorter,public singleton: SingletonProvider) {
	
		console.log('Hello NotifyProvider Provider');
  	}

	notification(Json: any) {
        let MapJson = Json;
		console.log(MapJson);
        var headers = new Headers();
        headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        let params = "&message="+JSON.stringify(MapJson);
        console.log("f");
        return this.http.post(this.singleton.dynamicresturl+'/mobileserviceapi/ionicnotfication/',params,{headers: headers});
	}
	
	notificationIndb(data){
		console.log(data);
		let offlinesql ="";
		let table ="";
		let sqlstart="";
		table = 'CREATE TABLE IF NOT EXISTS notification (title VARCHAR(1000),body VARCHAR(10000))';
		try
		{
			sqlstart = 'INSERT INTO notification (title,body)  VALUES ("'+data.payload.title+'", "'+data.payload.body+'")';
		}catch(err)
		{
			sqlstart = 'INSERT INTO notification (title,body)  VALUES ("'+data.notification["payload"].title+'", "'+data.notification["payload"].body+'")';
		}
	   	offlinesql = table+';'+sqlstart;
	   	console.log(offlinesql);
	    this.sqlite.create({
			name: 'data.db',
			location: 'default'
		}).then((db: SQLiteObject) => {
			this.sqlitePorter.importSqlToDb(db, offlinesql)
      		.then(() =>{
				let offdata = this.datapresent(db);
				 /* Using Cordova Sqlite Porter Plugin*/
			}).catch(e => console.error(e));
		}).catch(e => console.log(e));
	}
	
	
	datapresent(db){
		this.sqlitePorter.exportDbToJson(db)
		.then((data) =>{
			console.log(data);
			return data;
		}).catch(e => console.error(e));
		var successFn = function(json, count){
        	//console.log("Exported JSON: "+json);
        	alert("Exported JSON contains equivalent of "+count+" SQL statements");
    	};
	}

	getNotificationMsg(roleJson){
		var headers = new Headers();
        headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        let params = "&role="+JSON.stringify(roleJson);
        console.log("f");
        return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/getNotificationMessages/',params,{headers: headers});
	}

	updateNotificationStatus(notificationJson){
		var headers = new Headers();
        headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        let params = "&msg="+JSON.stringify(notificationJson);
        console.log("f");
        return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/updateNotificationStatus/',params,{headers: headers});

	}

	deleteNotification(delJson){
		var headers = new Headers();
        headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        let params = "&message="+JSON.stringify(delJson);
        console.log("f");
        return this.http.post(this.singleton.dynamicresturl+'mobileserviceapi/deleteNotification/',params,{headers: headers});

	}
}
