import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';

import { TxserviceProvider } from '../../providers/txservice/txservice';
import { SingletonProvider } from '../../providers/singleton/singleton';
import { LoginPage } from '../login/login';

/**
 * Generated class for the RegistrationPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-registration',
  templateUrl: 'registration.html',
  providers:[TxserviceProvider],
})
export class RegistrationPage {

  constructor(public navCtrl: NavController, public navParams: NavParams, public mytxservice: TxserviceProvider,public singleton: SingletonProvider) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad RegistrationPage');
  }
  onFocus(event){
    console.log(event);
    let id = event._elementRef.nativeElement.id;
    if (event._type == 'password'){
      document.getElementById("message").hidden = false;
    } 
    else{ 
      document.getElementsByName(id+'er')[0].textContent =""; 
    }
	 
  }
  
  checkBlur(event){
    console.log(event);
    let id = event._elementRef.nativeElement.id;
    
    if(event._type == 'text'){
      if(event._value == ""){
        document.getElementsByName(id+'er')[0].textContent ="This field is required";
      }
    }
    
    else if(event._type == 'email'){
      if(event._value == ""){
        document.getElementsByName(id+'er')[0].textContent ="This field is required";
      }
      else{
        this.ValidateEmail(event._value,id);
      }	 
    }
    
    else if(event._type == 'number'){
      if(event._value == ""){
        document.getElementsByName(id+'er')[0].textContent ="This field is required";
      }
      else{
        this.mobileno(event._value,id);
      }	 	  
    }
	  
    else if(event._type == 'password'){
      if(event._value == ""){
        document.getElementsByName(id+'er')[0].textContent ="This field is required";
      }	 
      else{
        if(id == 'confirmpassword'){
          this.matchPassword(event._value,'pswd',id);
        }
        else{ 
          this.CheckPassword(event._value,id);
        }
      }	 		  
    } 	
  }
  
  ValidateEmail(mail,id){  
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)){  
      return (true)  
    }  
    document.getElementsByName(id+'er')[0].textContent ="Email Entered is incorrect";
    return (false)  
  } 
  
  mobileno(inputtxt,id){
    if (/^\d{10}$/.test(inputtxt)){
      return true; 
    }	
    document.getElementsByName(id+'er')[0].textContent ="enter correct contact number";
    return false;
  }
  
  CheckPassword(inputtxt,id){   
	  let lowerCaseLetters = /[a-z]/g;
	  if(inputtxt.match(lowerCaseLetters)){  
    
    }else{
      document.getElementsByName(id+'er')[0].textContent ="Please follow instruction";
	  }

    // Validate capital letters
    let upperCaseLetters = /[A-Z]/g;
    if(inputtxt.match(upperCaseLetters)) {  
    
    }else{
      document.getElementsByName(id+'er')[0].textContent ="Please follow instruction";
    }

    // Validate numbers
    let numbers = /[0-9]/g;
    if(inputtxt.match(numbers)) {  
    
    }else{
      document.getElementsByName(id+'er')[0].textContent ="Please follow instruction";
    }
  
    // Validate length
    if(inputtxt.length >= 8) {
    
    }else{
      document.getElementsByName(id+'er')[0].textContent ="Please follow instruction";
    }
  } 
  
  matchPassword(confirminput,passid,id){
    let password : any;
    try{
      password = document.getElementById(id).getElementsByTagName("input")[0].value;
    }
    catch(e){
      password = ""; 
    }
    if (confirminput != password )	{
      document.getElementsByName(id+'er')[0].textContent ="Password does not match";
    }
	}
  
  checkChange(event,elemtId) {

  }

  checkClick(event){
    let saveStatus;
    let UserDetails = {
      "PROJECTID":this.singleton.PID,
      "USERID":"",
      "USERNAME":"",
      "PAGE" : "RegistrationPage",
    };
    saveStatus = this.mytxservice.saveJson(UserDetails);
    console.log(saveStatus)
    if (saveStatus == "TRUE") {

        this.navCtrl.setRoot(LoginPage);
    }
  }

  Login(){
    this.navCtrl.setRoot(LoginPage);
  }
}
