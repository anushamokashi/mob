import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Storage } from '@ionic/storage';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { LoginserviceProvider } from '../../providers/loginservice/loginservice';
import 'rxjs/add/operator/map';
declare var Expression:any;
/*
  Generated class for the ExpressionProvider provider.

  See https://angular.io/docs/ts/latest/guide/dependency-injection.html
  for more info on providers and Angular DI.
*/
@Injectable()
export class ExpressionProvider {
  stValues:any;
  constructor(public http: Http,public storage: Storage,public myservice: LoginserviceProvider,public singleton: SingletonProvider) {
    console.log('Hello ExpressionProvider Provider');
  }

	hiddenElementexp(components,UserDetails,preset_value,selectedOptions,type,thisCallbk,isAllHidden){

        let datasetForHiddenComp : any;
        if(components.length>0){
            let component = components[0]
            let nextElement = document.getElementsByName(component);
            datasetForHiddenComp = document.getElementById(component);
            
            //CHECK FOR SQL 
            if (datasetForHiddenComp.dataset.sql == "" || datasetForHiddenComp.dataset.sql == "None" || datasetForHiddenComp.dataset.sql == undefined){

                //call service for sql
                var sql = datasetForHiddenComp.dataset.sql;
                let mapValue = {};
                let finalSql = "";
                let paramStr = this.findParamValues(sql,preset_value);
                
                let data  = {
                    fieldType : "combofield",
                    eFormId : datasetForHiddenComp.dataset.eformid,
                    fieldName : datasetForHiddenComp.dataset.fieldname,
                    type : type,
                    projectName : this.singleton.projectname,
                    projectId : this.singleton.PID,
                    username : UserDetails["USERNAME"],
                    MapValue : paramStr,
                
                };
                console.log(data); 

                this.myservice.hiddenSqlService(data).subscribe(loginData => {
                    let responseOfSqlArray = loginData.json();

                    if (responseOfSqlArray){
                        let responseOfSql = responseOfSqlArray[0];
                        console.log(responseOfSql);
                        // document.getElementById(component).getElementsByTagName("input")[0].value = responseOfSql;
                        if(datasetForHiddenComp.dataset.widgettype == "check" ||datasetForHiddenComp.dataset.widgettype == "select" || datasetForHiddenComp.dataset.widgettype == "radio" ){
                            selectedOptions[component] = responseOfSql[datasetForHiddenComp.dataset.sqlvalue];
                        }
                       
                        preset_value[component] = responseOfSql[datasetForHiddenComp.dataset.sqlvalue];
                        
                        
                        if(datasetForHiddenComp.dataset.componenttype == "OneToOneField"){
                            for(var key in responseOfSql){
                                let logicalFieldID = "logical_"+component+"_"+key;
                                preset_value[logicalFieldID] = responseOfSql[key];
                            
                
                            }

                        }
                        components.splice(0,1);
                        if(components.length > 0){
                            this.hiddenElementexp(components,UserDetails,preset_value,selectedOptions,type,thisCallbk,isAllHidden);
                        }
                        else{
                            if(type=="report" && isAllHidden == true){
                                thisCallbk.getreport();
                            }
                            
                        }

                    }
                });

                
            }

            //CHECK FOR EXP
            else if (datasetForHiddenComp.dataset.expression != ""){
                this.evaluateExp("",nextElement,UserDetails,preset_value);
                components.splice(0,1);
                if(components.length > 0){
                    this.hiddenElementexp(components,UserDetails,preset_value,selectedOptions,type,thisCallbk,isAllHidden);
                }
                else{
                    if(type=="report"){
                        thisCallbk.getreport();
                    }
                    
                }
            }

            //IF BOTH ARE NONE MIGHT BE A LOGICAL FIELD
            else if (datasetForHiddenComp.dataset.expression == "" && datasetForHiddenComp.dataset.sql == ""){
                components.splice(0,1);
                if(components.length > 0){
                    this.hiddenElementexp(components,UserDetails,preset_value,selectedOptions,type,thisCallbk,isAllHidden);
                }
                else{
                    if(type=="report"){
                        thisCallbk.getreport();
                    }
                    
                }

            }
        }
        
    }

