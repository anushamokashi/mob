import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { AlertController } from 'ionic-angular';
import { Http } from '@angular/http';
//import {BrowserXhr} from 'angular2/http';
import { Storage } from '@ionic/storage';
import { Network } from '@ionic-native/network';
import { SQLite, SQLiteObject } from '@ionic-native/sqlite';
//import {Injectable} from 'angular2/core';
import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer';
import { File } from '@ionic-native/file';
import { ModalController, ViewController } from 'ionic-angular';
import { DomSanitizer, SafeResourceUrl, SafeUrl} from '@angular/platform-browser';
import { DatePipe } from '@angular/common';
import { CmserviceProvider } from '../../providers/cmservice/cmservice';
import { ExpressionProvider } from '../../providers/expression/expression';
import { PagenavProvider } from '../../providers/pagenav/pagenav';
import { Injector } from '@angular/core';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { BarcodeScanner } from '@ionic-native/barcode-scanner';
declare var cordova : any;
declare var Mustache:any;

/**
 * Generated class for the ExamplePage page.
 *
 * See http://ionicframework.com/docs/components/#navigation for more info
 * on Ionic pages and navigation.
 */


@Component({
    selector: 'page-report',
    templateUrl: 'report.html',
    providers: [ExpressionProvider],
})
export class ReportPage {
    subtitle: any;
    subtitles: any;
    projectname: any;
    reportid: any;
    show_grand_total: any;
    groupfield: any;
    columnproperty: any;
    reports: any;
    title: any;
    titles: any;
    reportfield: any;
    values: any;
    LoginDetails: any;
    username: any;
    names: any[] = [];
    datass:any[] = [];
    inputValue: string;
    jsonObj: any;
    column: any;
    UserDetails: any;
    norepeatUniqueColumnName: any;
    reportHeaderFooter: any;
    otherService: any;
    report_meta: any;
    elementList: any[] = [];
	selectId:any;
    selectedOptions: Object =  {};
    preset_value: Object =  {};
    rptName:any;
    report_result_array = [];
    resturl :any;
    multitenant:any;
	isAllHiddenParams : Boolean = false;
    public Options:any = {
        scales: { yAxes: [{ticks: {beginAtZero:true }}]}};
      public Labels:string[] = [];
      public Type: string = "bar";
      public Legend:boolean = true;      
      public Data:any[] = [{label: 'Nil',data:[],borderWidth: 1}];
    constructor(public datePipe: DatePipe,public modalCtrl: ModalController, public http: Http, public navCtrl: NavController, public navParams: NavParams, public mycmservice: CmserviceProvider, public alertCtrl: AlertController,
        public transfer: FileTransfer, public file: File, public myexpression: ExpressionProvider, private network: Network, public storage: Storage, private sqlite: SQLite, 
        private injector: Injector,private _sanitizer: DomSanitizer,public singleton: SingletonProvider,private barcodeScanner: BarcodeScanner) {
        this.resturl = this.singleton.resturl;
        this.multitenant = this.singleton.ismultitenant;
		this.rptName = 'report_id';
        this.otherService = this.injector.get(PagenavProvider);
        this.http.get('assets/json/report.json').map(res => res.json()).subscribe(data => {
            this.subtitles = data;
            this.report_meta = data;
            this.Type=this.subtitles.gtype;
            this.reportHeaderFooter = {
                report_header_line1: this.subtitles.rh1,
                report_header_line2: this.subtitles.rh2,
                report_footer_line1: this.subtitles.rf1,
                report_footer_line2: this.subtitles.rf2,
            };
            this.UserDetails = this.navParams.get("userdetails");
            if (this.UserDetails == undefined) {
                this.storage.get('userObj').then((loginInfo) => {
                    this.UserDetails = loginInfo;
                    this.UserDetails['pagetype'] = 'displayreport'; //for differentiate transaction or report in expr.js
                });
            } else {
                this.UserDetails['pagetype'] = 'displayreport'; //for differentiate transaction or report in expr.js
            }


            let reporttype = this.subtitles.rt;
            
            if (reporttype == "displayreport") {
                let templatehtml = this.subtitles.template;
                let keys = JSON.stringify(this.subtitles.reportparamfield_meta);
                console.log(keys);
                let jsonObj = JSON.parse(keys);
                let projectname = this.subtitles.proj;
                let reportid = this.subtitles.tit;
                let multiselectvalues = "[]";
                let stl = "[]";
                let multitenant=this.multitenant;
                let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
                let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
                //***withoutparams***/// 
                if (jsonObj.length == 0) {
                    this.mycmservice.sendReportwithoutParams(projectname, reportid, multiselectvalues, groupfield, columnproperty, stl,multitenant).subscribe(responseData => {
                        console.log(responseData);
                        this.reports = responseData.json();   
						let reportfield = this.reports['reportData'];    
						let datas =JSON.parse(reportfield);
						console.log(datas);
						let id =datas['store']['fields'].indexOf('pname');
						this.column=datas['store']['data']['frame'];
						console.log(this.column);
						this.titles = datas['store']['fields'];
						console.log(this.titles);               
						let names =[];
						for (var i = 0; i < this.column.length; i++) {
							let values = {};
							for(var j=0;j< this.titles.length; j++){
								values[this.titles[j]] =(this.column[i][j]);
							}
							this.names.push(values);
						}
						console.log(this.names);
                        let imageid=this.names; 
                        //console.log(imageid)  ;
                        for (var k=0;k< imageid.length;k++){
                            let objId=imageid[k].objectid;
                            let imagetable = imageid[k].imagetable;
                            //console.log(objId);
                            console.log(objId,imagetable);
                            this.getImageById(objId,imagetable); 
                        } 
                    });
                } 
                else {
                    //display report with param
                    let initalHiddenComponents: any[] = [];
				    let formid = this.rptName+"paramForm";
                    let elements = document.getElementById(formid).querySelectorAll('*[name]');
                    for (let i = 0; i < elements.length; i++) {
                        if (elements[i].id != "") {
                            this.elementList.push(elements[i].id);
                        }
                    }
                    for (let i of this.elementList) {
                        if (document.getElementsByName(i)[0].hidden == true) {
                            initalHiddenComponents.push(i);
                        } else if (document.getElementById(i).dataset.readonly == "True") {
                            let nextElement = document.getElementsByName(i);
                            this.myexpression.evaluateExp("", nextElement, this.UserDetails,this.preset_value);
                        } else {
                            break;
                        }
                    }
					
					if(initalHiddenComponents.length == this.elementList.length){
						this.isAllHiddenParams = true;
					}
                    //call hidden function if there is hidden fields 
                    if ((initalHiddenComponents.length) != 0) {
                        this.UserDetails['pagetype'] = 'txview';
                        this.myexpression.hiddenElementexp(initalHiddenComponents, this.UserDetails,this.preset_value,this.selectedOptions,"report",this,this.isAllHiddenParams);
                    }
                
                   
                    
                }
            }
            else if (reporttype == "graphicalreport")
            {
                
                let keys = JSON.stringify(this.subtitles.reportparamfield_meta);
                console.log(keys);
                let jsonObj = JSON.parse(keys);
                let projectname = this.subtitles.proj;
                let reportid = this.subtitles.tit;
                let multiselectvalues = "[]";
                let stl = "[]";
                let multitenant=this.multitenant;
                let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
                let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
                if (jsonObj.length == 0) {
                    this.mycmservice.sendReportwithoutParams(projectname, reportid, multiselectvalues, groupfield, columnproperty, stl,multitenant).subscribe(responseData => {
                        console.log(responseData);
                        this.reports = responseData.json();   
						let reportfield = this.reports['reportData'];    
						let datas =JSON.parse(reportfield);
						console.log(datas);
						let id =datas['store']['fields'].indexOf('pname');
						this.column=datas['store']['data']['frame'];
						console.log(this.column);
						this.titles = datas['store']['fields'];
                        console.log(this.titles);     
                        //this.Labels = this.titles;
                        let xaxis=this.subtitles.xcoord;
                        let xaxis_index = this.titles.findIndex(item =>{
                            return (item == xaxis);
                        });
                        let yaxis=this.subtitles.ycoord;   
                        let yaxis_index = this.titles.findIndex(item =>{
                            return (item == yaxis);
                        });
                        let datass =[];
                        let names=[];
                        for(var j=0;j< this.titles.length; j++){
                            let xaxis=(this.subtitles.xcoord);                                
                            if(xaxis==this.titles[j]){
                                for (var i = 0; i < this.column.length; i++) {                                    
                                     let labels={};
                                     labels=this.column[i][xaxis_index];
                                     this.names.push(labels);
                            }                                
                                    
                                }
                                if(yaxis==this.titles[j]){
                                    for (var k = 0; k < this.column.length; k++) {
                                            let values = {};                                         	                               
                                             values =this.column[k][yaxis_index];                                
                                             this.datass.push(values);
                                        	//for(var s=0;s< this.titles.length; s++){ //}
                                }
                            }
                        }                      
                        this.Labels=this.names;
                        console.log( this.Labels);
                        this.Data[0].data = this.datass;
                        //this.barChartData[0].data = this.datass;
                        console.log( "barChartData");                        
                      
                    });
                }
                else {
                    let projectname = this.subtitles.proj;
                    let reportid = this.subtitles.tit;
                    let multiselectvalues = "[]";
                    let stl = "[]";
                    let multitenant=this.multitenant;
                    let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
                    let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
                    let keys = JSON.stringify(this.subtitles.reportparamfield_meta);
                    console.log(keys);
                    let jsonObj = JSON.parse(keys);
                    let keyset = [];
                    let obj = [];
                    let inputValue = {};
                    
                    for (var i = 0; i < jsonObj.length; i++) {

                        keyset.push(jsonObj[i]['sl']);
                        console.log(keyset);
                        let id = jsonObj[i]["idt"];
                        obj.push(jsonObj[i]["idt"]);
                        console.log(obj)
                        inputValue[keyset[i]] = this.preset_value[id];
                        console.log(inputValue)
        
                    }
        
                    this.mycmservice.sendReportParams(inputValue, projectname, reportid, multiselectvalues, groupfield, columnproperty, stl,multitenant).subscribe(responseData => {
                      console.log(responseData);
                      this.reports = responseData.json();   
						let reportfield = this.reports['reportData'];    
						let datas =JSON.parse(reportfield);
						console.log(datas);
						let id =datas['store']['fields'].indexOf('pname');
						this.column=datas['store']['data']['frame'];
						console.log(this.column);
						this.titles = datas['store']['fields'];
                        console.log(this.titles);     
                        //this.Labels = this.titles;
                        let xaxis=this.subtitles.xcoord;
                        let xaxis_index = this.titles.findIndex(item =>{
                            return (item == xaxis);
                        });
                        let yaxis=this.subtitles.ycoord;   
                        let yaxis_index = this.titles.findIndex(item =>{
                            return (item == yaxis);
                        });
                        let datass =[];
                        let names=[];
                        for(var j=0;j< this.titles.length; j++){
                            let xaxis=(this.subtitles.xcoord);                                
                            if(xaxis==this.titles[j]){
                                for (var i = 0; i < this.column.length; i++) {                                    
                                     let labels={};
                                     labels=this.column[i][xaxis_index];
                                     this.names.push(labels);
                            }                                
                                    
                                }
                                if(yaxis==this.titles[j]){
                                    for (var k = 0; k < this.column.length; k++) {
                                            let values = {};                                         	                               
                                             values =this.column[k][yaxis_index];                                
                                             this.datass.push(values);
                                        	//for(var s=0;s< this.titles.length; s++){ //}
                                }
                            }
                        }                      
                        this.Labels=this.names;
                        console.log( this.Labels);
                        this.Data[0].label =yaxis;
                        this.Data[0].data = this.datass;
                        //this.barChartData[0].data = this.datass;
                        console.log( "barChartData");                        
                      

                    });
                }
                             
            }
             else {

                if (this.network.type == "none") {

                    let keys = JSON.stringify(this.subtitles.reportparamfield_meta);
                    console.log(keys);
                    let jsonObj = JSON.parse(keys);
                    if (jsonObj == 0) {
                        let sqldata = this.subtitles.query_meta;
                        let sql = sqldata[0]["sq"];
                        let columns = this.subtitles.reportfield_meta;
                        this.reporttbgrid(sql, columns);
                    } else {
                        let sqldata = this.subtitles.query_meta;
                        let sql = sqldata[0]["sq"];
                        let columns = this.subtitles.reportfield_meta;
                        this.reporttbgrid(sql, columns);
                    }
                } else {
                    let keys = JSON.stringify(this.subtitles.reportparamfield_meta);
                    console.log(keys);
                    let jsonObj = JSON.parse(keys);
                    let projectname = this.subtitles.proj;
                    let reportid = this.subtitles.tit;
                    let multiselectvalues = "[]";
                    let stl = "[]";
                    let multitenant=this.multitenant;
                    let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
                    let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
                    //***withoutparams***/// 
                    if (jsonObj == 0) {
                        this.mycmservice.sendReportwithoutParams(projectname, reportid, multiselectvalues, groupfield, columnproperty, stl,multitenant).subscribe(responseData => {
                            console.log(responseData);
                            this.reports = responseData.json();
                            let reportfield = this.reports['reportData'];
                            let datas = JSON.parse(reportfield);
                            console.log(datas);
                            let id = datas['store']['fields'].indexOf('pname');
                            this.titles = datas['store']['data']['frame'];

                            let table = document.getElementsByName('reporttb')[0];
                            let tbody = table.getElementsByTagName('tbody')[0];
                            let thead = table.getElementsByTagName('thead')[0];
                            if (tbody.rows.length > 0) {
                                for (let k = tbody.children.length; k > 0; k--) {
                                    //tbody.removeChild(tbody.children[k-1]);
                                    tbody.deleteRow(k - 1);
                                }
                            }
                            console.log(this.titles);
                            //for(var i=0;i<this.titles.length ; i++)
                            //{
                            //console.log(this.title[i][id]);
                            // this.names.push (this.titles[i][id]);
                            // }

                            for (var i = 0; i < this.titles.length; i++) {

                                let rowlength = tbody.rows.length;
                                let rowdata = this.titles[i];
                                let newRow = tbody.insertRow(tbody.rows.length);
                                //let row = table["insertRow"](rowlength);

                                if (rowlength == 0) {
                                    newRow.id = 'id' + rowlength;
                                    for (let j = 0; j < thead["children"].length; j++) {
                                        let newCell = newRow.insertCell(j);
                                        if (thead["children"][j]["hidden"] == true) {
                                            newCell["hidden"] = true;
                                        }

                                        if (thead["children"][j]['dataset']['type'] == "button") {
                                            var btn = document.createElement("BUTTON");
                                            var iconcls=thead["children"][j]['dataset']['icons']
                                            console.log(iconcls);
                                            btn.setAttribute("ion-button","");
                                            btn.setAttribute("icon-only","");
                                            btn.className = "reportButton";
                                            btn.innerHTML='<ion-icon name="'+iconcls+'" class="icon icon-md ion-md-'+iconcls+'"></ion-icon>';
                                            btn.dataset['exp'] = thead["children"][j]['dataset']['exp'];
                                            if(thead["children"][j]['dataset']['exp'] == "print()"){
                                                btn.addEventListener('click',(evt) =>  this.printReport(evt),false);
                                                btn.dataset['tableheaders'] =JSON.stringify( datas["store"]["fields"]);
                                            }
                                            else{
                                                btn.addEventListener('click',(evt) =>  this.reportButtonOnClick(evt),false);
                                            }

                                            //var t = document.createTextNode();
                                            //btn.appendChild(t);                         
                                            newCell.appendChild(btn);       
                                        }else{
                                        
                                        // Append a text node to the cell
                                        let newText = document.createTextNode(rowdata[j]);
                                        //this.norepeat.push (rowdata[j]);
                                        newCell.appendChild(newText);
                                        }
                                    }
                                } else {
                                    let previousRowvalue = rowlength - 1;
                                    let currentValue = "";
                                    newRow.id = 'id' + rowlength;
                                    for (let j = 0; j < thead["children"].length; j++) {
                                        let newCell = newRow.insertCell(j);
                                        if (thead["children"][j]["dataset"]["dontrepeat"] == "true") {
                                            let previousValue = tbody["children"][previousRowvalue]["children"][j].textContent;
                                            if (previousValue == rowdata[j] || previousValue == "") {
                                                currentValue = "";
                                            } else {
                                                currentValue = rowdata[j];
                                            }
                                        } else {

                                            currentValue = rowdata[j];
                                        }

                                        if (thead["children"][j]["hidden"] == true) {
                                            newCell["hidden"] = true;
                                        }
                                        if (thead["children"][j]['dataset']['type'] == "button") {
                                            var btn = document.createElement("BUTTON");
                                            var iconcls=thead["children"][j]['dataset']['icons']
                                            console.log(iconcls);
                                            btn.setAttribute("ion-button","");
                                            btn.setAttribute("icon-only","");
                                            btn.className = "reportButton";
                                            btn.innerHTML='<ion-icon name="'+iconcls+'" class="icon icon-md ion-md-'+iconcls+'"></ion-icon>';
                                            btn.dataset['exp'] = thead["children"][j]['dataset']['exp'];
                                            if(thead["children"][j]['dataset']['exp'] == "print()"){
                                                btn.addEventListener('click',(evt) =>  this.printReport(evt),false);
                                                btn.dataset['tableheaders'] =JSON.stringify( datas["store"]["fields"]);
                                            }
                                            else{
                                                btn.addEventListener('click',(evt) =>  this.reportButtonOnClick(evt),false);
                                            }

                                            //var t = document.createTextNode();
                                            //btn.appendChild(t);                         
                                            newCell.appendChild(btn);       
                                        }else{
                                        
                                        // Append a text node to the cell
                                        let newText = document.createTextNode(rowdata[j]);
                                        //this.norepeat.push (rowdata[j]);
                                        newCell.appendChild(newText);
                                        }

                                    }
                                }

                            }
                        });
                    }
					else {
                    // report with allparam
                    let localThis = this;
                    let initalHiddenComponents: any[] = [];
                    let formid = this.rptName+"paramForm";
                    let elements = document.getElementById(formid).querySelectorAll('*[name]');
                    for (let i = 0; i < elements.length; i++) {
                        if (elements[i].id != "") {
                            this.elementList.push(elements[i].id);
                        }
                    }
                    for (let i of this.elementList) {
                        if (document.getElementsByName(i)[0].hidden == true) {
                            initalHiddenComponents.push(i);
                        } else if (document.getElementById(i).dataset.readonly == "True") {
                            let nextElement = document.getElementsByName(i);
                            this.myexpression.evaluateExp("", nextElement, this.UserDetails,this.preset_value);
                        } else {
                            break;
                        }
                    }
					if(initalHiddenComponents.length == this.elementList.length){
						this.isAllHiddenParams = true;
					}
                    //call hidden function if there is hidden fields 
                    if ((initalHiddenComponents.length) != 0) {
                        this.UserDetails['pagetype'] = 'txview';
						this.myexpression.hiddenElementexp(initalHiddenComponents, this.UserDetails, this.preset_value,this.selectedOptions,"report",this,this.isAllHiddenParams);
                        //this.getreport();
                            
                    }
                    
                }

                }
            }

        });
    }

    

