import { Http } from '@angular/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the PagenavProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class PagenavProvider {

  constructor(public http: Http) {
    console.log('Hello PagenavProvider Provider');
  }

}