    findParamValues(sql,preset_value){
        let paramStr = "";
        var found = [],          // an array to collect the strings that are found
            rxp = /\:(\w+)/g,
            str = sql,
            curMatch;

        while( curMatch = rxp.exec( str ) ) {
            found.push( curMatch[1] );
        }
        console.log(found);

        //Creating JSON Object
        if(found.length>0){
            for(let k=0;k<found.length;k++){
                // mapValue[found[k]] = preset_value[found[k]]
                paramStr += "&"+found[k]+"="+preset_value[found[k]];
                
            }

        }
        return paramStr;
    }

	evaluateExp(event,document,stValues,preset_value){
		//let ptexpression;
        //this.requiredValue = "";
        let id = "";
		let modeofEntry="";
		let onChangevalue ="";
		//let  expressionValue ="";
        //let expProceed;
        let GetVal;
        //console.log(event);
        //console.log("focusIn");
        //let expression =event.currentTarget.dataset["expression"];
        let expression = document[0].dataset["expression"];
        let suggestive = document[0].dataset["suggestive"];
        let eformid =  document[0].dataset["eformid"];
        id = document[0].dataset["id"];
		modeofEntry = document[0].dataset["modeofentry"];
		stValues['preset_value'] = preset_value;
        //id = event.currentTarget.dataset["id"];
        //let value = Expression(expression);
        if (expression) {
			if (suggestive =="False" || document != undefined || event._text =="" || modeofEntry =='tbc'){	
            let ExprObj = new Expression("");
            ExprObj.Expression(expression, stValues, eformid, "");
            GetVal = ExprObj.Evaluate();
			 if(GetVal == 'AUTOGENERATE'){
				 let prefix = id.substring(0, 3).toUpperCase();
				 let uniqueId = new Date().valueOf().toString();
				 GetVal = prefix+uniqueId;
			 }
            console.log(GetVal);	
				//fieldValue = document.getElementsByName(id);
            //this.requiredValue = this.myexpression.evaluateExpression(ptexpression,event);
			if (document[0].tagName == "ION-INPUT" || document[0].tagName =="ION-TEXTAREA")
			{
				preset_value[id] = GetVal;
				if(event){
				event._value = GetVal;
				event['_native']['nativeElement']['value'] = GetVal;
				
			   event['_native']["nativeElement"].onblur = function() {
                {
					onChangevalue = preset_value[id];
					
				    if(modeofEntry == 'tbe' && suggestive =="False"){
					preset_value[id] ='';	
					preset_value[id] = onChangevalue ;
					}
					else if(modeofEntry == 'tbc')
					{
					//let tbcValue = document.getElementsByName(id);
					if(onChangevalue == ""){	
					preset_value[id] ="";	
                    preset_value[id] = GetVal;	
					}
					else if(onChangevalue)
					 {
					preset_value[id] ="";	
                    preset_value[id] = GetVal;	
					}
					}
            }
        } 	
				}
			}
			else if(document[0].tagName =="ION-DATETIME")
			{
				//event._picker._ts = 1507552371000;
				if (event.displayFormat =="HH:mm"){
				var time = new Date(GetVal).toLocaleTimeString('en-GB', { hour: "numeric", 
                                             minute: "numeric"});
				event._text = time;
				event._value["hour"] = GetVal.getHours();
				event._value["minute"] = GetVal.getMinutes();
				event._picker.data.columns[0].selectedIndex = GetVal.getHours();
				event._picker.data.columns[1].selectedIndex = GetVal.getMinutes();
				}
				else if(event.displayFormat =="MM/DD/YYYY"){
					preset_value[id] = GetVal;
				}
				else{
					preset_value[id] = GetVal;
				}
				//document.getElementsByName(id)[0].onblur = function() {
          
				//alert("hi");
           // }
				
				//document.getElementsByName('empjoindate')[0].onchange = function(){
				//alert("hi");
				//};
			}
				
            //fieldValue[1].value = GetVal;
			
        }
        }
   
	}

    evaluateEventexp(elementEvent,stValues,eformid){
        if(this.singleton.ismultitenant == "True"){
			stValues["RESTURL"] = this.singleton.dynamicresturl;
		}
		else if(this.singleton.ismultitenant == "False"){
			stValues["RESTURL"] = this.singleton.resturl;

		}
        
        stValues["PROJECTID"] = this.singleton.PID;
        stValues["PROJECTNAME"] = this.singleton.projectname;
        stValues["ISMULTITENANT"] = this.singleton.ismultitenant;
        let ExprObj = new Expression("");
        ExprObj.Expression(elementEvent, stValues, eformid, "");
        let GetVal = ExprObj.Evaluate();
        console.log(GetVal)
        return GetVal ;	  

    }
	
}
