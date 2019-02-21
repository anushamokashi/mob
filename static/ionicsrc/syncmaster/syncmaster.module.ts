import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { SyncmasterPage } from './syncmaster';

@NgModule({
  declarations: [
    SyncmasterPage,
  ],
  imports: [
    IonicPageModule.forChild(SyncmasterPage),
  ],
})
export class SyncmasterPageModule {}