    public buttonClicked: boolean = true;
    public onButtonClick() {
        this.buttonClicked = !this.buttonClicked;
    }

    //***withparams***///
    getreport() {
        this.buttonClicked = !this.buttonClicked;
        let projectname = this.subtitles.proj;
        let reportid = this.subtitles.tit;
        let multiselectvalues = "[]";
        let stl = "[]";
        let multitenant=this.multitenant;
        let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
        let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
        let keys = JSON.stringify(this.subtitles.reportparamfield_meta);
        console.log(keys);
        let jsonObj = JSON.parse(keys);
        let keyset = [];
        let obj = [];
        let inputValue = {};
        if (this.subtitles["rt"] == 'offlinereport') {
            let elementnodelList = [];
            let sql = "";
            sql = this.subtitles["query_meta"][0]["sq"];
            let columns = this.subtitles['reportfield_meta'];
	    let formid = this.rptName+"paramForm";
            let elements = document.getElementById(formid).querySelectorAll('*[name]');
            console.log(elements);
            for (let i = 0; i < elements.length; i++) {
                if (elements[i].id != "") {
                    elementnodelList.push(elements[i].id);
                }
            }
            console.log(elementnodelList);
            for (let e = 0; e < elementnodelList.length; e++) {
                let id = elementnodelList[e];
                let fieldvalue = document.getElementById(id).getElementsByTagName("input")[0].value;
                sql = sql.replace(":" + id, "'" + fieldvalue + "'")
            }
            this.reporttbgrid(sql, columns);
        } else {
            for (var i = 0; i < jsonObj.length; i++) {

                keyset.push(jsonObj[i]['sl']);
                console.log(keyset);
                let id = jsonObj[i]["idt"];
                obj.push(jsonObj[i]["idt"]);
                if(jsonObj[i]["wt"]=="date"){                
                  let date=this.preset_value[id]
                  inputValue[keyset[i]]=this.datePipe.transform(date,"dd-MMM-yy")
                }
                else{
                 inputValue[keyset[i]] = this.preset_value[id];
                console.log(inputValue);
                 }

            }

            this.mycmservice.sendReportParams(inputValue, projectname, reportid, multiselectvalues, groupfield, columnproperty, stl,multitenant).subscribe(responseData => {
              console.log(responseData);
              if(this.subtitles["rt"] == "displayreport")
                {
                  this.dpreport_construction(responseData);
                }
                else if(this.subtitles["rt"] == "graphicalreport"){
                    this.graphreport_construction(responseData);
                }
              else{
                this.reports = responseData.json();
                let reportfield = this.reports['reportData'];
                let datas = JSON.parse(reportfield);
                console.log(datas);
                let id = datas['store']['fields'].indexOf('pname')
                this.titles = datas['store']['data']['frame'];
                console.log(this.titles);
                let table = document.getElementsByName('reporttb')[0];
                let tbody = table.getElementsByTagName('tbody')[0];
                let thead = table.getElementsByTagName('thead')[0];
                if (tbody.rows.length > 0) {
                    for (let k = tbody.children.length; k > 0; k--) {
                        tbody.deleteRow(k - 1);
                    }
                }
                console.log(this.titles);
                for (var i = 0; i < this.titles.length; i++) {

                    let rowlength = tbody.rows.length;
                    let rowdata = this.titles[i];
                    let newRow = tbody.insertRow(tbody.rows.length);

                    if (rowlength == 0) {
                        newRow.id = 'id' + rowlength;
                        for (let j = 0; j < thead["children"].length; j++) {
                            let newCell = newRow.insertCell(j);
                            if (thead["children"][j]["hidden"] == true) {
                                newCell["hidden"] = true;
                            }

                            if (thead["children"][j]['dataset']['type'] == "button") {
                                var btn = document.createElement("BUTTON");
                                var iconcls=thead["children"][j]['dataset']['icons']
                                console.log(iconcls);
                                btn.setAttribute("ion-button","");
                                btn.setAttribute("icon-only","");
                                btn.className = "reportButton";
                                btn.innerHTML='<ion-icon name="'+iconcls+'" class="icon icon-md ion-md-'+iconcls+'"></ion-icon>';
                                btn.dataset['exp'] = thead["children"][j]['dataset']['exp'];
                                if(thead["children"][j]['dataset']['exp'] == "print()"){
                                    btn.addEventListener('click',(evt) =>  this.printReport(evt),false);
                                    btn.dataset['tableheaders'] =JSON.stringify( datas["store"]["fields"]);
                                }
                                else{
                                    btn.addEventListener('click',(evt) =>  this.reportButtonOnClick(evt),false);
                                }

                                //var t = document.createTextNode();
                                //btn.appendChild(t);                         
                                newCell.appendChild(btn);      
                            }else{
                            
                                // Append a text node to the cell
                                let newText = document.createTextNode(rowdata[j]);
                                //this.norepeat.push (rowdata[j]);
                                newCell.appendChild(newText);
                            }
                        }
                    } else {
                        let previousRowvalue = rowlength - 1;
                        let currentValue = "";
                        newRow.id = 'id' + rowlength;
                        for (let j = 0; j < thead["children"].length; j++) {
                            let newCell = newRow.insertCell(j);
                            if (thead["children"][j]["dataset"]["dontrepeat"] == "true") {
                                let previousValue = tbody["children"][previousRowvalue]["children"][j].textContent;
                                if (previousValue == rowdata[j] || previousValue == "") {
                                    currentValue = "";
                                } else {
                                    currentValue = rowdata[j];
                                }
                            } else {

                                currentValue = rowdata[j];
                            }

                            if (thead["children"][j]["hidden"] == true) {
                                newCell["hidden"] = true;
                            }
                            if (thead["children"][j]['dataset']['type'] == "button") {
                                var btn = document.createElement("BUTTON");
                                var iconcls=thead["children"][j]['dataset']['icons']
                                console.log(iconcls);
                                btn.setAttribute("ion-button","");
                                btn.setAttribute("icon-only","");
                                btn.className = "reportButton";
                                btn.innerHTML='<ion-icon name="'+iconcls+'" class="icon icon-md ion-md-'+iconcls+'"></ion-icon>';
                                btn.dataset['exp'] = thead["children"][j]['dataset']['exp'];
                                if(thead["children"][j]['dataset']['exp'] == "print()"){
                                    btn.addEventListener('click',(evt) =>  this.printReport(evt),false);
                                    btn.dataset['tableheaders'] =JSON.stringify( datas["store"]["fields"]);
                                }
                                else{
                                    btn.addEventListener('click',(evt) =>  this.reportButtonOnClick(evt),false);
                                }
                                

                                //var t = document.createTextNode();
                                //btn.appendChild(t);                         
                                newCell.appendChild(btn);      
                            }else{
                            
                            // Append a text node to the cell
                            let newText = document.createTextNode(rowdata[j]);
                            //this.norepeat.push (rowdata[j]);
                            newCell.appendChild(newText);
                            }

                        }
                    }

                }
                }
            });
        }
    }


