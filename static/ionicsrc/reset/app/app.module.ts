import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';

import { MyApp } from './app.component';
import { HomePage } from '../pages/home/home';
import { TxserviceProvider } from '../providers/txservice/txservice';
import { LoginserviceProvider } from '../providers/loginservice/loginservice';
import { SingletonProvider } from '../providers/singleton/singleton';
import { ExpressionProvider } from '../providers/expression/expression';
import { CmserviceProvider } from '../providers/cmservice/cmservice';
import { NotifyProvider } from '../providers/notify/notify';
import { PagenavProvider } from '../providers/pagenav/pagenav';

@NgModule({
  declarations: [
    MyApp,
    HomePage
  ],
  imports: [
    BrowserModule,
    IonicModule.forRoot(MyApp)
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    TxserviceProvider,
    LoginserviceProvider,
    SingletonProvider,
    ExpressionProvider,
    CmserviceProvider,
    NotifyProvider,
    PagenavProvider
  ]
})
export class AppModule {}