    pdf() {
        let para = JSON.stringify(this.subtitles.reportparamfield_meta);
        console.log(para);
        let paraObj = JSON.parse(para);
        if (paraObj == 0) {
            let projectname = this.subtitles.proj;
            let reportid = this.subtitles.tit;
            let multiselectvalues = "[]";
            let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
            let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
            let title = this.subtitles.tit;
            let stl = "[]";
            let multitenant=this.multitenant;
            let username = this.UserDetails["first_name"];
            let reportHeaderFooter = this.reportHeaderFooter;
            let columnhidden = this.subtitles.reportfield_meta;
            console.log(columnhidden);
            let columnHide = [];
            for (var col = 0; col < columnhidden.length; col++) {
                if (columnhidden[col].ih == "True") {


                    columnHide.push(columnhidden[col].sl);
                }
            }

            let columnhid = JSON.stringify(columnHide);
            console.log(columnhid);
            this.mycmservice.sendwithoutpdfParams(projectname, reportid, multiselectvalues, groupfield, columnproperty, title, stl, username, reportHeaderFooter, columnhid,multitenant).subscribe(responseData => {
                console.log(responseData);
                let htmldata = responseData.text();

                cordova.plugins.pdf.htmlToPDF({
                        data: htmldata,
                        documentSize: "A4",
                        landscape: 'portrait',
                        type: "share"
                    },
                    (sucess) => console.log('sucess: ', sucess),
                    (error) => console.log('error:', error));


            })
        } else {
            let projectname = this.subtitles.proj;
            let reportid = this.subtitles.tit;
            let multiselectvalues = "[]";
            let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
            let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
            let title = this.subtitles.tit;
            let stl = "[]";
            let multitenant=this.multitenant;
            let username = this.UserDetails["first_name"];
            let reportHeaderFooter = this.reportHeaderFooter;
            let columnhidden = this.subtitles.reportfield_meta;
            console.log(columnhidden);
            let columnHide = [];
            for (var col = 0; col < columnhidden.length; col++) {
                if (columnhidden[col].ih == "True") {


                    columnHide.push(columnhidden[col].sl);
                }
            }

            let columnhid = JSON.stringify(columnHide);
            console.log(columnhid);
            this.mycmservice.sendpdfParams(title, stl, username, reportHeaderFooter, columnhid,multitenant).subscribe(responseData => {
                console.log(responseData);
                let htmldata = responseData.text();

                cordova.plugins.pdf.htmlToPDF({
                        data: htmldata,
                        documentSize: "A4",
                        landscape: 'portrait',
                        type: "share"
                    },
                    (sucess) => console.log('sucess: ', sucess),
                    (error) => console.log('error:', error));


            })

        }
    }
    csv() {
        let para = JSON.stringify(this.subtitles.reportparamfield_meta);
        console.log(para);
        let paraObj = JSON.parse(para);
        if (paraObj == 0) {
            let projectname = this.subtitles.proj;
            let reportid = this.subtitles.tit;
            let multiselectvalues = "[]";
            let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
            let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
            let title = this.subtitles.tit;
            let stl = "[]";
            let multitenant=this.multitenant;
            let username = this.UserDetails["first_name"];
            let reportHeaderFooter = this.reportHeaderFooter;
            let columnhidden = this.subtitles.reportfield_meta;
            console.log(columnhidden);
            let columnHide = [];
            for (var col = 0; col < columnhidden.length; col++) {
                if (columnhidden[col].ih == "True") {


                    columnHide.push(columnhidden[col].sl);
                }
            }

            let columnhid = JSON.stringify(columnHide);
            console.log(columnhid);
            this.mycmservice.csvFormatwithoutparam(projectname, reportid, multiselectvalues, groupfield, columnproperty, title, stl, username, reportHeaderFooter, columnhid,multitenant).subscribe(responseData => {
                console.log(responseData);

            })
        } else {
            let csvdata: any;
            const fileTransfer: FileTransferObject = this.transfer.create();
            let projectname = this.subtitles.proj;
            let reportid = this.subtitles.tit;
            let multiselectvalues = "[]";
            let groupfield = JSON.stringify(this.subtitles.repgrouping_meta);
            let columnproperty = JSON.stringify(this.subtitles.reportfield_meta);
            let title = this.subtitles.tit;
            let stl = "[]";
            let multitenant=this.multitenant;
            let username = this.UserDetails["first_name"];
            let reportHeaderFooter = this.reportHeaderFooter;
            let columnhidden = this.subtitles.reportfield_meta;
            console.log(columnhidden);
            let columnHide = [];
            for (var col = 0; col < columnhidden.length; col++) {
                if (columnhidden[col].ih == "True") {


                    columnHide.push(columnhidden[col].sl);
                }
            }

            let columnhid = JSON.stringify(columnHide);
            console.log(columnhid);
            this.mycmservice.csvFormatparam(projectname, reportid, multiselectvalues, groupfield, columnproperty, title, stl, username, reportHeaderFooter, columnhid,multitenant).subscribe(responseData => {
                //console.log(responseData);
                csvdata = responseData.text();
                console.log(csvdata);
                this.file.createFile(this.file.externalRootDirectory, this.subtitles.sl + ".csv", true)
                    .then(function(success) {
                        console.log(success);
                        console.log("successfully created");
                    }, function(error) {
                        console.log(error);
                    });

                this.file.writeExistingFile(this.file.externalRootDirectory, this.subtitles.sl + ".csv", csvdata)
                    .then(function(success) {
                        console.log(success);
                        console.log("successfully write");
                    }, function(error) {
                        console.log(error);
                    });


            })

        }
    }
    reporttbgrid(sql, columns) {
        let itm = [];
        let table = document.getElementsByName('reporttb')[0];
        let tbody = table.getElementsByTagName('tbody')[0];
        if (tbody.rows.length > 0) {
            for (let k = tbody.children.length; k > 0; k--) {
                //tbody.removeChild(tbody.children[k-1]);
                tbody.deleteRow(k - 1);
            }
        }
        let rowlength = tbody.rows.length;
        console.log(table);
        this.sqlite.create({
            name: 'data.db',
            location: 'default'
        }).then((db: SQLiteObject) => {

            db.executeSql(sql, {}).then((data) => {
                //console.log(JSON.stringify(data));
                if (data.rows.length > 0) {
                    for (let i = 0; i < data.rows.length; i++) {
                        let rowlength = tbody.rows.length;
                        //alert(data.rows.item(i).name);
                        itm.push(data.rows.item(i));
                        let rowdata = data.rows.item(i);
                        let newRow = tbody.insertRow(tbody.rows.length);
                        //let row = table["insertRow"](rowlength);
                        newRow.id = 'id' + rowlength;
                        for (let j = 0; j < columns.length; j++) {
                            let header = columns[j]['sl'];
                            console.log(rowdata[header]);
                            let newCell = newRow.insertCell(j);
                            // Append a text node to the cell
                            let newText = document.createTextNode(rowdata[header]);
                            newCell.appendChild(newText);
                        }

                    }
                }
                console.log(itm);

            }).catch(e => console.log(e));
        }).catch(e => console.log(e));

    }

    ionViewDidLoad() {
        console.log('ionViewDidLoad ReportdetailsPage');
    }

    epostlink() {
        let saveStatus;
        saveStatus = this.mycmservice.reportEpostSave(this.names, this.report_meta, this.UserDetails, this.otherService, this.navCtrl,this.selectedOptions);
    }

    add(event) {
        console.log(event);
        try {
            let required_id = event['currentTarget']['dataset']["inputid"];
            document.getElementById(required_id).setAttribute('name', required_id)
            let input = document.getElementsByName(required_id);
            let fieldValue = input[0]['children'][0]['value'];
            let parsedValue = parseInt(fieldValue);
            if (parsedValue <= 20) {
                let newvalue = parsedValue + 1;
                input[0]['children'][0]['value'] = newvalue;
            }
        } catch (err) {
            console.log(err);
        }

    }
    sub(event) {
        try {
            let required_id = event['currentTarget']['dataset']["inputid"];
            document.getElementById(required_id).setAttribute('name', required_id)
            let input = document.getElementsByName(required_id);
            let fieldValue = input[0]['children'][0]['value'];
            let parsedValue = parseInt(fieldValue);
            if (parsedValue > 0) {
                let newvalue = parsedValue - 1;
                input[0]['children'][0]['value'] = newvalue;
            }
        } catch (err) {}
    }

  dpreport_construction(response){
    this.reports = response.json();
    let reportfield = this.reports['reportData'];
    let datas = JSON.parse(reportfield);
    let id = datas['store']['fields'].indexOf('pname');
    this.column = datas['store']['data']['frame'];
    this.titles = datas['store']['fields'];
    let names = [];
    for (var i = 0; i < this.column.length; i++) {
      let values = {};
      for (var j = 0; j < this.titles.length; j++) {
        values[this.titles[j]] = (this.column[i][j]);
      }
      this.names.push(values);
	  this.report_result_array.push(values);
    }
    console.log(this.names);
    let imageid=this.names; 
    //console.log(imageid)  ;
    for (var k=0;k< imageid.length;k++){
            let objId=imageid[k].objectid;
            let imagetable = imageid[k].imagetable;
            //console.log(objId);
            console.log(objId,imagetable);
        this.getImageById(objId,imagetable); 
            } 
  }
  graphreport_construction(responseData){
    this.reports = responseData.json();   
    let reportfield = this.reports['reportData'];    
    let datas =JSON.parse(reportfield);
    console.log(datas);
    let id =datas['store']['fields'].indexOf('pname');
    this.column=datas['store']['data']['frame'];
    console.log(this.column);
    this.titles = datas['store']['fields'];
    console.log(this.titles);     
    //this.Labels = this.titles;
    let xaxis=this.subtitles.xcoord;
    let xaxis_index = this.titles.findIndex(item =>{
        return (item == xaxis);
    });
    let yaxis=this.subtitles.ycoord;   
    let yaxis_index = this.titles.findIndex(item =>{
        return (item == yaxis);
    });
    let datass =[];
    let names=[];
    for(var j=0;j< this.titles.length; j++){
        let xaxis=(this.subtitles.xcoord);                                
        if(xaxis==this.titles[j]){
            for (var i = 0; i < this.column.length; i++) {                                    
                 let labels={};
                 labels=this.column[i][xaxis_index];
                 this.names.push(labels);
        }                                
                
            }
            if(yaxis==this.titles[j]){
                for (var k = 0; k < this.column.length; k++) {
                        let values = {};                                         	                               
                         values =this.column[k][yaxis_index];                                
                         this.datass.push(values);
                        //for(var s=0;s< this.titles.length; s++){ //}
            }
        }
    }
    //let chartType=this.subtitles.gtype
    //if(chartType =="bar"){                      
        this.Labels=this.names;
        console.log( this.Labels);
        //this.Options[0].scales.yAxes.ticks.beginAtZero=true
               
        this.Data[0].label =yaxis;
        this.Data[0].data = this.datass;
        //this.barChartData[0].data = this.datass;
        console.log( "barChartData");                        
       // }
        // else if(chartType =="pie")
        //     {                      
        //     this.Labels=this.names;
        //     console.log( this.Labels);
        //     //this.Data[0].label =yaxis;
        //     this.Data[0].data = this.datass;
        //     //this.barChartData[0].data = this.datass;
        //     console.log( "barChartData");                        
        //     }
    // else (chartType =="line")
    //        {                      
    //             this.Labels=this.names;
    //             console.log( this.Labels);
    //             this.Data[0].label =yaxis;
    //             this.Data[0].data = this.datass;
    //             //this.barChartData[0].data = this.datass;
    //             console.log( "barChartData");                        
    //         }    
}

checkfocus(event){
    this.selectId = event._elementRef.nativeElement.id;
}
checkchange(event)
{
	console.log(event);
	this.selectedOptions[this.selectId] = event;
}

newEntry($event){
    console.log(event);
    let exp = "";
    try{
        exp = $event.currentTarget.dataset.exp;
    }
    catch (e){
        exp = "";
    }
    if(exp){
        if(exp.includes("viewtxn")){
            let txnViewpage;
            let transacionview = exp.substring(
                exp.lastIndexOf("(") + 1, 
                exp.lastIndexOf(")")
            );
            for (let i=0;i<this.otherService['pages'].length;i++){
                if(this.otherService['pages'][i]['id'] == transacionview){
                    txnViewpage = this.otherService['pages'][i]['component'];

                }

            }
            this.navCtrl.push(txnViewpage).then(() => {
                const startIndex = this.navCtrl.getActive().index - 1;
                this.navCtrl.remove(startIndex, 1);
            });


        }

    }

}

getImageById(objId,imagetable){
    let imagedata: SafeResourceUrl;
    let path = this.resturl+'/mobileserviceapi/getImageId/'+imagetable+'/'+objId
         this.http.get(path).subscribe(responseData =>  {
                console.log(responseData); 
                var imageData =responseData.text();
                   var imagedata =this.photo_url(imageData);
                   ////this._sanitizer.bypassSecurityTrustResourceUrl("data:Image;base64,"+this.//imageData);          
            })
    
    }
     public image: SafeResourceUrl;
    photo_url(imageData: string){
       
       this.image = this._sanitizer.bypassSecurityTrustResourceUrl("data:Image;base64,"+imageData); 
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


  pay(event) {
	  console.log(event);
	  let expression;
	  for(let i =0;i<this.report_meta['repaction_meta'].length;i++){
		  if(this.report_meta['repaction_meta'][i]["at"] == 'payment'){
			  expression = this.report_meta['repaction_meta'][i]["Payconfig"]["exp"];
		  }
	  }
	  let fun = this;
	  let payment ={};
	  let amount = this.report_result_array[0][event.AMOUNT];
	  var amount_value = amount*100;
	  let paymentId;
    var options = {
      description: 'Auvit',
      image: 'https://i.imgur.com/3g7nmJC.png',
      currency: 'INR',
      key: 'rzp_test_AXW4kUkDymcZJ1',
      name: 'Auvit',
	  method: 'card',	
	   external: {
	   },
      prefill: {
        email: this.UserDetails['EMAIL'],
        contact: this.UserDetails['MOBILENUMBER'],
        name: this.UserDetails['USERNAME']
      },
      theme: {
        color: "#8080ff"
      },
      modal: {
        ondismiss: function() {
          alert('dismissed')
        }
      }
    };
	  options["amount"] = amount_value.toFixed(2);
	  payment['customer_email'] = this.UserDetails['EMAIL'];
	  payment['amount'] = amount.toFixed(2);
	  payment['description'] = options['description'];
	  payment['order_no'] = this.report_result_array[0][event.ORDERNO];
	  

    var successCallback = function(payment_id) {
      //alert('payment_id: ' + payment_id);
		paymentId = payment_id;
		console.log(payment_id);
		payment['payment_id'] = paymentId;
		payment['razor_pay_id'] = paymentId;
		payment['payment_status'] = 'paid';
		fun.mycmservice.savePaymentstatus(payment,fun.UserDetails,fun.otherService, fun.navCtrl,expression);
		alert('Payment Made Successfully')
    };


    var cancelCallback = function(error) {
     alert(error.description + ' (Error ' + error.code + ')');
		console.log(error);
		console.log(error.description);
		payment['payment_id'] = "";
		payment['razor_pay_id'] = "";
		payment['payment_status'] = 'not paid';
		fun.mycmservice.savePaymentstatus(payment,fun.UserDetails,fun.otherService, fun.navCtrl,expression);
		alert('Payment Failed.Please Retry!');
		
    };

    RazorpayCheckout.open(options, successCallback, cancelCallback);
  }

    reportButtonOnClick($event){
        debugger;
        console.log(event);
      

        let reportExp = event.currentTarget['dataset']['exp'];
        if(reportExp.includes("viewtxn") || reportExp.includes("viewreport")){
            let txnViewpage;
            let transacionview = reportExp.substring(
                reportExp.lastIndexOf("(") + 1, 
                reportExp.lastIndexOf(")")
            );
            for (let i=0;i<this.otherService.pages.length;i++){
                if(this.otherService.pages[i]['id'] == transacionview){
                    txnViewpage = this.otherService.pages[i]['component'];

                }

            }
            this.navCtrl.push(txnViewpage).then(() => {
                const startIndex = this.navCtrl.getActive().index - 1;
                this.navCtrl.remove(startIndex, 1);
            });


        }
    }

    printReport($event){
        debugger;
        console.log(event);
        let headers = [];
        let reportType = ""
        try{
            headers = JSON.parse(event.currentTarget['dataset']['tableheaders']);
        }
        catch(err){
            headers = [];
        }
        try{
            reportType = event.currentTarget['dataset']['reporttype'];
        }
        catch(err){
            reportType = "";
        }
            
        let mustacheJson = {};
        let rowIndex = event.currentTarget['parentElement']['parentElement']['rowIndex'];
        let mapValue = {};
        
        let actions = this.subtitles["repaction_meta"]; //Actions of report
        for(let i =0;i<actions.length;i++){
            if(actions[i]["at"] == "print_format"){
                let pfActionObj = actions[i]["ReportPrintFormatAction"]["pfc"]; //PF Action Object
                console.log(pfActionObj);
                if (pfActionObj){
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
                            if(reportType == "displayreport"){
                                for(let k=0;k<found.length;k++){
                                    mapValue[found[k]] = this.report_result_array[0][found[k]];
                                }
                            }
                            else{
                                for(let k=0;k<found.length;k++){
                                    let columnindex = headers.indexOf(found[k]);
                                    mapValue[found[k]] = this.titles[rowIndex][columnindex]
                                    
                                }
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
                                    this.http.get('assets/mustache/report.html').map(res => res.text()).subscribe(html => {
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
                                        }
                                        else if (sqlArray[j]["st"] == "Grid"){
                                            mustacheJson[sqlArray[j]["do"]] = resJson;
                                        }
                                    }
                                    

                                    if(j==sqlArray.length-1){
                                        this.http.get('assets/mustache/report.html').map(res => res.text()).subscribe(html => {
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

    checkBlur(event) {
        let id = event._elementRef.nativeElement.dataset["id"];
        this.next_hiddenelements(id);

    }  
    
    checkChange($event, elemtId) {
        this.next_hiddenelements(elemtId);
    }
    onFocus(event) {
        let elelmentId = event._elementRef.nativeElement.dataset["id"];
        let DOM = document.getElementsByName(elelmentId);
        try {
            this.UserDetails['pagetype'] = 'txview';
            this.myexpression.evaluateExp(event, DOM, this.UserDetails,this.preset_value);
        }
        catch(e){
        
        }
        
    }

    next_hiddenelements(id){
        let nextHiddenComponents: any[] = [];
		let elementIdList = [];
        let formid = this.rptName+"paramForm";
        let elements = document.getElementById(formid).querySelectorAll('*[name]');
        
        for (let i = 0; i < elements.length; i++) {
            if (elements[i].id != "") {
                elementIdList.push(elements[i].id);
            }
        }
        var unique = elementIdList.filter(function(elem, index, self) {
            return index === self.indexOf(elem);
        })
        var remainigArray  = unique.slice((unique.indexOf(id)+1),(unique.length+1));
       
        for (let i of remainigArray) {
            if (document.getElementById(i).dataset.hidden == "True") {
                nextHiddenComponents.push(i);
            }
            else{
                break;
            }
        }

        if ((nextHiddenComponents.length) != 0) {
            this.myexpression.hiddenElementexp(nextHiddenComponents, this.UserDetails,this.preset_value,this.selectedOptions,"report",this,false);
        }

    }

}